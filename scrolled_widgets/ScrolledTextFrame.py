from tkinter import Text as _tkText
from tkinter import ttk as _ttk
from tkinter import constants as _tk_constants

"""
ScrolledTextFrame is a ttk Frame that has a Tkinter Text inside it with scrollbars attached to it
The Text widget can be accessed using "text" attribute. Eg: scrolled_text_frame.text 
"""


class ScrolledTextFrame(_ttk.Frame):

    def __init__(self, master=None,
                 vertical_scroll=True, horizontal_scroll=False, allow_keyboard_input=True, kwargs_for_frame=None,
                 **kw_for_text_widget):
        """
        :param master:
        :param vertical_scroll:
        :param horizontal_scroll:
        :param allow_keyboard_input:
        :param kwargs_for_frame: these are the keyword arguments dictionary for the frame that holds
         the Text widget and the scrollbars
        :param kw_for_text_widget: there are the keyword arguments for Text widget
        """

        if kwargs_for_frame is None:
            kwargs_for_frame = {}
        super().__init__(master, **kwargs_for_frame)

        self.text = _tkText(self, **kw_for_text_widget)
        self.text.grid(row=0, column=0, sticky='news')
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self._v_scroll = None
        if vertical_scroll:
            self._v_scroll = _ttk.Scrollbar(self, orient=_tk_constants.VERTICAL, command=self.text.yview)
            self._v_scroll.grid(row=0, column=1, sticky='ns')
            self.text.configure(yscrollcommand=self._v_scroll.set)

        self._h_scroll = None
        if horizontal_scroll:
            self._h_scroll = _ttk.Scrollbar(self, orient=_tk_constants.HORIZONTAL, command=self.text.xview)
            self._h_scroll.grid(row=1, column=0, sticky='ew')
            self.text.configure(xscrollcommand=self._h_scroll.set)
            self.text.configure(wrap=_tk_constants.NONE)  # using horizontal scroll => long lines shouldn't be wrapped

        if not allow_keyboard_input:
            self.text.bind('<Key>', lambda *_: 'break')

    def disable_key_board_input(self):
        self.text.bind('<Key>', lambda *_: 'break')

    def enable_key_board_input(self):
        self.text.bind('<Key>', lambda *_: True)


if __name__ == '__main__':
    from tkinter import Tk
    import random

    root = Tk()

    scrolled_text_frame = ScrolledTextFrame(root, horizontal_scroll=True)
    scrolled_text_frame.grid(row=0, column=0, sticky='news')
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # insert some random data
    random.seed("this is a seed")
    for i in range(100):
        text = f"{i + 1}: " + " ".join(map(str, range(random.randint(1, 20)))) + "\n"
        scrolled_text_frame.text.insert(f"{i + 1}.0", text)

    root.mainloop()
