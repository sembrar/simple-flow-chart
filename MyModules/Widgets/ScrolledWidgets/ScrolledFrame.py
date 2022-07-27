from MyModules.Widgets.ScrolledWidgets.ScrolledCanvas import ScrolledCanvas
import tkinter as _tk
from tkinter import ttk as _ttk
from queue import Queue as _Queue


class ScrolledFrame(_tk.Frame):

    def __init__(self, master=None, vertical_scroll=True, horizontal_scroll=True, **kw):
        self._scrolled_canvas = ScrolledCanvas(master=master, horizontal_scroll=horizontal_scroll,
                                               vertical_scroll=vertical_scroll, bg='blue', confine=True)
        super().__init__(self._scrolled_canvas, bg='red', **kw)
        self._frame_id = self._scrolled_canvas.create_window(0, 0, window=self, anchor='nw')

        self.bind("<Configure>", self.set_scroll_region)
        self._scrolled_canvas.bind("<Configure>", self.frame_fill)

    def set_scroll_region(self, *_):
        frame_width = self.winfo_width()
        frame_height = self.winfo_height()
        self._scrolled_canvas.configure(scrollregion=(0, 0, frame_width, frame_height))
        self._bind_all_good_children_to_mouse_scroll()

    def frame_fill(self, *_):
        frame_width = self.winfo_reqwidth()
        frame_height = self.winfo_reqheight()
        canvas_width = self._scrolled_canvas.winfo_width()
        canvas_height = self._scrolled_canvas.winfo_height()

        if frame_width < canvas_width:
            self._scrolled_canvas.itemconfigure(self._frame_id, width=canvas_width-4)

        if frame_height < canvas_height:
            self._scrolled_canvas.itemconfigure(self._frame_id, height=canvas_height-4)

    @staticmethod
    def get_clean_event_dict_for_mouse_scroll(event):
        new_dict = {}
        for e in event.__dict__:
            if event.__dict__[e] == '??' or e in ('type', 'widget', 'num'):
                continue
            new_dict[e] = event.__dict__[e]
        if 'x_root' in new_dict:
            new_dict['rootx'] = new_dict.pop('x_root')
        if 'y_root' in new_dict:
            new_dict['rooty'] = new_dict.pop('y_root')
        return new_dict

    def mouse_v_scroll(self, event):
        self._scrolled_canvas.event_generate("<MouseWheel>", **self.get_clean_event_dict_for_mouse_scroll(event))

    def mouse_h_scroll(self, event):
        self._scrolled_canvas.event_generate("<Control-MouseWheel>",
                                             **self.get_clean_event_dict_for_mouse_scroll(event))

    def _bind_all_good_children_to_mouse_scroll(self, **optional_class_and_bool):
        """
        :type kwargs: dict[class, bool]
        """
        available_classes = (_tk.Button, _tk.Checkbutton, _tk.Frame, _tk.Label, _tk.LabelFrame, _tk.Message,
                             _tk.OptionMenu, _tk.PanedWindow, _tk.Radiobutton, _tk.Scale, _tk.Spinbox,
                             _ttk.Button, _ttk.Checkbutton, _ttk.Frame, _ttk.Label, _ttk.LabelFrame, _ttk.Notebook,
                             _ttk.PanedWindow, _ttk.Radiobutton, _ttk.Scale)

        for c in available_classes:
            if c not in optional_class_and_bool:
                optional_class_and_bool[c] = True

        widgets = _Queue()
        widgets.put(self)
        while not widgets.empty():
            w = widgets.get()
            # print(w, type(w))

            if w == self or (type(w) in optional_class_and_bool and optional_class_and_bool[type(w)]):
                w.bind("<MouseWheel>", self.mouse_v_scroll)
                w.bind("<Control-MouseWheel>", self.mouse_h_scroll)

            children = w.winfo_children()
            for child in children:
                widgets.put(child)

    def grid(self, **kw):
        self._scrolled_canvas.grid(**kw)

    def grid_bbox(self, column=None, row=None, col2=None, row2=None):
        return self._scrolled_canvas.grid_bbox(column, row, col2, row2)

    def grid_forget(self):
        self._scrolled_canvas.grid_forget()

    def grid_info(self):
        return self._scrolled_canvas.grid_info()

    def grid_location(self, x, y):
        return self._scrolled_canvas.grid_location(x, y)

    def grid_propagate(self, flag=0):
        return self._scrolled_canvas.grid_propagate(flag)

    def grid_remove(self):
        self._scrolled_canvas.grid_remove()

    def grid_size(self):
        return self._scrolled_canvas.grid_size()
