"""Module managing starting and stopping the application

"""

from julesTk import ThreadSafeObject
import sys
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk

__author__ = "Joeri Jongbloets <joeri@jongbloets.net>"


class Application(ThreadSafeObject, tk.Tk):
    """Manage the application entry point"""

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

    def is_registered(self, c):
        """Check whether the given controller is registered"""
        return c in self.controllers.values()

    def get_registration_key(self, c):
        """Return the name under which the controller is registered"""
        for key in self.controllers.keys():
            if self.get_controller(key) is c:
                break
        return key

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

    def create_hook(self, name):
        """Create a hook to which functions can be registered"""
        if self.has_hook(name):
            raise KeyError("Hook %s already exists" % name)
        self._hooks[name] = []

    def register_hook(self, name, f):
        """Register a function to a hook
        
        - Use lambda to register a parametrized function
        - Functions should return a boolean to report their success
        """
        if not self.has_hook(name):
            self.create_hook(name)
        self._hooks[name].append(f)
        return self

    def remove_hook(self, name, f):
        """Remove the function registration from a hook"""
        if self.has_hook(name):
            hooks = self._hooks[name]
            if f in hooks:
                hooks.remove(f)
        return self

    def empty_hook(self, name):
        """Remove all function registrations from a hook"""
        if self.has_hook(name):
            self._hooks[name] = []
        return self

    def process_hook(self, name):
        """Run all functions registered to the hook
        
        :return: Whether all functions ran successful
        :rtype: bool
        """
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
        self._execute()
        with self.lock:
            # clean up
            self.stop()

    def _execute(self):
        """Run the main loop"""
        result = False
        try:
            self.mainloop()
            result = True
        except KeyboardInterrupt:
            pass
        return result

    def start(self):
        if not self._configured:
            self.prepare()
        # run all hooks associated with starting
        if self.process_hook("APP_START"):
            # if successful: start
            self._start()
        else:
            # else exit immediately
            self._stop()

    def _start(self):
        """Everything to show and run the application"""
        raise NotImplementedError

    def stop(self):
        # run all hooks associated with closing
        if self.process_hook("APP_CLOSE"):
            # if hooks were successful: exit
            self._stop()
        else:
            # if hooks failed: keep in mainloop
            self._execute()

    def _stop(self):
        """Clean-up after execution
        
        Will request all controllers to clean-up and close
        """
        while len(self.controllers) > 0:
            name = self.controllers.keys()[0]
            controller = self.get_controller(name)
            self.remove_controller(name)
            if controller.is_running():
                controller.stop()
        tk.Tk.quit(self)
