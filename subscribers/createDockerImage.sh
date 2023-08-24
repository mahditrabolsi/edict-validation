#! /bin/bash

docker build -t docker-planiot-subscribers .
docker tag docker-planiot-subscribers houssamhh/planiot-subscribers:latest
docker push houssamhh/planiot-subscribers:latest
echo "Done"