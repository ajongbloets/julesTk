"""A simple view with a text box, to display log messages obtained from the stream handler"""

from julesTk import view

__author__ = "Joeri Jongbloets <joeri@jongbloets.net>"


class LogView(view.Frame):
    """A view to show log messages"""

    def __init__(self, parent):
        super(LogView, self).__init__(parent=parent)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        xscroll = view.tk.Scrollbar(self, orient=view.tk.HORIZONTAL)
        xscroll.grid(row=1, column=0, sticky="ew")

        yscroll = view.tk.Scrollbar(self)
        yscroll.grid(row=0, column=1, sticky="ns")

        self._text = view.tk.Text(
            self, wrap="none",
            xscrollcommand=xscroll.set,
            yscrollcommand=yscroll.set
        )
        self._text.config(state="disabled")
        self._text.bind("<1>", lambda event: self._text.focus_set())

        self._text.grid(row=0, column=0, sticky="nsew")

        xscroll.config(command=self._text.xview)
        yscroll.config(command=self._text.yview)

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
