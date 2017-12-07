
from pyhiveapi import Pyhiveapi
import json

HiveAPI = Pyhiveapi()
HiveDevice = Pyhiveapi.Light()

print('Using File')
devices = (input("Enter path for the devices file : ") or None)
if devices != None:
    JSON_File = open(devices, 'r')
    devices_t = JSON_File.read()
    JSON_File.close()
    devices = json.loads(devices_t)

products = (input("Enter path for the products file : ") or None)
if products != None:
    JSON_File = open(products, 'r')
    products_t = JSON_File.read()
    JSON_File.close()
    products = json.loads(products_t)
print()

for a_product in products:
    print(a_product["type"] + " : " + a_product["id"])
print()
node_id = input("Enter Node id : ")
result = HiveAPI.test_use_file(devices, products)
info = HiveDevice.set_colour(node_id, new_colour=(0, 99, 100))
print(info)