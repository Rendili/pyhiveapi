#### Check if data needs updating on each get and set
#### Set private def prefix

import operator
from datetime import datetime
from datetime import timedelta
import requests

HIVE_NODE_UPDATE_INTERVAL_DEFAULT = 120
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


class HiveProducts:
    """Initiate Hive Products Class."""

    heating = []
    hotwater = []
    light = []
    plug = []
    sensors = []


class HivePlatformData:
    """Initiate Hive PlatformData Class."""

    min_max_data = {}


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
    platform_data = HivePlatformData()
#    holiday_mode = Hive_HolidayMode()
    update_interval_seconds = HIVE_NODE_UPDATE_INTERVAL_DEFAULT
    last_update = datetime(2017, 1, 1, 12, 0, 0)
    logging = False
    hass = None


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
    def __init__(self):
        """Initialise the base variable values."""
####        print("Initialise instance and base variables")

        HIVE_API.platform_name = ""

        HIVE_API.urls.global_login = \
            "https://beekeeper.hivehome.com/1.0/global/login"
        HIVE_API.urls.base = ""
        HIVE_API.urls.weather = "https://weather-prod.bgchprod.info/weather"
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

####        print("*** Finished setting base variables ***")


    def hive_api_json_call(self, request_type, request_url, json_string_content, login_request):
        """Call the JSON Hive API and return any returned data."""
        api_headers = {HIVE_API.headers.content_type_key:
                       HIVE_API.headers.content_type_value,
                       HIVE_API.headers.accept_key:
                       HIVE_API.headers.accept_value,
                       HIVE_API.headers.session_id_key:
                       HIVE_API.headers.session_id_value}

        json_return = {}
        full_request_url = ""

        if login_request:
            full_request_url = request_url
        else:
            full_request_url = HIVE_API.urls.base + request_url

        json_call_try_finished = False
        try:
            if request_type == "POST":
                json_response = requests.post(full_request_url,
                                              data=json_string_content,
                                              headers=api_headers)
            elif request_type == "GET":
                json_response = requests.get(full_request_url,
                                             data=json_string_content,
                                             headers=api_headers)
            elif request_type == "PUT":
                json_response = requests.put(full_request_url,
                                             data=json_string_content,
                                             headers=api_headers)
            else:
                json_response = ""
#                _LOGGER.error("Unknown JSON API call RequestType : %s", request_type)

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
####        print("log in to Hive API")
        login_details_found = True
        HSC.session_id = None

        try_finished = False
        try:
            api_resp_d = {}
            api_resp_p = None

            json_string_content = '{"username": "' \
                                  + HSC.username \
                                  + '","password": "' \
                                  + HSC.password + '"}'

            api_resp_d = self.hive_api_json_call("POST", HIVE_API.urls.global_login, json_string_content, True)
####            print ("Login API Response :")
####            print (api_resp_d)

            api_resp_p = api_resp_d['parsed']
####            print ("api_resp_d parsed to api_resp_p")
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
####            print ("SessionID :: " + HSC.session_id)
        except (IOError, RuntimeError, ZeroDivisionError):
            try_finished = False
        finally:
            if not try_finished:
                login_details_found = False

        if not login_details_found:
            HSC.session_id = None
#            _LOGGER.error("Hive API login failed with error : %s", api_resp_p)


    def check_hive_api_logon(self):
        """Check if currently logged in with a valid Session ID."""
        current_time = datetime.now()
        l_logon_secs = (current_time - HSC.session_logon_datetime).total_seconds()
        l_logon_mins = int(round(l_logon_secs / 60))

        if l_logon_mins >= MINUTES_BETWEEN_LOGONS or HSC.session_id is None:
            self.hive_api_logon()


    def hive_api_get_nodes_rl(self, node_id, device_type):
        """Get latest data for Hive nodes - rate limiting."""
        nodes_updated = False
        current_time = datetime.now()
        last_update_secs = (current_time - HSC.last_update).total_seconds()
        if last_update_secs >= HSC.update_interval_seconds:
            HSC.last_update = current_time
            nodes_updated = self.hive_api_get_nodes(node_id, device_type)
        return nodes_updated


    def hive_api_get_nodes_nl(self):
        """Get latest data for Hive nodes - not rate limiting."""
        self.hive_api_get_nodes("NoID", "NoDeviceType")


    def hive_api_get_nodes(self, node_id, device_type):
        """Get latest data for Hive nodes."""
        get_nodes_successful = True

        self.check_hive_api_logon()

        # pylint: disable=too-many-nested-blocks
        if HSC.session_id is not None:
            tmp_devices_hub = []
            tmp_devices_thermostat = []
            tmp_devices_boiler_module = []
            tmp_devices_plug = []
            tmp_devices_light = []
            tmp_devices_sensors = []

            tmp_products_heating = []
            tmp_products_hotwater = []
            tmp_products_light = []
            tmp_products_plug = []
            tmp_products_sensors = []

            try_finished = False
            try:
                api_resp_d = {}
                api_resp_p = None
                api_resp_d = self.hive_api_json_call("GET", HIVE_API.urls.devices, "", False)

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
 #                   _LOGGER.error("Error parsing Hive Devices")

            try_finished = False
            try:
                api_resp_d = {}
                api_resp_p = None
                api_resp_d = self.hive_api_json_call("GET",
                                                HIVE_API.urls.products,
                                                "",
                                                False)

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
#                    _LOGGER.error("Error parsing Hive Products")

            try_finished = False
            try:
                if len(tmp_devices_hub) > 0:
                    HSC.devices.hub = tmp_devices_hub
                if len(tmp_devices_thermostat) > 0:
                    HSC.devices.thermostat = tmp_devices_thermostat
                if len(tmp_devices_boiler_module) > 0:
                    HSC.devices.boiler_module = tmp_devices_boiler_module
                if len(tmp_devices_plug) > 0:
                    HSC.devices.plug = tmp_devices_plug
                if len(tmp_devices_light) > 0:
                    HSC.devices.light = tmp_devices_light
                if len(tmp_devices_sensors) > 0:
                    HSC.devices.sensors = tmp_devices_sensors

                if len(tmp_products_heating) > 0:
                    HSC.products.heating = tmp_products_heating
                if len(tmp_products_hotwater) > 0:
                    HSC.products.hotwater = tmp_products_hotwater
                if len(tmp_products_plug) > 0:
                    HSC.products.plug = tmp_products_plug
                if len(tmp_products_light) > 0:
                    HSC.products.light = tmp_products_light
                if len(tmp_products_sensors) > 0:
                    HSC.products.sensors = tmp_products_sensors

                try_finished = True
            except (IOError, RuntimeError, ZeroDivisionError):
                try_finished = False
            finally:
                if not try_finished:
                    get_nodes_successful = False
#                    _LOGGER.error("Error adding discovered Products / Devices")
        else:
            get_nodes_successful = False
#            _LOGGER.error("No Session ID")

#        if get_nodes_successful:
#            fire_bus_event(node_id, device_type)  ##### replace this in HA code ####

        return get_nodes_successful


    def p_get_heating_min_temp(self, node_id, device_type):
        """Get heating minimum target temperature."""
        heating_min_temp_default = 5
        heating_min_temp_return = 0
        heating_min_temp_tmp = 0
        heating_min_temp_found = False

        heating_min_temp_tmp = heating_min_temp_default

        current_node_attribute = "Heating_Min_Temperature_" + node_id

        if heating_min_temp_found:
            NODE_ATTRIBS[current_node_attribute] = heating_min_temp_tmp
            heating_min_temp_return = heating_min_temp_tmp
        else:
            if current_node_attribute in NODE_ATTRIBS:
                heating_min_temp_return = NODE_ATTRIBS.get(current_node_attribute)
            else:
                heating_min_temp_return = heating_min_temp_default

        return heating_min_temp_return


    def p_get_heating_max_temp(self, node_id, device_type):
        """Get heating maximum target temperature."""
        heating_max_temp_default = 32
        heating_max_temp_return = 0
        heating_max_temp_tmp = 0
        heating_max_temp_found = False

        heating_max_temp_tmp = heating_max_temp_default

        current_node_attribute = "Heating_Max_Temperature_" + node_id

        if heating_max_temp_found:
            NODE_ATTRIBS[current_node_attribute] = heating_max_temp_tmp
            heating_max_temp_return = heating_max_temp_tmp
        else:
            if current_node_attribute in NODE_ATTRIBS:
                heating_max_temp_return = NODE_ATTRIBS.get(current_node_attribute)
            else:
                heating_max_temp_return = heating_max_temp_default

        return heating_max_temp_return


    def p_get_heating_current_temp(self, node_id, device_type):
        """Get heating current temperature."""
        node_index = -1

        current_temp_return = 0
        current_temp_tmp = 0
        current_temp_found = False

        current_node_attribute = "Heating_CurrentTemp_" + node_id

        if len(HSC.products.heating) > 0:
            for current_node_index in range(0, len(HSC.products.heating)):
                if "id" in HSC.products.heating[current_node_index]:
                    if HSC.products.heating[current_node_index]["id"] == node_id:
                        node_index = current_node_index
                        break

            if node_index != -1:
                if "props" in HSC.products.heating[node_index]:
                    if "temperature" in HSC.products.heating[node_index]["props"]:
                        current_temp_tmp = (HSC.products.heating[node_index]
                                            ["props"]["temperature"])
                        current_temp_found = True

        if current_temp_found:
            NODE_ATTRIBS[current_node_attribute] = current_temp_tmp
            current_temp_return = current_temp_tmp
        else:
            if current_node_attribute in NODE_ATTRIBS:
                current_temp_return = NODE_ATTRIBS.get(current_node_attribute)
            else:
                current_temp_return = -1000

        if current_temp_return != -1000:
            if node_id in HSC.platform_data.min_max_data:
                if (HSC.platform_data.min_max_data[node_id]['TodayDate'] !=
                        datetime.date(datetime.now())):
                    HSC.platform_data.min_max_data[node_id]['TodayMin'] = 1000
                    HSC.platform_data.min_max_data[node_id]['TodayMax'] = -1000
                    HSC.platform_data.min_max_data[node_id]['TodayDate'] = \
                        datetime.date(datetime.now())

                if (current_temp_return <
                        HSC.platform_data.min_max_data[node_id]['TodayMin']):
                    HSC.platform_data.min_max_data[node_id]['TodayMin'] = \
                        current_temp_return

                if (current_temp_return >
                        HSC.platform_data.min_max_data[node_id]['TodayMax']):
                    HSC.platform_data.min_max_data[node_id]['TodayMax'] = \
                        current_temp_return

                if (current_temp_return <
                        HSC.platform_data.min_max_data[node_id]['RestartMin']):
                    HSC.platform_data.min_max_data[node_id]['RestartMin'] = \
                        current_temp_return

                if current_temp_return > \
                        HSC.platform_data.min_max_data[node_id]['RestartMax']:
                    HSC.platform_data.min_max_data[node_id]['RestartMax'] = \
                        current_temp_return
            else:
                current_node_max_min_data = {}
                current_node_max_min_data['TodayMin'] = current_temp_return
                current_node_max_min_data['TodayMax'] = current_temp_return
                current_node_max_min_data['TodayDate'] = \
                    datetime.date(datetime.now())
                current_node_max_min_data['RestartMin'] = current_temp_return
                current_node_max_min_data['RestartMax'] = current_temp_return
                HSC.platform_data.min_max_data[node_id] = \
                    current_node_max_min_data

        else:
            current_temp_return = 0

        return current_temp_return


    def initialise_api(self, username, password, mins_between_updates):
        """Setup the Hive platform."""
#        initialise_app()

#        HSC.hass = hass

        HSC.username = username
        HSC.password = password

#        hive_config = config[DOMAIN]

#        if "username" in hive_config and "password" in hive_config:
#            HSC.username = config[DOMAIN]['username']
#            HSC.password = config[DOMAIN]['password']
#        else:
#            _LOGGER.error("Missing UserName or Password in config")

#        if "minutes_between_updates" in hive_config:
#            tmp_mins_between_upds = config[DOMAIN]['minutes_between_updates']
#        else:
#            tmp_mins_between_upds = 2

#        hive_node_update_interval = tmp_mins_between_upds * 60
        if mins_between_updates <= 0:
            mins_between_updates = 2

        hive_node_update_interval = mins_between_updates * 60

#        if "logging" in hive_config:
#            if config[DOMAIN]['logging']:
#                HSC.logging = True
#                _LOGGER.warning("Logging is Enabled")
#            else:
#                HSC.logging = False
#        else:
#            HSC.logging = False

        if HSC.username is None or HSC.password is None:
            return None
#            _LOGGER.error("Missing UserName or Password in Hive Session details")
        else:
####            print ("Logging in : " + username + " :: " + password)
            self.hive_api_logon()
            if HSC.session_id is not None:
                HSC.update_interval_seconds = hive_node_update_interval
                self.hive_api_get_nodes_nl()

        config_devices = []

#        if "devices" in hive_config:
#            config_devices = config[DOMAIN]['devices']

#        device_count = 0

        device_list_all = {}
        device_list_sensor = []
        device_list_climate = []
        device_list_light = []
        device_list_plug = []

        if len(HSC.products.heating) > 0:
            for product in HSC.products.heating:
                if ("id" in product and "state" in product and "name" in product["state"]):
                    node_name = product["state"]["name"]
                    if len(HSC.products.heating) == 1:
                        node_name = None

#                    if (len(config_devices) == 0 or (len(config_devices) > 0 and "hive_heating" in config_devices)):
#                        device_count = device_count + 1
                    device_list_climate.append({'HA_DeviceType': 'Heating', 'Hive_NodeID': product["id"], 'Hive_NodeName': node_name})

#                    if (len(config_devices) == 0 or (len(config_devices) > 0 and "hive_heating_currenttemperature" in config_devices)):
#                        device_count = device_count + 1
                    device_list_sensor.append({'HA_DeviceType': 'Heating_CurrentTemperature', 'Hive_NodeID': product["id"], 'Hive_NodeName': node_name})

#                    if (len(config_devices) == 0 or (len(config_devices) > 0 and "hive_heating_targettemperature" in config_devices)):
#                        device_count = device_count + 1
                    device_list_sensor.append({'HA_DeviceType': 'Heating_TargetTemperature', 'Hive_NodeID': product["id"], 'Hive_NodeName': node_name})

#                    if (len(config_devices) == 0 or (len(config_devices) > 0 and "hive_heating_state" in config_devices)):
#                        device_count = device_count + 1
                    device_list_sensor.append({'HA_DeviceType': 'Heating_State', 'Hive_NodeID': product["id"], 'Hive_NodeName': node_name})

#                    if (len(config_devices) == 0 or (len(config_devices) > 0 and "hive_heating_mode" in config_devices)):
#                        device_count = device_count + 1
                    device_list_sensor.append({'HA_DeviceType': 'Heating_Mode', 'Hive_NodeID': product["id"], 'Hive_NodeName': node_name})

#                    if (len(config_devices) == 0 or (len(config_devices) > 0 and "hive_heating_boost" in config_devices)):
#                        device_count = device_count + 1
                    device_list_sensor.append({'HA_DeviceType': 'Heating_Boost', 'Hive_NodeID': product["id"], 'Hive_NodeName': node_name})

        if len(HSC.products.hotwater) > 0:
            for product in HSC.products.hotwater:
                if ("id" in product and "state" in product and "name" in product["state"]):
                    node_name = product["state"]["name"]
                    if len(HSC.products.hotwater) == 1:
                        node_name = None

#                   if (len(config_devices) == 0 or (len(config_devices) > 0 and "hive_hotwater" in config_devices)):
#                        device_count = device_count + 1
                    device_list_climate.append({'HA_DeviceType': 'HotWater', 'Hive_NodeID': product["id"], 'Hive_NodeName': node_name})

#                    if (len(config_devices) == 0 or (len(config_devices) > 0 and "hive_hotwater_state" in config_devices)):
#                        device_count = device_count + 1
                    device_list_sensor.append({'HA_DeviceType': 'HotWater_State', 'Hive_NodeID': product["id"], 'Hive_NodeName': node_name})

#                    if (len(config_devices) == 0 or (len(config_devices) > 0 and "hive_hotwater_mode" in config_devices)):
#                        device_count = device_count + 1
                    device_list_sensor.append({'HA_DeviceType': 'HotWater_Mode', 'Hive_NodeID': product["id"], 'Hive_NodeName': node_name})

#                    if (len(config_devices) == 0 or (len(config_devices) > 0 and "hive_hotwater_boost" in config_devices)):
#                        device_count = device_count + 1
                    device_list_sensor.append({'HA_DeviceType': 'HotWater_Boost', 'Hive_NodeID': product["id"], 'Hive_NodeName': node_name})

        if len(HSC.devices.thermostat) > 0 or len(HSC.devices.sensors) > 0:
            all_devices = HSC.devices.thermostat + HSC.devices.sensors
            for a_device in all_devices:
                if ("id" in a_device and "state" in a_device and "name" in a_device["state"]):
                    node_name = a_device["state"]["name"]
                    if (a_device["type"] == "thermostatui" and len(HSC.devices.thermostat) == 1):
                        node_name = None
                    if (len(config_devices) == 0 or len(config_devices) > 0 and "hive_thermostat_batterylevel" or len(config_devices) > 0 and "hive_sensor_batterylevel" in config_devices):
#                        device_count = device_count + 1
                        if "type" in a_device:
                            hive_device_type = a_device["type"]
                            device_list_sensor.append({'HA_DeviceType': 'Hive_Device_BatteryLevel', 'Hive_NodeID': a_device["id"], 'Hive_NodeName': node_name, "Hive_DeviceType": hive_device_type})

        # pylint: disable=too-many-nested-blocks
        if len(HSC.products.light) > 0:
            for product in HSC.products.light:
                if ("id" in product and "state" in product and "name" in product["state"]):
                    if (len(config_devices) == 0 or (len(config_devices) > 0 and "hive_active_light" in config_devices)):
#                        device_count = device_count + 1
                        if "type" in product:
                            light_device_type = product["type"]
#                            if HSC.logging:
#                                _LOGGER.warning("Adding %s, %s to device list",
#                                                product["type"],
#                                                product["state"]["name"])
                            device_list_light.append({'HA_DeviceType': 'Hive_Device_Light', 'Hive_Light_DeviceType': light_device_type, 'Hive_NodeID': product["id"], 'Hive_NodeName': product["state"]["name"]})
                            if (len(config_devices) == 0 or (len(config_devices) > 0 and "hive_active_light_sensor" in config_devices)):
                                device_list_sensor.append({'HA_DeviceType': 'Hive_Device_Light_Mode', 'Hive_NodeID': product["id"], 'Hive_NodeName': product["state"]["name"], "Hive_DeviceType": light_device_type})

        # pylint: disable=too-many-nested-blocks
        if len(HSC.products.plug) > 0:
            for product in HSC.products.plug:
                if ("id" in product and "state" in product and "name" in product["state"]):
                    if (len(config_devices) == 0 or (len(config_devices) > 0 and "hive_active_plug" in config_devices)):
#                        device_count = device_count + 1
                        if "type" in product:
                            plug_device_type = product["type"]
#                            if HSC.logging:
#                                _LOGGER.warning("Adding %s, %s to device list",
#                                                product["type"],
#                                                product["state"]["name"])
                            device_list_plug.append({'HA_DeviceType': 'Hive_Device_Plug', 'Hive_Plug_DeviceType': plug_device_type, 'Hive_NodeID': product["id"], 'Hive_NodeName': product["state"]["name"]})
                            if (len(config_devices) == 0 or (len(config_devices) > 0 and "hive_active_plug_sensor" in config_devices)):
                                device_list_sensor.append({'HA_DeviceType': 'Hive_Device_Plug_Mode', 'Hive_NodeID': product["id"], 'Hive_NodeName': product["state"]["name"], "Hive_DeviceType": plug_device_type})

        if len(HSC.products.sensors) > 0:
            for product in HSC.products.sensors:
                if ("id" in product and "state" in product and "name" in product["state"]):
                    if (len(config_devices) == 0 or len(config_devices) > 0 and "hive_active_sensor" in config_devices):
#                        device_count = device_count + 1
                        if "type" in product:
                            hive_sensor_device_type = product["type"]
                            device_list_sensor.append({'HA_DeviceType': 'Hive_Device_Sensor', 'Hive_NodeID': product["id"], 'Hive_NodeName': product["state"]["name"], "Hive_DeviceType": hive_sensor_device_type})

#        global HGO

#        try:
#            HGO = HiveObjects()
#        except RuntimeError:
#            return False

#        if (len(device_list_sensor) > 0 or len(device_list_climate) > 0 or len(device_list_light) > 0 or len(device_list_plug) > 0):
####            print (device_list_climate)
#            return device_list_climate
#        else:
#            return None
#            if len(device_list_sensor) > 0:
#                load_platform(hass, 'sensor', DOMAIN, device_list_sensor)
#            if len(device_list_climate) > 0:
 #               load_platform(hass, 'climate', DOMAIN, device_list_climate)
 #           if len(device_list_light) > 0:
#                load_platform(hass, 'light', DOMAIN, device_list_light)
#            if len(device_list_plug) > 0:
#                load_platform(hass, 'switch', DOMAIN, device_list_plug)
#            return True

        device_list_all['device_list_sensor'] = device_list_sensor
        device_list_all['device_list_climate'] = device_list_climate
        device_list_all['device_list_light'] = device_list_light
        device_list_all['device_list_plug'] = device_list_plug


        return device_list_all
 
    def GetSessionID(self):
        return HSC.session_id
