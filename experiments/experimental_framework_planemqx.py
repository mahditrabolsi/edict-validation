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

planemqxDocker = network.addDocker(
	'broker',
	ip='10.0.0.252',
	dimage='planemqx:latest',
	dcmd="/run-all.sh",
	ports=[1883, 18083, 8883, 8083, 8084, 8780,8880,8780],
	port_bindings={1883: 1883, 18083: 18083, 8883: 8883, 8083: 8083, 8084: 8084, 8780: 8780, 8880: 8880, 8780: 8780},
)

publisherDocker = network.addDocker(
	'publisher',
	ip='10.0.0.251',
	dimage="mqtt-publishers:latest",
	ports=[1883],
	ports_binding={1883: 1883},
	environment={"url": "tcp://10.0.0.252:1883", "topic": "my-custom-topic", "count": "50", "interval": "1", "size": "50000"}
)

subscriberDocker = network.addDocker(
	'subscriber',
	ip='10.0.0.253',
	dimage="mqtt-subscribers:latest",
	ports=[1883],
	ports_binding={1883: 1883},
	environment={"url": "tcp://10.0.0.252:1883", "topic": "my-custom-topic", "count": "50"}
)


info('*** Adding switches\n')
publisherSwitch = network.addSwitch('s1')
planemqxSwitch = network.addSwitch('s2')
subscriberSwitch = network.addSwitch('s3')

info('*** Creating links\n')
network.addLink(publisherDocker, publisherSwitch)
network.addLink(publisherSwitch, planemqxSwitch)
network.addLink(planemqxDocker, planemqxSwitch)
network.addLink(subscriberDocker, subscriberSwitch)
network.addLink(planemqxSwitch, subscriberSwitch, cls=TCLink, bw=8)		#Change bandwidth here (in Mbps)

info('*** Starting network\n')
network.start()
network.ping([publisherDocker, planemqxDocker])
network.ping([planemqxDocker, subscriberDocker])
network.ping([publisherDocker, subscriberDocker])

info('*** Setting up experiment')
time.sleep(5)
info('*** Running CLI\n')
CLI(network)
info('*** Stopping network')
network.stop()
