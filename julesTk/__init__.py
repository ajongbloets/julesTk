"""Some basic classes"""

from threading import RLock

import six
import sys
import functools
if sys.version_info[0] < 3:
    import Tkinter as tk
    import ttk
else:
    import tkinter as tk
    from tkinter import ttk

__author__ = "Joeri Jongbloets <joeri@jongbloets.net>"
__all__ = [
    "JTkObject", "JTkException", "receives", "triggers", "thread_safe", "tk", "ttk"
]


class JTkMeta(type):
    """A meta object"""

    @staticmethod
    def __new__(mcs, name, bases=None, attrs=None):
        if bases is None:
            bases = []
        if attrs is None:
            attrs = {}
        result = super(JTkMeta, mcs).__new__(mcs, name, bases, attrs)
        # setattr(result, "class_event_hooks", class_event_hooks)
        # setattr(result, "class_event_slots", class_event_slots)
        # class_event_hooks = set()
        # # add base hooks
        # direct_bases = mcs.filterDistantBases(name, bases)
        # for base in direct_bases:
        #     if isinstance(base, JTkMeta):
        #         class_event_hooks = class_event_hooks.union(base.class_event_hooks)
        # for attr_name, attr in attrs.items():
        #     if hasattr(attr, "_hook"):
        #         class_event_hooks = mcs._registerHook(attr, class_event_hooks)
        # setattr(result, "class_event_hooks", class_event_hooks)
        # class_event_slots = mcs._mergeSlots(direct_bases)
        # for attr_name, attr in attrs.items():
        #     if hasattr(attr, "_slot"):
        #         class_event_slots = mcs._registerSlot(attr, class_event_slots)
        # setattr(result, "class_event_slots", class_event_slots)
        return result

    def __init__(cls, name, bases=None, attrs=None):
        class_event_hooks = set()
        class_event_slots = {}
        attributes = filter(lambda a: hasattr(cls, a), dir(cls))
        # find event hooks and slots
        for name in attributes:
            attr = getattr(cls, name)
            if hasattr(attr, "_hook"):
                hook = getattr(attr, "_hook")
                class_event_hooks.add(hook)
            elif hasattr(attr, "_slot"):
                slot = getattr(attr, "_slot")
                if slot not in class_event_slots.keys():
                    class_event_slots[slot] = {attr}
                else:
                    class_event_slots[slot].add(attr)
        cls.class_event_hooks = class_event_hooks
        cls.class_event_slots = class_event_slots
        super(JTkMeta, cls).__init__(name, bases, attrs)


@six.add_metaclass(JTkMeta)
class JTkObject(object):
    """A julesTk object; comes with a event-driven communication system"""

    def __init__(self):
        super(JTkObject, self).__init__()
        self._lock = RLock()
        # names of the events being raised by this class
        self._event_hooks = self.class_event_hooks.copy()
        """:type: set[str]"""
        # functions being called when a event is received by this class
        import copy
        self._event_slots = copy.deepcopy(self.class_event_slots)
        """:type: dict[str, set[callable | julesTk.JTkObject]]"""
        # update with class event slots
        # register observers
        self._event_observers = set()

    def __del__(self):
        # check if we passed __init__
        if hasattr(self, "_event_observers"):
            while len(self._event_observers) > 0:
                observer = next(iter(self._event_observers))
                self.remove_observer(observer)
                if isinstance(observer, JTkObject):
                    observer.remove_observer(self)

    @property
    def lock(self):
        """Retrieve the lock of this object"""
        return self._lock

    def get_event_hooks(self):
        """List the names of the event hooks provided by this class"""
        return self._event_hooks

    @property
    def event_hooks(self):
        return self.get_event_hooks()

    def has_event_hook(self, name):
        return name in self.get_event_hooks()

    def get_event_slots(self):
        """List the names of the event slots implemented by this class"""
        return self._event_slots.keys()

    @property
    def event_slots(self):
        return self.get_event_slots()

    def has_event_slot(self, name):
        return name in self.get_event_slots()

    def add_event_slot(self, name, handler):
        if not callable(handler) and not isinstance(handler, JTkObject):
            raise ValueError("Invalid handler")
        if name in self._event_slots.keys():
            self._event_slots[name].add(handler)
        else:
            self._event_slots[name] = {handler}

    def add_observer(self, observer):
        """Register an `observer` to receive events raised by this class

        Whenever the event is triggered by the class, it will call all observers registered to that event
        """
        result = False
        if not callable(observer) and not isinstance(observer, JTkObject):
            raise TypeError("Expected a callable or julesTk2.core.JTkObject")
        if observer not in self._event_observers:
            self._event_observers.add(observer)
            result = True
        return result

    def remove_observer(self, observer):
        """Remove `observer` from being called when `event` is raised by this class"""
        result = False
        if not callable(observer) and not isinstance(observer, JTkObject):
            raise TypeError("Expected a callable or julesTk2.core.JTkObject")
        if observer in self._event_observers:
            self._event_observers.remove(observer)
            result = True
        return result

    def trigger_event(self, event, data=None):
        """Triggers an event"""
        for observer in self._event_observers:
            if isinstance(observer, JTkObject):
                observer.receive_event(event, self, data)
            elif callable(observer):
                observer(event, self, data)

    def receive_event(self, event, source, data=None):
        """Receives an event and relays it to the appropriate slot"""
        if event in self._event_slots.keys():
            handlers = self._event_slots[event]
            for handler in handlers:
                if callable(handler):
                    try:
                        import inspect
                        if 'self' in inspect.getargspec(handler).args:
                            handler(self, event, source, data)
                        else:
                            handler(event, source, data)
                    except TypeError as te:
                        pass


def thread_safe(f):
    """A decorator for making methods thread-safe"""
    @functools.wraps(f)
    def magic(self, *args, **kwargs):
        try:
            self.lock.acquire()
            result = f(self, *args, **kwargs)
        finally:
            self.lock.release()
        return result
    return magic


def triggers(name=None, before=False):
    """A decorator for triggering an event after the method was called"""
    def decorator(f):
        hook_name = f.__name__
        if name is not None:
            hook_name = name
        f._hook = hook_name

        @functools.wraps(f)
        def magic(self, *args, **kwargs):
            result = None
            if before:
                self.trigger_event(hook_name, result)
            try:
                result = f(self, *args, **kwargs)
            finally:
                if not before:
                    self.trigger_event(hook_name, result)
            return result
        return magic
    return decorator


def receives(name=None):
    """A decorator for connecting a method to an event handler"""
    def decorator(f):
        hook_name = f.__name__
        if name is not None:
            hook_name = name
        f._slot = hook_name

        return f
    return decorator


class JTkException(BaseException):
    """A simple exception with the option to add messages"""

    def __init__(self, msg=None):
        if msg is None:
            self._msg = self.__class__.__name__
        self._msg = msg

    def __str__(self):
        return self._msg
