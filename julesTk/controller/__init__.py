"""Provide Controller classes"""

from julesTk.app import Application
from julesTk.model import Model
from julesTk.view import BaseView, View, tk

__author__ = "Joeri Jongbloets <joeri@jongbloets.net>"


class BaseController(object):
    """A bare-bones controller, without view or model"""

    def __init__(self, parent):
        super(BaseController, self).__init__()
        self._parent = parent
        self._configured = False

    def __del__(self):
        self.stop()

    def prepare(self):
        self._prepare()
        self._configured = True
        return self

    def _prepare(self):
        """Configures the controller (set-up model, view)"""
        raise NotImplementedError

    def start(self):
        """Start the controller"""
        if not self._configured:
            self.prepare()
        return self._start()

    def _start(self):
        raise NotImplementedError

    def stop(self):
        """Stop the controller"""
        return self._stop()

    def _stop(self):
        raise NotImplementedError

    @property
    def parent(self):
        """Return reference to the parent object

        :rtype: julesTk.controller.BaseController or julesTk.app.Application
        """
        return self._parent

    @property
    def application(self):
        """Return the application instance

        :rtype: julesTk.app.Application
        """
        result = self.parent
        if not isinstance(result, tk.Tk):
            result = self.parent.application
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

    @property
    def parent_view(self):
        """Return the view of the parent of this controller

        :rtype: julesTk.view.View
        """
        pview = self.parent
        if isinstance(pview, BaseController):
            pview = self.parent.view
        return pview

    def has_view(self):
        """Whether the controller has a view attached"""
        return self.view is not None

    def _start(self):
        """Start the controller and open the view"""
        self.view.show()

    def _stop(self):
        """Stop the controller and close the view managed by the view"""
        self.view.close()

    def _prepare(self):
        """Configure the controller and view.

        Should be called before showing the view or starting the controller.
        Preferably after initialization of the controller.

        :rtype: julesTk.controller.ViewController
        """
        if not self.has_view():
            self.load_view()
        self.view.prepare()
        return self

    def load_view(self):
        """Returns a new instance of the view as defined in VIEW_CLASS

        :return:
        :rtype: julesTk.view.View
        """
        if not issubclass(self.VIEW_CLASS, BaseView):
            raise ValueError("Expected a view not {}".format(self.VIEW_CLASS.__name__))
        self._view = self.VIEW_CLASS(self.parent_view, self)
        return self.view


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

    def _start(self):
        """Start the controller"""
        raise NotImplementedError

    def _stop(self):
        """Stop the controller"""
        raise NotImplementedError

    def _prepare(self):
        """Set-up and configure the controller"""
        raise NotImplementedError


class Controller(ViewController, ModelController):
    """A controller with both a model and view"""

    def __init__(self, parent, view=None, model=None):
        ViewController.__init__(self, parent=parent, view=view)
        ModelController.__init__(self, parent=parent, model=model)
