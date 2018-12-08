""""Hive Hotwater Module. """
from pyhiveapi.hive_api import Hive


class Hotwater():
        """Hive Hotwater Code."""

        def get_mode(self, node_id):
            """Get hot water current mode."""
            node_index = -1

            hotwater_mode_return = "UNKNOWN"
            hotwater_mode_tmp = "UNKNOWN"
            hotwater_mode_found = False

            current_node_attribute = "HotWater_Mode_" + node_id

            if len(HSC.products.hotwater) > 0:
                for current_node_index in range(0, len(HSC.products.hotwater)):
                    if "id" in HSC.products.hotwater[current_node_index]:
                        if HSC.products.hotwater[current_node_index]["id"] == node_id:
                            node_index = current_node_index
                            break

                if node_index != -1:
                    if ("state" in HSC.products.hotwater[node_index] and
                            "mode" in HSC.products.hotwater[node_index]["state"]):
                        hotwater_mode_tmp = (HSC.products.hotwater[node_index]
                                             ["state"]["mode"])
                        if hotwater_mode_tmp == "BOOST":
                            if ("props" in HSC.products.hotwater[node_index] and
                                    "previous" in
                                    HSC.products.hotwater[node_index]["props"] and
                                    "mode" in
                                    HSC.products.hotwater[node_index]
                                    ["props"]["previous"]):
                                hotwater_mode_tmp = (HSC.products.hotwater[node_index]
                                                     ["props"]["previous"]["mode"])
                        elif hotwater_mode_tmp == "MANUAL":
                            hotwater_mode_tmp = "ON"
                        hotwater_mode_found = True

            if hotwater_mode_found:
                NODE_ATTRIBS[current_node_attribute] = hotwater_mode_tmp
                hotwater_mode_return = hotwater_mode_tmp
            else:
                if current_node_attribute in NODE_ATTRIBS:
                    hotwater_mode_return = NODE_ATTRIBS.get(current_node_attribute)
                else:
                    hotwater_mode_return = "UNKNOWN"

            return hotwater_mode_return

        def get_operation_modes(self, node_id):
            """Get heating list of possible modes."""
            hotwater_operation_list = ["SCHEDULE", "ON", "OFF"]
            return hotwater_operation_list

        def get_boost(self, node_id):
            """Get hot water current boost status."""
            node_index = -1

            hotwater_boost_return = "UNKNOWN"
            hotwater_boost_tmp = "UNKNOWN"
            hotwater_boost_found = False

            current_node_attribute = "HotWater_Boost_" + node_id

            if len(HSC.products.hotwater) > 0:
                for current_node_index in range(0, len(HSC.products.hotwater)):
                    if "id" in HSC.products.hotwater[current_node_index]:
                        if HSC.products.hotwater[current_node_index]["id"] == node_id:
                            node_index = current_node_index
                            break

                if node_index != -1:
                    if ("state" in HSC.products.hotwater[node_index] and
                            "boost" in HSC.products.hotwater[node_index]["state"]):
                        hotwater_boost_tmp = (HSC.products.hotwater[node_index]
                                              ["state"]["boost"])
                        if hotwater_boost_tmp is None:
                            hotwater_boost_tmp = "OFF"
                        else:
                            hotwater_boost_tmp = "ON"
                        hotwater_boost_found = True

            if hotwater_boost_found:
                NODE_ATTRIBS[current_node_attribute] = hotwater_boost_tmp
                hotwater_boost_return = hotwater_boost_tmp
            else:
                if current_node_attribute in NODE_ATTRIBS:
                    hotwater_boost_return = NODE_ATTRIBS.get(current_node_attribute)
                else:
                    hotwater_boost_return = "UNKNOWN"

            return hotwater_boost_return

        def get_boost_time(self, node_id):
            """Get hotwater boost time remaining."""
            hotwater_boost = "UNKNOWN"

            if Pyhiveapi.Hotwater.get_boost(self, node_id) == "ON":
                node_index = -1

                hotwater_boost_tmp = "UNKNOWN"
                hotwater_boost_found = False

                if len(HSC.products.hotwater) > 0:
                    for current_node_index in range(0, len(HSC.products.hotwater)):
                        if "id" in HSC.products.hotwater[current_node_index]:
                            if HSC.products.hotwater[current_node_index]["id"] == node_id:
                                node_index = current_node_index
                                break

                    if node_index != -1:
                        if "state" in HSC.products.hotwater[node_index] and "boost" in HSC.products.hotwater[node_index]["state"]:
                            hotwater_boost_tmp = (HSC.products.hotwater[node_index]["state"]["boost"])
                            hotwater_boost_found = True

                if hotwater_boost_found:
                    hotwater_boost = hotwater_boost_tmp

            return hotwater_boost

        def get_state(self, node_id):
            """Get hot water current state."""
            node_index = -1

            state_return = "OFF"
            state_tmp = "OFF"
            state_found = False
            mode_current = Pyhiveapi.Hotwater.get_mode(self, node_id)

            current_node_attribute = "HotWater_State_" + node_id

            if len(HSC.products.hotwater) > 0:
                for current_node_index in range(0, len(HSC.products.hotwater)):
                    if "id" in HSC.products.hotwater[current_node_index]:
                        if HSC.products.hotwater[current_node_index]["id"] == node_id:
                            node_index = current_node_index
                            break

                if node_index != -1:
                    if ("state" in HSC.products.hotwater[node_index] and
                            "status" in HSC.products.hotwater[node_index]["state"]):
                        state_tmp = (HSC.products.hotwater[node_index]
                                     ["state"]["status"])
                        if state_tmp is None:
                            state_tmp = "OFF"
                        else:
                            if mode_current == "SCHEDULE":
                                if Pyhiveapi.Hotwater.get_boost(self, node_id) == "ON":
                                    state_tmp = "ON"
                                    state_found = True
                                else:
                                    if ("state" in
                                            HSC.products.hotwater[node_index] and
                                            "schedule" in
                                            HSC.products.hotwater[node_index]
                                            ["state"]):
                                        snan = Pyhiveapi.p_get_schedule_now_next_later(
                                            HSC.products.hotwater[node_index]["state"]["schedule"])
                                        if 'now' in snan:
                                            if ('value' in snan["now"] and
                                                    'status' in snan["now"]["value"]):
                                                state_tmp = (snan["now"]["value"]
                                                             ["status"])
                                                state_found = True
                            else:
                                state_found = True

            if state_found:
                NODE_ATTRIBS[current_node_attribute] = state_tmp
                state_return = state_tmp
            else:
                if current_node_attribute in NODE_ATTRIBS:
                    state_return = NODE_ATTRIBS.get(current_node_attribute)
                else:
                    state_return = "UNKNOWN"

            return state_return

        def get_schedule_now_next_later(self, node_id):
            """Hive get hotwater schedule now, next and later."""
            hotwater_mode_current = Pyhiveapi.Hotwater.get_mode(self, node_id)

            snan = None

            if hotwater_mode_current == "SCHEDULE":
                node_index = -1

                if len(HSC.products.hotwater) > 0:
                    for current_node_index in range(0, len(HSC.products.hotwater)):
                        if "id" in HSC.products.hotwater[current_node_index]:
                            if HSC.products.hotwater[current_node_index]["id"] == node_id:
                                node_index = current_node_index
                                break

                if node_index != -1:
                    snan = Pyhiveapi.p_get_schedule_now_next_later(
                        HSC.products.hotwater[node_index]["state"]["schedule"])
                else:
                    snan = None
            else:
                snan = None

            return snan

        def set_mode(self, node_id, new_mode):
            """Set hot water mode."""
            Pyhiveapi.check_hive_api_logon(self)

            set_mode_success = False
            api_resp_d = {}
            api_resp = ""

            if HSC.session_id is not None:
                node_index = -1
                if len(HSC.products.hotwater) > 0:
                    for current_node_index in range(0, len(HSC.products.hotwater)):
                        if "id" in HSC.products.hotwater[current_node_index]:
                            if HSC.products.hotwater[current_node_index]["id"] == node_id:
                                node_index = current_node_index
                                break

                    if node_index != -1:
                        if "id" in HSC.products.hotwater[node_index]:
                            if new_mode == "SCHEDULE":
                                json_string_content = '{"mode": "SCHEDULE"}'
                            elif new_mode == "ON":
                                json_string_content = '{"mode": "MANUAL"}'
                            elif new_mode == "OFF":
                                json_string_content = '{"mode": "OFF"}'

                            if new_mode == "SCHEDULE" or new_mode == "ON" or new_mode == "OFF":
                                hive_api_url = (HIVE_API.urls.nodes + "/hotwater/" + HSC.products.hotwater[node_index]["id"])
                                api_resp_d = Pyhiveapi.hive_api_json_call(
                                    "POST", hive_api_url, json_string_content, False)

                                api_resp = api_resp_d['original']

                                if str(api_resp) == "<Response [200]>":
                                    Pyhiveapi.hive_api_get_nodes(self, node_id)
                                    set_mode_success = True

            return set_mode_success

        def turn_boost_on(self, node_id, length_minutes):
            """Turn hot water boost on."""
            set_boost_success = False
            hotwater_node_found = False
            api_resp_d = {}
            api_resp = ""

            if length_minutes > 0:
                hotwater_node_found = False
            else:
                return False

            for a_hotwater in HSC.products.hotwater:
                if "id" in a_hotwater:
                    if a_hotwater["id"] == node_id:
                        hotwater_node_found = True
                        break

            Pyhiveapi.check_hive_api_logon(self)

            if hotwater_node_found:
                json_string_content = '{"mode": "BOOST", "boost": ' + str(length_minutes) + '}'
                hive_api_url = (HIVE_API.urls.nodes + "/hotwater/" + node_id)
                api_resp_d = Pyhiveapi.hive_api_json_call("POST", hive_api_url, json_string_content, False)

                api_resp = api_resp_d['original']

                if str(api_resp) == "<Response [200]>":
                    Pyhiveapi.hive_api_get_nodes(self, node_id)
                    set_boost_success = True

            return set_boost_success

        def turn_boost_off(self, node_id):
            """Turn hot water boost off."""
            set_boost_success = False
            hotwater_node_found = False
            api_resp_d = {}
            api_resp = ""

            for a_hotwater in HSC.products.hotwater:
                if "id" in a_hotwater:
                    if a_hotwater["id"] == node_id:
                        hotwater_node_found = True
                        break

            Pyhiveapi.check_hive_api_logon(self)

            if hotwater_node_found:
                Pyhiveapi.hive_api_get_nodes(self, node_id)
                boost_state = self.get_boost(node_id)

                node_index = -1
                for current_node_index in range(0, len(HSC.products.hotwater)):
                    if "id" in HSC.products.hotwater[current_node_index]:
                        if HSC.products.hotwater[current_node_index]["id"] == node_id:
                            node_index = current_node_index
                            break

                if node_index != -1 and boost_state == "ON":
                    send_previous_mode = ''

                    if "props" in HSC.products.hotwater[node_index] and "previous" in HSC.products.hotwater[node_index]["props"] and "mode" in HSC.products.hotwater[node_index]["props"]["previous"]:
                        previous_mode = HSC.products.hotwater[node_index]["props"]["previous"]["mode"]
                        send_previous_mode = '"mode": "' + str(previous_mode) + '"'

                        json_string_content = '{' + send_previous_mode + '}'
                        hive_api_url = (HIVE_API.urls.nodes + "/hotwater/" + node_id)
                        api_resp_d = Pyhiveapi.hive_api_json_call("POST", hive_api_url, json_string_content, False)

                        api_resp = api_resp_d['original']

                    if str(api_resp) == "<Response [200]>":
                        Pyhiveapi.hive_api_get_nodes(self, node_id)
                        set_boost_success = True

            return set_boost_success