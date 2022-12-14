import tkinter
from tkinter import ttk

from .available_command_types_and_detail_types import *


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

    @staticmethod
    def _int_validation(new_text_if_allowed):
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

    @staticmethod
    def _restrict_keyboard_input():
        return False

    def _run_function_to_update_choices(self, _):
        self.configure(values=self._func_get_choices())


class FrameWithAddDeleteMoveChildren(ttk.Frame):

    def __init__(self, master=None, child_widget_class=None, child_creation_additional_args_dict=None,
                 put_buttons_to_the_left=False, **kw):
        super().__init__(master, **kw)

        if child_creation_additional_args_dict is None:
            child_creation_additional_args_dict = {}

        self._child_widget_class = child_widget_class
        self._child_creation_additional_args_dict = child_creation_additional_args_dict
        self._put_buttons_to_the_left = put_buttons_to_the_left

        self._children_frames = []

        self._button_add = ttk.Button(self, text="+", width=5)
        self._button_add.grid(row=0, column=0, sticky='w')

        self._button_add.bind("<ButtonRelease-1>", self._clicked_button_add)

    def _clicked_button_add(self, event):
        if not event.widget.instate(["!disabled", "hover"]):
            return
        self._add_new_child()

    def _add_new_child(self, above=None):
        child_frame = ttk.Frame(self)
        name_of_the_child_frame = child_frame.winfo_name()

        widget = self._child_widget_class(child_frame, **self._child_creation_additional_args_dict)
        button_move_up = ttk.Button(child_frame, text=u"\u25B2", width=5)
        button_move_down = ttk.Button(child_frame, text=u"\u25BC", width=5)
        button_delete = ttk.Button(child_frame, text=u"\u274C", width=5)
        button_add_above = ttk.Button(child_frame, text=u"+\u2191", width=5)  # the button has + sign, up arrow sign

        child_frame.inner_widget_name = widget.winfo_name()  # this can be used to grab the widget from outside

        col = -1

        if self._put_buttons_to_the_left:
            pass
        else:  # then the widget is the one that is to the left
            col += 1
            widget.grid(row=0, column=col, sticky='ew')
            child_frame.columnconfigure(col, weight=1)

        col += 1
        button_move_up.grid(row=0, column=col)

        col += 1
        button_move_down.grid(row=0, column=col)

        col += 1
        button_delete.grid(row=0, column=col)

        col += 1
        button_add_above.grid(row=0, column=col)

        if self._put_buttons_to_the_left:
            col += 1
            widget.grid(row=0, column=col, sticky='ew')
            child_frame.columnconfigure(col, weight=1)
        else:  # then the widget is the one to the left and it is already put in grid above
            pass

        if above is None:
            self._children_frames.append(name_of_the_child_frame)
        else:
            index_to_insert_at = self._children_frames.index(above)
            self._children_frames.insert(index_to_insert_at, name_of_the_child_frame)
        self._reset_grid_configuration_of_children()

        # store name of the frame as an attribute of buttons for easy access during event listening
        button_move_up.name_of_child = name_of_the_child_frame
        button_move_down.name_of_child = name_of_the_child_frame
        button_delete.name_of_child = name_of_the_child_frame
        button_add_above.name_of_child = name_of_the_child_frame

        button_move_up.bind("<ButtonRelease-1>", self._clicked_up_button_in_child_frame)
        button_move_down.bind("<ButtonRelease-1>", self._clicked_down_button_in_child_frame)
        button_delete.bind("<ButtonRelease-1>", self._clicked_delete_in_child_frame)
        button_add_above.bind("<ButtonRelease-1>", self._clicked_add_above_button_in_child_frame)

    def _reset_grid_configuration_of_children(self):
        for i in range(len(self._children_frames)):
            self.nametowidget(self._children_frames[i]).grid(row=i, column=0, sticky='ew')
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

    def _clicked_delete_in_child_frame(self, event):
        if not event.widget.instate(["!disabled", "hover"]):
            return

        name_of_frame = event.widget.name_of_child  # this is saved in button after creation
        self.nametowidget(name_of_frame).destroy()

        # remove it from children frames list and reset grid configuration
        self._children_frames.remove(name_of_frame)
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

    def _clicked_add_above_button_in_child_frame(self, event):
        if not event.widget.instate(["!disabled", "hover"]):
            return

        name_of_frame = event.widget.name_of_child  # this is saved in button after creation
        self._add_new_child(name_of_frame)

    def delete_all_children(self):
        while len(self._children_frames) > 0:
            last_child_frame_name = self._children_frames.pop()
            self.nametowidget(last_child_frame_name).destroy()


class CombosNameAndDirection(ttk.Frame):

    def __init__(self, master=None, func_to_get_names=None, **kw):
        super().__init__(master, **kw)

        self._func_to_get_names = func_to_get_names
        self.name_combo = SelectOnlyCombobox(self, self._func_to_get_names)
        self.name_combo.grid(row=0, column=0)

        self.direction_combo = SelectOnlyCombobox(self, values=("north", "east", "south", "west"))
        self.direction_combo.grid(row=0, column=1)


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

    def get_data(self):
        x_type = self._combo_x.get()
        try:
            x_delta = int(self._entry_int_dx.get())
        except ValueError:
            x_delta = ""

        y_type = self._combo_y.get()
        try:
            y_delta = int(self._entry_int_dy.get())
        except ValueError:
            y_delta = ""

        return (x_type, x_delta), (y_type, y_delta)

    def set_data(self, data):
        try:
            ((x_type, x_delta), (y_type, y_delta)) = data
        except ValueError:
            ((x_type, x_delta), (y_type, y_delta)) = (("", ""), ("", ""))
        try:
            int(x_delta)
        except ValueError:
            x_delta = ""
        try:
            int(y_delta)
        except ValueError:
            y_delta = ""
        self._combo_x.set(x_type)
        self._combo_y.set(y_type)
        self._entry_int_dx.delete(0, tkinter.END)
        self._entry_int_dx.insert(0, str(x_delta))
        self._entry_int_dy.delete(0, tkinter.END)
        self._entry_int_dy.insert(0, str(y_delta))


class Points(FrameWithAddDeleteMoveChildren):

    def __init__(self, master=None, **kw):
        super().__init__(master, SinglePoint, **kw)

    def get_data(self):
        data = []
        for child_frame_name in self._children_frames:
            # child_frame_name is the name of the frame enclosing the SinglePoint object and different buttons
            # SinglePoint object's name can be accessed by converting the above name to widget and accessing its
            # inner_widget_name attribute
            child_frame = self.nametowidget(child_frame_name)
            single_point_object = child_frame.nametowidget(child_frame.inner_widget_name)  # type: SinglePoint
            data.append(single_point_object.get_data())
        return data

    def set_data(self, data):
        """
        :type data: list[tuple]
        """

        self.delete_all_children()

        for each_data_tuple in data:
            self._add_new_child()  # create new child
            child_frame = self.nametowidget(self._children_frames[-1])  # recently converted child frame
            single_point_object = child_frame.nametowidget(child_frame.inner_widget_name)  # type: SinglePoint
            single_point_object.set_data(each_data_tuple)

    def is_empty(self):
        return len(self._children_frames) == 0


class LabelFramedWidget(ttk.Labelframe):

    def __init__(self, master=None, label_text="", inner_widget_class=None,
                 kwargs_for_label_frame=None, **kwargs_for_inner_widget):
        if kwargs_for_label_frame is None:
            kwargs_for_label_frame = {}
        kwargs_for_label_frame["text"] = label_text  # if "text" is also in the kwargs, it will be overwritten
        super().__init__(master, **kwargs_for_label_frame)

        self._inner_widget = inner_widget_class(master=self, **kwargs_for_inner_widget)
        self._inner_widget.grid(row=0, column=0)

    def get_data(self):
        raise NotImplementedError

    def set_data(self, data):
        raise NotImplementedError

    def is_empty(self):
        raise NotImplementedError


class LabelFramedEntry(LabelFramedWidget):

    def __init__(self, master=None, label_text="",
                 kwargs_for_label_frame=None, **kwargs_for_inner_widget):
        super().__init__(master, label_text, ttk.Entry, kwargs_for_label_frame, **kwargs_for_inner_widget)

    def get_data(self):
        return ttk.Entry.get(self._inner_widget)

    def set_data(self, data):
        inner_widget = self._inner_widget  # type: ttk.Entry
        inner_widget.delete(0, tkinter.END)
        inner_widget.insert(0, data)

    def is_empty(self):
        if self.get_data() == "":
            return True
        return False


class LabelFramedIntEntry(LabelFramedWidget):

    def __init__(self, master=None, label_text="",
                 kwargs_for_label_frame=None, **kwargs_for_inner_widget):
        super().__init__(master, label_text, IntEntry, kwargs_for_label_frame, **kwargs_for_inner_widget)

    def get_data(self):
        try:
            return int(IntEntry.get(self._inner_widget))
        except ValueError:
            return ""

    def set_data(self, data):
        try:
            value = str(int(data))
        except ValueError:
            value = ""
        inner_widget = self._inner_widget  # type: IntEntry
        inner_widget.delete(0, tkinter.END)
        inner_widget.insert(0, value)

    def is_empty(self):
        if self.get_data() == "":
            return True
        return False


class LabelFramedSelectOnlyCombobox(LabelFramedWidget):

    def __init__(self, master=None, label_text="",
                 kwargs_for_label_frame=None, **kwargs_for_inner_widget):
        super().__init__(master, label_text, SelectOnlyCombobox, kwargs_for_label_frame, **kwargs_for_inner_widget)

    def get_data(self):
        return SelectOnlyCombobox.get(self._inner_widget)

    def set_data(self, data):
        inner_widget = self._inner_widget  # type: SelectOnlyCombobox
        inner_widget.set(data)  # Combobox provides this direct set method

    def is_empty(self):
        if self.get_data() == "":
            return True
        return False


class LabelFramedCombosNameAndDirection(LabelFramedWidget):

    def __init__(self, master=None, label_text="",
                 kwargs_for_label_frame=None, **kwargs_for_inner_widget):
        super().__init__(master, label_text, CombosNameAndDirection, kwargs_for_label_frame, **kwargs_for_inner_widget)

    def get_data(self):
        inner_widget = self._inner_widget  # type: CombosNameAndDirection
        return inner_widget.name_combo.get(), inner_widget.direction_combo.get()

    def set_data(self, data):
        inner_widget = self._inner_widget  # type: CombosNameAndDirection
        try:
            name, direction = data
        except ValueError:
            name, direction = "", ""
        inner_widget.name_combo.set(name)
        inner_widget.direction_combo.set(direction)

    def is_empty(self):
        if self.get_data() == ("", ""):
            return True
        return False


class LabelFramedPoints(LabelFramedWidget):

    def __init__(self, master=None, label_text="",
                 kwargs_for_label_frame=None, **kwargs_for_inner_widget):
        super().__init__(master, label_text, Points, kwargs_for_label_frame, **kwargs_for_inner_widget)

    def get_data(self):
        inner_widget = self._inner_widget  # type: Points
        return inner_widget.get_data()

    def set_data(self, data):
        inner_widget = self._inner_widget  # type: Points
        inner_widget.set_data(data)

    def is_empty(self):
        inner_widget = self._inner_widget  # type: Points
        return inner_widget.is_empty()


class SingleCommandFrame(ttk.Frame):
    def __init__(self, master=None, function_to_get_names_of_boxes=None, **kw):
        super().__init__(master, **kw)

        self._function_to_get_names_of_boxes = function_to_get_names_of_boxes

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
            if d == "name" or d == "text" or d == "label" or d == "label-color":
                label_framed_widget = LabelFramedEntry(self, label_text=d)
            elif d == "placement" or d == "start" or d == "end":
                label_framed_widget = LabelFramedCombosNameAndDirection(
                    self, label_text=d, func_to_get_names=self._function_to_get_names_of_boxes)
            elif d == "autostart":
                label_framed_widget = LabelFramedSelectOnlyCombobox(self, label_text=d, values=("False", "True"))
            elif d == "dx" or d == "dy" or d == "angle" or d == "label-dx" or d == "label-dy" or d == "width" or d == "size":
                label_framed_widget = LabelFramedIntEntry(self, label_text=d, width=INT_ENTRY_WIDTH)
            elif d == "points":
                label_framed_widget = LabelFramedPoints(self, label_text=d)
            elif d == "weight":
                label_framed_widget = LabelFramedSelectOnlyCombobox(self, label_text=d, values=("normal", "bold"))
            else:
                print("Unknown detail type:", d)
                return

            label_framed_widget.grid(row=0, column=i + 1)  # the column=0 is for "Type" i.e. command type

    def _remove_existing_detail_frames(self):
        children = self.winfo_children()
        for child in children:
            detail_name = child.cget("text").lower()
            if detail_name == "type":
                continue
            # todo save the value of the child to the dictionary for use later
            child.destroy()
            debug_print("Removed detail:", detail_name)

    def get_data(self):
        d = {"type": self._var_command_type.get()}
        children = self.winfo_children()
        for child in children:
            if isinstance(child, LabelFramedWidget):
                if child.is_empty():
                    continue
                d[child.cget("text").lower()] = child.get_data()
        return d

    def set_data(self, data):
        try:
            self._var_command_type.set(data["type"])  # this will trigger the bounding function and will create
            # required LabelFramedWidgets
        except KeyError:
            return
        children = self.winfo_children()
        for child in children:
            if isinstance(child, LabelFramedWidget):
                try:
                    child.set_data(data[child.cget("text").lower()])
                except KeyError:
                    pass


class FlowChartFrame(FrameWithAddDeleteMoveChildren):

    def __init__(self, master=None, put_buttons_to_the_left=False, **kw):
        super().__init__(master, SingleCommandFrame,
                         child_creation_additional_args_dict={
                             "function_to_get_names_of_boxes": self._get_names_of_boxes_from_commands},
                         put_buttons_to_the_left=put_buttons_to_the_left, **kw)

    def _get_names_of_boxes_from_commands(self):
        names = []
        for widget_name in self._children_frames:
            child_frame = self.nametowidget(widget_name)
            inner_widget = child_frame.nametowidget(child_frame.inner_widget_name)
            # this above inner widget is a SingleCommandFrame obj
            # todo make the following efficient by creating get functions in SingleCommandFrame class
            for c in inner_widget.winfo_children():
                if isinstance(c, LabelFramedWidget) and c.cget("text").lower() == "name":
                    name = c.winfo_children()[0].get().strip()
                    if name != "":
                        names.append(name)
                    break
        return names

    def get_data(self):
        data = []
        for widget_name in self._children_frames:
            child_frame = self.nametowidget(widget_name)
            inner_widget = child_frame.nametowidget(
                child_frame.inner_widget_name)  # this will be a SingleCommandFrame obj
            data.append(inner_widget.get_data())
        return data

    def set_data(self, data):
        """
        :type data: list[dict]
        """
        self.delete_all_children()

        for d in data:
            self._add_new_child()
            child_frame = self.nametowidget(self._children_frames[-1])
            inner_single_command_frame = child_frame.nametowidget(child_frame.inner_widget_name)
            inner_single_command_frame.set_data(d)


def main():
    root = tkinter.Tk()
    widget = FlowChartFrame(root, put_buttons_to_the_left=True)
    widget.set_data([{"type": "start", "name": "start"}, {"type": "operation", "name": "mix"}])
    widget.grid(row=0, column=0)
    root.mainloop()


if __name__ == '__main__':
    DEBUG = True
    main()
