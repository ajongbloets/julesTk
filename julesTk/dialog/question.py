
from julesTk import view
from julesTk.dialog import DialogTemplate


class QuestionBox(DialogTemplate):
    """Creates a Modal Question Box"""

    def __init__(self, parent, ctrl):
        super(QuestionBox, self).__init__(parent, ctrl)
        self._question = view.tk.StringVar(self)
        self._answer = view.tk.StringVar(self)
        self._error = view.tk.StringVar(self)

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

    def _prepare_header(self, parent):
        # add question
        lbq = view.ttk.Label(parent, textvariable=self._question)
        self.configure_grid(
            lbq, padx=10, pady=5
        )

    def _prepare_body(self, parent):
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

    def _prepare_footer(self, parent):
        self.configure_column(parent, [0, 1])
        # add cancel
        view.ttk.Button(
            parent, text="Cancel", command=self.cancel
        ).pack(side=view.tk.LEFT)
        self.bind("<Escape>", self.cancel)
        # add ok
        view.ttk.Button(
            parent, text="Ok", command=self.ok
        ).pack(side=view.tk.LEFT)
        self.bind("<Return>", self.ok)

    def validate(self):
        response = self._answer.get()
        result = response not in (None, "")
        if not result:
            self.error = "Please provide an answer"
            self.show_validation_msg()
        return result

    def cancel(self, event=None):
        self.close()

    def ok(self, event=None):
        if self.validate():
            self._response = self._answer.get()
            self.close()


def ask_question(parent, question, default=None):
    """Show a dialog, asking a question"""
    if not isinstance(parent, (view.tk.Tk, view.tk.Frame, view.JTkView)):
        raise ValueError("Expected a view as parent, not a {}".format(type(parent)))
    qb = QuestionBox(parent, None)
    qb.question = question
    qb._response = default
    qb.answer = default
    qb.show()
    return qb.response
