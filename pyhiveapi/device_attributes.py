"""Hive Device Attribute Module."""
from pyhiveapi.custom_logging import Logger
from pyhiveapi.hive_data import Data


class Attributes:
    """Device Attributes Code."""

    def __init__(self):
        self.log = Logger()
        self.type = "Attribute"

    def state_attributes(self, id):
        """Get HA State Attributes"""
        self.log.log("attribute", "Getting state_attributes for: " + id)
        state_attributes = {}

        state_attributes.update({"availability": (self.online_offline(id))})
        if id in Data.BATTERY:
            state_attributes.update({"battery_level": str(self.batt(id)) + "%"})
        if id in Data.MODE:
            state_attributes.update({"mode": (self.get_mode(id))})

        return state_attributes

    def online_offline(self, id):
        """Check if device is online"""
        self.log.log("attribute", "Checking device availability for : " +
                     Data.NAME[id])
        state = 'offline'

        if id in Data.devices:
            data = Data.devices[id]
            state = data["props"]["online"]
            Data.NODES["Device_Availability_" + id] = state
            self.log.log("attribute", "Availability of device " +
                         Data.NAME[id] + " is : " +
                         Data.HIVETOHA[type].get(state))
        else:
            self.log.log("attribute", "Device does not have " +
                         "availability info : " + Data.NAME[id])

        return Data.HIVETOHA[self.type].get(state, 'UNKNOWN')

    def get_mode(self, id):
        """Get sensor mode."""
        self.log.log("attribute", "Checking device mode for : " +
                     Data.NAME[id])
        state = None

        if id in Data.products:
            data = Data.products[id]
            state = data["state"]["mode"]
            Data.NODES["Device_Mode_" + id] = state
            self.log.log("attribute", "Mode for device " +
                         Data.NAME[id] + " is : " + str(state))
        else:
            self.log.log("attribute", "Device does not have mode info : " +
                         Data.NAME[id])
        return state

    def batt(self, id):
        """Get device battery level."""
        self.log.log("attribute", "Checking battery level for : " +
                     Data.NAME[id])
        state = None

        if id in Data.devices:
            data = Data.devices[id]
            state = data["props"]["battery"]
            Data.NODES["BatteryLevel_" + id] = state
            self.log.log("attribute", "Battery level for device " +
                         Data.NAME[id] + " is : " + str(state))
        else:
            self.log.log("attribute", "Could not get battery level for : " +
                         Data.NAME[id])
        return state
