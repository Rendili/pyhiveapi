""""Hive Hotwater Module. """
from pyhiveapi.custom_logging import Logger
from pyhiveapi.device_attributes import Attributes
from pyhiveapi.hive_api import Hive
from pyhiveapi.hive_data import Data


class Hotwater():
    """Hive Hotwater Code."""

    def __init__(self):
        """Initialise."""
        self.hive = Hive()
        self.log = Logger()
        self.attr = Attributes()
        self.type = "Hotwater"

    def get_mode(self, n):
        """Get hotwater current mode."""
        self.log.log('hotwater', "Getting mode of hotwater: " + Data.NAME[n])
        state = self.attr.online_offline(n)

        if state != 'offline' and n in Data.products:
            data = Data.products[n]
            state = data["state"]["mode"]
            if state == "BOOST":
                state = data["props"]["previous"]["mode"]
            Data.NODES[n]['Mode'] = Data.HIVETOHA[self.type].get(state, state)

        return Data.HIVETOHA[self.type].get(state, Data.NODES[n]['Mode'])

    def get_operation_modes(self, n):
        """Get heating list of possible modes."""
        return ["SCHEDULE", "ON", "OFF"]

    def get_boost(self, n):
        """Get hot water current boost status."""
        self.log.log('hotwater', "Getting boost of hotwater: " + Data.NAME[n])
        state = self.attr.online_offline(n)

        if state != 'offline' and n in Data.products:
            data = Data.products[n]
            state = Data.HIVETOHA[self.type].get((data["state"]["boost"]),
                                                 'ON')
            Data.NODES[n]['Boost'] = state

        return Data.HIVETOHA[self.type].get(state, Data.NODES[n]['Boost'])

    def get_boost_time(self, n):
        """Get hotwater boost time remaining."""
        if self.get_boost(n) == "ON":
            self.log.log('hotwater', "Getting boost time" + Data.NAME[n])
            state = None

            if n in Data.products:
                data = Data.products[n]
                state = data["state"]["boost"]
                Data.NODES[n]['Boost'] = state

        return state if state is None else Data.NODES[n].get('Boost')

    def get_state(self, n):
        """Get hot water current state."""
        from pyhiveapi.hive_session import Session
        self.log.log('hotwater', "Getting state " + Data.NAME[n])
        state = None

        if n in Data.products:
            data = Data.products[n]
            state = data["state"]["status"]
            mode_current = self.get_mode(n)
            if mode_current == "SCHEDULE":
                if self.get_boost(n) == "ON":
                    state = 'ON'
                else:
                    snan = Session.p_get_schedule_now_next_later(
                        data["state"]["schedule"])
                    state = snan["now"]["value"]["status"]
            Data.NODES[n]['State'] = Data.HIVETOHA[self.type].get(state, state)

        return state if state is None else Data.NODES[n].get('State')

    def get_schedule_now_next_later(self, n):
        """Hive get hotwater schedule now, next and later."""
        from pyhiveapi.hive_session import Session
        Session.check_hive_api_logon(Session())
        mode_current = self.get_mode(n)
        snan = None

        if n in Data.products:
            data = Data.products[n]
            if mode_current == "SCHEDULE":
                snan = Session.p_get_schedule_now_next_later(
                    data["state"]["schedule"])

        return snan

    def set_mode(self, n, new_mode):
        """Set hot water mode."""
        from pyhiveapi.hive_session import Session
        Session.check_hive_api_logon(Session())
        state = False

        resp = self.hive.set_mode(Data.sess_id, 'hotwater', n, new_mode)
        if str(resp['original']) == "<Response [200]>":
            state = True
            Session.hive_api_get_nodes(Session(), n, False)
            self.log.log("hotwater", "Light " + Data.NAME[n] +
                         " has been successfully switched on")
        else:
            self.log.log("hotwater", "Failed to set mode: " + Data.NAME[n])

        return state

    def turn_boost_on(self, n, length_minutes):
        """Turn hot water boost on."""
        from pyhiveapi.hive_session import Session
        state = False

        if length_minutes > 0:
            Session.check_hive_api_logon(Session())

            resp = self.hive.set_mode(Data.sess_id, 'hotwater', n,
                                      'BOOST', mins=length_minutes)
            if str(resp['original']) == "<Response [200]>":
                state = True
                Session.hive_api_get_nodes(Session(), n, False)
                self.log.log("hotwater", "Hotwater boost has been " +
                             "successfully set")
            else:
                self.log.log("hotwater", "Failed to turn boost on : " +
                             Data.NAME[n])
        else:
            self.log.log('hotwater', "No boost time set")
        return state

    def turn_boost_off(self, n):
        """Turn hot water boost off."""
        from pyhiveapi.hive_session import Session
        Session.check_hive_api_logon(Session())
        state = False

        if n in Data.products and self.get_boost(n) == "ON":
            data = Data.products[n]
            previous_mode = data["props"]["previous"]["mode"]
            resp = self.hive.set_mode(Data.sess_id, 'hotwater',
                                      n, previous_mode)
            if str(resp['original']) == "<Response [200]>":
                Session.hive_api_get_nodes(Session(), n)
                state = True

        return state
