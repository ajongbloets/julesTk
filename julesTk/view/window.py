"""Provides TopLevel views; i.e. Windows"""

from julesTk.view import tk, BaseView


class Window(tk.Toplevel, BaseView):

    def __init__(self, parent, controller):
        tk.Toplevel.__init__(self, parent)
        BaseView.__init__(self, parent, controller)
        self.protocol("WM_DELETE_WINDOW", self.close)

    def _prepare(self):
        raise NotImplementedError

    def _show(self):
        self.deiconify()
        self.grab_set()

    def _hide(self):
        self.withdraw()

    def _close(self):
        self.destroy()


class ModalWindow(Window):

    def __init__(self, parent, controller):
        super(ModalWindow, self).__init__(parent, controller)
        self._response = None

    @property
    def response(self):
        """Returns the input of the user given in the ModalWindow

        Developers can use this communicate the input of the window to the controller
        """
        return self._response

    @response.setter
    def response(self, value):
        self._response = value

    def _prepare(self):
        raise NotImplementedError

    def _show(self):
        self.transient(self.parent)
        self.grab_set()
        self.application.wait_window(self)

    def _hide(self):
        pass
