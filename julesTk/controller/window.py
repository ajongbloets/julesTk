
from . import ViewController
from julesTk.view.window import Window, ModalWindow

__author__ = "Joeri Jongbloets <joeri@jongbloets.net>"


class WindowController(ViewController):

    VIEW_CLASS = Window

    def load_view(self):
        if not issubclass(self.VIEW_CLASS, Window):
            raise ValueError("Expected a ModalWindow not {}".format(self.VIEW_CLASS.__name__))
        self._view = self.VIEW_CLASS(self.parent_view, self)


class ModalWindowController(ViewController):

    VIEW_CLASS = ModalWindow

    @property
    def view(self):
        """ The view managed by this controller

        :return:
        :rtype: julesTk.view.window.ModalWindow
        """
        return super(ModalWindowController, self).view

    @property
    def response(self):
        return self.view.response

    def load_view(self):
        if not issubclass(self.VIEW_CLASS, ModalWindow):
            raise ValueError("Expected a ModalWindow not {}".format(self.VIEW_CLASS.__name__))
        self._view = self.VIEW_CLASS(self.parent_view, self)

    def _start(self):
        self.view.show()
        return self.view.response
