#!/bin/sh

LOAD_BALANCER=$1
#CUSTOMER_NAME=$(($RANDOM % 1000))
CUSTOMER_NAME=$(tr -cd "[:digit:]" < /dev/urandom | head -c 6)

for value in 1 2 3
do
  response=$(curl -X POST -s -w "%{http_code}" --output /dev/null "http://$LOAD_BALANCER/RestaurantService/seatCustomer?firstName=$CUSTOMER_NAME&address=mainst")
  echo $response
done
