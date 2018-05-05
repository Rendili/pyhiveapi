
from .pyhiveapi import Pyhiveapi


class Light():
        """Hive Lights."""

        def get_state(self, node_id):
            """Get light current state."""
            if HSC.logging.all or HSC.logging.light:
                Pyhiveapi.logger("Getting state of light : " + node_id)
            result = Pyhiveapi.Attributes.online_offline(self, node_id)
            node_index = -1

            light_state_return = "UNKNOWN"
            light_state_tmp = "UNKNOWN"
            light_state_found = False

            current_node_attribute = "Light_State_" + node_id

            if len(HSC.products.light) > 0:
                for current_node_index in range(0, len(HSC.products.light)):
                    if "id" in HSC.products.light[current_node_index]:
                        if HSC.products.light[current_node_index][
                            "id"] == node_id:
                            node_index = current_node_index
                            break

                if node_index != -1:
                    if ("state" in HSC.products.light[
                        node_index] and "status" in
                        HSC.products.light[node_index]["state"]):
                        light_state_tmp = (HSC.products.light[node_index]
                                           ["state"]["status"])
                        light_state_found = True

            if result == "offline":
                light_state_return = "OFF"
            elif light_state_found:
                NODE_ATTRIBS[current_node_attribute] = light_state_tmp
                light_state_return = light_state_tmp
            else:
                if current_node_attribute in NODE_ATTRIBS:
                    light_state_return = NODE_ATTRIBS.get(
                        current_node_attribute)
                else:
                    light_state_return = "UNKNOWN"

            light_state_return_b = False

            if light_state_return == "ON":
                light_state_return_b = True

            if HSC.logging.all or HSC.logging.light:
                Pyhiveapi.logger("State of light "  +
                                 HSC.products.light[node_index]["state"]["name"] +
                                 " is : " + light_state_return)

            return light_state_return_b

        def get_brightness(self, node_id):
            """Get light current brightness."""
            if HSC.logging.all or HSC.logging.light:
                Pyhiveapi.logger("Getting brightness of light : " + node_id)
            node_index = -1

            tmp_brightness_return = 0
            light_brightness_return = 0
            light_brightness_tmp = 0
            light_brightness_found = False

            current_node_attribute = "Light_Brightness_" + node_id

            if len(HSC.products.light) > 0:
                for current_node_index in range(0, len(HSC.products.light)):
                    if "id" in HSC.products.light[current_node_index]:
                        if HSC.products.light[current_node_index][
                            "id"] == node_id:
                            node_index = current_node_index
                            break

                if node_index != -1:
                    if ("state" in HSC.products.light[
                        node_index] and "brightness" in
                        HSC.products.light[node_index]["state"]):
                        light_brightness_tmp = (HSC.products.light[node_index]
                                                ["state"]["brightness"])
                        light_brightness_found = True

            if light_brightness_found:
                NODE_ATTRIBS[current_node_attribute] = light_brightness_tmp
                tmp_brightness_return = light_brightness_tmp
                light_brightness_return = ((tmp_brightness_return / 100) * 255)
            else:
                if current_node_attribute in NODE_ATTRIBS:
                    tmp_brightness_return = NODE_ATTRIBS.get(
                        current_node_attribute)
                    light_brightness_return = (
                    (int(tmp_brightness_return) / 100) * 255)
                else:
                    light_brightness_return = 0

            if HSC.logging.all or HSC.logging.light:
                Pyhiveapi.logger("Brightness of light "  +
                                 HSC.products.light[node_index]["state"]["name"] +
                                 " is : " + str(light_brightness_return))

            return light_brightness_return

        def get_min_color_temp(self, node_id):
            """Get light minimum color temperature."""
            if HSC.logging.all or HSC.logging.light:
                Pyhiveapi.logger("Getting min colour temperature of light : " +
                                 node_id)
            node_index = -1

            light_min_color_temp_tmp = 0
            light_min_color_temp_return = 0
            light_min_color_temp_found = False

            node_attrib = "Light_Min_color_Temp_" + node_id

            if len(HSC.products.light) > 0:
                for current_node_index in range(0, len(HSC.products.light)):
                    if "id" in HSC.products.light[current_node_index]:
                        if HSC.products.light[current_node_index][
                            "id"] == node_id:
                            node_index = current_node_index
                            break

                if node_index != -1:
                    if ("props" in HSC.products.light[node_index] and
                                "colourTemperature" in
                                HSC.products.light[node_index][
                                    "props"] and "max" in
                        HSC.products.light[node_index]
                        ["props"]["colourTemperature"]):
                        light_min_color_temp_tmp = (
                        HSC.products.light[node_index]
                        ["props"]
                        ["colourTemperature"]["max"])
                        light_min_color_temp_found = True

            if light_min_color_temp_found:
                NODE_ATTRIBS[node_attrib] = light_min_color_temp_tmp
                light_min_color_temp_return = round(
                    (1 / light_min_color_temp_tmp)
                    * 1000000)
            else:
                if node_attrib in NODE_ATTRIBS:
                    light_min_color_temp_return = (
                    NODE_ATTRIBS.get(node_attrib))
                else:
                    light_min_color_temp_return = 0

            if HSC.logging.all or HSC.logging.light:
                Pyhiveapi.logger("Min Colour temperature of light "  +
                                 HSC.products.light[node_index]["state"]["name"] +
                                 " is : " + str(light_min_color_temp_return))

            return light_min_color_temp_return

        def get_max_color_temp(self, node_id):
            """Get light maximum color temperature."""
            if HSC.logging.all or HSC.logging.light:
                Pyhiveapi.logger("Getting max colour temperature of light : " +
                                 node_id)
            node_index = -1

            light_max_color_temp_tmp = 0
            light_max_color_temp_return = 0
            light_max_color_temp_found = False

            node_attrib = "Light_Max_color_Temp_" + node_id

            if len(HSC.products.light) > 0:
                for current_node_index in range(0, len(HSC.products.light)):
                    if "id" in HSC.products.light[current_node_index]:
                        if HSC.products.light[current_node_index][
                            "id"] == node_id:
                            node_index = current_node_index
                            break

                if node_index != -1:
                    if ("props" in HSC.products.light[node_index] and
                                "colourTemperature" in
                                HSC.products.light[node_index]["props"] and
                                "min" in
                                HSC.products.light[node_index]["props"]
                                ["colourTemperature"]):
                        light_max_color_temp_tmp = (
                        HSC.products.light[node_index]
                        ["props"]["colourTemperature"]
                        ["min"])
                        light_max_color_temp_found = True

            if light_max_color_temp_found:
                NODE_ATTRIBS[node_attrib] = light_max_color_temp_tmp
                light_max_color_temp_return = round(
                    (1 / light_max_color_temp_tmp)
                    * 1000000)
            else:
                if node_attrib in NODE_ATTRIBS:
                    light_max_color_temp_return = NODE_ATTRIBS.get(node_attrib)
                else:
                    light_max_color_temp_return = 0

            if HSC.logging.all or HSC.logging.light:
                Pyhiveapi.logger("Max Colour temperature of light "  +
                                 HSC.products.light[node_index]["state"]["name"] +
                                 " is : " + str(light_max_color_temp_return))

            return light_max_color_temp_return

        def get_color_temp(self, node_id):
            """Get light current color temperature."""
            if HSC.logging.all or HSC.logging.light:
                Pyhiveapi.logger("Getting colour temperature of light : " +
                                 node_id)
            node_index = -1

            light_color_temp_tmp = 0
            light_color_temp_return = 0
            light_color_temp_found = False

            current_node_attribute = "Light_Color_Temp_" + node_id

            if len(HSC.products.light) > 0:
                for current_node_index in range(0, len(HSC.products.light)):
                    if "id" in HSC.products.light[current_node_index]:
                        if HSC.products.light[current_node_index][
                            "id"] == node_id:
                            node_index = current_node_index
                            break

                if node_index != -1:
                    if ("state" in HSC.products.light[node_index] and
                                "colourTemperature" in
                                HSC.products.light[node_index]["state"]):
                        light_color_temp_tmp = (HSC.products.light[node_index]
                                                ["state"]["colourTemperature"])
                        light_color_temp_found = True

            if light_color_temp_found:
                NODE_ATTRIBS[current_node_attribute] = light_color_temp_tmp
                light_color_temp_return = round(
                    (1 / light_color_temp_tmp) * 1000000)
            else:
                if current_node_attribute in NODE_ATTRIBS:
                    light_color_temp_return = NODE_ATTRIBS.get(
                        current_node_attribute)
                else:
                    light_color_temp_return = 0

            if HSC.logging.all or HSC.logging.light:
                Pyhiveapi.logger("Colour temperature of light "  +
                                 HSC.products.light[node_index]["state"]["name"] +
                                 " is : " + str(light_color_temp_return))

            return light_color_temp_return

        def get_color(self, node_id):
            """Get color"""
            if HSC.logging.all or HSC.logging.light:
                Pyhiveapi.logger("Getting colour of light : " + node_id)
            node_index = -1

            light_color_hue_tmp = 0
            light_color_saturation_tmp = 0
            light_color_value_tmp = 0
            rgb = 0
            light_color_return = 0
            light_color_found = False

            current_node_attribute = "Light_Color_" + node_id

            if len(HSC.products.light) > 0:
                for current_node_index in range(0, len(HSC.products.light)):
                    if "id" in HSC.products.light[current_node_index]:
                        if HSC.products.light[current_node_index][
                            "id"] == node_id:
                            node_index = current_node_index
                            break

                if node_index != -1:
                    light_color_hue_tmp = (HSC.products.light[node_index]["state"]["hue"])
                    light_color_saturation_tmp = (HSC.products.light[node_index]["state"]["saturation"])
                    light_color_value_tmp = (HSC.products.light[node_index]["state"]["value"])
                    light_color_found = True

            if light_color_found:
                h = light_color_hue_tmp / 360
                s = light_color_saturation_tmp / 100
                v = light_color_value_tmp / 100
                rgb = tuple(int(i * 255) for i in colorsys.hsv_to_rgb(h, s, v))
                NODE_ATTRIBS[current_node_attribute] = rgb
                light_color_return = rgb
            else:
                if current_node_attribute in NODE_ATTRIBS:
                    light_color_return = NODE_ATTRIBS.get(
                        current_node_attribute)
                else:
                    light_color_return = 0

            if HSC.logging.all or HSC.logging.light:
                Pyhiveapi.logger("Colour of light " + HSC.products.light[node_index]["state"]["name"] +
                                 " is : " + str(light_color_return))

            return light_color_return

        def turn_off(self, node_id):
            """Set light to turn off."""
            if HSC.logging.all or HSC.logging.light:
                Pyhiveapi.logger("Turning off light : " + node_id)
            Pyhiveapi.check_hive_api_logon(self)

            node_index = -1

            set_mode_success = False
            api_resp_d = {}
            api_resp = ""

            if HSC.session_id is not None:
                if len(HSC.products.light) > 0:
                    for current_node_index in range(0,
                                                    len(HSC.products.light)):
                        if "id" in HSC.products.light[current_node_index]:
                            if (HSC.products.light[current_node_index]
                                ["id"] == node_id):
                                node_index = current_node_index
                                break
                    if node_index != -1:
                        json_string_content = '{"status": "OFF"}'
                        hive_api_url = (HIVE_API.urls.nodes
                                        + '/'
                                        + HSC.products.light[node_index]["type"]
                                        + '/'
                                        + HSC.products.light[node_index]["id"])
                        api_resp_d = Pyhiveapi.hive_api_json_call(self, "POST",
                                                        hive_api_url,
                                                        json_string_content,
                                                        False)

                        api_resp = api_resp_d['original']

                        if str(api_resp) == "<Response [200]>":
                            Pyhiveapi.hive_api_get_nodes(self, node_id)
                            set_mode_success = True
                            if HSC.logging.all or HSC.logging.light:
                                Pyhiveapi.logger("Light " + HSC.products.light[node_index]["state"]["name"] +
                                                 " has been sucessfully switched off")

            return set_mode_success

        def turn_on(self, node_id, nodedevicetype, new_brightness,
                    new_color_temp, new_color):
            """Set light to turn on."""
            if HSC.logging.all or HSC.logging.light:
                Pyhiveapi.logger("Turning on light : " + node_id)
            Pyhiveapi.check_hive_api_logon(self)

            if new_brightness is not None:
                Pyhiveapi.Light.set_brightness(self, node_id, new_brightness)
            if new_color_temp is not None:
                Pyhiveapi.Light.set_color_temp(self, node_id, nodedevicetype,
                                               new_color_temp)
            if new_color is not None:
                Pyhiveapi.Light.set_color(self, node_id, new_color)

            node_index = -1

            set_mode_success = False
            api_resp_d = {}
            api_resp = ""

            if HSC.session_id is not None:
                if len(HSC.products.light) > 0:
                    for cni in range(0, len(HSC.products.light)):
                        if "id" in HSC.products.light[cni]:
                            if HSC.products.light[cni]["id"] == node_id:
                                node_index = cni
                                break
                    if node_index != -1:
                        json_string_content = '{"status": "ON"}'
                        hive_api_url = (HIVE_API.urls.nodes
                                        + '/' + HSC.products.light[node_index][
                                            "type"]
                                        + '/' + HSC.products.light[node_index][
                                            "id"])
                        api_resp_d = Pyhiveapi.hive_api_json_call(self, "POST",
                                                        hive_api_url,
                                                        json_string_content,
                                                        False)

                        api_resp = api_resp_d['original']

                    if str(api_resp) == "<Response [200]>":
                        Pyhiveapi.hive_api_get_nodes(self, node_id)
                        set_mode_success = True
                        if HSC.logging.all or HSC.logging.light:
                            Pyhiveapi.logger("Light " + HSC.products.light[node_index]["state"]["name"] +
                                             " has been sucessfully switched on")

            return set_mode_success

        def set_brightness(self, node_id, new_brightness):
            """Set light to turn on."""
            if HSC.logging.all or HSC.logging.light:
                Pyhiveapi.logger("Setting brightness of : " + node_id)
            Pyhiveapi.check_hive_api_logon(self)

            node_index = -1

            set_mode_success = False
            api_resp_d = {}
            api_resp = ""

            if HSC.session_id is not None:
                if len(HSC.products.light) > 0:
                    for cni in range(0, len(HSC.products.light)):
                        if "id" in HSC.products.light[cni]:
                            if HSC.products.light[cni]["id"] == node_id:
                                node_index = cni
                                break
                    if node_index != -1:
                        json_string_content = \
                            ('{"status": "ON", "brightness": '
                            + str(new_brightness)
                            + '}')
                        hive_api_url = (HIVE_API.urls.nodes
                                        + '/' + HSC.products.light[node_index][
                                            "type"]
                                        + '/' + HSC.products.light[node_index][
                                            "id"])
                        api_resp_d = Pyhiveapi.hive_api_json_call(self, "POST",
                                                        hive_api_url,
                                                        json_string_content,
                                                        False)

                        api_resp = api_resp_d['original']

                    if str(api_resp) == "<Response [200]>":
                        Pyhiveapi.hive_api_get_nodes(self, node_id)
                        set_mode_success = True
                        if HSC.logging.all or HSC.logging.light:
                            Pyhiveapi.logger("Sucessfully set the brightness " +
                                             HSC.products.light[node_index]["state"]["name"] +
                                             " to : " + str(new_brightness))

            return set_mode_success

        def set_color_temp(self, node_id, nodedevicetype, new_color_temp):
            """Set light to turn on."""
            if HSC.logging.all or HSC.logging.light:
                Pyhiveapi.logger("Setting colour temperature of : " + node_id)
            Pyhiveapi.check_hive_api_logon(self)

            node_index = -1

            set_mode_success = False
            api_resp_d = {}
            api_resp = ""

            if HSC.session_id is not None:
                if len(HSC.products.light) > 0:
                    for cni in range(0, len(HSC.products.light)):
                        if "id" in HSC.products.light[cni]:
                            if HSC.products.light[cni]["id"] == node_id:
                                node_index = cni
                                break
                    if node_index != -1:
                        if nodedevicetype == "tuneablelight":
                            json_string_content = '{"colourTemperature": ' + str(new_color_temp) + '}'
                        else:
                            json_string_content = '{"colourMode": "COLOUR", ' \
                                                  '"hue": "48", ' \
                                                  '"saturation": "70", ' \
                                                  '"value": "96"}'
                            hive_api_url = (HIVE_API.urls.nodes
                                            + '/' +
                                            HSC.products.light[node_index][
                                                "type"]
                                            + '/' +
                                            HSC.products.light[node_index][
                                                "id"])
                            api_resp_d = Pyhiveapi.hive_api_json_call(self,
                                                                      "POST",
                                                                      hive_api_url,
                                                                      json_string_content,
                                                                      False)

                            json_string_content = '{"colourMode": "WHITE", "colourTemperature": ' + str(
                                new_color_temp) + '}'
                        hive_api_url = (HIVE_API.urls.nodes
                                        + '/' + HSC.products.light[node_index][
                                            "type"]
                                        + '/' + HSC.products.light[node_index][
                                            "id"])

                        api_resp_d = Pyhiveapi.hive_api_json_call(self, "POST",
                                                        hive_api_url,
                                                        json_string_content,
                                                        False)

                        api_resp = api_resp_d['original']

                    if str(api_resp) == "<Response [200]>":
                        Pyhiveapi.hive_api_get_nodes(self, node_id)
                        set_mode_success = True
                        if HSC.logging.all or HSC.logging.light:
                            Pyhiveapi.logger("Sucessfully set the colour temperature for " +
                                             HSC.products.light[node_index]["state"]["name"] +
                                             " to : " + str(new_color_temp))

            return set_mode_success

        def set_color(self, node_id, new_color):
            """Set light to turn on."""
            if HSC.logging.all or HSC.logging.light:
                Pyhiveapi.logger("Setting colour of : " + node_id)
            Pyhiveapi.check_hive_api_logon(self)

            node_index = -1

            set_mode_success = False
            api_resp_d = {}
            api_resp = ""
            new_hue = None
            new_saturation = None
            new_value = None

            if HSC.session_id is not None:
                if len(HSC.products.light) > 0:
                    for cni in range(0, len(HSC.products.light)):
                        if "id" in HSC.products.light[cni]:
                            if HSC.products.light[cni]["id"] == node_id:
                                node_index = cni
                                break
                    if node_index != -1:
                        new_hue = new_color[0]
                        new_saturation = new_color[1]
                        new_value = new_color[2]
                        json_string_content = '{"colourMode": "COLOUR", "hue": ' + str(
                            new_hue) + ', "saturation": ' + str(
                            new_saturation) + ', "value": ' + str(
                            new_value) + '}'
                        hive_api_url = (HIVE_API.urls.nodes
                                        + '/' + HSC.products.light[node_index][
                                            "type"]
                                        + '/' + HSC.products.light[node_index][
                                            "id"])
                        api_resp_d = Pyhiveapi.hive_api_json_call(self, "POST",
                                                                  hive_api_url,
                                                                  json_string_content,
                                                                  False)

                        api_resp = api_resp_d['original']

                    if str(api_resp) == "<Response [200]>":
                        Pyhiveapi.hive_api_get_nodes(self, node_id)
                        set_mode_success = True
                        if HSC.logging.all or HSC.logging.light:
                            Pyhiveapi.logger("Sucessfully set the colour for " +
                                             HSC.products.light[node_index]["state"]["name"] +
                                             " to : {hue: " + str(new_hue) +
                                             ', "saturation": ' + str(new_saturation) +
                                             ', "value": ' + str(new_value) + '}')

                    return set_mode_success