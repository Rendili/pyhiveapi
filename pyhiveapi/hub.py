"""Hive Hub Module."""
from pyhiveapi.hive_api import Hive
from pyhiveapi.hive_data import Data


class Hub:
    """ Hive Hub Code. """

    def hub_online_status(self, node_id):
        """Get the online status of the Hive hub."""
        if HSC.logging.all or HSC.logging.sensor:
            Pyhiveapi.logger("Getting Hive hub status: " + node_id)
        return_status = "Offline"

        for a_hub in HSC.devices.hub:
            if "id" in a_hub:
                if a_hub["id"] == node_id:
                    if "props" in a_hub and "online" in a_hub["props"]:
                        if a_hub["props"]["online"]:
                            return_status = "Online"
                        else:
                            return_status = "Offline"
        if HSC.logging.all or HSC.logging.sensor:
            Pyhiveapi.logger("Hive hub status is : " + return_status)

        return return_status