from pyhiveapi.plug import Plug
from pyhiveapi.hive_data import Data
import unittest
import json
import os


def open_file(file):
    path = os.getcwd() + '/tests/responses/' + file
    json_data = open(path).read()

    return json.loads(json_data)


class Plug_Tests(unittest.TestCase):
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

    def test_get_state(self):
        id_n = "plug-0000-0000-0000-000000000001"
        end = Plug.get_state(Plug(), id_n)
        print(end)
        self.assertIsNotNone(end)

    def test_get_power_usage(self):
        id_n = "plug-0000-0000-0000-000000000001"
        end = Plug.get_power_usage(Plug(), id_n)
        print(end)
        self.assertIsNotNone(end)


if __name__ == '__main__':
    unittest.main()
