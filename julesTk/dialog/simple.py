from julesTk import view
from julesTk.dialog import DialogTemplate


class MessageBox(DialogTemplate):

    def __init__(self, parent, ctrl, buttons=None):
        super(MessageBox, self).__init__(parent, ctrl)
        self._message = view.tk.StringVar("")
        if buttons is None:
            buttons = []
        if len(buttons) == 0:
            buttons = [{"id": "ok", "caption": "Ok", "value": True}]
        self._buttons = buttons

    @property
    def message(self):
        return self._message.get()

    @message.setter
    def message(self, v):
        self._message.set(v)

    def _prepare_body(self, parent):
        lbm = view.ttk.Label(parent, textvariable=self._message)
        lbm.pack(side=view.tk.TOP, fill=view.tk.BOTH, expand=1)

    def _prepare_footer(self, parent):
        idx = 0
        for button in self._buttons:
            # get button id
            name = button.get("id", None)
            if name is None:
                name = idx
                idx += 1
            # get caption
            caption = button.get("caption", name)
            # get return value
            value = button.get("value", name)
            # check if set to default
            is_default = button.get("default", False)
            if is_default:
                self._response = value
            # add button
            btn = self.make_button(parent, name, caption, value, is_default)
            btn.pack(side=view.tk.LEFT, padx=5)

    def make_button(self, parent, name, caption, value, is_default=False):
        """Creates a button"""
        default = view.tk.ACTIVE if is_default else view.tk.NORMAL
        btn = view.ttk.Button(
            parent, text=caption, default=default,
            command=lambda i=value: self.process_click(i)
        )
        # add_observer button in registry
        self.add_widget(name, btn)
        return btn

    def process_click(self, value):
        self._response = value
        self.close()


def inform(parent, title, message, buttons=None):
    """Show a messagebox"""
    if not isinstance(parent, (view.tk.Tk, view.tk.Frame, view.JTkView)):
        raise ValueError("Expected a controller not a {}".format(type(parent)))
    mb = MessageBox(parent, None, buttons=buttons)
    mb.title(title)
    mb.message = message
    mb.show()
    return mb.response


