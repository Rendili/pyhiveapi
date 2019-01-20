"""Hive Data Module."""
from datetime import datetime


class Data:
    """Hive Data"""

    NODE_INTERVAL_DEFAULT = 120
    WEATHER_INTERVAL_DEFAULT = 600

    # API Data
    MODE = []
    BATTERY = []
    products = None
    devices = None
    actions = None
    NODES = {'Header': 'HeaderText'}
    HIVETOHA = {'Attribute': {True: 'Online', False: 'Offline'},
                'Boost': {None: 'OFF', 'offline': 'OFF'},
                'Heating': {'offline': 'OFF'},
                'Hotwater': {'MANUAL': 'ON', None: 'OFF'},
                'Hub': {'Status': {True: 'Online', False: 'Offline', 'offline': 'Offline'},
                        'Smoke': {True: "Smoke Alarm Detected", False:
                                  "Nothing Detected", 'offline': 'Offline'},
                        'Dog': {True: "Dog Bark Detected", False:
                                "Nothing Detected", 'offline': 'Offline'},
                        'Glass': {True: "Broken Glass Detected", False:
                                  "Nothing Detected", 'offline': 'Offline'}},
                'Light': {'ON': True, 'OFF': False, 'offline': False},
                'Sensor': {'OPEN': True, 'CLOSED': False, 'offline': False},
                'Switch': {'ON': True, 'OFF': False, 'offline': False}
                }
    NAME = {}
    types = {'hub': ['hub', 'sense'],
             'thermo': ['thermostatui'],
             'heating': ['heating'],
             'hotwater': ['hotwater'],
             'plug': ['activeplug'],
             'light': ['warmwhitelight', 'tuneablelight',
                       'colourtuneablelight'],
             'sensor': ['motionsensor', 'contactsensor']}

    # Session Data
    sess_id = ''
    s_platform_name = '',
    s_logon_datetime = datetime(2017, 1, 1, 12, 0, 0)
    s_username = ''
    s_password = ''
    s_postcode = ''
    s_timezone = ''
    s_countrycode = ''
    s_locale = ''
    s_temperature_unit = ''
    s_interval_seconds = NODE_INTERVAL_DEFAULT
    s_last_update = datetime(2017, 1, 1, 12, 0, 0)
    s_file = False
    t_file = None

    # Weather data
    w_last_update = datetime(2017, 1, 1, 12, 0, 0)
    w_nodeid = ''
    w_icon = ''
    w_description = ''
    w_interval_seconds = WEATHER_INTERVAL_DEFAULT
    w_temperature_unit = ''
    w_temperature_value = 0.00

    # Platform data
    p_minmax = {}

    # Logging data
    l_o_folder = ''
    l_o_file = ''
    l_files = {'all': 'logging.all',
               'action': 'logging.aciton',
               'core': 'logging.core',
               'http': 'logging.http',
               'heating': 'logging.heating',
               'hotwater':  'logging.hotwater',
               'light': 'logging.light',
               'switch': 'logging.switch',
               'sensor': 'logging.sensor',
               'attribute': 'logging.attribute'}
    l_values = {}
