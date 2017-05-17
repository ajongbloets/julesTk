"""Class implementing a ProgressBar Dialog"""

from modals import view, SimpleDialog

__author__ = "Joeri Jongbloets <joeri@jongbloets.net>"


class ProgressBar(SimpleDialog):

    def __init__(self, parent, controller, mode="indeterminate", blocking=True):
        self._value = view.tk.DoubleVar(0)
        self._mode = mode
        self._blocking = blocking
        buttons = [{"id": "ok", "caption": "Close", "value": False}]
        super(ProgressBar, self).__init__(parent, controller, buttons=buttons)

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
            self.get_widget("progress").config(mode = self._mode)

    @property
    def value(self):
        return self._value.get()

    @value.setter
    def value(self, v):
        if not isinstance(v, (int, float)):
            raise ValueError("Invalid value: {}".format(v))
        self._value.set(v)
        if self.has_bar():
            maximum = self.bar.cget("maximum")
            if v >= maximum:
                self.set_blocking(False)

    def is_blocking(self):
        return self._blocking is True

    def set_blocking(self, state):
        self._blocking = state is True
        if self.has_widget("ok"):
            self.get_widget("ok").config(state="disabled" if state else "normal")

    def body(self, parent):
        super(ProgressBar, self).body(parent)
        pgb = view.ttk.Progressbar(parent, variable=self._value)
        pgb.pack(side=view.tk.BOTTOM, fill=view.tk.X, expand=1)
        self.add_widget("progress", pgb)

    def _show(self):
        if self.mode == "indeterminate":
            self.get_widget("progress").start()
        if self.is_blocking():
            self.get_widget("ok").config(state="disabled")
        super(ProgressBar, self)._show()

    def process_click(self, value):
        self._response = value
        if not self.is_blocking():
            self.close()
