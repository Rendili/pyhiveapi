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

    def hub_status(self, n_id):
        """Get the online status of the Hive hub."""
        self.log.log('sensor', "Getting Hive hub status")
        state = self.attr.online_offline(n_id)
        final = None

        if n_id in Data.devices:
            if state != 'offline':
                data = Data.devices[n_id]
                state = data["props"]["online"]
            final = Data.HIVETOHA[self.type]["Status"].get(state, state)
            Data.NODES[n_id]['State'] = final
            self.log.log('sensor', "Hive hub status is: " + final)
        else:
            self.log.log('sensor', "Failed to get hive hub state")

        return final if final is None else Data.NODES[n_id]['State']

    def hub_smoke(self, n_id):
        """Get the online status of the Hive hub."""
        self.log.log('sensor', "Getting Hive hub smoke detection status")
        state = self.attr.online_offline(n_id)
        final = None

        if n_id in Data.products:
            if state != 'offline':
                data = Data.products[n_id]
                state = data["props"]["sensors"]["SMOKE_CO"]["active"]
            final = Data.HIVETOHA[self.type]["Smoke"].get(state, state)
            Data.NODES[n_id]['Smoke'] = final
            self.log.log('sensor', "Hive smoke detection status is : " + final)
        else:
            self.log.log('sensor', "Failed to get smoke detection status")

        return final if final is None else Data.NODES[n_id]['Smoke']

    def hub_dog_bark(self, n_id):
        """Get the online status of the Hive hub."""
        self.log.log('sensor', "Getting Hive hub barking detection status")
        state = self.attr.online_offline(n_id)
        final = None

        if n_id in Data.products:
            if state != 'offline':
                data = Data.products[n_id]
                state = data["props"]["sensors"]["DOG_BARK"]["active"]
            final = Data.HIVETOHA[self.type]["Smoke"].get(state, state)
            Data.NODES[n_id]['Dog'] = final
            self.log.log('sensor', "Hive barking detection status is : " + final)
        else:
            self.log.log('sensor', "Failed to get barking detection status")

        return final if final is None else Data.NODES[n_id]['Dog']

    def hub_glass(self, n_id):
        """Get the glass detected status from the Hive hub."""
        self.log.log('sensor', "Getting Hive hub glass detection status")
        state = self.attr.online_offline(n_id)
        final = None

        if n_id in Data.products:
            if state != 'offline':
                data = Data.products[n_id]
                state = data["props"]["sensors"]["GLASS_BREAK"]["active"]
            final = Data.HIVETOHA[self.type]["Smoke"].get(state, state)
            Data.NODES[n_id]['Glass'] = final
            self.log.log('sensor', "Hive glass detection status is : " + final)
        else:
            self.log.log('sensor', "Failed to get glass detection status")

        return final if final is None else Data.NODES[n_id]['Glass']
