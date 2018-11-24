"""Attributes Class."""
from .data import Data
from .logging import Logger


class Attributes:
    """Device Attributes Weather."""

    def __init__(self):
        self.log = Logger()
        self.type = "Attribute"

    def state_attributes(self, n):
        """Get HA State Attributes"""
        self.log.log("attribute", "Getting state_attributes for: " + n)
        state_attributes = {}

        state_attributes.update({"availability": (self.online_offline(n))})
        if n in Data.BATTERY:
            state_attributes.update({"battery_level": str(self.batt(n)) + "%"})
        if n in Data.MODE:
            state_attributes.update({"mode": (self.get_mode(n))})

        return state_attributes

    def online_offline(self, n):
        """Check if device is online"""
        self.log.log("attribute", "Checking device availability for : " +
                     Data.NAME[n])
        end = 'offline'

        if Data.data_present:
            data = Data.devices[n]
            end = data["props"]["online"]
            Data.NODES["Device_Availability_" + n] = end
            self.log.log("attribute", "Availability of device " +
                         Data.NAME[n] + " is : " +
                         Data.HIVETOHA[type].get(end))
        else:
            self.log.log("attribute", "Device does not have " +
                         "availability info : " + Data.NAME[n])

        return Data.HIVETOHA[self.type].get(end, 'UNKNOWN')

    def get_mode(self, n):
        """Get sensor mode."""
        self.log.log("attribute", "Checking device mode for : " +
                     Data.NAME[n])
        end = None

        if Data.data_present:
            data = Data.products[n]
            end = data["state"]["mode"]
            Data.NODES["Device_Mode_" + n] = end
            self.log.log("attribute", "Mode for device " +
                         Data.NAME[n] + " is : " + str(end))
        else:
            self.log.log("attribute", "Device does not have mode info : " +
                         Data.NAME[n])
        return end

    def batt(self, n):
        """Get device battery level."""
        self.log.log("attribute", "Checking battery level for : " +
                     Data.NAME[n])
        end = None

        if Data.data_present:
            data = Data.devices[n]
            end = data["props"]["battery"]
            Data.NODES["BatteryLevel_" + n] = end
            self.log.log("attribute", "Battery level for device " +
                         Data.NAME[n] + " is : " + str(end))
        else:
            self.log.log("attribute", "Could not get battery level for : " +
                         Data.NAME[n])
        return end
