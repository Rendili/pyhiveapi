""" Pyhiveapi"""
import operator
from datetime import datetime
from datetime import timedelta
import threading
import time
import requests
import colorsys
import os

HIVE_NODE_UPDATE_INTERVAL_DEFAULT = 120
HIVE_WEATHER_UPDATE_INTERVAL_DEFAULT = 600
MINUTES_BETWEEN_LOGONS = 15

NODE_ATTRIBS = {"Header": "HeaderText"}


class HiveDevices:
    """Initiate Hive Devices Class."""

    hub = []
    thermostat = []
    boiler_module = []
    plug = []
    light = []
    sensors = []
    id_list = {}


class HiveProducts:
    """Initiate Hive Products Class."""

    heating = []
    hotwater = []
    light = []
    plug = []
    sensors = []
    id_list = {}


class HivePlatformData:
    """Initiate Hive PlatformData Class."""

    minmax = {}


class HiveTemperature:
    """Initiate Hive Temperature Class."""

    unit = ""
    value = 0.00


class HiveWeather:
    """Initiate Hive Weather Class."""

    last_update = datetime(2017, 1, 1, 12, 0, 0)
    nodeid = ""
    icon = ""
    description = ""
    temperature = HiveTemperature()


class Logging:
    """Initiate Logging Class."""

    output_folder = ""
    output_file = ""
    file_all = ""
    file_core = ""
    file_http = ""
    file_heating = ""
    file_hotwater = ""
    file_light = ""
    file_switch = ""
    file_sensor = ""
    file_attribute = ""
    enabled = False
    all = False
    core = False
    http = False
    heating = False
    hotwater = False
    light = False
    switch = False
    sensor = False
    attribute = False


class HiveSession:
    """Initiate Hive Session Class."""

    session_id = ""
    session_logon_datetime = datetime(2017, 1, 1, 12, 0, 0)
    username = ""
    password = ""
    postcode = ""
    timezone = ""
    countrycode = ""
    locale = ""
    temperature_unit = ""
    devices = HiveDevices()
    products = HiveProducts()
    weather = HiveWeather()
    data = HivePlatformData()
    logging = Logging()
#    holiday_mode = Hive_HolidayMode()
    update_node_interval_seconds = HIVE_NODE_UPDATE_INTERVAL_DEFAULT
    update_weather_interval_seconds = HIVE_WEATHER_UPDATE_INTERVAL_DEFAULT
    last_update = datetime(2017, 1, 1, 12, 0, 0)
    file = False


class HiveAPIURLS:
    """Initiate Hive API URLS Class."""

    global_login = ""
    base = ""
    weather = ""
    holiday_mode = ""
    devices = ""
    products = ""
    nodes = ""


class HiveAPIHeaders:
    """Initiate Hive API Headers Class."""

    accept_key = ""
    accept_value = ""
    content_type_key = ""
    content_type_value = ""
    session_id_key = ""
    session_id_value = ""


class HiveAPIDetails:
    """Initiate Hive API Details Class."""

    urls = HiveAPIURLS()
    headers = HiveAPIHeaders()
    platform_name = ""


HIVE_API = HiveAPIDetails()
HSC = HiveSession()


class Pyhiveapi:
    """Pyhiveapi Class"""

    def __init__(self):
        """Initialise the base variable values."""
        self.lock = threading.Lock()

        HIVE_API.platform_name = ""

        HIVE_API.urls.global_login = "https://beekeeper.hivehome.com/1.0/global/login"
        HIVE_API.urls.base = ""
        HIVE_API.urls.weather = "https://weather.prod.bgchprod.info/weather"
        HIVE_API.urls.holiday_mode = "/holiday-mode"
        HIVE_API.urls.devices = "/devices"
        HIVE_API.urls.products = "/products"
        HIVE_API.urls.nodes = "/nodes"

        HIVE_API.headers.accept_key = "Accept"
        HIVE_API.headers.accept_value = "*/*"
        HIVE_API.headers.content_type_key = "content-type"
        HIVE_API.headers.content_type_value = "application/json"
        HIVE_API.headers.session_id_key = "authorization"
        HIVE_API.headers.session_id_value = None

        HSC.logging.file_all = "pyhiveapi.logging.all"
        HSC.logging.file_core = "pyhiveapi.logging.core"
        HSC.logging.file_http = "pyhiveapi.logging.http"
        HSC.logging.file_heating = "pyhiveapi.logging.heating"
        HSC.logging.file_hotwater = "pyhiveapi.logging.hotwater"
        HSC.logging.file_light = "pyhiveapi.logging.light"
        HSC.logging.file_switch = "pyhiveapi.logging.switch"
        HSC.logging.file_sensor = "pyhiveapi.logging.sensor"
        HSC.logging.file_attribute = "pyhiveapi.logging.attribute"

    def hive_api_json_call(self, request_type, request_url, json_string_content, absolute_request_url):
        """Call the JSON Hive API and return any returned data."""
        api_headers = {HIVE_API.headers.content_type_key:
                       HIVE_API.headers.content_type_value,
                       HIVE_API.headers.accept_key:
                       HIVE_API.headers.accept_value,
                       HIVE_API.headers.session_id_key:
                       HIVE_API.headers.session_id_value}

        requests_timeout = 10
        json_return = {}
        full_request_url = ""

        if absolute_request_url:
            full_request_url = request_url
        else:
            full_request_url = HIVE_API.urls.base + request_url

        json_call_try_finished = False
        try:
            if request_type == "POST":
                json_response = requests.post(full_request_url,
                                              data=json_string_content,
                                              headers=api_headers,
                                              timeout=requests_timeout)
            elif request_type == "GET":
                json_response = requests.get(full_request_url,
                                             data=json_string_content,
                                             headers=api_headers,
                                             timeout=requests_timeout)
            elif request_type == "PUT":
                json_response = requests.put(full_request_url,
                                             data=json_string_content,
                                             headers=api_headers,
                                             timeout=requests_timeout)
            else:
                json_response = ""

            json_call_try_finished = True
        except (IOError, RuntimeError, ZeroDivisionError):
            json_call_try_finished = False
        finally:
            if not json_call_try_finished:
                json_return['original'] = "No response to JSON Hive API request"
                json_return['parsed'] = "No response to JSON Hive API request"

        if json_call_try_finished:
            parse_json_try_finished = False
            try:
                json_return['original'] = json_response
                json_return['parsed'] = json_response.json()

                parse_json_try_finished = True
            except (IOError, RuntimeError, ZeroDivisionError):
                parse_json_try_finished = False
            finally:
                if not parse_json_try_finished:
                    json_return['original'] = "Error parsing JSON data"
                    json_return['parsed'] = "Error parsing JSON data"

        return json_return

    def hive_api_logon(self):
        """Log in to the Hive API and get the Session ID."""
        if HSC.logging.all or HSC.logging.core:
            Pyhiveapi.logger("hive_api_logon")

        login_details_found = True
        HSC.session_id = None

        try_finished = False
        try:
            api_resp_d = {}
            api_resp_p = None

            json_string_content = '{"username": "' + HSC.username + '","password": "' + HSC.password + '"}'

            api_resp_d = Pyhiveapi.hive_api_json_call(self, "POST", HIVE_API.urls.global_login, json_string_content, True)
            api_resp_p = api_resp_d['parsed']

            if ('token' in api_resp_p and
                    'user' in api_resp_p and
                    'platform' in api_resp_p):
                HIVE_API.headers.session_id_value = api_resp_p["token"]
                HSC.session_id = HIVE_API.headers.session_id_value
                HSC.session_logon_datetime = datetime.now()

                if 'endpoint' in api_resp_p['platform']:
                    HIVE_API.urls.base = api_resp_p['platform']['endpoint']
                else:
                    login_details_found = False

                if 'name' in api_resp_p['platform']:
                    HIVE_API.platform_name = api_resp_p['platform']['name']
                else:
                    login_details_found = False

                if 'locale' in api_resp_p['user']:
                    HSC.locale = api_resp_p['user']['locale']
                else:
                    login_details_found = False

                if 'countryCode' in api_resp_p['user']:
                    HSC.countrycode = api_resp_p['user']['countryCode']
                else:
                    login_details_found = False

                if 'timezone' in api_resp_p['user']:
                    HSC.timezone = api_resp_p['user']['timezone']
                else:
                    login_details_found = False

                if 'postcode' in api_resp_p['user']:
                    HSC.postcode = api_resp_p['user']['postcode']
                else:
                    login_details_found = False

                if 'temperatureUnit' in api_resp_p['user']:
                    HSC.temperature_unit = api_resp_p['user']['temperatureUnit']
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
            HSC.session_id = None

    def check_hive_api_logon(self):
        """Check if currently logged in with a valid Session ID."""
        if HSC.logging.all or HSC.logging.core:
            Pyhiveapi.logger("check_hive_api_logon")

        current_time = datetime.now()
        l_logon_secs = (current_time - HSC.session_logon_datetime).total_seconds()
        l_logon_mins = int(round(l_logon_secs / 60))

        if l_logon_mins >= MINUTES_BETWEEN_LOGONS or HSC.session_id is None:
            Pyhiveapi.hive_api_logon(self)

        if HSC.file == True:
            HSC.session_id = "Test"

    def update_data(self, node_id):
        """Get latest data for Hive nodes - rate limiting."""
        self.lock.acquire()
        try:
            nodes_updated = False
            current_time = datetime.now()
            nodes_last_update_secs = (current_time - HSC.last_update).total_seconds()
            if nodes_last_update_secs >= HSC.update_node_interval_seconds:
                nodes_updated = Pyhiveapi.hive_api_get_nodes(self, node_id)

            weather_last_update_secs = (current_time - HSC.weather.last_update).total_seconds()
            if weather_last_update_secs >= HSC.update_weather_interval_seconds:
                nodes_updated = Pyhiveapi.hive_api_get_weather(self)
        finally:
            self.lock.release()

        return nodes_updated

    def hive_api_get_nodes_nl(self):
        """Get latest data for Hive nodes - not rate limiting."""
        if HSC.logging.all or HSC.logging.core:
            Pyhiveapi.logger("hive_api_get_nodes_nl")
        Pyhiveapi.hive_api_get_nodes(self, "NoID")

    def hive_api_get_nodes(self, node_id):
        """Get latest data for Hive nodes."""
        get_nodes_successful = True

        if HSC.logging.all or HSC.logging.core:
            Pyhiveapi.logger("hive_api_get_nodes : NodeID = " + node_id)

        Pyhiveapi.check_hive_api_logon(self)

        if HSC.session_id is not None:
            tmp_devices_hub = []
            tmp_devices_thermostat = []
            tmp_devices_boiler_module = []
            tmp_devices_plug = []
            tmp_devices_light = []
            tmp_devices_sensors = []
            HSC.devices.id_list = {}

            tmp_products_heating = []
            tmp_products_hotwater = []
            tmp_products_light = []
            tmp_products_plug = []
            tmp_products_sensors = []
            HSC.products.id_list = {}

            try_finished = False
            try:
                api_resp_d = {}
                api_resp_p = None
                api_resp_d = Pyhiveapi.hive_api_json_call(self, "GET", HIVE_API.urls.devices, "", False)

                if HSC.logging.all or HSC.logging.core or HSC.logging.http:
                    api_resp = str(api_resp_d['original'])
                    if api_resp == "<Response [200]>":
                        Pyhiveapi.logger("Devices API call successful : " + api_resp)
                    else:
                        Pyhiveapi.logger("Devices API call failed : " + api_resp)

                api_resp_p = api_resp_d['parsed']

                for a_device in api_resp_p:
                    if "type" in a_device:
                        if a_device["type"] == "hub":
                            tmp_devices_hub.append(a_device)
                        if a_device["type"] == "thermostatui":
                            tmp_devices_thermostat.append(a_device)
                        if a_device["type"] == "boilermodule":
                            tmp_devices_boiler_module.append(a_device)
                        if a_device["type"] == "activeplug":
                            tmp_devices_plug.append(a_device)
                        if (a_device["type"] == "warmwhitelight" or
                                a_device["type"] == "tuneablelight" or
                                a_device["type"] == "colourtuneablelight"):
                            tmp_devices_light.append(a_device)
                        if (a_device["type"] == "motionsensor" or
                                a_device["type"] == "contactsensor"):
                            tmp_devices_sensors.append(a_device)

                try_finished = True
            except (IOError, RuntimeError, ZeroDivisionError):
                try_finished = False
            finally:
                if not try_finished:
                    try_finished = False

            try_finished = False
            try:
                api_resp_d = {}
                api_resp_p = None
                api_resp_d = Pyhiveapi.hive_api_json_call(self, "GET", HIVE_API.urls.products, "", False)

                if HSC.logging.all or HSC.logging.core or HSC.logging.http:
                    api_resp = str(api_resp_d['original'])
                    if api_resp == "<Response [200]>":
                        Pyhiveapi.logger("Products API call successful : " + api_resp)
                    else:
                        Pyhiveapi.logger("Products API call failed : " + api_resp)

                api_resp_p = api_resp_d['parsed']

                for a_product in api_resp_p:
                    if "type" in a_product:
                        if a_product["type"] == "heating":
                            tmp_products_heating.append(a_product)
                        if a_product["type"] == "hotwater":
                            tmp_products_hotwater.append(a_product)
                        if a_product["type"] == "activeplug":
                            tmp_products_plug.append(a_product)
                        if (a_product["type"] == "warmwhitelight" or
                                a_product["type"] == "tuneablelight" or
                                a_product["type"] == "colourtuneablelight"):
                            tmp_products_light.append(a_product)
                        if (a_product["type"] == "motionsensor" or
                                a_product["type"] == "contactsensor"):
                            tmp_products_sensors.append(a_product)
                try_finished = True
            except (IOError, RuntimeError, ZeroDivisionError):
                try_finished = False
            finally:
                if not try_finished:
                    try_finished = False

            try_finished = False
            try:
                if len(tmp_devices_hub) > 0:
                    HSC.devices.hub = tmp_devices_hub
                    for node in HSC.devices.hub:
                        HSC.devices.id_list.update({node["id"]: HSC.devices.hub})
                if len(tmp_devices_thermostat) > 0:
                    HSC.devices.thermostat = tmp_devices_thermostat
                    for node in HSC.devices.thermostat:
                        HSC.devices.id_list.update({node["id"]: HSC.devices.thermostat})
                if len(tmp_devices_boiler_module) > 0:
                    HSC.devices.boiler_module = tmp_devices_boiler_module
                    for node in HSC.devices.boiler_module:
                        HSC.devices.id_list.update({node["id"]: HSC.devices.boiler_module})
                if len(tmp_devices_plug) > 0:
                    HSC.devices.plug = tmp_devices_plug
                    for node in HSC.devices.plug:
                        HSC.devices.id_list.update({node["id"]: HSC.devices.plug})
                if len(tmp_devices_light) > 0:
                    HSC.devices.light = tmp_devices_light
                    for node in HSC.devices.light:
                        HSC.devices.id_list.update({node["id"]: HSC.devices.light})
                if len(tmp_devices_sensors) > 0:
                    HSC.devices.sensors = tmp_devices_sensors
                    for node in HSC.devices.sensors:
                        HSC.devices.id_list.update({node["id"]: HSC.devices.sensors})

                if len(tmp_products_heating) > 0:
                    HSC.products.heating = tmp_products_heating
                    for node in HSC.products.heating:
                        HSC.products.id_list.update({node["id"]: HSC.products.heating})
                if len(tmp_products_hotwater) > 0:
                    HSC.products.hotwater = tmp_products_hotwater
                    for node in HSC.products.hotwater:
                        HSC.products.id_list.update({node["id"]: HSC.products.hotwater})
                if len(tmp_products_plug) > 0:
                    HSC.products.plug = tmp_products_plug
                    for node in HSC.products.plug:
                        HSC.products.id_list.update({node["id"]: HSC.products.plug})
                if len(tmp_products_light) > 0:
                    HSC.products.light = tmp_products_light
                    for node in HSC.products.light:
                        HSC.products.id_list.update({node["id"]: HSC.products.light})
                if len(tmp_products_sensors) > 0:
                    HSC.products.sensors = tmp_products_sensors
                    for node in HSC.products.sensors:
                        HSC.products.id_list.update({node["id"]: HSC.products.sensors})

                try_finished = True
            except (IOError, RuntimeError, ZeroDivisionError):
                try_finished = False
            finally:
                if not try_finished:
                    get_nodes_successful = False
        else:
            get_nodes_successful = False

        if get_nodes_successful:
            HSC.last_update = datetime.now()
            now = datetime.now()

            start_date = str(now.day) + '.' + str(now.month) + '.' \
                         + str(now.year) + ' 00:00:00'
            fromepoch = Pyhiveapi.epochtime(self, start_date) * 1000
            end_date = str(now.day) + '.' + str(now.month) + '.' \
                       + str(now.year) + ' 23:59:59'
            toepoch = Pyhiveapi.epochtime(self, end_date) * 1000
            allsensors = HSC.products.sensors
            for sensor in allsensors:
                if sensor["type"] == "motionsensor":
                    hive_api_url = (HIVE_API.urls.products + '/' +
                                    sensor["type"] + '/' + sensor["id"]
                                    + '/events?from=' + str(fromepoch) +
                                    '&to=' + str(toepoch))

                    api_resp_d = Pyhiveapi.hive_api_json_call(self, "GET",
                                                              hive_api_url,
                                                              "",
                                                              False)
                    api_resp_o = api_resp_d['original']
                    api_resp_p = api_resp_d['parsed']

                    if str(api_resp_o) == "<Response [200]>":
                        if len(api_resp_p) > 0 and 'inMotion' in api_resp_p[0]:
                            sensor["props"]["motion"]["status"] = api_resp_p[0]['inMotion']
                        if HSC.logging.all or HSC.logging.core or HSC.logging.http:
                            api_resp = str(api_resp_d['original'])
                            if api_resp == "<Response [200]>":
                                Pyhiveapi.logger(
                                    "Sensor " + sensor["state"]["name"] + " - " + "HTTP call successful : " + api_resp)
                            else:
                                Pyhiveapi.logger(
                                    "Sensor " + sensor["state"]["name"] + " - " + "HTTP call failed : " + api_resp)

        return get_nodes_successful

    def hive_api_get_weather(self):
        """Get latest weather data from Hive."""
        if HSC.logging.all or HSC.logging.core:
            Pyhiveapi.logger("hive_api_get_weather")

        get_weather_successful = True

        current_time = datetime.now()

        Pyhiveapi.check_hive_api_logon(self)

        if HSC.session_id is not None:
            try_finished = False
            try:
                api_resp_d = {}
                api_resp_p = None
                weather_url = HIVE_API.urls.weather + "?postcode=" + HSC.postcode + "&country=" + HSC.countrycode
                weather_url = weather_url.replace(" ", "%20")
                api_resp_d = Pyhiveapi.hive_api_json_call(self, "GET", weather_url, "", True)
                api_resp_p = api_resp_d['parsed']
                if "weather" in api_resp_p:
                    if "icon" in api_resp_p["weather"]:
                        HSC.weather.icon = api_resp_p["weather"]["icon"]
                    if "description" in api_resp_p["weather"]:
                        HSC.weather.description = api_resp_p["weather"]["icon"]
                    if "temperature" in api_resp_p["weather"]:
                        if "unit" in api_resp_p["weather"]["temperature"]:
                            HSC.weather.temperature.unit = api_resp_p["weather"]["temperature"]["unit"]
                        if "unit" in api_resp_p["weather"]["temperature"]:
                            HSC.weather.temperature.value = api_resp_p["weather"]["temperature"]["value"]
                    HSC.weather.nodeid = "HiveWeather"
                else:
                    get_weather_successful = False

                HSC.weather.last_update = current_time
                try_finished = True
            except (IOError, RuntimeError, ZeroDivisionError):
                try_finished = False
            finally:
                if not try_finished:
                    try_finished = False
        else:
            get_weather_successful = False

        return get_weather_successful

    def p_minutes_to_time(self, minutes_to_convert):
        """Convert minutes string to datetime."""
        hours_converted, minutes_converted = divmod(minutes_to_convert, 60)
        converted_time = datetime.strptime(str(hours_converted)
                                           + ":"
                                           + str(minutes_converted),
                                           "%H:%M")
        converted_time_string = converted_time.strftime("%H:%M")
        return converted_time_string

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
            current_day_schedule = hive_api_schedule[days_rolling_list[day_index]]
            current_day_schedule_sorted = sorted(current_day_schedule,
                                                 key=operator.itemgetter('start'),
                                                 reverse=False)

            for current_slot in range(0, len(current_day_schedule_sorted)):
                current_slot_custom = current_day_schedule_sorted[current_slot]

                slot_date = datetime.now() + timedelta(days=day_index)
                slot_time = Pyhiveapi.p_minutes_to_time(self, current_slot_custom["start"])
                slot_time_date_s = (slot_date.strftime("%d-%m-%Y")
                                    + " "
                                    + slot_time)
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

    def initialise_api(self, username, password, mins_between_updates):
        """Setup the Hive platform."""
        HSC.username = username
        HSC.password = password

        HSC.logging.output_folder = os.path.expanduser('~') + "/pyhiveapi"
        HSC.logging.output_file = HSC.logging.output_folder + "/pyhiveapi.log"

        try:
            if os.path.isfile(HSC.logging.output_file):
                os.remove(HSC.logging.output_file)

            if os.path.isdir(HSC.logging.output_folder):
                if os.path.isfile(HSC.logging.output_folder + "/" + HSC.logging.file_all):
                    HSC.logging.all = True
                    HSC.logging.enabled = True
                if os.path.isfile(HSC.logging.output_folder + "/" + HSC.logging.file_core):
                    HSC.logging.core = True
                    HSC.logging.enabled = True
                if os.path.isfile(HSC.logging.output_folder + "/" + HSC.logging.file_http):
                    HSC.logging.http = True
                    HSC.logging.enabled = True
                if os.path.isfile(HSC.logging.output_folder + "/" + HSC.logging.file_heating):
                    HSC.logging.heating = True
                    HSC.logging.enabled = True
                if os.path.isfile(HSC.logging.output_folder + "/" + HSC.logging.file_hotwater):
                    HSC.logging.hotwater = True
                    HSC.logging.enabled = True
                if os.path.isfile(HSC.logging.output_folder + "/" + HSC.logging.file_light):
                    HSC.logging.light = True
                    HSC.logging.enabled = True
                if os.path.isfile(HSC.logging.output_folder + "/" + HSC.logging.file_sensor):
                    HSC.logging.sensor = True
                    HSC.logging.enabled = True
                if os.path.isfile(HSC.logging.output_folder + "/" + HSC.logging.file_switch):
                    HSC.logging.switch = True
                    HSC.logging.enabled = True
                if os.path.isfile(HSC.logging.output_folder + "/" + HSC.logging.file_attribute):
                    HSC.logging.attribute = True
                    HSC.logging.enabled = True
        except:
            HSC.logging.all = False
            HSC.logging.enabled = False

        if HSC.logging.all or HSC.logging.core:
            Pyhiveapi.logger("pyhiveapi initialising")

        if mins_between_updates <= 0:
            mins_between_updates = 2

        hive_node_update_interval = mins_between_updates * 60

        if HSC.username is None or HSC.password is None:
            return None
        else:
            Pyhiveapi.hive_api_logon(self)
            if HSC.session_id is not None:
                HSC.update_node_interval_seconds = hive_node_update_interval
                Pyhiveapi.hive_api_get_nodes_nl(self)
                Pyhiveapi.hive_api_get_weather(self)

        device_list_all = {}
        device_list_sensor = []
        device_list_binary_sensor = []
        device_list_climate = []
        device_list_light = []
        device_list_plug = []

        if len(HSC.devices.hub) > 0:
            for a_device in HSC.devices.hub:
                if "id" in a_device and "state" in a_device and "name" in a_device["state"]:
                    device_list_sensor.append({'HA_DeviceType': 'Hub_OnlineStatus', 'Hive_NodeID': a_device["id"], 'Hive_NodeName': a_device["state"]["name"], "Hive_DeviceType": "Hub"})

        if len(HSC.products.heating) > 0:
            for product in HSC.products.heating:
                for device in HSC.devices.thermostat:
                    if product["parent"] == device["props"]["zone"]:
                        if "id" in product and "state" in product and "name" in product["state"]:
                            node_name = product["state"]["name"]
                            if len(HSC.products.heating) == 1:
                                node_name = None
                            device_list_climate.append({'HA_DeviceType': 'Heating', 'Hive_NodeID': product["id"], 'Hive_NodeName': node_name, 'Hive_DeviceType': "Heating", 'Thermostat_NodeID': device["id"]})
                            device_list_sensor.append({'HA_DeviceType': 'Heating_CurrentTemperature', 'Hive_NodeID': product["id"], 'Hive_NodeName': node_name, "Hive_DeviceType": "Heating"})
                            device_list_sensor.append({'HA_DeviceType': 'Heating_TargetTemperature', 'Hive_NodeID': product["id"], 'Hive_NodeName': node_name, "Hive_DeviceType": "Heating"})
                            device_list_sensor.append({'HA_DeviceType': 'Heating_State', 'Hive_NodeID': product["id"], 'Hive_NodeName': node_name, "Hive_DeviceType": "Heating"})
                            device_list_sensor.append({'HA_DeviceType': 'Heating_Mode', 'Hive_NodeID': product["id"], 'Hive_NodeName': node_name, "Hive_DeviceType": "Heating"})
                            device_list_sensor.append({'HA_DeviceType': 'Heating_Boost', 'Hive_NodeID': product["id"], 'Hive_NodeName': node_name, "Hive_DeviceType": "Heating"})

        if len(HSC.products.hotwater) > 0:
            for product in HSC.products.hotwater:
                if "id" in product and "state" in product and "name" in product["state"]:
                    node_name = product["state"]["name"]
                    if len(HSC.products.hotwater) == 1:
                        node_name = None
                    device_list_climate.append({'HA_DeviceType': 'HotWater', 'Hive_NodeID': product["id"], 'Hive_NodeName': node_name, "Hive_DeviceType": "HotWater"})
                    device_list_sensor.append({'HA_DeviceType': 'HotWater_State', 'Hive_NodeID': product["id"], 'Hive_NodeName': node_name, "Hive_DeviceType": "HotWater"})
                    device_list_sensor.append({'HA_DeviceType': 'HotWater_Mode', 'Hive_NodeID': product["id"], 'Hive_NodeName': node_name, "Hive_DeviceType": "HotWater"})
                    device_list_sensor.append({'HA_DeviceType': 'HotWater_Boost', 'Hive_NodeID': product["id"], 'Hive_NodeName': node_name, "Hive_DeviceType": "HotWater"})

        if len(HSC.devices.thermostat) > 0 or len(HSC.devices.sensors) > 0:
            all_devices = HSC.devices.thermostat + HSC.devices.sensors
            for a_device in all_devices:
                if "id" in a_device and "state" in a_device and "name" in a_device["state"]:
                    node_name = a_device["state"]["name"]
                    if a_device["type"] == "thermostatui" and len(HSC.devices.thermostat) == 1:
                        node_name = None
                    if "type" in a_device:
                        hive_device_type = a_device["type"]
                        device_list_sensor.append({'HA_DeviceType': 'Hive_Device_BatteryLevel', 'Hive_NodeID': a_device["id"], 'Hive_NodeName': node_name, "Hive_DeviceType": hive_device_type})
                        device_list_sensor.append({'HA_DeviceType': 'Hive_Device_Availability', 'Hive_NodeID': a_device["id"], 'Hive_NodeName': node_name, "Hive_DeviceType": hive_device_type})


        if len(HSC.products.light) > 0:
            for product in HSC.products.light:
                if "id" in product and "state" in product and "name" in product["state"]:
                    if "type" in product:
                        light_device_type = product["type"]
                        device_list_light.append({'HA_DeviceType': 'Hive_Device_Light', 'Hive_Light_DeviceType': light_device_type, 'Hive_NodeID': product["id"], 'Hive_NodeName': product["state"]["name"], "Hive_DeviceType": "Light"})
                        device_list_sensor.append({'HA_DeviceType': 'Hive_Device_Light_Mode', 'Hive_NodeID': product["id"], 'Hive_NodeName': product["state"]["name"], "Hive_DeviceType": light_device_type})
                        device_list_sensor.append({'HA_DeviceType': 'Hive_Device_Light_Availability', 'Hive_NodeID': product["id"], 'Hive_NodeName': product["state"]["name"], "Hive_DeviceType": light_device_type})


        if len(HSC.products.plug) > 0:
            for product in HSC.products.plug:
                if "id" in product and "state" in product and "name" in product["state"]:
                    if "type" in product:
                        plug_device_type = product["type"]
                        device_list_plug.append({'HA_DeviceType': 'Hive_Device_Plug', 'Hive_Plug_DeviceType': plug_device_type, 'Hive_NodeID': product["id"], 'Hive_NodeName': product["state"]["name"], "Hive_DeviceType": "Switch"})
                        device_list_sensor.append({'HA_DeviceType': 'Hive_Device_Plug_Mode', 'Hive_NodeID': product["id"], 'Hive_NodeName': product["state"]["name"], "Hive_DeviceType": plug_device_type})
                        device_list_sensor.append({'HA_DeviceType': 'Hive_Device_Plug_Availability', 'Hive_NodeID': product["id"], 'Hive_NodeName': product["state"]["name"], "Hive_DeviceType": plug_device_type})


        if len(HSC.products.sensors) > 0:
            for product in HSC.products.sensors:
                if "id" in product and "state" in product and "name" in product["state"]:
                    if "type" in product:
                        hive_sensor_device_type = product["type"]
                        device_list_binary_sensor.append({'HA_DeviceType': 'Hive_Device_Binary_Sensor', 'Hive_NodeID': product["id"], 'Hive_NodeName': product["state"]["name"], "Hive_DeviceType": hive_sensor_device_type})

        if HSC.weather.nodeid == "HiveWeather":
            device_list_sensor.append({'HA_DeviceType': 'Hive_OutsideTemperature', 'Hive_NodeID': HSC.weather.nodeid, 'Hive_NodeName': "Hive Weather", "Hive_DeviceType": "Weather"})

        device_list_all['device_list_sensor'] = device_list_sensor
        device_list_all['device_list_binary_sensor'] = device_list_binary_sensor
        device_list_all['device_list_climate'] = device_list_climate
        device_list_all['device_list_light'] = device_list_light
        device_list_all['device_list_plug'] = device_list_plug

        if HSC.logging.all or HSC.logging.core:
            Pyhiveapi.logger("pyhiveapi initialised")

        return device_list_all

    def test_use_file(self, devices, products):
        """Get latest data for Hive nodes."""
        get_nodes_successful = True

        usefile = True
        if usefile:
            HSC.file = True
            HSC.session_id = 'Test'

        tmp_devices_all = []
        tmp_devices_hub = []
        tmp_devices_thermostat = []
        tmp_devices_boiler_module = []
        tmp_devices_plug = []
        tmp_devices_light = []
        tmp_devices_sensors = []

        tmp_products_all = []
        tmp_products_heating = []
        tmp_products_hotwater = []
        tmp_products_light = []
        tmp_products_plug = []
        tmp_products_sensors = []

        if devices != None:
            try_finished = False
            try:
                api_resp_d = {}
                api_resp_p = None
                api_resp_d = devices

                api_resp_p = api_resp_d

                for a_device in api_resp_p:
                    tmp_devices_all.append(a_device)
                    if "type" in a_device:
                        if a_device["type"] == "hub":
                            tmp_devices_hub.append(a_device)
                        if a_device["type"] == "thermostatui":
                            tmp_devices_thermostat.append(a_device)
                        if a_device["type"] == "boilermodule":
                            tmp_devices_boiler_module.append(a_device)
                        if a_device["type"] == "activeplug":
                            tmp_devices_plug.append(a_device)
                        if (a_device["type"] == "warmwhitelight" or
                                a_device["type"] == "tuneablelight" or
                                a_device["type"] == "colourtuneablelight"):
                            tmp_devices_light.append(a_device)
                        if (a_device["type"] == "motionsensor" or
                                a_device["type"] == "contactsensor"):
                            tmp_devices_sensors.append(a_device)

                try_finished = True
            except (IOError, RuntimeError, ZeroDivisionError):
                try_finished = False
            finally:
                if not try_finished:
                    try_finished = False

        if products != None:

            try_finished = False
            try:
                api_resp_d = {}
                api_resp_p = None
                api_resp_d = products

                api_resp_p = api_resp_d
                for a_product in api_resp_p:
                    tmp_products_all.append(a_product)
                    if "type" in a_product:
                        if a_product["type"] == "heating":
                            tmp_products_heating.append(a_product)
                        if a_product["type"] == "hotwater":
                            tmp_products_hotwater.append(a_product)
                        if a_product["type"] == "activeplug":
                            tmp_products_plug.append(a_product)
                        if (a_product["type"] == "warmwhitelight" or
                                a_product["type"] == "tuneablelight" or
                                a_product["type"] == "colourtuneablelight"):
                            tmp_products_light.append(a_product)
                        if (a_product["type"] == "motionsensor" or
                                a_product["type"] == "contactsensor"):
                            tmp_products_sensors.append(a_product)
                try_finished = True
            except (IOError, RuntimeError, ZeroDivisionError):
                try_finished = False
            finally:
                if not try_finished:
                    try_finished = False

        try_finished = False
        try:
            if len(tmp_devices_hub) > 0:
                HSC.devices.hub = tmp_devices_hub
                for node in HSC.devices.hub:
                    HSC.devices.id_list.update({node["id"]: HSC.devices.hub})
            if len(tmp_devices_thermostat) > 0:
                HSC.devices.thermostat = tmp_devices_thermostat
                for node in HSC.devices.thermostat:
                    HSC.devices.id_list.update(
                        {node["id"]: HSC.devices.thermostat})
            if len(tmp_devices_boiler_module) > 0:
                HSC.devices.boiler_module = tmp_devices_boiler_module
                for node in HSC.devices.boiler_module:
                    HSC.devices.id_list.update(
                        {node["id"]: HSC.devices.boiler_module})
            if len(tmp_devices_plug) > 0:
                HSC.devices.plug = tmp_devices_plug
                for node in HSC.devices.plug:
                    HSC.devices.id_list.update({node["id"]: HSC.devices.plug})
            if len(tmp_devices_light) > 0:
                HSC.devices.light = tmp_devices_light
                for node in HSC.devices.light:
                    HSC.devices.id_list.update({node["id"]: HSC.devices.light})
            if len(tmp_devices_sensors) > 0:
                HSC.devices.sensors = tmp_devices_sensors
                for node in HSC.devices.sensors:
                    HSC.devices.id_list.update(
                        {node["id"]: HSC.devices.sensors})

            if len(tmp_products_heating) > 0:
                HSC.products.heating = tmp_products_heating
                for node in HSC.products.heating:
                    HSC.products.id_list.update(
                        {node["id"]: HSC.products.heating})
            if len(tmp_products_hotwater) > 0:
                HSC.products.hotwater = tmp_products_hotwater
                for node in HSC.products.hotwater:
                    HSC.products.id_list.update(
                        {node["id"]: HSC.products.hotwater})
            if len(tmp_products_plug) > 0:
                HSC.products.plug = tmp_products_plug
                for node in HSC.products.plug:
                    HSC.products.id_list.update(
                        {node["id"]: HSC.products.plug})
            if len(tmp_products_light) > 0:
                HSC.products.light = tmp_products_light
                for node in HSC.products.light:
                    HSC.products.id_list.update(
                        {node["id"]: HSC.products.light})
            if len(tmp_products_sensors) > 0:
                HSC.products.sensors = tmp_products_sensors
                for node in HSC.products.sensors:
                    HSC.products.id_list.update(
                        {node["id"]: HSC.products.sensors})

            try_finished = True
        except (IOError, RuntimeError, ZeroDivisionError):
                try_finished = False
        finally:
            if not try_finished:
                get_nodes_successful = False

        return get_nodes_successful

    def logger(new_message):
        """Output new log entry if logging is turned on."""
        if HSC.logging.enabled:
            try:
                log_file = open(HSC.logging.output_file, "a")
                log_file.write(datetime.now().strftime("%d-%b-%Y %H:%M:%S") + " : " + new_message + "\n")
                log_file.close
            except:
                log_file = None

    def epochtime(self, date_time):
        """ date/time conversion to epoch"""
        pattern = '%d.%m.%Y %H:%M:%S'
        epochtime = int(time.mktime(time.strptime(date_time, pattern)))
        return epochtime

   

   

   

   

   

   

   
