"""Hive Switch Module."""
from pyhiveapi.custom_logging import Logger
from pyhiveapi.device_attributes import Attributes
from pyhiveapi.hive_api import Hive
from pyhiveapi.hive_data import Data


class Plug:
    """Hive Switch Code."""
    def __init__(self):
        """Initialise."""
        self.hive = Hive()
        self.log = Logger()
        self.attr = Attributes()
        self.type = "Switch"

    def get_state(self, n_id):
        """Get light current state."""
        self.log.log('switch', "Getting state for switch : " + Data.NAME[n_id])
        final = self.attr.online_offline(n_id)
        data = Data.products[n_id]

        if final != 'offline' and n_id in Data.products:
            final = data["state"]["status"]
            Data.NODES["Switch_State" + n_id] = final
        else:
            self.log.log('switch', "Failed to get state - " + Data.NAME[n_id])

        self.log.log('switch', "State of switch " +
                     Data.NAME[n_id] + " is: " + final)
        return Data.HIVETOHA[self.type].get(final,
                                            Data.NODES.get("Switch_State_" +
                                                           n_id))

    def get_power_usage(self, n_id):
        """Get smart plug current power usage."""
        self.log.log('switch', "Getting power usage for: " + Data.NAME[n_id])
        final = None

        if n_id in Data.products:
            data = Data.products[n_id]
            final = data["props"]["powerConsumption"]
            Data.NODES["Switch_State" + n_id] = final
        else:
            self.log.log('switch', "For switch " + Data.NAME[n_id] +
                         " power usage is : " + str(final))

        return final if final is None else Data.NODES.get("Switch_State" + n_id)

    def turn_on(self, n_id):
        """Set smart plug to turn on."""
        from .hive_session import Session
        self.log.log('switch', "Turning on switch : " + Data.NAME[n_id])
        final = False
        Session.check_hive_api_logon(Session())
        data = Data.products[n_id]

        resp = self.hive.set_state(Data.sess_id, data['type'], n_id, status='ON')
        if str(resp['original']) == "<Response [200]>":
            final = True
            Session.hive_api_get_nodes(Session(), n_id)
            self.log.log("switch", "Switch  " + Data.NAME[n_id] +
                         " has been successfully switched on")
        else:
            self.log.log("switch", "Failed to switch on switch: " +
                         Data.NAME[n_id])

        return final

    def turn_off(self, n_id):
        """Set smart plug to turn off."""
        from .hive_session import Session
        self.log.log('switch', "Turning off switch : " + Data.NAME[n_id])
        final = False
        Session.check_hive_api_logon(Session())
        data = Data.products[n_id]

        resp = self.hive.set_state(Data.sess_id, data['type'], n_id, status='OFF')
        if str(resp['original']) == "<Response [200]>":
            final = True
            Session.hive_api_get_nodes(Session(), n_id)
            self.log.log("switch", "Switch  " + Data.NAME[n_id] +
                         " has been successfully switched off")
        else:
            self.log.log("switch", "Failed to switch off switch: " +
                         Data.NAME[n_id])

        return final
