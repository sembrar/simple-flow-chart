import json
from collections import OrderedDict
from tkinter import constants as tk_constants

from scrolled_widgets.ScrolledTextFrame import ScrolledTextFrame
from .available_command_types_and_detail_types import *


class FlowChartTextFrame(ScrolledTextFrame):
    def __init__(self, master=None, kwargs_for_frame=None, **kw_for_text_widget):
        super().__init__(master, horizontal_scroll=True, kwargs_for_frame=kwargs_for_frame, **kw_for_text_widget)

    def get_data(self):
        text = self.text.get("1.0", tk_constants.END).strip()
        if text == "":
            return []
        str_commands = text.split("\n")  # list[str]
        commands = []
        for c in str_commands:
            try:
                commands.append(json.loads(c))
            except json.JSONDecodeError:
                print("Couldn't json-decode command:", c)
                commands.append(dict())  # append an empty dictionary # fixme raise error instead for better handling
        return commands

    def set_data(self, data):
        """
        :type data: list[dict]
        """
        self.text.delete("1.0", tk_constants.END)

        for d, i in zip(data, range(len(data))):
            if "type" not in d:  # todo this should be an error
                self.text.insert(f"{i + 1}.0", "\n")  # type of command is not there, just add a new line
                continue

            command_type = d["type"]
            if command_type == "":  # this can happen if data is from GUI builder and user didn't select any type yet
                # for this command
                continue

            ordered_dict = OrderedDict()
            ordered_dict["type"] = command_type

            for detail_type in DETAIL_TYPES_FOR_COMMANDS[command_type]:
                if detail_type not in d:
                    continue
                ordered_dict[detail_type] = d[detail_type]

            self.text.insert(f"{i + 1}.0", f"{json.dumps(ordered_dict)}\n")


def main():
    from tkinter import Tk
    root = Tk()
    root.title("FlowChartTextFrame")
    widget = FlowChartTextFrame()
    widget.grid(row=0, column=0, sticky='news')
    widget.set_data([
        {'name': 'start', 'placement': ('', ''), 'type': 'start', 'autostart': '', 'dx': '', 'dy': ''},
        {'placement': ('', ''), 'autostart': '', 'dx': '', 'type': 'operation', 'name': 'mix', 'text': '', 'dy': ''},
        {'type': 'stop', 'name': 'stop', 'placement': ('', ''), 'autostart': '', 'dx': '', 'dy': ''}
    ])
    print(widget.get_data())
    root.mainloop()
