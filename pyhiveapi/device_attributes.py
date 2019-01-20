"""Hive Device Attribute Module."""
from pyhiveapi.custom_logging import Logger
from pyhiveapi.hive_data import Data


class Attributes:
    """Device Attributes Code."""

    def __init__(self):
        self.log = Logger()
        self.type = "Attribute"

    def state_attributes(self, n_id):
        """Get HA State Attributes"""
        self.log.log("attribute", "Getting state_attributes for: " + n_id)
        state_attributes = {}

        state_attributes.update({"availability": (self.online_offline(n_id))})
        if n_id in Data.BATTERY:
            state_attributes.update({"battery_level": str(self.batt(n_id)) + "%"})
        if n_id in Data.MODE:
            state_attributes.update({"mode": (self.get_mode(n_id))})

        return state_attributes

    def online_offline(self, n_id):
        """Check if device is online"""
        self.log.log("attribute", "Checking device availability for : " +
                     Data.NAME[n_id])
        final = None

        if n_id in Data.devices:
            data = Data.devices[n_id]
            state = data["props"]["online"]
            final = Data.HIVETOHA[self.type].get(state, 'UNKNOWN')
            Data.NODES[n_id]['Device_Availability'] = final
            self.log.log("attribute", "Availability of device " +
                         Data.NAME[n_id] + " is : " +
                         Data.HIVETOHA[type].get(state))
        else:
            self.log.log("attribute", "Device does not have " +
                         "availability info : " + Data.NAME[n_id])

        return final if final is None else Data.NODES[n_id]['Device_Availability']

    def get_mode(self, n_id):
        """Get sensor mode."""
        self.log.log("attribute", "Checking device mode for : " +
                     Data.NAME[n_id])
        state = self.online_offline(n_id)
        final = None

        if n_id in Data.products:
            if state != 'Offline':
                data = Data.products[n_id]
                state = data["state"]["mode"]
            final = Data.HIVETOHA[self.type].get(state, state)
            Data.NODES[n_id]["Device_Mode"] = final
            self.log.log("attribute", "Mode for device " +
                         Data.NAME[n_id] + " is : " + str(final))
        else:
            self.log.log("attribute", "Device does not have mode info : " +
                         Data.NAME[n_id])
        return final if final is None else Data.NODES[n_id]['Device_Mode']

    def batt(self, n_id):
        """Get device battery level."""
        self.log.log("attribute", "Checking battery level for : " +
                     Data.NAME[n_id])
        state = None

        if n_id in Data.devices:
            data = Data.devices[n_id]
            state = data["props"]["battery"]
            Data.NODES["BatteryLevel_" + n_id] = state
            self.log.log("attribute", "Battery level for device " +
                         Data.NAME[n_id] + " is : " + str(state))
        else:
            self.log.log("attribute", "Could not get battery level for : " +
                         Data.NAME[n_id])
        return state
