"""Provide Controller classes"""

from julesTk.model import Model
from julesTk.view import View, tk

__author__ = "Joeri Jongbloets <joeri@jongbloets.net>"


class BaseController(object):
    """A bare-bones controller, without view or model"""

    def __init__(self, parent):
        super(BaseController, self).__init__()
        self._parent = parent

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
    def parent(self):
        """Return reference to the parent object

        :rtype: julesTk.app.Application
        """
        return self._parent

    @property
    def application(self):
        result = self.parent
        if not isinstance(result, tk.Tk):
            result = self.parent.parent
        return result


class ViewController(BaseController):
    """A controller with a view (no model)"""

    VIEW_CLASS = View

    def __init__(self, parent, view=None):
        super(ViewController, self).__init__(parent=parent)
        self._view = view

    @property
    def view(self):
        """Return the view managed by this controller

        :rtype: julesTk.view.View
        """
        return self._view

    def has_view(self):
        """Whether the controller has a view attached"""
        return self.view is not None

    def start(self):
        """Start the controller and open the view"""
        self.view.show()

    def stop(self):
        """Stop the controller and close the view managed by the view"""
        self.view.close()

    def setup(self):
        """Configure the controller and view.

        Should be called before showing the view or starting the controller.
        Preferably after initialization of the controller.

        :rtype: julesTk.controller.ViewController
        """
        if not self.has_view():
            if not issubclass(self.VIEW_CLASS, View):
                raise ValueError("Expected a view not {}".format(self.VIEW_CLASS.__name__))
            pview = self.parent
            if isinstance(pview, BaseController):
                pview = self.parent.view
            self._view = self.VIEW_CLASS(pview, self)
        self.view.setup()
        return self


class ModelController(BaseController):
    """A controller with a model (no view)"""

    def __init__(self, parent, model=None):
        super(ModelController, self).__init__(parent=parent)
        self._model = model

    @property
    def model(self):
        """The model used by this controller

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
        """Whether the controller has a model attached"""
        return self.model is not None

    def start(self):
        """Start the controller"""
        raise NotImplementedError

    def stop(self):
        """Stop the controller"""
        raise NotImplementedError

    def setup(self):
        """Set-up and configure the controller"""
        raise NotImplementedError


class Controller(ViewController, ModelController):
    """A controller with both a model and view"""

    def __init__(self, parent, view=None, model=None):
        ViewController.__init__(self, parent=parent, view=view)
        ModelController.__init__(self, parent=parent, model=model)
