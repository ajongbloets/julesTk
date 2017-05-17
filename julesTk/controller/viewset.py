
from . import ViewController


class ViewSetController(ViewController):

    def __init__(self, parent, view=None):
        super(ViewSetController, self).__init__(parent, view)
        self._controllers = {}

    @property
    def controllers(self):
        """ Dictionary with all controllers used in this viewset

        :return:
        :rtype: dict[str, julesTk.controller.BaseController]
        """
        return self._controllers

    def has_controller(self, name):
        """Whether a controller is registered to this controller using the given name"""
        return name in self.controllers.keys()

    def get_controller(self, name):
        """Return the controller registered under the given name"""
        if not self.has_controller(name):
            raise KeyError("No controller registered using the name: {}".format(name))
        return self.controllers[name]

    def add_controller(self, name, c):
        """Register a controller under a new name"""
        if self.has_controller(name):
            raise KeyError("Another controller is already registered under: {}".format(name))
        self.controllers[name] = c

    def remove_controller(self, name):
        """Remove controller and name from the registry"""
        if not self.has_controller(name):
            raise KeyError("No controller registered using the name: {}".format(name))
        return self.controllers.pop(name)

    def remove_controllers(self):
        """Remove all controllers from the registry

        And tell them to stop
        """
        while len(self.controllers.keys()) > 0:
            key = self.controllers.keys()[0]
            self.remove_controller(key).stop()
        return len(self.controllers.keys()) == 0

    def _stop(self):
        self.remove_controllers()
        super(ViewSetController, self)._stop()
