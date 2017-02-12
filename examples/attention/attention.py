
from julesTk import app, controller, view
from julesTk.utils import modals


class AttentionApp(app.Application):

    def __init__(self):
        super(AttentionApp, self).__init__()

    def _prepare(self):
        self.add_controller("main", MainController(self))

    @property
    def main(self):
        return self.get_controller("main")

    def _start(self):
        self.main.start()


class MainView(view.View):

    def _prepare(self):
        self.configure_grid(self)
        self.configure_column(self, [0, 1])
        self.configure_row(self, [0, 1])
        btn = view.ttk.Button(self, text="Attention 1", command=self.attention)
        self.add_widget("button1", btn)
        self.configure_grid(btn, row=0, column=0)
        btn = view.ttk.Button(self, text="Attention 2", command=self.alert)
        self.add_widget("button2", btn)
        self.configure_grid(btn, row=0, column=1)
        lbd = view.ttk.Label(self, text="Your response:")
        self.add_widget("description", lbd)
        self.configure_grid(lbd, row=1, column=0)
        response = view.tk.StringVar(self)
        self.add_variable("response", response)
        lbr = view.ttk.Label(self, textvariable=response)
        self.add_widget("response", lbr)
        self.configure_grid(lbr, row=1, column=1)

    def attention(self):
        self.controller.attention()

    def alert(self):
        self.controller.alert()

    @property
    def response(self):
        return self.get_variable("response").get()

    @response.setter
    def response(self, value):
        self.get_variable("response").set(value)


class MainController(controller.ViewController):

    VIEW_CLASS = MainView

    def attention(self):
        alert = AlertController(self).prepare()
        alert.start()
        self.view.response = "Undefined"
        if alert.response is True:
            self.view.response = "Yes"
        if alert.response is False:
            self.view.response = "No"

    def alert(self):
        alert = modals.MessageBox(self.view, self, [
            {'id': 'no', 'caption': 'No', 'value': "No", 'default': True},
            {'id': 'yes', 'caption': 'Yes', 'value': "Yes"}
        ])
        alert.title = "YES or NO?"
        alert.message = "YES or NO?"
        alert.start()
        self.view.response = alert.response


class Alert(modals.Dialog):

    def body(self, parent):
        lbl = view.ttk.Label(parent, text="YES or NO?")
        self.add_widget("label", lbl)

    def footer(self, parent):
        btn = view.ttk.Button(parent, text="No", command=self.no)
        self.add_widget("no", btn)
        self.configure_grid(btn, row=1, column=0)
        bty = view.ttk.Button(parent, text="Yes", command=self.yes)
        self.add_widget("yes", bty)
        self.configure_grid(bty, row=1, column=2)

    def _close(self):
        self.no()

    def no(self):
        self._response = False
        self.destroy()

    def yes(self):
        self._response = True
        self.destroy()


class AlertController(controller.ViewController):

    VIEW_CLASS = Alert

    def _start(self):
        return self.view.show()

    @property
    def response(self):
        return self.view.response

if __name__ == "__main__":

    app = AttentionApp()
    app.run()
