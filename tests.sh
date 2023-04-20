#!/bin/sh

LOAD_BALANCER=$1
#CUSTOMER_NAME=$(($RANDOM % 1000))
CUSTOMER_NAME=$(tr -cd "[:digit:]" < /dev/urandom | head -c 6)

SEAT_CUSTOMER_VALID_FAILS=0
for value in 1 2 3
do
  TEST_VAL=$((TEST_VAL+1))
  echo "Pinging /seatCustomer with valid request, should return 200..."
  response=$(curl -X POST -s -w "%{http_code}" --output /dev/null "http://$LOAD_BALANCER/RestaurantService/seatCustomer?firstName=$CUSTOMER_NAME&address=mainst&cash=1.23")
  echo $response
  if [ $response -eq 200 ]; then break; else SEAT_CUSTOMER_VALID_FAILS=$((SEAT_CUSTOMER_VALID_FAILS+1)); fi
  if [ $value -eq 3 ]; then exit 1; fi
done
echo "failures: $SEAT_CUSTOMER_VALID_FAILS out of 3 attempts\n"

SEAT_CUSTOMER_MISSING_PARAM_FAILS=0
for value in 1 2 3
do
  echo "Pinging /seatCustomer with missing param, should return 400..."
  response=$(curl -X POST -s -w "%{http_code}" --output /dev/null "http://$LOAD_BALANCER/RestaurantService/seatCustomer?firstName=$CUSTOMER_NAME&address=mainst")
  echo $response
  if [ $response -eq 400 ]; then break; else SEAT_CUSTOMER_MISSING_PARAM_FAILS=$((SEAT_CUSTOMER_MISSING_PARAM_FAILS+1)); fi
  if [ $value -eq 3 ]; then exit 1; fi
done
echo "failures: $SEAT_CUSTOMER_MISSING_PARAM_FAILS out of 3 attempts\n"

SEAT_CUSTOMER_INVALID_PARAM_FAILS=0
for value in 1 2 3
do
  echo "Pinging /seatCustomer with invalid param, should return 400..."
  response=$(curl -X POST -s -w "%{http_code}" --output /dev/null "http://$LOAD_BALANCER/RestaurantService/seatCustomer?firstName=$CUSTOMER_NAME&address=mainst&cash=bad-value")
  echo $response
  if [ $response -eq 400 ]; then break; else SEAT_CUSTOMER_INVALID_PARAM_FAILS=$((SEAT_CUSTOMER_INVALID_PARAM_FAILS+1)); fi
  if [ $value -eq 3 ]; then exit 1; fi
done
echo "failures: $SEAT_CUSTOMER_INVALID_PARAM_FAILS out of 3 attempts\n"


GET_OPEN_TABLES_FAILS=0
for value in 1 2 3
do
  echo "Pinging /getOpenTables..."
  response=$(curl -s -w "%{http_code}" --output /dev/null "http://$LOAD_BALANCER/RestaurantService/getOpenTables")
  echo $response
  if [ $response -eq 200 ]; then break; else GET_OPEN_TABLES_FAILS=$((GET_OPEN_TABLES_FAILS+1)); fi
  if [ $value -eq 3 ]; then exit 1; fi
done
echo "failures: $GET_OPEN_TABLES_FAILS out of 3 attempts\n"


SUBMIT_ORDER_FAILS=0
for value in 1 2 3
do
  echo "Pinging /submitOrder with valid request, should return 200..."
  response=$(curl -X POST -s -w "%{http_code}" --output /dev/null "http://$LOAD_BALANCER/RestaurantService/submitOrder?firstName=$CUSTOMER_NAME&tableNumber=5&dish=burg&bill=1.00")
  echo $response
  if [ $response -eq 200 ]; then break; else SUBMIT_ORDER_FAILS=$((SUBMIT_ORDER_FAILS+1)); fi
  if [ $value -eq 3 ]; then exit 1; fi
done
echo "failures: $SUBMIT_ORDER_FAILS out of 3 attempts\n"

SUBMIT_ORDER_INSUFFICIENT_FUNDS_FAILS=0
for value in 1 2 3
do
  echo "Pinging /submitOrder with insufficient funds, should return 500..."
  response=$(curl -X POST -s -w "%{http_code}" --output /dev/null "http://$LOAD_BALANCER/RestaurantService/submitOrder?firstName=$CUSTOMER_NAME&tableNumber=5&dish=burg&bill=100.00")
  echo $response
  if [ $response -eq 500 ]; then break; else SUBMIT_ORDER_INSUFFICIENT_FUNDS_FAILS=$((SUBMIT_ORDER_INSUFFICIENT_FUNDS_FAILS+1)); fi
  if [ $value -eq 3 ]; then exit 1; fi
done
echo "failures: $SUBMIT_ORDER_INSUFFICIENT_FUNDS_FAILS out of 3 attempts\n"

SUBMIT_ORDER_MISSING_PARAM_FAILS=0
for value in 1 2 3
do
  echo "Pinging /submitOrder with missing param, should return 400..."
  response=$(curl -X POST -s -w "%{http_code}" --output /dev/null "http://$LOAD_BALANCER/RestaurantService/submitOrder?firstName=$CUSTOMER_NAME&tableNumber=5&dish=burg")
  echo $response
  if [ $response -eq 400 ]; then break; else SUBMIT_ORDER_MISSING_PARAM_FAILS=$((SUBMIT_ORDER_MISSING_PARAM_FAILS+1)); fi
  if [ $value -eq 3 ]; then exit 1; fi
done
echo "failures: $SUBMIT_ORDER_MISSING_PARAM_FAILS out of 3 attempts\n"

SUBMIT_ORDER_BAD_PARAM_FAILS=0
for value in 1 2 3
do
  echo "Pinging /submitOrder with bad param, should return 400..."
  response=$(curl -X POST -s -w "%{http_code}" --output /dev/null "http://$LOAD_BALANCER/RestaurantService/submitOrder?firstName=$CUSTOMER_NAME&tableNumber=5&dish=burg&bill=bad-param")
  echo $response
  if [ $response -eq 400 ]; then break; else SUBMIT_ORDER_BAD_PARAM_FAILS=$((SUBMIT_ORDER_BAD_PARAM_FAILS+1)); fi
  if [ $value -eq 3 ]; then exit 1; fi
done
echo "failures: $SUBMIT_ORDER_BAD_PARAM_FAILS out of 3 attempts\n"