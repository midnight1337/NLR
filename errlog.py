"""
Class: Errlog
Author: Kamil Koltowski
Date: 2022-06-02
Description: This class represents a errlog.
"""
from log import Log
import commands
import hashdata


class Errlog(Log):
    def __init__(self):
        super().__init__()
        self._log_identifier: str = hashdata.ERRLOG_ID
        self._log_format: str = hashdata.ERRLOG_FORMAT
        self._log_pid_identifier: str = "tcpdump"
        self.__script_output: str = "errlog_output.txt"
        self.__cached_filename: str = ""

    @property
    def script_name(self) -> str:
        return hashdata.ERRLOG_SCRIPT_FILENAME

    @property
    def script_cfg_filename(self) -> str:
        return hashdata.ERRLOG_SCRIPT_CFG_FILENAME

    @property
    def errlog_output(self) -> str:
        """Returns command, that reads output from errlog"""
        return commands.read_errlog_output(script_output=self.__script_output,
                                           script_directory=hashdata.ERRLOG_SCRIPT_DIRECTORY)

    @property
    def errlog_fail_message_when_started(self) -> str:
        """Returns string, which appears when errlog fails to start"""
        return hashdata.ERRLOG_FAIL_MESSAGE_WHEN_STARTED

    @property
    def start_log_command(self) -> str:
        """Returns linux command, that starts errlog command"""
        return commands.start_errlog(script_filename=hashdata.ERRLOG_SCRIPT_FILENAME,
                                     script_directory=hashdata.ERRLOG_SCRIPT_DIRECTORY,
                                     script_output=self.__script_output)

    @property
    def create_errlog_environment_command(self) -> str:
        """Returns linux command, that creates errlog environment"""
        return commands.create_errlog_environment(default_directory=hashdata.SYSMODULE_DEFAULT_DIR,
                                                  script_filename=hashdata.ERRLOG_SCRIPT_FILENAME,
                                                  script_cfg_filename=hashdata.ERRLOG_SCRIPT_CFG_FILENAME,
                                                  script_directory=hashdata.ERRLOG_SCRIPT_DIRECTORY)

    @property
    def search_for_errlog_environment_command(self) -> str:
        """Returns Linux command, that checks if errlog env is created"""
        return commands.search_for_errlog_environment(script_filename=hashdata.ERRLOG_SCRIPT_FILENAME,
                                                      script_cfg_filename=hashdata.ERRLOG_SCRIPT_CFG_FILENAME,
                                                      script_directory=hashdata.ERRLOG_SCRIPT_DIRECTORY)

    @property
    def change_errlog_file_command(self) -> str:
        """Returns Linux command, that adds date to errlog filename"""
        return commands.change_errlog_filename(old_filename=hashdata.ERRLOG_ORG_FILENAME,
                                               new_filename=self._log_filename,
                                               directory=self._log_directory)

    def cache_filename(self):
        """Cache assigned filename"""
        self.__cached_filename = self._log_filename
        self.log_filename = hashdata.ERRLOG_ORG_FILENAME

    def uncache_filename(self):
        """Restore cached filename"""
        self._log_filename = self.__cached_filename
