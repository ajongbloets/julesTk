"""Example of a application using a progress bar

There are two buttons: determinate and indeterminate.

- Determinate: will track the progress of our very long process and close automatically when done.
- Indeterminate: Shows a "bouncing" progress bar not specific to progress.

"""

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


class MainView(view.FrameView):

    def _prepare(self):
        self.root.resizable(False, False)
        self.configure_grid(self)
        btn = view.ttk.Button(self, text="Determinate", command=self.controller.progress_det)
        self.add_widget("button1", btn)
        self.configure_grid(btn, row=0, column=0)
        btn = view.ttk.Button(self, text="Indeterminate", command=self.controller.progress_indet)
        self.add_widget("button2", btn)
        self.configure_grid(btn, row=0, column=1)


class MainController(controller.ViewController):

    VIEW_CLASS = MainView

    def __init__(self, parent, view=None):
        super(MainController, self).__init__(parent=parent, view=view)
        self._pb = None

    def _prepare(self):
        return controller.ViewController._prepare(self)

    def _start(self):
        controller.ViewController._start(self)

    def progress_det(self):
        self._pb = progress.ProgressBar(self.view, mode="determinate")
        self._pb.view.title("Loading..")
        self._pb.view.message = "Please wait.."
        self._pb.view.geometry('300x100+200+200')
        self._pb.start(self.long_process, block=True, auto_close=True)

    def long_process(self):
        import time
        i = 0
        while i < 100:
            i += 5
            self._pb.increase(5)
            time.sleep(0.1)
        return True

    def progress_indet(self):
        self._pb = progress.ProgressBar(self.view, mode="indeterminate", auto_close=False)
        self._pb.view.message = "Please wait..."
        self._pb.view.title("Operation in progress..")
        self._pb.view.geometry('300x100+200+200')
        self._pb.start(self.long_process)


if __name__ == "__main__":

    app = ProgressApp()
    app.run()
