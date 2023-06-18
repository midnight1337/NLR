"""
Author: Kamil Koltowski
Date: 2022-07-28
Description: This file contains exceptions, for better errors handling.
"""


class LogPidError(Exception):
    """Exception raised, when PID is unsuccessfully read"""
    def __init__(self):
        self.__message = "Failed to read log PID"
        super().__init__(self.__message)


class LogSizeError(Exception):
    """Exception raised, when log size can't be verified"""
    def __init__(self):
        self.__message = "Failed to read log size"
        super().__init__(self.__message)


class LogDownloadError(Exception):
    """Exception raised, when downloading log is interrupted by is_logging parameter in Log()"""
    def __init__(self):
        self.__message = "Downloading log failed"
        super().__init__(self.__message)


class ErrlogEnvironmentError(Exception):
    """Exception raised, when errlog scripts aren't found on remote."""
    def __init__(self):
        self.__message = "Failed to find errlog scripts"
        super().__init__(self.__message)


class ErrlogHwError(Exception):
    """Exception raised, when errlog script couldn't be executed because of HwError."""
    def __init__(self):
        self.__message = "Unknow controlCardHwType"
        super().__init__(self.__message)


class SyslogNotActiveError(Exception):
    """Exception raised, when syslog session isn't established."""
    def __init__(self):
        self.__message = "Failed to connect to syslog"
        super().__init__(self.__message)


class SyslogScriptError(Exception):
    """Exception raised, when syslog script can't be found on remote."""
    def __init__(self):
        self.__message = "Failed to find syslog script"
        super().__init__(self.__message)


class LogInterrupt(Exception):
    """Exception raised, when log was interrupted remotely"""
    def __init__(self, log):
        self.__message = f"{log} not found"
        super().__init__(self.__message)
