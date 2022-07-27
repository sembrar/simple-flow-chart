import argparse
import os
import math

import tkinter
from tkinter import ttk
from tkinter import messagebox

from MyModules.Widgets.ScrolledWidgets.ScrolledText import ScrolledText

import json


PADDING_FOR_NEW_OBJECT = 50
PADDING_BETWEEN_BOX_BOUNDARY_AND_TEXT = 10
DEFAULT_COLOR_BOX_TEXT = "black"
DEFAULT_COLOR_BOX_BOUNDARY = "black"
DEFAULT_DECISION_BOX_ACUTE_ANGLE = 80


class FlowChart(tkinter.Tk):

    def __init__(self, commands_text_file_path=None):
        tkinter.Tk.__init__(self)
        self.title("FlowChart")

        self._commands_text_file_path = commands_text_file_path

        paned_window = ttk.Panedwindow(self, orient=tkinter.HORIZONTAL)
        paned_window.grid(row=0, column=0, sticky='news')
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self._label_frame_for_canvas = ttk.Labelframe(paned_window, text="FlowChart")
        # the above is saved in var to be able to change title
        paned_window.add(self._label_frame_for_canvas)

        label_frame_for_text = ttk.Labelframe(paned_window, text="Text: Commands")
        paned_window.add(label_frame_for_text)

        self._canvas = tkinter.Canvas(self._label_frame_for_canvas, bg="light blue")
        self._canvas.grid(row=0, column=0, sticky='news')
        self._label_frame_for_canvas.rowconfigure(0, weight=1)
        self._label_frame_for_canvas.columnconfigure(0, weight=1)

        v_scroll_for_canvas = ttk.Scrollbar(
            self._label_frame_for_canvas, orient=tkinter.VERTICAL, command=self._canvas.yview)
        v_scroll_for_canvas.grid(row=0, column=1, sticky='ns')
        h_scroll_for_canvas = ttk.Scrollbar(
            self._label_frame_for_canvas, orient=tkinter.HORIZONTAL, command=self._canvas.xview)
        h_scroll_for_canvas.grid(row=1, column=0, sticky='ew')

        self._canvas.configure(yscrollcommand=v_scroll_for_canvas.set)
        self._canvas.configure(xscrollcommand=h_scroll_for_canvas.set)

        self._text = ScrolledText(label_frame_for_text, horizontal_scroll=True)
        self._text.grid(row=0, column=0, sticky='news')
        label_frame_for_text.rowconfigure(0, weight=1)
        label_frame_for_text.columnconfigure(0, weight=1)

        self._original_text = None
        if commands_text_file_path is not None:
            try:
                with open(commands_text_file_path) as f:
                    self._original_text = f.read()
                    self._text.insert("1.0", self._original_text)
            except IOError:
                pass

        self._commands = []

        buttons_frame = ttk.Frame(label_frame_for_text)
        buttons_frame.grid(row=1, column=0, sticky='ew')

        button_run_a_flow_chart_command = ttk.Button(buttons_frame, text="Run next command")
        button_run_a_flow_chart_command.grid(row=0, column=0, sticky='w')
        button_run_a_flow_chart_command.bind("<ButtonRelease-1>", self._run_a_command)

        button_run_all_commands = ttk.Button(buttons_frame, text="Run all commands")
        button_run_all_commands.grid(row=1, column=0, sticky='w')
        button_run_all_commands.bind("<ButtonRelease-1>", self._run_all_remaining_commands)

        button_send_commands_to_canvas = ttk.Button(buttons_frame, text="Send commands json to canvas")
        button_send_commands_to_canvas.grid(row=2, column=0, sticky='w')
        button_send_commands_to_canvas.bind("<ButtonRelease-1>", self._re_read_commands_from_text)

        button_reset_text = ttk.Button(buttons_frame, text="Reset commands text")
        button_reset_text.grid(row=3, column=0, sticky='w')
        if self._commands_text_file_path is None:
            button_reset_text.state(["disabled"])
        button_reset_text.bind("<ButtonRelease-1>", self._reset_commands_text_to_original)

        if self._commands_text_file_path is not None:
            self._re_read_commands_from_text(None)

    def _re_read_commands_from_text(self, event=None):
        if event is not None:
            if not event.widget.instate(["!disabled", "hover"]):
                return

        try:
            self._commands = json.loads(self._text.get("1.0", tkinter.END))
            self._commands.reverse()
            if event is not None:
                messagebox.showinfo("Success", "{} commands read".format(len(self._commands)))
        except json.JSONDecodeError:
            messagebox.showerror("Bad JSON", "Commands text JSON couldn't be decoded")
            self._commands = []

    def _reset_commands_text_to_original(self, event):
        if not event.widget.instate(["!disabled", "hover"]):
            return
        self._text.delete("1.0", tkinter.END)
        self._text.insert("1.0", self._original_text)
        self._re_read_commands_from_text()

    def destroy(self):
        if self._commands_text_file_path is not None:
            text = self._text.get("1.0", tkinter.END)
            if text.strip() != self._original_text.strip():
                save_result = messagebox.askyesno(
                    "Save changes?",
                    "The commands text has changed.\n"
                    "Do you want to overwrite the input file?"
                )
                if save_result:
                    with open(self._commands_text_file_path, 'w') as f:
                        f.write(text)
                    print("Commands overwritten to", self._commands_text_file_path)
                else:
                    print("Changed discarded")
        tkinter.Tk.destroy(self)

    def _run_a_command(self, event=None):
        if event is not None and not event.widget.instate(["!disabled", "hover"]):
            return

        try:
            try:
                command_data = self._commands.pop()
            except IndexError:
                return

            command_type = command_data["type"]

            if command_type == "title":
                self._label_frame_for_canvas.configure(text=command_data["text"])
                return

            if command_type == "connection":
                return

            allowed_command_types = ("start", "stop", "operation", "decision")
            if command_type not in allowed_command_types:
                raise ValueError("CommandType {} not in allowed {}".format(command_type, allowed_command_types))

            if command_type == "start" or command_type == "stop":
                box_text = command_type.title()
            else:
                box_text = command_data["text"]

            _, _, x1, y1, x2, y2, tags = \
                self._put_text_below_lowest_canvas_object_and_get_north_x_y_and_bbox_tags_as_seven_tuple(
                    command_data["color"] if "color" in command_data else DEFAULT_COLOR_BOX_TEXT,
                    command_type, command_data["name"], box_text
                )

            if command_type == "start" or command_type == "stop":
                self._canvas.create_oval(
                    x1 - PADDING_BETWEEN_BOX_BOUNDARY_AND_TEXT, y1 - PADDING_BETWEEN_BOX_BOUNDARY_AND_TEXT,
                    x2 + PADDING_BETWEEN_BOX_BOUNDARY_AND_TEXT, y2 + PADDING_BETWEEN_BOX_BOUNDARY_AND_TEXT,
                    tags=tags)
                return

            if command_type == "operation":
                self._canvas.create_rectangle(
                    x1 - PADDING_BETWEEN_BOX_BOUNDARY_AND_TEXT, y1 - PADDING_BETWEEN_BOX_BOUNDARY_AND_TEXT,
                    x2 + PADDING_BETWEEN_BOX_BOUNDARY_AND_TEXT, y2 + PADDING_BETWEEN_BOX_BOUNDARY_AND_TEXT,
                    tags=tags)
                return

            if command_type == "decision":
                try:
                    acute_angle = command_data["angle"]
                except KeyError:
                    acute_angle = DEFAULT_DECISION_BOX_ACUTE_ANGLE
                obtuse_angle = 180 - acute_angle

                x1 -= PADDING_BETWEEN_BOX_BOUNDARY_AND_TEXT
                y1 -= PADDING_BETWEEN_BOX_BOUNDARY_AND_TEXT
                x2 += PADDING_BETWEEN_BOX_BOUNDARY_AND_TEXT
                y2 += PADDING_BETWEEN_BOX_BOUNDARY_AND_TEXT

                dx = abs(x2 - x1)
                dy = abs(y2 - y1)

                # print("dx,dy:", dx, dy)

                if dy < dx:
                    angle_to_use_for_x_extremes = acute_angle
                    angle_to_use_for_y_extremes = obtuse_angle
                else:
                    angle_to_use_for_x_extremes = obtuse_angle
                    angle_to_use_for_y_extremes = acute_angle

                # print("Angles:x,y:", angle_to_use_for_x_extremes, angle_to_use_for_y_extremes)

                dx_for_rhombus = int(math.ceil((dy / 2) / abs(math.tan(math.radians(angle_to_use_for_x_extremes)))))
                dy_for_rhombus = int(math.ceil((dx / 2) / abs(math.tan(math.radians(angle_to_use_for_y_extremes)))))

                # print("deltas for rhombus:x,y:", dx_for_rhombus, dy_for_rhombus)

                point_east = x1 - dx_for_rhombus, y1 + int(dy / 2)
                point_west = x2 + dx_for_rhombus, y1 + int(dy / 2)
                point_north = x1 + int(dx / 2), y1 - dy_for_rhombus
                point_south = x1 + int(dx / 2), y2 + dy_for_rhombus

                # print("NESW:", point_north, point_east, point_south, point_west)

                # self._canvas.create_rectangle(x1, y1, x2, y2, tags=tags)

                self._canvas.create_polygon(
                    *point_north, *point_east, *point_south, *point_west,
                    fill='', outline=DEFAULT_COLOR_BOX_BOUNDARY, tags=tags)
                return

        except Exception as e:
            messagebox.showerror("Error occurred", "Please see command prompt window for details")
            raise e

    def _get_x_middle_y_lower_from_lowest_canvas_object(self):
        x = None
        y = 0
        object_ids = self._canvas.find_all()
        for obj_id in object_ids:
            x1, y1, x2, y2 = self._canvas.bbox(obj_id)
            y = max(y, y1, y2)
        if x is None:
            x = int(self._canvas.cget("width")) / 2
        return x, y

    def _put_text_below_lowest_canvas_object_and_get_north_x_y_and_bbox_tags_as_seven_tuple(
            self, color, box_type, box_name, box_text):
        x, y = self._get_x_middle_y_lower_from_lowest_canvas_object()
        y += PADDING_FOR_NEW_OBJECT

        tags = (box_type, box_name)
        obj_id = \
            self._canvas.create_text(x, y, anchor="n", fill=color, tags=tags, text=box_text, justify=tkinter.CENTER)
        x1, y1, x2, y2 = self._canvas.bbox(obj_id)
        return x, y, x1, y1, x2, y2, tags

    def _run_all_remaining_commands(self, event):
        if not event.widget.instate(["!disabled", "hover"]):
            return

        while len(self._commands) > 0:
            self._run_a_command()


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
