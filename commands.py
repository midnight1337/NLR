"""
Author: Kamil Koltowski
Date: 2022-04-11
Description: This file provides a list of all Linux commands, that are executed remotely (mainly for log collection).
"""


def create_remote_nlr_directory(path: str):
    return f'mkdir {path}'


def login_to_remote(hostname: str, username: str, password: str) -> str:
    return f'sshpass -p "{password}" {username}@{hostname}'


def download_file_from_remote(username: str, hostname: str, password: str, directory: str, filename: str) -> str:
    return f'sshpass -p "{password}" scp {username}@{hostname}:{directory}{filename} .'


def download_log_from_sysmodule(password: str, username: str, hostname: str, filename: str, directory: str, destination_directory) -> str:
    return f'sshpass -p "{password}" scp {username}@{hostname}:{directory}{filename} {destination_directory}'


def upload_file_on_sysmodule(password: str, username: str, hostname: str, destination_directory: str, filename: str, directory: str) -> str:
    return f'sshpass -p "{password}" scp {directory}{filename} {username}@{hostname}:{destination_directory}'


def get_size_of_log(filename: str, directory: str) -> str:
    return f"du -sh {directory}{filename}"


def get_pid(pid_name: str) -> str:
    return f"ps --sort=start_time -ef | grep {pid_name} | tac | tail -n +3 | head -n 1 | tr -s ' ' | cut -d ' ' -f 2"


def get_is_pid_alive(pid: str) -> str:
    return f"ps -p {pid} | tail -n 1 | awk '{{print $1;}}'"


def kill_pid(pid: str) -> str:
    return f"kill -9 {pid}"


def start_tcpdump(filename: str, directory: str) -> str:
    return f"nohup tcpdump -i any sctp -w {directory}{filename} &"


def start_snapshot(script_filename: str, script_directory: str) -> str:
    return f'{script_directory}{script_filename}'


def create_snapshot_script(log_filename: str, script_filename: str, script_directory: str, script_output: str,
                           telnet_ip: str, telnet_port: str) -> str:
    shebang = "#!/bin/bash"
    command = f'(echo log -a -z {log_filename}; sleep 300) | telnet {telnet_ip} {telnet_port} | tee {script_output} >/dev/null'
    return f'killall telnet\n' \
           f'echo -e "{shebang}\n{command}" > {script_directory}{script_filename}\nchmod +x {script_directory}{script_filename}'


def read_last_snapshot_message(script_output: str) -> str:
    return f"cat {script_output} | tail -n 2 | head -n 1"


def start_syslog(script_filename: str, script_directory: str, script_output: str) -> str:
    return f"nohup {script_directory}{script_filename} > {script_directory}{script_output} &"


def force_kill(filename: str) -> str:
    return f"killall {filename}"


def check_if_syslog_script_exists(script_filename: str, script_directory: str) -> str:
    return f"ls {script_directory}{script_filename}"


def give_permissions_to_syslog_script(script_filename: str, script_directory: str) -> str:
    return f"chmod 711 {script_directory}{script_filename}"


def clear_syslog_ports(port: str) -> str:
    return f"netstat -lnp | grep -E '{port}' | awk '{{print $6}}' | tail -n+2 | cut -d / -f 1 | xargs kill -9 $6"
    

def search_for_syslog_name(script_output: str) -> str:
    return f"cat {script_output} | head -n 1 | cut -d ' ' -f 4"


def change_syslog_filename(log_filename: str, log_directory: str, script_filename: str, script_directory: str) -> str:
    return rf"""sed -i '/my $log_file =/c\my $log_file = "{log_directory}{log_filename}";' {script_directory}{script_filename}"""


def move_syslog_from_tmp_dir_to_home_dir(log_directory: str, log_filename: str, home_directory: str) -> str:
    return f"mv {log_directory}{log_filename} {home_directory}"


def start_errlog(script_filename: str, script_directory: str, script_output: str) -> str:
    return f"nohup sh {script_directory}{script_filename} | tee {script_directory}{script_output} &"


def search_for_errlog_environment(script_filename: str, script_cfg_filename: str, script_directory: str) -> str:
    return f"ls {script_directory}{script_filename}; ls {script_directory}{script_cfg_filename}"


def create_errlog_environment(default_directory: str, script_filename: str, script_cfg_filename: str, script_directory: str) -> str:
    return f"mkdir {script_directory}; cp {default_directory}{script_filename} {default_directory}{script_cfg_filename} {script_directory}; " \
           f"chmod 711 {script_directory}{script_filename}; chmod 711 {script_directory}{script_cfg_filename} "


def change_errlog_filename(old_filename: str, new_filename: str, directory: str) -> str:
    return f"mv {directory}{old_filename} {directory}{new_filename}"


def read_errlog_output(script_output: str, script_directory: str) -> str:
    return f"cat {script_directory}{script_output}"
