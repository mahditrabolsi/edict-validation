#!/usr/bin/python

import time

from mininet.net import Containernet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import info, setLogLevel

setLogLevel('info')

network = Containernet(controller=Controller)

info('*** Adding controller\n')
network.addController('c0')

info('*** Adding docker containers\n')

brokerDocker = network.addDocker(
	'broker',
	ip='10.0.0.252',
	dimage='emqx-experiments:1.0.0',
	dcmd="/opt/emqx/bin/emqx foreground",
	ports=[1883, 18083, 8883, 8083, 8084, 8780],
	port_bindings={1883: 1883, 18083: 18083, 8883: 8883, 8083: 8083, 8084: 8084, 8780: 8780}
)

publisherDocker = network.addDocker(
	'publisher',
	ip='10.0.0.251',
	dimage="publishers:latest",
	#dcmd="java -jar mqtt-publisher/mqtt-publisher.jar",
	#dcmd = "java -jar ./mqtt-publisher.jar",
	ports=[1883],
	ports_binding={1883: 1883},
	environment={"url": "tcp://10.0.0.252:1883", "topic": "my-custom-topic", "count": "50", "interval": "1", "size": "50000"}
)

subscriberANDocker = network.addDocker(
	'an',
	ip='10.0.0.253',
	dimage="subscribers-an:latest",
	#dcmd="java -jar /mqtt-subscriber/mqtt-subscriber.jar",
	ports=[1883],
	ports_binding={1883: 1883},
	environment={"url": "tcp://10.0.0.252:1883", "topic": "my-custom-topic", "count": "50"}
)

subscriberRTDocker = network.addDocker(
	'rt',
	ip='10.0.1.253',
	dimage="subscribers-rt:latest",
	#dcmd="java -jar /mqtt-subscriber/mqtt-subscriber.jar",
	ports=[1883],
	ports_binding={1883: 1883},
	environment={"url": "tcp://10.0.0.252:1883", "topic": "my-custom-topic", "count": "50"}
)

subscriberTSDocker = network.addDocker(
	'ts',
	ip='10.0.2.253',
	dimage="subscribers-ts:latest",
	#dcmd="java -jar /mqtt-subscriber/mqtt-subscriber.jar",
	ports=[1883],
	ports_binding={1883: 1883},
	environment={"url": "tcp://10.0.0.252:1883", "topic": "my-custom-topic", "count": "50"}
)

subscriberVSDocker = network.addDocker(
	'vs',
	ip='10.0.3.253',
	dimage="subscribers-vs:latest",
	#dcmd="java -jar /mqtt-subscriber/mqtt-subscriber.jar",
	ports=[1883],
	ports_binding={1883: 1883},
	environment={"url": "tcp://10.0.0.252:1883", "topic": "my-custom-topic", "count": "50"}
)

apiDocker = network.addDocker(
	'api',
	ip='10.0.0.254',
	dimage="emqx-api:1.0.0",
	ports=[8780, 8080],
	ports_binding={8780: 8780, 8080: 8080}
)

agentDocker = network.addDocker(
	'agent',
	ip='10.0.0.255',
	dimage="planemqx-agent:latest",
	#dcmd="java -jar /mqtt-subscriber/mqtt-subscriber.jar",
	ports=[8880],
	ports_binding={8880: 8880}
)

info('*** Adding switches\n')
publisherSwitch = network.addSwitch('s1')
brokerSwitch = network.addSwitch('s2')
subscriberANSwitch = network.addSwitch('s3')
apiSwitch = network.addSwitch('s4')
agentSwitch = network.addSwitch('s5')
subscriberRTSwitch = network.addSwitch('s6')
subscriberTSSwitch = network.addSwitch('s7')
subscriberVSSwitch = network.addSwitch('s8')

info('*** Creating links\n')
network.addLink(publisherDocker, publisherSwitch)
network.addLink(publisherSwitch, brokerSwitch)
network.addLink(brokerDocker, brokerSwitch)
network.addLink(subscriberANDocker, subscriberANSwitch)
network.addLink(subscriberRTDocker, subscriberRTSwitch)
network.addLink(subscriberTSDocker, subscriberTSSwitch)
network.addLink(subscriberVSDocker, subscriberVSSwitch)
network.addLink(brokerSwitch, subscriberANSwitch, cls=TCLink, bw=250)
network.addLink(brokerSwitch, subscriberRTSwitch, cls=TCLink, bw=250)
network.addLink(brokerSwitch, subscriberTSSwitch, cls=TCLink, bw=250)
network.addLink(brokerSwitch, subscriberVSSwitch, cls=TCLink, bw=250)
network.addLink(brokerSwitch, apiSwitch)
network.addLink(apiDocker, apiSwitch)
network.addLink(brokerSwitch, agentSwitch)
network.addLink(agentDocker, agentSwitch)

info('*** Starting network\n')
network.start()

# info('*** Testing connectivity\n')
network.ping([publisherDocker, brokerDocker])
network.ping([brokerDocker, subscriberANDocker])
network.ping([brokerDocker, subscriberRTDocker])
network.ping([brokerDocker, subscriberTSDocker])
network.ping([brokerDocker, subscriberVSDocker])
network.ping([publisherDocker, subscriberANDocker])
network.ping([publisherDocker, subscriberRTDocker])
network.ping([publisherDocker, subscriberTSDocker])
network.ping([publisherDocker, subscriberVSDocker])
network.ping([publisherDocker, agentDocker])
network.ping([brokerDocker, agentDocker])
network.ping([subscriberANDocker, agentDocker])
network.ping([subscriberRTDocker, agentDocker])
network.ping([subscriberTSDocker, agentDocker])
network.ping([subscriberVSDocker, agentDocker])
network.ping([publisherDocker, apiDocker])
network.ping([brokerDocker, apiDocker])
network.ping([subscriberANDocker, apiDocker])
network.ping([subscriberRTDocker, apiDocker])
network.ping([subscriberTSDocker, apiDocker])
network.ping([subscriberVSDocker, apiDocker])

info('*** Setting up experiment')
apiDocker.cmd('java -jar target/planiot-0.0.1-SNAPSHOT.jar &')
time.sleep(5)
agentDocker.cmd('java -jar agent.jar &')
#subscriberDocker.cmd('xterm &')
#publisherDocker.cmd('xterm &')
info('*** Running CLI\n')
CLI(network)
#time.sleep(60)

info('*** Stopping network')
network.stop()

