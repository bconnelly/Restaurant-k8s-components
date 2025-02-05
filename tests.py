import logging
import string
import time
import uuid

import requests
import random
import sys
import logging
import secrets
from enum import Enum

LOAD_BALANCER = sys.argv[1]
SERVICE_PATH = "RestaurantService"

# random unique name
CUSTOMER_NAME = str(uuid.uuid4())

retryCount = 3


class RequestType(Enum):
    GET = 0
    POST = 1
    PUT = 2
    DELETE = 3


def sendRequest(params, endpoint, reqType, expectedCode):
    print(CUSTOMER_NAME)
    for i in range(retryCount):
        logging.debug(f"Sending {reqType} request to {endpoint} with params {params}")

        if reqType == RequestType.GET:
            response = requests.get(f"http://{LOAD_BALANCER}/{SERVICE_PATH}/{endpoint}", params=params)
        elif reqType == RequestType.POST:
            response = requests.post(f"http://{LOAD_BALANCER}/{SERVICE_PATH}/{endpoint}", params=params)
        elif reqType == RequestType.PUT:
            response = requests.put(f"http://{LOAD_BALANCER}/{SERVICE_PATH}/{endpoint}", params=params)
        elif reqType == RequestType.DELETE:
            response = requests.delete(f"http://{LOAD_BALANCER}/{SERVICE_PATH}/{endpoint}", params=params)
        else:
            raise Exception(f"Request type {reqType} not supported")

        if response.status_code == expectedCode:
            return
        elif i == 2:
            logging.debug(f"Expected response code {expectedCode}, got {response.status_code}")
            raise Exception(f"Expected response code {expectedCode}, got {response.status_code}")


def main():
    # /seatCustomer with missing param
    sendRequest({"firstName": CUSTOMER_NAME, "address": "someaddress"}, "seatCustomer", RequestType.POST, 400)
    # /seatCustomer with bad param value
    sendRequest({"firstName": CUSTOMER_NAME, "address": "someaddress", "cash": "bad-value"}, "seatCustomer", RequestType.POST, 400)
    # /getOpenTables with valid request
    sendRequest(None, "getOpenTables", RequestType.GET, 200)
    # /bootCustomer with customer not in restaurant
    sendRequest({"firstName": CUSTOMER_NAME}, "bootCustomer", RequestType.POST, 404)
    time.sleep(5)


if __name__ == "__main__":
    main()
