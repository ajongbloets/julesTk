"""A simple view with a text box, to display log messages obtained from the stream handler"""

from julesTk import view

__author__ = "Joeri Jongbloets <j.a.jongbloets@uva.nl>"


class LogView(view.Frame):
    """A view to show log messages"""

    def __init__(self, parent):
        super(LogView, self).__init__(parent=parent)
        self._text = view.tk.Text(self)
        self._text.config(state="disabled")
        self._text.bind("<1>", lambda event: self._text.focus_set())
        self._text.pack(fill=view.tk.BOTH, expand=1)

    @property
    def text(self):
        """The text widget"""
        return self._text

    def write(self, message):
        """Write a message to the console"""
        self._text.config(state="normal")
        self._text.insert(view.tk.END, message)
        self._text.config(state="disabled")

    def flush(self):
        pass

    def clear(self, event=None):
        """Remove all messages from the console"""
        self._text.config(state="normal")
        self._text.delete(1.0, view.tk.END)
        self._text.config(state="disabled")
