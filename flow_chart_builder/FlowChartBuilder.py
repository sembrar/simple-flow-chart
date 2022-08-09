import tkinter
from tkinter import ttk


DEBUG = False


def debug_print(*args, **kwargs):
    if not DEBUG:
        return
    print(*args, **kwargs)


class IntEntry(ttk.Entry):

    def __init__(self, master=None, widget=None, **kw):
        super().__init__(master, widget, **kw)
        validation_command = self.register(self._int_validation)  # register needed for additional substitution args
        self.configure(validate="key", validatecommand=(validation_command, "%P"))

    def _int_validation(self, new_text_if_allowed):
        new_text_if_allowed = new_text_if_allowed.strip()
        if new_text_if_allowed == "":
            return True
        if new_text_if_allowed == "-":
            return True
        if new_text_if_allowed == "+":
            return True
        try:
            int(new_text_if_allowed)
            return True
        except ValueError:
            debug_print("IntEntry: Validation Error: Not a valid int")
            return False


if __name__ == '__main__':
    # DEBUG = True
    root = tkinter.Tk()
    widget = IntEntry(root)
    widget.grid(row=0, column=0)
    root.mainloop()
