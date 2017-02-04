"""Provide Controller classes"""

from julesTk.model import Model
from julesTk.view import View

__author__ = "Joeri Jongbloets <joeri@jongbloets.net>"


class BaseController(object):
    """A bare-bones controller, without view or model"""

    def __init__(self, app):
        super(BaseController, self).__init__()
        self._app = app

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


class ViewController(BaseController):
    """A controller with a view (no model)"""

    VIEW_CLASS = View

    def __init__(self, app, view=None):
        super(ViewController, self).__init__(app=app)
        self._view = view

    @property
    def view(self):
        """Return the view

        :rtype: julesTk.view.View
        """
        return self._view

    def has_view(self):
        return self.view is not None

    def start(self):
        self.view.show()

    def stop(self):
        self.view.close()

    def setup(self):
        if not self.has_view():
            if not issubclass(self.VIEW_CLASS, View):
                raise ValueError("Expected a view not {}".format(self.VIEW_CLASS.__name__))
            self._view = self.VIEW_CLASS(self.application, self)
        self.view.setup()
        return self


class ModelController(BaseController):
    """A controller with a model (no view)"""

    def __init__(self, app, model=None):
        super(ModelController, self).__init__(app=app)
        self._model = model

    @property
    def model(self):
        """

        :return:
        :rtype: julesTk.model.Model
        """
        return self._model

    @model.setter
    def model(self, model):
        self._set_model(model)

    def _set_model(self, model):
        if not isinstance(model, Model):
            raise ValueError("Expected a model class")
        self._model = model

    def has_model(self):
        return self.model is not None

    def start(self):
        raise NotImplementedError

    def stop(self):
        raise NotImplementedError

    def setup(self):
        raise NotImplementedError


class Controller(ViewController, ModelController):
    """A controller with both a model and view"""

    def __init__(self, app, view=None, model=None):
        ViewController.__init__(self, app, view=view)
        ModelController.__init__(self, app, model=model)
