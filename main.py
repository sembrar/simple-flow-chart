import argparse
import os

import tkinter
from tkinter import ttk
from tkinter import messagebox

from MyModules.Widgets.ScrolledWidgets.ScrolledCanvas import ScrolledCanvas
from MyModules.Widgets.ScrolledWidgets.ScrolledText import ScrolledText

import json


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

        self._canvas = ScrolledCanvas(self._label_frame_for_canvas, bg="light blue")
        self._canvas.grid(row=0, column=0, sticky='news')
        self._label_frame_for_canvas.rowconfigure(0, weight=1)
        self._label_frame_for_canvas.columnconfigure(0, weight=1)

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

        button_send_commands_to_canvas = ttk.Button(buttons_frame, text="Send commands json to canvas")
        button_send_commands_to_canvas.grid(row=1, column=0, sticky='w')
        button_send_commands_to_canvas.bind("<ButtonRelease-1>", self._re_read_commands_from_text)

        button_reset_text = ttk.Button(buttons_frame, text="Reset commands text")
        button_reset_text.grid(row=2, column=0, sticky='w')
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

    def _run_a_command(self, event):
        if not event.widget.instate(["!disabled", "hover"]):
            return

        try:
            command_data = self._commands.pop()
            if command_data["type"] == "title":
                self._label_frame_for_canvas.configure(text=command_data["text"])
                return
        except Exception as e:
            messagebox.showerror("Error", "{}".format(e.args))


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
