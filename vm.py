"""
Class: Vm
Author: Kamil Koltowski
Date: 2022-04-26
Description: This class represents a remote Virtual machine.
"""
import paramiko
import exceptions
from sysmodule import Sysmodule
from ssh import Ssh
from syslog import Syslog
import hashdata


class Vm(Ssh):
    def __init__(self, hostname, username, password, description):
        super().__init__(hostname=hostname, username=username,
                         password=password, description=description)
        self._default_dir: str = hashdata.VM_DEFAULT_DIR
        self.__sysmodule: Sysmodule = Sysmodule()
        self.__syslog: Syslog = Syslog()
        self.__logs: list['Log'] = [self.__syslog]
        self.__syslog_client: paramiko.SSHClient = None

    def __str__(self):
        return f"hostname: {self.hostname}, description: {self.description}"

    @property
    def sysmodule(self) -> Sysmodule:
        """Return Sys-module object assigned to Vm"""
        return self.__sysmodule

    @property
    def syslog(self) -> Syslog:
        """Return syslog object assigned to Vm"""
        return self.__syslog

    @property
    def logs(self) -> list['Log']:
        return self.__logs

    def connect_to_sysmodule(self):
        """Connect to Sysmodule and assign Vm client"""
        self.__sysmodule.start_session(vm_client=self._ssh_client,
                                       vm_hostname=self._hostname,
                                       vm_description=self._description)

    def connect_to_syslog(self):
        """Create syslog session"""
        try:
            self.__syslog_client = paramiko.SSHClient()
            self.__syslog_client.load_system_host_keys()
            self.__syslog_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.__syslog_client.connect(hostname=self._hostname,
                                         port=self._port,
                                         username=self._username,
                                         password=self._password)
        except Exception as e:
            self._fail_message(method=self.connect_to_syslog, error=e)
        else:
            self._pass_message(method=self.connect_to_syslog)

    def start_syslog(self):
        """Start syslog. It is necessary to create 2nd ssh session used only for syslog logging,
         running syslog script directly on a Vm ssh doesn't work good and makes that Vm acts strange"""
        try:
            """If syslog session is not active, connect to syslog"""
            if self.__syslog_client is None or not self.__syslog_client.get_transport().is_active():
                self.connect_to_syslog()

            if not self.__syslog_client.get_transport().is_active():
                raise exceptions.SyslogNotActiveError

            self._start_logging(log=self.__syslog, syslog=True, syslog_client=self.__syslog_client)
        except Exception as e:
            self._fail_message(method=self.start_syslog, error=e)
        else:
            self._pass_message(method=self.start_syslog)

    def stop_syslog(self):
        """Stop logging syslog"""
        self._stop_logging(log=self.__syslog)

    def stop_logs_on_exit(self):
        self._stop_logs_on_exit(self.__syslog)

    def download_tcpdump_from_sysmodule(self):
        """Download tcpdump"""
        self._download_log_from_sysmodule_on_vm(log=self.__sysmodule.tcpdump)

    def download_snapshot_from_sysmodule(self):
        """Download snapshot"""
        self._download_log_from_sysmodule_on_vm(log=self.__sysmodule.snapshot)

    def download_errlog_from_sysmodule(self):
        """Download errlog"""
        self._download_log_from_sysmodule_on_vm(log=self.__sysmodule.errlog)

    def upload_syslog_script(self):
        """Uploads syslog script on Vm"""
        self._upload_file_on_vm(filename=self.__syslog.script_name)

    def upload_errlog_scripts(self):
        """Upload errlog sripts, PC -> Vm -> Sys-module"""
        for script in [self.__sysmodule.errlog.script_name, self.__sysmodule.errlog.script_cfg_filename]:
            self._upload_file_on_vm(script)
            self._upload_file_on_sysmodule(script)
