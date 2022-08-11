from tkinter import Canvas as _tkCanvas
from tkinter import ttk as _ttk
from tkinter import constants as _tk_constants


"""
ScrolledCanvasFrame is a ttk Frame that has a Tkinter Canvas inside it with scrollbars attached to it
The Canvas widget can be accessed using "canvas" attribute. Eg: scrolled_canvas_frame.canvas 

When required, call "reset_scroll_region" function, to recalculate and set scroll region
"""


class ScrollCanvasFrame(_ttk.Frame):

    def __init__(self, master=None, vertical_scroll=True, horizontal_scroll=True,
                 kwargs_for_frame=None, **kwargs_for_canvas):
        """
        :param master:
        :param vertical_scroll:
        :param horizontal_scroll:
        :param kwargs_for_frame: these are the keyword arguments dictionary for the frame that holds
         the Canvas widget and the scrollbars
        :param kwargs_for_canvas: there are the keyword arguments for Canvas widget
        """

        if kwargs_for_frame is None:
            kwargs_for_frame = {}
        super().__init__(master, **kwargs_for_frame)

        self.canvas = _tkCanvas(self, **kwargs_for_canvas)
        self.canvas.grid(row=0, column=0, sticky='news')
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self._v_scroll = None
        if vertical_scroll:
            self._v_scroll = _ttk.Scrollbar(self, orient=_tk_constants.VERTICAL, command=self.canvas.yview)
            self._v_scroll.grid(row=0, column=1, sticky='ns')
            self.canvas.configure(yscrollcommand=self._v_scroll.set)

        self._h_scroll = None
        if horizontal_scroll:
            self._h_scroll = _ttk.Scrollbar(self, orient=_tk_constants.HORIZONTAL, command=self.canvas.xview)
            self._h_scroll.grid(row=1, column=0, sticky='ew')
            self.canvas.configure(xscrollcommand=self._h_scroll.set)

    def reset_scroll_region(self, padding_at_boundary=0):
        # canvas's .bbox should return the bbox enclosing all objects if tagOrId parameter is not specified, but,
        # it is not working, so, need to manually determine the bbox enclosing all objects

        all_canvas_objects = self.canvas.find_all()
        if len(all_canvas_objects) == 0:
            return

        x_min, y_min, x_max, y_max = self.canvas.bbox(all_canvas_objects[0])

        for i in range(1, len(all_canvas_objects)):
            x1, y1, x2, y2 = self.canvas.bbox(all_canvas_objects[i])
            if x_min > x1:
                x_min = x1
            if y_min > y1:
                y_min = y1
            if x_max < x2:
                x_max = x2
            if y_max < y2:
                y_max = y2

        self.canvas.configure(
            scrollregion=(x_min - padding_at_boundary, y_min - padding_at_boundary,
                          x_max + padding_at_boundary, y_max + padding_at_boundary))  # tuple is (w, n, e, s)


if __name__ == '__main__':
    from tkinter import Tk

    root = Tk()

    scrolled_canvas_frame = ScrollCanvasFrame(root)
    scrolled_canvas_frame.grid(row=0, column=0, sticky='news')
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    scrolled_canvas_frame.canvas.create_line(0, 0, 1000, 1000)
    scrolled_canvas_frame.reset_scroll_region()

    root.mainloop()
