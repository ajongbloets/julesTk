"""Model classes"""

from julesTk import *

__author__ = "Joeri Jongbloets <joeri@jongbloets.net>"


class Model(JTkObject):
    """Thread-Safe"""

    def __init__(self):
        super(Model, self).__init__()
        self._data = None

    @property
    def data(self):
        """RAW Representation of the data contained in the model"""
        with self.lock:
            result = self._data
        return result

    @triggers("model_update")
    def update(self):
        """Request the model to update it self"""
        raise NotImplementedError

