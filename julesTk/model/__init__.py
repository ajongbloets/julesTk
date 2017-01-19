"""Model classes"""

from julesTk import Observable, ThreadSafeObject

__author__ = "Joeri Jongbloets <joeri@jongbloets.net>"


class Model(Observable, ThreadSafeObject):

    def __init__(self):
        super(Model, self).__init__()
        self._data = None

    @property
    def data(self):
        with self.lock:
            result = self._data
        return result

    def update(self):
        """Request the model to update it self"""
        raise NotImplementedError
