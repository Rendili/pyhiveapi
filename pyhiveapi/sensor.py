

from .pyhiveapi import Pyhiveapi




class Sensor():
        """Hive Sensors."""

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

        def get_state(self, node_id, node_device_type):
            """Get sensor state."""
            if HSC.logging.all or HSC.logging.sensor:
                Pyhiveapi.logger("Getting sensor status for: " + node_id)
            result = Pyhiveapi.Attributes.online_offline(self, node_id)
            node_index = -1

            start_date = ''
            end_date = ''
            sensor_state_tmp = False
            sensor_state_return = False
            sensor_found = False

            current_node_attribute = "Sensor_State_" + node_id

            if len(HSC.products.sensors) > 0:
                for current_node_index in range(0, len(HSC.products.sensors)):
                    if "id" in HSC.products.sensors[current_node_index]:
                        if HSC.products.sensors[current_node_index]["id"] == node_id:
                            node_index = current_node_index
                            break

                if node_index != -1:
                    if node_device_type == "contactsensor":
                        state = (HSC.products.sensors[node_index]["props"]["status"])
                        if state == 'OPEN':
                            sensor_state_tmp = True
                        sensor_found = True
                    elif node_device_type == "motionsensor":
                        sensor_state_tmp = (HSC.products.sensors[
                            node_index]["props"]["motion"]["status"])
                        sensor_found = True

            if result == 'offline':
                sensor_state_return = False
            elif sensor_found:
                NODE_ATTRIBS[current_node_attribute] = sensor_state_tmp
                sensor_state_return = sensor_state_tmp
            else:
                if current_node_attribute in NODE_ATTRIBS:
                    sensor_state_return = NODE_ATTRIBS.get(current_node_attribute)
                else:
                    sensor_state_return = False

            if HSC.logging.all or HSC.logging.sensor:
                Pyhiveapi.logger("State for " + HSC.products.sensors[node_index]["type"] +
                                 " - " + HSC.products.sensors[node_index]["state"]["name"] +
                                 " is : " + str(sensor_state_return))

            return sensor_state_return