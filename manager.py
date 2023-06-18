"""
Class: Manager
Author: Kamil Koltowski
Date: 2022-04-04
Description: This class represents a Manager, it manages the logic of entire tool between gui and backend.
"""
import os.path
import hashdata
from vm import Vm
from database import Database
from threads import Thread
from gui import gui


class Manager(object):
    def __init__(self):
        self.__vm_index: int = 0
        self.__Db = Database()
        self.__Thread = Thread()

    def run(self):
        gui.mainloop()

    def setup(self):
        self.__erase_backlog()
        self.__setup_database()
        self.__initialise_database()
        self.__Thread.run_main_thread()
        gui.setup_frames()
        gui.get_logs_page().setup(set_vm_index=self.__set_vm_index,
                                  get_vm_info=self.__get_vm_info,
                                  set_gui_tl_list=self.__get_vms_for_gui,
                                  connect_to_vm=self.__connect_to_vm,
                                  connect_to_sysmodule=self.__connect_to_sysmodule,
                                  disconnect_from_vm=self.__disconnect_from_vm,
                                  disconnect_from_sysmodule=self.__disconnect_from_sysmodule,
                                  get_tcpdump_info=self.__get_tcpdump_info,
                                  get_snapshot_info=self.__get_snapshot_info,
                                  get_syslog_info=self.__get_syslog_info,
                                  get_errlog_info=self.__get_errlog_info,
                                  start_tcpdump=self.__start_tcpdump,
                                  stop_tcpdump=self.__stop_tcpdump,
                                  download_tcpdump=self.__download_tcpdump,
                                  start_snapshot=self.__start_snapshot,
                                  download_snapshot=self.__download_snapshot,
                                  start_syslog=self.__start_syslog,
                                  stop_syslog=self.__stop_syslog,
                                  upload_syslog_script=self.__upload_syslog_script,
                                  start_errlog=self.__start_errlog,
                                  stop_errlog=self.__stop_errlog,
                                  download_errlog=self.__download_errlog,
                                  upload_errlog_scripts=self.__upload_errlog_scripts,
                                  stop_main_thread=self.__stop_all_logs_and_main_thread,
                                  database_length=self.__database_length)

        gui.get_database_page().setup(get_vm_index=self.__get_vm_index,
                                      set_vm_index=self.__set_vm_index,
                                      get_vm_info=self.__get_vm_info,
                                      get_vms_for_gui=self.__get_vms_for_gui,
                                      connect_to_vm=self.__connect_to_vm,
                                      connect_to_sysmodule=self.__connect_to_sysmodule,
                                      disconnect_from_vm=self.__disconnect_from_vm,
                                      disconnect_from_sysmodule=self.__disconnect_from_sysmodule,
                                      add_new_vm=self.__add_new_vm_and_initialise_it,
                                      edit_vm=self.__edit_vm,
                                      remove_vm=self.__remove_vm,
                                      move_vm_up=self.__move_vm_up,
                                      move_vm_down=self.__move_vm_down,
                                      database_length=self.__database_length)

    def __get_vm_index(self) -> int:
        return self.__vm_index

    def __set_vm_index(self, index: int):
        """Set current chosen vm ID, default operations on VMs are based on that ID
        :param index: VM's index to be set
        """
        self.__vm_index = index
        gui.set_vm_info_by_other_page_call(self.__vm_index)

    def __stop_all_logs_on_exit(self):
        for vm in self.__Db.initialised_database:
            if vm.is_connected:
                for log in vm.logs:
                    if log.is_logging:
                        vm.stop_logs_on_exit()
            if vm.sysmodule.is_connected:
                if vm.sysmodule.is_connected:
                    for log in vm.sysmodule.logs:
                        if log.is_logging:
                            vm.sysmodule.stop_logs_on_exit()

    def __stop_all_logs_and_main_thread(self):
        self.__stop_all_logs_on_exit()
        self.__Thread.stop_main_thread()

    def __erase_backlog(self):
        if os.path.exists(hashdata.PATH_TO_BACKLOG):
            open(f"{hashdata.PATH_TO_BACKLOG}", "w").close()

    def __setup_database(self):
        self.__Db.setup_database()

    def __database_length(self):
        return self.__Db.initialised_database_length

    def __initialise_database(self):
        """Initialise VM objects"""
        for i in range(len(self.__Db.raw_database)):
            self.__Db.add_vm_to_initialised_database(vm=Vm(**self.__Db.raw_database[i]))

    def __get_vm_info(self) -> dict:
        """Returns VMs info, based on assigned ID. It reads data from Database."""
        if self.__Db.initialised_database_length > 0:
            vm_info = self.__Db.get_vm_info(index=self.__vm_index)
            # obj = self.__Db.initialised_database[self.__vm_index]
            vm_status = self.__Db.initialised_database[self.__vm_index].is_connected
            sysmodule_status = self.__Db.initialised_database[self.__vm_index].sysmodule.is_connected
            vm_info |= {'vm_status': vm_status, 'sysmodule_status': sysmodule_status}
            return vm_info

    def __get_vms_for_gui(self) -> tuple:
        return self.__Db.get_converted_database_names()

    def __add_new_vm_and_initialise_it(self, hostname: str, username: str, password: str, description: str):
        """Adds new VM to a raw database, create VM object and append it to initialised database
        :param hostname: new hostname
        :param username: new username
        :param password: new password
        :param description: new description
        """
        self.__Db.add_vm_to_database(hostname=hostname, username=username, password=password, description=description)
        self.__Db.add_vm_to_initialised_database(vm=Vm(**self.__Db.raw_database[-1]))

    def __edit_vm(self, hostname: str, username: str, password: str, description: str):
        """ Edit existed VM in raw_database, Initialise again existed VM object, with new parameters, but same index
        :param hostname: new hostname
        :param username: new username
        :param password: new password
        :param description: new description
        """
        if not self.__Db.initialised_database[self.__vm_index].is_connected:
            self.__Db.edit_vm_in_database(index=self.__vm_index, hostname=hostname, username=username,
                                          password=password, description=description)
            self.__Db.edit_vm_in_initialised_database(index=self.__vm_index,
                                                      vm=Vm(**self.__Db.raw_database[self.__vm_index]))

    def __remove_vm(self):
        if not self.__Db.initialised_database[self.__vm_index].is_connected:
            self.__Db.remove_session_from_database(index=self.__vm_index)

    def __move_vm_up(self):
        if self.__vm_index > 0:
            self.__Db.move_vm(state='up', index=self.__vm_index)
            self.__set_vm_index(index=self.__vm_index - 1)

    def __move_vm_down(self):
        if self.__vm_index < self.__database_length() - 1:
            self.__Db.move_vm(state='down', index=self.__vm_index)
            self.__set_vm_index(index=self.__vm_index + 1)

    def __connect_to_vm(self):
        if not self.__Db.initialised_database[self.__vm_index].is_connected:
            self.__Db.initialised_database[self.__vm_index].start_session()

            if self.__Db.initialised_database[self.__vm_index].is_connected:
                self.__Thread.run_thread(
                    thread=self.__Db.initialised_database[self.__vm_index].thread_is_session_active,
                    collection=self.__Thread.ssh_threads,
                    name=self.__Db.initialised_database[self.__vm_index].description)

    def __connect_to_sysmodule(self):
        if not self.__Db.initialised_database[self.__vm_index].sysmodule.is_connected and \
                self.__Db.initialised_database[self.__vm_index].is_connected:
            self.__Db.initialised_database[self.__vm_index].connect_to_sysmodule()
            self.__Thread.run_thread(
                thread=self.__Db.initialised_database[self.__vm_index].sysmodule.thread_is_session_active,
                collection=self.__Thread.ssh_threads,
                name=self.__Db.initialised_database[self.__vm_index].sysmodule.description)

    def __disconnect_from_vm(self):
        self.__Db.initialised_database[self.__vm_index].stop_session()

    def __disconnect_from_sysmodule(self):
        self.__Db.initialised_database[self.__vm_index].sysmodule.stop_session()

    def __get_tcpdump_info(self):
        return self.__Db.initialised_database[self.__vm_index].sysmodule.tcpdump.log_info

    def __get_snapshot_info(self):
        return self.__Db.initialised_database[self.__vm_index].sysmodule.snapshot.log_info

    def __get_syslog_info(self):
        return self.__Db.initialised_database[self.__vm_index].syslog.log_info

    def __get_errlog_info(self):
        return self.__Db.initialised_database[self.__vm_index].sysmodule.errlog.log_info

    def __start_tcpdump(self):
        if not self.__Db.initialised_database[self.__vm_index].sysmodule.tcpdump.is_logging and \
                self.__Db.initialised_database[self.__vm_index].sysmodule.is_connected:
            self.__Db.initialised_database[self.__vm_index].sysmodule.start_tcpdump()
            self.__Thread.run_thread(
                thread=self.__Db.initialised_database[self.__vm_index].sysmodule.thread_is_pid_alive,
                collection=self.__Thread.log_threads,
                log=self.__Db.initialised_database[self.__vm_index].sysmodule.tcpdump,
                name=self.__Db.initialised_database[self.__vm_index].sysmodule.tcpdump.log_filename)

    def __stop_tcpdump(self):
        if self.__Db.initialised_database[self.__vm_index].sysmodule.tcpdump.is_logging:
            self.__Db.initialised_database[self.__vm_index].sysmodule.stop_tcpdump()

    def __download_tcpdump(self):
        if not self.__Db.initialised_database[self.__vm_index].sysmodule.tcpdump.is_logging and \
                self.__Db.initialised_database[self.__vm_index].sysmodule.is_connected:
            self.__Db.initialised_database[self.__vm_index].download_tcpdump_from_sysmodule()

    def __start_snapshot(self):
        if not self.__Db.initialised_database[self.__vm_index].sysmodule.snapshot.is_logging and \
                self.__Db.initialised_database[self.__vm_index].sysmodule.is_connected:
            self.__Db.initialised_database[self.__vm_index].sysmodule.start_snapshot()
            self.__Thread.run_thread(
                thread=self.__Db.initialised_database[self.__vm_index].sysmodule.thread_is_pid_alive,
                collection=self.__Thread.log_threads,
                log=self.__Db.initialised_database[self.__vm_index].sysmodule.snapshot,
                name=self.__Db.initialised_database[self.__vm_index].sysmodule.snapshot.log_filename)
            self.__Thread.run_thread(
                thread=self.__Db.initialised_database[self.__vm_index].sysmodule.thread_snapshot_verifier)

    def __download_snapshot(self):
        if not self.__Db.initialised_database[self.__vm_index].sysmodule.snapshot.is_logging and \
                self.__Db.initialised_database[self.__vm_index].sysmodule.is_connected:
            self.__Db.initialised_database[self.__vm_index].download_snapshot_from_sysmodule()

    def __start_syslog(self):
        if not self.__Db.initialised_database[self.__vm_index].syslog.is_logging and \
                self.__Db.initialised_database[self.__vm_index].is_connected:
            self.__Db.initialised_database[self.__vm_index].start_syslog()
            self.__Thread.run_thread(thread=self.__Db.initialised_database[self.__vm_index].thread_is_pid_alive,
                                     collection=self.__Thread.log_threads,
                                     log=self.__Db.initialised_database[self.__vm_index].syslog,
                                     name=self.__Db.initialised_database[
                                         self.__vm_index].syslog.log_filename)

    def __stop_syslog(self):
        if self.__Db.initialised_database[self.__vm_index].is_connected and \
                self.__Db.initialised_database[self.__vm_index].syslog.is_logging:
            self.__Db.initialised_database[self.__vm_index].stop_syslog()

    def __upload_syslog_script(self):
        if self.__Db.initialised_database[self.__vm_index].is_connected:
            self.__Db.initialised_database[self.__vm_index].upload_syslog_script()

    def __start_errlog(self):
        if not self.__Db.initialised_database[self.__vm_index].sysmodule.errlog.is_logging and \
                self.__Db.initialised_database[self.__vm_index].sysmodule.is_connected:
            self.__Db.initialised_database[self.__vm_index].sysmodule.start_errlog()
            self.__Thread.run_thread(
                thread=self.__Db.initialised_database[self.__vm_index].sysmodule.thread_is_pid_alive,
                collection=self.__Thread.log_threads,
                log=self.__Db.initialised_database[self.__vm_index].sysmodule.errlog,
                name=self.__Db.initialised_database[self.__vm_index].sysmodule.errlog.log_filename,
                errlog=True)

    def __stop_errlog(self):
        if self.__Db.initialised_database[self.__vm_index].sysmodule.is_connected and \
                self.__Db.initialised_database[self.__vm_index].sysmodule.errlog.is_logging:
            self.__Db.initialised_database[self.__vm_index].sysmodule.stop_errlog()

    def __download_errlog(self):
        if self.__Db.initialised_database[self.__vm_index].sysmodule.is_connected:
            self.__Db.initialised_database[self.__vm_index].download_errlog_from_sysmodule()

    def __upload_errlog_scripts(self):
        if self.__Db.initialised_database[self.__vm_index].sysmodule.is_connected:
            self.__Db.initialised_database[self.__vm_index].upload_errlog_scripts()
            self.__Db.initialised_database[self.__vm_index].sysmodule.create_errlog_environment()
