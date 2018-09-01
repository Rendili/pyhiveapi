""" Pyhiveapi."""
from .api import Hive
from .attributes import Attributes
from .data import Data as Dt
from .heating import Heating
from .hotwater import Hotwater
from .light import Light
from .logging import Logger
from .sensor import Sensor
from .switch import Switch
from .weather import Weather
from datetime import datetime
from datetime import timedelta
import threading
import operator
import time

MINUTES_BETWEEN_LOGONS = 15


class Pyhiveapi:
    """api Class"""

    def __init__(self):
        """Initialise the base variable values."""
        self.lock = threading.Lock()
        self.api = Hive()
        self.attibutes = Attributes()
        self.heating = Heating()
        self.hotwater = Hotwater()
        self.light = Light()
        self.sensor = Sensor()
        self.switch = Switch()
        self.weather = Weather()
        self.log = Logger()

    def hive_api_logon(self):
        """Log in to the Hive API and get the Session IDt."""
        self.log.log('core', "hive_api_logon")

        login_details_found = True
        try_finished = False

        try:
            resp_p = self.api.login(Dt.s_username, Dt.s_password)[
                'parsed']

            if ('token' in resp_p and 'user' in resp_p and
                    'platform' in resp_p):
                Dt.s_session_id = resp_p['token']
                Dt.s_logon_datetime = datetime.now()

                if 'endpoint' in resp_p['platform']:
                    self.api.urls.update({'base': resp_p['platform'][
                        'endpoint']})
                else:
                    login_details_found = False

                if 'name' in resp_p['platform']:
                    Dt.s_platform_name = resp_p['platform']['name']
                else:
                    login_details_found = False

                if 'locale' in resp_p['user']:
                    Dt.s_locale = resp_p['user']['locale']
                else:
                    login_details_found = False

                if 'countryCode' in resp_p['user']:
                    Dt.s_countrycode = resp_p['user']['countryCode']
                else:
                    login_details_found = False

                if 'timezone' in resp_p['user']:
                    Dt.s_timezone = resp_p['user']['timezone']
                else:
                    login_details_found = False

                if 'postcode' in resp_p['user']:
                    Dt.s_postcode = resp_p['user']['postcode']
                else:
                    login_details_found = False

                if 'temperatureUnit' in resp_p['user']:
                    Dt.s_temperature_unit = resp_p['user'][
                        'temperatureUnit']
                else:
                    login_details_found = False
            else:
                login_details_found = False

            try_finished = True

        except (IOError, RuntimeError, ZeroDivisionError):
            try_finished = False
        finally:
            if not try_finished:
                login_details_found = False

        if not login_details_found:
            Dt.s_session_id = ""

    def check_hive_api_logon(self):
        """Check if currently logged in with a valid Session IDt."""
        self.log.log('core', "check_hive_api_logon")

        if Dt.s_file is False:
            c_time = datetime.now()
            l_logon_secs = (c_time - Dt.s_logon_datetime).total_seconds()
            l_logon_mins = int(round(l_logon_secs / 60))

            if l_logon_mins >= MINUTES_BETWEEN_LOGONS or \
                    Dt.s_session_id is None:
                self.hive_api_logon()

    def update_data(self, node_id):
        """Get latest data for Hive nodes - rate limiting."""
        self.lock.acquire()
        self.log.check_logging(False)
        try:
            updated = False
            ct = datetime.now()
            last_update_secs = (ct - Dt.s_last_update).total_seconds()
            if last_update_secs >= Dt.s_interval_seconds:
                updated = self.hive_api_get_nodes(node_id, None)

            w_last_update_secs = (ct - Dt.w_last_update).total_seconds()
            if w_last_update_secs >= Dt.w_interval_seconds:
                updated = self.hive_api_get_weather()
        finally:
            self.lock.release()

        return updated

    def hive_api_get_nodes_nl(self, file):
        """Get latest data for Hive nodes - not rate limiting."""
        if file:
            Dt.s_file = True

        self.log.log('core', "hive_api_get_nodes_nl")
        self.hive_api_get_nodes("NoID", file)

    def hive_api_get_nodes(self, node_id, file):
        """Get latest data for Hive nodes."""
        get_nodes_successful = False
        api_resp_d = None
        self.log.log('core', "hive_api_get_nodes : NodeID = " + node_id)

        self.check_hive_api_logon()
        try:
            if Dt.s_file:
                api_resp_d = file['devices']
            elif Dt.s_session_id is not None:
                Dt.devices = {}
                Dt.products = {}
                api_resp_d = self.api.get_devices(Dt.s_session_id)

                api_resp = str(api_resp_d['original'])
                if api_resp == "<Response [200]>":
                    self.log.log('core_http', "Devices API call "
                                 + "successful: " + api_resp)
                else:
                    self.log.log('core_http', "Devices API call "
                                 + "failed : " + api_resp)

            api_resp_p = api_resp_d['parsed']

            for a_device in api_resp_p:
                if 'id' in a_device:
                    Dt.devices.update({a_device['id']: a_device})
            try_finished_devices = True
        except (IOError, RuntimeError, ZeroDivisionError):
            self.log.log('core_http', "Api didnt receive any data")
            try_finished_devices = False

        try:
            if Dt.s_file:
                resp = file['devices']
            elif Dt.s_session_id is not None:
                resp = self.api.get_products(Dt.s_session_id)
                if resp['original'] == "<Response [200]>":
                    self.log.log('core_http', "Products API "
                                 + "successful: " + resp['original'])
                else:
                    self.log.log('core_http', "Products API "
                                 + "failed : " + resp['original'])

            for a_product in resp['parsed']:
                if 'id' in a_product:
                    Dt.products.update({a_product['id']: a_product})
            try_finished_products = True
        except (IOError, RuntimeError, ZeroDivisionError):
            try_finished_products = False

        if try_finished_devices and try_finished_products:
            get_nodes_successful = True

        if get_nodes_successful:
            Dt.s_last_update = datetime.now()
            now = datetime.now()

            start_date = str(now.day) + '.' + str(now.month) + '.' \
                         + str(now.year) + ' 00:00:00'
            fromepoch = self.epochtime(start_date) * 1000
            end_date = str(now.day) + '.' + str(now.month) + '.' \
                       + str(now.year) + ' 23:59:59'
            toepoch = self.epochtime(end_date) * 1000
            for sensor in Dt.products:
                if Dt.products[sensor]["type"] == "motionsensor":
                    p = Dt.products[sensor]
                    resp = self.api.motion_sensor(Dt.s_session_id, p,
                                                  fromepoch, toepoch)

                    if str(resp['original']) == "<Response [200]>":
                        if len(resp['parsed']) > 0 and 'inMotion' \
                                in resp['parsed'][0]:
                            p["props"]["motion"]["status"] = resp['parsed'][0][
                                'inMotion']

                        self.log.log('core_http',
                                     "Sensor " + p["state"]["name"]
                                     + " - " + "HTTP call successful : "
                                     + resp['original'])
                    else:
                        self.log.log('core_http', "Sensor "
                                     + p["state"]["name"] + " - "
                                     + "HTTP call failed : "
                                     + resp['original'])
        return get_nodes_successful

    def hive_api_get_weather(self):
        """Get latest weather data from Hive."""
        self.log.log('core', "hive_api_get_weather")

        get_weather_successful = True
        current_time = datetime.now()
        self.check_hive_api_logon()

        try:
            if Dt.s_session_id is not None:
                weather_url = "?postcode=" + Dt.s_postcode \
                              + "&country=" + Dt.s_countrycode

                resp = self.api.get_weather(weather_url, Dt.s_session_id)
                if "weather" in resp['parsed']:
                    if "icon" in resp['parsed']["weather"]:
                        Dt.w_icon = resp['parsed']["weather"]["icon"]
                    if "description" in resp['parsed']["weather"]:
                        Dt.w_description = resp['parsed']["weather"]["icon"]
                    if "temperature" in resp['parsed']["weather"]:
                        if "unit" in resp['parsed']["weather"]["temperature"]:
                            Dt.t_unit = resp['parsed']["weather"][
                                "temperature"]["unit"]
                        if "unit" in resp['parsed']["weather"]["temperature"]:
                            Dt.t_value = resp['parsed']["weather"][
                                "temperature"]["value"]
                    Dt.w_nodeid = "HiveWeather"
                else:
                    get_weather_successful = False

            Dt.w_last_update = current_time
        except (IOError, RuntimeError, ZeroDivisionError):
            get_weather_successful = False

        return get_weather_successful

    @staticmethod
    def p_minutes_to_time(self, minutes_to_convert):
        """Convert minutes string to datetime."""
        hours_converted, minutes_converted = divmod(minutes_to_convert, 60)
        converted_time = datetime.strptime(str(hours_converted)
                                           + ":"
                                           + str(minutes_converted),
                                           "%H:%M")
        converted_time_string = converted_time.strftime("%H:%M")
        return converted_time_string

    @staticmethod
    def p_get_schedule_now_next_later(self, hive_api_schedule):
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
                slot_time_date_s = (slot_date.strftime("%d-%m-%Y")
                                    + " " + slot_time)
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

        schedule_now['Start_DateTime'] = (schedule_now['Start_DateTime']
                                          - timedelta(days=7))

        schedule_now['End_DateTime'] = schedule_next['Start_DateTime']
        schedule_next['End_DateTime'] = schedule_later['Start_DateTime']
        schedule_later['End_DateTime'] = fsl_sorted[2]['Start_DateTime']

        schedule_now_and_next['now'] = schedule_now
        schedule_now_and_next['next'] = schedule_next
        schedule_now_and_next['later'] = schedule_later

        return schedule_now_and_next

    def initialise_api(self, username, password, sbu, file, session):
        """Setup the Hive platform."""
        self.log.check_logging(session)
        Dt.s_username = username
        Dt.s_password = password
        self.log.log('core', "api initialising")

        if sbu <= 0:
            sbu = 2

        hive_update_interval = sbu

        if file is not None:
            self.hive_api_get_nodes_nl(file)
        elif Dt.s_username is None or Dt.s_password is None:
            return None
        else:
            self.hive_api_logon()
            if Dt.s_session_id is not None:
                Dt.s_interval_seconds = hive_update_interval
                self.hive_api_get_nodes_nl(file)
                self.hive_api_get_weather()

        if Dt.devices is None or Dt.products is None:
            self.log.log('core', "Failed to get devicies and products")

        device_all = {}
        sensor = []
        binary_sensor = []
        climate = []
        light = []
        plug = []

        for a_device in Dt.devices:
            if Dt.devices[a_device]["type"] in Dt.types['hub']:
                d = Dt.devices[a_device]
                try:
                    Dt.NAME.update({d["id"]: d["state"]["name"]})
                    sensor.append({'HA_DeviceType': 'Hub_OnlineStatus',
                                   'Hive_NodeID': d["id"],
                                   'Hive_NodeName': d["state"]["name"],
                                   "Hive_DeviceType": "Hub"})
                except KeyError:
                    self.log.log('core', "Failed to get hive hubs")

        count = sum(1 for i in Dt.products
                    if Dt.products[i]['type'] == 'heating')
        for product in Dt.products:
            if Dt.products[product]['type'] in Dt.types['heating']:
                p = Dt.products[product]
                for device in Dt.devices:
                    if Dt.devices[device]['type'] in Dt.types['thermostat']:
                        d = Dt.devices[device]
                        if p["parent"] == d["props"]["zone"]:
                            try:
                                node_name = p["state"]["name"]
                                Dt.NAME.update({p["id"]: node_name})
                                if count == 1:
                                    node_name = None
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
                                self.log.log('core', "Failed to get hive "
                                             + "heating")

        count = sum(1 for i in Dt.products
                    if Dt.products[i]['type'] == 'hotwater')
        for product in Dt.products:
            if Dt.products[product]['type'] in Dt.types['hotwater']:
                p = Dt.products[product]['type']
                try:
                    node_name = p["state"]["name"]
                    Dt.NAME.update({p["id"]: node_name})
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
                    self.log.log('core', "Failed to get hive hotwater")

        count = sum(1 for i in Dt.devices
                    if Dt.devices[i]['type'] == 'thermostatui')
        for a_device in Dt.devices:
            if Dt.devices[a_device]['type'] in Dt.types['thermostat'] or \
                    Dt.devices[a_device]['type'] in Dt.types['sensor']:
                d = Dt.devices[a_device]
                try:
                    node_name = d["state"]["name"]
                    Dt.NAME.update({d["id"]: node_name})
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
                    self.log.log('core', "Failed to get hive sensors")

        for product in Dt.products:
            if Dt.products[product]['type'] in Dt.types['light']:
                p = Dt.products[product]
                try:
                    Dt.NAME.update({p["id"]: p["state"]["name"]})
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
                    self.log.log('core', "Failed to get hive lights")

        for product in Dt.products:
            if Dt.products[product]['type'] in Dt.types['plug']:
                p = Dt.products[product]
                try:
                    Dt.NAME.update({p["id"]: p["state"]["name"]})
                    plug.append({'HA_DeviceType': 'Hive_Device_Plug',
                                 'Hive_Plug_DeviceType': p["type"],
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
                    self.log.log('core', "Failed to get hive plugs")

        for product in Dt.products:
            if Dt.products[product]['type'] in Dt.types['sensor']:
                p = Dt.products[product]
                try:
                    Dt.NAME.update({p["id"]: p["state"]["name"]})
                    binary_sensor.append({'HA_DeviceType':
                                              'Hive_Device_Binary_Sensor',
                                          'Hive_NodeID': p["id"],
                                          'Hive_NodeName': p["state"]["name"],
                                          "Hive_DeviceType": p["type"]})
                except KeyError:
                    self.log.log('core', "Failed to get hive sensors")

        if Dt.w_nodeid == "HiveWeather":
            sensor.append({'HA_DeviceType': 'Hive_OutsideTemperature',
                           'Hive_NodeID': Dt.w_nodeid,
                           'Hive_NodeName': "Hive Weather",
                           "Hive_DeviceType": "Weather"})

        device_all['device_list_sensor'] = sensor
        device_all['device_list_binary_sensor'] = binary_sensor
        device_all['device_list_climate'] = climate
        device_all['device_list_light'] = light
        device_all['device_list_plug'] = plug

        self.log.log('core', "api initialised")

        return device_all

    @staticmethod
    def epochtime(date_time):
        """ date/time conversion to epoch"""
        pattern = '%d.%m.%Y %H:%M:%S'
        epochtime = int(time.mktime(time.strptime(date_time, pattern)))
        return epochtime

    def online_offline(self, node):
        """Check if device is online"""
        data = None
        current_node_attribute = "Device_Availability_" + node
        hive_tmp = None
        hive_return = "UNKNOWN"

        self.log.log('attribute', "Checking device availabilit for : " + node)

        try:
            data = Dt.devices[node]
            hive_tmp = (data["props"]["online"])
            hive_found = True
        except KeyError:
            hive_found = False

        if hive_found:
            if hive_tmp:
                hive_return = 'online'
            elif not hive_tmp:
                hive_return = 'offline'
            Dt.NODES[current_node_attribute] = hive_return
        else:
            if current_node_attribute in Dt.NODES:
                hive_return = Dt.NODES.get(current_node_attribute)
            else:
                hive_return = "UNKNOWN"

        if hive_return != "UNKNOWN":
            self.log.log('attribute', "Availability of device "
                         + data["state"]["name"] + " is : " + hive_return)
        else:
            self.log.log('attirbute',
                         "Device does not have availability info: " + node)

        return hive_return
