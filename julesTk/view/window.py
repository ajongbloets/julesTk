"""Provides TopLevel views; i.e. Windows"""

from julesTk.view import tk, JTkView, WmView
from julesTk.view.viewset import BaseViewSet

__author__ = "Joeri Jongbloets <joeri@jongbloets>"


class Window(tk.Toplevel, WmView):

    def __init__(self, parent, controller):
        tk.Toplevel.__init__(self, parent)
        WmView.__init__(self, parent, controller)
        self.protocol("WM_DELETE_WINDOW", self.exit)

    @property
    def root(self):
        """Return the root view

        :rtype: Tkinter.Tk or tkinter.Tk
        """
        result = self.parent
        if self.controller is not None:
            result = self.controller.root
        if isinstance(self.parent, JTkView):
            result = self.parent.root
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


class ModalWindow(Window):
    """A window taking all focus and blocking interaction with other windows"""

    STATE_BLOCKED = 4

    def __init__(self, parent, ctrl):
        super(ModalWindow, self).__init__(parent, ctrl)
        self.parent.add_observer(self)
        self.add_event_slot("app_close", self.close)

    def _prepare(self):
        raise NotImplementedError

    def _show(self):
        super(ModalWindow, self)._show()
        self.transient(self.parent)
        self.grab_set()
        self._block()

    def block(self):
        self._view_state = self.STATE_BLOCKED
        return self._block()

    def _block(self):
        self.update()
        self.root.wait_window(self)

    def _hide(self):
        return False

    def _close(self):
        self.parent.remove_observer(self)
        super(ModalWindow, self)._close()

    def is_blocked(self):
        return self._view_state == self.STATE_BLOCKED
