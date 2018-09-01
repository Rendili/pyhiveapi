"""Logger.py"""

from .data import Data as Dt
from datetime import datetime
import os


class Logger:
    """Logger Class."""
    
    def __init__(self):
        """Logger Initialisation"""

    @staticmethod
    def check_logging(new_session):
        """Check Logging Active"""
        Dt.l_o_folder = os.path.expanduser('~') + "/pyhiveapi"
        Dt.l_o_file = Dt.l_o_folder + "/pyhiveapi.log"
        try:
            if new_session and os.path.isfile(Dt.l_o_file):
                os.remove(Dt.l_o_file)

            if os.path.isdir(Dt.l_o_folder):
                for a in Dt.l_files:
                    t = Dt.l_o_folder + "/" + Dt.l_files[a]
                    if os.path.isfile(t):
                        Dt.l_values.update({a: True})
                        Dt.l_values.update({'enabled': True})
        except FileNotFoundError:
            Dt.l_values.update({'all': False})
            Dt.l_values.update({'enabled': False})

    @staticmethod
    def log(log_type, new_message):
        """Output new log entry if logging is turned on."""
        f = False
        if '_' in log_type:
            x = log_type.split("_")
            for i in x:
                if i in Dt.l_values:
                    f = i
                    break
        else:
            f = log_type

        if f in Dt.l_values and Dt.l_values['enabled']:
            try:
                l_file = open(Dt.l_o_file, "a")
                l_file.write(datetime.now().strftime("%d-%b-%Y %H:%M:%S")
                             + " : " + new_message + "\n")
                l_file.close()
            except FileNotFoundError:
                pass

    @staticmethod
    def error():
        """Error has occured."""
