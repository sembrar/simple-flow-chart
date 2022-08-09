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


class SelectOnlyCombobox(ttk.Combobox):

    def __init__(self, master=None, func_get_choices=None, **kw):
        """
        :param master:
        :param func_get_choices: a function can be specified that returns a list/tuple of choice
            this can be used to update choices dynamically, as it will be called whenever the list of choices is
            pulled down which triggers a button down event
        :param kw:
        """
        super().__init__(master, **kw)
        self._func_get_choices = func_get_choices
        self.configure(validate="key", validatecommand=self._restrict_keyboard_input)
        if self._func_get_choices is not None:
            self.bind("<Button-1>", self._run_function_to_update_choices)

    def _restrict_keyboard_input(self):
        return False

    def _run_function_to_update_choices(self, _):
        self.configure(values=self._func_get_choices())


if __name__ == '__main__':
    DEBUG = True

    import time


    def get_time():
        return time.time(), time.ctime()

    root = tkinter.Tk()
    widget = SelectOnlyCombobox(root, func_get_choices=get_time)
    widget.grid(row=0, column=0)
    widget2 = SelectOnlyCombobox(root, values="north east south west".split())
    widget2.grid(row=1, column=0)
    root.mainloop()
