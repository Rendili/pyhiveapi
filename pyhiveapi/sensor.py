"""Hive Sensor Module."""
from pyhiveapi.custom_logging import Logger
from pyhiveapi.device_attributes import Attributes
from pyhiveapi.hive_api import Hive
from pyhiveapi.hive_data import Data


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
        self.log.log(n_id, self.type, "Getting state")
        state = self.attr.online_offline(n_id)
        final = None

        if n_id in Data.products:
            if state != 'Offline':
                data = Data.products[n_id]
                if data["type"] == "contactsensor":
                    state = data["props"]["status"]
                elif data["type"] == "motionsensor":
                    state = data["props"]["motion"]["status"]
                final = Data.HIVETOHA[self.type].get(state, state)
                self.log.log(n_id, self.type, "Status is {0}", info=final)
            self.log.error_check(n_id, self.type, state)
            final = Data.HIVETOHA[self.type].get(state, state)
            Data.NODES[n_id]['State'] = final
        else:
            self.log.error_check(n_id, 'ERROR', 'Failed')

        return final if final is None else Data.NODES[n_id]['State']
