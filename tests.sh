#!/bin/sh

LOAD_BALANCER=$1
#CUSTOMER_NAME=$(($RANDOM % 1000))
CUSTOMER_NAME=$(tr -cd "[:digit:]" < /dev/urandom | head -c 6)

for value in 1 2 3
do
  echo "Pinging /seatCustomer with valid request, should return 200..."
  response=$(curl -X POST -s -w "%{http_code}" --output /dev/null "http://$LOAD_BALANCER/RestaurantService/seatCustomer?firstName=$CUSTOMER_NAME&address=mainst&cash=1.23")
  echo $response
  if [ $response -eq 200 ]; then break; fi
  if [ $value -eq 3 ]; then exit 1; fi
done

for value in 1 2 3
do
  echo "Pinging /seatCustomer with missing param, should return 400..."
  response=$(curl -X POST -s -w "%{http_code}" --output /dev/null "http://$LOAD_BALANCER/RestaurantService/seatCustomer?firstName=$CUSTOMER_NAME&address=mainst")
  echo $response
  if [ $response -eq 400 ]; then break; fi
  if [ $value -eq 3 ]; then exit 1; fi
done

