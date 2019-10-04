"""Custom Logging Module."""
import os
from datetime import datetime

from pyhiveapi.hive_data import Data


class Logger:
    """Custom Logging Code."""

    def __init__(self):
        """Logger Initialisation"""

    @staticmethod
    def check_logging(new_session):
        """Check Logging Active"""
        Data.l_o_folder = os.path.expanduser("~") + "/.homeassistant/pyhiveapi"
        Data.l_o_file = Data.l_o_folder + "/pyhiveapi.log"
        count = 0
        try:
            if new_session and os.path.isfile(Data.l_o_file):
                os.remove(Data.l_o_file)

            if os.path.isdir(Data.l_o_folder):
                for name in Data.l_files:
                    loc = Data.l_o_folder + "/" + Data.l_files[name]
                    if os.path.isfile(loc):
                        Data.l_values.update({name: True})
                        Data.l_values.update({"enabled": True})
                    elif os.path.isfile(loc) is False:
                        count += 1
                        if count == len(Data.l_files):
                            Data.l_values = {}
        except FileNotFoundError:
            Data.l_values = {}

    @staticmethod
    def log(n_id, l_type, new_message, **kwargs):
        """Output new log entry if logging is turned on."""
        name = Data.NAME.get(n_id, n_id)
        data = kwargs.get("info", None)
        values = Data.l_values
        if n_id == "No_ID":
            name = "Hive"
        final = False
        if "_" in l_type:
            nxt = l_type.split("_")
            for i in nxt:
                if i in Data.l_values or "All" in Data.l_values:
                    if Data.l_values["enabled"]:
                        final = True
                        break
        elif l_type in values or "All" in values:
            if Data.l_values["enabled"]:
                final = True

        if final:
            try:
                l_file = open(Data.l_o_file, "a")
                l_file.write(
                    datetime.now().strftime("%d-%b-%Y %H:%M:%S")
                    + " - "
                    + l_type
                    + " - "
                    + name
                    + " : "
                    + new_message.format(data)
                    + "\n"
                )
                l_file.close()
            except FileNotFoundError:
                pass
        else:
            pass

    def error_check(self, n_id, n_type, error_type, **kwargs):
        """Error has occurred."""
        import re

        message = None
        new_data = None
        if error_type == "Offline":
            message = "Device offline could not update entity."
        elif error_type == "Failed":
            message = "ERROR - No data found for device."
        elif error_type == "Failed_API":
            code = kwargs.get("resp")
            new_data = re.search("[0-9][0-9][0-9]", str(code)).group(0)
            message = "ERROR - Received {0} response from API."
        self.log(n_id, n_type, message, info=new_data)
