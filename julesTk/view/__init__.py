"""Implementing basic view objects"""

from julesTk import *

__author__ = "Joeri Jongbloets <joeri@jongbloets.net>"


class Frame(ttk.Frame, object):

    FONT_FAMILY = "Verdana"
    FONT_SMALL = (FONT_FAMILY, 8)
    FONT_NORMAL = (FONT_FAMILY, 10)
    FONT_LARGE = (FONT_FAMILY, 14)

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

    def __init__(self, parent):
        """

        :rtype: Tkinter.Frame
        """
        ttk.Frame.__init__(self, parent)
        self._parent = parent

    @property
    def parent(self):
        return self._parent

    def setup(self):
        raise NotImplementedError


class View(Frame):
    """Interacting frame"""

    def __init__(self, parent, controller):
        super(View, self).__init__(parent)
        self._controller = controller
        self._variables = {}
        self._widgets = {}

    @property
    def controller(self):
        """ The controller

        :rtype: julesTk.controller.Controller
        """
        return self._controller

    @property
    def variables(self):
        """Dictionary of variables registered to this view

        :rtype: dict[str, tk.Variable]
        """
        return self._variables

    def has_variable(self, name):
        """Returns whether a variable is registered to this view using the given name

        :rtype: bool
        """
        return name in self.variables.keys()

    def get_variable(self, name):
        """Returns a variable registered to this view

        :param name: Name of the variable
        :type name: str
        :return: The variable
        :rtype: tk.Variable
        """
        if not self.has_variable(name):
            raise KeyError("Unknown variable: {}".format(name))
        return self.variables[name]

    def add_variable(self, name, variable):
        """Registers a variable under a new name to this view

        :param name: The name under which the variable should be registered
        :type name: str
        :param variable: The variable to register
        :type variable: tk.Variable
        :return: The registered variable
        :rtype: tk.Variable
        """
        if self.has_variable(name):
            raise KeyError("Already registered a variable as: {}".format(name))
        self.variables[name] = variable
        return variable

    def remove_variable(self, name):
        """Removes a variable (name) from the registry

        :return: Whether the variable is still in the registry
        :rtype: bool
        """
        if not self.has_variable(name):
            raise KeyError("Unknown variable: {}".format(name))
        self.variables.pop(name)
        return not self.has_variable(name)

    @property
    def widgets(self):
        """Dictionary of widgets registered to this view

        :rtype: dict[str, tk.Widget]
        """
        return self._widgets

    def has_widget(self, name):
        """Whether this view has a widget registered under the given name

        :param name: Name to look for
        :type name: str
        :rtype: bool
        """
        return name in self.widgets.keys()

    def get_widget(self, name):
        """Returns the widget registered to this view under the given name

        :param name: Name to look for
        :type name: str
        :rtype: tk.Widget
        """
        if not self.has_widget(name):
            raise KeyError("Unknown widget: {}".format(name))
        return self.widgets[name]

    def add_widget(self, name, widget):
        """Registers a widget under a new name to the view

        :raises: KeyError, if name is already used

        :param name: Name to register the widget under
        :type name: str
        :param widget: The widget to register
        :type widget: tk.Widget
        :return: The widget that as registered
        :rtype: tk.Widget
        """
        if self.has_widget(name):
            raise KeyError("Already registered a widget as: {}".format(name))
        self.widgets[name] = widget
        return widget

    def remove_widget(self, name):
        """Removes a widget (name) from the registry

        :param name: Name to remove
        :type name: str
        :return: Whether the widget is still registered
        :rtype: bool
        """
        if not self.has_widget(name):
            raise KeyError("Unknown widget: {}".format(name))
        self.widgets.pop(name)
        return name not in self.widgets.keys()

    def show(self):
        """Shows the view"""
        self.tkraise()

    def hide(self):
        """Hides the view (temporarily)"""
        self.grid_remove()

    def close(self):
        """Closes the view"""
        return True

    def setup(self):
        """Configure this view"""
        raise NotImplementedError


class ViewSet(View):
    """A view can contain one or more views"""

    def __init__(self, parent, controller):
        super(ViewSet, self).__init__(parent, controller)
        self._views = {}

    @property
    def views(self):
        """

        :rtype: dict[str, pyLabJackView.view.View]
        """
        return self._views

    def get_view(self, name):
        """

        :param name: Name of the view
        :rtype: julesTk.view.View
        """
        if not self.has_view(name):
            KeyError("No view registered under: {}".format(name))
        return self.views[name]

    def has_view(self, name):
        return name in self.views

    def add_view(self, name, frame):
        if self.has_view(name):
            KeyError("Already registered a view under: {}".format(name))
        self.views[name] = frame

    def remove_view(self, name):
        if not self.has_view(name):
            KeyError("No view registered under: {}".format(name))
        self.get_view(name).close()
        self.views.pop(name)

    def show_view(self, name):
        """Show a specific View"""
        v = self.get_view(name)
        v.show()

    def hide_views(self):
        """Hide all Views"""
        for v in self._views.keys():
            self.hide_view(v)
        # done

    def hide_view(self, name):
        """Hide a specific View"""
        v = self.get_view(name)
        v.grid_remove()

    def show(self):
        """Show this ViewSet"""
        raise NotImplementedError

    def hide(self):
        """Hide this ViewSet"""
        raise NotImplementedError

    def setup(self):
        """Configure this ViewSet"""
        raise NotImplementedError

    def close(self):
        """Close this ViewSet"""
        while len(self.views.values()) > 0:
            v = self.views.keys()[0]
            self.get_view(v).close()
            self.remove_view(v)
        super(ViewSet, self).close()
