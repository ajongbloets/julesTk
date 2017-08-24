
from __future__ import absolute_import
from . import Model, receives, triggers
import random


class RandomModel(Model):

    def __init__(self, mean=0, std=1):
        super(RandomModel, self).__init__()
        self._mean = mean
        self._std = std
        self.reset()

    @property
    def mean(self):
        with self.lock:
            result = self._mean
        return result

    @property
    def std(self):
        with self.lock:
            result = self._std
        return result

    @triggers("model_reset")
    def reset(self):
        with self.lock:
            self._data = []

    def generate(self):
        return random.gauss(self.mean, self.std)

    @triggers("model_update")
    def update(self):
        with self.lock:
            self._data.append(self.generate())
