from julesTk.view import ttk, View


class ViewSet(View):
    """A viewset can contain one or more views"""

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

    def prepare(self):
        """Configure this ViewSet"""
        raise NotImplementedError

    def close(self):
        """Close this ViewSet"""
        while len(self.views.values()) > 0:
            v = self.views.keys()[0]
            self.get_view(v).close()
            self.remove_view(v)
        super(ViewSet, self).close()
