from tkinter import ttk

from .FlowChartBuilderText import FlowChartTextFrame
from .FlowChartBuilderGUI import FlowChartFrame as FlowChartGUIFrame

from scrolled_widgets.ScrolledFrameInFrame import ScrolledFrameInFrame


class FlowChartBuilderFrame(ttk.Frame):

    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)

        self._notebook = ttk.Notebook(self)
        self._notebook.grid(row=0, column=0, sticky='nsew')
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self._text_flow_chart = FlowChartTextFrame(self._notebook)
        scrolled_frame_for_gui_flow_chart = ScrolledFrameInFrame(self._notebook)
        self._gui_flow_chart = FlowChartGUIFrame(scrolled_frame_for_gui_flow_chart.inner_scrolled_frame)
        self._gui_flow_chart.grid(row=0, column=0, sticky='news')

        self._notebook.add(self._text_flow_chart, text="Text for Commands")
        self._notebook.add(scrolled_frame_for_gui_flow_chart, text="GUI for Commands")

        self._notebook.bind("<<NotebookTabChanged>>", self._notebook_tab_changed_event_raised)
        self._currently_ready_for_edit_is_text = True  # if False, then it is GUI that is being edited by user, this is
        # used when notebook tab is changed to know which widget has new changes to be taken to other widget.
        # By default, as text is added first, it will be visible first, so the above is set to True

    def _notebook_tab_changed_event_raised(self, _):
        tab_opened = self._notebook.select()
        if tab_opened.endswith(self._text_flow_chart.winfo_name()):
            # text is opened
            if self._currently_ready_for_edit_is_text:
                return  # don't bring changes from GUI, Text is opened while currently ready for edit is Text, this
                # happens when GUI was tried to be opened, but it couldn't get correct data from Text, so an error is
                # present in the Text which needs to be corrected before opening the GUI with the data from Text
            # else
            # try to bring in data from GUI
            try:
                data = self._gui_flow_chart.get_data()
            except Exception as e:
                print(e.args)
                self._notebook.select(1)  # reselect GUI tab
                return
            self._text_flow_chart.set_data(data)
            self._currently_ready_for_edit_is_text = True
        else:
            # GUI is opened
            if not self._currently_ready_for_edit_is_text:
                return  # same reason as above for text (just the above condition has not in it, which means we are
                # checking if the currently available for edit is GUI
            # else
            # try to bring in data from text
            try:
                data = self._text_flow_chart.get_data()
            except Exception as e:
                print(e.args)
                self._notebook.select(0)  # reselect text tab
                return
            self._gui_flow_chart.set_data(data)
            self._currently_ready_for_edit_is_text = False

    def set_data(self, data):
        if self._currently_ready_for_edit_is_text:
            self._text_flow_chart.set_data(data)
        else:
            self._gui_flow_chart.set_data(data)

    def get_data(self):
        if self._currently_ready_for_edit_is_text:
            return self._text_flow_chart.get_data()
        else:
            return self._gui_flow_chart.get_data()


def main():
    from tkinter import Tk
    root = Tk()
    widget = FlowChartBuilderFrame(root)
    widget.grid(row=0, column=0, sticky='nsew')
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    root.mainloop()
