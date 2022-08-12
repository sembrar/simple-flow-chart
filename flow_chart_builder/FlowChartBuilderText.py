from scrolled_widgets.ScrolledTextFrame import ScrolledTextFrame


class FlowChartTextFrame(ScrolledTextFrame):
    def __init__(self, master=None, kwargs_for_frame=None, **kw_for_text_widget):
        super().__init__(master, horizontal_scroll=True, kwargs_for_frame=kwargs_for_frame, **kw_for_text_widget)


def main():
    from tkinter import Tk
    root = Tk()
    root.title("FlowChartTextFrame")
    widget = FlowChartTextFrame()
    widget.grid(row=0, column=0, sticky='news')
    root.mainloop()
