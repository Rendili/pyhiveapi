"""Hive API Module."""
import requests
from pyhiveapi.custom_logging import Logger


class Hive:
    """Hive API Code."""

    def __init__(self):
        """Hive API initialisation."""
        self.log = Logger()
        self.urls = {
            'login': "https://beekeeper.hivehome.com/1.0/global/login",
            'base': "https://beekeeper-uk.hivehome.com/1.0",
            'weather': "https://weather.prod.bgchprod.info/weather",
            'holiday_mode': "/holiday-mode",
            'devices': "/devices",
            'products': "/products",
            'actions': "/actions",
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

    def get_actions(self, session_id):
        self.headers.update({'authorization': session_id})
        url = self.urls['base'] + self.urls['actions']
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
        url = (self.urls['base'] + self.urls['products'] + '/' +
               sensor["type"] + '/' + sensor["id"] +
               '/events?from=' + str(fromepoch) + '&to=' + str(toepoch))
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
        except (IOError, RuntimeError, ZeroDivisionError, ConnectionError):
            self.error()

        return self.json_return

    def set_state(self, session_id, n_type, n_id, **kwargs):
        self.headers.update({'authorization': session_id})
        jsc = '{' + ','.join(('"' + str(i) + '": ' '"' + str(t) +
                              '" ' for i, t in kwargs.items())) + '}'

        url = self.urls['base'] + self.urls['nodes'].format(n_type, n_id)

        self.log.log(n_id, 'api_core', "Headers >\n{0}\nURL >\n{1}\n" +
                     "Payload\n{2}\n".format(self.headers, url, jsc))
        try:
            response = requests.post(url=url, headers=self.headers,
                                     data=jsc, timeout=self.timeout)
            self.json_return.update({'original': str(response)})
            self.json_return.update({'parsed': response.json()})
        except (IOError, RuntimeError, ZeroDivisionError, ConnectionError):
            self.error()

        return self.json_return

    def set_action(self, session_id, n_id, data):
        self.headers.update({'authorization': session_id})
        jsc = data
        url = self.urls['base'] + self.urls['actions'] + "/" + n_id
        self.log.log(n_id, 'api_core', "Headers >\n{0}\nURL >\n{1}\n" +
                     "Payload\n{2}\n".format(self.headers, url, jsc))
        try:
            response = requests.put(url=url, headers=self.headers,
                                    data=jsc, timeout=self.timeout)
            self.json_return.update({'original': str(response)})
            self.json_return.update({'parsed': response.json()})
        except (IOError, RuntimeError, ZeroDivisionError, ConnectionError):
            self.error()

        return self.json_return

    def set_brightness(self, session_id, n_type, n_id, brightness):
        self.headers.update({'authorization': session_id})
        jsc = '{{"status": "ON", "brightness": {0}}}'.format(brightness)
        url = self.urls['base'] + self.urls['nodes'].format(n_type, n_id)
        try:
            response = requests.post(url=url, headers=self.headers,
                                     data=jsc, timeout=self.timeout)
            self.json_return.update({'original': str(response)})
            self.json_return.update({'parsed': response.json()})
        except (IOError, RuntimeError, ZeroDivisionError, ConnectionError):
            self.error()

        return self.json_return

    def set_color_temp(self, session_id, n_type, n_id, color_temp):
        self.headers.update({'authorization': session_id})
        if n_type == "tuneablelight":
            jsc = '{{"colourTemperature": "{0}"}}'.format(color_temp)
        else:
            jsc = '{"colourMode": "WHITE", "colourTemperature": ' \
                  + '"0}"}'.format(color_temp)
        url = self.urls['base'] + self.urls['nodes'].format(n_type, n_id)
        try:
            response = requests.post(url=url, headers=self.headers,
                                     data=jsc, timeout=self.timeout)
            self.json_return.update({'original': str(response)})
            self.json_return.update({'parsed': response.json()})
        except (IOError, RuntimeError, ZeroDivisionError, ConnectionError):
            self.error()

        return self.json_return

    def set_color(self, session_id, n_type, n_id, hue, sat, val):
        self.headers.update({'authorization': session_id})
        jsc = '{{"colourMode": "COLOUR", "hue": "{0}", "saturation": "{1}", ' \
              + '"value": "{2}"}}'.format(hue, sat, val)

        url = self.urls['base'] + self.urls['nodes'].format(n_type, n_id)
        try:
            response = requests.post(url=url, headers=self.headers,
                                     data=jsc, timeout=self.timeout)
            self.json_return.update({'original': str(response)})
            self.json_return.update({'parsed': response.json()})
        except (IOError, RuntimeError, ZeroDivisionError, ConnectionError):
            self.error()

        return self.json_return

    def error(self):
        self.json_return.update({'original': "Error making API call"})
        self.json_return.update({'parsed': "Error making API call"})
        self.log.log('API_ERROR', 'ERROR', "Error attempting API call")
