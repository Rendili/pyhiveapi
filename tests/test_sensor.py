from pyhiveapi.sensor import Sensor
from pyhiveapi.hive_data import Data
import unittest
import json
import os


def open_file(file):
    path = os.getcwd() + '/tests/responses/' + file
    json_data = open(path).read()

    return json.loads(json_data)


class Hub_Tests(unittest.TestCase):
    """Unit tests for the Logger Class."""

    def setUp(self):
        products = open_file('parsed_products.json')
        devices = open_file('parsed_devices.json')
        nodes = open_file('NODES.json')
        Data.products = products
        Data.devices = devices
        Data.NODES = nodes

    def tearDown(self):
        Data.products = {}
        Data.devices = {}
