import json
import os
import platform

from e2e_cli.core.py_manager import Py_version_manager
from e2e_cli.core.alias_service import check_user_cred
from e2e_cli.config.config_service import is_valid

class AuthConfig:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.home_directory = os.path.expanduser("~")
        if platform.system() == "Windows":
            self.folder= self.home_directory + "\.E2E_CLI"
            self.file= self.home_directory + "\.E2E_CLI\config.json"
        elif platform.system() == "Linux" or platform.system() == "Mac":
            self.folder= self.home_directory + "/.E2E_CLI"
            self.file= self.home_directory + "/.E2E_CLI/config.json"

    def windows_hider(self):
        os.system("attrib +h " + self.folder)
        
    def windows_file_check(self):
        if not os.path.isdir(self.folder):
            return -1
        elif not os.path.isfile(self.file):
            self.windows_hider()
            return 0
        else:
            self.windows_hider()
            return 1

    def linux_mac_file_check(self):
        if not os.path.isdir(self.folder):
            return -1
        elif not os.path.isfile(self.file):
            return 0
        else:
            return 1
        
    def check_if_file_exist(self):
        if platform.system() == "Windows":
            return self.windows_file_check()
        elif platform.system() == "Linux" or platform.system() == "Mac":
            return self.linux_mac_file_check()

    def add_json_to_file(self):
        api_access_credentials_object = {"api_key": self.kwargs["api_key"],
                                         "api_auth_token": self.kwargs["api_auth_token"]}
        if(is_valid(api_access_credentials_object["api_key"], api_access_credentials_object["api_auth_token"])):
            with open(self.file, 'r+') as file_reference:
                read_string = file_reference.read()
                if read_string == "":
                    file_reference.write(json.dumps({self.kwargs["alias"]:
                                                        api_access_credentials_object}))
                else:
                    api_access_credentials = json.loads(read_string)
                    api_access_credentials.update({self.kwargs["alias"]:
                                                    api_access_credentials_object})
                    file_reference.seek(0)
                    file_reference.write(json.dumps(api_access_credentials))
            Py_version_manager.py_print()
            Py_version_manager.py_print("Alias/user_name/Token name successfully added")
        else:
            Py_version_manager.py_print()
            Py_version_manager.py_print("Invalid credentials given please enter correct Api key and Authorisation")
            return

    def add_to_config(self):
        file_exist_check_variable = self.check_if_file_exist()
        if file_exist_check_variable == -1:
            os.mkdir(self.folder)
            with open(self.file, 'w'):
                pass
            self.add_json_to_file()
        elif file_exist_check_variable == 0:
            with open(self.file, 'w'):
                pass
            self.add_json_to_file()
        elif file_exist_check_variable == 1:
            if (check_user_cred(self.kwargs['alias'])):
                Py_version_manager.py_print("The given alias/username already exist!! Please use another name or delete the previous one")
            else:
                self.add_json_to_file()

    def delete_from_config(self):
        file_exist_check_variable = self.check_if_file_exist()
        if file_exist_check_variable == -1 | file_exist_check_variable == 0:
            Py_version_manager.py_print("You need to add your api access credentials using the add functionality ")
            Py_version_manager.py_print("To know more please write e2e_cli config add -h on your terminal")

        elif file_exist_check_variable == 1:
            with open(self.file, 'r+') as file_reference:
                file_contents_object = json.loads(file_reference.read())
                delete_output = file_contents_object.pop(self.kwargs["alias"], 'No key found')
                if delete_output == "No key found":
                    Py_version_manager.py_print()
                    Py_version_manager.py_print("No such alias found. Please re-check and enter again")
                else:
                    file_reference.seek(0)
                    file_reference.write(json.dumps(file_contents_object))
                    file_reference.truncate()
                    Py_version_manager.py_print()
                    Py_version_manager.py_print("Alias/name Successfully deteted")
