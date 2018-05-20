#!/usr/bin/python
 
from mininet.net import Mininet
from mininet.node import Controller, RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink
from mininet.topo import Topo


def int2dpid( dpid ):
   try:
      dpid = hex( dpid )[ 2: ]
      dpid = '0' * ( 16 - len( dpid ) ) + dpid
      return dpid
   except IndexError:
      raise Exception( 'Unable to derive default datapath ID - '
                       'please either specify a dpid or use a '
		       'canonical switch name such as s23.' )

setLogLevel( 'info' )
info( '*** Init mininet Network\n' )
print '##########################################'
print '## Topology Assigment 1                 ##'
print '##                                      ##'
print '## +----+        +----+        +----+   ##'
print '## | h1 |        | s2 |        | h3 |   ##'
print '## +----+       1+----+2       +----+   ##'
print '##       \      /      \      /         ##'
print '##       3+----+1      1+----+3         ##'
print '##        | s1 |        | s1 |          ##'
print '##       4+----+2      2+----+4         ##'
print '##       /      \      /      \         ##'
print '## +----+       1+----+2       +----+   ##'
print '## | h2 |        | s3 |        | h4 |   ##'
print '## +----+        +----+        +----+   ##'
print '##########################################'

class AssingmentTopology(Topo):
   def __init__(self):
     Topo.__init__(self)
     
   def build(self):
     "Create a simulated network"
     #info( '*** Adding hosts\n' )
     h1 = self.addHost('h1', ip='10.0.0.1', mac='00:00:00:00:00:01')
     h2 = self.addHost('h2', ip='10.0.0.2', mac='00:00:00:00:00:02')
     h3 = self.addHost('h3', ip='10.0.0.3', mac='00:00:00:00:00:03')
     h4 = self.addHost('h4', ip='10.0.0.4', mac='00:00:00:00:00:04')

     #info( '*** Adding switches\n' )
##     s1 = self.addSwitch( 's1', dpid=int2dpid(1) )
##     s2 = self.addSwitch( 's2', dpid=int2dpid(2) )
##     s3 = self.addSwitch( 's3', dpid=int2dpid(3) )
##     s4 = self.addSwitch( 's4', dpid=int2dpid(4) )
     s1 = self.addSwitch( 's1', dpid='1' )
     s2 = self.addSwitch( 's2', dpid='2' )
     s3 = self.addSwitch( 's3', dpid='3' )
     s4 = self.addSwitch( 's4', dpid='4' )
   
     #info( '*** Creating links\n' )
     self.addLink(h1, s1,          port2=3       )
     self.addLink(h2, s1,          port2=4       )
     self.addLink(h3, s4,          port2=3       )
     self.addLink(h4, s4,          port2=4       )
     
     self.addLink(s1, s2, port1=1, port2=1, bw=1 )
     self.addLink(s2, s4, port1=2, port2=1, bw=1 )
     self.addLink(s1, s3, port1=2, port2=1, bw=10)
     self.addLink(s3, s4, port1=2, port2=2, bw=10)


topo = AssingmentTopology()
net = Mininet(topo=topo, controller=lambda name: RemoteController(name, ip='127.0.0.1', protocol='tcp', port = 6633), link=TCLink)


info( '*** Starting network\n')
net.start()
info( '*** Running CLI\n' )
CLI( net )
info( '*** Stopping network' )
net.stop()

