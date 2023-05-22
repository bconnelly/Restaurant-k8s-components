import requests
import random
import sys

LOAD_BALANCER = sys.argv[1]
SERVICE_PATH = "RestaurantService"
CUSTOMER_NAME = random.randint(0, 10000)

retryCount = 3

for i in range(retryCount):
    print("Pinging /seatCustomer with missing param...")
    response = requests.post(f"http://{LOAD_BALANCER}/{SERVICE_PATH}/seatCustomer",
                             data = {"firstName": CUSTOMER_NAME, "address": "someaddress"})
    print(f"response: {str(response.status_code)}")
    if response.status_code == 400: break
    if i == 2: sys.exit(1)

for i in range(retryCount):
    print("Pinging /seatCustomer with invalid param...")
    response = requests.post(f"http://{LOAD_BALANCER}/{SERVICE_PATH}/seatCustomer",
                             data = {"firstName": CUSTOMER_NAME, "address": "someaddress", "cash": "bad-value"})
    print(f"response: {str(response.status_code)}")
    if response.status_code == 400: break
    if i == 2: sys.exit(1)

for i in range(retryCount):
    print("Pinging /getOpenTables with valid request...")
    response = requests.get(f"http://{LOAD_BALANCER}/{SERVICE_PATH}/getOpenTables")
    print(f"response: {str(response.status_code)}")
    if response.status_code == 200: break
    if i == 2: sys.exit(1)

for i in range(retryCount):
    print("Pinging /bootCustomer that has already been booted...")
    response = requests.post(f"http://{LOAD_BALANCER}/{SERVICE_PATH}/bootCustomer",
                             data={"firstName": CUSTOMER_NAME})
    print(f"response: {str(response.status_code)}")
    if response.status_code == 404: break
    if i == 2: sys.exit(1)
