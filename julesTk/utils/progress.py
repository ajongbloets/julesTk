"""A threaded progress bar dialog

Show a progress bar dialog and run a (long) method in a separate thread.
Can block the flow in the Main Thread without blocking GUI updates.

Options
-------

* command: The command (or lambda) to execute.
* mode: Determinate or indeterminate, track progress or show a non-specific 'bouncing' bar.
* auto_close: Whether to close the dialog, as soon the command has finished.
* block: Whether to block program flow in the main thread while running.

"""

from modals import view, SimpleDialog
import threading

__author__ = "Joeri Jongbloets <joeri@jongbloets.net>"


class ProgressBarView(SimpleDialog):
    """Show a dialog with a progress bar
    
    """

    def __init__(self, parent, controller, mode="indeterminate"):
        """Initialize the progressbar
        
        :param parent: Parent view of this progressbar modal
        :param controller: Controller controlling this progressbar (not used)
        :param mode: Whether to show a determinate progress bar or indeterminate progress bar
        """
        self._value = view.tk.DoubleVar(0)
        self._mode = mode
        self._is_blocked = True
        buttons = [{"id": "ok", "caption": "Close", "value": False}]
        super(ProgressBarView, self).__init__(parent, controller, buttons=buttons)

    @property
    def bar(self):
        result = None
        if self.has_widget("progress"):
            result = self.get_widget("progress")
        return result

    def has_bar(self):
        return self.bar is not None

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, v):
        if v not in ["determinate", "indeterminate"]:
            raise ValueError("Invalid value for mode: {}".format(v))
        self._mode = v
        # update widget
        if self.has_widget("progress"):
            self.get_widget("progress").config(mode=self._mode)

    @property
    def value(self):
        return self._value.get()

    @value.setter
    def value(self, v):
        if not isinstance(v, (int, float)):
            raise ValueError("Invalid value: {}".format(v))
        self._value.set(v)

    def body(self, parent):
        super(ProgressBarView, self).body(parent)
        pgb = view.ttk.Progressbar(parent)
        if self.mode == "determinate":
            pgb.config(variable=self._value)
        pgb.pack(side=view.tk.LEFT, fill=view.tk.X, expand=1)
        self.add_widget("progress", pgb)

    def footer(self, parent):
        btc = view.ttk.Button(parent, text="Close", command=lambda: self.process_click(True))
        self.add_widget("ok", btc)
        btc.pack(side=view.tk.BOTTOM)

    def _show(self):
        if self.mode == "indeterminate":
            self.get_widget("progress").start()
        if self._is_blocked:
            self.get_widget("ok").config(state="disabled")
        super(ProgressBarView, self)._show()

    def _block(self):
        return True

    def set_blocked(self, state):
        self._is_blocked = state is True
        if self.has_widget("ok"):
            self.get_widget("ok").config(state="disabled" if state else "normal")
            if not state:
                self.get_widget("ok").focus_set()

    def process_click(self, value):
        if not self._is_blocked:
            self.close()


class ProgressBar(threading.Thread):
    """Show a progress bar and run a (long) process in the background
    
    Creates and manages the ProgressBar Dialog.
    
    """

    def __init__(self, parent, command=None, mode="indeterminate", maximum=100, auto_close=False):
        """Initialize a progress bar and run command in a separate thread

        :param parent: Parent VIEW to connect dialog to.
        :type parent: julesTk.view.View
        :param: The command to execute in the separate thread
        :type command: callable
        :param mode: What kind of progress bar to show?
        :type mode: str
        :param maximum: Maximum value of the progress bar, defaults to 100 (%).
        :type maximum: int | float
        :param auto_close: Automatically close the dialog when the thread is finished?
        :type auto_close: boolean
        :rtype: julesTk.utils.progress.ProgressBar
        """
        super(ProgressBar, self).__init__()
        self._view = ProgressBarView(parent, None, mode=mode)
        self._auto_close = auto_close
        self._command = command
        self._result = None
        self._lock = threading.RLock()
        self._is_running = False
        self._is_finished= threading.Event()
        self._mode = mode
        self._progress = 0
        self._maximum = maximum

    @property
    def lock(self):
        return self._lock

    def is_running(self):
        """Whether the thread"""
        with self.lock:
            result = self._is_running
        return result

    def is_stopped(self):
        """Whether the thread is finished running"""
        return not self.is_running()

    @property
    def is_finished(self):
        """Event that will be triggered when the thread is done"""
        return self._is_finished

    @property
    def auto_close(self):
        with self.lock:
            result = self._auto_close
        return result

    @auto_close.setter
    def auto_close(self, v):
        with self.lock:
            if not self.is_running():
                self._auto_close = v
        # done

    @property
    def command(self):
        with self.lock:
            result = self._command
        return result

    @command.setter
    def command(self, cmd):
        if callable(cmd) or cmd is None:
            with self.lock:
                if not self.is_running():
                    self._command = cmd
        # done

    @property
    def result(self):
        result = None
        if not self.is_running():
            result = self._result
        return result

    @property
    def mode(self):
        with self.lock:
            result = self._mode
        return result

    @property
    def maximum(self):
        with self.lock:
            result = self._maximum
        return result

    @maximum.setter
    def maximum(self, value):
        with self.lock:
            self._maximum = value

    @property
    def progress(self):
        with self.lock:
            result = self._progress
        return result

    @progress.setter
    def progress(self, v):
        if not isinstance(v, (int, float)):
            raise ValueError("Expected a numeric value, got: {}".format(type(v)))
        with self.lock:
            self._progress = v
            self._view.value = v

    def increase(self, step=1):
        """Increase progress"""
        with self.lock:
            new_progress = self.progress + step
            if new_progress <= self.maximum:
                self.progress = new_progress
            else:
                new_progress = self.maximum
        return new_progress

    @property
    def view(self):
        return self._view

    def _prepare(self):
        return True

    def start(self, command=None, block=False, auto_close=None):
        if command is not None and callable(command):
            self.command = command
        if auto_close is not None:
            self.auto_close = auto_close
        with self.lock:
            self._is_finished.clear()
            self._is_running = True
            self._view.show()
            threading.Thread.start(self)
        if block:
            while not self.is_finished.isSet():
                # wait
                self.view.update()
        return self

    def run(self):
        # work on the job
        if self._command is not None and callable(self._command):
            self._result = self._command()
        # finish
        with self.lock:
            self.view.set_blocked(False)
            if self.auto_close and not self.view.is_closed():
                self.view.close()
            self._is_running = False
            self._is_finished.set()

    def stop(self):
        self.progress = self.maximum
