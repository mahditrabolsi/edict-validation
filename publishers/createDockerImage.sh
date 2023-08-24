#! /bin/bash

docker build -t docker-planiot-publishers .
docker tag docker-planiot-publishers houssamhh/planiot-publishers:latest
docker push houssamhh/planiot-publishers:latest
echo "Done"