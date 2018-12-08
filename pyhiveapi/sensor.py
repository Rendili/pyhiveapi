"""Hive Sensor Module."""
from pyhiveapi.hive_api import Hive
from pyhiveapi.hive_data import Data
from pyhiveapi.custom_logging import Logger
from pyhiveapi.device_attributes import Attributes


class Sensor():
    """Hive Sensor Code."""
    def __init__(self):
        """Initialise."""
        self.hive = Hive()
        self.log = Logger()
        self.attr = Attributes()
        self.type = "Sensor"

    def get_state(self, n):
        """Get sensor state."""
        self.log.log('sensor', "Getting state of sensor: " +
                     Data.NAME[n])
        end = self.attr.online_offline(n)

        if end != 'offline' and n in Data.products:
            data = Data.products[n]
            if data["type"] == "contactsensor":
                end = data["props"]["status"]
            elif data["type"] == "motionsensor":
                end = data["props"]["motion"]["status"]
            Data.NODES["Sensor_State_" + n] = end
            self.log.log('sensor', "State for " + Data.NAME[n] +
                         " is : " + str(end))
        else:
            self.log.log('sensor', "Failed to get state for " + Data.NAME[n])

        return Data.HIVETOHA[self.type].get(end,
                                            Data.NODES.get(
                                                "Sensor_State_" + n))
