# PlanEMQX
PlanEMQX is a broker for the MQTT protocol that is based on the famous open-source broker [EMQX](https://www.emqx.io/).It allows to prioritize the messages and add dropping to the different categories of messages.
## Prerequisites
Your machine should run Ubuntu 20.04 LTS and Python 3.
You should also install [Containernet](https://containernet.github.io/), an extension of [mininet](http://mininet.org/) that allows using Docker containers as hosts in emulated network topologies.Also you should have [Docker](https://docs.docker.com/engine/install/ubuntu/) installed.

## Building the docker images
After cloning the repository, you can start by building the necessary docker images.
Run the commands from the root directory of the project.
Change `{arch}` to the architecture of your machine (amd64, arm64).

Planemqx:
```
$ docker build -f Dockerfile.{arch} -t planemqx .
```
Publishers:
```
$ docker build -t mqtt-publishers publishers/
```
Subscribers:
```
$ docker build -t mqtt-subscribers subscribers/
```

## Starting the experiment
To start the experiment, you have to run the following commands from the root directory of the project.
```
$ sudo python3 experiments/experimental_framework.py
```
This will create a network topology using mininet which includes planemqx and the hosts( publishers and subscribers).
### Running the subscribers and publishers
Subscribers:
```
$ docker exec -it mn.subscriber /bin/bash -c "java -jar subscribers.jar"
```
Publishers:
```
$ docker exec -it mn.publisher /bin/bash -c "java -jar publishers.jar"
```

Make sure to run the subscribers before the publishers so that the subscribers can subscribe to the topics before the publishers start publishing.
 
## Collecting metrics
When the experiment is done (you can see this by viewing the display of the susbcribers' container), the metrics of the response time for each message are saved in the directory `results` (in the container).

It includes the following files:
- `response_time.csv` : the response time of each message.
- `results.csv` : the average response time of each subscription.

To copy them to your local machine, run the command:

```
$ docker cp mn.subscriber:/appPlaniotSubscribers/results/ {path_to_directory_on_local_machine}
```
Where `{path_to_directory_on_local_machine}` is the path to the directory where you want to copy the results on your local machine.


## Configurations
You can add update the dropping of the categories of messages in the file `prioritizer_dropper\data\AIPlanner.txt` by changing `0 : DROPPING_VS2_RT0_TS0_AN5` to your desired dropping.Each category have its own dropping.For example here `VS` has a dropping of 2%, `RT` has a dropping of 0%, `TS` has a dropping of 0% and `AN` has a dropping of 5%.
You can change which scenario to use by changing the value of `scenario` in the files `prioritizer_dropper\config\config.properties`, `publishers\config\config.properties` and `publishers\config\config.properties` to the desired scenario.

Other Configuration related to the broker can be changed in the emqx dashboard (http://localhost:18083/).
Also 
