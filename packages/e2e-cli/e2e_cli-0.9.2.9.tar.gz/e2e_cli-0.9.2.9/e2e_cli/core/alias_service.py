import json
import os
import platform

from e2e_cli.core.py_manager import Py_version_manager

class AliasServices:
    def __init__(self, alias):
        self.alias = alias

    def get_api_credentials(self):
        file= os.path.expanduser("~") + '/.E2E_CLI/config.json'
        file_reference = open(file, "r")
        config_file_object = json.loads(file_reference.read())
        if self.alias in config_file_object:
            return {"api_credentials": config_file_object[self.alias],
                    "message": "Valid alias"}
        else:
            return {"message": "Invalid alias provided"}

def system_file():
    if platform.system() == "Windows":  
                return os.path.expanduser("~") + '\.E2E_CLI\config.json'
    elif platform.system() == "Linux" or platform.system() == "Mac":  
                return os.path.expanduser("~") + '/.E2E_CLI/config.json'


def get_user_cred(name, x=0):
    
    file= system_file()

    # Opening JSON file
    f = open(file)
    
    # returns JSON object as 
    # a dictionary
    data = json.load(f)

    if(name=="all" and x==1):
            return data.keys()
    
    # Closing file
    f.close()

    if(name in data):
        return[ data[name]['api_auth_token'], data[name]['api_key'] ]
    else:
        Py_version_manager.py_print("the given alias/credential doesn't exist")
        return None


def check_user_cred(name):
        
    file= system_file()

    # Opening JSON file
    f = open(file)
    
    # returns JSON object as 
    # a dictionary
    data = json.load(f)
    
    # Closing file
    f.close()

    if(name in data):
        return[ data[name]['api_auth_token'], data[name]['api_key'] ]
    else:
        return None
