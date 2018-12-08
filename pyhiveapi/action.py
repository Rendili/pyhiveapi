"""Hive Action Module."""
from pyhiveapi.hive_api import Hive
from pyhiveapi.hive_data import Data
from pyhiveapi.custom_logging import Logger
from pyhiveapi.device_attributes import Attributes


class Action:
    """Hive Action Code."""
    def __init__(self):
        """Initialise."""
        self.hive = Hive()
        self.log = Logger()
        self.attr = Attributes()
        self.type = "Action"

    def get_state(self, n):
        """Get action state."""
        self.log.log('action', "Getting state of action: " +
                     Data.NAME[n])
        end = False

        if n in Data.actions:
            data = Data.actions[n]
            end = data["enabled"]
            Data.NODES["Action_State_" + n] = end
            self.log.log('action', "State for " + Data.NAME[n] +
                         " is : " + str(end))
        else:
            self.log.log('sensor', "Failed to get state for " + Data.NAME[n])

        return end if end is False else Data.NODES.get("Action_State_" + n)

    def turn_on(self, n):
        """Set action turn on."""
        from pyhiveapi.hive_session import Session
        self.log.log('action', "Enabling action : " + Data.NAME[n])
        resp = None
        end = False
        Session.check_hive_api_logon(Session())
        data = Data.actions[n]

        data.update({"enabled": "true"})
        resp = self.hive.set_state(Data.sess_id, data['type'], n, data)
        if str(resp['original']) == "<Response [200]>":
            end = True
            Session.hive_api_get_nodes(Session(), n, False)
            self.log.log("action", "Action  " + Data.NAME[n] +
                         " has been successfully enabled")
        else:
            self.log.log("action", "Failed to enable on action: " +
                         Data.NAME[n])

        return end

    def turn_off(self, n):
        """Set action to turn off."""
        from pyhiveapi.hive_session import Session
        self.log.log('action', "Diabling off action : " + Data.NAME[n])
        resp = None
        end = False
        Session.check_hive_api_logon(Session())
        data = Data.actions[n]

        data.update({"enabled": "false"})
        resp = self.hive.set_state(Data.sess_id, data['type'], n, data)
        if str(resp['original']) == "<Response [200]>":
            end = True
            Session.hive_api_get_nodes(Session(), n, False)
            self.log.log("action", "Action  " + Data.NAME[n] +
                         " has been successfully disabiled on")
        else:
            self.log.log("action", "Failed to disable on action: " +
                         Data.NAME[n])
