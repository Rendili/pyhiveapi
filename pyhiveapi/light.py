"""Light Class Code."""

import colorsys
from .api import Hive
from .logging import Logger
from .data import Data as Dt
from .attributes import Attributes


class Light:
    """Home Assistant Hive Lights."""

    type = "Light"

    def __init__(self):
        """Initialise."""
        self.hive = Hive()
        self.log = Logger()
        self.attr = Attributes()
        self.tmp = None
        self.result = False
        self.resp = False

    def get_state(self, n):
        """Get light current state."""
        self.log.log('light', "Getting state of light: " + Dt.NAME[n])
        self.__init__()
        self.result = self.attr.online_offline(n)
        data = Dt.products[n]

        if self.result != 'offline':
            try:
                self.result = data["state"]["status"]
                Dt.NODES["Light_State_" + n] = self.result
            except KeyError:
                pass

        self.log.log('light', "State of light " + Dt.NAME[n] + " is: "
                     + self.result)
        return Dt.HIVETOHA[type].get(self.result,
                                     Dt.NODES.get("Light_State_" + n))

    def get_brightness(self, n):
        """Get light current brightness."""
        self.log.log('Light', "Getting brightness of light: " + Dt.NAME[n])
        self.__init__()
        data = Dt.products[n]

        try:
            self.tmp = data["state"]["brightness"]
            self.result = ((self.tmp / 100) * 255)
            Dt.NODES["Light_Bright_" + n] = self.result
        except KeyError:
            pass

        self.log.log("Light", "Brightness of light " + Dt.NAME[n] + " is: "
                     + str(self.result))

        return self.result if self.result is not None \
            else Dt.NODES.get("Light_Bright_" + n)

    def get_min_color_temp(self, n):
        """Get light minimum color temperature."""
        self.log.log("Light", "Getting min colour temperature of light: "
                     + Dt.NAME[n])
        self.__init__()
        data = Dt.products[n]

        try:
            self.tmp = data["props"]["colourTemperature"]["max"]
            self.result = round((1 / self.tmp) * 1000000)
            Dt.NODES["Light_Min_CT_" + n] = self.result
        except KeyError:
            pass

        self.log.log("Light", "Min Colour temperature of light " + Dt.NAME[n]
                     + " is: " + str(self.result))

        return self.result

    def get_max_color_temp(self, n):
        """Get light maximum color temperature."""
        self.log.log("Light", "Getting max colour temperature of light: "
                     + Dt.NAME[n])
        self.__init__()
        data = Dt.products[n]

        try:
            self.tmp = data["props"]["colourTemperature"]["min"]
            self.result = round((1 / self.tmp) * 1000000)
            Dt.NODES["Light_Max_CT_" + n] = self.result
        except KeyError:
            pass

        self.log.log("Light", "Max Colour temperature of light " + Dt.NAME[n]
                     + " is: " + str(self.result))

        return self.result

    def get_color_temp(self, n):
        """Get light current color temperature."""
        self.log.log("Light", "Getting colour temperature of light: "
                     + Dt.NAME[n])
        self.__init__()
        data = Dt.products[n]

        try:
            self.tmp = data["state"]["colourTemperature"]
            self.result = round((1 / self.tmp) * 1000000)
            Dt.NODES["Light_CT_" + n] = self.result
        except KeyError:
            pass

        self.log.log("Light", "Colour temperature of light " + Dt.NAME[n]
                     + " is: " + str(self.result))

        return self.result if self.result is not None \
            else Dt.NODES.get("Light_CT_" + n)

    def get_color(self, n):
        """Get light current colour"""
        self.log.log("Light", "Getting colour of light : " + Dt.NAME[n])
        self.__init__()
        data = Dt.products[n]

        try:
            self.tmp = [
                ((data["state"]["hue"]) / 360),
                ((data["state"]["saturation"]) / 100),
                ((data["state"]["value"]) / 100)]
            self.result = tuple(int(i * 255) for i in colorsys.hsv_to_rgb(
                self.tmp[0],
                self.tmp[1],
                self.tmp[2]))
            Dt.NODES["Light_Color_" + n] = self.result
        except KeyError:
            pass

        self.log.log("Light", "Colour of light " + Dt.NAME[n] + " is: "
                     + str(self.result))

        return self.result if self.result is not None \
            else Dt.NODES.get("Light_Color_" + n)

    def turn_off(self, n):
        """Set light to turn off."""
        from .pyhiveapi import Pyhiveapi
        self.log.log("Light", "Turning off light : " + Dt.NAME[n])
        self.__init__()
        Pyhiveapi.check_hive_api_logon(Pyhiveapi())
        data = Dt.products[n]

        self.resp = self.hive.set_state(Dt.s_session_id, data['type'], n)
        if str(self.resp['original']) == "<Response [200]>":
            self.result = True
            Pyhiveapi.hive_api_get_nodes(Pyhiveapi(), n, False)
            self.log.log("Light", "Light " + Dt.NAME[n]
                         + " has been sucessfully switched off")
        else:
            self.log.log("Light", "Failed to switch off light: " + Dt.NAME[n])

        return self.result

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
                    api_resp_d = Pyhiveapi.hive_api_json_call("POST",
                                                              hive_api_url,
                                                              json_string_content,
                                                              False)

                    api_resp = api_resp_d['original']

                if str(api_resp) == "<Response [200]>":
                    Pyhiveapi.hive_api_get_nodes(self, node_id)
                    set_mode_success = True
                    if HSC.logging.all or HSC.logging.light:
                        Pyhiveapi.logger(
                            "Light " + HSC.products.light[node_index]["state"][
                                "name"] +
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
                    api_resp_d = Pyhiveapi.hive_api_json_call("POST",
                                                              hive_api_url,
                                                              json_string_content,
                                                              False)

                    api_resp = api_resp_d['original']

                if str(api_resp) == "<Response [200]>":
                    Pyhiveapi.hive_api_get_nodes(self, node_id)
                    set_mode_success = True
                    if HSC.logging.all or HSC.logging.light:
                        Pyhiveapi.logger("Sucessfully set the brightness " +
                                         HSC.products.light[node_index][
                                             "state"]["name"] +
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
                        json_string_content = '{"colourTemperature": ' + str(
                            new_color_temp) + '}'
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
                        api_resp_d = Pyhiveapi.hive_api_json_call("POST",
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

                    api_resp_d = Pyhiveapi.hive_api_json_call("POST",
                                                              hive_api_url,
                                                              json_string_content,
                                                              False)

                    api_resp = api_resp_d['original']

                if str(api_resp) == "<Response [200]>":
                    Pyhiveapi.hive_api_get_nodes(self, node_id)
                    set_mode_success = True
                    if HSC.logging.all or HSC.logging.light:
                        Pyhiveapi.logger(
                            "Sucessfully set the colour temperature for " +
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
                    api_resp_d = Pyhiveapi.hive_api_json_call("POST",
                                                              hive_api_url,
                                                              json_string_content,
                                                              False)

                    api_resp = api_resp_d['original']

                if str(api_resp) == "<Response [200]>":
                    Pyhiveapi.hive_api_get_nodes(self, node_id)
                    set_mode_success = True
                    if HSC.logging.all or HSC.logging.light:
                        Pyhiveapi.logger("Sucessfully set the colour for " +
                                         HSC.products.light[node_index][
                                             "state"]["name"] +
                                         " to : {hue: " + str(new_hue) +
                                         ', "saturation": ' + str(
                            new_saturation) +
                                         ', "value": ' + str(new_value) + '}')

                return set_mode_success
