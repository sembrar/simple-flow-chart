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
DEFAULT_DECISION_BOX_ACUTE_ANGLE = 60


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

        # bind left-click-hold-and-drag to move flow chart boxes
        self._box_name_tag_being_moved = None
        self._moving_old_x, self._moving_old_y = 0, 0
        self._canvas.bind("<Button-1>", self._left_button_click_on_canvas)
        self._canvas.bind("<Motion>", self._mouse_move_on_canvas)
        self._canvas.bind("<ButtonRelease-1>", self._left_button_release_on_canvas)

        if self._commands_text_file_path is not None:
            self._re_read_commands_from_text(None)

    def _re_read_commands_from_text(self, event=None):
        if event is not None:
            if not event.widget.instate(["!disabled", "hover"]):
                return

        try:
            self._commands = json.loads(self._text.get("1.0", tkinter.END))
            self._commands.reverse()
            self._canvas.delete("canvas-obj")
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
                start_box_name, start_box_connection_corner = command_data["start"]
                end_box_name, end_box_connection_corner = command_data["end"]

                start_box_id = self._canvas.find_withtag("flow-chart-box-" + start_box_name)[0]
                end_box_id = self._canvas.find_withtag("flow-chart-box-" + end_box_name)[0]

                start_box_bbox = self._canvas.bbox(start_box_id)
                end_box_bbox = self._canvas.bbox(end_box_id)

                start_point = self._get_point_from_bbox_and_corner(start_box_bbox, start_box_connection_corner)
                end_point = self._get_point_from_bbox_and_corner(end_box_bbox, end_box_connection_corner)

                coordinates = []
                coordinates.extend(start_point)
                try:
                    intermediate_points_data = command_data["points"]
                    start_x, start_y = start_point
                    end_x, end_y = end_point
                    for ((which_x, x_inc), (which_y, y_inc)) in intermediate_points_data:

                        if which_x == "start_x":
                            x = start_x
                        elif which_x == "end_x":
                            x = end_x
                        elif which_x == "min_x":
                            x = min(start_x, end_x)
                        elif which_x == "max_x":
                            x = max(start_x, end_x)
                        else:
                            raise ValueError("which_x is unknown: {}".format(which_x))
                        x += x_inc

                        if which_y == "start_y":
                            y = start_y
                        elif which_y == "end_y":
                            y = end_y
                        elif which_y == "min_y":
                            y = min(start_y, end_y)
                        elif which_y == "max_y":
                            y = max(start_y, end_y)
                        else:
                            raise ValueError("which_y is unknown: {}".format(which_y))
                        y += y_inc

                        coordinates.append(x)
                        coordinates.append(y)

                except KeyError:
                    pass
                coordinates.extend(end_point)

                tags = ("canvas-obj", "connection")
                self._canvas.create_line(*coordinates, arrow=tkinter.LAST, tags=tags)
                return

            allowed_command_types = ("start", "stop", "operation", "decision")
            if command_type not in allowed_command_types:
                raise ValueError("CommandType {} not in allowed {}".format(command_type, allowed_command_types))

            if command_type == "start" or command_type == "stop":
                box_text = command_type.title()
            else:
                box_text = command_data["text"]

            text_id, x, y, x1, y1, x2, y2, tags = \
                self._put_text_below_lowest_canvas_object_and_get_obj_id_north_x_y_and_bbox_tags_as_eight_tuple(
                    command_data["color"] if "color" in command_data else DEFAULT_COLOR_BOX_TEXT,
                    command_type, command_data["name"], box_text
                )

            tags = tuple(list(tags) + ["flow-chart-box-" + command_data["name"]])

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
                    angle_to_use_for_x_extremes = acute_angle / 2
                    angle_to_use_for_y_extremes = obtuse_angle / 2
                else:
                    angle_to_use_for_x_extremes = obtuse_angle / 2
                    angle_to_use_for_y_extremes = acute_angle / 2

                # print("Angles:x,y:", angle_to_use_for_x_extremes, angle_to_use_for_y_extremes)

                dx_for_rhombus = int(math.ceil((dy / 2) / abs(math.tan(math.radians(angle_to_use_for_x_extremes)))))
                dy_for_rhombus = int(math.ceil((dx / 2) / abs(math.tan(math.radians(angle_to_use_for_y_extremes)))))

                # print("deltas for rhombus:x,y:", dx_for_rhombus, dy_for_rhombus)

                point_west = x1 - dx_for_rhombus, y1 + int(dy / 2)
                point_east = x2 + dx_for_rhombus, y1 + int(dy / 2)
                point_north = x1 + int(dx / 2), y1 - dy_for_rhombus
                point_south = x1 + int(dx / 2), y2 + dy_for_rhombus

                # print("NESW:", point_north, point_east, point_south, point_west)

                # self._canvas.create_rectangle(x1, y1, x2, y2, tags=tags)

                rhombus_id = self._canvas.create_polygon(
                    *point_north, *point_east, *point_south, *point_west,
                    fill='', outline=DEFAULT_COLOR_BOX_BOUNDARY, tags=tags)

                for decision in ("yes", "no"):
                    try:
                        corner = command_data[decision]
                        if corner == "north":
                            point = point_north
                        elif corner == "south":
                            point = point_south
                        elif corner == "east":
                            point = point_east
                        elif corner == "west":
                            point = point_west
                        else:
                            raise ValueError("decision box yes unknown corner {}".format(corner))
                        self._canvas.create_text(*point, text=decision.title(), tags=tags,
                                                 fill={"yes": "green", "no": "blue"}[decision])
                    except KeyError:
                        pass

                self._canvas.move("name:" + command_data["name"], 0, abs(point_north[1] - y))
                return

        except Exception as e:
            messagebox.showerror("Error occurred", "Please see command prompt window for details")
            raise e

        finally:
            self._set_canvas_scroll_region()

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

    def _put_text_below_lowest_canvas_object_and_get_obj_id_north_x_y_and_bbox_tags_as_eight_tuple(
            self, color, box_type, box_name, box_text):
        x, y = self._get_x_middle_y_lower_from_lowest_canvas_object()
        y += PADDING_FOR_NEW_OBJECT

        tags = ("canvas-obj", box_type, "name:" + box_name)
        obj_id = \
            self._canvas.create_text(x, y, anchor="n", fill=color, tags=tags, text=box_text, justify=tkinter.CENTER)
        x1, y1, x2, y2 = self._canvas.bbox(obj_id)
        return obj_id, x, y, x1, y1, x2, y2, tags

    def _run_all_remaining_commands(self, event):
        if not event.widget.instate(["!disabled", "hover"]):
            return

        while len(self._commands) > 0:
            self._run_a_command()

    def _left_button_click_on_canvas(self, event):
        # print("Left button click release on canvas")
        try:
            closest_obj = self._canvas.find_closest(event.x, event.y)[0]
        except IndexError:
            # print("No closest object found")
            return

        tags_closest_obj = self._canvas.gettags(closest_obj)
        if "connector" in tags_closest_obj:  # connectors are automatic, they should not be moved
            return

        self._box_name_tag_being_moved = None
        for tag in tags_closest_obj:
            if tag.startswith("name:"):
                self._box_name_tag_being_moved = tag
                self._moving_old_x = event.x
                self._moving_old_y = event.y
                break

        # print("Closest:", closest_obj, "Tags:", tags_closest_obj)

    def _left_button_release_on_canvas(self, _):
        # print("Left button release on canvas")
        self._box_name_tag_being_moved = None

    def _mouse_move_on_canvas(self, event):
        if self._box_name_tag_being_moved is None:
            return
        dx = event.x - self._moving_old_x
        dy = event.y - self._moving_old_y
        self._canvas.move(self._box_name_tag_being_moved, dx, dy)
        self._moving_old_x = event.x
        self._moving_old_y = event.y

    @staticmethod
    def _get_point_from_bbox_and_corner(bbox, corner):
        x1, y1, x2, y2 = bbox
        if corner == "north":
            return int((x1 + x2) / 2), y1
        if corner == "south":
            return int((x1 + x2) / 2), y2
        if corner == "west":
            return x1, int((y1 + y2) / 2)
        if corner == "east":
            return x2, int((y1 + y2) / 2)
        raise ValueError("corner {} is unknown".format(corner))

    def _set_canvas_scroll_region(self):
        all_canvas_objects = self._canvas.find_all()
        if len(all_canvas_objects) == 0:
            return

        bboxes = tuple(map(lambda x: self._canvas.bbox(x), all_canvas_objects))

        if len(all_canvas_objects) == 1:
            x_min, y_min, x_max, y_max = bboxes[0]
        else:
            x_min = min(bboxes, key=lambda b: b[0])[0]
            x_max = max(bboxes, key=lambda b: b[2])[2]
            y_min = min(bboxes, key=lambda b: b[1])[1]
            y_max = max(bboxes, key=lambda b: b[3])[3]

        scroll_region = (
            x_min - PADDING_FOR_NEW_OBJECT, y_min - PADDING_FOR_NEW_OBJECT,
            x_max + PADDING_FOR_NEW_OBJECT, y_max + PADDING_FOR_NEW_OBJECT)

        self._canvas.configure(scrollregion=scroll_region)


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
