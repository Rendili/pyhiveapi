"""Light Class Code."""
import colorsys

from .api import Hive
from .attributes import Attributes
from .data import Data
from .logging import Logger


class Light:
    """Home Assistant Hive Lights."""

    def __init__(self):
        """Initialise."""
        self.hive = Hive()
        self.log = Logger()
        self.attr = Attributes()
        self.type = "Light"

    @staticmethod
    def data_list():
        return {"tmp": None, "end": False, "resp": False}

    def get_state(self, n):
        """Get light current state."""
        self.log.log('light', "Getting state of light: " + Data.NAME[n])
        dl = self.data_list()
        dl.update({"end": (self.attr.online_offline(n))})
        data = Data.products[n]

        if dl['end'] != 'offline':
            try:
                dl.update({"end": (data["state"]["status"])})
                Data.NODES["Light_State_" + n] = dl['end']
            except KeyError:
                self.log.log('switch', "Failed to get state - " + Data.NAME[n])

        self.log.log('light', "State of light " + Data.NAME[n] + " is: "
                     + dl['end'])
        return Data.HIVETOHA[self.type].get(dl['end'],
                                            Data.NODES.get("Light_State_" + n))

    def get_brightness(self, n):
        """Get light current brightness."""
        self.log.log('Light', "Getting brightness of light: " + Data.NAME[n])
        dl = self.data_list()
        data = Data.products[n]

        try:
            dl.update({"tmp": (data["state"]["brightness"])})
            dl.update(dict(end=((dl['tmp'] / 100) * 255)))
            Data.NODES["Light_Bright_" + n] = dl['end']
        except KeyError:
            pass

        self.log.log("Light", "Brightness of light " + Data.NAME[n] + " is: "
                     + str(dl['end']))

        return dl['end'] if dl['end'] is False \
            else Data.NODES.get("Light_Bright_" + n)

    def get_min_color_temp(self, n):
        """Get light minimum color temperature."""
        self.log.log("Light", "Getting min colour temperature of light: "
                     + Data.NAME[n])
        dl = self.data_list()
        data = Data.products[n]

        try:
            dl.update({"tmp": (data["props"]["colourTemperature"]["max"])})
            dl.update(dict(end=(round((1 / dl['tmp']) * 1000000))))
            Data.NODES["Light_Min_CT_" + n] = dl['end']
        except KeyError:
            pass

        self.log.log("Light", "Min Colour temperature of light " + Data.NAME[n]
                     + " is: " + str(dl['end']))

        return dl['end']

    def get_max_color_temp(self, n):
        """Get light maximum color temperature."""
        self.log.log("Light", "Getting max colour temperature of light: "
                     + Data.NAME[n])
        dl = self.data_list()
        data = Data.products[n]

        try:
            dl.update({"tmp": (data["props"]["colourTemperature"]["min"])})
            dl.update(dict(end=(round((1 / dl['tmp']) * 1000000))))
            Data.NODES["Light_Max_CT_" + n] = dl['end']
        except KeyError:
            pass

        self.log.log("Light", "Max Colour temperature of light " + Data.NAME[n]
                     + " is: " + str(dl['end']))

        return dl['end']

    def get_color_temp(self, n):
        """Get light current color temperature."""
        self.log.log("Light", "Getting colour temperature of light: "
                     + Data.NAME[n])
        dl = self.data_list()
        data = Data.products[n]

        try:
            dl.update({"tmp": (data["state"]["colourTemperature"])})
            dl.update(dict(end=(round((1 / dl['tmp']) * 1000000))))
            Data.NODES["Light_CT_" + n] = dl['end']
        except KeyError:
            pass

        self.log.log("Light", "Colour temperature of light " + Data.NAME[n]
                     + " is: " + str(dl['end']))

        return dl['end'] if dl['end'] is False \
            else Data.NODES.get("Light_CT_" + n)

    def get_color(self, n):
        """Get light current colour"""
        self.log.log("Light", "Getting colour of light : " + Data.NAME[n])
        dl = self.data_list()
        data = Data.products[n]

        try:
            dl.update(dict(tmp=(
                ((data["state"]["hue"]) / 360),
                ((data["state"]["saturation"]) / 100),
                ((data["state"]["value"]) / 100))))
            dl.update(
                dict(end=(tuple(int(i * 255) for i in colorsys.hsv_to_rgb(
                    dl['tmp'][0],
                    dl['tmp'][1],
                    dl['tmp'][2])))))
            Data.NODES["Light_Color_" + n] = dl['end']
        except KeyError:
            pass

        self.log.log("Light", "Colour of light " + Data.NAME[n] + " is: "
                     + str(dl['end']))

        return dl['end'] if dl['end'] is False \
            else Data.NODES.get("Light_Color_" + n)

    def turn_off(self, n):
        """Set light to turn off."""
        from .pyhiveapi import Pyhiveapi
        self.log.log("Light", "Turning off light : " + Data.NAME[n])
        dl = self.data_list()
        Pyhiveapi.check_hive_api_logon(Pyhiveapi())
        data = Data.products[n]

        dl.update({'resp': (self.hive.set_state(Data.sess_id, data['type'],
                                                n, "OFF"))})
        if str(dl['resp']['original']) == "<Response [200]>":
            dl.update({'end': True})
            Pyhiveapi.hive_api_get_nodes(Pyhiveapi(), n, False)
            self.log.log("Light", "Light " + Data.NAME[n]
                         + " has been successfully switched off")
        else:
            self.log.log("Light", "Failed to switch off - " + Data.NAME[n])

        return dl['end']

    def turn_on(self, n, brightness, color_temp, color):
        """Set light to turn on."""
        from .pyhiveapi import Pyhiveapi
        self.log.log("Light", "Turning on light : " + Data.NAME[n])
        dl = self.data_list()
        Pyhiveapi.check_hive_api_logon(Pyhiveapi())
        data = Data.products[n]

        if brightness is not None:
            self.set_brightness(n, brightness)
        if color_temp is not None:
            self.set_color_temp(n, color_temp)
        if color is not None:
            self.set_color(n, color)

        dl.update({'resp': (self.hive.set_state(Data.sess_id, data['type'],
                                                n, 'ON'))})
        if str(dl['resp']['original']) == "<Response [200]>":
            dl.update({'end': True})
            Pyhiveapi.hive_api_get_nodes(Pyhiveapi(), n, False)
            self.log.log("Light", "Light " + Data.NAME[n]
                         + " has been successfully switched on")
        else:
            self.log.log("Light", "Failed to switch on light: " + Data.NAME[n])

        return dl['end']

    def set_brightness(self, n, brightness):
        """Set brightness of the light."""
        from .pyhiveapi import Pyhiveapi
        self.log.log("Light", "Setting brightness of : " + Data.NAME[n])
        dl = self.data_list()
        Pyhiveapi.check_hive_api_logon(Pyhiveapi())
        data = Data.products[n]

        dl.update({'resp': (self.hive.set_brightness(Data.sess_id,
                                                     data['type'], n,
                                                     brightness))})
        if str(dl['resp']['original']) == "<Response [200]>":
            dl['end'] = True
            Pyhiveapi.hive_api_get_nodes(Pyhiveapi(), n, False)
            self.log.log("Light", "successfully set the brightness of " +
                         Data.NAME[n] + " to : " + str(brightness))
        else:
            self.log.log("Light", "Failed to set brightness for light: " +
                         Data.NAME[n])

        return dl['end']

    def set_color_temp(self, n, color_temp):
        """Set light to turn on."""
        from .pyhiveapi import Pyhiveapi
        self.log.log("Light", "Setting color temp of : " + Data.NAME[n])
        dl = self.data_list()
        Pyhiveapi.check_hive_api_logon(Pyhiveapi())
        data = Data.products[n]

        if data['type'] == "tuneablelight":
            dl.update({'resp': (self.hive.set_color_temp(Data.sess_id,
                                                         data['type'], n,
                                                         color_temp))})
        else:
            self.hive.set_color(Data.sess_id, data['type'], n,
                                '48', '70', '96')
            dl.update({'resp': (self.hive.set_color_temp(Data.sess_id,
                                                         data['type'], n,
                                                         color_temp))})

        if str(dl['resp']['original']) == "<Response [200]>":
            dl.update({'end': True})
            Pyhiveapi.hive_api_get_nodes(Pyhiveapi(), n, False)
            self.log.log("Light", "successfully set the color temp of " +
                         Data.NAME[n] + " to : " + str(color_temp))
        else:
            self.log.log("Light", "Failed to set color temp for light: " +
                         Data.NAME[n])

        return dl['end']

    def set_color(self, n, new_color):
        """Set light to turn on."""
        from .pyhiveapi import Pyhiveapi
        self.log.log("Light", "Setting color of : " + Data.NAME[n])
        dl = self.data_list()
        Pyhiveapi.check_hive_api_logon(Pyhiveapi())
        data = Data.products[n]

        dl.update({'resp': (self.hive.set_color(Data.sess_id, data['type'], n,
                                                str(new_color[0]),
                                                str(new_color[1]),
                                                str(new_color[2])))})
        if str(dl['resp']['original']) == "<Response [200]>":
            dl.update({'end': True})
            Pyhiveapi.hive_api_get_nodes(Pyhiveapi(), n, False)
            self.log.log("Light", "successfully set the color for " +
                         Data.NAME[n] + ' to : {hue: "' + str(new_color[0]) +
                         ', "saturation": ' + str(new_color[1]) +
                         ', "value": ' + str(new_color[2]) + '}')
        else:
            self.log.log("Light", "Failed to set color for light: " +
                         Data.NAME[n])

        return dl['end']
