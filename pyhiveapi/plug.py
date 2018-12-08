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

    def get_state(self, n):
        """Get light current state."""
        self.log.log('switch', "Getting state for switch : " + Data.NAME[n])
        end = self.attr.online_offline(n)
        data = Data.products[n]

        if end != 'offline' and n in Data.products:
            end = data["state"]["status"]
            Data.NODES["Switch_State" + n] = end
        else:
            self.log.log('switch', "Failed to get state - " + Data.NAME[n])

        self.log.log('switch', "State of switch " +
                     Data.NAME[n] + " is: " + end)
        return Data.HIVETOHA[self.type].get(end,
                                            Data.NODES.get("Switch_State_" +
                                                           n))

    def get_power_usage(self, n):
        """Get smart plug current power usage."""
        self.log.log('switch', "Getting power usage for: " + Data.NAME[n])
        end = None

        if n in Data.products:
            data = Data.products[n]
            end = data["props"]["powerConsumption"]
            Data.NODES["Switch_State" + n] = end
        else:
            self.log.log('switch', "For switch " + Data.NAME[n] +
                         " power usage is : " + str(end))

        return end if end is None else Data.NODES.get("Switch_State" + n)

    def turn_on(self, n):
        """Set smart plug to turn on."""
        from .hive_session import Pyhiveapi
        self.log.log('switch', "Turning on switch : " + Data.NAME[n])
        resp = None
        end = False
        Pyhiveapi.check_hive_api_logon(Pyhiveapi())
        data = Data.products[n]

        resp = self.hive.set_state(Data.sess_id, data['type'], n, 'ON')
        if str(resp['original']) == "<Response [200]>":
            end = True
            Pyhiveapi.hive_api_get_nodes(Pyhiveapi(), n, False)
            self.log.log("switch", "Switch  " + Data.NAME[n] +
                         " has been successfully switched on")
        else:
            self.log.log("switch", "Failed to switch on switch: " +
                         Data.NAME[n])

        return end

    def turn_off(self, n):
        """Set smart plug to turn off."""
        from .hive_session import Pyhiveapi
        self.log.log('switch', "Turning off switch : " + Data.NAME[n])
        resp = None
        end = False
        Pyhiveapi.check_hive_api_logon(Pyhiveapi())
        data = Data.products[n]

        resp = self.hive.set_state(Data.sess_id, data['type'], n, 'OFF')
        if str(resp['original']) == "<Response [200]>":
            end = True
            Pyhiveapi.hive_api_get_nodes(Pyhiveapi(), n, False)
            self.log.log("switch", "Switch  " + Data.NAME[n] +
                         " has been successfully switched off")
        else:
            self.log.log("switch", "Failed to switch off switch: " +
                         Data.NAME[n])

        return end
