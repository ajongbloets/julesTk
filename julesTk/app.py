"""Module managing starting and stopping the application

"""

from julesTk import *
# import sys
# if sys.version_info[0] < 3:
#     import Tkinter as tk
# else:
#     import tkinter as tk

__author__ = "Joeri Jongbloets <joeri@jongbloets.net>"


class Application(JTkObject):
    """Manage the application entry point"""

    def __init__(self, root=None, *args, **kwargs):
        super(Application, self).__init__()
        if root is None:
            root = tk.Tk()
        self._root = root
        self._configured = False
        self._can_start = False
        self._can_stop = True
        self.root.protocol("WM_DELETE_WINDOW", self.stop)
        self._controllers = {}

    @property
    def root(self):
        return self._root

    def can_start(self):
        return self._can_start is True

    def allow_start(self, state):
        self._can_start = state is True

    def can_stop(self):
        return self._can_stop is True

    def allow_stop(self, state):
        self._can_stop = state is True

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

    def get_controller_name(self, c):
        """Return the name under which the controller is registered"""
        name = None
        for name in self.controllers.keys():
            if self.get_controller(name) is c:
                break
        return name

    def add_controller(self, name, controller):
        """Registers a new controller under the given name

        :raises KeyError: If another controller is already registered under the same name

        :param name: Name to add_observer the controller under
        :type name: str
        :param controller: The controller to add_observer
        :type controller: julesTk.controller.BaseController
        """
        if self.has_controller(name):
            raise KeyError("Already registered a controller under: {}".format(name))
        self.controllers[name] = controller
        self.add_observer(controller)
        controller.add_observer(self)

    def remove_controller(self, name):
        """Removes a controller from the application

        :raises KeyError: If no controller is registered with that name
        :param name: Name of the controller
        :type name: str
        """
        if not self.has_controller(name):
            raise KeyError("No controller registered under: {}".format(name))
        controller = self.controllers.pop(name)
        self.remove_observer(controller)
        controller.remove_observer(self)

    def prepare(self):
        if self._prepare():
            self._configured = True
            self._can_start = True
        return self

    def _prepare(self):
        """Configures the application and loads at least one controller"""
        return True

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
            self.root.mainloop()
            result = True
        except KeyboardInterrupt:
            pass
        return result

    def start(self):
        if not self._configured:
            self.prepare()
        # run all hooks associated with starting
        self.trigger_event("application_start")
        if self.can_start():
            self._start()

    def _start(self):
        """Everything to show and run the application"""
        raise NotImplementedError

    def stop(self):
        self.trigger_event("application_close")
        if self.can_stop():
            self._stop()
        else:
            self._execute()

    @receives("app_close")
    def _app_close(self, event, source, data=None):
        self.stop()

    def _stop(self):
        """Clean-up after execution

        Will request all controllers to clean-up and close
        """
        while len(self.controllers) > 0:
            name = next(iter(self.controllers))
            controller = self.get_controller(name)
            self.remove_controller(name)
            if controller.is_running():
                controller.stop()
        tk.Tk.quit(self.root)
