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
        self.log.log(n_id, self.type, "Getting state")
        state = self.attr.online_offline(n_id)
        final = None

        if n_id in Data.products:
            if state != 'Offline':
                data = Data.products[n_id]
                state = data["state"]["status"]
                self.log.log(n_id, self.type, "Status is {0}", info=state)
            self.log.error_check(n_id, self.type, state)
            final = Data.HIVETOHA[self.type].get(state, state)
            Data.NODES[n_id]['State'] = final
        else:
            self.log.error_check(n_id, 'ERROR', 'Failed')

        return final if final is None else Data.NODES[n_id]['State']

    def get_brightness(self, n_id):
        """Get light current brightness."""
        self.log.log(n_id, self.type, "Getting brightness")
        state = self.attr.online_offline(n_id)
        final = None

        if n_id in Data.products:
            if state != 'Offline':
                data = Data.products[n_id]
                state = data["state"]["brightness"]
                final = ((state / 100) * 255)
                Data.NODES[n_id]["Brightness"] = final
                self.log.log(n_id, self.type, "Brightness is {0}", info=final)
            self.log.error_check(n_id, self.type, state)
        else:
            self.log.error_check(n_id, 'ERROR', 'Failed')

        return final if final is None else Data.NODES[n_id]["Brightness"]

    def get_min_color_temp(self, n_id):
        """Get light minimum color temperature."""
        self.log.log(n_id, self.type, "Getting min colour temperature")
        state = self.attr.online_offline(n_id)
        final = None

        if n_id in Data.products:
            if state != 'Offline':
                data = Data.products[n_id]
                state = data["props"]["colourTemperature"]["max"]
                final = round((1 / state) * 1000000)
                Data.NODES[n_id]["Min_CT"] = final
                self.log.log(n_id, self.type, "Min colour temp is {0}",
                             info=final)
            self.log.error_check(n_id, self.type, state)
        else:
            self.log.error_check(n_id, 'ERROR', 'Failed')

        return final if final is None else Data.NODES[n_id]["Min_CT"]

    def get_max_color_temp(self, n_id):
        """Get light maximum color temperature."""
        self.log.log(n_id, self.type, "Getting max colour temperature")
        state = self.attr.online_offline(n_id)
        final = None

        if n_id in Data.products:
            if state != 'Offline':
                data = Data.products[n_id]
                state = data["props"]["colourTemperature"]["min"]
                final = round((1 / state) * 1000000)
                Data.NODES[n_id]["Max_CT"] = final
                self.log.log(n_id, self.type, "Max colour temp is {0}",
                             info=final)
            self.log.error_check(n_id, self.type, state)
        else:
            self.log.error_check(n_id, 'ERROR', 'Failed')

        return final if final is None else Data.NODES[n_id]["Max_CT"]

    def get_color_temp(self, n_id):
        """Get light current color temperature."""
        self.log.log(n_id, self.type, "Getting colour temperature")
        state = self.attr.online_offline(n_id)
        final = None

        if n_id in Data.products:
            if state != 'Offline':
                data = Data.products[n_id]
                state = data["state"]["colourTemperature"]
                final = round((1 / state) * 1000000)
                Data.NODES[n_id]["CT"] = final
                self.log.log(n_id, self.type, "Colour temp is {0}",
                             info=final)
            self.log.error_check(n_id, self.type, state)
        else:
            self.log.error_check(n_id, 'ERROR', 'Failed')

        return final if final is None else Data.NODES[n_id]["CT"]

    def get_color(self, n_id):
        """Get light current colour"""
        self.log.log(n_id, self.type, "Getting colour info")
        state = self.attr.online_offline(n_id)
        final = None

        if n_id in Data.products:
            if state != 'Offline':
                data = Data.products[n_id]
                state = [(data["state"]["hue"]) / 360,
                         (data["state"]["saturation"]) / 100,
                         (data["state"]["value"]) / 100]
                final = tuple(int(i * 255) for i in colorsys.hsv_to_rgb(
                    state[0],
                    state[1],
                    state[2]))
                Data.NODES[n_id]["Colour"] = final
            self.log.error_check(n_id, self.type, state)
        else:
            self.log.error_check(n_id, 'ERROR', 'Failed')

        return final if final is None else Data.NODES[n_id]["Colour"]

    def turn_off(self, n_id):
        """Set light to turn off."""
        from pyhiveapi.hive_session import Session
        self.log.log(n_id, self.type, "Turning off light")
        final = False

        if n_id in Data.products:
            Session.check_hive_api_logon(Session())
            data = Data.products[n_id]
            resp = self.hive.set_state(Data.sess_id, data['type'], n_id,
                                       status='OFF')
            print(resp)
            if str(resp['original']) == "<Response [200]>":
                final = True
                Session.hive_api_get_nodes(Session(), n_id)
                self.log.log(n_id, 'API', "Light off - API response 200")
            else:
                self.log.error_check(n_id, 'ERROR', 'Failed_API',
                                     resp=resp['original'])

        return final

    def turn_on(self, n_id, brightness, color_temp, color):
        """Set light to turn on."""
        from pyhiveapi.hive_session import Session
        self.log.log(n_id, self.type, "Turning on light")
        final = False

        if n_id in Data.products:
            Session.check_hive_api_logon(Session())
            data = Data.products[n_id]

            if brightness is not None:
                return self.set_brightness(n_id, brightness)
            if color_temp is not None:
                return self.set_color_temp(n_id, color_temp)
            if color is not None:
                return self.set_color(n_id, color)

            resp = self.hive.set_state(Data.sess_id, data['type'], n_id,
                                       status='ON')
            if str(resp['original']) == "<Response [200]>":
                final = True
                Session.hive_api_get_nodes(Session(), n_id)
                self.log.log(n_id, 'API', "Light on - API response 200")
            else:
                self.log.error_check(n_id, 'ERROR', 'Failed_API',
                                     resp=resp['original'])

        return final

    def set_brightness(self, n_id, n_brightness):
        """Set brightness of the light."""
        from pyhiveapi.hive_session import Session
        self.log.log(n_id, self.type, "Setting brightness")
        final = False

        if n_id in Data.products:
            Session.check_hive_api_logon(Session())
            data = Data.products[n_id]
            resp = self.hive.set_state(Data.sess_id, data['type'], n_id,
                                       status='ON', brightness=n_brightness)
            if str(resp['original']) == "<Response [200]>":
                final = True
                Session.hive_api_get_nodes(Session(), n_id)
                self.log.log(n_id, 'API', "Brightness set - API response 200")
            else:
                self.log.error_check(n_id, 'ERROR', 'Failed_API',
                                     resp=resp['original'])

        return final

    def set_color_temp(self, n_id, color_temp):
        """Set light to turn on."""
        from pyhiveapi.hive_session import Session
        self.log.log(n_id, self.type, "Setting color temp")
        final = False

        if n_id in Data.products:
            Session.check_hive_api_logon(Session())
            data = Data.products[n_id]

            if data['type'] == "tuneablelight":
                resp = self.hive.set_state(Data.sess_id, data['type'], n_id,
                                           colourTemperature=color_temp)
            else:
                self.hive.set_state(Data.sess_id, data['type'], n_id,
                                    colourMode='COLOUR', hue='48',
                                    saturation='70', value='96')
                resp = self.hive.set_state(Data.sess_id, data['type'],
                                           n_id, colourMode='WHITE',
                                           colourTemperature=color_temp)

            if str(resp['original']) == "<Response [200]>":
                final = True
                Session.hive_api_get_nodes(Session(), n_id)
                self.log.log(n_id, 'API', "Colour temp set - API response 200")
            else:
                self.log.error_check(n_id, 'ERROR', 'Failed_API',
                                     resp=resp['original'])

        return final

    def set_color(self, n_id, new_color):
        """Set light to turn on."""
        from pyhiveapi.hive_session import Session
        self.log.log(n_id, self.type, "Setting color")
        final = False

        if n_id in Data.products:
            Session.check_hive_api_logon(Session())
            data = Data.products[n_id]

            resp = self.hive.set_state(Data.sess_id, data['type'], n_id,
                                       colourMode='COLOUR',
                                       hue=str(new_color[0]),
                                       saturation=str(new_color[1]),
                                       value=str(new_color[2]))
            if str(resp['original']) == "<Response [200]>":
                final = True
                Session.hive_api_get_nodes(Session(), n_id)
                self.log.log(n_id, 'API', "Colour set - API response 200")
            else:
                self.log.error_check(n_id, 'ERROR', 'Failed_API',
                                     resp=resp['original'])

        return final
