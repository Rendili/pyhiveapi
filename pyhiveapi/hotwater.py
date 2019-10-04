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
        self.log.log(n_id, self.type, "Getting mode")
        state = self.attr.online_offline(n_id)
        final = None

        if n_id in Data.products:
            if state != "Offline":
                data = Data.products[n_id]
                state = data["state"]["mode"]
                if state == "BOOST":
                    state = data["props"]["previous"]["mode"]
                final = Data.HIVETOHA[self.type].get(state, state)
                self.log.log(n_id, self.type, "Mode is {0}", info=final)
            self.log.error_check(n_id, self.type, state)
            final = Data.HIVETOHA[self.type].get(state, state)
            Data.NODES[n_id]["Mode"] = final
        else:
            self.log.error_check(n_id, "ERROR", "Failed")

        return final if final is None else Data.NODES[n_id]["Mode"]

    @staticmethod
    def get_operation_modes():
        """Get heating list of possible modes."""
        return ["SCHEDULE", "ON", "OFF"]

    def get_boost(self, n_id):
        """Get hot water current boost status."""
        self.log.log(n_id, self.type, "Getting boost")
        state = self.attr.online_offline(n_id)
        final = None

        if n_id in Data.products:
            if state != "Offline":
                data = Data.products[n_id]
                state = data["state"]["boost"]
                final = Data.HIVETOHA["Boost"].get(state, "ON")
                self.log.log(n_id, self.type, "Boost is {0}", info=final)
            self.log.error_check(n_id, self.type, state)
            final = Data.HIVETOHA["Boost"].get(state, "ON")
            Data.NODES[n_id]["Boost"] = final
        else:
            self.log.error_check(n_id, "ERROR", "Failed")

        return final if final is None else Data.NODES[n_id]["Boost"]

    def get_boost_time(self, n_id):
        """Get hotwater boost time remaining."""
        if self.get_boost(n_id) == "ON":
            self.log.log(n_id, self.type, "Getting boost time")
            state = self.attr.online_offline(n_id)
            final = None

            if n_id in Data.products:
                if state != "Offline":
                    data = Data.products[n_id]
                    state = data["state"]["boost"]
                    self.log.log(n_id, self.type, "Boost time is {0}", info=state)
                self.log.error_check(n_id, self.type, state)
                final = state
                Data.NODES[n_id]["Boost_Time"] = final
            else:
                self.log.error_check(n_id, "ERROR", "Failed")

            return final if final is None else Data.NODES[n_id]["Boost_Time"]

    def get_state(self, n_id):
        """Get hot water current state."""
        from pyhiveapi.hive_session import Session

        self.log.log(n_id, self.type, "Getting state")
        state = self.attr.online_offline(n_id)
        final = None

        if n_id in Data.products:
            if state != "Offline":
                data = Data.products[n_id]
                state = data["state"]["status"]
                mode_current = self.get_mode(n_id)
                if mode_current == "SCHEDULE":
                    if self.get_boost(n_id) == "ON":
                        state = "ON"
                    else:
                        snan = Session.p_get_schedule_nnl(
                            Session(), data["state"]["schedule"]
                        )
                        state = snan["now"]["value"]["status"]
            self.log.error_check(n_id, self.type, state)
            final = Data.HIVETOHA[self.type].get(state, state)
            Data.NODES[n_id]["State"] = final
        else:
            self.log.error_check(n_id, "ERROR", "Failed")

        return final if final is None else Data.NODES[n_id]["State"]

    def get_schedule_now_next_later(self, n_id):
        """Hive get hotwater schedule now, next and later."""
        from pyhiveapi.hive_session import Session

        self.log.log(n_id, self.type, "Getting schedule info.")
        state = self.attr.online_offline(n_id)
        final = None

        if n_id in Data.products:
            Session.check_hive_api_logon(Session())
            mode_current = self.get_mode(n_id)
            if state != "Offline" and mode_current == "SCHEDULE":
                data = Data.products[n_id]
                state = Session.p_get_schedule_nnl(Session(), data["state"]["schedule"])
                final = state
                Data.NODES[n_id]["snnl"] = final
                self.log.log(n_id, self.type, "Schedule is {0}", info=final)
            self.log.error_check(n_id, self.type, state)
        else:
            self.log.error_check(n_id, "ERROR", "Failed")

        return final

    def set_mode(self, n_id, new_mode):
        """Set hot water mode."""
        from pyhiveapi.hive_session import Session

        self.log.log(n_id, self.type, "Setting Mode")
        final = False

        if n_id in Data.products:
            Session.check_hive_api_logon(Session())
            data = Data.products[n_id]
            resp = self.hive.set_state(Data.sess_id, data[type], n_id, mode=new_mode)
            if str(resp["original"]) == "<Response [200]>":
                final = True
                Session.hive_api_get_nodes(Session(), n_id)
                self.log.log(
                    n_id, "API", "Mode set to {0} - API response 200", info=new_mode
                )
            else:
                self.log.error_check(n_id, "ERROR", "Failed_API", resp=resp["original"])

            return final

    def turn_boost_on(self, n_id, mins):
        """Turn hot water boost on."""
        from pyhiveapi.hive_session import Session

        self.log.log(n_id, self.type, "Turning on boost")
        final = False

        if mins > 0 and n_id in Data.products:
            Session.check_hive_api_logon(Session())
            data = Data.products[n_id]
            resp = self.hive.set_state(
                Data.sess_id, data["type"], n_id, mode="BOOST", boost=mins
            )
            if str(resp["original"]) == "<Response [200]>":
                final = True
                Session.hive_api_get_nodes(Session(), n_id)
                self.log.log(n_id, "API", "Boost on - API response 200")
            else:
                self.log.error_check(n_id, "ERROR", "Failed_API", resp=resp["original"])

        return final

    def turn_boost_off(self, n_id):
        """Turn hot water boost off."""
        from pyhiveapi.hive_session import Session

        self.log.log(n_id, self.type, "Turning off boost")
        final = False

        if n_id in Data.products and self.get_boost(n_id) == "ON":
            Session.check_hive_api_logon(Session())
            data = Data.products[n_id]
            prev_mode = data["props"]["previous"]["mode"]
            resp = self.hive.set_state(Data.sess_id, data["type"], n_id, mode=prev_mode)
            if str(resp["original"]) == "<Response [200]>":
                Session.hive_api_get_nodes(Session(), n_id)
                final = True
                self.log.log(n_id, "API", "Boost off - API response 200")
            else:
                self.log.error_check(n_id, "ERROR", "Failed_API", resp=resp["original"])

        return final
