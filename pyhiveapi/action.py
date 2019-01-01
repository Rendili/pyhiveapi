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

    def get_state(self, id):
        """Get action state."""
        self.log.log('action', "Getting state of action: " +
                     Data.NAME[id])
        end = False

        if id in Data.actions:
            data = Data.actions[id]
            end = data["enabled"]
            Data.NODES["Action_State_" + id] = end
            self.log.log('action', "State for " + Data.NAME[id] +
                         " is : " + str(end))
        else:
            self.log.log('sensor', "Failed to get state for " + Data.NAME[id])

        return end if end is False else Data.NODES.get("Action_State_" + id)

    def turn_on(self, id):
        """Set action turn on."""
        from pyhiveapi.hive_session import Session
        self.log.log('action', "Enabling action : " + Data.NAME[id])
        resp = None
        end = False
        Session.check_hive_api_logon(Session())
        data = Data.actions[id]

        data.update({"enabled": "true"})
        resp = self.hive.set_state(Data.sess_id, "action", id, data)
        if str(resp['original']) == "<Response [200]>":
            end = True
            Session.hive_api_get_nodes(Session(), id, False)
            self.log.log("action", "Action  " + Data.NAME[id] +
                         " has been successfully enabled")
        else:
            self.log.log("action", "Failed to enable on action: " +
                         Data.NAME[id])

        return end

    def turn_off(self, id):
        """Set action to turn off."""
        from pyhiveapi.hive_session import Session
        self.log.log('action', "Diabling off action : " + Data.NAME[id])
        resp = None
        end = False
        Session.check_hive_api_logon(Session())
        data = Data.actions[id]

        data.update({"enabled": "false"})
        resp = self.hive.set_state(Data.sess_id, data['type'], id, data)
        if str(resp['original']) == "<Response [200]>":
            end = True
            Session.hive_api_get_nodes(Session(), id, False)
            self.log.log("action", "Action  " + Data.NAME[id] +
                         " has been successfully disabiled on")
        else:
            self.log.log("action", "Failed to disable on action: " +
                         Data.NAME[id])
