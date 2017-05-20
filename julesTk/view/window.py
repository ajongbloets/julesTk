"""Provides TopLevel views; i.e. Windows"""

from julesTk.view import tk, BaseView
from viewset import BaseViewSet

__author__ = "Joeri Jongbloets <joeri@jongbloets>"


class Window(tk.Toplevel, BaseView):

    def __init__(self, parent, controller):
        tk.Toplevel.__init__(self, parent)
        BaseView.__init__(self, parent, controller)
        self.protocol("WM_DELETE_WINDOW", self.exit)

    @property
    def application(self):
        result = self.parent
        if self.controller is not None:
            result = self.controller.application
        elif isinstance(result, BaseView):
            result = self.parent.application
        return result

    def _prepare(self):
        raise NotImplementedError

    def _show(self):
        self.deiconify()

    def _hide(self):
        self.withdraw()
        return True

    def _close(self):
        if self.controller is not None and not self.controller.is_stopped():
            self.controller.stop()
        self.destroy()
        return True

    def exit(self):
        self.close()


class WindowViewSet(Window, BaseViewSet):
    """A window that can contain multiple views"""

    def _prepare(self):
        raise NotImplementedError

    def _close(self):
        BaseViewSet.close_views(self)
        return super(WindowViewSet, self)._close()
