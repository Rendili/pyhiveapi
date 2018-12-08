"""Hive Hub Module."""
from pyhiveapi.hive_api import Hive
from pyhiveapi.hive_data import Data
from pyhiveapi.custom_logging import Logger
from pyhiveapi.device_attributes import Attributes


class Hub:
    """ Hive Hub Code. """

    def __init__(self):
        """Initialise."""
        self.hive = Hive()
        self.log = Logger()
        self.attr = Attributes()
        self.type = "Hub"

    def hub_online_status(self, n):
        """Get the online status of the Hive hub."""
        self.log.log('sensor', "Getting Hive hub status: " +
                     Data.NAME[n])
        tmp = None
        end = None

        if n in Data.devices:
            data = Data.devices[n]
            tmp = data["props"]["online"]
            end = Data.HIVETOHA[self.type][tmp]
            Data.NODES["Sensor_State_" + n] = end
            self.log.log('sensor', "Hive hub status is : " + end)
        else:
            self.log.log('sensor', "Failed to get state: " + Data.NAME[n])

        return end if end is None else Data.NODES.get("Sensor_State_" + n)
