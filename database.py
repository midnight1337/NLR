"""
Class: Database
Author: Kamil Koltowski
Date: 2022-07-28
Description: This class provides management for raw_database of the tool.
"""
import ast
import os.path
import hashdata
import re


class Database(object):
    def __init__(self):
        """This raw_database stores vm info only as dictionary, read from local_database.txt"""
        self.__raw_database: list[dict] = []
        """This initialised_database stores initialised VM objects only (objects are based on raw_database[])"""
        self.__initialised_database: list['Vm'] = []

    @property
    def raw_database(self) -> list:
        """Return local raw_database, which is basic vm info only: hostname, password, user, description)"""
        return self.__raw_database

    @property
    def raw_database_length(self) -> int:
        """Returns amount of VMs in raw_database"""
        return len(self.__raw_database)

    @property
    def initialised_database(self) -> list:
        """Return initialised VM objects raw_database"""
        return self.__initialised_database

    @property
    def initialised_database_length(self) -> int:
        return len(self.__initialised_database)

    def filter_description(self, description: str) -> str:
        """Filters description from all special characters, only simple characters are allowed"""
        pattern = r'[^a-zA-Z0-9]'
        replace_with = '_'
        filtered_description = re.sub(pattern, replace_with, description)
        return filtered_description

    def get_vm_info(self, index: int) -> dict:
        """Return info about chosen VM from raw_database"""
        ip = self.__raw_database[index]['hostname']
        username = self.__raw_database[index]['username']
        password = self.__raw_database[index]['password']
        description = self.__raw_database[index]['description']
        vm_info = {'ip': ip, 'username': username, 'password': password, 'description': description}
        return vm_info

    def get_converted_database_names(self) -> tuple:
        """Converts and returns name of VMs from raw_database, visible in GUI TLs list. Style: Description | hostname"""
        vms_converted_names = []
        for vm in self.__raw_database:
            name = vm['description'] + " | " + vm['hostname']
            vms_converted_names.append(name)
        vms_converted_names = tuple(vms_converted_names)
        return vms_converted_names

    def add_vm_to_database(self, hostname: str, username: str, password: str, description: str):
        """Add new VM to raw_database"""
        description = self.filter_description(description)

        new_vm = {
            'description': description,
            'hostname': hostname,
            'username': username,
            'password': password
        }
        self.__raw_database.append(new_vm)
        self.write_data_to_local_database_file()

    def add_vm_to_initialised_database(self, vm: 'Vm'):
        """Add VM object to initialised_database"""
        self.__initialised_database.append(vm)

    def edit_vm_in_database(self, index: int, hostname: str, username: str, password: str, description: str):
        """Edit data of selected VM"""
        description = self.filter_description(description)

        self.__raw_database[index]['hostname'] = hostname
        self.__raw_database[index]['username'] = username
        self.__raw_database[index]['password'] = password
        self.__raw_database[index]['description'] = description
        self.write_data_to_local_database_file()

    def edit_vm_in_initialised_database(self, index: int, vm: 'Vm'):
        """Edit (replace) existing VM object"""
        self.__initialised_database[index] = vm

    def remove_session_from_database(self, index: int):
        """Remove VM from raw_database and initialised_database, save changes in file"""
        self.__raw_database.pop(index)
        self.__initialised_database.pop(index)
        self.write_data_to_local_database_file()

    def move_vm(self, state: str, index: int):
        """Moves VM up or down in raw_database and initialised_database
        :param state: up or down
        :param index: index of chosen vm
        """
        if state == 'up':
            if not index > 0:
                return
            index_to_be_replaced = index - 1
        elif state == 'down':
            if not index < self.raw_database_length:
                return
            index_to_be_replaced = index + 1

        chosen_vm = self.__raw_database[index]
        chosen_vm_object = self.__initialised_database[index]
        vm_info_to_be_replaced = self.__raw_database[index_to_be_replaced]
        vm_object_to_be_replaced = self.__initialised_database[index_to_be_replaced]

        self.__raw_database[index_to_be_replaced] = chosen_vm
        self.__initialised_database[index_to_be_replaced] = chosen_vm_object
        self.__raw_database[index] = vm_info_to_be_replaced
        self.__initialised_database[index] = vm_object_to_be_replaced

        self.write_data_to_local_database_file()

    def setup_database(self):
        """Setup raw_database directly from database_file, if it doesn't exist yet -> read it from moba file"""
        if self.check_if_database_file_exists():
            self.read_data_from_database_file_and_add_it_to_raw_database()
        else:
            # return
            self.read_moba_sessions()
            self.write_data_to_local_database_file()

    def check_if_database_file_exists(self) -> bool:
        """Check if NLR dir exists, check if local_database.txt file exists, if so check if it's not empty"""
        if not os.path.isdir(hashdata.NLR_PATH):
            os.mkdir(hashdata.NLR_PATH)
        if os.path.exists(path=hashdata.DATABASE_FILE_PATH):
            if not os.stat(f"{hashdata.DATABASE_FILE_PATH}").st_size == 0:
                return True

    def read_data_from_database_file_and_add_it_to_raw_database(self):
        """Read data from database_file, cast it from str to dict, and append it to raw_database"""
        with open(f"{hashdata.DATABASE_FILE_PATH}", 'r') as database_file:
            for read_line in database_file.readlines():
                data = ast.literal_eval(read_line)  # removes "\n" from the end of line and converts str to dict
                self.__raw_database.append(data)
        database_file.close()

    def write_data_to_local_database_file(self):
        """Save data to database_file"""
        with open(f"{hashdata.DATABASE_FILE_PATH}", 'w') as database_file:
            for data in self.__raw_database:
                database_file.writelines(str(data) + '\n')
        database_file.close()

    def read_moba_sessions(self):
        """Read sessions from moba file, filter out all necessary parameters and append to session raw_database"""
        session_match_1: str = "ImgNum=41"
        session_match_2: str = "ImgNum=42"
        pc_match: str = "PC"
        sysmodule_match: str = hashdata.SYSMODULE_HOSTNAME

        '''Open moba raw_database file and read it, if not found then return no values'''
        try:
            moba_database = open(f"{hashdata.MOBA_DATABASE_FILE_PATH}", 'r').readlines()
        except Exception as e:
            return

        for index, read_line in enumerate(moba_database):
            """If defined match found in current line"""
            if session_match_1 in read_line or session_match_2 in read_line:
                """If next line is blank space, continue"""
                if moba_database[index + 1].isspace():
                    continue

                """Read tl_name and ip_addr by defined signs"""
                tl_name = moba_database[index + 1].partition("=")[0]
                ip_addr = moba_database[index + 1].split("%")[1]

                """If read parameters contains string below (PC name or Sysmodule IP), continue"""
                if pc_match in tl_name or sysmodule_match in ip_addr:
                    continue

                """If session not already in raw_database"""
                if tl_name not in self.__raw_database and ip_addr not in self.__raw_database:
                    tl_name = self.filter_description(tl_name)

                    self.__raw_database.append(
                        {
                            "description": tl_name,
                            "hostname": ip_addr,
                            "username": hashdata.VM_USERNAME,
                            "password": hashdata.VM_PASSWORD
                        }
                    )
