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

    def hub_status(self, n):
        """Get the online status of the Hive hub."""
        self.log.log('sensor', "Getting Hive hub status")
        tmp = None
        end = None

        if n in Data.devices:
            data = Data.devices[n]
            tmp = data["props"]["online"]
            end = Data.HIVETOHA[self.type]["Status"][tmp]
            Data.NODES["Sensor_State_" + n] = end
            self.log.log('sensor', "Hive hub status is: " + end)
        else:
            self.log.log('sensor', "Failed to get hive hub state")

        return end if end is None else Data.NODES.get("Sensor_State_" + n)

    def hub_smoke(self, n):
        """Get the online status of the Hive hub."""
        self.log.log('sensor', "Getting Hive hub smoke detection status")
        tmp = None
        end = None

        if n in Data.products:
            data = Data.products[n]
            tmp = data["props"]["sensors"]["SMOKE_CO"]["active"]
            end = Data.HIVETOHA[self.type]["Smoke"][tmp]
            Data.NODES["Sensor_Smoke_" + n] = end
            self.log.log('sensor', "Hive smoke detection status is : " + end)
        else:
            self.log.log('sensor', "Failed to get smoke detection status")

        return end if end is None else Data.NODES.get("Sensor_Smoke_" + n)

    def hub_dog_bark(self, n):
        """Get the online status of the Hive hub."""
        self.log.log('sensor', "Getting Hive hub barking detection status")
        tmp = None
        end = None

        if n in Data.products:
            data = Data.products[n]
            tmp = data["props"]["sensors"]["DOG_BARK"]["active"]
            end = Data.HIVETOHA[self.type]["Dog"][tmp]
            Data.NODES["Sensor_Dog_" + n] = end
            self.log.log('sensor', "Hive barking detection status is : " + end)
        else:
            self.log.log('sensor', "Failed to get barking detection status")

        return end if end is None else Data.NODES.get("Sensor_Dog_" + n)

    def hub_glass(self, n):
        """Get the glass detected status from the Hive hub."""
        self.log.log('sensor', "Getting Hive hub glass detection status")
        tmp = None
        end = None

        if n in Data.products:
            data = Data.products[n]
            tmp = data["props"]["sensors"]["GLASS_BREAK"]["active"]
            end = Data.HIVETOHA[self.type]["Glass"][tmp]
            Data.NODES["Sensor_Glass_" + n] = end
            self.log.log('sensor', "Hive glass detection status is : " + end)
        else:
            self.log.log('sensor', "Failed to get glass detection status")

        return end if end is None else Data.NODES.get("Sensor_Glass_" + n)
