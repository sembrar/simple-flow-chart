import tkinter
from tkinter import ttk


DEBUG = False

INT_ENTRY_WIDTH = 8


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
        if "values" in kw:
            self.configure(width=len(max(kw["values"], key=lambda x: len(x))) + 3)

    def _restrict_keyboard_input(self):
        return False

    def _run_function_to_update_choices(self, _):
        self.configure(values=self._func_get_choices())


class FrameWithAddDeleteMoveChildren(ttk.Frame):

    def __init__(self, master=None, child_widget_class=None, child_creation_additional_args_dict=None, **kw):
        super().__init__(master, **kw)

        if child_creation_additional_args_dict is None:
            child_creation_additional_args_dict = {}

        self._child_widget_class = child_widget_class
        self._child_creation_additional_args_dict = child_creation_additional_args_dict

        self._children_frames = []

        self._button_add = ttk.Button(self, text="+", width=5)
        self._button_add.grid(row=0, column=0, sticky='w')

        self._button_add.bind("<Button-1>", self._clicked_button_add)

    def _clicked_button_add(self, event):
        if not event.widget.instate(["!disabled", "hover"]):
            return
        self._add_new_child()

    def _add_new_child(self, above=None):
        child_frame = ttk.Frame(self)
        name_of_the_child_frame = child_frame.winfo_name()

        child_widget = self._child_widget_class(child_frame, **self._child_creation_additional_args_dict)
        child_widget.grid(row=0, column=0)

        button_move_up = ttk.Button(child_frame, text=u"\u25B2", width=5)
        button_move_up.grid(row=0, column=1)

        button_move_down = ttk.Button(child_frame, text=u"\u25BC", width=5)
        button_move_down.grid(row=0, column=2)

        self._children_frames.append(name_of_the_child_frame)
        self._reset_grid_configuration_of_children()

        button_move_up.name_of_child = name_of_the_child_frame
        button_move_down.name_of_child = name_of_the_child_frame
        button_move_up.bind("<Button-1>", self._clicked_up_button_in_child_frame)
        button_move_down.bind("<Button-1>", self._clicked_down_button_in_child_frame)

    def _reset_grid_configuration_of_children(self):
        for i in range(len(self._children_frames)):
            self.nametowidget(self._children_frames[i]).grid(row=i, column=0, sticky='w')
        self._button_add.grid(row=len(self._children_frames), sticky='w')

    def _clicked_up_button_in_child_frame(self, event):
        if not event.widget.instate(["!disabled", "hover"]):
            return

        name_of_frame = event.widget.name_of_child  # this is saved in button after creation
        cur_index = self._children_frames.index(name_of_frame)

        if cur_index == 0:  # it is the first one in the list
            return

        # swap names in the list
        self._children_frames[cur_index], self._children_frames[cur_index-1] =\
            self._children_frames[cur_index-1], self._children_frames[cur_index]

        self._reset_grid_configuration_of_children()

    def _clicked_down_button_in_child_frame(self, event):
        if not event.widget.instate(["!disabled", "hover"]):
            return

        name_of_frame = event.widget.name_of_child  # this is saved in button after creation
        cur_index = self._children_frames.index(name_of_frame)

        if cur_index == len(self._children_frames) - 1:  # it is the last widget in the list
            return

        # swap names in the list
        self._children_frames[cur_index], self._children_frames[cur_index + 1] = \
            self._children_frames[cur_index + 1], self._children_frames[cur_index]

        self._reset_grid_configuration_of_children()


AVAILABLE_COMMAND_TYPES = "start stop operation decision connection delete delete-all title box font connector".split()

DETAIL_TYPES_FOR_COMMANDS = dict()
DETAIL_TYPES_FOR_COMMANDS["start"] = ("name", "placement", "autostart", "dx", "dy")
DETAIL_TYPES_FOR_COMMANDS["stop"] = DETAIL_TYPES_FOR_COMMANDS["start"]
DETAIL_TYPES_FOR_COMMANDS["operation"] = ("name", "text", "placement", "autostart", "dx", "dy")
DETAIL_TYPES_FOR_COMMANDS["decision"] = DETAIL_TYPES_FOR_COMMANDS["operation"]
DETAIL_TYPES_FOR_COMMANDS["connection"] = ("start", "end", "points", "autostart", "label", "label-dx", "label-dy", "label-color")
DETAIL_TYPES_FOR_COMMANDS["delete"] = ("name", "autostart")
DETAIL_TYPES_FOR_COMMANDS["delete-all"] = ("autostart",)
DETAIL_TYPES_FOR_COMMANDS["title"] = ("text", "autostart")
DETAIL_TYPES_FOR_COMMANDS["box"] = ("width", "autostart")
DETAIL_TYPES_FOR_COMMANDS["font"] = ("size", "weight", "autostart")
DETAIL_TYPES_FOR_COMMANDS["connector"] = ("width", "autostart")


class CombosNameAndDirection(ttk.Frame):

    def __init__(self, master=None, func_to_get_names=None, **kw):
        super().__init__(master, **kw)

        self._func_to_get_names = func_to_get_names
        self._name_combo = SelectOnlyCombobox(self, self._func_to_get_names)
        self._name_combo.grid(row=0, column=0)

        self._direction_combo = SelectOnlyCombobox(self, values=("north", "east", "south", "west"))
        self._direction_combo.grid(row=0, column=1)


class SinglePoint(ttk.Frame):

    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)

        col = -1  # used in .grid method

        col += 1
        ttk.Label(self, text="(").grid(row=0, column=col)

        self._combo_x = SelectOnlyCombobox(self, values=("start_x", "end_x", "min_x", "max_x", "mid_x"))
        col += 1
        self._combo_x.grid(row=0, column=col)

        col += 1
        ttk.Label(self, text="+").grid(row=0, column=col)

        self._entry_int_dx = IntEntry(self, width=INT_ENTRY_WIDTH)
        col += 1
        self._entry_int_dx.grid(row=0, column=col)

        col += 1
        ttk.Label(self, text=",").grid(row=0, column=col)

        self._combo_y = SelectOnlyCombobox(self, values=("start_y", "end_y", "min_y", "max_y", "mid_y"))
        col += 1
        self._combo_y.grid(row=0, column=col)

        col += 1
        ttk.Label(self, text="+").grid(row=0, column=col)

        self._entry_int_dy = IntEntry(self, width=INT_ENTRY_WIDTH)
        col += 1
        self._entry_int_dy.grid(row=0, column=col)

        col += 1
        ttk.Label(self, text=")").grid(row=0, column=col)


class Points(ttk.Frame):

    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)

        ttk.Label(self, text="Placeholder").grid(row=0, column=0)


class SingleCommandFrame(ttk.Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)

        label_frame_type = ttk.Labelframe(self, text="Type")
        label_frame_type.grid(row=0, column=0, sticky='w')

        self._var_command_type = tkinter.StringVar(self)

        self._type = SelectOnlyCombobox(
            label_frame_type, textvariable=self._var_command_type, values=AVAILABLE_COMMAND_TYPES)
        self._type.grid(row=0, column=0)

        self._chosen_settings = {}

        self._var_command_type.trace_variable("w", self._changed_command_type)

    def _changed_command_type(self, *_):
        available_detail_types = DETAIL_TYPES_FOR_COMMANDS.get(self._var_command_type.get(), None)

        if available_detail_types is None:
            print("There are no detail types available for", self._var_command_type.get())
            return

        self._remove_existing_detail_frames()

        for d, i in zip(available_detail_types, range(len(available_detail_types))):
            label_frame = ttk.Labelframe(self, text=d)
            label_frame.grid(row=0, column=i+1)  # the column=0 is for "Type" i.e. command type

            if d == "name" or d == "text" or d == "label" or d == "label-color":
                child = ttk.Entry(label_frame)
            elif d == "placement" or d == "start" or d == "end":
                child = CombosNameAndDirection(label_frame)  # todo pass function to get names for combo
            elif d == "autostart":
                child = SelectOnlyCombobox(label_frame, values=("False", "True"))
            elif d == "dx" or d == "dy" or d == "label-dx" or d == "label-dy" or d == "width" or d == "size":
                child = IntEntry(label_frame, width=INT_ENTRY_WIDTH)
            elif d == "points":
                child = Points(label_frame)
            elif d == "weight":
                child = SelectOnlyCombobox(label_frame, values=("normal", "bold"))
            else:
                print("Unknown detail type:", d)
                return

            child.grid(row=0, column=0)

    def _remove_existing_detail_frames(self):
        children = self.winfo_children()
        for child in children:
            detail_name = child.cget("text").lower()
            if detail_name == "type":
                continue
            # todo save the value of the child to the dictionary for use later
            child.destroy()
            debug_print("Removed detail:", detail_name)


if __name__ == '__main__':
    DEBUG = True

    root = tkinter.Tk()
    widget = FrameWithAddDeleteMoveChildren(root, ttk.Entry)
    widget.grid(row=0, column=0)
    root.mainloop()
