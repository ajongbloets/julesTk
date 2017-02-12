"""Implementing basic view objects"""

import sys
if sys.version_info[0] < 3:
    import Tkinter as tk
    import ttk
else:
    import tkinter as tk
    from tkinter import ttk
from julesTk.app import Application

__author__ = "Joeri Jongbloets <joeri@jongbloets.net>"


class BaseFrame(object):
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


class Frame(ttk.Frame, BaseFrame):

    def __init__(self, parent):
        super(Frame, self).__init__(parent)


class BaseView(BaseFrame):
    """Empty Base class used for checking if an object belongs to the view family"""

    def __init__(self, parent, controller):
        """Initialize a BaseView

        """
        super(BaseView, self).__init__()
        self._configured = False
        self._parent = parent
        self._controller = controller
        self._variables = {}
        self._widgets = {}

    def __del__(self):
        self.close()

    @property
    def parent(self):
        """Return the master of this widget

        :rtype: julesTk.view.BaseView
        """
        return self._parent

    @property
    def application(self):
        """Return the root level widget

        :rtype: Tkinter.Tk or tkinter.Tk
        """
        result = self.parent
        if not isinstance(result, Application):
            result = self.parent.application
        return result

    @property
    def controller(self):
        """ The controller

        :rtype: julesTk.controller.BaseController
        """
        return self._controller

    @property
    def variables(self):
        """Variables registered to this view

        :rtype: dict[str, Tkinter.Variable | tkinter.Variable]
        """
        return self._variables

    @property
    def widgets(self):
        """Widgets registered to this view

        :rtype: dict[str, Tkinter.BaseWidget | tkinter.BaseWidget]
        """
        return self._widgets

    def prepare(self):
        self._prepare()
        self._configured = True
        return self

    def _prepare(self):
        raise NotImplementedError

    def show(self):
        if not self._configured:
            self.prepare()
        return self._show()

    def _show(self):
        raise NotImplementedError

    def hide(self):
        return self._hide()

    def _hide(self):
        raise NotImplementedError

    def close(self):
        return self._close()

    def _close(self):
        raise NotImplementedError

    def has_variable(self, name):
        """Whether a variable is registered under the given name

        :param name: Name to search for
        :type name: str
        :rtype: bool
        """
        return name in self.variables.keys()

    def add_variable(self, name, variable):
        """Register a variable under a new name to the view

        :param name: Name to register the variable under
        :type name: str
        :param variable: The variable to register
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
        :param widget: The widget to register
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


class View(Frame, BaseView):
    """A Frame acting as """

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        BaseView.__init__(self, parent, controller)

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
        self.destroy()
        return True

    def _prepare(self):
        """Configure this view"""
        raise NotImplementedError
