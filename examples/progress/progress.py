
from julesTk import app, controller, view
from julesTk.controller import poller
from julesTk.utils import progress


class ProgressApp(app.Application):

    def __init__(self):
        super(ProgressApp, self).__init__()

    def _prepare(self):
        self.add_controller("main", MainController(self))

    @property
    def main(self):
        return self.get_controller("main")

    def _start(self):
        self.main.start()


class MainView(view.View):

    def _prepare(self):
        self.application.resizable(False, False)
        self.configure_grid(self)
        btn = view.ttk.Button(self, text="Determinate", command=self.controller.progress_det)
        self.add_widget("button1", btn)
        self.configure_grid(btn, row=0, column=0)
        btn = view.ttk.Button(self, text="Indeterminate", command=self.controller.progress_indet)
        self.add_widget("button2", btn)
        self.configure_grid(btn, row=0, column=1)


class MainController(poller.Poller, controller.ViewController):

    VIEW_CLASS = MainView

    def __init__(self, parent, view=None):
        super(MainController, self).__init__(parent=parent, view=view)
        self._pb = None

    def _prepare(self):
        return controller.ViewController._prepare(self)

    def _start(self):
        controller.ViewController._start(self)

    def progress_det(self):
        self._pb = progress.ProgressBar(self.view, self, mode="determinate", blocking=True)
        self._pb.message = "Please wait.."
        self.interval = 0.1
        self.run()
        self._pb.start()
        self._pb.close()

    def execute(self):
        self._pb.value += 5
        if self._pb.value == 100:
            self.set_polling(False)
            # self._pb.close()

    def progress_indet(self):
        pb = progress.ProgressBar(self.view, self, mode="indeterminate", blocking=False)
        pb.message = "Please wait..."
        pb.title("Operation in progress..")
        pb.start()


if __name__ == "__main__":

    app = ProgressApp()
    app.run()
