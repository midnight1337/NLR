"""
Class: Log
Author: Kamil Koltowski
Date: 2022-04-26
Description: This class represents a template for any log related class and provides common methods for them.
"""
from abc import ABC, abstractmethod
import commands
import datetime


class Log(ABC):
    def __init__(self):
        self._log_identifier: str = "default_log_identifier"
        self._log_filename: str = None
        self._log_format: str = "default_log_format"
        self._log_directory: str = "/tmp/"
        self._log_pid_identifier: str = "default_log_pid_identifier"
        self._log_pid: str = None
        self._log_size: str = None
        self._is_logging: bool = False
        self._is_downloading: bool = False
        self._logging_time: float = 0
        self._log_stopwatch: datetime = None
        self._log_info: dict = {}

    @property
    def log_filename(self) -> str:
        return self._log_filename

    @log_filename.setter
    def log_filename(self, filename):
        self._log_filename = filename

    @property
    def log_identifier(self) -> str:
        return self._log_identifier

    @property
    def log_size(self) -> str:
        return self._log_size

    @log_size.setter
    def log_size(self, size: str):
        self._log_size = size

    @property
    def log_pid(self) -> str:
        return self._log_pid

    @log_pid.setter
    def log_pid(self, pid):
        self._log_pid = pid

    @property
    def is_logging(self) -> bool:
        return self._is_logging

    @is_logging.setter
    def is_logging(self, status: bool):
        self._is_logging = status

    @property
    def is_downloading(self) -> bool:
        return self._is_downloading

    @is_downloading.setter
    def is_downloading(self, state: bool):
        self._is_downloading = state

    @property
    def log_directory(self) -> str:
        return self._log_directory

    @property
    def logging_time(self) -> float:
        return self._logging_time

    @property
    def log_info(self) -> dict:
        self._log_info = {
            "log file": self._log_filename,
            "log directory": self._log_directory,
            "log size": self._log_size,
            "log pid": self._log_pid,
            "logging time": self._logging_time,
            "is logging": self._is_logging}
        return self._log_info

    @property
    @abstractmethod
    def start_log_command(self) -> str:
        """Returns linux command, that starts particular log. Overridden function in each Log related class"""

    @property
    def stop_log_command(self) -> str:
        """Returns linux command, that stops log by given PID"""
        return commands.kill_pid(pid=self._log_pid)

    @property
    def force_kill_command(self) -> str:
        """Returns linux command, that basically does killall based on log filename"""
        return commands.force_kill(filename=self._log_filename)

    @property
    def log_pid_command(self) -> str:
        """Returns linux command, that gets log PID"""
        return commands.get_pid(pid_name=self._log_pid_identifier)

    @property
    def log_size_command(self) -> str:
        """Returns linux command, that gets log size"""
        return commands.get_size_of_log(filename=self._log_filename, directory=self._log_directory)

    def set_log_filename(self, vm_description: str, date: str):
        self._log_filename = vm_description + "_" + self._log_identifier + date + self._log_format

    def start_log_stopwatch(self):
        """Starts log stopwatch, when logging begins"""
        self._log_stopwatch = datetime.datetime.now()

    def update_logging_time(self):
        """Measure and update logging time"""
        self._logging_time = int(round((datetime.datetime.now() - self._log_stopwatch).total_seconds(), 0))
