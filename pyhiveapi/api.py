"""Hive APi."""
import requests


class Hive:
    """Hive API Class."""

    def __init__(self):
        """Hive API initialisation."""
        self.urls = {
            'login': "https://beekeeper.hivehome.com/1.0/global/login",
            'base': "https://beekeeper-uk.hivehome.com/1.0",
            'weather': "https://weather.prod.bgchprod.info/weather",
            'holiday_mode': "/holiday-mode",
            'devices': "/devices",
            'products': "/products",
            'nodes': "/nodes/{0}/{1}"
        }
        self.headers = {'content-type': 'application/json',
                        'Accept': '*/*',
                        'authorization': 'None'}
        self.timeout = 10
        self.json_return = {'original': "No response to Hive API request",
                            'parsed': "No response to Hive API request"}

    def login(self, username, password):
        try:
            j = '{{"username": "{0}", "password": "{1}"}}'.format(username,
                                                                  password)
            response = requests.post(url=self.urls['login'],
                                     headers=self.headers,
                                     data=j, timeout=self.timeout)
            self.json_return.update({'original': str(response)})
            self.json_return.update({'parsed': response.json()})
        except (ConnectionError, IOError, RuntimeError, ZeroDivisionError):
            self.error()

        return self.json_return

    def get_devices(self, session_id):
        self.headers.update({'authorization': session_id})
        url = self.urls['base'] + self.urls['devices']
        try:
            jsc = None
            response = requests.get(url=url, headers=self.headers,
                                    data=jsc, timeout=self.timeout)
            self.json_return.update({'original': str(response)})
            self.json_return.update({'parsed': response.json()})
        except (IOError, RuntimeError, ZeroDivisionError):
            self.error()

        return self.json_return

    def get_products(self, session_id):
        self.headers.update({'authorization': session_id})
        url = self.urls['base'] + self.urls['products']
        try:
            jsc = None
            response = requests.get(url=url, headers=self.headers,
                                    data=jsc, timeout=self.timeout)
            self.json_return.update({'original': str(response)})
            self.json_return.update({'parsed': response.json()})
        except (IOError, RuntimeError, ZeroDivisionError):
            self.error()

        return self.json_return

    def motion_sensor(self, session_id, sensor, fromepoch, toepoch):
        self.headers.update({'authorization': session_id})
        url = (self.urls['base'] + self.urls['products'] + '/'
               + sensor["type"] + '/' + sensor["id"]
               + '/events?from=' + str(fromepoch) + '&to=' + str(toepoch))
        try:
            jsc = None
            response = requests.get(url=url, headers=self.headers,
                                    data=jsc, timeout=self.timeout)
            self.json_return.update({'original': str(response)})
            self.json_return.update({'parsed': response.json()})
        except (IOError, RuntimeError, ZeroDivisionError):
            self.error()

        return self.json_return

    def get_weather(self, session_id, weather_url):
        self.headers.update({'authorization': session_id})
        t_url = self.urls['weather'] + weather_url
        url = t_url.replace(" ", "%20")
        try:
            jsc = None
            response = requests.get(url=url, headers=self.headers,
                                    data=jsc, timeout=self.timeout)
            self.json_return.update({'original': str(response)})
            self.json_return.update({'parsed': response.json()})
        except (IOError, RuntimeError, ZeroDivisionError):
            self.error()

        return self.json_return

    def set_state(self, session_id, type, id):
        self.headers.update({'authorization': session_id})
        jsc = '{"status": "OFF"}'
        url = self.urls['base'] + self.urls['nodes'].format(type, id)
        try:
            response = requests.post(url=url, headers=self.headers,
                                     data=jsc, timeout=self.timeout)
            self.json_return.update({'original': str(response)})
            self.json_return.update({'parsed': response.json()})
        except (IOError, RuntimeError, ZeroDivisionError):
            self.error()

        return self.json_return



    def set_brightness(self, session_id):
        self.headers.update({'authorization': session_id})

    def set_colour_temp(self, session_id):
        self.headers.update({'authorization': session_id})

    def set_colour(self, session_id):
        self.headers.update({'authorization': session_id})

    def error(self):
        self.json_return.update({'original': "Error parsing JSON data"})
        self.json_return.update({'original': "Error parsing JSON data"})
