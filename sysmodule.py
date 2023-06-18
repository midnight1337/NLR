"""
Class: Sysmodule
Author: Kamil Koltowski
Date: 2022-04-26
Description: This class represents a Sysmodule.
"""
import time
import paramiko
import exceptions
import hashdata
from ssh import Ssh
from tcpdump import Tcpdump
from snapshot import Snapshot
from errlog import Errlog


class Sysmodule(Ssh):
    def __init__(self):
        super().__init__(hostname=hashdata.SYSMODULE_HOSTNAME, username=hashdata.SYSMODULE_USERNAME,
                         password=hashdata.SYSMODULE_PASSWORD, description="")
        self._default_dir: str = hashdata.SYSMODULE_DEFAULT_DIR
        self.__tcpdump: Tcpdump = Tcpdump()
        self.__snapshot: Snapshot = Snapshot()
        self.__errlog: Errlog = Errlog()
        self.__logs: list['Log'] = [self.__tcpdump, self.__snapshot, self.__errlog]

    @property
    def tcpdump(self) -> Tcpdump:
        """Return tcpdump object assigned to sysmodule"""
        return self.__tcpdump

    @property
    def snapshot(self) -> Snapshot:
        """Return snapshot object assigned to sysmodule"""
        return self.__snapshot

    @property
    def errlog(self) -> Errlog:
        """Return errlog object assigned to sysmodule"""
        return self.__errlog

    @property
    def logs(self) -> list['Log']:
        return self.__logs

    def __connect_to_sysmodule(self, vm_client, vm_hostname, vm_description):
        """Establish ssh connection with sysmodule via VM"""
        try:
            self._jump_hostname = vm_hostname
            self._description = hashdata.SYSMODULE_ID_ + vm_description

            target_address = (self._hostname, self._port)
            local_address = (self._jump_hostname, self._port)
            client_channel = vm_client.get_transport().open_channel("direct-tcpip", target_address, local_address)

            self._ssh_client = paramiko.SSHClient()
            self._ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self._ssh_client.connect(hostname=self._hostname, username=self._username,
                                     password=self._password, sock=client_channel, timeout=5)
        except Exception as e:
            self._fail_message(error=e, method=self.__connect_to_sysmodule)
        else:
            self._pass_message(method=self.__connect_to_sysmodule)

    def start_session(self, vm_client, vm_hostname, vm_description):
        """Start sysmodule session"""
        try:
            self.__connect_to_sysmodule(vm_client, vm_hostname, vm_description)
            if self._ssh_client.get_transport().is_active():
                self._is_connected = True
                self._start_session_stopwatch()
        except Exception as e:
            self._fail_message(method=self.start_session, error=e)
        else:
            self._pass_message(method=self.start_session, arg=f"Connected")
            self.gui_display_vm_status()

    def stop_session(self):
        """Stop all active logs and close sysmodule ssh session"""
        try:
            for log in [self.__tcpdump, self.__snapshot, self.__errlog]:
                if log.is_logging:
                    self._stop_logging(log=log)
            self._ssh_client.close()
        except Exception as e:
            self._fail_message(error=e, method=self.stop_session)
        else:
            self._pass_message(method=self.stop_session)

    def stop_logs_on_exit(self):
        self._stop_logs_on_exit(self.__tcpdump, self.__errlog)

    def start_tcpdump(self):
        """Start logging tcpdump"""
        self._start_logging(log=self.__tcpdump)

    def stop_tcpdump(self):
        """Stop logging tcpdump"""
        self._stop_logging(log=self.__tcpdump)

    def start_snapshot(self):
        """Start logging snapshot"""
        self._start_logging(log=self.__snapshot, snapshot=True)

    def thread_snapshot_verifier(self):
        """Method runs through snapshot output file and searches for specific snapshot verifier message,
         which means that log has been collected. (runs in background)"""
        try:
            time.sleep(3)
            time_counter = 0
            while True:
                if self.__snapshot.is_logging:
                    '''(1) This block purpose is to verify snapshot collection, by searching for a verifier message 
                    in snapshot output text file, which is generated when snapshot collection is going on.'''
                    self._send_command(command=self.__snapshot.read_last_snapshot_message)
                    output = self.stdout

                    # verifier_1 has been reported as latest verifier, verifier_2 hasn't shown from some time
                    # probably some changes in BTS Software caused different output
                    if self.__snapshot.snapshot_verifier_1 == output or self.__snapshot.snapshot_verifier_2 == output:
                        break

                    '''(2) This block purpose is to verify if snapshot isn't collecting anymore by checking log size.
                    If the size isn't changing, and verifier above hasn't handled output message, then log might be broken. (or not, it depends)'''
                    self._update_log_size(log=self.__snapshot)
                    old_size = self.__snapshot.log_size

                    time.sleep(1)

                    self._update_log_size(log=self.__snapshot)
                    new_size = self.__snapshot.log_size

                    if old_size == new_size:
                        time_counter += 1
                    else:
                        time_counter = 0

                    if time_counter > 20:
                        break
        except Exception as e:
            self._fail_message(error=e, method=self.thread_snapshot_verifier, arg=f"Snapshot failed")
        else:
            self._pass_message(method=self.thread_snapshot_verifier, arg=f"Snapshot collected")
        finally:
            self._stop_logging(log=self.__snapshot)

    def start_errlog(self):
        """Start errlog. If errlog env not found, raise ErrlogEnvironmentError, else start logging"""
        try:
            if not self.__check_if_errlog_environment_exists():
                raise exceptions.ErrlogEnvironmentError
            self._start_logging(log=self.__errlog, errlog=True)
        except exceptions.ErrlogEnvironmentError as e:
            self._fail_message(error=e, method=self.start_errlog, arg=f"{e}")
        else:
            self._pass_message(method=self.start_errlog)

    def stop_errlog(self):
        """Stop logging errlog"""
        self._stop_logging(log=self.__errlog, errlog=True)

    def create_errlog_environment(self):
        """Create errlog environment"""
        command = self.__errlog.create_errlog_environment_command
        self._send_command(command=command)

    def __check_if_errlog_environment_exists(self):
        """Check if errlog env/scripts exists"""
        command = self.__errlog.search_for_errlog_environment_command
        self._send_command(command=command)
        output = self.stdout
        if output != "":
            return True
