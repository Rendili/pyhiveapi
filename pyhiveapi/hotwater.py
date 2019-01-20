""""Hive Hotwater Module. """
from pyhiveapi.custom_logging import Logger
from pyhiveapi.device_attributes import Attributes
from pyhiveapi.hive_api import Hive
from pyhiveapi.hive_data import Data


class Hotwater:
    """Hive Hotwater Code."""

    def __init__(self):
        """Initialise."""
        self.hive = Hive()
        self.log = Logger()
        self.attr = Attributes()
        self.type = "Hotwater"

    def get_mode(self, n_id):
        """Get hotwater current mode."""
        self.log.log('hotwater', "Getting mode of hotwater: " + Data.NAME[n_id])
        state = self.attr.online_offline(n_id)

        if state != 'offline' and n_id in Data.products:
            data = Data.products[n_id]
            state = data["state"]["mode"]
            if state == "BOOST":
                state = data["props"]["previous"]["mode"]
            Data.NODES[n_id]['Mode'] = Data.HIVETOHA[self.type].get(state, state)

        return Data.HIVETOHA[self.type].get(state, Data.NODES[n_id]['Mode'])

    def get_operation_modes(self):
        """Get heating list of possible modes."""
        return ["SCHEDULE", "ON", "OFF"]

    def get_boost(self, n_id):
        """Get hot water current boost status."""
        self.log.log('hotwater', "Getting boost of hotwater: " + Data.NAME[n_id])
        state = self.attr.online_offline(n_id)

        if state != 'offline' and n_id in Data.products:
            data = Data.products[n_id]
            state = Data.HIVETOHA['Boost'].get((data["state"]["boost"]),
                                               'ON')
            Data.NODES[n_id]['Boost'] = state

        return Data.HIVETOHA['Boost'].get(state, Data.NODES[n_id]['Boost'])

    def get_boost_time(self, n_id):
        """Get hotwater boost time remaining."""
        if self.get_boost(n_id) == "ON":
            self.log.log('hotwater', "Getting boost time")
            final = None

            if n_id in Data.products:
                data = Data.products[n_id]
                state = data["state"]["boost"]
                Data.NODES[n_id]['Boost_Time'] = state

            return final if final is None else Data.NODES[n_id].get('Boost_Time')

    def get_state(self, n_id):
        """Get hot water current state."""
        from pyhiveapi.hive_session import Session
        self.log.log('hotwater', "Getting state " + Data.NAME[n_id])
        state = None

        if n_id in Data.products:
            data = Data.products[n_id]
            state = data["state"]["status"]
            mode_current = self.get_mode(n_id)
            if mode_current == "SCHEDULE":
                if self.get_boost(n_id) == "ON":
                    state = 'ON'
                else:
                    snan = Session.p_get_schedule_now_next_later(Session(),
                                                                 data["state"]["schedule"])
                    state = snan["now"]["value"]["status"]
            Data.NODES[n_id]['State'] = Data.HIVETOHA[self.type].get(state, state)

        return Data.HIVETOHA[self.type].get(state, Data.NODES[n_id]['State'])

    def get_schedule_now_next_later(self, n_id):
        """Hive get hotwater schedule now, next and later."""
        from pyhiveapi.hive_session import Session
        Session.check_hive_api_logon(Session())
        mode_current = self.get_mode(n_id)
        snan = None

        if n_id in Data.products and mode_current == "SCHEDULE":
            data = Data.products[n_id]
            snan = Session.p_get_schedule_now_next_later(Session(),
                                                         data["state"]["schedule"])

        return snan

    def set_mode(self, n_id, new_mode):
        """Set hot water mode."""
        from pyhiveapi.hive_session import Session
        Session.check_hive_api_logon(Session())
        final = False

        if n_id in Data.products:
            data = Data.products[n_id]
            resp = self.hive.set_state(Data.sess_id, data[type], n_id, mode=new_mode)
            if str(resp['original']) == "<Response [200]>":
                final = True
                Session.hive_api_get_nodes(Session(), n_id)
                self.log.log("hotwater", "Howater has been " +
                                         "successfully set to " + new_mode)
            else:
                self.log.log("hotwater", "Failed to set hotwater to " + new_mode)

        return final

    def turn_boost_on(self, n_id, mins):
        """Turn hot water boost on."""
        from pyhiveapi.hive_session import Session
        state = False

        if mins > 0:
            Session.check_hive_api_logon(Session())

            resp = self.hive.set_state(Data.sess_id, 'hotwater', n_id,
                                       mode='BOOST', boost=mins)
            if str(resp['original']) == "<Response [200]>":
                state = True
                Session.hive_api_get_nodes(Session(), n_id)
                self.log.log("hotwater", "Hotwater boost has been " +
                             "successfully set")
            else:
                self.log.log("hotwater", "Failed to turn boost on : " +
                             Data.NAME[n_id])
        else:
            self.log.log('hotwater', "No boost time set")
        return state

    def turn_boost_off(self, n_id):
        """Turn hot water boost off."""
        from pyhiveapi.hive_session import Session
        Session.check_hive_api_logon(Session())
        state = False

        if n_id in Data.products and self.get_boost(n_id) == "ON":
            data = Data.products[n_id]
            prev_mode = data["props"]["previous"]["mode"]
            resp = self.hive.set_state(Data.sess_id, 'hotwater',
                                       n_id, mode=prev_mode)
            if str(resp['original']) == "<Response [200]>":
                Session.hive_api_get_nodes(Session(), n_id)
                state = True

        return state
