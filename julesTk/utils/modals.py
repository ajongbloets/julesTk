"""Classes for creating basic modal dialogs

Such as YES-NO, Question, Information dialogs etc.

"""

from julesTk.controller.window import WindowController
from julesTk import view, controller
from julesTk.view.window import Window

__author__ = "Joeri Jongbloets <joeri@jongbloets.net>"


class ModalWindow(Window):

    def __init__(self, parent, controller):
        super(ModalWindow, self).__init__(parent, controller)
        self.application.register_hook("APP_CLOSE", self.hide)

    def _prepare(self):
        raise NotImplementedError

    def _show(self):
        super(ModalWindow, self)._show()
        self.transient(self.parent)
        self.grab_set()
        self.application.wait_window(self)

    def _hide(self):
        return False

    def _close(self):
        self.application.remove_hook("APP_CLOSE", self.hide)
        super(ModalWindow, self)._close()


class Dialog(ModalWindow):

    def __init__(self, parent, controller):
        super(Dialog, self).__init__(parent, controller)
        self._response = None

    @property
    def response(self):
        """Returns the input of the user given in the ModalWindow

        Developers can use this communicate the input of the window to the controller
        """
        return self._response

    def _prepare(self):
        self.grid()
        self.configure_column(self, 0)
        self.configure_row(self, [0, 1, 2])
        # header
        fmh = self.add_widget(
            "header", view.ttk.Frame(self)
        )
        self.header(fmh)
        self.configure_grid(fmh, row=0, column=0)
        # body
        fmb = self.add_widget(
            "body", view.ttk.Frame(self)
        )
        self.body(fmb)
        self.configure_grid(fmb, row=1, column=0)
        # footer
        fmf = self.add_widget(
            "footer", view.ttk.Frame(self)
        )
        self.footer(fmf)
        self.configure_grid(fmf, row=2, column=0)

    def header(self, parent):
        """Header of the dialog"""
        return True  ## override

    def body(self, parent):
        """Build the body of the dialog, parent refers to parent frame"""
        return True  ## override

    def footer(self, parent):
        """Build the buttons of the dialog, parent refers to parent frame"""
        return True  ## override

    def validate(self):
        return True  ## override

    def start(self):
        self.show()


class MessageBox(Dialog):

    def __init__(self, parent, controller, buttons=None):
        """ Initialize a MessageBox

        :param parent:
        :type parent:
        :param controller:
        :type controller:
        :param buttons: List of button definitions.
            A button definition is dictionary with the keys: id, caption, value
        :type buttons: list[dict[str, str | int | float]]
        """
        super(MessageBox, self).__init__(parent, controller)
        self._message = view.tk.StringVar("")
        if buttons is None:
            buttons = []
        if len(buttons) == 0:
            buttons = [{"id": "ok", "caption": "Ok", "value": True}]
        self._buttons = buttons
        self._functions = {}

    @classmethod
    def alert(cls, parent, title, message, buttons=None):
        """Show an alert"""
        if not isinstance(parent, controller.BaseController):
            raise ValueError("Expected a controller not a {}".format(type(parent)))
        mb = cls(parent.view, parent, buttons=buttons)
        mb.title = title
        mb.message = message
        mb.show()

    @property
    def message(self):
        return self._message.get()

    @message.setter
    def message(self, value):
        self._message.set(value)

    def body(self, parent):
        lbm = view.ttk.Label(parent, textvariable=self._message)
        self.configure_grid(lbm, padx=10, pady=5)

    def footer(self, parent):
        idx = 0
        for col, button in enumerate(self._buttons):
            btn = None
            # get button id
            id_ = button.get("id", None)
            if id_ is None:
                id_ = idx
                idx += 1
            # get caption
            caption = button.get("caption", id_)
            # get return value
            value = button.get("value", id_)
            # check if set to default
            default = button.get("default", False)
            if default:
                self._response = value
            # add button
            btn = view.ttk.Button(
                parent, text=caption,
                default=view.tk.ACTIVE if default else view.tk.NORMAL,
                command=lambda i=value: self.process_click(i)
            )
            self.add_widget(id_, btn)
            btn.pack(side=view.tk.LEFT, padx=5)

    def process_click(self, value):
        self._response = value
        self.close()


class QuestionBox(Dialog):

    def __init__(self, parent, controller):
        super(QuestionBox, self).__init__(parent, controller)
        self._question = view.tk.StringVar(self)
        self._answer = view.tk.StringVar(self)
        self._error = view.tk.StringVar(self)

    @classmethod
    def ask(cls, parent, question, default=None):
        if not isinstance(parent, controller.BaseController):
            raise ValueError("Expected a controller not a {}".format(type(parent)))
        qb = cls(parent.view, parent)
        qb.question = question
        qb._response = default
        qb.answer = default
        qb.show()
        return qb.response

    @property
    def question(self):
        return self._question.get()

    @question.setter
    def question(self, value):
        self._question.set(value)

    @property
    def answer(self):
        return self._answer.get()

    @answer.setter
    def answer(self, value):
        value = "" if value is None else value
        self._answer.set(value)

    @property
    def error(self):
        return self._error

    @error.setter
    def error(self, text):
        self._error.set(text)

    def show_validation_msg(self):
        lbv = self.get_widget("validate")
        lbv.grid()

    def hide_validation_msg(self):
        lbv = self.get_widget("validate")
        lbv.grid_remove()

    def header(self, parent):
        # add question
        lbq = view.ttk.Label(parent, textvariable=self._question)
        self.configure_grid(
            lbq, padx=10, pady=5
        )

    def body(self, parent):
        # add answer
        ena = view.ttk.Entry(
            parent, textvariable=self._answer
        )
        self.configure_grid(
            ena, padx=15, pady=5
        )
        # add validation
        view.ttk.Style().configure(
            "Error.TLabel", foreground="red"
        )
        lbv = view.ttk.Label(
            parent, textvariable=self._error, style="Error.TLabel"
        )
        self.add_widget("validate", lbv)
        self.configure_grid(
            lbv, row=1, padx=20
        )
        self.hide_validation_msg()

    def footer(self, parent):
        self.configure_column(parent, [0, 1])
        # add cancel
        view.ttk.Button(
            parent, text="Cancel", command=self.cancel
        ).pack(side=view.tk.LEFT)
        self.bind("<Escape>", lambda x: self.cancel())
        # add ok
        view.ttk.Button(
            parent, text="Ok", command=self.ok
        ).pack(side=view.tk.LEFT)
        self.bind("<Return>", lambda x: self.ok())

    def validate(self):
        response = self._answer.get()
        result = response not in (None, "")
        if not result:
            self.error = "Please provide an answer"
            self.show_validation_msg()
        return result

    def cancel(self):
        self.close()

    def ok(self):
        if self.validate():
            self._response = self._answer.get()
            self.close()
