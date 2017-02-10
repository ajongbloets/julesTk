
from julesTk import app, controller, view

__author__ = "Joeri Jongbloets <joeri@jongbloets.net>"


class HelloWorld(app.Application):

    def __init__(self):
        super(HelloWorld, self).__init__()

    def _prepare(self):
        self.add_controller("main", HelloWorldController(self))

    @property
    def main(self):
        return self.get_controller("main")

    def _start(self):
        self.main.start()


class HelloWorldView(view.View):

    def _prepare(self):
        # resize frame with window size
        self.configure_grid(self)
        self.configure_row(self, 0)
        self.configure_column(self, 0)
        # parent should also resize with window
        self.configure_row(self.parent, 0)
        self.configure_column(self.parent, 0)
        lbl = view.ttk.Label(self, text="Hello World!", font=self.FONT_LARGE)
        self.add_widget("label1", lbl)
        self.configure_grid(lbl, padx=10, pady=10)


class HelloWorldController(controller.ViewController):

    VIEW_CLASS = HelloWorldView

    def update(self, observable):
        pass

if __name__ == "__main__":

    app = HelloWorld()
    app.run()
