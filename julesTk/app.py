"""Module managing starting and stopping the application

"""

import sys
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk
from . import ThreadSafeObject

__author__ = "Joeri Jongbloets <joeri@jongbloets.net>"


class Application(ThreadSafeObject, tk.Tk):
    """Application entry point"""

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        super(Application, self).__init__()
        self._configured = False
        self.protocol("WM_DELETE_WINDOW", self.stop)
        self._controllers = {}
        self._hooks = {}

    @property
    def controllers(self):
        """All controllers attached to this application

        :return: A dictionary of the name - controller mapping
        :rtype: dict[str, julesTk.controller.BaseController]
        """
        return self._controllers

    def get_controller(self, name):
        """Returns the controller registered under the given name

        :raises KeyError: If no controller is registered with that name

        :param name: Name of the controller
        :type name: str
        :rtype: julesTk.controller.BaseController
        """
        if not self.has_controller(name):
            raise KeyError("No controller registered under: {}".format(name))
        return self.controllers[name]

    def has_controller(self, name):
        """Returns whether a controller is registered under the given name

        :param name: Name of the controller
        :type name: str
        :rtype: bool
        """
        return name in self.controllers.keys()

    def add_controller(self, name, controller):
        """Registers a new controller under the given name

        :raises KeyError: If another controller is already registered under the same name

        :param name: Name to register the controller under
        :type name: str
        :param controller: The controller to register
        :type controller: julesTk.controller.BaseController
        """
        if self.has_controller(name):
            raise KeyError("Already registered a controller under: {}".format(name))
        self.controllers[name] = controller

    def remove_controller(self, name):
        """Removes a controller from the application

        :raises KeyError: If no controller is registered with that name
        :param name: Name of the controller
        :type name: str
        """
        if not self.has_controller(name):
            raise KeyError("No controller registered under: {}".format(name))
        self.controllers.pop(name)

    def has_hook(self, name):
        return name in self._hooks.keys()

    def register_hook(self, name, f):
        if self.has_hook(name):
            self._hooks[name].append(f)
        else:
            self._hooks[name] = [f]
        return self

    def remove_hook(self, name, f):
        if self.has_hook(name):
            hooks = self._hooks[name]
            if f in hooks:
                hooks.remove(f)
        return self

    def process_hook(self, name):
        hooks = []
        if self.has_hook(name):
            hooks = self._hooks[name]
        result = True
        for f in hooks:
            result = f() and result
        return result

    def prepare(self):
        self._prepare()
        self._configured = True
        return self

    def _prepare(self):
        """Configures the application and loads at least one controller"""
        raise NotImplementedError

    def run(self):
        """Start the application"""
        with self.lock:
            # _prepare the application
            self.prepare()
            # now start the application
            self.start()
        # in the main loop we wait, so we do not need a lock
        self.mainloop()
        with self.lock:
            # clean up
            self.stop()

    def start(self):
        if not self._configured:
            self.prepare()
        self._start()

    def _start(self):
        """Everything to show and run the application"""
        raise NotImplementedError

    def stop(self):
        # process app close hook
        if self.process_hook("APP_CLOSE"):
            self._stop()

    def _stop(self):
        """Clean-up after execution"""
        while len(self.controllers) > 0:
            name = self.controllers.keys()[0]
            self.get_controller(name).stop()
            self.remove_controller(name)
        tk.Tk.quit(self)
