"""Hive Action Module."""
from pyhiveapi.custom_logging import Logger
from pyhiveapi.device_attributes import Attributes
from pyhiveapi.hive_api import Hive
from pyhiveapi.hive_data import Data


class Action:
    """Hive Action Code."""

    def __init__(self):
        """Initialise."""
        self.hive = Hive()
        self.log = Logger()
        self.attr = Attributes()
        self.type = "Action"

    def get_state(self, n_id):
        """Get action state."""
        self.log.log(n_id, self.type, "Getting state")
        final = None

        if n_id in Data.actions:
            data = Data.actions[n_id]
            final = data["enabled"]
            Data.NODES[n_id]["State"] = final
            self.log.log(n_id, self.type, "Status is {0}", info=final)
        else:
            self.log.error_check(n_id, "ERROR", "Failed")

        return final if final is None else Data.NODES[n_id].get("State")

    def turn_on(self, n_id):
        """Set action turn on."""
        from pyhiveapi.hive_session import Session
        import json

        self.log.log(n_id, self.type, "Enabling action")
        final = False

        if n_id in Data.actions:
            Session.check_hive_api_logon(Session())
            data = Data.actions[n_id]
            data.update({"enabled": True})
            send = json.dumps(data)
            resp = self.hive.set_action(Data.sess_id, n_id, send)
            if str(resp["original"]) == "<Response [200]>":
                final = True
                Session.hive_api_get_nodes(Session(), n_id)
                self.log.log(n_id, "API", "Enabled action - API response 200")
            else:
                self.log.error_check(n_id, "ERROR", "Failed_API", resp=resp["original"])

        return final

    def turn_off(self, n_id):
        """Set action to turn off."""
        from pyhiveapi.hive_session import Session
        import json

        self.log.log(n_id, self.type, "Disabling action")
        final = False

        if n_id in Data.actions:
            Session.check_hive_api_logon(Session())
            data = Data.actions[n_id]
            data.update({"enabled": False})
            send = json.dumps(data)
            resp = self.hive.set_action(Data.sess_id, n_id, send)
            if str(resp["original"]) == "<Response [200]>":
                final = True
                Session.hive_api_get_nodes(Session(), n_id)
                self.log.log(n_id, "API", "Disabled action - API response 200")
            else:
                self.log.error_check(n_id, "ERROR", "Failed_API", resp=resp["original"])

        return final
