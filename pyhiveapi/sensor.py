"""Hive Sensor Module."""
from pyhiveapi.hive_api import Hive
from pyhiveapi.hive_data import Data
from pyhiveapi.custom_logging import Logger
from pyhiveapi.device_attributes import Attributes


class Sensor:
    """Hive Sensor Code."""

    def __init__(self):
        """Initialise."""
        self.hive = Hive()
        self.log = Logger()
        self.attr = Attributes()
        self.type = "Sensor"

    def get_state(self, n_id):
        """Get sensor state."""
        self.log.log('sensor', "Getting state of sensor: " +
                     Data.NAME[n_id])
        state = self.attr.online_offline(n_id)
        final = None

        if n_id in Data.products:
            if state != 'offline':
                data = Data.products[n_id]
                if data["type"] == "contactsensor":
                    state = data["props"]["status"]
                elif data["type"] == "motionsensor":
                    state = data["props"]["motion"]["status"]
            final = Data.HIVETOHA[self.type].get(state, state)
            Data.NODES[n_id]['State'] = final
            self.log.log('sensor', "State for " + Data.NAME[n_id] +
                         " is : " + str(state))

        return final if final is None else Data.NODES[n_id]['State']
