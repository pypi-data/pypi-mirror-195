from __future__ import print_function
import sys

class Py_version_manager:
    def __init__(self):
        pass

    @classmethod
    def py_input(self, msg):
        if(int(sys.version[0:1])<3):
                return raw_input(msg)
        else:
                return input(msg)
    
    @classmethod
    def py_print(self, *args):
        # if(int(sys.version[0:1])<3):
        #         print(*args, sep = " ")
        # else:
                print(*args, sep = " ")
                # return print(args)
        
