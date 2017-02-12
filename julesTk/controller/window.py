
from . import ViewController
from julesTk.view.window import Window

__author__ = "Joeri Jongbloets <joeri@jongbloets.net>"


class WindowController(ViewController):

    VIEW_CLASS = Window

    def load_view(self):
        if not issubclass(self.VIEW_CLASS, Window):
            raise ValueError("Expected a ModalWindow not {}".format(self.VIEW_CLASS.__name__))
        self._view = self.VIEW_CLASS(self.parent_view, self)
