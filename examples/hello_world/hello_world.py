
from julesTk import app, controller, view

__author__ = "Joeri Jongbloets <joeri@jongbloets.net>"


class HelloWorld(app.Application):

    def __init__(self):
        super(HelloWorld, self).__init__()

    def setup(self):
        c = HelloWorldController(self).setup()
        self.add_controller("main", c)

    def run(self):
        self.get_controller("main").start()


class HelloWorldController(controller.Controller):

    def setup(self):
        if self.view is None:
            self._view = HelloWorldView(self.application, self)
        self.view.setup()
        return self

    def start(self):
        self.view.show()

    def stop(self):
        self.view.close()


class HelloWorldView(view.View):

    def setup(self):
        self.grid(sticky="nsew")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        lbl = view.ttk.Label(self, text="Hello World!", font=self.FONT_LARGE)
        self.add_widget("label1", lbl)
        lbl.grid(sticky="nsew")


if __name__ == "__main__":

    app = HelloWorld()
    app.start()
