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
        self.log.log(n_id, self.type, "Getting state of switch")
        state = self.attr.online_offline(n_id)
        final = None

        if n_id in Data.products:
            if state != 'Offline':
                data = Data.products[n_id]
                state = data["state"]["status"]
                self.log.log(n_id, self.type, "Status is {0}", info=state)
            self.log.error_check(n_id, self.type, state)
            final = Data.HIVETOHA[self.type].get(state, state)
            Data.NODES[n_id]["State"] = final
        else:
            self.log.error_check(n_id, 'ERROR', 'Failed')

        return final if final is None else Data.NODES[n_id]['State']

    def get_power_usage(self, n_id):
        """Get smart plug current power usage."""
        self.log.log(n_id, self.type, "Getting power consumption.")
        state = self.attr.online_offline(n_id)
        final = None

        if n_id in Data.products:
            if state != 'Offline':
                data = Data.products[n_id]
                state = data["props"]["powerConsumption"]
                self.log.log(n_id, self.type, "Power consumption is {0}",
                             info=state)
            self.log.error_check(n_id, self.type, state)
            final = state
            Data.NODES[n_id]["Power"] = final
        else:
            self.log.error_check(n_id, 'ERROR', 'Failed')

        return final if final is None else Data.NODES[n_id]["Power"]

    def turn_on(self, n_id):
        """Set smart plug to turn on."""
        from .hive_session import Session
        self.log.log(n_id, self.type, "Powering switch")
        final = False

        if n_id in Data.products:
            Session.check_hive_api_logon(Session())
            data = Data.products[n_id]
            resp = self.hive.set_state(Data.sess_id, data['type'], n_id,
                                       status='ON')
            if str(resp['original']) == "<Response [200]>":
                final = True
                Session.hive_api_get_nodes(Session(), n_id)
                self.log.log(n_id, 'API', "Switched on - API response 200")
            else:
                self.log.error_check(n_id, 'ERROR', 'Failed_API',
                                     resp=resp['original'])

        return final

    def turn_off(self, n_id):
        """Set smart plug to turn off."""
        from .hive_session import Session
        self.log.log(n_id, self.type, "Turning off switch.")
        final = False

        if n_id in Data.products:
            Session.check_hive_api_logon(Session())
            data = Data.products[n_id]
            resp = self.hive.set_state(Data.sess_id, data['type'], n_id,
                                       status='OFF')
            if str(resp['original']) == "<Response [200]>":
                final = True
                Session.hive_api_get_nodes(Session(), n_id)
                self.log.log(n_id, 'API', "Switch off - API response 200")
            else:
                self.log.error_check(n_id, 'ERROR', 'Failed_API',
                                     resp=resp['original'])

        return final
