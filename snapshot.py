"""
Class: Snapshot
Author: Kamil Koltowski
Date: 2022-04-27
Description: This class represents a snapshot log.
"""
from log import Log
import commands
import hashdata


class Snapshot(Log):
    def __init__(self):
        super().__init__()
        self._log_identifier: str = "SNAPSHOT"
        self._log_format: str = ".zip"
        self._log_pid_identifier: str = "telnet"
        self.__script_filename: str = "snapshot_script.sh"
        self.__script_output: str = "snapshot_output.txt"
        self.__script_directory: str = "/tmp/"

    @property
    def snapshot_verifier_1(self) -> str:
        """Snapshot verifier - it returns string that should match with last message of snapshot output"""
        return hashdata.SNAPSHOT_VERIFIER_1

    @property
    def snapshot_verifier_2(self) -> str:
        return hashdata.SNAPSHOT_VERIFIER_2

    @property
    def start_log_command(self) -> str:
        """Returns linux command, that starts snapshot script"""
        return commands.start_snapshot(script_filename=self.__script_filename,
                                       script_directory=self._log_directory)

    @property
    def create_snapshot_script_command(self) -> str:
        """Returns linux command, that creates snapshot script"""
        return commands.create_snapshot_script(log_filename=self._log_filename,
                                               script_filename=self.__script_filename,
                                               script_directory=self.__script_directory,
                                               script_output=self.__script_output,
                                               telnet_ip=hashdata.SNAPSHOT_TELNET_IP,
                                               telnet_port=hashdata.SNAPSHOT_TELNET_PORT)

    @property
    def read_last_snapshot_message(self) -> str:
        """Returns linux command, that outputs last collected message"""
        return commands.read_last_snapshot_message(script_output=self.__script_output)
