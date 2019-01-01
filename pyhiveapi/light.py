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

    def get_state(self, id):
        """Get light current state."""
        self.log.log('light', "Getting state of light: " + Data.NAME[id])
        state = self.attr.online_offline(id)

        if state != 'offline' and id in Data.products:
            data = Data.products[id]
            state = data["state"]["status"]
            Data.NODES[id]['State'] = Data.HIVETOHA[self.type].get(state)
        else:
            self.log.log('light', "Failed to get state - " + Data.NAME[id])

        self.log.log('light', "State of light " + Data.NAME[id] +
                     " is " + state)
        return Data.HIVETOHA[self.type].get(state, Data.NODES[id]['State'])

    def get_brightness(self, id):
        """Get light current brightness."""
        self.log.log('light', "Getting brightness of light: " + Data.NAME[id])
        tmp = None
        state = False

        if id in Data.products:
            data = Data.products[id]
            tmp = data["state"]["brightness"]
            state = ((tmp / 100) * 255)
            Data.NODES[id]["Brightness"] = state
            self.log.log("light", "Brightness of light " + Data.NAME[id] +
                         " is: " + str(state))

        return state if state is False else Data.NODES[id].get("Brightness")

    def get_min_color_temp(self, id):
        """Get light minimum color temperature."""
        self.log.log("light", "Getting min colour temperature of light: " +
                     Data.NAME[id])
        tmp = None
        state = None

        if id in Data.products:
            data = Data.products[id]
            tmp = data["props"]["colourTemperature"]["max"]
            state = round((1 / tmp) * 1000000)
            Data.NODES[id]["Min_CT"] = state

        self.log.log("light", "Min Colour temperature of light " +
                     Data.NAME[id] + " is: " + str(state))

        return state

    def get_max_color_temp(self, id):
        """Get light maximum color temperature."""
        self.log.log("light", "Getting max colour temperature of light: " +
                     Data.NAME[id])
        tmp = 0
        state = None

        if id in Data.products:
            data = Data.products[id]
            tmp = data["props"]["colourTemperature"]["min"]
            state = round((1 / tmp) * 1000000)
            Data.NODES[id]["Max_CT"] = state

        self.log.log("light", "Max Colour temperature of light " +
                     Data.NAME[id] + " is: " + str(state))

        return state

    def get_color_temp(self, id):
        """Get light current color temperature."""
        self.log.log("light", "Getting colour temperature of light: " +
                     Data.NAME[id])
        tmp = 0
        state = None

        if id in Data.products:
            data = Data.products[id]
            tmp = data["state"]["colourTemperature"]
            state = round((1 / tmp) * 1000000)
            Data.NODES[id]["CT"] = state

        self.log.log("light", "Colour temperature of light " +
                     Data.NAME[id] + " is: " + str(state))

        return state if state is None else Data.NODES[id].get("CT")

    def get_color(self, id):
        """Get light current colour"""
        self.log.log("light", "Getting colour of light : " + Data.NAME[id])
        tmp = []
        state = None

        if id in Data.products:
            data = Data.products[id]
            tmp = dict(
                ((data["state"]["hue"]) / 360),
                ((data["state"]["saturation"]) / 100),
                ((data["state"]["value"]) / 100))
            state = tuple(int(i * 255) for i in colorsys.hsv_to_rgb(
                tmp[0],
                tmp[1],
                tmp[2]))
            Data.NODES[id]["Color"] = state

        self.log.log("light", "Colour of light " + Data.NAME[id] + " is: " +
                     str(state))

        return state if state is None else Data.NODES[id].get("Color")

    def turn_off(self, id):
        """Set light to turn off."""
        from pyhiveapi.hive_session import Session
        self.log.log("light", "Turning off light : " + Data.NAME[id])
        resp = None
        state = False
        Session.check_hive_api_logon(Session())
        data = Data.products[id]

        resp = self.hive.set_state(Data.sess_id, data['type'], id, "OFF")
        if str(resp['original']) == "<Response [200]>":
            state = True
            Session.hive_api_get_nodes(Session(), id, False)
            self.log.log("light", "Light " + Data.NAME[id] +
                         " has been successfully switched off")
        else:
            self.log.log("light", "Failed to switch off - " + Data.NAME[id])

        return state

    def turn_on(self, id, brightness, color_temp, color):
        """Set light to turn on."""
        from pyhiveapi.hive_session import Session
        self.log.log("light", "Turning on light : " + Data.NAME[id])
        resp = None
        state = False
        Session.check_hive_api_logon(Session())
        data = Data.products[id]

        if brightness is not None:
            self.set_brightness(id, brightness)
        if color_temp is not None:
            self.set_color_temp(id, color_temp)
        if color is not None:
            self.set_color(id, color)

        resp = self.hive.set_state(Data.sess_id, data['type'], id, 'ON')
        if str(resp['original']) == "<Response [200]>":
            state = True
            Session.hive_api_get_nodes(Session(), id, False)
            self.log.log("light", "Light " + Data.NAME[id] +
                         " has been successfully switched on")
        else:
            self.log.log("light", "Failed to switch on light: " + Data.NAME[id])

        return state

    def set_brightness(self, id, brightness):
        """Set brightness of the light."""
        from pyhiveapi.hive_session import Session
        self.log.log("light", "Setting brightness of : " + Data.NAME[id])
        resp = None
        state = False
        Session.check_hive_api_logon(Session())
        data = Data.products[id]

        resp = self.hive.set_brightness(
            Data.sess_id, data['type'], id, brightness)
        if str(resp['original']) == "<Response [200]>":
            state = True
            Session.hive_api_get_nodes(Session(), id, False)
            self.log.log("light", "successfully set the brightness of " +
                         Data.NAME[id] + " to : " + str(brightness))
        else:
            self.log.log("light", "Failed to set brightness for light: " +
                         Data.NAME[id])

        return state

    def set_color_temp(self, id, color_temp):
        """Set light to turn on."""
        from pyhiveapi.hive_session import Session
        self.log.log("light", "Setting color temp of : " + Data.NAME[id])
        resp = None
        state = False
        Session.check_hive_api_logon(Session())
        data = Data.products[id]

        if data['type'] == "tuneablelight":
            resp = self.hive.set_color_temp(
                Data.sess_id, data['type'], id, color_temp)
        else:
            self.hive.set_color(Data.sess_id, data['type'], id,
                                '48', '70', '96')
            resp = self.hive.set_color_temp(
                Data.sess_id, data['type'], id, color_temp)

        if str(resp['original']) == "<Response [200]>":
            state = True
            Session.hive_api_get_nodes(Session(), id, False)
            self.log.log("light", "successfully set the color temp of " +
                         Data.NAME[id] + " to : " + str(color_temp))
        else:
            self.log.log("light", "Failed to set color temp for light: " +
                         Data.NAME[id])

        return state

    def set_color(self, id, new_color):
        """Set light to turn on."""
        from pyhiveapi.hive_session import Session
        self.log.log("light", "Setting color of : " + Data.NAME[id])
        resp = None
        state = False
        Session.check_hive_api_logon(Session())
        data = Data.products[id]

        resp = self.hive.set_color(Data.sess_id, data['type'], id,
                                   str(new_color[0]),
                                   str(new_color[1]),
                                   str(new_color[2]))
        if str(resp['original']) == "<Response [200]>":
            state = True
            Session.hive_api_get_nodes(Session(), id, False)
            self.log.log("light", "successfully set the color for " +
                         Data.NAME[id] + ' to : {hue: "' + str(new_color[0]) +
                         ', "saturation": ' + str(new_color[1]) +
                         ', "value": ' + str(new_color[2]) + '}')
        else:
            self.log.log("light", "Failed to set color for light: " +
                         Data.NAME[id])

        return state
