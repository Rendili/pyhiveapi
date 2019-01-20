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

    def get_state(self, n_id):
        """Get action state."""
        self.log.log('action', "Getting state of action: " +
                     Data.NAME[n_id])
        end = False

        if n_id in Data.actions:
            data = Data.actions[n_id]
            end = data["enabled"]
            Data.NODES["Action_State_" + n_id] = end
            self.log.log('action', "State for " + Data.NAME[n_id] +
                         " is : " + str(end))
        else:
            self.log.log('sensor', "Failed to get state for " + Data.NAME[n_id])

        return end if end is False else Data.NODES.get("Action_State_" + n_id)

    def turn_on(self, n_id):
        """Set action turn on."""
        from pyhiveapi.hive_session import Session
        self.log.log('action', "Enabling action : " + Data.NAME[n_id])
        end = False
        Session.check_hive_api_logon(Session())
        data = Data.actions[n_id]

        data.update({"enabled": "true"})
        resp = self.hive.set_action(Data.sess_id, n_id, data)
        if str(resp['original']) == "<Response [200]>":
            end = True
            Session.hive_api_get_nodes(Session(), n_id)
            self.log.log("action", "Action  " + Data.NAME[n_id] +
                         " has been successfully enabled")
        else:
            self.log.log("action", "Failed to enable on action: " +
                         Data.NAME[n_id])

        return end

    def turn_off(self, n_id):
        """Set action to turn off."""
        from pyhiveapi.hive_session import Session
        self.log.log('action', "Diabling off action : " + Data.NAME[n_id])
        final = False

        if n_id in Data.products:
            Session.check_hive_api_logon(Session())
            data = Data.actions[n_id]

            data.update({"enabled": "false"})
            resp = self.hive.set_action(Data.sess_id, n_id, data)
            if str(resp['original']) == "<Response [200]>":
                final = True
                Session.hive_api_get_nodes(Session(), n_id)
                self.log.log("action", "Action  " + Data.NAME[n_id] +
                             " has been successfully disabiled on")
            else:
                self.log.log("action", "Failed to disable on action: " +
                             Data.NAME[n_id])
        return final
