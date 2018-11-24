"""Custom Logging Module."""

import os
from datetime import datetime
from .hive_data import Data


class Logger:
    """Custom Logging Code."""
    def __init__(self):
        """Logger Initialisation"""

    @staticmethod
    def check_logging(new_session):
        """Check Logging Active"""
        Data.l_o_folder = os.path.expanduser('~') + "/.homeassistant/pyhiveapi"
        Data.l_o_file = Data.l_o_folder + "/pyhiveapi.log"
        try:
            if new_session and os.path.isfile(Data.l_o_file):
                os.remove(Data.l_o_file)

            if os.path.isdir(Data.l_o_folder):
                for a in Data.l_files:
                    t = Data.l_o_folder + "/" + Data.l_files[a]
                    if os.path.isfile(t):
                        Data.l_values.update({a: True})
                        Data.l_values.update({'enabled': True})
            else:
                Data.l_values = {}
        except FileNotFoundError:
            Data.l_values.update({'all': False})
            Data.l_values.update({'enabled': False})

    @staticmethod
    def log(log_type, new_message):
        """Output new log entry if logging is turned on."""
        f = False
        if '_' in log_type:
            x = log_type.split("_")
            for i in x:
                if i in Data.l_values or 'all' in Data.l_values:
                    if Data.l_values['enabled']:
                        f = True
                        break
        elif log_type in Data.l_values or 'all' in Data.l_values:
            if Data.l_values['enabled']:
                f = True

        if f:
            try:
                l_file = open(Data.l_o_file, "a")
                l_file.write(datetime.now().strftime("%d-%b-%Y %H:%M:%S") +
                             " : " + new_message + "\n")
                l_file.close()
            except FileNotFoundError:
                pass
        else:
            pass

    @staticmethod
    def error():
        """Error has occured."""
