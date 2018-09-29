"""Attributes Class."""
from .data import Data
from .logging import Logger


class Attributes:
    """Device Attributes Weather."""

    def __init__(self):
        self.log = Logger()
        self.type = "Attribute"

    @staticmethod
    def data_list():
        return {"tmp": None, "end": False, "resp": False}

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
        self.log.log("attribute", "Checking device availability for : "
                     + Data.NAME[n])
        dl = self.data_list()
        data = Data.devices[n]

        try:
            dl.update({"end": (data["props"]["online"])})
            Data.NODES["Device_Availability_" + n] = dl['end']
            self.log.log("attribute", "Availability of device "
                         + Data.NAME[n] + " is : "
                         + Data.HIVETOHA[type].get(dl['end']))
            raise KeyError
        except KeyError as ex:
            self.log.log("attribute", "EXCEPTION OCCURED" + str(ex))
            self.log.log("attribute", "Device does not have "
                         + "availability info : " + Data.NAME[n])

        return Data.HIVETOHA[self.type].get(dl['end'], 'UNKNOWN')

    def get_mode(self, n):
        """Get sensor mode."""
        self.log.log("attribute", "Checking device mode for : " +
                     Data.NAME[n])
        dl = self.data_list()
        data = Data.products[n]

        try:
            dl.update({"end": (data["state"]["mode"])})
            Data.NODES["Device_Mode_" + n] = dl['end']
            self.log.log("attribute", "Mode for device "
                         + Data.NAME[n] + " is : " + str(dl['end']))
        except KeyError:
            self.log.log("attribute", "EXCEPTION OCCURED")
            self.log.log("attribute", "Device does not have mode info : "
                         + Data.NAME[n])
        return dl['end']

    def batt(self, n):
        """Get device battery level."""
        self.log.log("attribute", "Checking battery level for : " +
                     Data.NAME[n])
        dl = self.data_list()
        data = Data.devices[n]

        try:
            dl.update({"end": (data["props"]["battery"])})
            Data.NODES["BatteryLevel_" + n] = dl['end']
            self.log.log("attribute", "Battery level for device "
                         + Data.NAME[n] + " is : " + str(dl['end']))
        except KeyError:
            self.log.log("attribute", "EXCEPTION OCCURED")
            self.log.log("attribute", "Could not get battery level for : "
                         + Data.NAME[n])
        return dl['end']
