"""
Class: Tcpdump
Author: Kamil Koltowski
Description: This class represents a tcpdump log.
"""
from log import Log
import commands


class Tcpdump(Log):
    def __init__(self):
        super().__init__()
        self._log_identifier: str = "TCPDUMP"
        self._log_format: str = ".pcap"
        self._log_pid_identifier: str = "tcpdump"

    @property
    def start_log_command(self) -> str:
        """Returns linux command, that starts tcpdump log"""
        return commands.start_tcpdump(filename=self._log_filename, directory=self._log_directory)
