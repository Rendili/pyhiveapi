""""Hive Heating Module. """
from pyhiveapi.custom_logging import Logger
from pyhiveapi.device_attributes import Attributes
from pyhiveapi.hive_api import Hive
from pyhiveapi.hive_data import Data


class Heating():
    """Hive Heating Code."""

    def __init__(self):
        """Initialise."""
        self.hive = Hive()
        self.log = Logger()
        self.attr = Attributes()
        self.type = "Hotwater"

    def min_temperature(self, id):
        """Get heating minimum target temperature."""
        return 5

    def max_temperature(self, id):
        """Get heating maximum target temperature."""
        return 32

    def current_temperature(self, id):
        """Get heating current temperature."""
        import datetime
        self.log.log('heating', "Heating - Getting current " +
                     "temp for " + Data.NAME[id])
        state = self.attr.online_offline(id)
        final = None

        if id in Data.products:
            if state != 'offline':
                data = Data.products[id]
                state = data["props"]["temperature"]
                final = state
                Data.NODES[id]['CurrentTemp'] = final

                if id in Data.p_minmax:
                    if Data.p_minmax[id]['TodayDate'] != datetime.date(datetime.now()):
                        Data.p_minmac[id]['TodayMin'] = 1000
                        Data.p_minmac[id]['TodayMax'] = -1000
                        Data.p_minmac[id]['TodayDate'] = datetime.date(
                            datetime.now())

                    if state < Data.p_minmac[id]['TodayMin']:
                        Data.p_minmac[id]['TodayMin'] = state

                    if state > Data.p_minmac[id]['TodayMax']:
                        Data.p_minmac[id]['TodayMax'] = state

                    if state < Data.p_minmac[id]['RestartMin']:
                        Data.p_minmac[id]['RestartMin'] = state

                    if state > Data.p_minmac[id]['RestartMax']:
                        Data.p_minmac[id]['RestartMax'] = state
                else:
                    current_node_max_min_data = {}
                    current_node_max_min_data['TodayMin'] = state
                    current_node_max_min_data['TodayMax'] = state
                    current_node_max_min_data['TodayDate'] = datetime.date(
                        datetime.now())
                    current_node_max_min_data['RestartMin'] = state
                    current_node_max_min_data['RestartMax'] = state
                    data.min[id] = current_node_max_min_data

        return final if final is None else Data.NODES[id]['CurrentTemp']

    def minmax_temperatures(self, id):
        """Min/Max Temp"""
        self.log.log('heating', "Heating - Getting current " +
                     "temp for " + Data.NAME[id])
        state = self.attr.online_offline(id)

        if state != 'offline' and id in Data.p_minmac:
            return Data.p_minmax[id]
        else:
            return None

    def get_target_temperature(self, id):
        """Get heating target temperature."""
        from pyhiveapi.hive_session import Session
        self.log.log('heating', "Heating - Getting current " +
                     "temp for " + Data.NAME[id])
        state = self.attr.online_offline(id)
        final = None

        if id in Data.products:
            if state != 'offline':
                data = Data.products[id]
                mode_current = self.get_mode(id)
                boost_current = self.get_boost(id)
                if boost_current == "ON" or mode_current == "SCHEDULE":
                    state = data["state"]["target"]

                else:
                    snan = Session.p_get_schedule_now_next_later(
                        data["state"]["schedule"])
                    if 'now' in snan:
                        state = snan["now"]["value"]["target"]
                    else:
                        state = data["state"]["target"]
                final = state
                Data.NODES[id]['TargetTemp'] = final

        return final if final is None else Data.NODES[id]['TargetTemp']

    def get_mode(self, id):
        """Get heating current mode."""
        self.log.log('heating', "Heating - Getting current " +
                     "temp for " + Data.NAME[id])
        state = self.attr.online_offline(id)
        final = None

        if id in Data.products:
            if state != 'offline':
                data = Data.products[id]
                state = data["state"]["mode"]
                if state == "BOOST":
                    state = data["props"]["previous"]["mode"]
            final = Data.HIVETOHA[self.type].get(state, state)
            Data.NODES[id]['Mode'] = final

        return final if final is None else Data.NODES[id]['Mode']

    def get_state(self, id):
        """Get heating current state."""
        self.log.log('heating', "Heating - Getting current " +
                     "temp for " + Data.NAME[id])
        state = self.attr.online_offline(id)
        final = None

        if id in Data.products:
            if state != 'offline':
                data = Data.products[id]
                current_temp = self.current_temperature(id)
                target_temp = self.get_target_temperature(id)
                if current_temp < target_temp:
                    state = "ON"
                else:
                    state = "OFF"
            final = Data.HIVETOHA[self.type].get(state, state)
            Data.NODES[id]['State'] = final

        return final if final is None else Data.NODES[id]['State']

    def get_boost(self, id):
        """Get heating boost current status."""
        self.log.log('heating', "Heating - Getting current " +
                     "temp for " + Data.NAME[id])
        state = self.attr.online_offline(id)
        final = None

        if id in Data.products:
            if state != 'offline':
                data = Data.products[id]
                state = data["state"]["boost"]
            final = Data.HIVETOHA['Boost'].get(state, 'ON')
            Data.NODES[id]['Boost'] = final

        return final if final is None else Data.NODES[id]['Boost']

    def get_boost_time(self, id):
        """Get heating boost time remaining."""
        if self. get_boost(id) == 'ON':
            self.log.log('heating', "Heating - Getting current " +
                         "temp for " + Data.NAME[id])
            state = self.attr.online_offline(id)
            final = None

            if id in Data.products:
                if state != 'offline':
                    data = Data.products[id]
                    state = data["state"]["boost"]
                    final = state
                    Data.NODES[id]['Boost_Time'] = final

            return final if final is None else Data.NODES[id]['Boost_Time']

    def get_operation_modes(self, id):
        """Get heating list of possible modes."""
        return ["SCHEDULE", "MANUAL", "OFF"]

    def get_schedule_now_next_later(self, id):
        """Hive get heating schedule now, next and later."""
        from pyhiveapi.hive_session import Session
        current_mode = self.get_mode(id)
        snan = None

        if id in Data.products and current_mode == "SCHEDULE":
            data = Data.products
            snan = Session.p_get_schedule_now_next_later(Session,
                                                         data["state"]["schedule"])

        return snan

    def set_target_temperature(self, id, new_temp):
        """Set heating target temperature."""
        from pyhiveapi.hive_session import Session
        Session.check_hive_api_logon(Session)
        resp = None
        final = False

        if id in Data.products:
            data = Data.products[id]
            resp = self.hive.set_state(Data.sess_id, data[type], id,
                                       target=new_temp)

            if str(resp['original']) == "<Response [200]>":
                Session.hive_api_get_nodes(self, id)
                final = True

        return final

    def set_mode(self, id, new_mode):
        """Set heating mode."""
        from pyhiveapi.hive_session import Session
        Session.check_hive_api_logon(Session)
        resp = None
        final = False

        if id in Data.products:
            data = Data.products[id]
            resp = self.hive.set_state(Data.sess_id, data[type], id,
                                       mode=new_mode)

            if str(resp['original']) == "<Response [200]>":
                Session.hive_api_get_nodes(self, id)
                final = True

        return final

    def turn_boost_on(self, id, mins, temp):
        """Turn heating boost on."""
        if mins > 0 and temp >= self.min_temperature(id) and temp <= self.max_temperature(id):
            from pyhiveapi.hive_session import Session
            Session.check_hive_api_logon(Session)
            resp = None
            final = False

            if id in Data.products:
                data = Data.products[id]
                resp = self.hive.set_state(Data.sess_id, data[type], id,
                                           mode='BOOST', boost=mins, target=temp)

                if str(resp['original']) == "<Response [200]>":
                    Session.hive_api_get_nodes(Session, id)
                    final = True

        return final

    def turn_boost_off(self, id):
        """Turn heating boost off."""
        from pyhiveapi.hive_session import Session
        Session.check_hive_api_logon(Session)
        final = False

        if id in Data.products:
            data = Data.products
            Session.hive_api_get_nodes(Session, id)
            if self.get_boost(id) == "ON":
                prev_mode = data["props"]["previous"]["mode"]
                if prev_mode == "MANUAL":
                    prev_temp = data["props"]["previous"]["target"]
                    resp = self.hive.set_state(Data.sess_id, data[type], id,
                                               mode=prev_mode, target=prev_temp)
                else:
                    resp = self.hive.set_state(Data.sess_id, data[type], id,
                                               mode=prev_mode)
                if str(resp['original']) == "<Response [200]>":
                    Session.hive_api_get_nodes(Session, id)
                    final = True

        return final
