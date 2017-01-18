"""Provide Controller classes"""

from model import Model

__author__ = "Joeri Jongbloets <joeri@jongbloets.net>"


class Controller(object):

    def __init__(self, app, view=None, model=None):
        super(Controller, self).__init__()
        self._app = app
        # handle to the view (main responsible view)
        self._view = view
        # handle to the model
        self._model = model

    def __del__(self):
        self.stop()

    def setup(self):
        """Configures the controller (set-up model, view)"""
        raise NotImplementedError

    def start(self):
        raise NotImplementedError

    def stop(self):
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
        if not isinstance(model, Model):
            raise ValueError("Invalid model")
        self._model = model
