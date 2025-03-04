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


def sendRequest(endpoint, reqType, expectedCode, params=None, data=None):
    headers = {"Content-Type": "application/json"}
    for i in range(retryCount):
        logging.debug(f"Sending {reqType} request to {endpoint} with params {params}")

        if reqType == RequestType.GET:
            response = requests.get(f"http://{LOAD_BALANCER}/{SERVICE_PATH}/{endpoint}", params=params, data=data, headers=headers)
        elif reqType == RequestType.POST:
            response = requests.post(f"http://{LOAD_BALANCER}/{SERVICE_PATH}/{endpoint}", params=params, data=data, headers=headers)
        elif reqType == RequestType.PUT:
            response = requests.put(f"http://{LOAD_BALANCER}/{SERVICE_PATH}/{endpoint}", params=params, data=data, headers=headers)
        elif reqType == RequestType.DELETE:
            response = requests.delete(f"http://{LOAD_BALANCER}/{SERVICE_PATH}/{endpoint}", params=params, data=data, headers=headers)
        else:
            raise Exception(f"Request type {reqType} not supported")

        if response.status_code == expectedCode:
            return
        elif i == 2:
            logging.debug(f"Expected response code {expectedCode}, got {response.status_code}")
            raise Exception(f"Expected response code {expectedCode}, got {response.status_code}")


def main():
    # seat customer with missing param
    sendRequest("customer", RequestType.POST, 400, data={"firstName": CUSTOMER_NAME, "address": 'someaddress'})
    # seat customer with bad param value
    sendRequest("customer", RequestType.POST, 400, data={"firstName": CUSTOMER_NAME, "address": "32someaddress", "cash": "bad-value"})
    # open tables with valid request
    sendRequest("tables/open", RequestType.GET, 200)
    # boot customer with customer not in restaurant
    sendRequest("customer", RequestType.DELETE, 404, {"firstName": CUSTOMER_NAME})


if __name__ == "__main__":
    main()
