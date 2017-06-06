
from julesTk import app, controller, view
from julesTk.utils.modals import QuestionBox


class QuestionApp(app.Application):

    def __init__(self):
        super(QuestionApp, self).__init__()

    def _prepare(self):
        self.add_controller("main", MainController(self))

    @property
    def main(self):
        return self.get_controller("main")

    def start(self):
        self.main.start()


class MainView(view.View):

    def _prepare(self):
        # prevent resize
        self.root.resizable(False, False)
        # layout this frame
        self.configure_grid(self)
        btn = view.ttk.Button(self, text="Ask!", command=self.ask_question)
        self.add_widget("button", btn)
        self.configure_grid(btn, row=0, column=0, columnspan=2)
        lbd = view.ttk.Label(self, text="Your said:")
        self.add_widget("description", lbd)
        self.configure_grid(lbd, row=1, column=0)
        response = view.tk.StringVar(self)
        self.add_variable("response", response)
        lbr = view.ttk.Label(self, textvariable=response)
        self.add_widget("response", lbr)
        self.configure_grid(lbr, row=1, column=1)

    def ask_question(self):
        self.controller.ask_question()

    @property
    def response(self):
        return self.get_variable("response").get()

    @response.setter
    def response(self, value):
        self.get_variable("response").set(value)


class MainController(controller.ViewController):

    VIEW_CLASS = MainView

    def ask_question(self):
        self.view.response = QuestionBox.ask(
            self.view, "What is your name?"
        )


if __name__ == "__main__":

    app = QuestionApp()
    app.run()
