"""Hive Heating Module."""
from pyhiveapi.hive_api import Hive

class Heating():
        """Hive Heating Code."""

        def min_temperature(self, node_id):
            """Get heating minimum target temperature."""
            heating_min_temp_default = 5
            heating_min_temp_return = 0
            heating_min_temp_tmp = 0
            heating_min_temp_found = False

            heating_min_temp_tmp = heating_min_temp_default

            current_node_attribute = "Heating_Min_Temperature_" + node_id

            if heating_min_temp_found:
                NODE_ATTRIBS[current_node_attribute] = heating_min_temp_tmp
                heating_min_temp_return = heating_min_temp_tmp
            else:
                if current_node_attribute in NODE_ATTRIBS:
                    heating_min_temp_return = NODE_ATTRIBS.get(current_node_attribute)
                else:
                    heating_min_temp_return = heating_min_temp_default

            return heating_min_temp_return

        def max_temperature(self, node_id):
            """Get heating maximum target temperature."""
            heating_max_temp_default = 32
            heating_max_temp_return = 0
            heating_max_temp_tmp = 0
            heating_max_temp_found = False

            heating_max_temp_tmp = heating_max_temp_default

            current_node_attribute = "Heating_Max_Temperature_" + node_id

            if heating_max_temp_found:
                NODE_ATTRIBS[current_node_attribute] = heating_max_temp_tmp
                heating_max_temp_return = heating_max_temp_tmp
            else:
                if current_node_attribute in NODE_ATTRIBS:
                    heating_max_temp_return = NODE_ATTRIBS.get(current_node_attribute)
                else:
                    heating_max_temp_return = heating_max_temp_default

            return heating_max_temp_return

        def current_temperature(self, node_id):
            """Get heating current temperature."""
            node_index = -1

            current_temp_return = 0
            current_temp_tmp = 0
            current_temp_found = False

            current_node_attribute = "Heating_CurrentTemp_" + node_id

            if len(HSC.products.heating) > 0:
                for current_node_index in range(0, len(HSC.products.heating)):
                    if "id" in HSC.products.heating[current_node_index]:
                        if HSC.products.heating[current_node_index]["id"] == node_id:
                            node_index = current_node_index
                            break

                if node_index != -1:
                    if "props" in HSC.products.heating[node_index]:
                        if "temperature" in HSC.products.heating[node_index]["props"]:
                            current_temp_tmp = (HSC.products.heating[node_index]
                                                ["props"]["temperature"])
                            current_temp_found = True

            if current_temp_found:
                NODE_ATTRIBS[current_node_attribute] = current_temp_tmp
                current_temp_return = current_temp_tmp
            else:
                if current_node_attribute in NODE_ATTRIBS:
                    current_temp_return = NODE_ATTRIBS.get(current_node_attribute)
                else:
                    current_temp_return = -1000

            if current_temp_return != -1000:
                if node_id in HSC.data.minmax:
                    if HSC.data.minmax[node_id]['TodayDate'] != datetime.date(datetime.now()):
                        HSC.data.minmax[node_id]['TodayMin'] = 1000
                        HSC.data.minmax[node_id]['TodayMax'] = -1000
                        HSC.data.minmax[node_id]['TodayDate'] = datetime.date(datetime.now())

                    if current_temp_return < HSC.data.minmax[node_id]['TodayMin']:
                        HSC.data.minmax[node_id]['TodayMin'] = current_temp_return

                    if current_temp_return > HSC.data.minmax[node_id]['TodayMax']:
                        HSC.data.minmax[node_id]['TodayMax'] = current_temp_return

                    if current_temp_return < HSC.data.minmax[node_id]['RestartMin']:
                        HSC.data.minmax[node_id]['RestartMin'] = current_temp_return

                    if current_temp_return > HSC.data.minmax[node_id]['RestartMax']:
                        HSC.data.minmax[node_id]['RestartMax'] = current_temp_return
                else:
                    current_node_max_min_data = {}
                    current_node_max_min_data['TodayMin'] = current_temp_return
                    current_node_max_min_data['TodayMax'] = current_temp_return
                    current_node_max_min_data['TodayDate'] = datetime.date(datetime.now())
                    current_node_max_min_data['RestartMin'] = current_temp_return
                    current_node_max_min_data['RestartMax'] = current_temp_return
                    HSC.data.minmax[node_id] = current_node_max_min_data
            else:
                current_temp_return = 0

            return current_temp_return

        def minmax_temperatures(self, node_id):
            """Min/Max Temp"""
            if node_id in HSC.data.minmax:
                return HSC.data.minmax[node_id]
            else:
                return None

        def get_target_temperature(self, node_id):
            """Get heating target temperature."""
            node_index = -1

            heating_target_temp_return = 0
            heating_target_temp_tmp = 0
            heating_target_temp_found = False

            current_node_attribute = "Heating_TargetTemp_" + node_id

            if len(HSC.products.heating) > 0:
                for current_node_index in range(0, len(HSC.products.heating)):
                    if "id" in HSC.products.heating[current_node_index]:
                        if HSC.products.heating[current_node_index]["id"] == node_id:
                            node_index = current_node_index
                            break

                if node_index != -1:
                    heating_mode_current = Pyhiveapi.Heating.get_mode(self, node_id)
                    heating_boost_current = Pyhiveapi.Heating.get_boost(self, node_id)

                    if heating_boost_current == "ON":
                        if "state" in HSC.products.heating[node_index] and "target" in HSC.products.heating[node_index]["state"]:
                            heating_target_temp_tmp = HSC.products.heating[node_index]["state"]["target"]
                            heating_target_temp_found = True
                    else:
                        if heating_mode_current == "SCHEDULE":
                            if 'props' in HSC.products.heating[node_index] and 'scheduleOverride' in HSC.products.heating[node_index]["props"]:
                                if HSC.products.heating[node_index]["props"]["scheduleOverride"]:
                                    if "state" in HSC.products.heating[node_index] and "target" in HSC.products.heating[node_index]["state"]:
                                        heating_target_temp_tmp = HSC.products.heating[node_index]["state"]["target"]
                                        heating_target_temp_found = True
                                else:
                                    snan = Pyhiveapi.p_get_schedule_now_next_later(
                                        HSC.products.heating[node_index]["state"]["schedule"])
                                    if 'now' in snan:
                                        if 'value' in snan["now"] and 'target' in snan["now"]["value"]:
                                            heating_target_temp_tmp = snan["now"]["value"]["target"]
                                            heating_target_temp_found = True
                        else:
                            if ("state" in HSC.products.heating[node_index] and "target"
                                    in HSC.products.heating[node_index]["state"]):
                                heating_target_temp_tmp = \
                                    HSC.products.heating[node_index]["state"]["target"]
                                heating_target_temp_found = True

            if heating_target_temp_found:
                NODE_ATTRIBS[current_node_attribute] = heating_target_temp_tmp
                heating_target_temp_return = heating_target_temp_tmp
            else:
                if current_node_attribute in NODE_ATTRIBS:
                    heating_target_temp_return = \
                        NODE_ATTRIBS.get(current_node_attribute)
                else:
                    heating_target_temp_return = 0

            return heating_target_temp_return

        def get_mode(self, node_id):
            """Get heating current mode."""
            node_index = -1

            mode_return = "UNKNOWN"
            mode_tmp = "UNKNOWN"
            mode_found = False

            current_node_attribute = "Heating_Mode_" + node_id

            if len(HSC.products.heating) > 0:
                for current_node_index in range(0, len(HSC.products.heating)):
                    if "id" in HSC.products.heating[current_node_index]:
                        if HSC.products.heating[current_node_index]["id"] == node_id:
                            node_index = current_node_index
                            break

                if node_index != -1:
                    if ("state" in HSC.products.heating[node_index] and
                            "mode" in HSC.products.heating[node_index]["state"]):
                        mode_tmp = HSC.products.heating[node_index]["state"]["mode"]
                        if mode_tmp == "BOOST":
                            if ("props" in HSC.products.heating[node_index] and
                                    "previous" in
                                    HSC.products.heating[node_index]["props"] and
                                    "mode" in
                                    HSC.products.heating[node_index]
                                    ["props"]["previous"]):
                                mode_tmp = (HSC.products.heating[node_index]
                                            ["props"]["previous"]["mode"])
                        mode_found = True

            if mode_found:
                NODE_ATTRIBS[current_node_attribute] = mode_tmp
                mode_return = mode_tmp
            else:
                if current_node_attribute in NODE_ATTRIBS:
                    mode_return = NODE_ATTRIBS.get(current_node_attribute)
                else:
                    mode_return = "UNKNOWN"

            return mode_return

        def get_state(self, node_id):
            """Get heating current state."""

            heating_state_return = "OFF"
            heating_state_tmp = "OFF"
            heating_state_found = False

            current_node_attribute = "Heating_State_" + node_id

            if len(HSC.products.heating) > 0:
                temperature_current = Pyhiveapi.Heating.current_temperature(self, node_id)
                temperature_target = Pyhiveapi.Heating.get_target_temperature(self, node_id)
                heating_boost = Pyhiveapi.Heating.get_boost(self, node_id)
                heating_mode = Pyhiveapi.Heating.get_mode(self, node_id)

                if (heating_mode == "SCHEDULE" or
                        heating_mode == "MANUAL" or
                        heating_boost == "ON"):
                    if temperature_current < temperature_target:
                        heating_state_tmp = "ON"
                        heating_state_found = True
                    else:
                        heating_state_tmp = "OFF"
                        heating_state_found = True
                else:
                    heating_state_tmp = "OFF"
                    heating_state_found = True

            if heating_state_found:
                NODE_ATTRIBS[current_node_attribute] = heating_state_tmp
                heating_state_return = heating_state_tmp
            else:
                if current_node_attribute in NODE_ATTRIBS:
                    heating_state_return = NODE_ATTRIBS.get(current_node_attribute)
                else:
                    heating_state_return = "UNKNOWN"

            return heating_state_return

        def get_boost(self, node_id):
            """Get heating boost current status."""
            node_index = -1

            heating_boost_return = "UNKNOWN"
            heating_boost_tmp = "UNKNOWN"
            heating_boost_found = False

            current_node_attribute = "Heating_Boost_" + node_id

            if len(HSC.products.heating) > 0:
                for current_node_index in range(0, len(HSC.products.heating)):
                    if "id" in HSC.products.heating[current_node_index]:
                        if HSC.products.heating[current_node_index]["id"] == node_id:
                            node_index = current_node_index
                            break

                if node_index != -1:
                    if ("state" in HSC.products.heating[node_index] and
                            "boost" in HSC.products.heating[node_index]["state"]):
                        heating_boost_tmp = (HSC.products.heating[node_index]
                                             ["state"]["boost"])
                        if heating_boost_tmp is None:
                            heating_boost_tmp = "OFF"
                        else:
                            heating_boost_tmp = "ON"
                        heating_boost_found = True

            if heating_boost_found:
                NODE_ATTRIBS[current_node_attribute] = heating_boost_tmp
                heating_boost_return = heating_boost_tmp
            else:
                if current_node_attribute in NODE_ATTRIBS:
                    heating_boost_return = NODE_ATTRIBS.get(current_node_attribute)
                else:
                    heating_boost_return = "UNKNOWN"

            return heating_boost_return

        def get_boost_time(self, node_id):
            """Get heating boost time remaining."""
            heating_boost = "UNKNOWN"

            if Pyhiveapi.Heating.get_boost(self, node_id) == "ON":
                node_index = -1

                heating_boost_tmp = "UNKNOWN"
                heating_boost_found = False

                if len(HSC.products.heating) > 0:
                    for current_node_index in range(0, len(HSC.products.heating)):
                        if "id" in HSC.products.heating[current_node_index]:
                            if HSC.products.heating[current_node_index]["id"] == node_id:
                                node_index = current_node_index
                                break

                    if node_index != -1:
                        if "state" in HSC.products.heating[node_index] and "boost" in HSC.products.heating[node_index]["state"]:
                            heating_boost_tmp = (HSC.products.heating[node_index]["state"]["boost"])
                            heating_boost_found = True

                if heating_boost_found:
                    heating_boost = heating_boost_tmp

            return heating_boost

        def get_operation_modes(self, node_id):
            """Get heating list of possible modes."""
            heating_operation_list = ["SCHEDULE", "MANUAL", "OFF"]
            return heating_operation_list

        def get_schedule_now_next_later(self, node_id):
            """Hive get heating schedule now, next and later."""
            heating_mode_current = Pyhiveapi.Heating.get_mode(self, node_id)

            snan = None

            if heating_mode_current == "SCHEDULE":
                node_index = -1

                if len(HSC.products.heating) > 0:
                    for current_node_index in range(0, len(HSC.products.heating)):
                        if "id" in HSC.products.heating[current_node_index]:
                            if HSC.products.heating[current_node_index]["id"] == node_id:
                                node_index = current_node_index
                                break

                if node_index != -1:
                    snan = Pyhiveapi.p_get_schedule_now_next_later(
                        HSC.products.heating[node_index]["state"]["schedule"])
                else:
                    snan = None
            else:
                snan = None

            return snan

        def set_target_temperature(self, node_id, new_temperature):
            """Set heating target temperature."""
            Pyhiveapi.check_hive_api_logon(self)

            set_temperature_success = False
            api_resp_d = {}
            api_resp = ""

            if HSC.session_id is not None:
                node_index = -1
                if len(HSC.products.heating) > 0:
                    for current_node_index in range(0, len(HSC.products.heating)):
                        if "id" in HSC.products.heating[current_node_index]:
                            if HSC.products.heating[current_node_index]["id"] == node_id:
                                node_index = current_node_index
                                break

                    if node_index != -1:
                        if "id" in HSC.products.heating[node_index]:
                            json_string_content = ('{"target":' + str(new_temperature) + '}')

                            hive_api_url = (HIVE_API.urls.nodes + "/heating/" + HSC.products.heating[node_index]["id"])
                            api_resp_d = Pyhiveapi.hive_api_json_call("POST", hive_api_url, json_string_content, False)

                            api_resp = api_resp_d['original']

                            if str(api_resp) == "<Response [200]>":
                                Pyhiveapi.hive_api_get_nodes(self, node_id)
                                set_temperature_success = True

            return set_temperature_success

        def set_mode(self, node_id, new_mode):
            """Set heating mode."""
            Pyhiveapi.check_hive_api_logon(self)

            set_mode_success = False
            api_resp_d = {}
            api_resp = ""

            if HSC.session_id is not None:
                node_index = -1
                if len(HSC.products.heating) > 0:
                    for current_node_index in range(0, len(HSC.products.heating)):
                        if "id" in HSC.products.heating[current_node_index]:
                            if HSC.products.heating[current_node_index]["id"] == node_id:
                                node_index = current_node_index
                                break

                    if node_index != -1:
                        if "id" in HSC.products.heating[node_index]:
                            if new_mode == "SCHEDULE":
                                json_string_content = '{"mode": "SCHEDULE"}'
                            elif new_mode == "MANUAL":
                                json_string_content = '{"mode": "MANUAL"}'
                            elif new_mode == "OFF":
                                json_string_content = '{"mode": "OFF"}'

                            if new_mode == "SCHEDULE" or new_mode == "MANUAL" or new_mode == "OFF":
                                hive_api_url = (HIVE_API.urls.nodes + "/heating/" + HSC.products.heating[node_index]["id"])
                                api_resp_d = Pyhiveapi.hive_api_json_call(
                                    "POST", hive_api_url, json_string_content, False)

                                api_resp = api_resp_d['original']

                                if str(api_resp) == "<Response [200]>":
                                    Pyhiveapi.hive_api_get_nodes(self, node_id)
                                    set_mode_success = True

            return set_mode_success

        def turn_boost_on(self, node_id, length_minutes, target_temperature):
            """Turn heating boost on."""
            set_boost_success = False
            heating_node_found = False
            api_resp_d = {}
            api_resp = ""

            if length_minutes > 0 and target_temperature >= self.min_temperature(node_id) and target_temperature <= self.max_temperature(node_id):
                heating_node_found = False
            else:
                return False

            for a_heating in HSC.products.heating:
                if "id" in a_heating:
                    if a_heating["id"] == node_id:
                        heating_node_found = True
                        break

            Pyhiveapi.check_hive_api_logon(self)

            if heating_node_found:
                json_string_content = '{"mode": "BOOST", "boost": ' + str(length_minutes) + ', "target": ' + str(target_temperature) + '}'
                hive_api_url = (HIVE_API.urls.nodes + "/heating/" + node_id)
                api_resp_d = Pyhiveapi.hive_api_json_call("POST", hive_api_url, json_string_content, False)

                api_resp = api_resp_d['original']

                if str(api_resp) == "<Response [200]>":
                    Pyhiveapi.hive_api_get_nodes(self, node_id)
                    set_boost_success = True

            return set_boost_success

        def turn_boost_off(self, node_id):
            """Turn heating boost off."""
            set_boost_success = False
            heating_node_found = False
            api_resp_d = {}
            api_resp = ""

            for a_heating in HSC.products.heating:
                if "id" in a_heating:
                    if a_heating["id"] == node_id:
                        heating_node_found = True
                        break

            Pyhiveapi.check_hive_api_logon(self)

            if heating_node_found:
                Pyhiveapi.hive_api_get_nodes(self, node_id)
                boost_state = self.get_boost(node_id)

                node_index = -1
                for current_node_index in range(0, len(HSC.products.heating)):
                    if "id" in HSC.products.heating[current_node_index]:
                        if HSC.products.heating[current_node_index]["id"] == node_id:
                            node_index = current_node_index
                            break

                if node_index != -1 and boost_state == "ON":
                    send_previous_mode = ''
                    send_previous_temperature = ''

                    if "props" in HSC.products.heating[node_index] and "previous" in HSC.products.heating[node_index]["props"] and "mode" in HSC.products.heating[node_index]["props"]["previous"]:
                        previous_mode = HSC.products.heating[node_index]["props"]["previous"]["mode"]
                        send_previous_mode = '"mode": "' + str(previous_mode) + '"'
                        if previous_mode == "MANUAL":
                            previous_temperature = HSC.products.heating[node_index]["props"]["previous"]["target"]
                            send_previous_temperature = ', "target": ' + str(previous_temperature)

                        json_string_content = '{' + send_previous_mode + send_previous_temperature + '}'
                        hive_api_url = (HIVE_API.urls.nodes + "/heating/" + node_id)
                        api_resp_d = Pyhiveapi.hive_api_json_call("POST", hive_api_url, json_string_content, False)

                        api_resp = api_resp_d['original']

                    if str(api_resp) == "<Response [200]>":
                        Pyhiveapi.hive_api_get_nodes(self, node_id)
                        set_boost_success = True

            return set_boost_success