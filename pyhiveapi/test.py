from pyhiveapi.hive_session import Session
from pyhiveapi.hive_data import Data
import json
import os


username = 'khole_47@hotmail.co.uk'
password = 'Aubree01062017'

devicelist = Session.initialise_api(Session(), username, password, 60)
print(devicelist)
with open(os.getcwd() + '/tests/responses/devicelist.json', 'w+', encoding="utf8") as f:
    json.dump(devicelist, f)
