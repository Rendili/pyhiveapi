from pyhiveapi.custom_logging import Logger
from pyhiveapi.hive_data import Data
import unittest
import os


class Custom_logging_Tests(unittest.TestCase):
    """Unit tests for the  Actiion Class."""

    def setUp(self):
        path = os.path.expanduser('~') + "/.homeassistant/pyhiveapi"
        filepath = os.path.join(path, 'log.all')
        try:
            f = open(filepath, 'w')
            f.close()
        except IOError:

    def tearDown(self):
        path = os.path.expanduser('~') + "/.homeassistant/pyhiveapi"
        filepath = os.path.join(path, 'log.all')
        os.remove(filepath)
        Data.l_values = {}

    def test_checking_if_logging_enabled(self):
        Logger.check_logging(new_session=False)
        self.assertIsNotNone(Data.l_values)


if __name__ == '__main__':
    unittest.main()
