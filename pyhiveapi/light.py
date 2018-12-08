"""Hive Light Module."""
import colorsys

from pyhiveapi.custom_logging import Logger
from pyhiveapi.device_attributes import Attributes
from pyhiveapi.hive_api import Hive
from pyhiveapi.hive_data import Data


class Light:
    """Hive Light Code."""
    def __init__(self):
        """Initialise."""
        self.hive = Hive()
        self.log = Logger()
        self.attr = Attributes()
        self.type = "Light"

    def get_state(self, n):
        """Get light current state."""
        self.log.log('light', "Getting state of light: " + Data.NAME[n])
        end = self.attr.online_offline(n)

        if end != 'offline' and n in Data.products:
            data = Data.products[n]
            end = data["state"]["status"]
            Data.NODES["Light_State_" + n] = end
        else:
            self.log.log('switch', "Failed to get state - " + Data.NAME[n])

        self.log.log('light', "State of light " + Data.NAME[n] + " is: " + end)
        return Data.HIVETOHA[self.type].get(end,
                                            Data.NODES.get("Light_State_" + n))

    def get_brightness(self, n):
        """Get light current brightness."""
        self.log.log('Light', "Getting brightness of light: " + Data.NAME[n])
        tmp = None
        end = False

        if n in Data.products:
            data = Data.products[n]
            tmp = data["state"]["brightness"]
            end = ((tmp / 100) * 255)
            Data.NODES["Light_Bright_" + n] = end
            self.log.log("Light", "Brightness of light " + Data.NAME[n] +
                         " is: " + str(end))

        return end if end is False else Data.NODES.get("Light_Bright_" + n)

    def get_min_color_temp(self, n):
        """Get light minimum color temperature."""
        self.log.log("Light", "Getting min colour temperature of light: " +
                     Data.NAME[n])
        tmp = None
        end = None

        if n in Data.products:
            data = Data.products[n]
            tmp = data["props"]["colourTemperature"]["max"]
            end = round((1 / tmp) * 1000000)
            Data.NODES["Light_Min_CT_" + n] = end['end']

        self.log.log("Light", "Min Colour temperature of light " +
                     Data.NAME[n] + " is: " + str(end['end']))

        return end

    def get_max_color_temp(self, n):
        """Get light maximum color temperature."""
        self.log.log("Light", "Getting max colour temperature of light: " +
                     Data.NAME[n])
        tmp = 0
        end = None

        if n in Data.products:
            data = Data.products[n]
            tmp = data["props"]["colourTemperature"]["min"]
            end = round((1 / tmp) * 1000000)
            Data.NODES["Light_Max_CT_" + n] = end

        self.log.log("Light", "Max Colour temperature of light " +
                     Data.NAME[n] + " is: " + str(end))

        return end

    def get_color_temp(self, n):
        """Get light current color temperature."""
        self.log.log("Light", "Getting colour temperature of light: " +
                     Data.NAME[n])
        tmp = 0
        end = None

        if n in Data.products:
            data = Data.products[n]
            tmp = data["state"]["colourTemperature"]
            end = round((1 / tmp) * 1000000)
            Data.NODES["Light_CT_" + n] = end

        self.log.log("Light", "Colour temperature of light " +
                     Data.NAME[n] + " is: " + str(end))

        return end if end is None else Data.NODES.get("Light_CT_" + n)

    def get_color(self, n):
        """Get light current colour"""
        self.log.log("Light", "Getting colour of light : " + Data.NAME[n])
        tmp = []
        end = None

        if n in Data.products:
            data = Data.products[n]
            tmp = dict(
                ((data["state"]["hue"]) / 360),
                ((data["state"]["saturation"]) / 100),
                ((data["state"]["value"]) / 100))
            end = tuple(int(i * 255) for i in colorsys.hsv_to_rgb(
                    tmp[0],
                    tmp[1],
                    tmp[2]))
            Data.NODES["Light_Color_" + n] = end

        self.log.log("Light", "Colour of light " + Data.NAME[n] + " is: " +
                     str(end))

        return end if end is None else Data.NODES.get("Light_Color_" + n)

    def turn_off(self, n):
        """Set light to turn off."""
        from .hive_session import Session
        self.log.log("Light", "Turning off light : " + Data.NAME[n])
        resp = None
        end = False
        Session.check_hive_api_logon(Session())
        data = Data.products[n]

        resp = self.hive.set_state(Data.sess_id, data['type'], n, "OFF")
        if str(resp['original']) == "<Response [200]>":
            end = True
            Session.hive_api_get_nodes(Session(), n, False)
            self.log.log("Light", "Light " + Data.NAME[n] +
                         " has been successfully switched off")
        else:
            self.log.log("Light", "Failed to switch off - " + Data.NAME[n])

        return end

    def turn_on(self, n, brightness, color_temp, color):
        """Set light to turn on."""
        from .hive_session import Session
        self.log.log("Light", "Turning on light : " + Data.NAME[n])
        resp = None
        end = False
        Session.check_hive_api_logon(Session())
        data = Data.products[n]

        if brightness is not None:
            self.set_brightness(n, brightness)
        if color_temp is not None:
            self.set_color_temp(n, color_temp)
        if color is not None:
            self.set_color(n, color)

        resp = self.hive.set_state(Data.sess_id, data['type'], n, 'ON')
        if str(resp['original']) == "<Response [200]>":
            end = True
            Session.hive_api_get_nodes(Session(), n, False)
            self.log.log("Light", "Light " + Data.NAME[n] +
                         " has been successfully switched on")
        else:
            self.log.log("Light", "Failed to switch on light: " + Data.NAME[n])

        return end

    def set_brightness(self, n, brightness):
        """Set brightness of the light."""
        from .hive_session import Session
        self.log.log("Light", "Setting brightness of : " + Data.NAME[n])
        resp = None
        end = False
        Session.check_hive_api_logon(Session())
        data = Data.products[n]

        resp = self.hive.set_brightness(
            Data.sess_id, data['type'], n, brightness)
        if str(resp['original']) == "<Response [200]>":
            end = True
            Session.hive_api_get_nodes(Session(), n, False)
            self.log.log("Light", "successfully set the brightness of " +
                         Data.NAME[n] + " to : " + str(brightness))
        else:
            self.log.log("Light", "Failed to set brightness for light: " +
                         Data.NAME[n])

        return end

    def set_color_temp(self, n, color_temp):
        """Set light to turn on."""
        from .hive_session import Session
        self.log.log("Light", "Setting color temp of : " + Data.NAME[n])
        resp = None
        end = False
        Session.check_hive_api_logon(Session())
        data = Data.products[n]

        if data['type'] == "tuneablelight":
            resp = self.hive.set_color_temp(
                Data.sess_id, data['type'], n, color_temp)
        else:
            self.hive.set_color(Data.sess_id, data['type'], n,
                                '48', '70', '96')
            resp = self.hive.set_color_temp(
                Data.sess_id, data['type'], n, color_temp)

        if str(resp['original']) == "<Response [200]>":
            end = True
            Session.hive_api_get_nodes(Session(), n, False)
            self.log.log("Light", "successfully set the color temp of " +
                         Data.NAME[n] + " to : " + str(color_temp))
        else:
            self.log.log("Light", "Failed to set color temp for light: " +
                         Data.NAME[n])

        return end

    def set_color(self, n, new_color):
        """Set light to turn on."""
        from .hive_session import Session
        self.log.log("Light", "Setting color of : " + Data.NAME[n])
        resp = None
        end = False
        Session.check_hive_api_logon(Session())
        data = Data.products[n]

        resp = self.hive.set_color(Data.sess_id, data['type'], n,
                                   str(new_color[0]),
                                   str(new_color[1]),
                                   str(new_color[2]))
        if str(resp['original']) == "<Response [200]>":
            end = True
            Session.hive_api_get_nodes(Session(), n, False)
            self.log.log("Light", "successfully set the color for " +
                         Data.NAME[n] + ' to : {hue: "' + str(new_color[0]) +
                         ', "saturation": ' + str(new_color[1]) +
                         ', "value": ' + str(new_color[2]) + '}')
        else:
            self.log.log("Light", "Failed to set color for light: " +
                         Data.NAME[n])

        return end
