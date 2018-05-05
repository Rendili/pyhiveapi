
from .pyhiveapi import Pyhiveapi




class Attributes():
        """Device Attributes Weather."""

        def state_attributes(self, node_id):
            """Get HA State Attributes"""
            if HSC.logging.all or HSC.logging.attribute:
                Pyhiveapi.logger("Getting state_attributes for: " + node_id)

            state_attributes = {}

            available = Pyhiveapi.Attributes.online_offline(self, node_id)
            if available != 'UNKNOWN':
                state_attributes.update({"availability": available})
            battery = Pyhiveapi.Attributes.battery_level(self, node_id)
            if battery != 'UNKNOWN':
                state_attributes.update({"battery_level": str(battery) + "%"})
            mode = Pyhiveapi.Attributes.get_mode(self, node_id)
            if mode != 'UNKNOWN':
                state_attributes.update({"mode": mode})

            return state_attributes

        def online_offline(self, node_id):
            """Check if device is online"""
            if HSC.logging.all or HSC.logging.attribute:
                Pyhiveapi.logger("Checking device availability for : " +
                                 node_id)
            node_index = -1

            hive_device_availibility_tmp = ""
            hive_device_availibility_return = "UNKNOWN"
            hive_device_availibility_found = False

            current_node_attribute = "Device_Availability_" + node_id

            if node_id in HSC.devices.id_list:
                data = HSC.devices.id_list[node_id]
                for current_node_index in range(0, len(data)):
                    if "id" in data[current_node_index]:
                        if data[current_node_index][
                            "id"] == node_id:
                            node_index = current_node_index
                            break

                if node_index != -1:
                    hive_device_availibility_tmp = (
                        data[node_index]["props"]["online"])
                    hive_device_availibility_found = True

            if hive_device_availibility_found:
                NODE_ATTRIBS[
                    current_node_attribute] = hive_device_availibility_tmp
                if hive_device_availibility_tmp == True:
                    hive_device_availibility_return = 'online'
                elif hive_device_availibility_tmp == False:
                    hive_device_availibility_return = 'offline'
            else:
                if current_node_attribute in NODE_ATTRIBS:
                    hive_device_availibility_return = NODE_ATTRIBS.get(
                        current_node_attribute)
                else:
                    hive_device_availibility_return = "UNKNOWN"

            if HSC.logging.all or HSC.logging.attribute:
                if hive_device_availibility_return != "UNKNOWN":
                    Pyhiveapi.logger("Availability of device " +
                                     data[node_index]["state"]["name"] +
                                     " is : " + hive_device_availibility_return)
                else:
                    Pyhiveapi.logger("Device does not have availability info : " + node_id)

            return hive_device_availibility_return

        def get_mode(self, node_id):
            """Get sensor mode."""
            if HSC.logging.all or HSC.logging.attribute:
                Pyhiveapi.logger("Checking device mode for : " + node_id)
            node_index = -1

            hive_device_mode_tmp = ""
            hive_device_mode_return = "UNKNOWN"
            hive_device_mode_found = False

            current_node_attribute = "Device_Mode_" + node_id

            if node_id in HSC.products.id_list:
                data = HSC.products.id_list[node_id]
                for current_node_index in range(0, len(data)):
                    if "id" in data[current_node_index]:
                        if data[current_node_index][
                            "id"] == node_id:
                            node_index = current_node_index
                            break

                if node_index != -1:
                    if ("state" in data[node_index] and
                            "mode" in data[node_index]["state"]):
                        hive_device_mode_tmp = (data[node_index]
                        ["state"]["mode"])
                        hive_device_mode_found = True

            if hive_device_mode_found:
                NODE_ATTRIBS[current_node_attribute] = hive_device_mode_tmp
                hive_device_mode_return = hive_device_mode_tmp
            else:
                hive_device_mode_return = "UNKNOWN"

            if HSC.logging.all or HSC.logging.attribute:
                if hive_device_mode_return != "UNKNOWN":
                    Pyhiveapi.logger("Mode for device " +
                                     data[node_index]["state"]["name"] +
                                     " is : " + hive_device_mode_return)
                else:
                    Pyhiveapi.logger("Device does not have mode info : " + node_id)

            return hive_device_mode_return

        def battery_level(self, node_id):
            """Get device battery level."""
            if HSC.logging.all or HSC.logging.attribute:
                Pyhiveapi.logger("Checking battery level for : " + node_id)
            node_index = -1

            battery_level_return = 0
            battery_level_tmp = 0
            battery_level_found = False

            current_node_attribute = "BatteryLevel_" + node_id

            if node_id in HSC.devices.id_list:
                data = HSC.devices.id_list[node_id]
                for current_node_index in range(0, len(data)):
                    if "id" in data[current_node_index]:
                        if data[current_node_index][
                            "id"] == node_id:
                            node_index = current_node_index
                            break

                if node_index != -1:
                    if ("props" in data[node_index] and "battery" in
                            data[node_index]["props"]):
                        battery_level_tmp = (
                            data[node_index]["props"]["battery"])
                        battery_level_found = True

            if battery_level_found:
                NODE_ATTRIBS[current_node_attribute] = battery_level_tmp
                battery_level_return = battery_level_tmp
            else:
                battery_level_return = 'UNKNOWN'

            if HSC.logging.all or HSC.logging.attribute:
                if battery_level_return != 'UNKNOWN':
                    Pyhiveapi.logger("Battery level for device " +
                                     data[node_index]["state"]["name"] +
                                     " is : " + str(battery_level_return) + "%")
                else:
                    Pyhiveapi.logger("Device does not have battery info : " + node_id)

            return battery_level_return