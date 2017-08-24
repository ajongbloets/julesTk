"""Implement Dialogs"""

from julesTk import view
from julesTk.view.window import ModalWindow

__all__ = [
    "BaseDialog", "DialogTemplate"
]


class BaseDialog(ModalWindow):
    """Implement basic dialog functions"""

    def __init__(self, parent, ctrl):
        super(BaseDialog, self).__init__(parent, ctrl)
        self._response = None

    @property
    def response(self):
        return self._response

    def _prepare(self):
        raise NotImplementedError


class DialogTemplate(BaseDialog):
    """Basic template with a header, body and footer"""

    def _prepare(self):
        self.grid()
        self.configure_column(self, 0)
        self.configure_row(self, [0, 1, 2])
        # header
        fmh = self.add_widget(
            "header", view.ttk.Frame(self)
        )
        self._prepare_header(fmh)
        self.configure_grid(fmh, row=0, column=0)
        # body
        fmb = self.add_widget(
            "body", view.ttk.Frame(self)
        )
        self._prepare_body(fmb)
        self.configure_grid(fmb, row=1, column=0)
        # footer
        fmf = self.add_widget(
            "footer", view.ttk.Frame(self)
        )
        self._prepare_footer(fmf)
        self.configure_grid(fmf, row=2, column=0)

    def _prepare_header(self, parent):
        """Header of the dialog"""
        return True  # override

    def _prepare_body(self, parent):
        """Build the body of the dialog, parent refers to parent frame"""
        return True  # override

    def _prepare_footer(self, parent):
        """Build the buttons of the dialog, parent refers to parent frame"""
        return True  # override

    def validate(self):
        return True  # override
