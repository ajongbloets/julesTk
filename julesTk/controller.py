"""Provide Controller classes"""

from julesTk import Observer
from model import Model

__author__ = "Joeri Jongbloets <joeri@jongbloets.net>"


class Controller(Observer):

    def __init__(self, app, view=None, model=None):
        super(Controller, self).__init__()
        self._app = app
        # handle to the view (main responsible view)
        self._view = view
        # handle to the model
        self._model = model
        # register as observer
        if self.model is not None:
            self.model.register_observer(self)

    def __del__(self):
        self.stop()

    def setup(self):
        """Configures the controller (set-up model, view)"""
        raise NotImplementedError

    def start(self):
        raise NotImplementedError

    def stop(self):
        raise NotImplementedError

    def update(self, observable):
        raise NotImplementedError

    @property
    def application(self):
        """Return reference to the application object

        :rtype: julesTk.app.Application
        """
        return self._app

    @property
    def view(self):
        """Return the view

        :rtype: julesTk.view.View
        """
        return self._view

    @property
    def model(self):
        """Return the model

        """
        return self._model

    @model.setter
    def model(self, model):
        if model is not None and not isinstance(model, Model):
            raise ValueError("Invalid model")
        self._model = model
        # register as observer
        if self.model is not None:
            self.model.register_observer(self)
