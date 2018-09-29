"""Switch Class Code."""
from .api import Hive
from .attributes import Attributes
from .data import Data
from .logging import Logger


class Switch:
    """Hive Switch Class."""

    def __init__(self):
        """Initialise."""
        self.hive = Hive()
        self.log = Logger()
        self.attr = Attributes()
        self.type = "Switch"

    @staticmethod
    def data_list():
        return {"tmp": None, "end": False, "resp": False}

    def get_state(self, n):
        """Get light current state."""
        self.log.log('switch', "Getting state for switch : " + Data.NAME[n])
        dl = self.data_list()
        dl.update({'end': (self.attr.online_offline(n))})
        data = Data.products[n]

        if dl['end'] != 'offline':
            try:
                dl.update({'end': data["state"]["status"]})
                Data.NODES["Switch_State" + n] = dl['end']
            except KeyError:
                self.log.log('switch', "Failed to get state - " + Data.NAME[n])

        self.log.log('switch', "State of switch " + Data.NAME[n] + " is: "
                     + dl['end'])
        return Data.HIVETOHA[self.type].get(dl['end'],
                                            Data.NODES.get("Switch_State_"
                                                           + n))

    def get_power_usage(self, n):
        """Get smart plug current power usage."""
        self.log.log('switch', "Getting power usage for: " + Data.NAME[n])
        dl = self.data_list()
        data = Data.products[n]

        try:
            dl.update({'end': data["props"]["powerConsumption"]})
            Data.NODES["Switch_State" + n] = dl['end']
        except KeyError:
            self.log.log('switch', "For switch " + Data.NAME[n]
                         + " power usage is : " + str(dl['end']))

        return dl['end'] if dl['end'] is False \
            else Data.NODES.get("Switch_State" + n)

    def turn_on(self, n):
        """Set smart plug to turn on."""
        from .pyhiveapi import Pyhiveapi
        self.log.log('switch', "Turning on switch : " + Data.NAME[n])
        dl = self.data_list()
        Pyhiveapi.check_hive_api_logon(Pyhiveapi())
        data = Data.products[n]

        dl.update({'resp': (self.hive.set_state(Data.sess_id, data['type'],
                                                n, 'ON'))})
        if str(dl['resp']['original']) == "<Response [200]>":
            dl.update({'end': True})
            Pyhiveapi.hive_api_get_nodes(Pyhiveapi(), n, False)
            self.log.log("switch", "Switch  " + Data.NAME[n]
                         + " has been successfully switched on")
        else:
            self.log.log("switch", "Failed to switch on switch: "
                         + Data.NAME[n])

        return dl['end']

    def turn_off(self, n):
        """Set smart plug to turn off."""
        from .pyhiveapi import Pyhiveapi
        self.log.log('switch', "Turning off switch : " + Data.NAME[n])
        dl = self.data_list()
        Pyhiveapi.check_hive_api_logon(Pyhiveapi())
        data = Data.products[n]

        dl.update({'resp': (self.hive.set_state(Data.sess_id, data['type'],
                                                n, 'OFF'))})
        if str(dl['resp']['original']) == "<Response [200]>":
            dl.update({'end': True})
            Pyhiveapi.hive_api_get_nodes(Pyhiveapi(), n, False)
            self.log.log("switch", "Switch  " + Data.NAME[n]
                         + " has been successfully switched off")
        else:
            self.log.log("switch", "Failed to switch off switch: "
                         + Data.NAME[n])

        return dl['end']
