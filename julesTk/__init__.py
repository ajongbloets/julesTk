"""Some basic classes"""

from threading import RLock

import sys
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk
import ttk
import functools

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
        @functools.wraps(f)
        def magic(self, *args, **kwargs):
            try:
                self.lock.acquire()
                result = f(self, *args, **kwargs)
            finally:
                self.lock.release()
            return result
        return magic

    thread_safe = staticmethod(thread_safe)
