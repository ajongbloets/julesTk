"""Implementing basic view objects"""

from julesTk import *

__author__ = "Joeri Jongbloets <joeri@jongbloets.net>"
__all__ = [
    "JTkView", "FrameView", "WmView",
    "tk", "ttk", "receives", "triggers"
]


class BaseWm(object):
    """Empty base class used to share most basic functions between frames and views"""

    FONT_FAMILY = "Verdana"
    FONT_SMALL = (FONT_FAMILY, 8)
    FONT_NORMAL = (FONT_FAMILY, 10)
    FONT_LARGE = (FONT_FAMILY, 14)
    FONT_HUGE = (FONT_FAMILY, 16)

    @staticmethod
    def configure_grid(w, sticky="nsew", **kwargs):
        w.grid(sticky=sticky, **kwargs)

    @staticmethod
    def configure_column(w, indexes, weight=1, **kwargs):
        if not isinstance(indexes, (tuple, list)):
            indexes = [indexes]
        kwargs["weight"] = weight
        for index in indexes:
            w.grid_columnconfigure(index, **kwargs)

    @staticmethod
    def configure_row(w, indexes, weight=1, **kwargs):
        if not isinstance(indexes, (tuple, list)):
            indexes = [indexes]
        kwargs["weight"] = weight
        for index in indexes:
            w.grid_rowconfigure(index, **kwargs)


class JTkView(JTkObject):
    """Base FrameView implementing most of the view functionality

    Preparation and loading of widgets
    ----------------------------------

    Use _prepare() (abstract method) to prepare the view for showing. Including the creation of widgets.
    Call prepare() to execute preparation.

    Widgets and variables can be stored in a dictionary registry.

    Showing, hiding and closing
    ---------------------------

    - call show() [ internal runs -> _show ]
    _show (abstract method) implements the specific routine, need to for showing the view.
    Call show() to execute this. show() will check if prepare() has been run before and run it necessary.
    - call hide to temporarily hide the view
    _hide() implements the specific routine for hiding the view.
    - call close to destroy the view
    _close() implements the specific routine for closing the view.
    """

    STATE_INITIALIZED = 0
    STATE_CONFIGURED = 1
    STATE_SHOWING = 2
    STATE_HIDDEN = 3
    STATE_CLOSED = -1

    def __init__(self, parent, controller=None):
        """Initialize a BaseView

        :param parent: Parent view (or application)
        :param controller: Controlling controller
        """
        super(JTkView, self).__init__()
        self._view_state = self.STATE_INITIALIZED
        self._parent = parent
        self._controller = None
        self.set_controller(controller)

    def __del__(self):
        self.close()

    @property
    def view_state(self):
        return self._view_state

    def is_initialized(self):
        return self.view_state == self.STATE_INITIALIZED

    def is_configured(self):
        return self.view_state == self.STATE_CONFIGURED

    def is_showing(self):
        return self.view_state == self.STATE_SHOWING

    def is_hidden(self):
        return self.view_state == self.STATE_HIDDEN

    def is_closed(self):
        return self.view_state == self.STATE_CLOSED

    @property
    def parent(self):
        """Return the master of this widget

        :rtype: julesTk.view.BaseView
        """
        return self._parent

    @property
    def root(self):
        """Return the root view

        :rtype: Tkinter.Tk or tkinter.Tk
        """
        result = self.parent
        if isinstance(result, JTkView):
            result = self.parent.root
        return result

    @property
    def application(self):
        """Return the application"""
        if self.has_controller():
            result = self.controller.application
        else:
            result = self.parent
            if isinstance(self.parent, JTkView):
                result = self.parent.application
        return result

    def get_controller(self):
        """ The controller

        :rtype: julesTk.controller.BaseController
        """
        return self._controller

    @property
    def controller(self):
        return self.get_controller()

    def has_controller(self):
        return self.get_controller() is not None

    def set_controller(self, c):
        from julesTk.controller import BaseController
        if c is not None and not isinstance(c, BaseController):
            raise ValueError("Expected a BaseController not a {}".format(type(c).__name__))
        if self.controller is not None:
            self.remove_observer(self.controller)
            self.controller.remove_observer(self)
        self._controller = c
        if self.controller is not None:
            self.add_observer(self.controller)
            self.controller.add_observer(self)

    def prepare(self):
        self._prepare()
        self._view_state = self.STATE_CONFIGURED
        return self

    def _prepare(self):
        raise NotImplementedError

    @receives("controller_start")
    def _event_controller_start(self, *args):
        self.show()

    def show(self):
        if self.view_state < self.STATE_CONFIGURED:
            self.prepare()
        self._view_state = self.STATE_SHOWING
        return self._show()

    def _show(self):
        raise NotImplementedError

    def hide(self):
        self._view_state = self.STATE_HIDDEN
        return self._hide()

    def _hide(self):
        raise NotImplementedError

    @receives("controller_stop")
    def _event_controller_stop(self, *args):
        self.close()

    @triggers("view_close", before=True)
    def close(self):
        self._view_state = self.STATE_CLOSED
        return self._close()

    def _close(self):
        raise NotImplementedError


class WmView(BaseWm, JTkView):
    """A Frame acting as """

    def __init__(self, parent, controller):
        BaseWm.__init__(self)
        JTkView.__init__(self, parent, controller)
        self._variables = {}
        self._widgets = {}

    @property
    def variables(self):
        """Variables registered to this view

        :rtype: dict[str, Tkinter.Variable | tkinter.Variable]
        """
        return self._variables

    def has_variable(self, name):
        """Whether a variable is registered under the given name

        :param name: Name to search for
        :type name: str
        :rtype: bool
        """
        return name in self.variables.keys()

    def add_variable(self, name, variable):
        """Register a variable under a new name to the view

        :param name: Name to add_observer the variable under
        :type name: str
        :param variable: The variable to add_observer
        :type variable: Tkinter.Variable | tkinter.Variable
        :rtype: Tkinter.Variable | tkinter.Variable
        """
        if self.has_variable(name):
            raise KeyError("Variable name already registered to this view")
        self.variables[name] = variable
        return variable

    def get_variable(self, name):
        """Get the variable registered to this view under the given name

        :param name: Name of the variable
        :type name: str
        :return: The requested variable
        :rtype: Tkinter.Variable | tkinter.Variable
        """
        if not self.has_variable(name):
            raise KeyError("Variable name not registered to this view")
        return self.variables[name]

    def remove_variable(self, name):
        """Remove a variable from the registry of this view

        The variable is NOT destroyed!

        :param name: Name of the variable to remove
        :type name: str
        :return: The removed variable
        :rtype: Tkinter.Variable | tkinter.Variable
        """
        if not self.has_variable(name):
            raise KeyError("Variable name not registered to this view")
        self.variables.pop(name)
        return not self.has_variable(name)

    @property
    def widgets(self):
        """Widgets registered to this view

        :rtype: dict[str, Tkinter.BaseWidget | tkinter.BaseWidget]
        """
        return self._widgets

    def has_widget(self, name):
        """Whether a widget is registered using the given name

        :type name: str
        :rtype: bool
        """
        return name in self.widgets.keys()

    def add_widget(self, name, widget):
        """Register a new widget to this view

        :param name: Name of the widget
        :type name: str
        :param widget: The widget to add_observer
        :type widget: Tkinter.BaseWidget | tkinter.BaseWidget
        :return: The registered widget
        :rtype: Tkinter.BaseWidget | tkinter.BaseWidget
        """
        if self.has_widget(name):
            raise KeyError("Widget name already registered to this view")
        self.widgets[name] = widget
        return widget

    def get_widget(self, name):
        """Get the widget registered under the given name

        :param name: Name of the widget
        :type name: str
        :return: The requested widget
        :rtype: Tkinter.BaseWidget | tkinter.BaseWidget
        """
        if not self.has_widget(name):
            raise KeyError("Widget name not registered to this view")
        return self.widgets[name]

    def remove_widget(self, name):
        """Remove a widget from the registry of this view

        The widget is NOT destroyed

        :param name: Name of the widget to remove
        :type name: str
        :return: The widget that was removed
        :rtype: Tkinter.BaseWidget | tkinter.BaseWidget
        """
        if not self.has_widget(name):
            raise KeyError("Widget name not registered to this view")
        self.widgets.pop(name)
        return not self.has_widget(name)

    def _show(self):
        raise NotImplementedError

    def _hide(self):
        raise NotImplementedError

    def _close(self):
        raise NotImplementedError

    def _prepare(self):
        """Configure this view"""
        raise NotImplementedError


class FrameView(ttk.Frame, WmView):

    def __init__(self, parent, controller=None):
        ttk.Frame.__init__(self, master=parent)
        WmView.__init__(self, parent=parent, controller=controller)

    def _show(self):
        """Shows the view"""
        self.tkraise()
        return True

    def _hide(self):
        """Hides the view (temporarily)"""
        self.grid_remove()
        return True

    def _close(self):
        """Closes the view"""
        if self.controller is not None and not self.controller.is_stopped():
            self.controller.stop()
        self.destroy()
        return True

    def _prepare(self):
        raise NotImplementedError
