from pyhiveapi.action import Actionll
from pyhiveapi.hive_data import Data
import unittest
import json
import os


def open_file(file):
    path = os.getcwd() + '/tests/responses/' + file
    json_data = open(path).read()

    return json.loads(json_data)


class Action_Tests(unittest.TestCase):
    """Unit tests for the  Actiion Class."""

    def setUp(self):
        actions = open_file('parsed_actions.json')
        nodes = open_file('NODES.json')
        Data.actions = actions
        Data.NODES = nodes

    def tearDown(self):
        Data.actions = {}
        Data.NODES = {'Preheader': {'Header': 'HeaderText'}}

    def test_actions_is_off(self):
        id_n = 'action2-0000-0000-0000-00000000002'
        end = Action.get_state(Action(), id_n)
        print(end)
        self.assertEqual(end, False)

    def test_actions_is_on(self):
        id_n = 'action1-0000-0000-0000-000000000001'
        end = Action.get_state(Action(), id_n)
        print(end)
        self.assertEqual(end, True)

    def test_turn_action_on(self):
        id_n = 'action2-0000-0000-0000-000000000002'
        Action.turn_on(Action(), id_n)
        print(Data.actions[id_n]['enabled'])
        self.assertEqual(Data.actions[id_n]['enabled'], True)


if __name__ == '__main__':
    unittest.main()
