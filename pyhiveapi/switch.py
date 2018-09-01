
from .api import Hive






class Switch():
        """Hive Switches."""

        def get_state(self, node_id):
            """Get smart plug current state."""
            if HSC.logging.all or HSC.logging.switch:
                Pyhiveapi.logger("Getting state for switch : " + node_id)
            result = Pyhiveapi.Attributes.online_offline(self, node_id)
            node_index = -1

            smartplug_state_tmp = "UNKNOWN"
            smartplug_state_return = "UNKNOWN"
            smartplug_state_found = False

            current_node_attribute = "Smartplug_State_" + node_id

            if len(HSC.products.plug) > 0:
                for current_node_index in range(0, len(HSC.products.plug)):
                    if "id" in HSC.products.plug[current_node_index]:
                        if HSC.products.plug[current_node_index]["id"] == node_id:
                            node_index = current_node_index
                            break

                if node_index != -1:
                    if ("state" in HSC.products.plug[
                        node_index] and "status" in
                        HSC.products.plug[node_index]["state"]):
                        smartplug_state_tmp = (HSC.products.plug[node_index]
                                               ["state"]["status"])
                        smartplug_state_found = True

            if result == "offline":
                smartplug_state_return = "OFF"
            elif smartplug_state_found:
                NODE_ATTRIBS[current_node_attribute] = smartplug_state_tmp
                smartplug_state_return = smartplug_state_tmp
            else:
                if current_node_attribute in NODE_ATTRIBS:
                    smartplug_state_return = NODE_ATTRIBS.get(
                        current_node_attribute)
                else:
                    smartplug_state_return = "UNKNOWN"

            smartplug_state_return_b = False

            if smartplug_state_return == "ON":
                smartplug_state_return_b = True

            if HSC.logging.all or HSC.logging.switch:
                Pyhiveapi.logger("State of switch " +
                                 HSC.products.plug[node_index]["state"]["name"] +
                                 " is : " + smartplug_state_return)

            return smartplug_state_return_b

        def get_power_usage(self, node_id):
            """Get smart plug current power usage."""
            if HSC.logging.all or HSC.logging.switch:
                Pyhiveapi.logger("Getting power usage for: " + node_id)
            node_index = -1

            current_power_tmp = 0
            current_power_return = 0
            current_power_found = False

            current_node_attribute = "Smartplug_Current_Power_" + node_id

            if len(HSC.products.plug) > 0:
                for current_node_index in range(0, len(HSC.products.plug)):
                    if "id" in HSC.products.plug[current_node_index]:
                        if HSC.products.plug[current_node_index]["id"] == node_id:
                            node_index = current_node_index
                            break

                if node_index != -1:
                    if ("props" in HSC.products.plug[node_index]
                        and "powerConsumption"
                        in HSC.products.plug[node_index]["props"]):
                        current_power_tmp = (HSC.products.plug[node_index]
                                             ["props"]["powerConsumption"])
                        current_power_found = True

            if current_power_found:
                NODE_ATTRIBS[current_node_attribute] = current_power_tmp
                current_power_return = current_power_tmp
            else:
                if current_node_attribute in NODE_ATTRIBS:
                    current_power_return = NODE_ATTRIBS.get(
                        current_node_attribute)
                else:
                    current_power_return = 0

            if HSC.logging.all or HSC.logging.switch:
                Pyhiveapi.logger("For switch " +
                                 HSC.products.plug[node_index]["state"]["name"] +
                                 " power usage is : " + str(current_power_return))

            return current_power_return

        def turn_on(self, node_id):
            """Set smart plug to turn on."""
            if HSC.logging.all or HSC.logging.switch:
                Pyhiveapi.logger("Turning on switch : " + node_id)
            Pyhiveapi.check_hive_api_logon(self)

            node_index = -1

            set_mode_success = False
            api_resp_d = {}
            api_resp = ""

            if HSC.session_id is not None:
                if len(HSC.products.plug) > 0:
                    for current_node_index in range(0, len(HSC.products.plug)):
                        if "id" in HSC.products.plug[current_node_index]:
                            if HSC.products.plug[current_node_index][
                                "id"] == node_id:
                                node_index = current_node_index
                                break
                    if node_index != -1:
                        json_string_content = '{"status": "ON"}'
                        hive_api_url = (HIVE_API.urls.nodes
                                        + '/'
                                        + HSC.products.plug[node_index]["type"]
                                        + '/'
                                        + HSC.products.plug[node_index]["id"])
                        api_resp_d = Pyhiveapi.hive_api_json_call("POST",
                                                                  hive_api_url,
                                                                  json_string_content,
                                                                  False)

                        api_resp = api_resp_d['original']

                        if str(api_resp) == "<Response [200]>":
                            Pyhiveapi.hive_api_get_nodes(self, node_id)
                            set_mode_success = True
                            if HSC.logging.all or HSC.logging.switch:
                                Pyhiveapi.logger("Switch " + HSC.products.plug[node_index]["state"]["name"] +
                                                 " has been sucessfully switched on")

            return set_mode_success

        def turn_off(self, node_id):
            """Set smart plug to turn off."""
            if HSC.logging.all or HSC.logging.switch:
                Pyhiveapi.logger("Turning off switch : " + node_id)
            Pyhiveapi.check_hive_api_logon(self)

            node_index = -1

            set_mode_success = False
            api_resp_d = {}
            api_resp = ""

            if HSC.session_id is not None:
                if len(HSC.products.plug) > 0:
                    for current_node_index in range(0, len(HSC.products.plug)):
                        if "id" in HSC.products.plug[current_node_index]:
                            if HSC.products.plug[current_node_index][
                                "id"] == node_id:
                                node_index = current_node_index
                                break
                    if node_index != -1:
                        json_string_content = '{"status": "OFF"}'
                        hive_api_url = (HIVE_API.urls.nodes
                                        + '/'
                                        + HSC.products.plug[node_index]["type"]
                                        + '/'
                                        + HSC.products.plug[node_index]["id"])
                        api_resp_d = Pyhiveapi.hive_api_json_call("POST",
                                                                  hive_api_url,
                                                                  json_string_content,
                                                                  False)

                        api_resp = api_resp_d['original']

                        if str(api_resp) == "<Response [200]>":
                            Pyhiveapi.hive_api_get_nodes(self, node_id)
                            set_mode_success = True
                            if HSC.logging.all or HSC.logging.switch:
                                Pyhiveapi.logger("Swicth " + HSC.products.plug[node_index]["state"]["name"] +
                                                 " has been sucessfully switched off")

            return set_mode_success