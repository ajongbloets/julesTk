
from julesTk import app, controller, view
from julesTk.view.listbox import *

__author__ = "Joeri Jongbloets <joeri@jongbloets.net>"


class ListboxExample(app.Application):

    def __init__(self):
        super(ListboxExample, self).__init__()

    def _prepare(self):
        self.root.title("Listbox Example")
        self.root.wm_minsize(200, 300)
        self.add_controller("main", ListboxExampleController(self))
        return True

    @property
    def main(self):
        return self.get_controller("main")

    def _start(self):
        self.main.start()


class ListboxExampleView(view.FrameView):

    @property
    def listbox(self):
        result = None
        if self.has_widget("listbox"):
            result = self.get_widget("listbox")
        return result

    def _prepare(self):
        self.configure_grid(self)
        # parent should also resize with window
        self.configure_row(self.parent, 0)
        self.configure_column(self.parent, 0)
        lb = Listbox(self, title="Example")
        self.add_widget("listbox", lb)
        lbc = ListboxController(self.controller, lb, self.controller.model)
        lbc.start()
        lb.pack(side="top", fill='both', expand=1, padx=10, pady=10)
        frmf = view.ttk.Frame(self)
        frmf.pack(side='bottom', fill='x', padx=10, pady=10)
        self._prepare_footer(frmf)
        return True

    def _prepare_footer(self, parent):
        # button to add items
        bta = view.ttk.Button(parent, text="+", command=self.add_item)
        bta.pack(side="right", fill='y')
        btd = view.ttk.Button(parent, text="-", command=self.remove_item)
        btd.pack(side="right", fill='y')

    def add_item(self):
        index = 0
        if len(self.controller.model) > 0:
            index = max(self.controller.model) + 1
        self.controller.model.add(index)

    def remove_item(self):
        index = self.listbox.get_selected_index()
        if index is not None:
            self.controller.model.pop(index)


class ListboxExampleController(controller.ViewController):

    VIEW_CLASS = ListboxExampleView

    def __init__(self, parent, v=None):
        super(ListboxExampleController, self).__init__(parent, view=v)
        self._model = ListModel()

    @property
    def model(self):
        return self._model

if __name__ == "__main__":

    app = ListboxExample()
    app.run()
