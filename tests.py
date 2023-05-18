import requests
import random
import sys

LOAD_BALANCER = sys.argv[1]
SERVICE_PATH = "RestaurantService"
CUSTOMER_NAME = random.randint(0, 10000)

retryCount = 3

for i in range(retryCount):
    print("Pinging /seatCustomer with missing param...")
    response = requests.post("http://" + LOAD_BALANCER + "/" + SERVICE_PATH + "/seatCustomer",
                             data = {'firstName': CUSTOMER_NAME, 'address': 'someaddress'})
    print("response: " + str(response.status_code))
    if response.status_code == 400: break
    if retryCount == 2: sys.exit(1)

for i in range(retryCount):
    print("Pinging /seatCustomer with invalid param...")
    response = requests.post("http://" + LOAD_BALANCER + "/" + SERVICE_PATH + "/seatCustomer",
                             data = {'firstName': CUSTOMER_NAME, 'address': 'someaddress', 'cash': "bad-value"})
    print("response: " + str(response.status_code))
    if response.status_code == 400: break
    if retryCount == 2: sys.exit(1)

for i in range(retryCount):
    print("Pinging /getOpenTables with valid request...")
    response = requests.get("http://" + LOAD_BALANCER + "/" + SERVICE_PATH + "/getOpenTables")
    print("response: " + str(response.status_code))
    if response.status_code == 200: break
    if retryCount == 2: sys.exit(1)

for i in range(retryCount):
    print("Pinging /submitOrder with insufficient funds...")
    response = requests.post("http://" + LOAD_BALANCER + "/" + SERVICE_PATH + "/submitOrder",
                             data = {'firstName': CUSTOMER_NAME, 'tableNumber': '1', 'dish': 'food', 'bill': 100.00})
    print("response: " + str(response.status_code))
    if response.status_code == 500: break
    if retryCount == 2: sys.exit(1)

for i in range(retryCount):
    print("Pinging /bootCustomer that has already been booted...")
    response = requests.post("http://" + LOAD_BALANCER + "/" + SERVICE_PATH + "/bootCustomer",
                             data={'firstName': CUSTOMER_NAME})
    print("response: " + str(response.status_code))
    if response.status_code == 404: break
    if retryCount == 2: sys.exit(1)
