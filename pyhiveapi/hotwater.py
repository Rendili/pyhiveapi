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

    def get_mode(self, id):
        """Get hotwater current mode."""
        self.log.log('hotwater', "Getting mode of hotwater: " + Data.NAME[id])
        state = self.attr.online_offline(id)

        if state != 'offline' and id in Data.products:
            data = Data.products[id]
            state = data["state"]["mode"]
            if state == "BOOST":
                state = data["props"]["previous"]["mode"]
            Data.NODES[id]['Mode'] = Data.HIVETOHA[self.type].get(state, state)

        return Data.HIVETOHA[self.type].get(state, Data.NODES[id]['Mode'])

    def get_operation_modes(self, id):
        """Get heating list of possible modes."""
        return ["SCHEDULE", "ON", "OFF"]

    def get_boost(self, id):
        """Get hot water current boost status."""
        self.log.log('hotwater', "Getting boost of hotwater: " + Data.NAME[id])
        state = self.attr.online_offline(id)

        if state != 'offline' and id in Data.products:
            data = Data.products[id]
            state = Data.HIVETOHA['Boost'].get((data["state"]["boost"]),
                                                 'ON')
            Data.NODES[id]['Boost'] = state

        return Data.HIVETOHA['Boost'].get(state, Data.NODES[id]['Boost'])

    def get_boost_time(self, id):
        """Get hotwater boost time remaining."""
        if self.get_boost(id) == "ON":
            self.log.log('hotwater', "Getting boost time" + Data.NAME[id])
            state = None

            if id in Data.products:
                data = Data.products[id]
                state = data["state"]["boost"]
                Data.NODES[id]['Boost_Time'] = state

        return state if state is None else Data.NODES[id].get('Boost_Time')

    def get_state(self, id):
        """Get hot water current state."""
        from pyhiveapi.hive_session import Session
        self.log.log('hotwater', "Getting state " + Data.NAME[id])
        state = None

        if id in Data.products:
            data = Data.products[id]
            state = data["state"]["status"]
            mode_current = self.get_mode(id)
            if mode_current == "SCHEDULE":
                if self.get_boost(id) == "ON":
                    state = 'ON'
                else:
                    snan = Session.p_get_schedule_now_next_later(
                        data["state"]["schedule"])
                    state = snan["now"]["value"]["status"]
            Data.NODES[id]['State'] = Data.HIVETOHA[self.type].get(state, state)

        return Data.HIVETOHA[self.type].get(state, Data.NODES[id]['State'])

    def get_schedule_now_next_later(self, id):
        """Hive get hotwater schedule now, next and later."""
        from pyhiveapi.hive_session import Session
        Session.check_hive_api_logon(Session())
        mode_current = self.get_mode(id)
        snan = None

        if id in Data.products and mode_current == "SCHEDULE":
            data = Data.products[id]
            snan = Session.p_get_schedule_now_next_later(
                data["state"]["schedule"])

        return snan

    def set_mode(self, id, new_mode):
        """Set hot water mode."""
        from pyhiveapi.hive_session import Session
        Session.check_hive_api_logon(Session())
        final = False

        if id in Data.products:
            data = Data.products[id]
            resp = self.hive.set_mode(Data.sess_id, data[type], id, new_mode)
            if str(resp['original']) == "<Response [200]>":
                final = True
                Session.hive_api_get_nodes(Session(), id, False)
                self.log.log("hotwater", "Howater has been " +
                "successfully set to " + new_mode)
            else:
                self.log.log("hotwater", "Failed to set hotwater to " + new_mode)

        return final

    def turn_boost_on(self, id, length_minutes):
        """Turn hot water boost on."""
        from pyhiveapi.hive_session import Session
        state = False

        if length_minutes > 0:
            Session.check_hive_api_logon(Session())

            resp = self.hive.set_mode(Data.sess_id, 'hotwater', id,
                                      'BOOST', mins=length_minutes)
            if str(resp['original']) == "<Response [200]>":
                state = True
                Session.hive_api_get_nodes(Session(), id, False)
                self.log.log("hotwater", "Hotwater boost has been " +
                             "successfully set")
            else:
                self.log.log("hotwater", "Failed to turn boost on : " +
                             Data.NAME[id])
        else:
            self.log.log('hotwater', "No boost time set")
        return state

    def turn_boost_off(self, id):
        """Turn hot water boost off."""
        from pyhiveapi.hive_session import Session
        Session.check_hive_api_logon(Session())
        state = False

        if id in Data.products and self.get_boost(id) == "ON":
            data = Data.products[id]
            previous_mode = data["props"]["previous"]["mode"]
            resp = self.hive.set_mode(Data.sess_id, 'hotwater',
                                      id, previous_mode)
            if str(resp['original']) == "<Response [200]>":
                Session.hive_api_get_nodes(Session(), id)
                state = True

        return state
