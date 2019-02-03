"""Hive Device Attribute Module."""
from pyhiveapi.custom_logging import Logger
from pyhiveapi.hive_data import Data


class Attributes:
    """Device Attributes Code."""

    def __init__(self):
        self.log = Logger()
        self.type = "Attribute"

    def state_attributes(self, n_id):
        """Get HA State Attributes"""
        from pyhiveapi.hive_session import Session
        self.log.log(n_id, self.type, "Getting state_attributes")
        attr = {}

        if n_id in Data.products:
            attr.update({"availability": (self.online_offline(n_id))})
            if n_id in Data.BATTERY:
                attr.update({"battery_level": str(self.battery(n_id)) + '%'})
            if n_id in Data.MODE:
                attr.update({"mode": (self.get_mode(n_id))})

            data = Data.products[n_id]
            if data['type'] in Data.types['Sensor']:
                s = str(data['props']['statusChanged'])
                t = '{:10.10}'.format(s)
                time = Session.epochtime(t, '%d-%m-%Y %H:%M:%S','from_epoch')
                attr.update({'state_changed': time})

        return attr

    def online_offline(self, n_id):
        """Check if device is online"""
        self.log.log(n_id, self.type, "Checking device availability")
        final = None

        if n_id in Data.devices:
            data = Data.devices[n_id]
            state = data["props"]["online"]
            final = Data.HIVETOHA[self.type].get(state, 'UNKNOWN')
            Data.NODES[n_id]['Availability'] = final
            self.log.log(n_id, self.type, "Device is {0}", info=str(final))
        else:
            self.log.error_check(n_id, 'ERROR', 'Failed')

        return final if final is None else Data.NODES[n_id]['Availability']

    def get_mode(self, n_id):
        """Get sensor mode."""
        self.log.log(n_id, self.type, "Getting mode of device")
        state = self.online_offline(n_id)
        final = None

        if n_id in Data.products:
            if state != 'Offline':
                data = Data.products[n_id]
                state = data["state"]["mode"]
                self.log.log(n_id, self.type, "Mode is {0}", info=str(final))
            self.log.error_check(n_id, self.type, state)
            final = Data.HIVETOHA[self.type].get(state, state)
            Data.NODES[n_id]["Device_Mode"] = final
        else:
            self.log.error_check(n_id, 'ERROR', 'Failed')

        return final if final is None else Data.NODES[n_id]['Device_Mode']

    def battery(self, n_id):
        """Get device battery level."""
        self.log.log(n_id, self.type, "Checking battery level")
        state = self.online_offline(n_id)
        final = None

        if n_id in Data.devices:
            if state != 'Offline':
                data = Data.devices[n_id]
                state = data["props"]["battery"]
                final = state
                Data.NODES[n_id]["BatteryLevel"] = final
                self.log.log(n_id, self.type, "Battery level is", info=final)
            self.log.error_check(n_id, self.type, state)
        else:
            self.log.error_check(n_id, 'ERROR', 'Failed')

        return final if final is None else Data.NODES[n_id]['BatteryLevel']
