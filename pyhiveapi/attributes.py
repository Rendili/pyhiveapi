"""Attributes Class."""
from .logging import Logger
from .data import Data as Dt


class Attributes:
        """Device Attributes Weather."""
        def __init__(self):
            self.log = Logger()

        def state_attributes(self, node):
            """Get HA State Attributes"""
            self.log.log("attribute", "Getting state_attributes for: " + node)

            state_attributes = {}

            available = self.online_offline(node)
            if available != 'UNKNOWN':
                state_attributes.update({"availability": available})
            battery = self.battery_level(node)
            if battery != 'UNKNOWN':
                state_attributes.update({"battery_level": str(battery) + "%"})
            mode = self.get_mode(node)
            if mode != 'UNKNOWN':
                state_attributes.update({"mode": mode})

            return state_attributes

        def online_offline(self, node):
            """Check if device is online"""
            self.log.log("attribute", "Checking device availability for : "
                         + node)

            hive_data_tmp = ""
            hive_data_return = "UNKNOWN"
            cna = "Device_Availability_" + node
            data = Dt.devices[node]

            try:
                hive_data_tmp = data["props"]["online"]
                hive_data_found = True
            except KeyError:
                hive_data_found = False

            if hive_data_found:
                Dt.NODES[cna] = hive_data_tmp
                if hive_data_tmp:
                    hive_data_return = 'online'
                elif not hive_data_tmp:
                    hive_data_return = 'offline'
            else:
                if cna in Dt.NODES:
                    hive_data_return = Dt.NODES.get(cna)
                else:
                    hive_data_return = "UNKNOWN"

            if hive_data_return != "UNKNOWN":
                self.log.log("attribute", "Availability of device "
                             + data["state"]["name"] + " is : "
                             + hive_data_return)
            else:
                self.log.log("attribute", "Device does not have "
                             + "availability info : " + node)

            return hive_data_return

        def get_mode(self, node):
            """Get sensor mode."""
            self.log.log("attribute", "Checking device mode for : " + node)

            hive_data_tmp = ""
            cna = "Device_Mode_" + node
            data = Dt.products[node]

            try:
                hive_data_tmp = data["state"]["mode"]
                hive_data_found = True
            except KeyError:
                hive_data_found = False

            if hive_data_found:
                Dt.NODES[cna] = hive_data_tmp
                hive_data_return = hive_data_tmp
            else:
                hive_data_return = "UNKNOWN"

            if hive_data_return != "UNKNOWN":
                self.log.log("attribute", "Mode for device "
                             + data["state"]["name"] + " is : "
                             + hive_data_return)
            else:
                self.log.log("attribute", "Device does not have mode info : "
                             + node)

            return hive_data_return

        def battery_level(self, node):
            """Get device battery level."""
            self.log.log("attribute", "Checking battery level for : " + node)

            hive_data_tmp = 0
            cna = "BatteryLevel_" + node
            data = Dt.devices[node]

            try:
                hive_data_tmp = data["props"]["battery"]
                hive_data_found = True
            except KeyError:
                hive_data_found = False

            if hive_data_found:
                Dt.NODES[cna] = hive_data_tmp
                hive_data_return = hive_data_tmp
            else:
                hive_data_return = 'UNKNOWN'

            if hive_data_return != 'UNKNOWN':
                self.log.log("attribute", "Battery level for device "
                             + data["state"]["name"] + " is : "
                             + str(hive_data_return) + "%")
            else:
                self.log.log("attribute", "Device does not have battery info: "
                             + node)

            return hive_data_return
