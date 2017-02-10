"""Provides classes that help with creating Observer-Observable structures"""

import functools

__author__ = "Joeri Jongbloets <joeri@jongbloets.net>"


class Observable(object):
    """An Observable will update it's observers whenever it is changed

    Notification can be triggered in two ways:

    1. Call `notify_observers()` directly from a method, after data was updated
    2. Use `@observed` decorator for methods that should call `notify_observers` when finished

    Observers can register themselves using the `register_observer` method.
    Only 1 observer registration per object.

    """

    def __init__(self):
        # super prevents disruption of mro chain
        super(Observable, self).__init__()
        self._observers = []

    def register_observer(self, observer):
        """Register an observer to get notified when this object is changed.

        Will only add the observer if it is not already observing.

        :param observer: The observer that should be notified
        :type observer: julesTk.Observer
        """
        if not isinstance(observer, Observer):
            raise ValueError("Expected a Observer, not {}".format(type(observer)))
        if observer not in self._observers:
            self._observers.append(observer)

    def notify_observers(self):
        """Notifies all observing observers"""
        for observer in self._observers:
            observer.update(self)

    def observed(f):
        """Decorator that will automatically call notify_observers after executing this method

        :type f: callable
        """
        @functools.wraps(f)
        def magic(self, *args, **kwargs):
            result = f(self, *args, **kwargs)
            self.notify_observers()
            return result
        return magic

    observed = staticmethod(observed)


class Observer(object):
    """An observer for observing a observable

    Implement `update` to handle notifications
    """

    def __init__(self):
        super(Observer, self).__init__()

    def update(self, observable):
        """Handle a update notification from an object that is being observed by this object.

        :param observable: Object that sent the notification
        :type observable: julesTk.Observable
        """
        raise NotImplementedError
