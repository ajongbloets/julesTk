"""Some basic classes"""

from threading import RLock

import sys
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk
import ttk

__author__ = "Joeri Jongbloets <joeri@jongbloets.net>"


class JulesException(BaseException):
    """A simple exception with the option to add messages"""

    def __init__(self, msg=None):
        if msg is None:
            self._msg = self.__class__.__name__
        self._msg = msg

    def __str__(self):
        return self._msg


class ThreadSafeObject(object):
    """A class providing infrastructure for creating thread-safe objects"""

    def __init__(self):
        super(ThreadSafeObject, self).__init__()
        self._lock = RLock()

    @property
    def lock(self):
        """Retrieve the lock of this object"""
        return self._lock

    def thread_safe(f):
        """A decorator for making methods thread-safe"""
        def magic(self, *args, **kwargs):
            with self.lock:
                result = f(self, *args, **kwargs)
            return result
        return magic

    thread_safe = staticmethod(thread_safe)


class Observable(object):
    """An Observable will update it's observers whenever it is changed

    Place the `observed` decorator

    """

    def __init__(self):
        super(Observable, self).__init__()
        self._observers = []

    def register_observer(self, observer):
        """Register an observer to get notified when this object is changed.

        Will only add the observer if it is not already observing.

        :param observer: The observer that should be notified
        :type observer: julesTk.Observer
        """
        if observer not in self._observers:
            self._observers.append(observer)

    def notify_observers(self):
        """Notifies all observing observers about that something changed in this object"""
        for observer in self._observers:
            observer.update(self)

    def observed(f):
        """Decorator that will automatically call notify_observers after executing this method

        :type f: callable
        """
        def magic(self, *args, **kwargs):
            result = f(self, *args, **kwargs)
            self.notify_observers()
            return result
        return magic

    observed = staticmethod(observed)


class Observer(object):
    """Object able to observe observable objects"""

    def __init__(self):
        super(Observer, self).__init__()

    def update(self, observable):
        """Handle a update notification from an object that is being observed by this object.

        :param observable: Object that sent the notification
        :type observable: julesTk.Observable
        """
        raise NotImplementedError

