"""Hive Data Module."""
import datetime


class Data:
    """Hive Data"""

    NODE_INTERVAL_DEFAULT = 120
    WEATHER_INTERVAL_DEFAULT = 600

    # API Data
    MODE = []
    BATTERY = []
    products = {}
    devices = {}
    actions = {}
    entities = {"Header": "HeaderText"}
    NODES = {"Preheader": {"Header": "HeaderText"}}
    HIVETOHA = {
        "Attribute": {True: "Online", False: "Offline"},
        "Boost": {None: "OFF", "Offline": "OFF"},
        "Heating": {"Offline": "OFF"},
        "Hotwater": {"MANUAL": "ON", None: "OFF", "Offline": "OFF"},
        "Hub": {
            "Status": {True: "Online", False: "Offline"},
            "Smoke": {True: "Alarm Detected", False: "Clear", "Offline": "Offline"},
            "Dog": {True: "Barking Detected", False: "Clear", "Offline": "Offline"},
            "Glass": {True: "Noise Detected", False: "Clear", "Offline": "Offline"},
        },
        "Light": {"ON": True, "OFF": False, "Offline": False},
        "Sensor": {"OPEN": True, "CLOSED": False, "Offline": False},
        "Switch": {"ON": True, "OFF": False, "Offline": False},
    }
    NAME = {}
    HIVE_TYPES = {
        "Hub": ["hub", "sense"],
        "Thermo": ["thermostatui"],
        "Heating": ["heating"],
        "Hotwater": ["hotwater"],
        "Plug": ["activeplug"],
        "Light": ["warmwhitelight", "tuneablelight", "colourtuneablelight"],
        "Sensor": ["motionsensor", "contactsensor"],
    }
    HA_TYPES = {
        "Climate": ["heating"],
        "Water_Heater": ["hotwater"],
        "Switch": ["activeplug", "action"],
        "Light": ["warmwhitelight", "tuneablelight", "colourtuneablelight"],
        "Sensor": ["hub", "sense", "thermostatui"],
        "Binary_Sensor": ["motionsensor", "contactsensor"],
    }

    # Session Data
    sess_id = None
    s_platform_name = ""
    s_logon_datetime = datetime.datetime.now()
    s_username = ""
    s_password = ""
    s_postcode = ""
    s_timezone = ""
    s_countrycode = ""
    s_locale = ""
    s_temperature_unit = ""
    s_interval_seconds = NODE_INTERVAL_DEFAULT
    s_last_update = datetime.datetime(2017, 1, 1, 12, 0, 0)
    s_file = False

    # Weather data
    w_last_update = datetime.datetime(2017, 1, 1, 12, 0, 0)
    w_nodeid = ""
    w_icon = ""
    w_description = ""
    w_interval_seconds = WEATHER_INTERVAL_DEFAULT
    w_temperature_unit = ""
    w_temperature_value = 0.00

    # Platform data
    p_minmax = {}

    # Logging data
    l_o_folder = ""
    l_o_file = ""
    l_files = {
        "All": "log.all",
        "Action": "log.aciton",
        "Attribute": "log.attribute",
        "API": "log.api",
        "API_CORE": "log.api_core",
        "ERROR": "log.error",
        "Heating": "log.heating",
        "Hotwater": "log.hotwater",
        "Light": "log.light",
        "Sensor": "log.sensor",
        "Session": "log.session",
        "Switch": "log.switch",
    }
    l_values = {}
