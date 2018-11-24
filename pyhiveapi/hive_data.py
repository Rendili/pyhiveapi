"""Hive Data Module."""
from datetime import datetime


class Data:
    """Hive Data"""

    NODE_INTERVAL_DEFAULT = 120
    WEATHER_INTERVAL_DEFAULT = 600
    data_present = False

    # API Data
    MODE = []
    BATTERY = []
    products = None
    devices = None
    NODES = {"Header": "HeaderText"}
    HIVETOHA = {"Light": {"ON": True, "OFF": False, "offline": False},
                "Switch": {"ON": True, "OFF": False, "offline": False},
                "Attribute": {True: "online", False: "offline"}}
    NAME = {}
    types = {'hub': ['hub'],
             'thermo': ['thermostatui'],
             'heating': ['heating'],
             'hotwater': ['hotwater'],
             'plug': ['activeplug'],
             'light': ['warmwhitelight', 'tuneablelight',
                       'colourtuneablelight'],
             'sensor': ['motionsensor', 'contactsensor']}

    # Session Data
    sess_id = ""
    s_platform_name = '',
    s_logon_datetime = datetime(2017, 1, 1, 12, 0, 0)
    s_username = ""
    s_password = ""
    s_postcode = ""
    s_timezone = ""
    s_countrycode = ""
    s_locale = ""
    s_temperature_unit = ""
    s_interval_seconds = NODE_INTERVAL_DEFAULT
    s_last_update = datetime(2017, 1, 1, 12, 0, 0)
    s_file = False

    # Weather data
    w_last_update = datetime(2017, 1, 1, 12, 0, 0)
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
    l_files = {'all': "logging.all",
               'core': "logging.core",
               'http': "logging.http",
               'heating': "logging.heating",
               'hotwater':  "logging.hotwater",
               'light': "logging.light",
               'switch': "logging.switch",
               'sensor': "logging.sensor",
               'attribute': "logging.attribute"}
    l_values = {}
