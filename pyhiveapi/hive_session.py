""" Hive Session Module."""
import operator
import threading
import time
from datetime import datetime, timedelta

from pyhiveapi.custom_logging import Logger
from pyhiveapi.hive_api import Hive
from pyhiveapi.hive_data import Data
from pyhiveapi.weather import Weather
from pyhiveapi.hub import Hub
from pyhiveapi.device_attributes import Attributes

MINUTES_BETWEEN_LOGONS = 15


class Session:
    """Hive Session Code"""

    def __init__(self):
        """Initialise the base variable values."""
        self.lock = threading.Lock()
        self.api = Hive()
        self.log = Logger()
        self.type = 'Session'

    def hive_api_logon(self):
        """Log in to the Hive API and get the Session Data."""
        self.log.log('No_ID', self.type, "Attempting to login to Hive.")

        login_details_found = False
        try_finished = False

        resp_p = self.api.login(Data.s_username, Data.s_password)

        if resp_p['original'] == "<Response [200]>":
            info = resp_p['parsed']
            if ('token' in info and 'user' in info and
                'platform' in info):
                Data.sess_id = info['token']
                Data.s_logon_datetime = datetime.now()
                login_details_found = True

                if 'endpoint' in info['platform']:
                    self.api.urls.update({'base': info['platform'][
                        'endpoint']})

                if 'name' in info['platform']:
                    Data.s_platform_name = info['platform']['name']

                if 'locale' in info['user']:
                    Data.s_locale = info['user']['locale']

                if 'countryCode' in info['user']:
                    Data.s_countrycode = info['user']['countryCode']

                if 'timezone' in info['user']:
                    Data.s_timezone = info['user']['timezone']

                if 'postcode' in info['user']:
                    Data.s_postcode = info['user']['postcode']

                if 'temperatureUnit' in info['user']:
                    Data.s_temperature_unit = info['user'][
                        'temperatureUnit']

    def check_hive_api_logon(self):
        """Check if currently logged in with a valid Session IData."""
        self.log.log('No_ID', self.type, "Checking Hive token is valid.")

        if Data.s_file is False:
            c_time = datetime.now()
            l_logon_secs = (c_time - Data.s_logon_datetime).total_seconds()
            l_logon_mins = int(round(l_logon_secs / 60))

            if l_logon_mins >= MINUTES_BETWEEN_LOGONS or Data.sess_id is None:
                self.hive_api_logon()

    def update_data(self, n_id):
        """Get latest data for Hive nodes - rate limiting."""
        self.lock.acquire()
        self.log.check_logging(False)
        try:
            updated = False
            ct = datetime.now()
            last_update_secs = (ct - Data.s_last_update).total_seconds()
            if last_update_secs >= Data.s_interval_seconds:
                updated = self.hive_api_get_nodes(n_id)

            w_last_update_secs = (ct - Data.w_last_update).total_seconds()
            if w_last_update_secs >= Data.w_interval_seconds:
                updated = self.hive_api_get_weather()
        finally:
            self.lock.release()

        return updated

    def hive_api_get_nodes_nl(self, **kwargs):
        """Get latest data for Hive nodes - not rate limiting."""
        file = kwargs.get('file', False)
        if file:
            Data.s_file = True
            Data.t_file = file

        self.log.log('No_ID', self.type, "Getting first set of data from Hive")
        self.hive_api_get_nodes("NoID")

    def hive_api_get_nodes(self, n_id):
        """Get latest data for Hive nodes."""
        get_nodes_successful = False
        api_resp_d = None
        self.log.log(n_id, self.type, "Getting data from Hive.")

        self.check_hive_api_logon()
        try:
            if Data.s_file:
                api_resp_d = Data.t_file['devices']
            elif Data.sess_id is not None:
                api_resp_d = self.api.get_devices(Data.sess_id)

                api_resp = str(api_resp_d['original'])
                if api_resp == "<Response [200]>":
                    self.log.log(n_id, 'API', "Devices - API response 200")
                else:
                    self.log.error_check(n_id, 'ERROR', 'Failed_API',
                                         resp=api_resp)

            api_resp_p = api_resp_d['parsed']

            for a_device in api_resp_p:
                if 'id' in a_device:
                    Data.devices.update({a_device['id']: a_device})
                    Data.NODES.update({a_device['id']: {'': ''}})
            try_finished_devices = True
        except (IOError, RuntimeError, ZeroDivisionError, ConnectionError):
            self.log.log('No_ID', 'Core_API', "Api didnt receive any data")
            try_finished_devices = False

        try:
            api_resp = None
            resp = None
            if Data.s_file:
                resp = Data.t_file['products']
            elif Data.sess_id is not None:
                resp = self.api.get_products(Data.sess_id)
                if api_resp == "<Response [200]>":
                    self.log.log(n_id, 'API', "Products - API response 200")
                else:
                    self.log.error_check(n_id, 'ERROR', 'Failed_API',
                                         resp=api_resp)

            for a_product in resp['parsed']:
                if 'id' in a_product:
                    Data.products.update({a_product['id']: a_product})
                    Data.NODES.update({a_product['id']: {'': ''}})
            try_finished_products = True
        except (IOError, RuntimeError, ZeroDivisionError, ConnectionError):
            try_finished_products = False

        try:
            api_resp = None
            resp = None
            if Data.s_file:
                resp = Data.t_file['actions']
            elif Data.sess_id is not None:
                resp = self.api.get_actions(Data.sess_id)
                if api_resp == "<Response [200]>":
                    self.log.log(n_id, 'API', "Actions - API response 200")
                else:
                    self.log.error_check(n_id, 'ERROR', 'Failed_API',
                                         resp=api_resp)

            for a_action in resp['parsed']:
                if 'id' in a_action:
                    Data.actions.update({a_action['id']: a_action})
                    Data.NODES.update({a_action['id']: {'': ''}})
            try_finished_actions = True
        except (IOError, RuntimeError, ZeroDivisionError, ConnectionError):
            try_finished_actions = False

        if try_finished_devices and try_finished_products \
                and try_finished_actions:
            get_nodes_successful = True
            Data.s_last_update = datetime.now()

        return get_nodes_successful

    def hive_api_get_weather(self):
        """Get latest weather data from Hive."""
        self.log.log('No_ID', self.type, "Getting Hive weather info.")

        get_weather_successful = True
        current_time = datetime.now()
        self.check_hive_api_logon()

        try:
            if Data.sess_id is not None:
                weather_url = "?postcode=" + Data.s_postcode \
                              + "&country=" + Data.s_countrycode

                resp = self.api.get_weather(weather_url, Data.sess_id)
                if "weather" in resp['parsed']:
                    if "icon" in resp['parsed']["weather"]:
                        Data.w_icon = resp['parsed']["weather"]["icon"]
                    if "description" in resp['parsed']["weather"]:
                        Data.w_description = resp['parsed']["weather"]["description"]
                    if "temperature" in resp['parsed']["weather"]:
                        if "unit" in resp['parsed']["weather"]["temperature"]:
                            Data.w_temperature_unit = resp['parsed']["weather"][
                                "temperature"]["unit"]
                        if "unit" in resp['parsed']["weather"]["temperature"]:
                            Data.w_temperature_value = resp['parsed']["weather"][
                                "temperature"]["value"]
                    Data.w_nodeid = "HiveWeather"
                else:
                    get_weather_successful = False

            Data.w_last_update = current_time
        except (IOError, RuntimeError, ZeroDivisionError):
            get_weather_successful = False

        return get_weather_successful

    @staticmethod
    def p_minutes_to_time(minutes_to_convert):
        """Convert minutes string to datetime."""
        hours_converted, minutes_converted = divmod(minutes_to_convert, 60)
        converted_time = datetime.strptime(str(hours_converted) +
                                           ":" +
                                           str(minutes_converted),
                                           "%H:%M")
        converted_time_string = converted_time.strftime("%H:%M")
        return converted_time_string

    @staticmethod
    def p_get_schedule_nnl(self, hive_api_schedule):
        """Get the schedule now, next and later of a given nodes schedule."""
        schedule_now_and_next = {}
        date_time_now = datetime.now()
        date_time_now_day_int = date_time_now.today().weekday()

        days_t = ('monday',
                  'tuesday',
                  'wednesday',
                  'thursday',
                  'friday',
                  'saturday',
                  'sunday')

        days_rolling_list = list(days_t[date_time_now_day_int:] + days_t)[:7]

        full_schedule_list = []

        for day_index in range(0, len(days_rolling_list)):
            current_day_schedule = hive_api_schedule[days_rolling_list[
                day_index]]
            current_day_schedule_sorted = sorted(current_day_schedule,
                                                 key=operator.itemgetter(
                                                     'start'),
                                                 reverse=False)

            for current_slot in range(0, len(current_day_schedule_sorted)):
                current_slot_custom = current_day_schedule_sorted[current_slot]

                slot_date = datetime.now() + timedelta(days=day_index)
                slot_time = self.p_minutes_to_time(current_slot_custom[
                    "start"])
                slot_time_date_s = (slot_date.strftime("%d-%m-%Y") +
                                    " " + slot_time)
                slot_time_date_dt = datetime.strptime(slot_time_date_s,
                                                      "%d-%m-%Y %H:%M")
                if slot_time_date_dt <= date_time_now:
                    slot_time_date_dt = slot_time_date_dt + timedelta(days=7)

                current_slot_custom['Start_DateTime'] = slot_time_date_dt
                full_schedule_list.append(current_slot_custom)

        fsl_sorted = sorted(full_schedule_list,
                            key=operator.itemgetter('Start_DateTime'),
                            reverse=False)

        schedule_now = fsl_sorted[-1]
        schedule_next = fsl_sorted[0]
        schedule_later = fsl_sorted[1]

        schedule_now['Start_DateTime'] = (schedule_now['Start_DateTime'] -
                                          timedelta(days=7))

        schedule_now['End_DateTime'] = schedule_next['Start_DateTime']
        schedule_next['End_DateTime'] = schedule_later['Start_DateTime']
        schedule_later['End_DateTime'] = fsl_sorted[2]['Start_DateTime']

        schedule_now_and_next['now'] = schedule_now
        schedule_now_and_next['next'] = schedule_next
        schedule_now_and_next['later'] = schedule_later

        return schedule_now_and_next

    def initialise_api(self, username, password, interval, **kwargs):
        """Setup the Hive platform."""
        self.log.check_logging(kwargs.get('session', False))
        Data.s_username = username
        Data.s_password = password
        self.log.log('No_ID', self.type, "Initialising Hive Component.")
        tmp_file = kwargs.get('file')

        if interval < 30:
            interval = Data.NODE_INTERVAL_DEFAULT

        if tmp_file is not None:
            self.hive_api_get_nodes_nl(file=tmp_file)
        elif Data.s_username is None or Data.s_password is None:
            return None
        else:
            self.hive_api_logon()
            if Data.sess_id is not None:
                Data.s_interval_seconds = interval
                self.hive_api_get_nodes_nl()
                self.hive_api_get_weather()

        if Data.devices is None or Data.products is None:
            self.log.log('No_ID', self.type, "Failed to get data")

        device_all = {}
        sensor = []
        binary_sensor = []
        climate = []
        light = []
        switch = []

        for a_device in Data.devices:
            if Data.devices[a_device]["type"] in Data.types['Hub']:
                d = Data.devices[a_device]
                try:
                    Data.NAME.update({d["id"]: d["state"]["name"]})
                    sensor.append({'HA_DeviceType': 'Hub_OnlineStatus',
                                   'Hive_NodeID': d["id"],
                                   'Hive_NodeName': d["state"]["name"],
                                   "Hive_DeviceType": "Hub"})
                except KeyError:
                    self.log.log('Hub', self.type, "No data found.")

        for a_product in Data.products:
            if Data.products[a_product]["type"] == 'sense':
                d = Data.products[a_product]
                try:
                    Data.NAME.update({d["id"]: d["state"]["name"]})
                    sensor.append({'HA_DeviceType': 'Hub_SMOKE_CO',
                                   'Hive_NodeID': d["id"],
                                   'Hive_NodeName': d["state"]["name"] +
                                   "Smoke Detection",
                                   "Hive_DeviceType": "Hub"})
                    sensor.append({'HA_DeviceType': 'Hub_DOG_BARK',
                                   'Hive_NodeID': d["id"],
                                   'Hive_NodeName': d["state"]["name"] +
                                   "Dog Bark Detection",
                                   "Hive_DeviceType": "Hub"})
                    sensor.append({'HA_DeviceType': 'Hub_GLASS_BREAK',
                                   'Hive_NodeID': d["id"],
                                   'Hive_NodeName': d["state"]["name"] +
                                   "Glass Break Detection",
                                   "Hive_DeviceType": "Hub"})
                except KeyError:
                    self.log.log('Hub 360', self.type, "No data found")

        count = sum(1 for i in Data.products
                    if Data.products[i]['type'] in Data.types['Heating'])
        for product in Data.products:
            if Data.products[product]['type'] in Data.types['Heating']:
                p = Data.products[product]
                for device in Data.devices:
                    if Data.devices[device]['type'] in Data.types['Thermo']:
                        d = Data.devices[device]
                        if p["parent"] == d["props"]["zone"]:
                            try:
                                node_name = p["state"]["name"]
                                Data.NAME.update({p["id"]: node_name})
                                Data.MODE.append(p["id"])
                                climate.append({'HA_DeviceType': 'Heating',
                                                'Hive_NodeID': p["id"],
                                                'Hive_NodeName': node_name,
                                                'Hive_DeviceType': "Heating",
                                                'Thermostat_NodeID': d["id"]})
                                sensor.append({'HA_DeviceType':
                                               'Heating_CurrentTemperature',
                                               'Hive_NodeID': p["id"],
                                               'Hive_NodeName': node_name,
                                               "Hive_DeviceType": "Heating"})
                                sensor.append({'HA_DeviceType':
                                               'Heating_TargetTemperature',
                                               'Hive_NodeID': p["id"],
                                               'Hive_NodeName': node_name,
                                               "Hive_DeviceType": "Heating"})
                                sensor.append({'HA_DeviceType':
                                               'Heating_State',
                                               'Hive_NodeID': p["id"],
                                               'Hive_NodeName': node_name,
                                               "Hive_DeviceType": "Heating"})
                                sensor.append({'HA_DeviceType': 'Heating_Mode',
                                               'Hive_NodeID': p["id"],
                                               'Hive_NodeName': node_name,
                                               "Hive_DeviceType": "Heating"})
                                sensor.append({'HA_DeviceType':
                                               'Heating_Boost',
                                               'Hive_NodeID': p["id"],
                                               'Hive_NodeName': node_name,
                                               "Hive_DeviceType": "Heating"})
                            except KeyError:
                                self.log.log('Hot', self.type, "No data found")

        count = sum(1 for i in Data.products
                    if Data.products[i]['type'] in Data.types['Hotwater'])
        for product in Data.products:
            if Data.products[product]['type'] in Data.types['Hotwater']:
                p = Data.products[product]
                try:
                    node_name = p["state"]["name"]
                    Data.NAME.update({p["id"]: node_name})
                    if count == 1:
                        node_name = None
                    climate.append({'HA_DeviceType': 'HotWater',
                                    'Hive_NodeID': p["id"],
                                    'Hive_NodeName': node_name,
                                    "Hive_DeviceType": "HotWater"})
                    sensor.append({'HA_DeviceType': 'HotWater_State',
                                   'Hive_NodeID': p["id"],
                                   'Hive_NodeName': node_name,
                                   "Hive_DeviceType": "HotWater"})
                    sensor.append({'HA_DeviceType': 'HotWater_Mode',
                                   'Hive_NodeID': p["id"],
                                   'Hive_NodeName': node_name,
                                   "Hive_DeviceType": "HotWater"})
                    sensor.append({'HA_DeviceType': 'HotWater_Boost',
                                   'Hive_NodeID': p["id"],
                                   'Hive_NodeName': node_name,
                                   "Hive_DeviceType": "HotWater"})
                except KeyError:
                    self.log.log('Hotwater', self.type, "No data found.")

        count = sum(1 for i in Data.devices
                    if Data.devices[i]['type'] in Data.types['Thermo'])
        for a_device in Data.devices:
            if Data.devices[a_device]['type'] in Data.types['Thermo'] or \
                    Data.devices[a_device]['type'] in Data.types['Sensor']:
                d = Data.devices[a_device]
                try:
                    node_name = d["state"]["name"]
                    Data.NAME.update({d["id"]: node_name})
                    Data.BATTERY.append(d["id"])
                    if count == 1:
                        node_name = None
                    sensor.append({'HA_DeviceType': 'Hive_Device_BatteryLevel',
                                   'Hive_NodeID': d["id"],
                                   'Hive_NodeName': node_name,
                                   "Hive_DeviceType": d["type"]})
                    sensor.append({'HA_DeviceType': 'Hive_Device_Availability',
                                   'Hive_NodeID': d["id"],
                                   'Hive_NodeName': node_name,
                                   "Hive_DeviceType": d["type"]})
                except KeyError:
                    self.log.log('Thermostat', self.type, "No data found")

        for product in Data.products:
            if Data.products[product]['type'] in Data.types['Light']:
                p = Data.products[product]
                Data.MODE.append(p["id"])
                try:
                    Data.NAME.update({p["id"]: p["state"]["name"]})
                    light.append({'HA_DeviceType': 'Hive_Device_Light',
                                  'Hive_Light_DeviceType': p["type"],
                                  'Hive_NodeID': p["id"],
                                  'Hive_NodeName': p["state"]["name"],
                                  "Hive_DeviceType": "Light"})
                    sensor.append({'HA_DeviceType': 'Hive_Device_Light_Mode',
                                   'Hive_NodeID': p["id"],
                                   'Hive_NodeName': p["state"]["name"],
                                   "Hive_DeviceType": p["type"]})
                    sensor.append({'HA_DeviceType':
                                   'Hive_Device_Light_Availability',
                                   'Hive_NodeID': p["id"],
                                   'Hive_NodeName': p["state"]["name"],
                                   "Hive_DeviceType": p["type"]})
                except KeyError:
                    self.log.log('Light', self.type, "No data found")

        for product in Data.products:
            if Data.products[product]['type'] in Data.types['Plug']:
                p = Data.products[product]
                Data.MODE.append(p["id"])
                try:
                    Data.NAME.update({p["id"]: p["state"]["name"]})
                    switch.append({'HA_DeviceType': 'Hive_Device_Plug',
                                   'Hive_Switch_DeviceType': p["type"],
                                   'Hive_NodeID': p["id"],
                                   'Hive_NodeName': p["state"]["name"],
                                   "Hive_DeviceType": "Switch"})
                    sensor.append({'HA_DeviceType': 'Hive_Device_Plug_Mode',
                                   'Hive_NodeID': p["id"],
                                   'Hive_NodeName': p["state"]["name"],
                                   "Hive_DeviceType": p["type"]})
                    sensor.append({'HA_DeviceType':
                                   'Hive_Device_Plug_Availability',
                                   'Hive_NodeID': p["id"],
                                   'Hive_NodeName': p["state"]["name"],
                                   "Hive_DeviceType": p["type"]})
                except KeyError:
                    self.log.log('Plug', self.type, "No data found")

        for action in Data.actions:
            a = Data.actions[action]
            try:
                Data.NAME.update({a["id"]: a["name"]})
                switch.append({'HA_DeviceType': 'Hive_Action',
                               'Hive_Switch_DeviceType': "Action",
                               'Hive_NodeID': a["id"],
                               'Hive_NodeName': a["name"],
                               "Hive_DeviceType": "Action"})
            except KeyError:
                self.log.log('Actions', self.type, "No data found")

        for product in Data.products:
            if Data.products[product]['type'] in Data.types['Sensor']:
                p = Data.products[product]
                try:
                    Data.NAME.update({p["id"]: p["state"]["name"]})
                    binary_sensor.append({'HA_DeviceType':
                                          'Hive_Device_Binary_Sensor',
                                          'Hive_NodeID': p["id"],
                                          'Hive_NodeName': p["state"]["name"],
                                          "Hive_DeviceType": p["type"]})
                except KeyError:
                    self.log.log('Sensor', self.type, "No data found")

        if Data.w_nodeid == "HiveWeather":
            sensor.append({'HA_DeviceType': 'Hive_OutsideTemperature',
                           'Hive_NodeID': Data.w_nodeid,
                           'Hive_NodeName': "Hive Weather",
                           "Hive_DeviceType": "Weather"})

        device_all['device_list_sensor'] = sensor
        device_all['device_list_binary_sensor'] = binary_sensor
        device_all['device_list_climate'] = climate
        device_all['device_list_light'] = light
        device_all['device_list_plug'] = switch

        self.log.log('Session', self.type, "Hive component has initialised")

        return device_all

    @staticmethod
    def epochtime(date_time, pattern, action):
        """ date/time conversion to epoch"""
        if action == 'to_epoch':
            pattern = '%d.%m.%Y %H:%M:%S'
            epochtime = int(time.mktime(
                time.strptime(str(date_time), pattern)))
            return epochtime
        elif action == 'from_epoch':
            date = datetime.fromtimestamp(int(date_time)).strftime(pattern)
            return date

    @staticmethod
    def device_type(n_id, n_type):
        """Decide which sensor to call."""
        if n_type == 'Hub_OnlineStatus':
            return Attributes.online_offline(Attributes(), n_id)
        elif n_type == 'Hive_OutsideTemperature':
            return Weather.temperature(Weather())
        elif n_type == 'Hub_SMOKE_CO':
            return Hub.hub_smoke(Hub(), n_id)
        elif n_type == 'Hub_DOG_BARK':
            return Hub.hub_dog_bark(Hub(), n_id)
        elif n_type == 'Hub_GLASS_BREAK':
            return Hub.hub_glass(Hub(), n_id)
