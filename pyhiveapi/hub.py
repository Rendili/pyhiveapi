"""Hive Hub Module."""
from pyhiveapi.custom_logging import Logger
from pyhiveapi.device_attributes import Attributes
from pyhiveapi.hive_api import Hive
from pyhiveapi.hive_data import Data


class Hub:
    """ Hive Hub Code. """

    def __init__(self):
        """Initialise."""
        self.hive = Hive()
        self.log = Logger()
        self.attr = Attributes()
        self.type = "Hub"
        self.log_type = "Sensor"

    def hub_status(self, n_id):
        """Get the online status of the Hive hub."""
        self.log.log(n_id, self.log_type, "Getting Hive hub status")
        state = self.attr.online_offline(n_id)
        final = None

        if n_id in Data.devices:
            if state != "Offline":
                data = Data.devices[n_id]
                state = data["props"]["online"]
                final = Data.HIVETOHA[self.type]["Status"].get(state, state)
                self.log.log(n_id, self.log_type, "Status is {0}", info=final)
            self.log.error_check(n_id, self.type, state)
            final = Data.HIVETOHA[self.type]["Status"].get(state, state)
            Data.NODES[n_id]["State"] = final

        else:
            self.log.error_check(n_id, "ERROR", "Failed")

        return final if final is None else Data.NODES[n_id]["State"]

    def hub_smoke(self, n_id):
        """Get the online status of the Hive hub."""
        self.log.log(n_id, self.log_type, "Getting smoke detection status")
        state = self.attr.online_offline(n_id)
        final = None

        if n_id in Data.products:
            if state != "Offline":
                data = Data.products[n_id]
                state = data["props"]["sensors"]["SMOKE_CO"]["active"]
                final = Data.HIVETOHA[self.type]["Smoke"].get(state, state)
                self.log.log(n_id, self.log_type, "Status is {0}", info=final)
            self.log.error_check(n_id, self.type, state)
            final = Data.HIVETOHA[self.type]["Smoke"].get(state, state)
            Data.NODES[n_id]["Smoke"] = final
        else:
            self.log.error_check(n_id, "ERROR", "Failed")

        return final if final is None else Data.NODES[n_id]["Smoke"]

    def hub_dog_bark(self, n_id):
        """Get the online status of the Hive hub."""
        self.log.log(n_id, self.log_type, "Getting barking detection status")
        state = self.attr.online_offline(n_id)
        final = None

        if n_id in Data.products:
            if state != "Offline":
                data = Data.products[n_id]
                state = data["props"]["sensors"]["DOG_BARK"]["active"]
                final = Data.HIVETOHA[self.type]["Dog"].get(state, state)
                self.log.log(n_id, self.log_type, "Status is {0}", info=final)
            self.log.error_check(n_id, self.type, state)
            final = Data.HIVETOHA[self.type]["Dog"].get(state, state)
            Data.NODES[n_id]["Dog"] = final
        else:
            self.log.error_check(n_id, "ERROR", "Failed")

        return final if final is None else Data.NODES[n_id]["Dog"]

    def hub_glass(self, n_id):
        """Get the glass detected status from the Hive hub."""
        self.log.log(n_id, self.log_type, "Getting glass detection status")
        state = self.attr.online_offline(n_id)
        final = None

        if n_id in Data.products:
            if state != "Offline":
                data = Data.products[n_id]
                state = data["props"]["sensors"]["GLASS_BREAK"]["active"]
                final = Data.HIVETOHA[self.type]["Glass"].get(state, state)
                self.log.log(n_id, self.log_type, "Status is {0}", info=final)
            self.log.error_check(n_id, self.type, state)
            final = Data.HIVETOHA[self.type]["Glass"].get(state, state)
            Data.NODES[n_id]["Glass"] = final
        else:
            self.log.error_check(n_id, "ERROR", "Failed")

        return final if final is None else Data.NODES[n_id]["Glass"]
