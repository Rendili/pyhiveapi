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

    def get_state(self, id):
        """Get light current state."""
        self.log.log('switch', "Getting state for switch : " + Data.NAME[id])
        end = self.attr.online_offline(id)
        data = Data.products[id]

        if end != 'offline' and id in Data.products:
            end = data["state"]["status"]
            Data.NODES["Switch_State" + id] = end
        else:
            self.log.log('switch', "Failed to get state - " + Data.NAME[id])

        self.log.log('switch', "State of switch " +
                     Data.NAME[id] + " is: " + end)
        return Data.HIVETOHA[self.type].get(end,
                                            Data.NODES.get("Switch_State_" +
                                                           id))

    def get_power_usage(self, id):
        """Get smart plug current power usage."""
        self.log.log('switch', "Getting power usage for: " + Data.NAME[id])
        end = None

        if id in Data.products:
            data = Data.products[id]
            end = data["props"]["powerConsumption"]
            Data.NODES["Switch_State" + id] = end
        else:
            self.log.log('switch', "For switch " + Data.NAME[id] +
                         " power usage is : " + str(end))

        return end if end is None else Data.NODES.get("Switch_State" + id)

    def turn_on(self, id):
        """Set smart plug to turn on."""
        from .hive_session import Session
        self.log.log('switch', "Turning on switch : " + Data.NAME[id])
        resp = None
        end = False
        Session.check_hive_api_logon(Session())
        data = Data.products[id]

        resp = self.hive.set_state(Data.sess_id, data['type'], id, 'ON')
        if str(resp['original']) == "<Response [200]>":
            end = True
            Session.hive_api_get_nodes(Session(), id, False)
            self.log.log("switch", "Switch  " + Data.NAME[id] +
                         " has been successfully switched on")
        else:
            self.log.log("switch", "Failed to switch on switch: " +
                         Data.NAME[id])

        return end

    def turn_off(self, id):
        """Set smart plug to turn off."""
        from .hive_session import Session
        self.log.log('switch', "Turning off switch : " + Data.NAME[id])
        resp = None
        end = False
        Session.check_hive_api_logon(Session())
        data = Data.products[id]

        resp = self.hive.set_state(Data.sess_id, data['type'], id, 'OFF')
        if str(resp['original']) == "<Response [200]>":
            end = True
            Session.hive_api_get_nodes(Session(), id, False)
            self.log.log("switch", "Switch  " + Data.NAME[id] +
                         " has been successfully switched off")
        else:
            self.log.log("switch", "Failed to switch off switch: " +
                         Data.NAME[id])

        return end
