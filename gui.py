"""
Class: Gui
Author: Kamil Koltowski
Date: 2022-11-06
Description: This is GUI Parent class.
"""
import datetime
import hashdata
import tkinter as tk
from tkinter.font import Font
from gui_logs_page import LogsPage
from gui_database_page import DatabasePage
from gui_about_page import AboutPage


class Gui(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__root_frame = tk.Frame(self)
        self.__frames = {}
        self.title("NLR")
        self.icon = tk.PhotoImage(file=hashdata.PATH_TO_ICON_PNG)
        self.iconphoto(False, self.icon)
        self.geometry(f"{800}x{500}")
        self.resizable(width=False, height=False)
        self.protocol("WM_DELETE_WINDOW", self.quit_tool)
        self.font = Font(
            family='Terminal',
            size=14,
            weight='normal',
            slant='roman',
            underline=False,
        )
        self.bg_color = "#D6A184"
        self.entry_and_button_color = "#F3D3BD"
        self.entry_fg_color = "#343434"
        self.frame_color = "#774936"
        self.button_border = tk.Frame(self, highlightbackground="black", highlightthickness=2, bd=0)

    def setup_frames(self):
        self.__setup_root_frame()
        self.__init_frames()

    def __init_frames(self):
        """Initialise frame"""
        for Frame in (LogsPage, DatabasePage, AboutPage):
            frame_name = Frame.__name__
            frame = Frame(parent=self.__root_frame, controller=self)
            self.__frames[frame_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(frame_name=LogsPage.__name__)

    def __setup_root_frame(self):
        """Setup root frame, tkinter gui stuff"""
        self.__root_frame.grid(row=0, column=0, sticky='nsew')
        self.__root_frame.rowconfigure(index=0, weight=1)
        self.__root_frame.columnconfigure(index=0, weight=1)

    def show_frame(self, frame_name):
        """Shows selected frame, store other pages (frames) on top
        :param frame_name: Name of frame to be raised, could be: LogsPage or DatabasePage
        """
        frame = self.__frames[frame_name]
        frame.tkraise()

    def get_logs_page(self) -> LogsPage:
        """Returns Logs Page"""
        return self.__frames[LogsPage.__name__]

    def get_database_page(self) -> DatabasePage:
        """Returns Database Page"""
        return self.__frames[DatabasePage.__name__]

    def quit_tool(self):
        self.__frames['LogsPage'].M_stop_main_thread()
        self.quit()
        self.destroy()

    def display_text(self, message: str):
        """Displays passed message on console, it determines current time as well
        :param message: message to be printed in console
        """
        date = datetime.datetime.now().strftime("%H:%M")
        for Frame in self.__frames.values():
            if Frame == self.__frames["AboutPage"]:
                return
            Frame.set_console_text(message=message, date=date)

    def display_vm_status(self):
        """Displays connection status of remotes on console"""
        for Frame in self.__frames.values():
            if Frame == self.__frames["AboutPage"]:
                return
            Frame.display_vm_status()

    def set_vm_info_by_other_page_call(self, vm_index):
        """When Test Line selected in one Page, update Test Line info immediately on another Page"""
        for Frame in self.__frames.values():
            if Frame == self.__frames["AboutPage"]:
                return
            Frame.set_vm_info_by_other_page_call(vm_index)


# Not cool calling it here
gui = Gui()
