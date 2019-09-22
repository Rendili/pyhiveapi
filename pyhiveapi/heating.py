""""Hive Heating Module. """
from pyhiveapi.custom_logging import Logger
from pyhiveapi.device_attributes import Attributes
from datetime import datetime
from pyhiveapi.hive_api import Hive
from pyhiveapi.hive_data import Data


class Heating:
    """Hive Heating Code."""

    def __init__(self):
        """Initialise."""
        self.hive = Hive()
        self.log = Logger()
        self.attr = Attributes()
        self.type = "Heating"

    @staticmethod
    def min_temperature():
        """Get heating minimum target temperature."""
        return 5

    @staticmethod
    def max_temperature():
        """Get heating maximum target temperature."""
        return 32

    def current_temperature(self, n_id):
        """Get heating current temperature."""
        from datetime import datetime
        self.log.log(n_id, self.type, "Getting current temp")
        state = self.attr.online_offline(n_id)
        final = None

        if n_id in Data.products:
            if state != 'Offline':
                data = Data.products[n_id]
                state = data["props"]["temperature"]

                if n_id in Data.p_minmax:
                    if Data.p_minmax[n_id]['TodayDate'] != datetime.date(
                            datetime.now()):
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
                    data = {'TodayMin': state, 'TodayMax': state,
                            'TodayDate': str(datetime.date(datetime.now())),
                            'RestartMin': state, 'RestartMax': state}
                    Data.p_minmax[n_id] = data
                f_state = round(float(state), 1)
                self.log.log(n_id, self.type, "Current Temp is {0}",
                             info=str(state))
            self.log.error_check(n_id, self.type, state)
            final = f_state
            Data.NODES[n_id]['CurrentTemp'] = final
        else:
            self.log.error_check(n_id, 'ERROR', 'Failed')

        return final if final is None else Data.NODES[n_id]['CurrentTemp']

    def minmax_temperatures(self, n_id):
        """Min/Max Temp"""
        self.log.log(n_id, self.type, "Getting Min/Max temp")
        state = self.attr.online_offline(n_id)
        final = None

        if n_id in Data.p_minmax:
            if state != 'Offline':
                state = Data.p_minmax[n_id]
                self.log.log(n_id, self.type, "Min/Max is {0}", info=state)
            self.log.error_check(n_id, self.type, state)
            final = state
            Data.NODES[n_id]['minmax'] = final
        else:
            self.log.error_check(n_id, 'ERROR', 'Failed')

        return final if final is None else Data.NODES[n_id]['minmax']

    def get_target_temperature(self, n_id):
        """Get heating target temperature."""
        self.log.log(n_id, self.type, "Getting target temp")
        state = self.attr.online_offline(n_id)
        final = None

        if n_id in Data.products:
            if state != 'Offline':
                data = Data.products[n_id]
                state = round(float(data["state"]["target"]), 1)
                self.log.log(n_id, self.type, "Target temp is {0}",
                             info=str(state))
            self.log.error_check(n_id, self.type, state)
            final = state
            Data.NODES[n_id]['TargetTemp'] = final
        else:
            self.log.error_check(n_id, 'ERROR', 'Failed')

        return final if final is None else Data.NODES[n_id]['TargetTemp']

    def get_mode(self, n_id):
        """Get heating current mode."""
        self.log.log(n_id, self.type, "Getting mode")
        state = self.attr.online_offline(n_id)
        final = None

        if n_id in Data.products:
            if state != 'Offline':
                data = Data.products[n_id]
                state = data["state"]["mode"]
                if state == "BOOST":
                    state = data["props"]["previous"]["mode"]
                self.log.log(n_id, self.type, "Mode is {0}", info=str(state))
            self.log.error_check(n_id, self.type, state)
            final = Data.HIVETOHA[self.type].get(state, state)
            Data.NODES[n_id]['Mode'] = final
        else:
            self.log.error_check(n_id, 'ERROR', 'Failed')

        return final if final is None else Data.NODES[n_id]['Mode']

    def get_state(self, n_id):
        """Get heating current state."""
        self.log.log(n_id, self.type, "Getting state")
        state = self.attr.online_offline(n_id)
        final = None

        if n_id in Data.products:
            if state != 'Offline':
                current_temp = self.current_temperature(n_id)
                target_temp = self.get_target_temperature(n_id)
                if current_temp < target_temp:
                    state = "ON"
                else:
                    state = "OFF"
                self.log.log(n_id, self.type, "State is {0}", info=str(state))
            self.log.error_check(n_id, self.type, state)
            final = Data.HIVETOHA[self.type].get(state, state)
            Data.NODES[n_id]['State'] = final
        else:
            self.log.error_check(n_id, 'ERROR', 'Failed')

        return final if final is None else Data.NODES[n_id]['State']

    def get_boost(self, n_id):
        """Get heating boost current status."""
        self.log.log(n_id, self.type, "Getting boost status")
        state = self.attr.online_offline(n_id)
        final = None

        if n_id in Data.products:
            if state != 'Offline':
                data = Data.products[n_id]
                state = Data.HIVETOHA['Boost'].get(data["state"]["boost"],
                                                   'ON')
                self.log.log(n_id, self.type, "Boost state is {0}",
                             info=str(state))
            self.log.error_check(n_id, self.type, state)
            final = state
            Data.NODES[n_id]['Boost'] = final
        else:
            self.log.error_check(n_id, 'ERROR', 'Failed')

        return final if final is None else Data.NODES[n_id]['Boost']

    def get_boost_time(self, n_id):
        """Get heating boost time remaining."""
        if self.get_boost(n_id) == 'ON':
            self.log.log(n_id, self.type, "Getting boost time")
            state = self.attr.online_offline(n_id)
            final = None

            if n_id in Data.products:
                if state != 'Offline':
                    data = Data.products[n_id]
                    state = data["state"]["boost"]
                    self.log.log(n_id, self.type, "Time left on boost is {0}",
                                 info=str(state))
                self.log.error_check(n_id, self.type, state)
                final = state
                Data.NODES[n_id]['Boost_Time'] = final
            else:
                self.log.error_check(n_id, 'ERROR', 'Failed')

            return final if final is None else Data.NODES[n_id]['Boost_Time']
        return None

    @staticmethod
    def get_operation_modes():
        """Get heating list of possible modes."""
        return ["SCHEDULE", "MANUAL", "OFF"]

    def get_schedule_now_next_later(self, n_id):
        """Hive get heating schedule now, next and later."""
        from pyhiveapi.hive_session import Session
        self.log.log(n_id, self.type, "Getting schedule")
        state = self.attr.online_offline(n_id)
        current_mode = self.get_mode(n_id)
        final = None

        if n_id in Data.products:
            if state != 'Offline' and current_mode == "SCHEDULE":
                data = Data.products[n_id]
                state = Session.p_get_schedule_nnl(Session(),
                                                   (data["state"]
                                                    ["schedule"]))
                self.log.log(n_id, self.type, "Schedule is {0}",
                             info=str(state))
            self.log.error_check(n_id, self.type, state)
            final = state
            Data.NODES[n_id]['snnl'] = final
        else:
            self.log.error_check(n_id, 'ERROR', 'Failed')

        return final if final is None else Data.NODES[n_id]['snnl']

    def set_target_temperature(self, n_id, new_temp):
        """Set heating target temperature."""
        from pyhiveapi.hive_session import Session
        final = False

        if n_id in Data.products:
            Session.check_hive_api_logon(Session())
            data = Data.products[n_id]
            resp = self.hive.set_state(Data.sess_id, data['type'], n_id,
                                       target=new_temp)

            if str(resp['original']) == "<Response [200]>":
                Session.hive_api_get_nodes(Session(), n_id)
                final = True
                self.log.log(n_id, 'API', "Temperature set - API response 200")
            else:
                self.log.error_check(n_id, 'ERROR', 'Failed_API',
                                     resp=resp['original'])

        return final

    def set_mode(self, n_id, new_mode):
        """Set heating mode."""
        from pyhiveapi.hive_session import Session
        Session.check_hive_api_logon(Session())
        final = False

        if n_id in Data.products:
            data = Data.products[n_id]
            resp = self.hive.set_state(Data.sess_id, data['type'], n_id,
                                       mode=new_mode)

            if str(resp['original']) == "<Response [200]>":
                Session.hive_api_get_nodes(Session(), n_id)
                final = True
                self.log.log(n_id, 'API', "Mode updated - API response 200")
            else:
                self.log.error_check(n_id, 'ERROR', 'Failed_API',
                                     resp=resp['original'])

        return final

    def turn_boost_on(self, n_id, mins, temp):
        """Turn heating boost on."""
        if mins > 0 and temp >= self.min_temperature():
            if temp <= self.max_temperature():
                self.log.log(self.type, "Enabling boost for {0}", n_id)
                from pyhiveapi.hive_session import Session
                Session.check_hive_api_logon(Session())
                final = False

                if n_id in Data.products:
                    data = Data.products[n_id]
                    resp = self.hive.set_state(Data.sess_id, data['type'],
                                               n_id, mode='BOOST', boost=mins,
                                               target=temp)

                    if str(resp['original']) == "<Response [200]>":
                        Session.hive_api_get_nodes(Session(), n_id)
                        final = True
                        self.log.log(n_id, 'API', "Boost enabled - " +
                                     "API response 200")
                    else:
                        self.log.error_check(n_id, 'ERROR', 'Failed_API',
                                             resp=resp['original'])

                return final
        return None

    def turn_boost_off(self, n_id):
        """Turn heating boost off."""
        from pyhiveapi.hive_session import Session
        self.log.log(self.type, "Disabling boost for {0}", n_id)
        final = False

        if n_id in Data.products:
            Session.check_hive_api_logon(Session())
            data = Data.products
            Session.hive_api_get_nodes(Session(), n_id)
            if self.get_boost(n_id) == "ON":
                prev_mode = data["props"]["previous"]["mode"]
                if prev_mode == "MANUAL":
                    pre_temp = data["props"]["previous"].get('target', 7)
                    resp = self.hive.set_state(Data.sess_id, data[type], n_id,
                                               mode=prev_mode, target=pre_temp)
                else:
                    resp = self.hive.set_state(Data.sess_id, data[type], n_id,
                                               mode=prev_mode)
                if str(resp['original']) == "<Response [200]>":
                    Session.hive_api_get_nodes(Session(), n_id)
                    final = True
                    self.log.log(n_id, 'API', "Boost disabled - " +
                                 "API response 200")
                else:
                    self.log.error_check(n_id, 'ERROR', 'Failed_API',
                                         resp=resp['original'])

        return final
