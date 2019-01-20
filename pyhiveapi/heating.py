""""Hive Heating Module. """
from pyhiveapi.custom_logging import Logger
from pyhiveapi.device_attributes import Attributes
from pyhiveapi.hive_api import Hive
from pyhiveapi.hive_data import Data


class Heating:
    """Hive Heating Code."""

    def __init__(self):
        """Initialise."""
        self.hive = Hive()
        self.log = Logger()
        self.attr = Attributes()
        self.type = "Hotwater"

    def min_temperature(self):
        """Get heating minimum target temperature."""
        return 5

    def max_temperature(self):
        """Get heating maximum target temperature."""
        return 32

    def current_temperature(self, n_id):
        """Get heating current temperature."""
        import datetime
        self.log.log('heating', "Heating - Getting current " +
                     "temp for " + Data.NAME[n_id])
        state = self.attr.online_offline(n_id)
        final = None

        if n_id in Data.products:
            if state != 'offline':
                data = Data.products[n_id]
                state = data["props"]["temperature"]
                final = state
                Data.NODES[n_id]['CurrentTemp'] = final

                if n_id in Data.p_minmax:
                    if Data.p_minmax[n_id]['TodayDate'] != datetime.date(datetime.now()):
                        Data.p_minmax[n_id]['TodayMin'] = 1000
                        Data.p_minmax[n_id]['TodayMax'] = -1000
                        Data.p_minmax[n_id]['TodayDate'] = datetime.date(
                            datetime.now())

                    if state < Data.p_minmax[n_id]['TodayMin']:
                        Data.p_minmax[n_id]['TodayMin'] = state

                    if state > Data.p_minmax[n_id]['TodayMax']:
                        Data.p_minmax[n_id]['TodayMax'] = state

                    if state < Data.p_minmax[n_id]['RestartMin']:
                        Data.p_minmax[n_id]['RestartMin'] = state

                    if state > Data.p_minmax[n_id]['RestartMax']:
                        Data.p_minmax[n_id]['RestartMax'] = state
                else:
                    data = {'TodayMin': state, 'TodayMax': state, 'TodayDate': datetime.date(
                        datetime.now()), 'RestartMin': state, 'RestartMax': state}
                    data.min[n_id] = data

        return final if final is None else Data.NODES[n_id]['CurrentTemp']

    def minmax_temperatures(self, n_id):
        """Min/Max Temp"""
        self.log.log('heating', "Heating - Getting current " +
                     "temp for " + Data.NAME[n_id])
        state = self.attr.online_offline(n_id)

        if state != 'offline' and n_id in Data.p_minmax:
            return Data.p_minmax[n_id]
        else:
            return None

    def get_target_temperature(self, n_id):
        """Get heating target temperature."""
        from pyhiveapi.hive_session import Session
        self.log.log('heating', "Heating - Getting current " +
                     "temp for " + Data.NAME[n_id])
        state = self.attr.online_offline(n_id)
        final = None

        if n_id in Data.products:
            if state != 'offline':
                data = Data.products[n_id]
                mode_current = self.get_mode(n_id)
                boost_current = self.get_boost(n_id)
                if boost_current == "ON" or mode_current == "SCHEDULE":
                    state = data["state"]["target"]

                else:
                    snan = Session.p_get_schedule_now_next_later(self,
                                                                 data["state"]["schedule"])
                    if 'now' in snan:
                        state = snan["now"]["value"]["target"]
                    else:
                        state = data["state"]["target"]
                final = state
                Data.NODES[n_id]['TargetTemp'] = final

        return final if final is None else Data.NODES[n_id]['TargetTemp']

    def get_mode(self, n_id):
        """Get heating current mode."""
        self.log.log('heating', "Heating - Getting current " +
                     "temp for " + Data.NAME[n_id])
        state = self.attr.online_offline(n_id)
        final = None

        if n_id in Data.products:
            if state != 'offline':
                data = Data.products[n_id]
                state = data["state"]["mode"]
                if state == "BOOST":
                    state = data["props"]["previous"]["mode"]
            final = Data.HIVETOHA[self.type].get(state, state)
            Data.NODES[n_id]['Mode'] = final

        return final if final is None else Data.NODES[n_id]['Mode']

    def get_state(self, n_id):
        """Get heating current state."""
        self.log.log('heating', "Heating - Getting current " +
                     "temp for " + Data.NAME[n_id])
        state = self.attr.online_offline(n_id)
        final = None

        if n_id in Data.products:
            if state != 'offline':
                current_temp = self.current_temperature(n_id)
                target_temp = self.get_target_temperature(n_id)
                if current_temp < target_temp:
                    state = "ON"
                else:
                    state = "OFF"
            final = Data.HIVETOHA[self.type].get(state, state)
            Data.NODES[n_id]['State'] = final

        return final if final is None else Data.NODES[n_id]['State']

    def get_boost(self, n_id):
        """Get heating boost current status."""
        self.log.log('heating', "Heating - Getting current " +
                     "temp for " + Data.NAME[n_id])
        state = self.attr.online_offline(n_id)
        final = None

        if n_id in Data.products:
            if state != 'offline':
                data = Data.products[n_id]
                state = data["state"]["boost"]
            final = Data.HIVETOHA['Boost'].get(state, 'ON')
            Data.NODES[n_id]['Boost'] = final

        return final if final is None else Data.NODES[n_id]['Boost']

    def get_boost_time(self, n_id):
        """Get heating boost time remaining."""
        if self. get_boost(n_id) == 'ON':
            self.log.log('heating', "Heating - Getting current " +
                         "temp for " + Data.NAME[n_id])
            state = self.attr.online_offline(n_id)
            final = None

            if n_id in Data.products:
                if state != 'offline':
                    data = Data.products[n_id]
                    state = data["state"]["boost"]
                    final = state
                    Data.NODES[n_id]['Boost_Time'] = final

            return final if final is None else Data.NODES[n_id]['Boost_Time']

    def get_operation_modes(self):
        """Get heating list of possible modes."""
        return ["SCHEDULE", "MANUAL", "OFF"]

    def get_schedule_now_next_later(self, n_id):
        """Hive get heating schedule now, next and later."""
        from pyhiveapi.hive_session import Session
        current_mode = self.get_mode(n_id)
        snan = None

        if n_id in Data.products and current_mode == "SCHEDULE":
            data = Data.products
            snan = Session.p_get_schedule_now_next_later(Session,
                                                         data["state"]["schedule"])

        return snan

    def set_target_temperature(self, n_id, new_temp):
        """Set heating target temperature."""
        from pyhiveapi.hive_session import Session
        Session.check_hive_api_logon(Session())
        final = False

        if n_id in Data.products:
            data = Data.products[n_id]
            resp = self.hive.set_state(Data.sess_id, data[type], n_id,
                                       target=new_temp)

            if str(resp['original']) == "<Response [200]>":
                Session.hive_api_get_nodes(Session(), n_id)
                final = True

        return final

    def set_mode(self, n_id, new_mode):
        """Set heating mode."""
        from pyhiveapi.hive_session import Session
        Session.check_hive_api_logon(Session())
        final = False

        if n_id in Data.products:
            data = Data.products[n_id]
            resp = self.hive.set_state(Data.sess_id, data[type], n_id,
                                       mode=new_mode)

            if str(resp['original']) == "<Response [200]>":
                Session.hive_api_get_nodes(Session(), n_id)
                final = True

        return final

    def turn_boost_on(self, n_id, mins, temp):
        """Turn heating boost on."""
        if mins > 0 and temp >= self.min_temperature():
            if temp <= self.max_temperature():
                from pyhiveapi.hive_session import Session
                Session.check_hive_api_logon(Session())
                final = False

                if n_id in Data.products:
                    data = Data.products[n_id]
                    resp = self.hive.set_state(Data.sess_id, data[type], n_id,
                                               mode='BOOST', boost=mins, target=temp)

                    if str(resp['original']) == "<Response [200]>":
                        Session.hive_api_get_nodes(Session(), n_id)
                        final = True

                return final

    def turn_boost_off(self, n_id):
        """Turn heating boost off."""
        from pyhiveapi.hive_session import Session
        Session.check_hive_api_logon(Session())
        final = False

        if n_id in Data.products:
            data = Data.products
            Session.hive_api_get_nodes(Session(), n_id)
            if self.get_boost(n_id) == "ON":
                prev_mode = data["props"]["previous"]["mode"]
                if prev_mode == "MANUAL":
                    prev_temp = data["props"]["previous"]["target"]
                    resp = self.hive.set_state(Data.sess_id, data[type], n_id,
                                               mode=prev_mode, target=prev_temp)
                else:
                    resp = self.hive.set_state(Data.sess_id, data[type], n_id,
                                               mode=prev_mode)
                if str(resp['original']) == "<Response [200]>":
                    Session.hive_api_get_nodes(Session(), n_id)
                    final = True

        return final
