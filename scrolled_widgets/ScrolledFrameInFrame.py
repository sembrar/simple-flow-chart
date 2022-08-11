from tkinter import ttk as _ttk

from .ScrolledCanvasFrame import ScrollCanvasFrame as _ScrollCanvasFrame


"""
ScrolledFrameInFrame is inherited from ScrollCanvasFrame which is a frame with a canvas and scrollbars
ScrolledFrameInFrame has a frame named "inner_scrolled_frame" added to the canvas
The Configure event of "inner_scrolled_frame" is bound to run "reset_scroll_region" function of ScrollCanvasFrame class
New widgets can be added to this "inner_scrolled_frame"
Eg (adding a label to the "inner_scrolled_frame":
 new_label = ttk.Label(master=scrolled_frame_in_frame.inner_scrolled_frame, text="Example label")
 new_label.grid(row=0, column=0)  
"""


class ScrolledFrameInFrame(_ScrollCanvasFrame):

    def __init__(self, master=None, kwargs_for_frame=None, kwargs_for_canvas=None, **kwargs_for_inner_scrolled_frame):
        """
        :param master:
        :param kwargs_for_frame: these are keyword arguments for the frame that holds the canvas and the scrollbars
        :param kwargs_for_canvas: these are keyword arguments for the canvas
        :param kwargs_for_inner_scrolled_frame: these are the keyword arguments for the inner_scrolled_frame to which
         new widgets are added
        """

        if kwargs_for_frame is None:
            kwargs_for_frame = {}
        if kwargs_for_canvas is None:
            kwargs_for_canvas = {}
        super().__init__(master, kwargs_for_frame=kwargs_for_frame, **kwargs_for_canvas)

        self.inner_scrolled_frame = _ttk.Frame(self.canvas, **kwargs_for_inner_scrolled_frame)
        self.canvas.create_window(0, 0, anchor="nw", window=self.inner_scrolled_frame)

        self.inner_scrolled_frame.bind("<Configure>", self._inner_frame_configured)
        self.bind("<Configure>", self._inner_frame_configured)

    def _inner_frame_configured(self, _):
        self.reset_scroll_region()


if __name__ == '__main__':
    from tkinter import Tk
    import random

    root = Tk()

    scrolled_frame_in_frame = ScrolledFrameInFrame(root, kwargs_for_canvas={"height": 500, "width": 500})
    scrolled_frame_in_frame.grid(row=0, column=0, sticky='news')
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    # insert some random data
    random.seed("this is a seed")
    for i in range(100):
        text = f"{i + 1}: " + " ".join(map(str, range(random.randint(1, 200)))) + "\n"
        _ttk.Label(scrolled_frame_in_frame.inner_scrolled_frame, text=text).grid(row=i, column=0, sticky='w')

    root.mainloop()
