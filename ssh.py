"""
Class: Ssh
Author: Kamil Koltowski
Date: 2022-04-06
Description: This class represents a template for any SSH related class, and share common methods and attributes.
"""
from abc import ABC
import paramiko
import os
import commands
import datetime
import time
import exceptions
import hashdata
from backlog import backlog
from gui import gui


class Ssh(ABC):
    def __init__(self, hostname, username, password, description, jump_hostname=None):
        self._hostname: str = hostname
        self._username: str = username
        self._password: str = password
        self._description: str = description
        self._port: int = 22
        self._jump_hostname: str = jump_hostname
        self._is_connected: bool = False
        self._default_dir: str = None
        self._ssh_client: paramiko.SSHClient = None
        self._ssh_info: dict = {}
        self._ssh_time: float = 0
        self._ssh_stopwatch: datetime = None
        self._sftp_client: paramiko.SSHClient = None
        self._stdin: str = None
        self._stdout: str = None
        self._stderr: str = None
        self._tool_directory: str = hashdata.NLR_PATH
        self._user_desktop_directory: str = hashdata.USER_DESKTOP_DIRECTORY
        self._logs_pid_database: list = []

    @property
    def stdin(self) -> str:
        """Return ssh client input"""
        return self._stdin.read().decode('utf-8')

    @property
    def stdout(self) -> str:
        """Return ssh client output"""
        return self._stdout.read().decode('utf-8')

    @property
    def stderr(self) -> str:
        """Return ssh client error"""
        return self._stderr.read().decode('utf-8')

    @property
    def hostname(self) -> str:
        """Return hostname of ssh client"""
        return self._hostname

    @property
    def description(self) -> str:
        """Return description of ssh client"""
        return self._description

    @property
    def is_connected(self) -> bool:
        """Return connection status of ssh client"""
        return self._is_connected

    @is_connected.setter
    def is_connected(self, state: bool):
        self._is_connected = state

    @property
    def ssh_info(self) -> dict:
        """Return info about ssh client"""
        self._ssh_info = {
            "ssh_client": self._ssh_client,
            "hostname": self._hostname,
            "username": self._username,
            "password": self._password,
            "port": self._port,
            "description": self._description,
            "jump_hostname": self._jump_hostname,
            "is_connected": self._is_connected,
            "session_time": self._ssh_time}
        return self._ssh_info

    def _send_command(self, command: str):
        """Send and execute remote Linux command"""
        try:
            self._stdin, self._stdout, self._stderr = self._ssh_client.exec_command(command)
        except Exception as e:
            self._fail_message(error=e, method=self._send_command, arg=command, no_gui_flag=True)

    def _start_session_stopwatch(self):
        """Start ssh session stopwatch"""
        self._ssh_stopwatch = datetime.datetime.now()

    def _update_current_session_time(self):
        """Measures ssh session time"""
        self._ssh_time = round((datetime.datetime.now() - self._ssh_stopwatch).total_seconds(), 2)

    def __connect_to_remote(self):
        """Establish Ssh connection"""
        try:
            self._ssh_client = paramiko.SSHClient()
            self._ssh_client.load_system_host_keys()
            self._ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self._ssh_client.connect(hostname=self._hostname, port=self._port,
                                     username=self._username, password=self._password)
        except Exception as e:
            self._fail_message(method=self.__connect_to_remote, error=e, no_gui_flag=True)
        else:
            self._pass_message(method=self.__connect_to_remote, no_gui_flag=True)

    def start_session(self):
        """Start ssh session"""
        try:
            self.__connect_to_remote()
            if self._ssh_client.get_transport().is_active():
                self.is_connected = True
                self._start_session_stopwatch()
                self.check_if_nlr_dir_exists_on_remote()
        except Exception as e:
            self._fail_message(method=self.start_session, error=e, arg="Connection failed")
        else:
            self._pass_message(method=self.start_session, arg="Connected")
            self.gui_display_vm_status()

    def stop_session(self):
        """Close ssh session"""
        try:
            self._ssh_client.close()
            self.is_connected = False
        except Exception as e:
            self._fail_message(method=self.stop_session, error=e)
        else:
            self._pass_message(method=self.stop_session)

    def check_if_nlr_dir_exists_on_remote(self):
        try:
            sftp_client = self._create_sftp_session()
            sftp_client.stat(path=self._default_dir)
        except IOError as e:
            command = commands.create_remote_nlr_directory(path=self._default_dir)
            self._send_command(command=command)

    def _create_sftp_session(self):
        try:
            self._sftp_client = self._ssh_client.open_sftp()
            self._sftp_client.window_size = 2147483647  # 3 * 1024 * 1024
            self._sftp_client.REKEY_BYTES = pow(2, 40)
        except Exception as e:
            self._fail_message(method=self._create_sftp_session, error=e)
        else:
            self._pass_message(method=self._create_sftp_session)
            return self._sftp_client

    def _close_sftp_session(self):
        try:
            self._sftp_client.close()
        except Exception as e:
            self._fail_message(method=self._close_sftp_session, error=e)
        else:
            self._pass_message(method=self._close_sftp_session)

    def _start_logging(self, log: 'Log', snapshot: bool = False, errlog: bool = False, syslog: bool = False,
                       syslog_client: paramiko.SSHClient = None):
        """ This method executes all instructions necessary for: starting log, tracking log collection, assigning info
        :param log: log object
        :param snapshot: snapshot flag, set to True if snapshot is collected
        :param errlog: errlog flag, set to True if errlog is collected
        :param syslog: syslog flag, set to True if syslog is collected
        :param syslog_client: syslog ssh client object, mandatory when syslog is collected
        """
        try:
            '''Assign new log name with vm description and current date'''
            description = self.description.replace(hashdata.SYSMODULE_ID_,
                                                   "") if hashdata.SYSMODULE_ID_ in self.description else self.description
            date = datetime.datetime.now().strftime("_%Y%m%d_%H%M%S")
            log.set_log_filename(vm_description=description, date=date)

            if syslog:
                '''Check if script can be found, else raise exception'''
                command = log.check_if_syslog_script_exists_command
                self._send_command(command)
                output = self.stdout.replace('\n', "")

                if output != f"{log.log_directory}{log.script_filename}":
                    raise exceptions.SyslogScriptError

                '''Add permissions to script'''
                command = log.give_permisions_to_syslog_script_command
                self._send_command(command)

                '''Set log name in script'''
                command = log.change_syslog_filename_command
                self._send_command(command)

                '''Clear syslog ports'''
                command = log.clear_syslog_ports_command
                self._send_command(command)

                '''Execute start log command'''
                command = log.start_log_command
                stdin, stdout, stderr = syslog_client.exec_command(command)

                time.sleep(1)

            if snapshot:
                command = log.create_snapshot_script_command
                self._send_command(command=command)

            '''Execute start log command, wait 1 second for establishment (syslog is executed with own ssh client).'''
            if not syslog:
                command = log.start_log_command
                self._send_command(command=command)
                time.sleep(1)

            '''Wait for errlog script establishment - sleep for 4 seconds is necessary for log establishment'''
            if errlog:
                time.sleep(4)
                command = log.errlog_output
                self._send_command(command=command)
                output = self.stdout

                '''If error occurres when errlog starts, raise exception'''
                if log.errlog_fail_message_when_started in output:
                    raise exceptions.ErrlogHwError

                log.cache_filename()

            '''Get and Set log PID'''
            self._update_log_pid(log=log)

            if log.log_pid is None:
                raise exceptions.LogPidError

            '''If all above passed, set logging status and start stopwatch'''
            log.is_logging = True
            log.start_log_stopwatch()
        except Exception as e:
            self._fail_message(method=self._start_logging, error=e, arg=f"{log.log_filename}, error: {e}")
        else:
            self._pass_message(method=self._start_logging, arg=f"{log.log_filename} started, PID: {log.log_pid}")

    def _stop_logging(self, log: 'Log', errlog: bool = False):
        """ This method executes all instructions needed for: stopping log, clearing and updating log info
        :param log: Log object
        :param errlog: Errlog flag
        """
        try:
            '''Execute stop log command'''
            command = log.stop_log_command
            self._send_command(command=command)

            if errlog:
                log.uncache_filename()
                command = log.change_errlog_file_command
                self._send_command(command=command)

            '''Set logging status to False'''
            log.is_logging = False

            '''Update log size'''
            self._update_log_size(log=log)

            '''Remove PID from logs PID database'''
            self._logs_pid_database = [pid for pid in self._logs_pid_database if pid != log.log_pid]
        except Exception as e:
            self._fail_message(method=self._stop_logging, error=e, arg=f"{log.log_filename}, PID: {log.log_pid}")
        else:
            self._pass_message(method=self._stop_logging, arg=f"{log.log_filename} stopped, PID: {log.log_pid}")
        finally:
            '''Reset PID'''
            log.log_pid = None
            self.gui_display_logs_info()

    def _stop_logs_on_exit(self, *logs):
        for log in logs:
            self._stop_logging(log=log)

    def _update_log_pid(self, log: 'Log'):
        """Read and set PID of provided log object"""
        command = log.log_pid_command
        try:
            '''Get output PID'''
            self._send_command(command=command)
            pid = self.stdout.replace('\n', "")

            '''If output isn't empty - then proceed (PID exists), else - raise exception (PID doesn't exist)'''
            if pid == "":
                return

            '''Append PID to logs PID database'''
            self._logs_pid_database.append(pid)

            '''Assign PID to log'''
            log.log_pid = pid
        except Exception as e:
            self._fail_message(method=self._update_log_pid, error=e, arg=log.log_filename)

    def _update_log_size(self, log: 'Log'):
        """Read and set size of provided log"""
        command = log.log_size_command
        try:
            self._send_command(command=command)
            log_size = self.stdout.partition('/')[0]
            log.log_size = log_size
        except Exception as e:
            self._fail_message(method=self._update_log_size, error=e, arg=log.log_filename)

    def _download_log_from_sysmodule_on_vm(self, log: 'Log'):
        """Download log on VM from Sys-module"""
        try:
            '''If provided log doesn't exists, raises exception'''
            if log.log_size == "" or log.log_size is None:
                raise exceptions.LogSizeError

            scp_command = commands.download_log_from_sysmodule(password=hashdata.SYSMODULE_PASSWORD,
                                                               username=hashdata.SYSMODULE_USERNAME,
                                                               hostname=hashdata.SYSMODULE_HOSTNAME,
                                                               filename=log.log_filename,
                                                               directory=log.log_directory,
                                                               destination_directory=self._default_dir)
            self._send_command(scp_command)
        except Exception as e:
            self._fail_message(method=self._download_log_from_sysmodule_on_vm, error=e,
                               arg=f"{log.log_filename} downloading on VM failed")
        else:
            self._pass_message(method=self._download_log_from_sysmodule_on_vm,
                               arg=f"{log.log_filename} downloaded on VM")

    def _upload_file_on_vm(self, filename: str):
        """Upload given filename on VM from user's PC """
        vm_log_directory = self._default_dir + filename
        userpc_log_directory = self._tool_directory + filename

        try:
            self._create_sftp_session()
            self._sftp_client.put(userpc_log_directory, vm_log_directory)
            self._close_sftp_session()
        except Exception as e:
            self._fail_message(method=self._upload_file_on_vm, error=e, arg=f"{filename} uploading on VM failed")
        else:
            self._pass_message(method=self._upload_file_on_vm, arg=f"{filename} uploaded on VM")

    def _upload_file_on_sysmodule(self, filename):
        """Upload given file from VM on Sys-module"""
        try:
            scp_command = commands.upload_file_on_sysmodule(password=hashdata.SYSMODULE_PASSWORD,
                                                            username=hashdata.SYSMODULE_USERNAME,
                                                            hostname=hashdata.SYSMODULE_HOSTNAME,
                                                            destination_directory=hashdata.SYSMODULE_DEFAULT_DIR,
                                                            filename=filename,
                                                            directory=hashdata.VM_DEFAULT_DIR)
            self._send_command(scp_command)
        except Exception as e:
            self._fail_message(method=self._upload_file_on_sysmodule, error=e,
                               arg=f"{filename} uploading on {hashdata.SYSMODULE_ID} failed")
        else:
            self._pass_message(method=self._upload_file_on_sysmodule,
                               arg=f"{filename} uploaded on {hashdata.SYSMODULE_ID}")

    @backlog
    def _pass_message(self, method: __name__, arg: str = None, no_gui_flag: bool = False) -> str:
        """ This method is called, when the other method has been executed successfully, it also displays text on GUI
        :param method: Method reference, used for getting method name
        :param arg: Arg is a message that is sent, to be displayed on GUI, and to be saved in backlog
        :param no_gui_flag: Is set to True, if message is saved to backlog, but not displayed in gui
        """
        if arg is not None and no_gui_flag is not True:
            self.gui_display_text_on_console(message=arg)
        message = f"Description: {self._description}\nMethod: {method.__name__}\nResult: PASS\nArgument: {arg}\n"
        return message

    @backlog
    def _fail_message(self, method: __name__, error: Exception, arg: str = None, no_gui_flag: bool = False) -> str:
        """ This method is called, when the other method has failed at some point, and exception has been raised,
        it also displays text on GUI
        :param method: Method reference, used for getting method name
        :param error: Error that has been raised in Exception block
        :param arg: Arg is a message that is sent, to be displayed on GUI, and to be saved in backlog
        """
        if arg is not None and no_gui_flag is not True:
            self.gui_display_text_on_console(message=arg)
        message = f"Description: {self._description}\nMethod: {method.__name__}\nResult: FAIL\nArgument: {arg}\nError: {error}\n"
        return message

    def gui_display_text_on_console(self, message: str):
        """Display given message, on a GUI console - Called only in pass/fail_message methods"""
        gui.display_text(message=f"{self._description}:\n{message}.")

    def gui_display_vm_status(self):
        """Display Vm status, on a GUI widgets"""
        gui.display_vm_status()

    def gui_display_logs_info(self):
        """Display logs info on a GUI widgets"""
        gui.get_logs_page().set_logs_info()

    def thread_is_session_active(self):
        """Check if ssh session is active - update session time, if not - then change status. (runs in background)"""
        try:
            while True:
                if not self._ssh_client.get_transport().is_active():
                    break
                self._update_current_session_time()
                time.sleep(1)
        except Exception as e:
            self._fail_message(method=self.thread_is_session_active, error=e, arg=f"Disconnected")
        else:
            self._pass_message(method=self.thread_is_session_active, arg=f"Disconnected")
        finally:
            self.stop_session()
            self.is_connected = False
            '''Update GUI'''  # don't touch it
            self.gui_display_vm_status()

    def thread_is_pid_alive(self, log: 'Log', errlog: bool = False):
        """ Thread runs when log is being collected. It checks if PID of a log is still alive,
        if so then it updates log size and logging time. It updates also GUI log info.
        :param log: Log object
        :param errlog: Errlog flag, set to True if errlog is collected
        """
        command = commands.get_is_pid_alive(pid=log.log_pid)

        try:
            if log.is_logging:
                while True:
                    '''Get output of PID'''
                    self._send_command(command=command)
                    output = self.stdout.replace("\n", "")

                    '''If logging status is False and PID not found - method stop_logging() was executed by user'''
                    '''elif output doesn't equal to PID, and logging status is True - remote interrupt'''
                    if output != log.log_pid and log.is_logging is False:
                        break
                    elif output != log.log_pid and log.is_logging is not False:
                        self._stop_logging(log=log, errlog=errlog)
                        force_kill = log.force_kill_command
                        self._send_command(force_kill)
                        raise exceptions.LogInterrupt(log=log.log_filename)

                    log.update_logging_time()
                    self._update_log_size(log=log)

                    '''Update GUI - logs info in real time'''
                    self.gui_display_logs_info()
                    time.sleep(1)
        except exceptions.LogInterrupt as e:
            self._fail_message(method=self.thread_is_pid_alive, error=e, arg=f"{log.log_filename} interrupted")
        except Exception as e:
            self._fail_message(method=self.thread_is_pid_alive, error=e, arg=f"{log.log_filename} failed",
                               no_gui_flag=True)
        else:
            self._pass_message(method=self.thread_is_pid_alive, arg=log.log_filename, no_gui_flag=True)

    # TODO: These methods will be fixed and released in further version
    def thread_download_log_from_vm_on_pc(self, log: 'Log'):
        """ Thread runs when log is about to be downloaded, running in thread is necessary to keep tool not freezed.
        :param log: Log object
        Issue: The problem with paramiko lib is that, the SFTP transfer is so slow - about 0.2 MB/s. workaround needed!
        """
        vm_log_directory = str(self._default_dir + log.log_filename)
        userpc_log_directory = str(self._user_desktop_directory + log.log_filename)

        sftp_client = self._create_sftp_session()

        try:
            if sftp_client is None:
                raise Exception
            if log.log_size == "":
                raise exceptions.LogSizeError

            log.is_downloading = True
            sftp_client.get(remotepath=vm_log_directory, localpath=userpc_log_directory)
        except Exception as e:
            self._fail_message(method=self._download_log_from_vm_on_pc, error=e,
                               arg=f"{log.log_filename} downloading on PC failed")
        else:
            self._pass_message(method=self._download_log_from_vm_on_pc, arg=f"{log.log_filename} downloaded on PC")
        finally:
            sftp_client.close()
            log.is_downloading = False

    def thread_calculate_downloading_time_of_a_log(self, log: 'Log'):
        """ Calculate downloading time, downloading speed, download progress in %, and size left
        :param log: Log object
        """
        log_size = log.log_size
        userpc_log_directory = str(self._user_desktop_directory + log.log_filename)

        try:
            if log_size == "":
                raise exceptions.LogSizeError
            '''Remove size character from size, and convert it to MB'''
            if 'K' in log_size:
                log_size = int(log_size.replace('K', '')) / 1000  # divide by 10^3 so it's MB
            elif 'M' in log_size:
                log_size = int(log_size.replace('M', ''))  # already in MB
            else:
                raise exceptions.LogSizeError

            size_cached = 0
            while True:
                time.sleep(2)

                if log.is_logging:
                    break

                size_downloaded = round(os.path.getsize(filename=userpc_log_directory) / 1000000,
                                        3)  # divide by 10^6 so it's MB
                size_left = round(log_size - size_downloaded, 3)
                download_speed = round(size_downloaded - size_cached, 3)
                time_left = round(size_left / download_speed, 3)
                progress = round((size_downloaded / log_size) * 100, 3)
                size_cached = size_downloaded

                if time_left < 0:
                    time_left = 0

                if progress > 100:
                    progress = 100

                print("log_size [MB]: ", log_size)
                print("size_downloaded [MB]: ", size_downloaded)
                print("size_left [MB]: ", size_left)
                print("download_speed [MB/sec]: ", download_speed)
                print("download_time [s]: ", time_left)
                print("progress [%]: ", progress)

                if size_downloaded >= log_size:
                    break
        except Exception as e:
            self._fail_message(method=self.thread_calculate_downloading_time_of_a_log, error=e,
                               arg=log.log_filename)
        else:
            self._pass_message(method=self.thread_calculate_downloading_time_of_a_log,
                               arg=log.log_filename,
                               no_gui_flag=True)

    # Not used
    def _download_log_from_vm_on_pc(self, log: 'Log'):
        """Download provided log on PC from VM"""
        vm_log_directory = str(self._default_dir + log.log_filename)
        userpc_log_directory = str(self._user_desktop_directory + log.log_filename)

        try:
            if log.log_size == "" or log.log_size is None:
                raise exceptions.LogSizeError
            self._create_sftp_session()
            self._sftp_client.get(remotepath=vm_log_directory, localpath=userpc_log_directory)
            self._close_sftp_session()
        except Exception as e:
            self._fail_message(method=self._download_log_from_vm_on_pc, error=e,
                               arg=f"{log.log_filename} downloading on PC failed")
        else:
            self._pass_message(method=self._download_log_from_vm_on_pc, arg=f"{log.log_filename} downloaded on PC")
