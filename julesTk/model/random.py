
from __future__ import absolute_import
from . import Model
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

    @Model.observed
    def reset(self):
        with self.lock:
            self._data = []

    def generate(self):
        return random.gauss(self.mean, self.std)

    @Model.observed
    def update(self):
        with self.lock:
            self._data.append(self.generate())
