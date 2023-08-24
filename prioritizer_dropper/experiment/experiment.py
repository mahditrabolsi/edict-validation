#!/usr/bin/python   
     
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
import time


class SingleSwitchTopo(Topo):
    "Single switch connected to n hosts."
    def build(self, n=2):
        switch = self.addSwitch('s1')
    # Python's range(N) generates 0..N-1
        for h in range(n):
            host = self.addHost('h%s' % (h + 1), ip='10.0.0.' + str(h+1))
            self.addLink(host, switch)

def simpleTest():
    "Create and test a simple network"
    n = 3
    topo = SingleSwitchTopo(n)
    net = Mininet(topo)
	
    # Configure nodes    
    h1 = net.get('h1')
    h1.cmd("./application/broker/emqx/bin/emqx start > ./test/emqx.log&")


    addr = 'tcp://10.0.0.1:1883'

    #h2 = net.get('h2')
    #h2.cmd("java -jar ./application/server/server.jar > ./test/server.log")
    
    #sleep
    time.sleep(1)

    
    h2 = net.get('h2')
    h2.cmd("java -jar ./application/subscriber/subscriber.jar " + addr + " > ./test/subscriber.log&")
    
    h3 = net.get('h3')
    h3.cmd("java -jar ./application/publisher/publisher.jar " + addr + " > ./test/publisher.log&")
    
    # SSH Configration
    for i in range(1, n+1):
        hi = net['h' + str(i)]
        hi.cmd('/usr/sbin/sshd')
    
    # Start network
    net.start()
    
    # Run
    print( "Dumping host connections" )
    dumpNodeConnections(net.hosts)
    print( "Testing network connectivity" )
    net.pingAll()
    
    #time.sleep(1)
    # Stop network
    #net.stop()

if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel('info')
    simpleTest()
