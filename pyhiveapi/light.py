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

    def get_state(self, n_id):
        """Get light current state."""
        self.log.log('light', "Getting state of light: " + Data.NAME[n_id])
        state = self.attr.online_offline(n_id)

        if state != 'offline' and n_id in Data.products:
            data = Data.products[n_id]
            state = data["state"]["status"]
            Data.NODES[n_id]['State'] = Data.HIVETOHA[self.type].get(state)
        else:
            self.log.log('light', "Failed to get state - " + Data.NAME[n_id])

        self.log.log('light', "State of light " + Data.NAME[n_id] +
                     " is " + state)
        return Data.HIVETOHA[self.type].get(state, Data.NODES[n_id]['State'])

    def get_brightness(self, n_id):
        """Get light current brightness."""
        self.log.log('light', "Getting brightness of light: " + Data.NAME[n_id])
        tmp = None
        state = False

        if n_id in Data.products:
            data = Data.products[n_id]
            tmp = data["state"]["brightness"]
            state = ((tmp / 100) * 255)
            Data.NODES[n_id]["Brightness"] = state
            self.log.log("light", "Brightness of light " + Data.NAME[n_id] +
                         " is: " + str(state))

        return state if state is False else Data.NODES[n_id].get("Brightness")

    def get_min_color_temp(self, n_id):
        """Get light minimum color temperature."""
        self.log.log("light", "Getting min colour temperature of light: " +
                     Data.NAME[n_id])
        tmp = None
        state = None

        if n_id in Data.products:
            data = Data.products[n_id]
            tmp = data["props"]["colourTemperature"]["max"]
            state = round((1 / tmp) * 1000000)
            Data.NODES[n_id]["Min_CT"] = state

        self.log.log("light", "Min Colour temperature of light " +
                     Data.NAME[n_id] + " is: " + str(state))

        return state

    def get_max_color_temp(self, n_id):
        """Get light maximum color temperature."""
        self.log.log("light", "Getting max colour temperature of light: " +
                     Data.NAME[n_id])
        tmp = 0
        state = None

        if n_id in Data.products:
            data = Data.products[n_id]
            tmp = data["props"]["colourTemperature"]["min"]
            state = round((1 / tmp) * 1000000)
            Data.NODES[n_id]["Max_CT"] = state

        self.log.log("light", "Max Colour temperature of light " +
                     Data.NAME[n_id] + " is: " + str(state))

        return state

    def get_color_temp(self, n_id):
        """Get light current color temperature."""
        self.log.log("light", "Getting colour temperature of light: " +
                     Data.NAME[n_id])
        tmp = 0
        state = None

        if n_id in Data.products:
            data = Data.products[n_id]
            tmp = data["state"]["colourTemperature"]
            state = round((1 / tmp) * 1000000)
            Data.NODES[n_id]["CT"] = state

        self.log.log("light", "Colour temperature of light " +
                     Data.NAME[n_id] + " is: " + str(state))

        return state if state is None else Data.NODES[n_id].get("CT")

    def get_color(self, n_id):
        """Get light current colour"""
        self.log.log("light", "Getting colour of light : " + Data.NAME[n_id])
        tmp = []
        state = None

        if n_id in Data.products:
            data = Data.products[n_id]
            tmp = dict(
                ((data["state"]["hue"]) / 360),
                ((data["state"]["saturation"]) / 100),
                ((data["state"]["value"]) / 100))
            state = tuple(int(i * 255) for i in colorsys.hsv_to_rgb(
                tmp[0],
                tmp[1],
                tmp[2]))
            Data.NODES[n_id]["Color"] = state

        self.log.log("light", "Colour of light " + Data.NAME[n_id] + " is: " +
                     str(state))

        return state if state is None else Data.NODES[n_id].get("Color")

    def turn_off(self, n_id):
        """Set light to turn off."""
        from pyhiveapi.hive_session import Session
        self.log.log("light", "Turning off light : " + Data.NAME[n_id])
        resp = None
        state = False
        Session.check_hive_api_logon(Session())
        data = Data.products[n_id]

        resp = self.hive.set_state(Data.sess_id, data['type'], n_id, "OFF")
        if str(resp['original']) == "<Response [200]>":
            state = True
            Session.hive_api_get_nodes(Session(), n_id, False)
            self.log.log("light", "Light " + Data.NAME[n_id] +
                         " has been successfully switched off")
        else:
            self.log.log("light", "Failed to switch off - " + Data.NAME[n_id])

        return state

    def turn_on(self, n_id, brightness, color_temp, color):
        """Set light to turn on."""
        from pyhiveapi.hive_session import Session
        self.log.log("light", "Turning on light : " + Data.NAME[n_id])
        resp = None
        state = False
        Session.check_hive_api_logon(Session())
        data = Data.products[n_id]

        if brightness is not None:
            self.set_brightness(n_id, brightness)
        if color_temp is not None:
            self.set_color_temp(n_id, color_temp)
        if color is not None:
            self.set_color(n_id, color)

        resp = self.hive.set_state(Data.sess_id, data['type'], n_id, 'ON')
        if str(resp['original']) == "<Response [200]>":
            state = True
            Session.hive_api_get_nodes(Session(), n_id, False)
            self.log.log("light", "Light " + Data.NAME[n_id] +
                         " has been successfully switched on")
        else:
            self.log.log("light", "Failed to switch on light: " + Data.NAME[n_id])

        return state

    def set_brightness(self, n_id, brightness):
        """Set brightness of the light."""
        from pyhiveapi.hive_session import Session
        self.log.log("light", "Setting brightness of : " + Data.NAME[n_id])
        resp = None
        state = False
        Session.check_hive_api_logon(Session())
        data = Data.products[n_id]

        resp = self.hive.set_brightness(
            Data.sess_id, data['type'], n_id, brightness)
        if str(resp['original']) == "<Response [200]>":
            state = True
            Session.hive_api_get_nodes(Session(), n_id, False)
            self.log.log("light", "successfully set the brightness of " +
                         Data.NAME[n_id] + " to : " + str(brightness))
        else:
            self.log.log("light", "Failed to set brightness for light: " +
                         Data.NAME[n_id])

        return state

    def set_color_temp(self, n_id, color_temp):
        """Set light to turn on."""
        from pyhiveapi.hive_session import Session
        self.log.log("light", "Setting color temp of : " + Data.NAME[n_id])
        resp = None
        state = False
        Session.check_hive_api_logon(Session())
        data = Data.products[n_id]

        if data['type'] == "tuneablelight":
            resp = self.hive.set_color_temp(
                Data.sess_id, data['type'], n_id, color_temp)
        else:
            self.hive.set_color(Data.sess_id, data['type'], n_id,
                                '48', '70', '96')
            resp = self.hive.set_color_temp(
                Data.sess_id, data['type'], n_id, color_temp)

        if str(resp['original']) == "<Response [200]>":
            state = True
            Session.hive_api_get_nodes(Session(), n_id)
            self.log.log("light", "successfully set the color temp of " +
                         Data.NAME[n_id] + " to : " + str(color_temp))
        else:
            self.log.log("light", "Failed to set color temp for light: " +
                         Data.NAME[n_id])

        return state

    def set_color(self, n_id, new_color):
        """Set light to turn on."""
        from pyhiveapi.hive_session import Session
        self.log.log("light", "Setting color of : " + Data.NAME[n_id])
        resp = None
        state = False
        Session.check_hive_api_logon(Session())
        data = Data.products[n_id]

        resp = self.hive.set_color(Data.sess_id, data['type'], n_id,
                                   str(new_color[0]),
                                   str(new_color[1]),
                                   str(new_color[2]))
        if str(resp['original']) == "<Response [200]>":
            state = True
            Session.hive_api_get_nodes(Session(), n_id, False)
            self.log.log("light", "successfully set the color for " +
                         Data.NAME[n_id] + ' to : {hue: "' + str(new_color[0]) +
                         ', "saturation": ' + str(new_color[1]) +
                         ', "value": ' + str(new_color[2]) + '}')
        else:
            self.log.log("light", "Failed to set color for light: " +
                         Data.NAME[n_id])

        return state
