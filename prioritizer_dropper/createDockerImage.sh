#! /bin/bash

docker build -t docker-planiot-agent .
docker tag docker-planiot-agent houssamhh/planiot-agent:latest
docker push houssamhh/planiot-agent:latest
echo "Done"