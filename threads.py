"""
Class: Thread
Author: Kamil Koltowski
Date: 2022-11-06
Description: This class provides threads management, e.g. checks in background connection with remote.
"""
import threading
import time
from backlog import backlog
from notifier import Notifier


class Thread(object):
    def __init__(self):
        self.__Notifier = Notifier()
        self.__ssh_threads = []
        self.__log_threads = []
        self.__main_thread: threading.Thread = None
        self.__stop_main_thread: bool = False

    @property
    def ssh_threads(self) -> list:
        """Store all alive ssh related threads in one list"""
        return self.__ssh_threads

    @property
    def log_threads(self) -> list:
        """Store all alive log related threads in one list"""
        return self.__log_threads

    @backlog
    def __is_thread_alive(self):
        """Checks if threads in collections are alive, if not then pop them out and raise toast notify"""
        try:
            while True:
                if self.__stop_main_thread:
                    break

                for index, thread in enumerate(self.__ssh_threads):
                    if not thread.is_alive():
                        self.__ssh_threads.pop(index)
                        self.__Notifier.run_notify(message=f"{thread._name}: Disconnected.")

                for index, thread in enumerate(self.__log_threads):
                    if not thread.is_alive():
                        self.__log_threads.pop(index)

                time.sleep(1)
        except Exception as e:
            return e

    def stop_main_thread(self):
        """Kill all sub-threads"""
        self.__stop_main_thread = True
        self.__main_thread.join()

    def run_main_thread(self):
        """Run main thread, which loops through method: is_thread_alive(self)"""
        self.__main_thread = threading.Thread(target=self.__is_thread_alive, name="__is_thread_alive")
        self.__main_thread.start()

    def run_thread(self, thread: any, name: str = None, collection: list = None, log: any = None,
                   errlog: bool = False, download_log: bool = False):
        """Run passed method as thread, append thread to collection which is then used in method: is_thread_alive(self)
        :param thread: method passed to be run in thread
        :param collection: collection raw_database (ssh or logs)
        :param name: thread name
        :param log: log object
        :param errlog: errlog flag, used when errlog is logging
        :param download_log: download log flag, used when log is about to be downloaded on PC from VM
        arg collection is set of arguments that are passed to method when log starts (thread_is_pid_alive())
        arg: it is assigned to None when ssh thread is about to be run,
        arg: it is assigned to dict when log thread is run (log thread requires 3 arguments to be run).
        There are some methods that don't require any collection, so they are not checked by: is_thread_alive(self)
        """
        # arg = None if log is None else {'log': log, 'errlog': errlog}

        if log is None:
            arg = None
        elif log is not None and download_log:
            arg = {'log': log}
        else:
            arg = {'log': log, 'errlog': errlog}

        t = threading.Thread(target=thread, daemon=True, name=name, kwargs=arg)
        t.start()
        if collection is not None:
            collection.append(t)
