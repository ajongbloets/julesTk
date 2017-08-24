
from julesTk import app, controller, view

__author__ = "Matt Swain <https://github.com/mcs07>, Joeri Jongbloets <joeri@jongbloets.net>"


class NestedApp(app.Application):

    def __init__(self):
        super(NestedApp, self).__init__()

    def _prepare(self):
        self.add_controller("main", MainController(self))

    @property
    def main(self):
        return self.get_controller("main")

    def _start(self):
        self.main.start()


class MainView(view.FrameView):

    def _prepare(self):
        # configure application frame to resize
        self.configure_row(self.parent, 0)
        self.configure_column(self.parent, 0)
        # configure this frame to resize it's grid
        self.configure_grid(self)
        self.configure_row(self, [0, 1])
        self.configure_column(self, 0)
        # initialize child
        # self.controller.child.start()
        # add child on first row
        self.configure_grid(self.controller.child.view, row=0, column=0)
        # add main text
        lbl = view.ttk.Label(self, text='Label in MainView')
        self.add_widget('label1', lbl)
        self.configure_grid(lbl, row=1, column=0)


class MainController(controller.ViewController):

    VIEW_CLASS = MainView

    def __init__(self, p, v=None):
        super(MainController, self).__init__(parent=p, view=v)
        self._child = ChildController(self)
        self.application.add_controller("child", self.child)

    @property
    def child(self):
        return self._child

    def start(self):
        self.child.start()
        super(MainController, self).start()


class ChildView(view.FrameView):

    def _prepare(self):
        self.configure_grid(self)
        lbl = view.ttk.Label(self, text='Label in ChildView')
        self.add_widget('label1', lbl)
        self.configure_grid(lbl, row=0, column=0)


class ChildController(controller.ViewController):

    VIEW_CLASS = ChildView


if __name__ == "__main__":

    app = NestedApp()
    app.run()
