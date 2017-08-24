"""Provide Controller classes"""

from julesTk import *
from julesTk.app import Application
from julesTk.model import Model
from julesTk.view import JTkView, FrameView, tk

__author__ = "Joeri Jongbloets <joeri@jongbloets.net>"


class BaseController(JTkObject):
    """A bare-bones controller, without view or model"""

    STATE_INITIALIZED = 0
    STATE_CONFIGURED = 1
    STATE_STARTED = 2
    STATE_STOPPED = -1

    def __init__(self, parent):
        if not isinstance(parent, (BaseController, Application)):
            raise TypeError("Invalid parent object, expected a Controller or Application")
        super(BaseController, self).__init__()
        self._parent = parent
        self.add_observer(self.parent)
        self.parent.add_observer(self)
        self._state = self.STATE_INITIALIZED

    def __del__(self):
        self.stop()
        super(BaseController, self).__del__()
        if hasattr(self, "_parent"):
            self.remove_observer(self.parent)
            if self.parent is not None:
                self.parent.remove_observer(self)

    @property
    def state(self):
        return self._state

    def is_initialized(self):
        return self.state == self.STATE_INITIALIZED

    def is_configured(self):
        return self.state == self.STATE_CONFIGURED

    def is_running(self):
        return self.state == self.STATE_STARTED

    def is_stopped(self):
        return self.state == self.STATE_STOPPED

    def prepare(self):
        self._prepare()
        self._state = self.STATE_CONFIGURED
        return self

    def _prepare(self):
        """Configures the controller (set-up model, view)"""
        raise NotImplementedError

    def start(self):
        """Start the controller"""
        result = True
        if not self.is_configured():
            self.prepare()
        if not self.is_running():
            self.trigger_event("controller_start")
            self._state = self.STATE_STARTED
            result = self._start()
        return result

    def _start(self):
        return True     # overload

    def stop(self):
        """Stop the controller"""
        result = True
        if not self.is_stopped():
            self._state = self.STATE_STOPPED
            self.trigger_event("controller_stop")
            result = self._stop()
        return result

    @receives("application_stop")
    def _event_application_stop(self, *args):
        self.stop()

    def _stop(self):
        return True     # overload

    @property
    def parent(self):
        """Return reference to the parent object

        :rtype: julesTk.controller.BaseController or julesTk.app.Application
        """
        return self._parent

    @property
    def application(self):
        """The application controller

        :rtype: julesTk.app.Application
        """
        result = self.parent
        if not isinstance(result, Application):
            result = result.application
        return result

    @property
    def root(self):
        """The root view

        :rtype: Tkinter.Tk | tkinter.Tk
        """
        return self.parent.root


class ViewController(BaseController):
    """A controller with a view (no model)"""

    VIEW_CLASS = FrameView

    def __init__(self, parent, view=None):
        super(ViewController, self).__init__(parent=parent)
        self._view = None
        self.set_view(view)

    @property
    def view(self):
        """Return the view managed by this controller

        :rtype: julesTk.view.FrameView
        """
        return self._view

    @property
    def parent_view(self):
        """Return the view of the parent of this controller

        :rtype: julesTk.view.FrameView
        """
        pview = self.parent
        if isinstance(pview, ViewController):
            pview = pview.view
        elif isinstance(pview, Application):
            pview = pview.root
        return pview

    def has_view(self):
        """Whether the controller has a view attached"""
        return self.view is not None

    def set_view(self, v):
        if v is not None and not isinstance(v, JTkView):
            raise ValueError("Expected a view not {}".format(v.__name__))
        # unregister with old view
        if self.view is not None:
            v.set_controller(None)
            v.remove_observer(self)
            self.remove_observer(v)
        self._view = v
        # register with new view
        if self.view is not None:
            v.set_controller(self)
            v.add_observer(self)
            self.add_observer(v)
        return self.view

    @receives("view_close")
    def view_close(self, *args):
        self.stop()

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
        :rtype: julesTk.view.FrameView
        """
        if not issubclass(self.VIEW_CLASS, JTkView):
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
        if self.model is not None:
            self.remove_observer(self.model)
            self.model.remove_observer(self)
        self._model = model
        if self.model is not None:
            self.add_observer(self.model)
            self.model.add_observer(self)

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
