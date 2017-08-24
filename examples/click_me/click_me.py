
from julesTk import app, controller, view, model
from julesTk.utils.observe import Observer

__author__ = "Joeri Jongbloets <joeri@jongbloets.net>"


class ClickMeApp(app.Application):

    def __init__(self):
        super(ClickMeApp, self).__init__()

    def _prepare(self):
        self.add_controller("main", MainController(self))

    @property
    def main(self):
        return self.get_controller("main")

    def _start(self):
        self.main.start()


class MainView(view.FrameView):

    def _prepare(self):
        # resize uniform over rows/columns with window
        self.grid(sticky="nsew")
        self.configure_column(self, [0, 1], uniform="foo")
        self.configure_row(self, [0, 1], uniform="foo")
        # parent should also resize
        self.configure_row(self.parent, 0)
        self.configure_column(self.parent, 0)
        lbl = view.ttk.Label(self, text="Hello World!", font=self.FONT_LARGE)
        self.add_widget("label1", lbl)
        lbl.grid(sticky="nsew", columnspan=2, padx=10, pady=10)
        btn = view.ttk.Button(self, text="Click Me!", command=self.clicked)
        self.add_widget("button", btn)
        btn.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        v = self.add_variable("clicks", view.tk.IntVar())
        lbl = view.ttk.Label(self, textvariable=v)
        self.add_widget("label2", lbl)
        lbl.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

    def clicked(self):
        self.controller.add_click()

    @property
    def clicks(self):
        return self.get_variable("clicks").get()

    @clicks.setter
    def clicks(self, v):
        self.get_variable("clicks").set(v)


class ClickModel(model.Model):

    def __init__(self):
        super(ClickModel, self).__init__()
        self.reset()

    @model.Model.thread_safe
    def reset(self):
        self._data = 0
        self.notify_observers()

    @model.Model.thread_safe
    def update(self):
        self._data += 1
        self.notify_observers()


class MainController(controller.Controller, Observer):

    VIEW_CLASS = MainView

    def _prepare(self):
        super(MainController, self)._prepare()
        if self.model is None:
            self.model = ClickModel()
            self.model.register_observer(self)
        return self

    def update(self, observable):
        if isinstance(observable, ClickModel):
            self.view.clicks = observable.data

    def add_click(self):
        self.model.update()


if __name__ == "__main__":

    app = ClickMeApp()
    app.run()
