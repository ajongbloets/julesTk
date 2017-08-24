"""Implements a MVC-style ListBox widget"""

from julesTk import JTkObject
from julesTk.view import *
from julesTk.controller import ViewController

import sys
if sys.version_info[0] < 3:
    import tkMessageBox
else:
    from tkinter import messagebox as tkMessageBox

__all__ = [
    "ListModel", "Listbox", "ListboxController"
]

class ListModel(JTkObject):

    def __init__(self):
        super(ListModel, self).__init__()
        self._data = []

    @property
    def size(self):
        return len(self._data)

    def add(self, item):
        """Add a new item to the list_model"""
        result = None
        if item not in self._data:
            self._data.append(item)
            result = item
            self.trigger_event("item_added", result)
        return result

    def get(self, index):
        result = None
        if 0 <= index < self.size:
            result = self._data[index]
        return result

    def index(self, item):
        result = None
        if item in self._data:
            result = self._data.index(item)
        return result

    def remove(self, item):
        result = None
        if item in self._data:
            self._data.remove(item)
            result = item
            self.trigger_event("item_removed", result)
        return result

    def pop(self, index):
        """Remove item at index"""
        result = None
        item = self.get(index)
        if item is not None:
            result = self.remove(item)
        return result

    @triggers("list_cleared")
    def clear(self):
        self._data = []

    def __contains__(self, item):
        return item in self._data


class Listbox(FrameView):

    def __init__(self, parent, controller=None):
        super(Listbox, self).__init__(parent, controller=controller)

    @property
    def listbox_widget(self):
        """ Return the listbox widget

        :return:
        :rtype: Tkinter.Listbox | tkinter.Listbox
        """
        return self.get_widget("list_model")

    def get_controller(self):
        """Return the Controller of this view

        :return:
        :rtype: ListboxController
        """
        return self._controller

    def get_list(self):
        result = None
        if self.has_controller():
            result = self.get_controller().get_list_model()
        return result

    def _prepare(self):
        frmh = ttk.Frame(self)
        frmh.grid(row=0, column=0, padx=5, sticky="nwe")
        self._prepare_header(frmh)
        frml = ttk.Frame(self, borderwidth=2, relief="sunken")
        # frml.pack(side="top", fill=view.tk.BOTH, expand=1, padx=5)
        frml.grid(row=1, column=0, padx=5, sticky="nswe")
        self._prepare_list(frml)
        # configure grid
        self.configure_column(self, 0)
        self.configure_row(self, 1)

    def _prepare_header(self, parent):
        lbl = ttk.Label(parent)
        lbl.pack(side="left", fill="x", padx=5)
        self.add_widget("title", lbl)
        self._prepare_buttons(parent)

    def _prepare_buttons(self, parent):
        btc = ttk.Button(parent, text="Clear", command=self.clear)
        btc.pack(side='right')

    def _prepare_list(self, parent):
        lb = tk.Listbox(parent, height="8", borderwidth=0)
        lb.bind("<Double-Button-1>", self.edit_item)
        lb.bind("<Button-2>", self.show_popup)
        self._prepare_scrollbar(parent, lb)
        self.add_widget("list_model", lb)

    def _prepare_scrollbar(self, parent, widget, direction="y"):
        if direction in ("y", "both"):
            scby = tk.Scrollbar(parent)
            widget.config(yscrollcommand=scby.set)
            scby.config(command=widget.yview, orient="vertical")
            scby.pack(side='right', fill='y')
            widget.pack(side="left", fill="both", expand=1)
        if direction in ("x", "both"):
            scbx = tk.Scrollbar(parent)
            widget.config(xscrollcommand=scbx.set)
            scbx.config(command=widget.xview, orient="horizontal")
            scbx.pack(side='bottom', fill='x')
            widget.pack(side="top", fill="both", expand=1)

    def get_selected_item(self):
        result = None
        indexes = self.listbox_widget.curselection()
        if len(indexes) > 0:
            result = self.get_list().get(indexes[0])
        return result

    def get_selected_items(self):
        results = []
        indexes = self.listbox_widget.curselection()
        for index in indexes:
            item = self.get_list().get(index)
            if item is not None:
                results.append(item)
        return results

    def add_item(self, event=None):
        self.trigger_event("add_item")

    def edit_item(self, event=None):
        item = self.get_selected_item()
        if item is not None:
            self.trigger_event("edit_item", data=item)

    def delete_item(self, event=None):
        item = self.get_selected_item()
        if item is None:
            self.show_nothing_selected()
        else:
            self.trigger_event("delete_item", data=item)

    def clear(self, event=None):
        self.trigger_event("clear_list")

    def show_popup(self, event):
        """Show pop-up menu when right-clicked on an item"""
        pass

    @receives("item_added")
    def _add_item(self, event, source, item=None):
        if item is not None:
            line = self.item_to_str(item)
            self.listbox_widget.insert('end', line)

    @receives("item_removed")
    def _remove_item(self, event, source, item=None):
        if item is not None:
            index = self.get_controller().get_list_model().index(item)
            self.listbox_widget.delete(index)

    @receives("list_cleared")
    def _clear_list(self, event, source, data=None):
        self.listbox_widget.delete(0, 'end')

    # utils

    def show_nothing_selected(self):
        tkMessageBox.showerror("Nothing selected!", "Please select an item...")

    def item_to_str(self, item):
        return str(item)


class ListboxController(ViewController):

    VIEW_CLASS = Listbox

    def __init__(self, parent, view=None, list_model=None):
        if view is not None and not isinstance(view, Listbox):
            raise ValueError("Invalid view, expected a Listbox")
        if list_model is not None and not isinstance(list_model, ListModel):
            raise ValueError("Invalid list model, expected a ListModel")
        super(ListboxController, self).__init__(parent, view=view)
        self._list = list_model

    def get_list_model(self):
        """Return the List Model

        :return:
        :rtype: julesTk.view.listbox.ListModel
        """
        return self._list

    @property
    def list_model(self):
        return self.get_list_model()

    def has_list_model(self):
        return self.get_list_model() is not None

    def _prepare(self):
        super(ListboxController, self)._prepare()
        if self.has_view() and self.has_list_model():
            self.list_model.add_observer(self.view)

    def _stop(self):
        if self.has_view() and self.has_list_model():
            self.list_model.remove_observer(self.view)
        super(ListboxController, self)._stop()

    @receives("clear_list")
    def event_clear_list(self, *args):
        self.clear_list()

    def clear_list(self):
        self.list_model.clear()

    @receives("add_item")
    def event_add_item(self, *args):
        self.add_item()

    def add_item(self):
        pass    # overload

    @receives("edit_item")
    def event_edit_item(self, event, source, item=None):
        if item is not None:
            self.edit_item(item)

    def edit_item(self, item):
        pass    # overload

    @receives("delete_item")
    def event_delete_item(self, event, source, item=None):
        if item is not None:
            self.delete_item(item)

    def delete_item(self, item):
        pass    # overload
