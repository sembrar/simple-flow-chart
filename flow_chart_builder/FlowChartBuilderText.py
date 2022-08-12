from tkinter import ttk

from scrolled_widgets.ScrolledTextFrame import ScrolledTextFrame


def main():
    from tkinter import Tk
    root = Tk()
    widget = ScrolledTextFrame()
    widget.grid(row=0, column=0, sticky='news')
    root.mainloop()
