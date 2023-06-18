"""
Class: LogsPage
Author: Kamil Koltowski
Date: 2022-12-17
Description: This is LogsPage. I have no clue what's going on in this code, it's really messy.
"""
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext

import hashdata


class LogsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        """Manager method assigned by reference in set_gui_functionality()"""
        self.M_ref_set_vm_index = ...
        self.M_ref_get_vm_info = ...
        self.M_ref_get_tcpdump_info = ...
        self.M_ref_get_snapshot_info = ...
        self.M_ref_get_syslog_info = ...
        self.M_ref_get_errlog_info = ...
        self.m_set_gui_tl_list = None
        self.M_stop_main_thread = ...
        self.M_database_length = None

        """Gui controller and frames"""
        self.controller = controller
        self.__menu_frame: tk.Frame = tk.Frame(self, background=self.controller.bg_color, width=270, height=500,
                                               highlightbackground=self.controller.frame_color, highlightthickness=2,
                                               padx=5, pady=10)
        self.__logs_frame = tk.Frame(self, background=self.controller.bg_color, width=530, height=500,
                                     highlightbackground=self.controller.frame_color, highlightthickness=2, padx=10,
                                     pady=5)
        """String vars"""
        self.S_tcpdump_pid: tk.StringVar = ...
        self.S_tcpdump_name: tk.StringVar = ...
        self.S_tcpdump_size: tk.StringVar = ...
        self.S_tcpdump_time: tk.StringVar = ...
        self.S_tcpdump_status: tk.StringVar = ...
        self.S_snapshot_pid: tk.StringVar = ...
        self.S_snapshot_name: tk.StringVar = ...
        self.S_snapshot_size: tk.StringVar = ...
        self.S_snapshot_time: tk.StringVar = ...
        self.S_snapshot_status: tk.StringVar = ...
        self.S_syslog_pid: tk.StringVar = ...
        self.S_syslog_name: tk.StringVar = ...
        self.S_syslog_size: tk.StringVar = ...
        self.S_syslog_time: tk.StringVar = ...
        self.S_syslog_status: tk.StringVar = ...
        self.S_errlog_pid: tk.StringVar = ...
        self.S_errlog_name: tk.StringVar = ...
        self.S_errlog_size: tk.StringVar = ...
        self.S_errlog_time: tk.StringVar = ...
        self.S_errlog_status: tk.StringVar = ...

        """Buttons"""
        self.button_connect_to_vm: tk.Button = ...
        self.button_connect_to_sysmodule: tk.Button = ...
        self.button_disconnect_from_vm: tk.Button = ...
        self.button_disconnect_from_sysmodule: tk.Button = ...
        self.button_start_tcpdump: tk.Button = ...
        self.button_start_snapshot: tk.Button = ...
        self.button_start_syslog: tk.Button = ...
        self.button_start_errlog: tk.Button = ...
        self.button_stop_tcpdump: tk.Button = ...
        self.button_stop_syslog: tk.Button = ...
        self.button_stop_errlog: tk.Button = ...
        self.button_download_tcpdump: tk.Button = ...
        self.button_download_snapshot: tk.Button = ...
        self.button_download_syslog: tk.Button = ...
        self.button_download_errlog: tk.Button = ...
        self.button_upload_syslog_script: tk.Button = ...
        self.button_upload_errlog_scripts: tk.Button = ...

        """Progress Bars"""
        self.tcpdump_progress_bar = ...

        """Other widgets"""
        self.text_output = ...
        self._C_vm_list: ttk.Combobox = ...  # store list with vms string

        """Setup containers"""
        self.__setup_menu_container()
        self.__setup_logs_container()

    def setup(self, set_vm_index, get_vm_info, set_gui_tl_list, connect_to_vm, connect_to_sysmodule,
              disconnect_from_vm,
              disconnect_from_sysmodule, get_tcpdump_info, get_snapshot_info, get_syslog_info,
              get_errlog_info,
              start_tcpdump, stop_tcpdump, download_tcpdump, start_snapshot, download_snapshot,
              start_syslog, stop_syslog, upload_syslog_script, start_errlog,
              stop_errlog, download_errlog, upload_errlog_scripts, stop_main_thread, database_length):
        """Setup of all widgets, assign Manager methods passed by reference"""
        # TODO: TEMP
        self.m_set_gui_tl_list = set_gui_tl_list
        """Set Manager methods, passed by reference"""
        self.M_ref_set_vm_index = set_vm_index
        self.M_ref_get_vm_info = get_vm_info
        self.M_ref_get_tcpdump_info = get_tcpdump_info
        self.M_ref_get_snapshot_info = get_snapshot_info
        self.M_ref_get_syslog_info = get_syslog_info
        self.M_ref_get_errlog_info = get_errlog_info
        self.M_stop_main_thread = stop_main_thread
        self.M_database_length = database_length

        '''Combobox'''
        self._C_vm_list['values'] = set_gui_tl_list()
        self._C_vm_list.set("Select your test line")

        '''Buttons'''
        self.button_connect_to_vm.configure(command=lambda: connect_to_vm())
        self.button_connect_to_sysmodule.configure(command=lambda: connect_to_sysmodule())
        self.button_disconnect_from_vm.configure(command=lambda: disconnect_from_vm())
        self.button_disconnect_from_sysmodule.configure(command=lambda: disconnect_from_sysmodule())
        self.button_start_tcpdump.configure(command=lambda: start_tcpdump())
        self.button_stop_tcpdump.configure(command=lambda: stop_tcpdump())
        self.button_download_tcpdump.configure(command=lambda: download_tcpdump())
        self.button_start_snapshot.configure(command=lambda: start_snapshot())
        self.button_download_snapshot.configure(command=lambda: download_snapshot())
        self.button_start_syslog.configure(command=lambda: start_syslog())
        self.button_stop_syslog.configure(command=lambda: stop_syslog())
        # self.button_download_syslog.configure(command=lambda: download_syslog())
        self.button_upload_syslog_script.configure(command=lambda: upload_syslog_script())
        self.button_start_errlog.configure(command=lambda: start_errlog())
        self.button_stop_errlog.configure(command=lambda: stop_errlog())
        self.button_download_errlog.configure(command=lambda: download_errlog())
        self.button_upload_errlog_scripts.configure(command=lambda: upload_errlog_scripts())

    def display_vm_status(self):
        """
        Method sets Vm's info on GUI, it takes current selected vm index and vm info from Manager class.
        TODO: This is common for both pages so make them shared between them - display_vm_status() in Db page
        """
        if self.M_database_length() > 0:
            vm_info = self.M_ref_get_vm_info()
            self._S_vm_ip.set(vm_info['ip'])
            self._S_vm_status.set("Connected") if vm_info['vm_status'] else self._S_vm_status.set("Disconnected")
            self._S_sysmodule_status.set("Connected") if vm_info['sysmodule_status'] else self._S_sysmodule_status.set("Disconnected")

    def set_logs_info(self):
        """Methods do smth"""
        tcpdump = self.M_ref_get_tcpdump_info()
        snapshot = self.M_ref_get_snapshot_info()
        syslog = self.M_ref_get_syslog_info()
        errlog = self.M_ref_get_errlog_info()

        '''Tcpdump'''
        # s_tcpdump = [self.S_tcpdump-pid...]
        # for i in s_tcpdump... bla bla .set() w jednej linijce
        self.S_tcpdump_pid.set(tcpdump['log pid']) if tcpdump['log pid'] else self.S_tcpdump_pid.set("")
        self.S_tcpdump_name.set(tcpdump['log file']) if tcpdump['log file'] else self.S_tcpdump_name.set("")
        self.S_tcpdump_size.set(tcpdump['log size']) if tcpdump['log size'] else self.S_tcpdump_size.set("")
        self.S_tcpdump_time.set(tcpdump['logging time']) if tcpdump['logging time'] else self.S_tcpdump_time.set("")
        self.S_tcpdump_status.set("Logging") if tcpdump['is logging'] else self.S_tcpdump_status.set("Not logging")

        '''Snapshot'''
        self.S_snapshot_pid.set(snapshot['log pid']) if snapshot['log pid'] else self.S_snapshot_pid.set("")
        self.S_snapshot_name.set(snapshot['log file']) if snapshot['log file'] else self.S_snapshot_name.set("")
        self.S_snapshot_size.set(snapshot['log size']) if snapshot['log size'] else self.S_snapshot_size.set("")
        self.S_snapshot_time.set(snapshot['logging time']) if snapshot['logging time'] else self.S_snapshot_time.set("")
        self.S_snapshot_status.set("Logging") if snapshot['is logging'] else self.S_snapshot_status.set("Not logging")

        '''syslog'''
        self.S_syslog_pid.set(syslog['log pid']) if syslog['log pid'] else self.S_syslog_pid.set("")
        self.S_syslog_name.set(syslog['log file']) if syslog['log file'] else self.S_syslog_name.set("")
        self.S_syslog_size.set(syslog['log size']) if syslog['log size'] else self.S_syslog_size.set("")
        self.S_syslog_time.set(syslog['logging time']) if syslog['logging time'] else self.S_syslog_time.set("")
        self.S_syslog_status.set("Logging") if syslog['is logging'] else self.S_syslog_status.set("Not logging")

        '''Errlog'''
        self.S_errlog_pid.set(errlog['log pid']) if errlog['log pid'] is not None else self.S_errlog_pid.set("")
        self.S_errlog_name.set(errlog['log file']) if errlog['log file'] else self.S_errlog_name.set("")
        self.S_errlog_size.set(errlog['log size']) if errlog['log size'] else self.S_errlog_size.set("")
        self.S_errlog_time.set(errlog['logging time']) if errlog['logging time'] else self.S_errlog_time.set("")
        self.S_errlog_status.set("Logging") if errlog['is logging'] else self.S_errlog_status.set("Not logging")

    def tracing_vm_index(self, *arg):
        """
        Method is tracing combobox index, it updates gui vm info immediately when new vm is chosen.
        :param arg: does smth for tracing
        """
        vm_index = self._C_vm_list.current()
        if vm_index > -1:
            self.M_ref_set_vm_index(index=vm_index)
            self.display_vm_status()
            self.set_logs_info()

    def set_vm_info_by_other_page_call(self, vm_index):
        """ Called from Manager in __set_vm_index()
        Used when combobox is used in other Page, so it can update in this Page - Not the best solution!"""
        if self.M_database_length() == 0:
            self._C_vm_list.set('')
            self.clear_widgets()
        else:
            self._C_vm_list['values'] = self.m_set_gui_tl_list()
            self._C_vm_list.current(newindex=vm_index)
            self.display_vm_status()
            self.set_logs_info()

    def set_console_text(self, message, date):
        self.text_output['state'] = 'normal'
        self.text_output.insert(tk.INSERT, f"\n {'-' * 26} \n{date} | {message}")
        self.text_output.see('end')
        self.text_output['state'] = 'disabled'  # kurwa ale druciarstwo

    def clear_widgets(self):
        widgets = [self._S_vm_ip, self._S_vm_status, self._S_sysmodule_status]
        for w in widgets:
            w.set("")

    def __setup_menu_container(self):
        """Creates widgets for menu container"""
        "Grid menu frame"
        self.__menu_frame.grid(row=0, column=0, sticky="nsew")
        self.__menu_frame.grid_propagate(False)

        "StringVars"
        self._S_vm_ip = tk.StringVar()
        self._S_vm_status = tk.StringVar()
        self._S_sysmodule_status = tk.StringVar()
        self._S_vm_list_index = tk.StringVar()

        "Combobox"
        self._C_vm_list = ttk.Combobox(self.__menu_frame, width=39, state="readonly",
                                       textvariable=self._S_vm_list_index)

        "Labels"
        l_vm_ip = tk.Label(self.__menu_frame, text="VM IP: ", font=self.controller.font, bg=self.controller.bg_color,
                           width=7,
                           height=1)
        l_vm_status = tk.Label(self.__menu_frame, text="VM: ", font=self.controller.font, bg=self.controller.bg_color,
                               width=7,
                               height=1)
        l_sysmodule_status = tk.Label(self.__menu_frame, text=f"{hashdata.SYSMODULE_ID}: ", font=self.controller.font,
                                      bg=self.controller.bg_color,
                                      width=7, height=1)

        "Entries"
        entry_vm_ip = tk.Entry(self.__menu_frame, readonlybackground=self.controller.entry_and_button_color,
                               borderwidth=2,
                               state='readonly',
                               font=self.controller.font, width=15, textvariable=self._S_vm_ip)
        entry_vm_status = tk.Entry(self.__menu_frame, disabledbackground=self.controller.entry_and_button_color,
                                   disabledforeground=self.controller.entry_fg_color,
                                   borderwidth=2,
                                   state='disabled',
                                   font=self.controller.font, width=15, textvariable=self._S_vm_status)
        entry_sysmodule_status = tk.Entry(self.__menu_frame, disabledbackground=self.controller.entry_and_button_color,
                                          disabledforeground=self.controller.entry_fg_color,
                                          borderwidth=2,
                                          state='disabled',
                                          font=self.controller.font, width=15, textvariable=self._S_sysmodule_status)

        "Buttons"
        self.button_connect_to_vm = tk.Button(self.__menu_frame, text="Connect\nto VM", width=20, relief=tk.RAISED,
                                              borderwidth=2,
                                              activebackground=self.controller.entry_and_button_color,
                                              bg=self.controller.entry_and_button_color)
        self.button_connect_to_sysmodule = tk.Button(self.__menu_frame, text=f"Connect\nto {hashdata.SYSMODULE_ID}", width=20, relief=tk.RAISED,
                                                     borderwidth=2,
                                                     activebackground=self.controller.entry_and_button_color,
                                                     bg=self.controller.entry_and_button_color)
        self.button_disconnect_from_vm = tk.Button(self.__menu_frame, text="Disconnect\nfrom VM", width=10,
                                                   relief=tk.RAISED,
                                                   borderwidth=2,
                                                   activebackground=self.controller.entry_and_button_color,
                                                   bg=self.controller.entry_and_button_color)
        self.button_disconnect_from_sysmodule = tk.Button(self.__menu_frame, text=f"Disconnect\nfrom {hashdata.SYSMODULE_ID}", width=10,
                                                          relief=tk.RAISED,
                                                          borderwidth=2,
                                                          activebackground=self.controller.entry_and_button_color,
                                                          bg=self.controller.entry_and_button_color)
        b_database = tk.Button(self.__menu_frame, text="Edit TLs\nDatabase", width=20, relief=tk.RAISED, borderwidth=2,
                               activebackground=self.controller.entry_and_button_color,
                               bg=self.controller.entry_and_button_color,
                               command=lambda: self.controller.show_frame("DatabasePage"))
        b_exit = tk.Button(self.__menu_frame, text="Exit", width=10, height=2, relief=tk.RAISED, borderwidth=2,
                           activebackground=self.controller.entry_and_button_color,
                           bg=self.controller.entry_and_button_color,
                           command=lambda: self.controller.quit_tool())

        "Text"
        self.text_output = scrolledtext.ScrolledText(self.__menu_frame, wrap=tk.WORD, state='normal',
                                                     background=self.controller.entry_and_button_color,
                                                     width=28, height=8)
        self.text_output.insert(tk.INSERT, hashdata.WELCOME_TEXT)
        self.text_output['state'] = 'disabled'  # kurwa ale druciarstwo

        "Layout widgets"
        self._C_vm_list.grid(row=0, columnspan=2)
        l_vm_ip.grid(row=2, column=0, sticky='', pady=10)
        l_vm_status.grid(row=3, column=0, sticky='', pady=10)
        l_sysmodule_status.grid(row=4, column=0, sticky='', pady=10)

        entry_vm_ip.grid(row=2, column=1, sticky='w', pady=10)
        entry_vm_status.grid(row=3, column=1, sticky='w', pady=10)
        entry_sysmodule_status.grid(row=4, column=1, sticky='w', pady=10)

        self.button_connect_to_vm.grid(row=5, column=1, pady=10)
        self.button_connect_to_sysmodule.grid(row=6, column=1, pady=10)
        self.button_disconnect_from_vm.grid(row=5, column=0, pady=10, padx=5)
        self.button_disconnect_from_sysmodule.grid(row=6, column=0, pady=10)

        self.text_output.grid(row=7, columnspan=2, pady=10)

        b_database.grid(row=9, column=1, pady=5)
        b_exit.grid(row=9, column=0, pady=5, padx=5)

        "Setup tracing"
        self._S_vm_list_index.trace('w', self.tracing_vm_index)

    def __setup_logs_container(self):
        """Creates widgets for logs container."""

        "Grid logs container"
        self.__logs_frame.grid(row=0, column=1, sticky="nsew")
        self.__logs_frame.grid_propagate(False)

        """String vars"""
        '''Tcpdump'''
        self.S_tcpdump_pid = tk.StringVar()
        self.S_tcpdump_name = tk.StringVar()
        self.S_tcpdump_size = tk.StringVar()
        self.S_tcpdump_time = tk.StringVar()
        self.S_tcpdump_status = tk.StringVar()

        '''Snapshot'''
        self.S_snapshot_pid = tk.StringVar()
        self.S_snapshot_name = tk.StringVar()
        self.S_snapshot_size = tk.StringVar()
        self.S_snapshot_time = tk.StringVar()
        self.S_snapshot_status = tk.StringVar()

        '''syslog'''
        self.S_syslog_pid = tk.StringVar()
        self.S_syslog_name = tk.StringVar()
        self.S_syslog_size = tk.StringVar()
        self.S_syslog_time = tk.StringVar()
        self.S_syslog_status = tk.StringVar()

        '''Errlog'''
        self.S_errlog_pid = tk.StringVar()
        self.S_errlog_name = tk.StringVar()
        self.S_errlog_size = tk.StringVar()
        self.S_errlog_time = tk.StringVar()
        self.S_errlog_status = tk.StringVar()

        "Labels"
        '''Tcpdump'''
        label_tcpdump_title = tk.Label(self.__logs_frame, text="TCPDUMP", font=self.controller.font,
                                       bg=self.controller.frame_color, fg='white',
                                       width=20)
        label_tcpdump_pid = tk.Label(self.__logs_frame, text="PID: ", bg=self.controller.frame_color, fg='white')
        label_tcpdump_name = tk.Label(self.__logs_frame, text="Name: ", bg=self.controller.bg_color)
        label_tcpdump_size = tk.Label(self.__logs_frame, text="Size: ", bg=self.controller.bg_color)
        label_tcpdump_time = tk.Label(self.__logs_frame, text="Time: ", bg=self.controller.bg_color)
        label_tcpdump_status = tk.Label(self.__logs_frame, text="Status: ", bg=self.controller.bg_color)
        # change label_log_empty to determine space between entreis and buttons
        label_tcpdump_empty = tk.Label(self.__logs_frame, text="", bg=self.controller.bg_color, width=6)

        '''Snapshot'''
        label_snapshot_title = tk.Label(self.__logs_frame, text="SNAPSHOT", font=self.controller.font,
                                        bg=self.controller.frame_color, fg='white',
                                        width=20)
        label_snapshot_pid = tk.Label(self.__logs_frame, text="PID: ", bg=self.controller.frame_color, fg='white')
        label_snapshot_name = tk.Label(self.__logs_frame, text="Name: ", bg=self.controller.bg_color)
        label_snapshot_size = tk.Label(self.__logs_frame, text="Size: ", bg=self.controller.bg_color)
        label_snapshot_time = tk.Label(self.__logs_frame, text="Time: ", bg=self.controller.bg_color)
        label_snapshot_status = tk.Label(self.__logs_frame, text="Status: ", bg=self.controller.bg_color)
        label_snapshot_empty = tk.Label(self.__logs_frame, text="", bg=self.controller.bg_color, width=6)

        '''syslog'''
        label_syslog_title = tk.Label(self.__logs_frame, text="SYSLOG", font=self.controller.font,
                                      bg=self.controller.frame_color, fg='white',
                                      width=20)
        label_syslog_pid = tk.Label(self.__logs_frame, text="PID: ", bg=self.controller.frame_color, fg='white')
        label_syslog_name = tk.Label(self.__logs_frame, text="Name: ", bg=self.controller.bg_color)
        label_syslog_size = tk.Label(self.__logs_frame, text="Size: ", bg=self.controller.bg_color)
        label_syslog_time = tk.Label(self.__logs_frame, text="Time: ", bg=self.controller.bg_color)
        label_syslog_status = tk.Label(self.__logs_frame, text="Status: ", bg=self.controller.bg_color)
        label_syslog_empty = tk.Label(self.__logs_frame, text="", bg=self.controller.bg_color, width=6)

        '''Errlog'''
        label_errlog_title = tk.Label(self.__logs_frame, text=f"{hashdata.ERRLOG_ID}", font=self.controller.font,
                                      bg=self.controller.frame_color, fg='white',
                                      width=20)
        label_errlog_pid = tk.Label(self.__logs_frame, text="PID: ", bg=self.controller.frame_color, fg='white')
        label_errlog_name = tk.Label(self.__logs_frame, text="Name: ", bg=self.controller.bg_color)
        label_errlog_size = tk.Label(self.__logs_frame, text="Size: ", bg=self.controller.bg_color)
        label_errlog_time = tk.Label(self.__logs_frame, text="Time: ", bg=self.controller.bg_color)
        label_errlog_status = tk.Label(self.__logs_frame, text="Status: ", bg=self.controller.bg_color)
        label_errlog_empty = tk.Label(self.__logs_frame, text="", bg=self.controller.bg_color, width=6)

        "Entries"
        '''Tcpdump'''
        entry_tcpdump_pid = tk.Entry(self.__logs_frame, readonlybackground=self.controller.entry_and_button_color,
                                     borderwidth=2, disabledforeground='#343434',
                                     state='readonly', width=8, textvariable=self.S_tcpdump_pid)
        # TODO: changed width to 37, was 36 - fitting both pages title bar
        entry_tcpdump_name = tk.Entry(self.__logs_frame, readonlybackground=self.controller.entry_and_button_color,
                                      borderwidth=2, disabledforeground='#343434',
                                      state='readonly', width=42, textvariable=self.S_tcpdump_name)
        entry_tcpdump_size = tk.Entry(self.__logs_frame, readonlybackground=self.controller.entry_and_button_color,
                                      borderwidth=2, disabledforeground='#343434',
                                      state='readonly', width=12, textvariable=self.S_tcpdump_size)
        entry_tcpdump_time = tk.Entry(self.__logs_frame, readonlybackground=self.controller.entry_and_button_color,
                                      borderwidth=2, disabledforeground='#343434',
                                      state='readonly', width=12, textvariable=self.S_tcpdump_time)
        entry_tcpdump_status = tk.Entry(self.__logs_frame, readonlybackground=self.controller.entry_and_button_color,
                                        borderwidth=2, disabledforeground='#343434',
                                        state='readonly', width=12, textvariable=self.S_tcpdump_status)

        '''Snapshot'''
        entry_snapshot_pid = tk.Entry(self.__logs_frame, readonlybackground=self.controller.entry_and_button_color,
                                      borderwidth=2, disabledforeground='#343434',
                                      state='readonly', width=8, textvariable=self.S_snapshot_pid)
        entry_snapshot_name = tk.Entry(self.__logs_frame, readonlybackground=self.controller.entry_and_button_color,
                                       borderwidth=2, disabledforeground='#343434',
                                       state='readonly', width=42, textvariable=self.S_snapshot_name)
        entry_snapshot_size = tk.Entry(self.__logs_frame, readonlybackground=self.controller.entry_and_button_color,
                                       borderwidth=2, disabledforeground='#343434',
                                       state='readonly', width=12, textvariable=self.S_snapshot_size)
        entry_snapshot_time = tk.Entry(self.__logs_frame, readonlybackground=self.controller.entry_and_button_color,
                                       borderwidth=2, disabledforeground='#343434',
                                       state='readonly', width=12, textvariable=self.S_snapshot_time)
        entry_snapshot_status = tk.Entry(self.__logs_frame, readonlybackground=self.controller.entry_and_button_color,
                                         borderwidth=2, disabledforeground='#343434',
                                         state='readonly', width=12, textvariable=self.S_snapshot_status)

        '''syslog'''
        entry_syslog_pid = tk.Entry(self.__logs_frame, readonlybackground=self.controller.entry_and_button_color,
                                    borderwidth=2, disabledforeground='#343434',
                                    state='readonly', width=8, textvariable=self.S_syslog_pid)
        entry_syslog_name = tk.Entry(self.__logs_frame, readonlybackground=self.controller.entry_and_button_color,
                                     borderwidth=2, disabledforeground='#343434',
                                     state='readonly', width=42, textvariable=self.S_syslog_name)
        entry_syslog_size = tk.Entry(self.__logs_frame, readonlybackground=self.controller.entry_and_button_color,
                                     borderwidth=2, disabledforeground='#343434',
                                     state='readonly', width=12, textvariable=self.S_syslog_size)
        entry_syslog_time = tk.Entry(self.__logs_frame, readonlybackground=self.controller.entry_and_button_color,
                                     borderwidth=2, disabledforeground='#343434',
                                     state='readonly', width=12, textvariable=self.S_syslog_time)
        entry_syslog_status = tk.Entry(self.__logs_frame, readonlybackground=self.controller.entry_and_button_color,
                                       borderwidth=2, disabledforeground='#343434',
                                       state='readonly', width=12, textvariable=self.S_syslog_status)

        '''Errlog'''
        entry_errlog_pid = tk.Entry(self.__logs_frame, readonlybackground=self.controller.entry_and_button_color,
                                    borderwidth=2, disabledforeground='#343434',
                                    state='readonly', width=8, textvariable=self.S_errlog_pid)
        entry_errlog_name = tk.Entry(self.__logs_frame, readonlybackground=self.controller.entry_and_button_color,
                                     borderwidth=2, disabledforeground='#343434',
                                     state='readonly', width=42, textvariable=self.S_errlog_name)
        entry_errlog_size = tk.Entry(self.__logs_frame, readonlybackground=self.controller.entry_and_button_color,
                                     borderwidth=2, disabledforeground='#343434',
                                     state='readonly', width=12, textvariable=self.S_errlog_size)
        entry_errlog_time = tk.Entry(self.__logs_frame, readonlybackground=self.controller.entry_and_button_color,
                                     borderwidth=2, disabledforeground='#343434',
                                     state='readonly', width=12, textvariable=self.S_errlog_time)
        entry_errlog_status = tk.Entry(self.__logs_frame, readonlybackground=self.controller.entry_and_button_color,
                                       borderwidth=2, disabledforeground='#343434',
                                       state='readonly', width=12, textvariable=self.S_errlog_status)

        "Buttons"
        '''Tcpdump'''
        self.button_start_tcpdump = tk.Button(self.__logs_frame, text="START\nTCPDUMP", relief=tk.RAISED, borderwidth=2,
                                              activebackground=self.controller.entry_and_button_color,
                                              bg=self.controller.entry_and_button_color,
                                              width=9)
        self.button_stop_tcpdump = tk.Button(self.__logs_frame, text="STOP\nTCPDUMP", relief=tk.RAISED, borderwidth=2,
                                             activebackground=self.controller.entry_and_button_color,
                                             bg=self.controller.entry_and_button_color,
                                             width=9)
        self.button_download_tcpdump = tk.Button(self.__logs_frame, text="DL\nTCPDUMP", relief=tk.RAISED, borderwidth=2,
                                                 activebackground=self.controller.entry_and_button_color,
                                                 bg=self.controller.entry_and_button_color, width=9)

        '''Snapshot'''
        self.button_start_snapshot = tk.Button(self.__logs_frame, text="START\nSNAPSHOT", relief=tk.RAISED,
                                               borderwidth=2,
                                               activebackground=self.controller.entry_and_button_color,
                                               bg=self.controller.entry_and_button_color, width=9)
        self.button_download_snapshot = tk.Button(self.__logs_frame, text="DL\nSNAPSHOT", relief=tk.RAISED,
                                                  borderwidth=2,
                                                  activebackground=self.controller.entry_and_button_color, width=9,
                                                  bg=self.controller.entry_and_button_color)

        '''syslog'''
        self.button_start_syslog = tk.Button(self.__logs_frame, text="START\nSYSLOG", relief=tk.RAISED, borderwidth=2,
                                             activebackground=self.controller.entry_and_button_color,
                                             bg=self.controller.entry_and_button_color,
                                             width=9)
        self.button_stop_syslog = tk.Button(self.__logs_frame, text="STOP\nSYSLOG", relief=tk.RAISED, borderwidth=2,
                                            activebackground=self.controller.entry_and_button_color,
                                            bg=self.controller.entry_and_button_color,
                                            width=9)
        # self.button_download_syslog = tk.Button(self.__logs_frame, text="DL\nSYSLOG", relief=tk.RAISED, borderwidth=2,
        #                                         activebackground=self.controller.entry_and_button_color,
        #                                         bg=self.controller.entry_and_button_color, width=9)
        self.button_upload_syslog_script = tk.Button(self.__logs_frame, text="UL\nSCRIPT", relief=tk.RAISED,
                                                     borderwidth=2,
                                                     activebackground=self.controller.entry_and_button_color,
                                                     bg=self.controller.entry_and_button_color,
                                                     width=9)

        '''Errlog'''
        self.button_start_errlog = tk.Button(self.__logs_frame, text=f"START\n{hashdata.ERRLOG_ID}", relief=tk.RAISED, borderwidth=2,
                                             activebackground=self.controller.entry_and_button_color,
                                             bg=self.controller.entry_and_button_color,
                                             width=9)
        self.button_stop_errlog = tk.Button(self.__logs_frame, text=f"STOP\n{hashdata.ERRLOG_ID}", relief=tk.RAISED, borderwidth=2,
                                            activebackground=self.controller.entry_and_button_color,
                                            bg=self.controller.entry_and_button_color,
                                            width=9)
        self.button_download_errlog = tk.Button(self.__logs_frame, text=f"DL\n{hashdata.ERRLOG_ID}", relief=tk.RAISED, borderwidth=2,
                                                activebackground=self.controller.entry_and_button_color,
                                                bg=self.controller.entry_and_button_color, width=9)
        self.button_upload_errlog_scripts = tk.Button(self.__logs_frame, text="UL\nSCRIPT", relief=tk.RAISED,
                                                      borderwidth=2,
                                                      activebackground=self.controller.entry_and_button_color,
                                                      bg=self.controller.entry_and_button_color,
                                                      width=9)
        '''Progress Bar'''
        # progressbar_style = ttk.Style()
        # progressbar_style.theme_use('clam')
        # progressbar_style.configure("red.Horizontal.TProgressbar", troughcolor=self.controller.entry_and_button_color,
        #                             bordercolor=self.controller.frame_color)

        # self.tcpdump_progress_bar = ttk.Progressbar(self.__logs_frame, style='red.Horizontal.TProgressbar',
        #                                             orient='horizontal', mode='determinate', length=180)
        # self.entry_downloading_time = tk.Entry(self.__logs_frame, readonlybackground=self.controller.entry_and_button_color,
        #                             borderwidth=2, disabledforeground='#343434',
        #                             state='readonly', width=8)
        # self.entry_downloading_speed = tk.Entry(self.__logs_frame, readonlybackground=self.controller.entry_and_button_color,
        #                             borderwidth=2, disabledforeground='#343434',
        #                             state='readonly', width=8)
        # self.entry_calculated_progress = tk.Entry()

        "Layout widgets"
        '''Tcpdump'''
        label_tcpdump_title.grid(row=0, column=0, columnspan=6, sticky='ew', pady=1)
        label_tcpdump_pid.grid(row=0, column=0, sticky='w', pady=1)
        label_tcpdump_name.grid(row=1, column=0, sticky='w', pady=1)
        label_tcpdump_size.grid(row=2, column=0, sticky='w', pady=1)
        label_tcpdump_time.grid(row=3, column=0, sticky='w', pady=1)
        label_tcpdump_status.grid(row=4, column=0, sticky='w', pady=1)

        label_tcpdump_empty.grid(row=1, column=3, sticky='ew', pady=1)

        entry_tcpdump_pid.grid(row=0, column=1, sticky='w')
        entry_tcpdump_name.grid(row=1, column=1, columnspan=2, sticky='w')
        entry_tcpdump_size.grid(row=2, column=1, sticky='w')
        entry_tcpdump_time.grid(row=3, column=1, sticky='w')
        entry_tcpdump_status.grid(row=4, column=1, sticky='w')

        # Progress bar
        # self.tcpdump_progress_bar.grid(row=4, column=2, columnspan=2, padx=18)
        # self.entry_downloading_time.grid(row=3, column=3, sticky='w', padx=3)
        # self.entry_downloading_speed.grid(row=2, column=3, sticky='w', padx=3)

        self.button_start_tcpdump.grid(row=1, column=5, rowspan=2, pady=3, padx=3, sticky='e')
        self.button_stop_tcpdump.grid(row=3, column=5, rowspan=2, pady=3, padx=3, sticky='e')
        self.button_download_tcpdump.grid(row=3, column=4, rowspan=2, pady=3, padx=3)

        '''Snapshot'''
        label_snapshot_title.grid(row=5, column=0, columnspan=6, sticky='ew', pady=1)
        label_snapshot_pid.grid(row=5, column=0, sticky='w', pady=1)
        label_snapshot_name.grid(row=6, column=0, sticky='w', pady=1)
        label_snapshot_size.grid(row=7, column=0, sticky='w', pady=1)
        label_snapshot_time.grid(row=8, column=0, sticky='w', pady=1)
        label_snapshot_status.grid(row=9, column=0, sticky='w', pady=1)

        label_snapshot_empty.grid(row=6, column=3, sticky='ew', pady=1)

        entry_snapshot_pid.grid(row=5, column=1, sticky='w')
        entry_snapshot_name.grid(row=6, column=1, columnspan=2, sticky='w')
        entry_snapshot_size.grid(row=7, column=1, sticky='w')
        entry_snapshot_time.grid(row=8, column=1, sticky='w')
        entry_snapshot_status.grid(row=9, column=1, sticky='w')

        self.button_start_snapshot.grid(row=6, column=5, rowspan=2, pady=3, padx=3)
        self.button_download_snapshot.grid(row=8, column=5, rowspan=2, pady=3, padx=3)

        '''syslog'''
        label_syslog_title.grid(row=10, column=0, columnspan=6, sticky='ew', pady=1)
        label_syslog_pid.grid(row=10, column=0, sticky='w', pady=1)
        label_syslog_name.grid(row=11, column=0, sticky='w', pady=1)
        label_syslog_size.grid(row=12, column=0, sticky='w', pady=1)
        label_syslog_time.grid(row=13, column=0, sticky='w', pady=1)
        label_syslog_status.grid(row=14, column=0, sticky='w', pady=1)

        label_syslog_empty.grid(row=11, column=3, sticky='ew', pady=1)

        entry_syslog_pid.grid(row=10, column=1, sticky='w')
        entry_syslog_name.grid(row=11, column=1, columnspan=2, sticky='w')
        entry_syslog_size.grid(row=12, column=1, sticky='w')
        entry_syslog_time.grid(row=13, column=1, sticky='w')
        entry_syslog_status.grid(row=14, column=1, sticky='w')

        self.button_start_syslog.grid(row=11, column=5, rowspan=2, pady=3, padx=3)
        self.button_stop_syslog.grid(row=13, column=5, rowspan=2, pady=3, padx=3)
        # self.button_download_syslog.grid(row=11, column=4, rowspan=2, pady=3, padx=3)
        self.button_upload_syslog_script.grid(row=13, column=4, rowspan=2, pady=3, padx=3)

        '''Errlog'''
        label_errlog_title.grid(row=15, column=0, columnspan=6, sticky='ew', pady=1)
        label_errlog_pid.grid(row=15, column=0, sticky='w', pady=1)
        label_errlog_name.grid(row=16, column=0, sticky='w', pady=1)
        label_errlog_size.grid(row=17, column=0, sticky='w', pady=1)
        label_errlog_time.grid(row=18, column=0, sticky='w', pady=1)
        label_errlog_status.grid(row=19, column=0, sticky='w', pady=1)

        label_errlog_empty.grid(row=16, column=3, sticky='ew', pady=1)

        entry_errlog_pid.grid(row=15, column=1, sticky='w')
        entry_errlog_name.grid(row=16, column=1, columnspan=2, sticky='w')
        entry_errlog_size.grid(row=17, column=1, sticky='w')
        entry_errlog_time.grid(row=18, column=1, sticky='w')
        entry_errlog_status.grid(row=19, column=1, sticky='w')

        self.button_start_errlog.grid(row=16, column=5, rowspan=2, pady=3, padx=3)
        self.button_stop_errlog.grid(row=18, column=5, rowspan=2, pady=3, padx=3)
        self.button_download_errlog.grid(row=18, column=4, rowspan=2, pady=3, padx=3)
        self.button_upload_errlog_scripts.grid(row=16, column=4, rowspan=2, pady=3, padx=3)
