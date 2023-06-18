"""
Class: DatabasePage
Author: Kamil Koltowski
Date: 2022-12-17
Description: This is DatabasePage. I have no clue what's going on in this code, it's really messy.
"""
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext

import hashdata


class DatabasePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        """Gui controller and frames"""
        self.controller = controller
        self.f_menu_frame: tk.Frame = tk.Frame(self, background=self.controller.bg_color, width=270, height=500,
                                               highlightbackground=self.controller.frame_color, highlightthickness=2,
                                               padx=5, pady=10)
        self.f_editor_frame = tk.Frame(self, background=self.controller.bg_color, width=530, height=500,
                                       highlightbackground=self.controller.frame_color, highlightthickness=2,
                                       padx=10, pady=5)
        """Manager referenced methods"""
        self.m_set_vm_index = None
        self.m_get_vm_info = None
        self.m_get_vms_for_gui = None
        self.m_add_new_vm = None
        self.m_edit_vm = None
        self.m_remove_vm = None
        self.m_move_vm_up = None
        self.m_move_vm_down = None
        self.m_database_length = None
        self.m_get_vm_index = None

        """Widgets"""
        "Combobox"
        # TODO: common for both pages, make them shared between them so status could be updated properly
        # Used to store vms in combobox
        self.c_vms_list: ttk.Combobox = ttk.Combobox()

        "StringVars"
        '''Menu Window'''
        # TODO: These are common for both pages, make them shared between them so status could be updated properly
        self.s_vm_ip: tk.StringVar = tk.StringVar()
        self.s_vm_status: tk.StringVar = tk.StringVar()
        self.s_sysmodule_status: tk.StringVar = tk.StringVar()
        self.s_vms_in_total: tk.StringVar = tk.StringVar()

        self.s_vm_description: tk.StringVar = tk.StringVar()
        self.s_vm_ip: tk.StringVar = tk.StringVar()
        self.s_vm_username: tk.StringVar = tk.StringVar()
        self.s_vm_password: tk.StringVar = tk.StringVar()
        self.s_vm_index: tk.StringVar = tk.StringVar()
        self.s_vms_in_total: tk.StringVar = tk.StringVar()

        self.s_vm_description_planned: tk.StringVar = tk.StringVar()
        self.s_vm_ip_planned: tk.StringVar = tk.StringVar()
        self.s_vm_username_planned: tk.StringVar = tk.StringVar()
        self.s_vm_password_planned: tk.StringVar = tk.StringVar()
        self.s_vm_index_planned: tk.StringVar = tk.StringVar()
        self.s_vms_in_total_planned: tk.StringVar = tk.StringVar()

        # Create a variable to track a combobox index (this is some kind of object necessary for tracing)
        self.s_trace_vm_index: tk.StringVar = tk.StringVar()
        # Create a variable to set a combobox index (this is a String Variable)
        self.s_vm_index: tk.StringVar = tk.StringVar()

        """Labels"""
        '''Menu Window'''
        self.l_vm_ip: tk.Label = tk.Label()
        self.l_vm_status: tk.Label = tk.Label()
        self.l_sysmodule_status: tk.Label = tk.Label()

        '''Database Window'''
        self.l_database_editor_title: tk.Label = tk.Label()
        self.l_vm_description: tk.Label = tk.Label()
        self.l_vm_ip: tk.Label = tk.Label()
        self.l_vm_username: tk.Label = tk.Label()
        self.l_vm_password: tk.Label = tk.Label()
        self.l_vm_index: tk.Label = tk.Label()
        self.l_vms_in_total: tk.Label = tk.Label()
        self.l_actual_value: tk.Label = tk.Label()
        self.l_planned_value: tk.Label = tk.Label()

        """Entries"""
        '''Menu Window'''
        self.e_vm_ip: tk.Entry = tk.Entry()
        self.e_vm_status: tk.Entry = tk.Entry()
        self.e_sysmodule_status: tk.Entry = tk.Entry()

        '''Database Window'''
        self.e_vm_description: tk.Entry = tk.Entry()
        self.e_vm_ip: tk.Entry = tk.Entry()
        self.e_vm_username: tk.Entry = tk.Entry()
        self.e_vm_password: tk.Entry = tk.Entry()
        self.e_vm_index: tk.Entry = tk.Entry()
        self.e_vms_in_total: tk.Entry = tk.Entry()
        self.e_vm_description_planned: tk.Entry = tk.Entry()
        self.e_vm_ip_planned: tk.Entry = tk.Entry()
        self.e_vm_username_planned: tk.Entry = tk.Entry()
        self.e_vm_password_planned: tk.Entry = tk.Entry()
        self.e_vm_index_planned: tk.Entry = tk.Entry()
        self.e_vms_in_total_planned: tk.Entry = tk.Entry()

        """Buttons"""
        '''Menu Window'''
        self.b_connect_to_vm: tk.Button = tk.Button()
        self.b_connect_to_sysmodule: tk.Button = tk.Button()
        self.b_disconnect_from_vm: tk.Button = tk.Button()
        self.b_disconnect_from_sysmodule: tk.Button = tk.Button()
        self.b_back: tk.Button = tk.Button()
        self.b_about: tk.Button = tk.Button()

        '''Database Window'''
        self.b_move_vm_up: tk.Button = tk.Button()
        self.b_move_vm_down: tk.Button = tk.Button()
        self.b_save_changes: tk.Button = tk.Button()
        self.b_discard_changes: tk.Button = tk.Button()
        self.b_add_new_vm: tk.Button = tk.Button()
        self.b_remove_vm: tk.Button = tk.Button()

        """ScrolledText"""
        self.st_console_text: tk.Text = tk.Text()

    def setup(self, get_vm_index, set_vm_index, get_vm_info, get_vms_for_gui, connect_to_vm, connect_to_sysmodule,
              disconnect_from_vm,
              disconnect_from_sysmodule, add_new_vm, edit_vm, remove_vm, move_vm_up, move_vm_down, database_length):
        """Setups gui functionality, assigning things to widgets
        :param vm_index: property vm_index
        :param set_vm_index: Passed by reference Manager method that sets vm index
        :param get_vm_info: Passed by reference Manager method that returns vm info
        :param get_vms_for_gui: Passed by reference Manager method that returns vms tuple for gui combobox
        :param connect_to_vm: Passed by reference Manager method that connects to vm
        :param connect_to_sysmodule: Passed by reference Manager method that connects to sysmodule
        :param disconnect_from_vm: Passed by reference Manager method that disconnects from vm
        :param disconnect_from_sysmodule: Passed by reference Manager method that disconnects from sysmodule
        :param add_new_vm:
        :param edit_vm:
        :param remove_vm:
        :param move_vm_up:
        :param move_vm_down:
        """
        '''Setup reference for Manager methods'''
        self.m_get_vm_index = get_vm_index
        self.m_set_vm_index = set_vm_index
        self.m_get_vm_info = get_vm_info
        self.m_add_new_vm = add_new_vm
        self.m_edit_vm = edit_vm
        self.m_remove_vm = remove_vm
        self.m_move_vm_up = move_vm_up
        self.m_move_vm_down = move_vm_down
        self.m_get_vms_for_gui = get_vms_for_gui
        self.m_database_length = database_length

        '''Setup containers'''
        self.setup_menu_container()
        self.setup_database_container()

        '''Configure buttons'''
        self.b_connect_to_vm.configure(command=lambda: connect_to_vm())
        self.b_connect_to_sysmodule.configure(command=lambda: connect_to_sysmodule())
        self.b_disconnect_from_vm.configure(command=lambda: disconnect_from_vm())
        self.b_disconnect_from_sysmodule.configure(command=lambda: disconnect_from_sysmodule())

    def set_console_text(self, message, date):
        # TODO: This should be defined once and used via reference by both pages
        self.st_console_text['state'] = 'normal'
        self.st_console_text.insert(tk.INSERT, f"\n {'-' * 26} \n{date} | {message}")
        self.st_console_text.see('end')
        self.st_console_text['state'] = 'disabled'

    def display_vm_status(self):
        """Method displays Vm status on GUI, it takes current selected VM info from Manager class.
         TODO: This is common for both pages so make them shared between them - set_vm_info() in Logs
        """
        if self.m_database_length() > 0:
            vm_info = self.m_get_vm_info()
            self.s_vm_ip.set(vm_info['ip'])
            self.s_vm_status.set("Connected") if vm_info['vm_status'] else self.s_vm_status.set("Disconnected")
            self.s_sysmodule_status.set("Connected") if vm_info['sysmodule_status'] else self.s_sysmodule_status.set(
                "Disconnected")

    def display_vm_info(self):
        """Method displays VMs info in editor frame"""
        if self.m_database_length() > 0:
            vm_info = self.m_get_vm_info()
            self.s_vm_ip.set(vm_info['ip'])
            self.s_vm_description.set(vm_info['description'])
            self.s_vm_username.set(vm_info['username'])
            self.s_vm_password.set(vm_info['password'])
            self.s_vm_index.set(self.m_get_vm_index() + 1)
            self.s_vms_in_total.set(self.m_database_length())

            self.s_vm_ip_planned.set(vm_info['ip'])
            self.s_vm_description_planned.set(vm_info['description'])
            self.s_vm_username_planned.set(vm_info['username'])
            self.s_vm_password_planned.set(vm_info['password'])
            self.s_vm_index_planned.set(self.m_get_vm_index() + 1)
            self.s_vms_in_total_planned.set(self.m_database_length())

    def set_vm_info_by_other_page_call(self, vm_index):
        """ Called from Manager
        Used when combobox is used in other Page, so it can update in this Page - Not the best solution!"""

        if self.m_database_length() == 0:
            self.c_vms_list.set('')
            self.clear_vm_entries()
        else:
            self.c_vms_list.current(newindex=vm_index)
            self.display_vm_status()
            self.display_vm_info()

    def trace_when_vm_from_combobox_is_selected(self, *args):
        """When item from combobox is selected, it triggers this method.
        :param args: no idea what is this, necessary for tracing
        """
        vm_index = self.c_vms_list.current()
        if vm_index > -1:
            self.m_set_vm_index(index=vm_index)
            self.display_vm_status()
            self.display_vm_info()

    def clear_vm_entries(self):
        widgets = [self.s_vm_ip, self.s_vm_username, self.s_vm_password, self.s_vm_description, self.s_vm_index,
                   self.s_vms_in_total, self.s_vm_ip_planned, self.s_vm_username_planned, self.s_vm_password_planned,
                   self.s_vm_description_planned, self.s_vm_index_planned, self.s_vms_in_total_planned,
                   self.s_vm_status, self.s_sysmodule_status]
        for w in widgets:
            w.set("")

    def refresh_vm_info(self):
        # set all instructions from other methods
        ...

    def add_new_vm(self):
        """Clean actual value spots, add in planned index+1 and vms in total + 1"""
        vm_info = self.m_get_vm_info()
        self.clear_vm_entries()
        self.s_vm_index_planned.set(self.m_database_length() + 1)
        self.s_vms_in_total_planned.set(self.m_database_length() + 1)

    def remove_vm(self):
        """Remove vm from list by index"""
        '''if database empty or index planned higher than actual, its edit mode so removing forbidden'''
        if self.m_database_length() == 0 or int(self.s_vms_in_total_planned.get()) == (self.m_database_length() + 1):
            return

        index = self.m_get_vm_index()

        self.m_remove_vm()

        if self.m_database_length == 0:
            self.c_vms_list.set('')
        else:
            self.c_vms_list['values'] = self.m_get_vms_for_gui()

        if index > self.m_database_length() - 1:
            self.m_set_vm_index(index=index - 1)
        elif index < self.m_database_length():
            self.m_set_vm_index(index=index)
        else:
            self.m_set_vm_index(index=0)

        self.display_vm_status()
        self.display_vm_info()

    def save_changes(self):
        ip = self.e_vm_ip_planned.get()
        username = self.e_vm_username_planned.get()
        password = self.e_vm_password_planned.get()
        description = self.e_vm_description_planned.get()
        vm_index = self.c_vms_list.current()

        '''If value in actual widget, is equal to in total -> user is editing VM'''
        if self.e_vms_in_total.get() == str(self.m_database_length()):
            """Save changes, if editing existing vm, replace parameters. If creating new, add vm to list"""
            self.m_edit_vm(hostname=ip,
                           username=username,
                           password=password,
                           description=description)
            self.c_vms_list['values'] = self.m_get_vms_for_gui()
            self.m_set_vm_index(index=vm_index)

        '''If value in planned widget, is greater than in total -> user is adding VM'''
        if self.e_vms_in_total_planned.get() > str(self.m_database_length()):
            self.m_add_new_vm(hostname=ip,
                              username=username,
                              password=password,
                              description=description)
            self.c_vms_list['values'] = self.m_get_vms_for_gui()
            if self.m_database_length() == 1:
                self.m_set_vm_index(index=self.m_database_length() - 1)
            else:
                self.m_set_vm_index(index=self.m_database_length() - 1)

        self.discard_changes()

    def discard_changes(self):
        """Clean planned entries, display actual values"""
        self.clear_vm_entries()
        self.display_vm_status()
        self.display_vm_info()

    def move_vm_up(self):
        if self.m_get_vm_index() > 0:
            self.m_move_vm_up()
            self.c_vms_list['values'] = self.m_get_vms_for_gui()
            self.c_vms_list.current(self.m_get_vm_index())
            self.display_vm_info()
            self.display_vm_status()

    def move_vm_down(self):
        self.m_move_vm_down()
        self.c_vms_list['values'] = self.m_get_vms_for_gui()
        self.c_vms_list.current(self.m_get_vm_index())
        self.display_vm_info()
        self.display_vm_status()

    def setup_menu_container(self):
        """Creates widgets for menu container"""
        """--=Setup Widgets=--"""
        "--=Grid menu frame=--"
        self.f_menu_frame.grid(row=0, column=0, sticky="nsew")
        self.f_menu_frame.grid_propagate(False)

        "Combobox"
        self.c_vms_list = ttk.Combobox(self.f_menu_frame, width=39, state="readonly",
                                       textvariable=self.s_trace_vm_index)
        self.c_vms_list.set("Select your test line")
        self.s_trace_vm_index.trace('w', self.trace_when_vm_from_combobox_is_selected)
        self.c_vms_list['values'] = self.m_get_vms_for_gui()

        "StringVars"
        self.s_vm_ip = tk.StringVar()
        self.s_vm_status = tk.StringVar()
        self.s_sysmodule_status = tk.StringVar()

        "Labels"
        self.l_vm_ip = tk.Label(self.f_menu_frame, text="VM IP: ", font=self.controller.font,
                                bg=self.controller.bg_color,
                                width=7,
                                height=1)
        self.l_vm_status = tk.Label(self.f_menu_frame, text="VM: ", font=self.controller.font,
                                    bg=self.controller.bg_color,
                                    width=7,
                                    height=1)
        self.l_sysmodule_status = tk.Label(self.f_menu_frame, text=f"{hashdata.SYSMODULE_ID}: ",
                                           font=self.controller.font,
                                           bg=self.controller.bg_color,
                                           width=7, height=1)

        "Entries"
        self.e_vm_ip = tk.Entry(self.f_menu_frame, readonlybackground=self.controller.entry_and_button_color,
                                borderwidth=2,
                                state='readonly',
                                font=self.controller.font, width=15, textvariable=self.s_vm_ip)
        self.e_vm_status = tk.Entry(self.f_menu_frame, disabledbackground=self.controller.entry_and_button_color,
                                    disabledforeground=self.controller.entry_fg_color,
                                    borderwidth=2,
                                    state='disabled',
                                    font=self.controller.font, width=15, textvariable=self.s_vm_status)
        self.e_sysmodule_status = tk.Entry(self.f_menu_frame, disabledbackground=self.controller.entry_and_button_color,
                                           disabledforeground=self.controller.entry_fg_color,
                                           borderwidth=2,
                                           state='disabled',
                                           font=self.controller.font, width=15, textvariable=self.s_sysmodule_status)

        "Buttons"
        self.b_connect_to_vm = tk.Button(self.f_menu_frame, text="Connect\nto VM", width=20, relief=tk.RAISED,
                                         borderwidth=2,
                                         activebackground=self.controller.entry_and_button_color,
                                         bg=self.controller.entry_and_button_color)
        self.b_connect_to_sysmodule = tk.Button(self.f_menu_frame, text=f"Connect\nto {hashdata.SYSMODULE_ID}", width=20,
                                                relief=tk.RAISED,
                                                borderwidth=2,
                                                activebackground=self.controller.entry_and_button_color,
                                                bg=self.controller.entry_and_button_color)
        self.b_disconnect_from_vm = tk.Button(self.f_menu_frame, text="Disconnect\nfrom VM", width=10,
                                              relief=tk.RAISED,
                                              borderwidth=2,
                                              activebackground=self.controller.entry_and_button_color,
                                              bg=self.controller.entry_and_button_color)
        self.b_disconnect_from_sysmodule = tk.Button(self.f_menu_frame, text=f"Disconnect\nfrom {hashdata.SYSMODULE_ID}",
                                                     width=10,
                                                     relief=tk.RAISED,
                                                     borderwidth=2,
                                                     activebackground=self.controller.entry_and_button_color,
                                                     bg=self.controller.entry_and_button_color)
        self.b_back = tk.Button(self.f_menu_frame, text="Back to\nLogs Page", width=20, relief=tk.RAISED, borderwidth=2,
                                activebackground=self.controller.entry_and_button_color,
                                bg=self.controller.entry_and_button_color,
                                command=lambda: self.controller.show_frame("LogsPage"))
        self.b_about = tk.Button(self.f_menu_frame, text="About", width=10, height=2, relief=tk.RAISED, borderwidth=2,
                                 activebackground=self.controller.entry_and_button_color,
                                 bg=self.controller.entry_and_button_color,
                                 command=lambda: self.controller.show_frame("AboutPage"))

        "ScrolledText"
        self.st_console_text = scrolledtext.ScrolledText(self.f_menu_frame, wrap=tk.WORD, state='normal',
                                                         background=self.controller.entry_and_button_color,
                                                         width=28, height=8)
        self.st_console_text.insert(tk.INSERT, hashdata.WELCOME_TEXT)
        self.st_console_text['state'] = 'disabled'  # kurwa ale druciarstwo

        "--=Layout widgets=--"
        """Combobox"""
        self.c_vms_list.grid(row=0, columnspan=2)

        """Labels"""
        self.l_vm_ip.grid(row=2, column=0, sticky='', pady=10)
        self.l_vm_status.grid(row=3, column=0, sticky='', pady=10)
        self.l_sysmodule_status.grid(row=4, column=0, sticky='', pady=10)

        """Entries"""
        self.e_vm_ip.grid(row=2, column=1, sticky='w', pady=10)
        self.e_vm_status.grid(row=3, column=1, sticky='w', pady=10)
        self.e_sysmodule_status.grid(row=4, column=1, sticky='w', pady=10)

        """Buttons"""
        self.b_connect_to_vm.grid(row=5, column=1, pady=10)
        self.b_connect_to_sysmodule.grid(row=6, column=1, pady=10)
        self.b_disconnect_from_vm.grid(row=5, column=0, pady=10, padx=5)
        self.b_disconnect_from_sysmodule.grid(row=6, column=0, pady=10)
        self.b_back.grid(row=9, column=1, pady=5)
        self.b_about.grid(row=9, column=0, pady=5, padx=5)

        """ScrolledText"""
        self.st_console_text.grid(row=7, columnspan=2, pady=10)

    def setup_database_container(self):
        """Creates widgets for config container"""

        "--=Grid settings frame=--"
        self.f_editor_frame.grid(row=0, column=1, sticky="nsew")
        self.f_editor_frame.grid_propagate(False)

        """--=Setup Widgets=--"""
        "Labels"
        self.l_database_editor_title = tk.Label(self.f_editor_frame, text="Test Line Editor",
                                                font=self.controller.font,
                                                bg=self.controller.frame_color, fg='white', width=20)
        self.l_planned_value = tk.Label(self.f_editor_frame, text="Planned Value", font=self.controller.font,
                                        bg=self.controller.bg_color, width=12, padx=20)
        self.l_actual_value = tk.Label(self.f_editor_frame, text="Actual Value", font=self.controller.font,
                                       bg=self.controller.bg_color, width=12, padx=20)
        self.l_vm_description = tk.Label(self.f_editor_frame, text="Description:", font=self.controller.font,
                                         bg=self.controller.bg_color, width=12, height=1, padx=3)
        self.l_vm_ip = tk.Label(self.f_editor_frame, text="VM IP:", font=self.controller.font,
                                bg=self.controller.bg_color, width=12)
        self.l_vm_username = tk.Label(self.f_editor_frame, text="Username:", font=self.controller.font,
                                      bg=self.controller.bg_color, width=12)
        self.l_vm_password = tk.Label(self.f_editor_frame, text="Password:", font=self.controller.font,
                                      bg=self.controller.bg_color, width=12)
        self.l_vm_index = tk.Label(self.f_editor_frame, text="Index:", font=self.controller.font,
                                   bg=self.controller.bg_color, width=12)
        self.l_vms_in_total = tk.Label(self.f_editor_frame, text="VMs:", font=self.controller.font,
                                       bg=self.controller.bg_color, width=12)
        l_empty_space = tk.Label(self.f_editor_frame, text="", bg=self.controller.bg_color, width=6)
        l_empty_space_2 = tk.Label(self.f_editor_frame, text="", bg=self.controller.bg_color, width=6)

        "Entries"
        self.e_vm_description = tk.Entry(self.f_editor_frame, disabledbackground=self.controller.entry_and_button_color,
                                         disabledforeground=self.controller.entry_fg_color,
                                         borderwidth=2, state='disabled', font=self.controller.font, width=15,
                                         textvariable=self.s_vm_description)
        self.e_vm_ip = tk.Entry(self.f_editor_frame, disabledbackground=self.controller.entry_and_button_color,
                                disabledforeground=self.controller.entry_fg_color,
                                borderwidth=2, state='disabled', font=self.controller.font, width=15,
                                textvariable=self.s_vm_ip)
        self.e_vm_username = tk.Entry(self.f_editor_frame, disabledbackground=self.controller.entry_and_button_color,
                                      disabledforeground=self.controller.entry_fg_color,
                                      borderwidth=2, state='disabled', font=self.controller.font, width=15,
                                      textvariable=self.s_vm_username)
        self.e_vm_password = tk.Entry(self.f_editor_frame, disabledbackground=self.controller.entry_and_button_color,
                                      disabledforeground=self.controller.entry_fg_color,
                                      borderwidth=2, state='disabled', font=self.controller.font, width=15,
                                      textvariable=self.s_vm_password)
        self.e_vm_index = tk.Entry(self.f_editor_frame, disabledbackground=self.controller.entry_and_button_color,
                                   disabledforeground=self.controller.entry_fg_color, borderwidth=2,
                                   state='disabled',
                                   font=self.controller.font, width=15, textvariable=self.s_vm_index)
        self.e_vms_in_total = tk.Entry(self.f_editor_frame, disabledbackground=self.controller.entry_and_button_color,
                                       disabledforeground=self.controller.entry_fg_color,
                                       borderwidth=2, state='disabled', font=self.controller.font, width=15,
                                       textvariable=self.s_vms_in_total)

        self.e_vm_description_planned = tk.Entry(self.f_editor_frame,
                                                 readonlybackground=self.controller.entry_and_button_color,
                                                 bg=self.controller.entry_and_button_color,
                                                 borderwidth=2, state='normal', font=self.controller.font, width=15,
                                                 textvariable=self.s_vm_description_planned)
        self.e_vm_ip_planned = tk.Entry(self.f_editor_frame, readonlybackground=self.controller.entry_and_button_color,
                                        bg=self.controller.entry_and_button_color,
                                        borderwidth=2, state='normal', font=self.controller.font, width=15,
                                        textvariable=self.s_vm_ip_planned)
        self.e_vm_username_planned = tk.Entry(self.f_editor_frame,
                                              readonlybackground=self.controller.entry_and_button_color,
                                              bg=self.controller.entry_and_button_color,
                                              borderwidth=2, state='normal', font=self.controller.font, width=15,
                                              textvariable=self.s_vm_username_planned)
        self.e_vm_password_planned = tk.Entry(self.f_editor_frame,
                                              readonlybackground=self.controller.entry_and_button_color,
                                              bg=self.controller.entry_and_button_color,
                                              borderwidth=2, state='normal', font=self.controller.font, width=15,
                                              textvariable=self.s_vm_password_planned)
        self.e_vm_index_planned = tk.Entry(self.f_editor_frame,
                                           disabledbackground=self.controller.entry_and_button_color,
                                           disabledforeground=self.controller.entry_fg_color, borderwidth=2,
                                           state='disabled',
                                           font=self.controller.font, width=15, textvariable=self.s_vm_index_planned)
        self.e_vms_in_total_planned = tk.Entry(self.f_editor_frame,
                                               disabledbackground=self.controller.entry_and_button_color,
                                               disabledforeground=self.controller.entry_fg_color,
                                               borderwidth=2, state='disabled', font=self.controller.font, width=15,
                                               textvariable=self.s_vms_in_total_planned)

        "Buttons"
        self.b_save_changes = tk.Button(self.f_editor_frame, text="Save\nChanges", width=20, relief=tk.RAISED,
                                        borderwidth=2, activebackground=self.controller.entry_and_button_color,
                                        bg=self.controller.entry_and_button_color, command=lambda: self.save_changes())
        self.b_discard_changes = tk.Button(self.f_editor_frame, text="Discard\nChanges", width=20, relief=tk.RAISED,
                                           borderwidth=2, activebackground=self.controller.entry_and_button_color,
                                           bg=self.controller.entry_and_button_color,
                                           command=lambda: self.discard_changes())
        self.b_add_new_vm = tk.Button(self.f_editor_frame, text="Add New\nVM", width=20, relief=tk.RAISED,
                                      borderwidth=2, activebackground=self.controller.entry_and_button_color,
                                      bg=self.controller.entry_and_button_color, command=lambda: self.add_new_vm())
        self.b_remove_vm = tk.Button(self.f_editor_frame, text="Remove\nVM", width=20, relief=tk.RAISED,
                                     borderwidth=2, activebackground=self.controller.entry_and_button_color,
                                     bg=self.controller.entry_and_button_color, command=lambda: self.remove_vm())
        self.b_move_vm_up = tk.Button(self.f_editor_frame, text="Move VM\nUp", width=10, relief=tk.RAISED,
                                      borderwidth=2, activebackground=self.controller.entry_and_button_color,
                                      bg=self.controller.entry_and_button_color, command=lambda: self.move_vm_up())
        self.b_move_vm_down = tk.Button(self.f_editor_frame, text="Move VM\nDown", width=10, relief=tk.RAISED,
                                        borderwidth=2, activebackground=self.controller.entry_and_button_color,
                                        bg=self.controller.entry_and_button_color, command=lambda: self.move_vm_down())

        "--=Layout widgets=--"
        # row 0
        self.l_database_editor_title.grid(row=0, column=0, columnspan=4, sticky='ew', pady=1)

        # row 1
        self.l_planned_value.grid(row=1, column=1, sticky='', pady=10)
        l_empty_space.grid(row=1, column=2, sticky='')
        self.l_actual_value.grid(row=1, column=3, sticky='', pady=9)

        # row 2
        self.l_vm_description.grid(row=2, column=0, sticky='', pady=10)
        self.e_vm_description_planned.grid(row=2, column=1, sticky='', pady=10)
        self.e_vm_description.grid(row=2, column=3, sticky='', pady=9)

        # row 3
        self.l_vm_ip.grid(row=3, column=0, sticky='', pady=10)
        self.e_vm_ip_planned.grid(row=3, column=1, sticky='', pady=10)
        self.e_vm_ip.grid(row=3, column=3, sticky='', pady=9)

        # row 4
        self.l_vm_username.grid(row=4, column=0, sticky='', pady=10)
        self.e_vm_username_planned.grid(row=4, column=1, sticky='', pady=10)
        self.e_vm_username.grid(row=4, column=3, sticky='', pady=9)

        # row 5
        self.l_vm_password.grid(row=5, column=0, sticky='', pady=10)
        self.e_vm_password_planned.grid(row=5, column=1, sticky='', pady=10)
        self.e_vm_password.grid(row=5, column=3, sticky='', pady=9)

        # row 6
        self.l_vm_index.grid(row=6, column=0, sticky='', pady=10)
        self.e_vm_index_planned.grid(row=6, column=1, sticky='', pady=10)
        self.e_vm_index.grid(row=6, column=3, sticky='', pady=9)

        # row 7
        self.l_vms_in_total.grid(row=7, column=0, sticky='', pady=10)
        self.e_vms_in_total_planned.grid(row=7, column=1, sticky='', pady=10)
        self.e_vms_in_total.grid(row=7, column=3, sticky='', pady=9)

        l_empty_space_2.grid(row=8, column=2, sticky='')

        # row 8
        self.b_move_vm_up.grid(row=9, column=0, pady=9)
        self.b_save_changes.grid(row=9, column=1, pady=9)
        self.b_discard_changes.grid(row=9, column=3, pady=9)

        # row 9
        self.b_move_vm_down.grid(row=10, column=0, pady=9)
        self.b_add_new_vm.grid(row=10, column=1, pady=9)
        self.b_remove_vm.grid(row=10, column=3, pady=9)
