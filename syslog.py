"""
Class: Syslog
Author: Kamil Koltowski
Date: 2022-06-24
Description: This class represents a syslog.
"""
from log import Log
import commands
import hashdata


class Syslog(Log):
    def __init__(self):
        super().__init__()
        self._log_identifier: str = "SYSLOG"
        self._log_format: str = ".log"
        self._log_pid_identifier: str = "syslog_script"
        self._log_directory: str = hashdata.VM_DEFAULT_DIR
        self.__script_filename: str = "syslog_script"
        self.__script_output: str = "syslog_output.txt"
        self.__script_directory: str = hashdata.VM_DEFAULT_DIR

    @property
    def script_filename(self) -> str:
        return self.__script_filename

    @property
    def force_kill_command(self) -> str:
        return f"killall {self.__script_filename}"

    @property
    def script_name(self):
        return self.__script_filename

    @property
    def start_log_command(self) -> str:
        return commands.start_syslog(script_filename=self.__script_filename,
                                     script_directory=self.__script_directory,
                                     script_output=self.__script_output)

    @property
    def check_if_syslog_script_exists_command(self) -> str:
        """Returns linux command, that searches for syslog script"""
        return commands.check_if_syslog_script_exists(script_filename=self.__script_filename,
                                                      script_directory=self.__script_directory)

    @property
    def change_syslog_filename_command(self) -> str:
        """Returns Linux command, that adds date to syslog filename"""
        return commands.change_syslog_filename(log_filename=self._log_filename,
                                               log_directory=self._log_directory,
                                               script_filename=self.__script_filename,
                                               script_directory=self.__script_directory)

    @property
    def give_permisions_to_syslog_script_command(self) -> str:
        """Returns Linux command, that add permision to syslog script on vm"""
        return commands.give_permissions_to_syslog_script(script_filename=self.__script_filename,
                                                          script_directory=self.__script_directory)
    
    @property
    def clear_syslog_ports_command(self) -> str:
        """Returns Linux command, that kill all used syslog ports"""
        return commands.clear_syslog_ports(port=hashdata.SYSLOG_PORT)
