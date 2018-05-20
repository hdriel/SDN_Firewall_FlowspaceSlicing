from pox.core import core
from pox.lib.util import dpidToStr
from pox.openflow import *
from pox.lib.addresses import IPAddr, EthAddr
from pox.lib.packet import *
import pox.openflow.libopenflow_01 as of
import pox.lib.packet as pkt
from pox.lib.util import str_to_bool
import time
import csv
import json


#############################################################################

VIDEO_PORT = 10000
h1_mac = "00:00:00:00:00:01"
h2_mac = "00:00:00:00:00:02"
h3_mac = "00:00:00:00:00:03"
h4_mac = "00:00:00:00:00:04"
hosts_mac = [h1_mac, h2_mac, h3_mac, h4_mac]

s1_dpid = "1"
s2_dpid = "2"
s3_dpid = "3"
s4_dpid = "4"
switch_dpid = [s1_dpid ,s2_dpid, s3_dpid, s4_dpid]

hosts_mac_from_ip = { 
  "10.0.0.1" : h1_mac,
  "10.0.0.2" : h2_mac,
  "10.0.0.3" : h3_mac,
  "10.0.0.4" : h4_mac,
  }

## {
##   (s1_dpid, h1_mac, h2_mac, Video_Packet): in switch dpid send to Port from h1 to h1,
##   ... 
## }
switch_ports = {
  # switch s1 routing
  (s1_dpid, h1_mac, h2_mac, False): 4, 
  (s1_dpid, h1_mac, h3_mac, False): 1,
  (s1_dpid, h1_mac, h4_mac, False): 1,
  (s1_dpid, h1_mac, h2_mac, True ): 4,
  (s1_dpid, h1_mac, h3_mac, True ): 2,
  (s1_dpid, h1_mac, h4_mac, True ): 2,

  (s1_dpid, h2_mac, h1_mac, False): 3, 
  (s1_dpid, h2_mac, h3_mac, False): 1,
  (s1_dpid, h2_mac, h4_mac, False): 1,
  (s1_dpid, h2_mac, h1_mac, True ): 3,
  (s1_dpid, h2_mac, h3_mac, True ): 2,
  (s1_dpid, h2_mac, h4_mac, True ): 2,

  (s1_dpid, h3_mac, h1_mac, False): 3, 
  (s1_dpid, h3_mac, h2_mac, False): 4,
  (s1_dpid, h3_mac, h4_mac, False): 1,
  (s1_dpid, h3_mac, h1_mac, True ): 3,
  (s1_dpid, h3_mac, h2_mac, True ): 4,
  (s1_dpid, h3_mac, h4_mac, True ): 2,

  (s1_dpid, h4_mac, h1_mac, False): 3, 
  (s1_dpid, h4_mac, h2_mac, False): 4,
  (s1_dpid, h4_mac, h3_mac, False): 1,
  (s1_dpid, h4_mac, h1_mac, True ): 3,
  (s1_dpid, h4_mac, h2_mac, True ): 4,
  (s1_dpid, h4_mac, h3_mac, True ): 2,

  # switch s2 routing
  (s2_dpid, h1_mac, h2_mac, False): 1, 
  (s2_dpid, h1_mac, h3_mac, False): 2,
  (s2_dpid, h1_mac, h4_mac, False): 2,
  (s2_dpid, h1_mac, h2_mac, True ): 1,
  (s2_dpid, h1_mac, h3_mac, True ): 2,
  (s2_dpid, h1_mac, h4_mac, True ): 2,

  (s2_dpid, h2_mac, h1_mac, False): 1, 
  (s2_dpid, h2_mac, h3_mac, False): 2,
  (s2_dpid, h2_mac, h4_mac, False): 2,
  (s2_dpid, h2_mac, h1_mac, True ): 1,
  (s2_dpid, h2_mac, h3_mac, True ): 2,
  (s2_dpid, h2_mac, h4_mac, True ): 2,

  (s2_dpid, h3_mac, h1_mac, False): 1, 
  (s2_dpid, h3_mac, h2_mac, False): 1,
  (s2_dpid, h3_mac, h4_mac, False): 2,
  (s2_dpid, h3_mac, h1_mac, True ): 1,
  (s2_dpid, h3_mac, h2_mac, True ): 1,
  (s2_dpid, h3_mac, h4_mac, True ): 2,

  (s2_dpid, h4_mac, h1_mac, False): 1, 
  (s2_dpid, h4_mac, h2_mac, False): 1,
  (s2_dpid, h4_mac, h3_mac, False): 2,
  (s2_dpid, h4_mac, h1_mac, True ): 1,
  (s2_dpid, h4_mac, h2_mac, True ): 1,
  (s2_dpid, h4_mac, h3_mac, True ): 2,
  
  # switch s3 routing
  (s3_dpid, h1_mac, h2_mac, False): 1, 
  (s3_dpid, h1_mac, h3_mac, False): 2,
  (s3_dpid, h1_mac, h4_mac, False): 2,
  (s3_dpid, h1_mac, h2_mac, True ): 1,
  (s3_dpid, h1_mac, h3_mac, True ): 2,
  (s3_dpid, h1_mac, h4_mac, True ): 2,

  (s3_dpid, h2_mac, h1_mac, False): 1, 
  (s3_dpid, h2_mac, h3_mac, False): 2,
  (s3_dpid, h2_mac, h4_mac, False): 2,
  (s3_dpid, h2_mac, h1_mac, True ): 1,
  (s3_dpid, h2_mac, h3_mac, True ): 2,
  (s3_dpid, h2_mac, h4_mac, True ): 2,

  (s3_dpid, h3_mac, h1_mac, False): 1, 
  (s3_dpid, h3_mac, h2_mac, False): 1,
  (s3_dpid, h3_mac, h4_mac, False): 2,
  (s3_dpid, h3_mac, h1_mac, True ): 1,
  (s3_dpid, h3_mac, h2_mac, True ): 1,
  (s3_dpid, h3_mac, h4_mac, True ): 2,

  (s3_dpid, h4_mac, h1_mac, False): 1, 
  (s3_dpid, h4_mac, h2_mac, False): 1,
  (s3_dpid, h4_mac, h3_mac, False): 2,
  (s3_dpid, h4_mac, h1_mac, True ): 1,
  (s3_dpid, h4_mac, h2_mac, True ): 1,
  (s3_dpid, h4_mac, h3_mac, True ): 2,
   
  # switch s4 routing
  (s4_dpid, h1_mac, h2_mac, False): 1, 
  (s4_dpid, h1_mac, h3_mac, False): 3,
  (s4_dpid, h1_mac, h4_mac, False): 4,
  (s4_dpid, h1_mac, h2_mac, True ): 2,
  (s4_dpid, h1_mac, h3_mac, True ): 3,
  (s4_dpid, h1_mac, h4_mac, True ): 4,

  (s4_dpid, h2_mac, h1_mac, False): 1, 
  (s4_dpid, h2_mac, h3_mac, False): 3,
  (s4_dpid, h2_mac, h4_mac, False): 4,
  (s4_dpid, h2_mac, h1_mac, True ): 2,
  (s4_dpid, h2_mac, h3_mac, True ): 3,
  (s4_dpid, h2_mac, h4_mac, True ): 4,

  (s4_dpid, h3_mac, h1_mac, False): 1, 
  (s4_dpid, h3_mac, h2_mac, False): 1,
  (s4_dpid, h3_mac, h4_mac, False): 4,
  (s4_dpid, h3_mac, h1_mac, True ): 2,
  (s4_dpid, h3_mac, h2_mac, True ): 2,
  (s4_dpid, h3_mac, h4_mac, True ): 4,

  (s4_dpid, h4_mac, h1_mac, False): 1, 
  (s4_dpid, h4_mac, h2_mac, False): 1,
  (s4_dpid, h4_mac, h3_mac, False): 3,
  (s4_dpid, h4_mac, h1_mac, True ): 2,
  (s4_dpid, h4_mac, h2_mac, True ): 2,
  (s4_dpid, h4_mac, h3_mac, True ): 3,
}
###########################################
## Topology Assigment 1                  ##
##                                       ##
## +----+        +----+         +----+   ##
## | h1 |        | s2 |         | h3 |   ##
## +----+       1+----+2        +----+   ##
##       \      /      \       /         ##
##       3+----+1  Non  1+----+3         ##
##        | s1 |  -----  | s1 |          ##
##       4+----+2  Vid  2+----+4         ##
##       /      \ P10K /       \         ##
## +----+       1+----+2        +----+   ##
## | h2 |        | s3 |         | h4 |   ##
## +----+        +----+         +----+   ##
###########################################

#############################################################################


address_mac = {}
#print "Init dictionery firewall"
with open('firewall-policies.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    #print "open file firewall-policies.csv"
    for row in reader:
        address_mac[row['id']] = (row['mac_0'], row['mac_1'])
        #print "add row: ", dict_mac[row['id']] 
        # dict_mac = {
        #    ( '1' : ('00:00:00:00:01' , '00:00:00:00:02') )
        # }

print "Firewall dictionary: "
print json.dumps(address_mac, indent = 1)

# START Assigment 1.a firewall-policies
def blocked_by_firewall(packet):
  for _,v in address_mac.items():
    if (str(packet.src), str(packet.dst)) == v or (str(packet.dst), str(packet.src)) == v:
      #print "",packet.dst," << Blocked By Firewall >> ",packet.src," !"
      return True
  return False
## End blocked_by_firewall method


macToPort = {}
def switch_routing(event, dst_mac):
  """ for now it like hub send packet to all links"""
  packet = event.parsed
  s_dpid = str(event.dpid)
  hi = str(packet.src)
  if dst_mac is None: hj = str(packet.dst)
  else:               hj = dst_mac
  
  ## START Assigment 1.b routing videos in the down slice
  vid = False
  tcp_packet = packet.find('tcp')
  if tcp_packet is not None: 
    vid = tcp_packet.dstport == VIDEO_PORT #or tcp_packet.srcport == VIDEO_PORT
  
  if (s_dpid, hi, hj, vid) in switch_ports:
    ## Routing between switches
    out_port = switch_ports[(s_dpid, hi, hj, vid)]
    if vid : pri_vid = "Videos"
    else   : pri_vid = "NonVid"
    #print "( s",s_dpid,", from: " ,hi,", to: " , hj,", type: " ,pri_vid , ") >> out to port >> " , out_port 

    msg = of.ofp_flow_mod()
    msg.match = of.ofp_match.from_packet(packet, event.port)
    msg.idle_timeout = 10
    msg.hard_timeout = 30
    msg.actions.append(of.ofp_action_output(port = out_port))
    msg.data = event.ofp
    event.connection.send(msg)
    
  else:
    # Sending by FLOOD method - for every one  
    msg = of.ofp_packet_out()
    msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
    msg.data = event.ofp
    msg.in_port = event.port
    event.connection.send(msg)


def drop (event, duration = None):
    """
    Drops this packet and optionally installs a flow 
    to continue dropping similar ones for a while
    """
    packet = event.parsed
    msg = of.ofp_flow_mod()
    msg.match = of.ofp_match.from_packet(packet)
    msg.idle_timeout = 0
    msg.hard_timeout = 1
    msg.buffer_id = event.ofp.buffer_id
    event.connection.send(msg)  


# handle ARP request and respond
def _arp(event):
  packet     = event.parsed
  arp_packet = packet.find('arp')  

  if arp_packet is not None:
    if arp_packet.opcode == arp.REQUEST:

      ip_src = str(arp_packet.protosrc)
      ip_dst = str(arp_packet.protodst)
      hi = hosts_mac_from_ip[ip_src]
      hj = hosts_mac_from_ip[ip_dst]

      #create arp packet
      a           = arp()
      a.opcode    = arp.REPLY
 
      #if request from h_i, fake reply from h_j
      #a           = create_arp_address(False ,arp_packet, a) 
      if arp_packet.hwsrc == EthAddr(hi): 
        a.hwsrc = EthAddr(hi)
        a.hwdst = EthAddr(hj) 
      elif arp_packet.hwsrc == EthAddr(hj):
        a.hwsrc = EthAddr(hi)
        a.hwdst = EthAddr(hj)

      #fake reply IP
      a.protosrc  = arp_packet.protodst
      a.protodst  = arp_packet.protosrc
      a.hwlen     = 6
      a.protolen  = 4
      a.hwtype    = arp.HW_TYPE_ETHERNET
      a.prototype = arp.PROTO_TYPE_IP            

      #create ethernet packet
      e = ethernet()
      e.set_payload(a)
      
      #e           = create_arp_address(True ,arp_packet, e)
      if arp_packet.hwsrc == EthAddr(hi): 
        e.src = EthAddr(hi)
        e.dst = EthAddr(hj) 
      elif arp_packet.hwsrc == EthAddr(hj):
        e.src = EthAddr(hi)
        e.dst = EthAddr(hj) 
  
      e.type      = ethernet.ARP_TYPE

      msg         = of.ofp_packet_out()
      msg.data    = e.pack()
          
      #send the packet back to the source
      msg.actions.append( of.ofp_action_output( port = event.port ) )
      event.connection.send( msg )
      
      return hosts_mac_from_ip[str(arp_packet.protodst)]




#############################################################################

def _handle_ConnectionUp (event):
  """ fire When the switches connect to the controller first time! """
  print "ConnectionUp event fired - init setup switch s", event.dpid, " !"
  ## create flow match rule   
  for k,port_out in switch_ports.items(): 
    s_dpid, h1, h2 , vid = k
    #for each packet from h1 to h2 in switch s forward via port p
    if (s_dpid == dpidToStr(event.dpid)):
      match = of.ofp_match()
      match.dl_src = EthAddr(h1)
      match.dl_dst = EthAddr(h2)

      fm = of.ofp_flow_mod()
      fm.match = match
      fm.hard_timeout = 300
      fm.idle_timeout = 100
      fm.actions.append(of.ofp_action_output(port=port_out))

      event.connection.send(fm)
    
def _handle_PacketIn(event):
  """fire each time host send a packet (ping) to another host... """
  dst_mac = _arp(event)
  packet = event.parsed
  
  ## Check if block the session between the hosts - Assignment 1
  if blocked_by_firewall(packet):
    return 
    #drop(event)
  else: 
    switch_routing(event, dst_mac)

#############################################################################
def launch ():
  core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
  core.openflow.addListenerByName("PacketIn"    , _handle_PacketIn)
  print "Custom Controller running."



    
    
    


    
