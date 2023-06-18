"""
Class: AboutPage
Author: Kamil Koltowski
Date: 2022-12-17
Description: This is AboutPage, it contains just about stuff.

Class: HyperlinkManager
Author: Unknown
E-mail: -
Date: 2023-02-17
Description: This class do all hyperlink stuff, found it on stackoverflow.
"""
import tkinter as tk
import webbrowser
import hashdata


class HyperlinkManager(object):
    def __init__(self, text):
        self.text = text
        self.text.tag_config("hyper", foreground="blue", underline=1)
        self.text.tag_bind("hyper", "<Enter>", self._enter)
        self.text.tag_bind("hyper", "<Leave>", self._leave)
        self.text.tag_bind("hyper", "<Button-1>", self._click)
        self.links = {}

    def add(self, action):
        tag = "hyper-%d" % len(self.links)
        self.links[tag] = action
        return "hyper", tag

    def _enter(self, event):
        self.text.config(cursor="hand2")

    def _leave(self, event):
        self.text.config(cursor="")

    def _click(self, event):
        for tag in self.text.tag_names(tk.CURRENT):
            if tag[:6] == "hyper-":
                self.links[tag]()
                return


class AboutPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.contact = hashdata.CONTACT
        self.url = hashdata.URL
        self.version = hashdata.VERSION
        self.text = hashdata.TEXT
        """Gui controller and frames"""
        self.controller = controller
        self.f_main_frame: tk.Frame = tk.Frame(self, background=self.controller.bg_color, width=800, height=500,
                                               highlightbackground=self.controller.frame_color, highlightthickness=2)
        self.image = tk.PhotoImage(file=hashdata.PATH_TO_ICON_PNG)
        self.setup_main_container()

    def open_url(self):
        webbrowser.open(url=self.url)

    def setup_main_container(self):
        """Create widgets for main container"""
        self.f_main_frame.grid(row=0, column=0, sticky="nsew")
        self.f_main_frame.grid_propagate(False)

        l_image = tk.Label(self.f_main_frame, image=self.image)
        l_text = tk.Label(self.f_main_frame, text=self.text, font=self.controller.font,
                          bg=self.controller.bg_color)
        l_contact = tk.Label(self.f_main_frame, text="Contact: ", font=self.controller.font,
                             bg=self.controller.bg_color)
        l_gitlab = tk.Label(self.f_main_frame, text="Github: ", font=self.controller.font,
                            bg=self.controller.bg_color)
        l_version = tk.Label(self.f_main_frame, text="Version: ", font=self.controller.font,
                             bg=self.controller.bg_color)

        t_contact = tk.Text(self.f_main_frame, width=35, height=1, font='Helvetica 10 bold', background=self.controller.entry_and_button_color)
        t_gitlab = tk.Text(self.f_main_frame, width=35, height=1, font='Helvetica 10 bold', background=self.controller.entry_and_button_color)
        t_version = tk.Text(self.f_main_frame, width=35, height=1, font='Helvetica 10 bold', background=self.controller.entry_and_button_color)
        hyperlink = HyperlinkManager(t_gitlab)
        t_contact.insert(tk.INSERT, self.contact)
        t_gitlab.insert(tk.INSERT, self.url, hyperlink.add(self.open_url))
        t_version.insert(tk.INSERT, self.version)

        t_contact.configure(state='disabled')
        t_gitlab.configure(state='disabled')
        t_version.configure(state='disabled')

        b_back = tk.Button(self.f_main_frame, text="Back to TLs\nDatabase Page", width=15, relief=tk.RAISED,
                           borderwidth=2,
                           activebackground=self.controller.entry_and_button_color,
                           bg=self.controller.entry_and_button_color,
                           command=lambda: self.controller.show_frame("DatabasePage"))

        l_image.grid(row=0, column=0, columnspan=20, sticky='', pady=20)
        l_text.grid(row=1, column=0, columnspan=20, sticky='w', pady=5)
        l_contact.grid(row=2, column=0, sticky='e', pady=5)
        l_gitlab.grid(row=3, column=0, sticky='e', pady=5)
        l_version.grid(row=4, column=0, sticky='e', pady=5)

        t_contact.grid(row=2, column=1, sticky='w', pady=5)
        t_gitlab.grid(row=3, column=1, sticky='w', pady=5)
        t_version.grid(row=4, column=1, sticky='w', pady=5)
        b_back.grid(row=6, column=0, columnspan=20, sticky='ws', pady=10, padx=10)
