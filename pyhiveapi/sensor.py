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

    def get_state(self, id):
        """Get sensor state."""
        self.log.log('sensor', "Getting state of sensor: " +
                     Data.NAME[id])
        end = self.attr.online_offline(id)

        if end != 'offline' and id in Data.products:
            data = Data.products[id]
            if data["type"] == "contactsensor":
                end = data["props"]["status"]
            elif data["type"] == "motionsensor":
                end = data["props"]["motion"]["status"]
            Data.NODES["Sensor_State_" + id] = end
            self.log.log('sensor', "State for " + Data.NAME[id] +
                         " is : " + str(end))
        else:
            self.log.log('sensor', "Failed to get state for " + Data.NAME[id])

        return Data.HIVETOHA[self.type].get(end,
                                            Data.NODES.get(
                                                "Sensor_State_" + id))
