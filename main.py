import argparse
import os

import tkinter
from tkinter import ttk

from MyModules.Widgets.ScrolledWidgets.ScrolledCanvas import ScrolledCanvas
from MyModules.Widgets.ScrolledWidgets.ScrolledText import ScrolledText


class FlowChart(tkinter.Tk):

    def __init__(self, commands_text_file_path=None):
        tkinter.Tk.__init__(self)
        self.title("FlowChart")

        paned_window = ttk.Panedwindow(self, orient=tkinter.HORIZONTAL)
        paned_window.grid(row=0, column=0, sticky='news')
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self._label_frame_for_canvas = ttk.Labelframe(paned_window, text="FlowChart")
        # the above is saved in var to be able to change title
        paned_window.add(self._label_frame_for_canvas)

        label_frame_for_text = ttk.Labelframe(paned_window, text="Text: Commands")
        paned_window.add(label_frame_for_text)

        self._canvas = ScrolledCanvas(self._label_frame_for_canvas, bg="light blue")
        self._canvas.grid(row=0, column=0, sticky='news')
        self._label_frame_for_canvas.rowconfigure(0, weight=1)
        self._label_frame_for_canvas.columnconfigure(0, weight=1)

        self._text = ScrolledText(label_frame_for_text, horizontal_scroll=True)
        self._text.grid(row=0, column=0, sticky='news')
        label_frame_for_text.rowconfigure(0, weight=1)
        label_frame_for_text.columnconfigure(0, weight=1)

        if commands_text_file_path is not None:
            try:
                with open(commands_text_file_path) as f:
                    self._text.insert("1.0", f.read())
            except IOError:
                pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", help="Flowchart commands text file", type=str)
    args = parser.parse_args()

    if args.f is not None:
        if not os.path.isfile(args.f):
            print("Couldn't find file:", args.f)
            return

    FlowChart(args.f).mainloop()


if __name__ == '__main__':
    main()
