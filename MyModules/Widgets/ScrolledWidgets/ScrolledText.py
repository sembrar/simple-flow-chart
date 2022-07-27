from tkinter import Text as _tkText
from tkinter import ttk as _ttk
from tkinter import constants as _tk_constants


class ScrolledText(_tkText):

    def __init__(self, master=None, vertical_scroll=True, horizontal_scroll=False, allow_keyboard_input=True, **kw):

        self._all_container = _ttk.Frame(master=master)

        super().__init__(self._all_container, **kw)

        _tkText.grid(self, row=0, column=0, sticky='nsew')
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._v_scroll = None
        if vertical_scroll:
            self._v_scroll = _ttk.Scrollbar(self._all_container, orient=_tk_constants.VERTICAL, command=self.yview)
            self._v_scroll.grid(row=0, column=1, sticky='ns')
            self.configure(yscrollcommand=self._v_scroll.set)

        self._h_scroll = None
        if horizontal_scroll:
            self._h_scroll = _ttk.Scrollbar(self._all_container, orient=_tk_constants.HORIZONTAL, command=self.xview)
            self._h_scroll.grid(row=1, column=0, sticky='ew')
            self.configure(xscrollcommand=self._h_scroll.set, wrap=_tk_constants.NONE)

        if not allow_keyboard_input:
            self.bind('<Key>', lambda *_: 'break')

    def disable_key_board_input(self):
        self.bind('<Key>', lambda *_: 'break')

    def enable_key_board_input(self):
        self.bind('<Key>', lambda *_: True)

    def destroy(self):
        if self._h_scroll is not None:
            self._h_scroll.destroy()
        if self._v_scroll is not None:
            self._v_scroll.destroy()
        _tkText.destroy(self)
        self._all_container.destroy()

    def grid(self, **kw):
        self._all_container.grid(**kw)

    def grid_bbox(self, column=None, row=None, col2=None, row2=None):
        return self._all_container.grid_bbox(column, row, col2, row2)

    def grid_forget(self):
        self._all_container.grid_forget()

    def grid_info(self):
        return self._all_container.grid_info()

    def grid_location(self, x, y):
        return self._all_container.grid_location(x, y)

    def grid_propagate(self, flag=0):
        return self._all_container.grid_propagate(flag)

    def grid_remove(self):
        self._all_container.grid_remove()

    def grid_size(self):
        return self._all_container.grid_size()

    def grid_slaves(self, row=None, column=None):
        return self._all_container.grid_slaves(row, column)

    def grid_configure(self, **kw):
        self._all_container.grid_configure(**kw)

    def grid_anchor(self, anchor=None):
        self._all_container.grid_anchor(anchor)

    def grid_columnconfigure(self, index, **kw):
        return self._all_container.grid_columnconfigure(index, **kw)

    def grid_rowconfigure(self, index, **kw):
        return self._all_container.grid_rowconfigure(index, **kw)

    def rowconfigure(self, index, **kw):
        self._all_container.rowconfigure(index, **kw)

    def columnconfigure(self, index, **kw):
        self._all_container.columnconfigure(index, **kw)
