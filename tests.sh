LOAD_BALANCER=$1
CUSTOMER_NAME=$(($RANDOM % 1000))

for value in {1..3}
do
  response=$(curl -X POST -s -w "%{http_code}" "http://$LOAD_BALANCER/RestaurantService/seatCustomer?firstName=$CUSTOMER_NAME&address=mainst")
  echo $response
done
