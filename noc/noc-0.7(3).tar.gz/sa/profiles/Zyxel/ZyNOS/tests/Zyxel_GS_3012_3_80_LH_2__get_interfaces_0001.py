# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Zyxel.ZyNOS.get_interfaces test
## Auto-generated by ./noc debug-script at 2011-10-18 13:11:30
##----------------------------------------------------------------------
## Copyright (C) 2007-2011 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

## NOC modules
from noc.lib.test import ScriptTestCase


class Zyxel_ZyNOS_get_interfaces_Test(ScriptTestCase):
    script = "Zyxel.ZyNOS.get_interfaces"
    vendor = "Zyxel"
    platform = 'GS-3012'
    version = '3.80(LH.2)'
    input = {}
    result = [{'forwarding_instance': 'default',
  'interfaces': [{'admin_status': True,
                  'mac': '00:A0:C5:D7:F9:C5',
                  'name': '1',
                  'oper_status': True,
                  'subinterfaces': [{'admin_status': True,
                                     'is_bridge': True,
                                     'name': '1',
                                     'oper_status': True,
                                     'untagged_vlan': 15}],
                  'type': 'physical'},
                 {'admin_status': True,
                  'mac': '00:A0:C5:D7:F9:C5',
                  'name': '2',
                  'oper_status': True,
                  'subinterfaces': [{'admin_status': True,
                                     'is_bridge': True,
                                     'name': '2',
                                     'oper_status': True,
                                     'tagged_vlans': [15,
                                                      20,
                                                      53,
                                                      56,
                                                      58,
                                                      60,
                                                      63,
                                                      68,
                                                      70,
                                                      95,
                                                      119,
                                                      138,
                                                      140,
                                                      142,
                                                      143]}],
                  'type': 'physical'},
                 {'admin_status': True,
                  'mac': '00:A0:C5:D7:F9:C5',
                  'name': '3',
                  'oper_status': True,
                  'subinterfaces': [{'admin_status': True,
                                     'is_bridge': True,
                                     'name': '3',
                                     'oper_status': True,
                                     'untagged_vlan': 15}],
                  'type': 'physical'},
                 {'admin_status': True,
                  'mac': '00:A0:C5:D7:F9:C5',
                  'name': '4',
                  'oper_status': True,
                  'subinterfaces': [{'admin_status': True,
                                     'is_bridge': True,
                                     'name': '4',
                                     'oper_status': True,
                                     'untagged_vlan': 15}],
                  'type': 'physical'},
                 {'admin_status': True,
                  'mac': '00:A0:C5:D7:F9:C5',
                  'name': '5',
                  'oper_status': True,
                  'subinterfaces': [{'admin_status': True,
                                     'is_bridge': True,
                                     'name': '5',
                                     'oper_status': True,
                                     'untagged_vlan': 15}],
                  'type': 'physical'},
                 {'admin_status': True,
                  'mac': '00:A0:C5:D7:F9:C5',
                  'name': '6',
                  'oper_status': True,
                  'subinterfaces': [{'admin_status': True,
                                     'is_bridge': True,
                                     'name': '6',
                                     'oper_status': True,
                                     'untagged_vlan': 15}],
                  'type': 'physical'},
                 {'admin_status': True,
                  'mac': '00:A0:C5:D7:F9:C5',
                  'name': '7',
                  'oper_status': False,
                  'subinterfaces': [{'admin_status': True,
                                     'is_bridge': True,
                                     'name': '7',
                                     'oper_status': False,
                                     'untagged_vlan': 15}],
                  'type': 'physical'},
                 {'admin_status': True,
                  'mac': '00:A0:C5:D7:F9:C5',
                  'name': '8',
                  'oper_status': True,
                  'subinterfaces': [{'admin_status': True,
                                     'is_bridge': True,
                                     'name': '8',
                                     'oper_status': True,
                                     'tagged_vlans': [15,
                                                      20,
                                                      53,
                                                      56,
                                                      58,
                                                      60,
                                                      68,
                                                      70,
                                                      95]}],
                  'type': 'physical'},
                 {'admin_status': True,
                  'mac': '00:A0:C5:D7:F9:C5',
                  'name': '9',
                  'oper_status': False,
                  'subinterfaces': [{'admin_status': True,
                                     'is_bridge': True,
                                     'name': '9',
                                     'oper_status': False,
                                     'tagged_vlans': [95]}],
                  'type': 'physical'},
                 {'admin_status': True,
                  'mac': '00:A0:C5:D7:F9:C5',
                  'name': '10',
                  'oper_status': False,
                  'subinterfaces': [{'admin_status': True,
                                     'is_bridge': True,
                                     'name': '10',
                                     'oper_status': False,
                                     'tagged_vlans': [95]}],
                  'type': 'physical'},
                 {'admin_status': True,
                  'mac': '00:A0:C5:D7:F9:C5',
                  'name': '11',
                  'oper_status': True,
                  'subinterfaces': [{'admin_status': True,
                                     'is_bridge': True,
                                     'name': '11',
                                     'oper_status': True,
                                     'tagged_vlans': [15,
                                                      18,
                                                      63,
                                                      95,
                                                      180,
                                                      800]}],
                  'type': 'physical'},
                 {'admin_status': True,
                  'mac': '00:A0:C5:D7:F9:C5',
                  'name': '12',
                  'oper_status': True,
                  'subinterfaces': [{'admin_status': True,
                                     'is_bridge': True,
                                     'name': '12',
                                     'oper_status': True,
                                     'tagged_vlans': [15,
                                                      18,
                                                      20,
                                                      53,
                                                      56,
                                                      58,
                                                      60,
                                                      63,
                                                      68,
                                                      70,
                                                      95,
                                                      102,
                                                      119,
                                                      138,
                                                      140,
                                                      142,
                                                      143,
                                                      149,
                                                      180,
                                                      800]}],
                  'type': 'physical'},
                 {'admin_status': True,
                  'description': 'Outband management',
                  'mac': '00:A0:C5:D7:F9:C5',
                  'name': 'Mgmt',
                  'oper_status': True,
                  'subinterfaces': [{'admin_status': True,
                                     'ipv4_adresses': ['172.16.16.222/24'],
                                     'is_ipv4': True,
                                     'name': 'Mgmt',
                                     'oper_status': True,
                                     'vlan_ids': []}],
                  'type': 'SVI'},
                 {'admin_status': True,
                  'description': 'vlan95',
                  'mac': '00:A0:C5:D7:F9:C5',
                  'name': 'vlan95',
                  'oper_status': True,
                  'subinterfaces': [{'admin_status': True,
                                     'ipv4_adresses': ['10.8.5.131/26'],
                                     'is_ipv4': True,
                                     'name': 'vlan95',
                                     'oper_status': True,
                                     'vlan_ids': [95]}],
                  'type': 'SVI'}],
  'type': 'ip'}]
    motd = ' ****\nCopyright (c) 1994 - 2008 ZyXEL Communications Corp.\n'
    cli = {
'show vlan-stacking':  ' show vlan-stacking\n  %Invalid command "vlan-stacking"\n', 
## 'show interface config 11'
'show interface config 11': """ show interface config 11
  Port Configurations:
  
  
  Port No \t:11
    Active \t:Yes
    Name  \t:
    PVID \t:1\t\tFlow Control \t:No
    Type \t:10/100/1000M\tSpeed/Duplex \t:auto
    BPDU \t:peer\t\t802.1p Priority :0
  """, 
## 'show trunk'
'show trunk': """ show trunk
Group ID 1:\tinactive 
  Status: -
  Member number: 0\t
Group ID 2:\tinactive 
  Status: -
  Member number: 0\t
Group ID 3:\tinactive 
  Status: -
  Member number: 0\t
Group ID 4:\tinactive 
  Status: -
  Member number: 0\t
Group ID 5:\tinactive 
  Status: -
  Member number: 0\t
Group ID 6:\tinactive 
  Status: -
  Member number: 0\t""", 
'show router rip':  ' show router rip\n  %Invalid command "router"\n', 
## 'show interface config 9'
'show interface config 9': """ show interface config 9
  Port Configurations:
  
  
  Port No \t:9
    Active \t:Yes
    Name  \t:
    PVID \t:1\t\tFlow Control \t:No
    Type \t:10/100/1000M\tSpeed/Duplex \t:auto
    BPDU \t:peer\t\t802.1p Priority :0
  """, 
## 'show vlan'
'show vlan': """ show vlan
  The Number of VLAN :    26
  Idx.  VID   Status     Elap-Time    TagCtl                                 
  ----  ----  ---------  -----------  ---------------------------------------
  
     1     1     Static    554:05:45  Untagged :
                                      Tagged   :
  
     2    15     Static    554:05:45  Untagged :1,3-7
                                      Tagged   :2,8,11-12
  
     3    18     Static    554:05:45  Untagged :
                                      Tagged   :11-12
  
     4    20     Static    311:47:02  Untagged :
                                      Tagged   :2,8,12
  
     5    53     Static    554:05:45  Untagged :
                                      Tagged   :2,8,12
  
     6    56     Static    554:05:45  Untagged :
                                      Tagged   :2,8,12
  
     7    58     Static    361:43:40  Untagged :
                                     Tagged   :2,8,12
  
     8    60     Static    524:05:34  Untagged :
                                      Tagged   :2,8,12
  
     9    63     Static    554:05:45  Untagged :
                                      Tagged   :2,11-12
  
    10    68     Static    554:05:45  Untagged :
                                      Tagged   :2,8,12
  
    11    70     Static    554:05:45  Untagged :
                                      Tagged   :2,8,12
  
   12   95     Static    554:05:45  Untagged :
                                      Tagged   :2,8-12
  
    13   102     Static    554:05:45  Untagged :
                                      Tagged   :12
  
    14   119     Static    554:05:45  Untagged :
                                      Tagged   :2,12
  
    15   138     Static    554:05:45  Untagged :
                                      Tagged   :2,12
  
    16   140     Static    554:05:45  Untagged :
                                      Tagged   :2,12
  
    27   142     Static    554:05:45  Untagged :
                                      Tagged   :2,12
  
    28   143     Static    554:05:45  Untagged :
                                      Tagged   :2,12
  
    19   149     Static    554:05:45  Untagged :
                                      Tagged   :12
 
    20   150     Static    554:05:45  Untagged :
                                      Tagged   :
  
    21   180     Static    554:05:45  Untagged :
                                      Tagged   :11-12
  
    22   777     Static    554:05:45  Untagged :
                                      Tagged   :
  
    23   800     Static    554:05:45  Untagged :
                                      Tagged   :11-12""", 
## 'show system-information'
'show system-information': """ show system-information

System Name\t\t: GS-3012
System Contact\t\t: 
System Location\t\t: 
Ethernet Address\t: 00:a0:c5:d7:f9:c5
ZyNOS F/W Version\t: V3.80(LH.2) | 03/04/2008
RomRasSize\t\t: 3234948 
System up Time\t\t:   554:06:06 (be3c5bf ticks)
Bootbase Version\t: V0.6 | 03/02/2004
ZyNOS CODE\t\t: RAS Mar  4 2008 11:51:18
Product Model\t\t: GS-3012""", 
## 'show interface config 6'
'show interface config 6': """ show interface config 6
  Port Configurations:
  
  
  Port No \t:6
    Active \t:Yes
    Name  \t:
    PVID \t:15\t\tFlow Control \t:No
    Type \t:10/100/1000M\tSpeed/Duplex \t:auto
    BPDU \t:peer\t\t802.1p Priority :0
  """, 
## 'show interfaces *'
'show interfaces *': """ show interfaces *
  Port Info\tPort NO.\t\t:1
  \t\tLink\t\t\t:1000M/F  
  \t\tStatus\t\t\t:FORWARDING
  \t\tLACP\t\t\t:Disabled
  \t\tTxPkts\t\t\t:6241963
  \t\tRxPkts\t\t\t:3478611
  \t\tErrors\t\t\t:0
  \t\tTx KBs/s\t\t:0.0
  \t\tRx KBs/s\t\t:0.0
  \t\tUp Time\t\t\t:105:53:55
  TX Packet\tTx Packets\t\t:6241963
  \t\tMulticast\t\t:1350684
  \t\tBroadcast\t\t:1546243
  \t\tPause\t\t\t:0
  \t\tTagged\t\t\t:220764
  RX Packet\tRx Packets\t\t:3478611
  \t\tMulticast\t\t:37795
  \t\tBroadcast\t\t:210456
  \t\tPause\t\t\t:0
  \t\tControl\t\t\t:0
  TX Collison\tSingle\t\t\t:0
  \t\tMultiple\t\t:0
  \t\tExcessive\t\t:0
 \t\tLate\t\t\t:0
  Error Packet\tRX CRC\t\t\t:0
  \t\tLength\t\t\t:0
  \t\tRunt\t\t\t:0
  Distribution\t64\t\t\t:2950113
  \t\t65 to 127\t\t:2718886
  \t\t128 to 255\t\t:2417823
  \t\t256 to 511\t\t:909941
  \t\t512 to 1023\t\t:155776
  \t\t1024 to 1518\t\t:568035
  \t\tGiant\t\t\t:0
  
  Port Info\tPort NO.\t\t:2
  \t\tLink\t\t\t:1000M/F  
  \t\tStatus\t\t\t:FORWARDING
  \t\tLACP\t\t\t:Disabled
  \t\tTxPkts\t\t\t:475809183
  \t\tRxPkts\t\t\t:372753925
  \t\tErrors\t\t\t:0
  \t\tTx KBs/s\t\t:21.516
  \t\tRx KBs/s\t\t:203.306
  \t\tUp Time\t\t\t:554:05:42
  TX Packet\tTx Packets\t\t:475809183
 \t\tMulticast\t\t:19617336
  \t\tBroadcast\t\t:98904319
  \t\tPause\t\t\t:0
  \t\tTagged\t\t\t:475809269
  RX Packet\tRx Packets\t\t:372753925
  \t\tMulticast\t\t:543078
  \t\tBroadcast\t\t:121478
  \t\tPause\t\t\t:0
  \t\tControl\t\t\t:0
  TX Collison\tSingle\t\t\t:0
  \t\tMultiple\t\t:0
  \t\tExcessive\t\t:0
  \t\tLate\t\t\t:0
  Error Packet\tRX CRC\t\t\t:0
  \t\tLength\t\t\t:0
  \t\tRunt\t\t\t:0
  Distribution\t64\t\t\t:91359539
  \t\t65 to 127\t\t:320889678
  \t\t128 to 255\t\t:24749911
  \t\t256 to 511\t\t:11544344
  \t\t512 to 1023\t\t:9561948
  \t\t1024 to 1518\t\t:263007147
  \t\tGiant\t\t\t:0
 
  Port Info\tPort NO.\t\t:3
  \t\tLink\t\t\t:1000M/F  
  \t\tStatus\t\t\t:FORWARDING
  \t\tLACP\t\t\t:Disabled
  \t\tTxPkts\t\t\t:36340694
  \t\tRxPkts\t\t\t:27950275
  \t\tErrors\t\t\t:0
  \t\tTx KBs/s\t\t:9.132
  \t\tRx KBs/s\t\t:0.630
  \t\tUp Time\t\t\t:554:05:43
  TX Packet\tTx Packets\t\t:36340694
  \t\tMulticast\t\t:1388428
  \t\tBroadcast\t\t:1706457
  \t\tPause\t\t\t:0
  \t\tTagged\t\t\t:220767
  RX Packet\tRx Packets\t\t:27950275
  \t\tMulticast\t\t:99
  \t\tBroadcast\t\t:50261
  \t\tPause\t\t\t:0
  \t\tControl\t\t\t:0
  TX Collison\tSingle\t\t\t:0
  \t\tMultiple\t\t:0
 \t\tExcessive\t\t:0
  \t\tLate\t\t\t:0
  Error Packet\tRX CRC\t\t\t:0
  \t\tLength\t\t\t:0
  \t\tRunt\t\t\t:0
  Distribution\t64\t\t\t:4383400
  \t\t65 to 127\t\t:24885256
  \t\t128 to 255\t\t:3253692
  \t\t256 to 511\t\t:5101627
  \t\t512 to 1023\t\t:4539160
  \t\t1024 to 1518\t\t:22127834
  \t\tGiant\t\t\t:0
  
  Port Info\tPort NO.\t\t:4
  \t\tLink\t\t\t:1000M/F  
  \t\tStatus\t\t\t:FORWARDING
  \t\tLACP\t\t\t:Disabled
  \t\tTxPkts\t\t\t:23347834
  \t\tRxPkts\t\t\t:15007192
  \t\tErrors\t\t\t:0
  \t\tTx KBs/s\t\t:0.126
  \t\tRx KBs/s\t\t:0.64
  \t\tUp Time\t\t\t:554:05:41
 TX Packet\tTx Packets\t\t:23347834
  \t\tMulticast\t\t:1378031
  \t\tBroadcast\t\t:1706615
  \t\tPause\t\t\t:0
  \t\tTagged\t\t\t:220767
  RX Packet\tRx Packets\t\t:15007192
  \t\tMulticast\t\t:10466
  \t\tBroadcast\t\t:50097
  \t\tPause\t\t\t:0
  \t\tControl\t\t\t:0
  TX Collison\tSingle\t\t\t:0
  \t\tMultiple\t\t:0
  \t\tExcessive\t\t:0
  \t\tLate\t\t\t:0
  Error Packet\tRX CRC\t\t\t:0
  \t\tLength\t\t\t:0
  \t\tRunt\t\t\t:0
  Distribution\t64\t\t\t:13965051
  \t\t65 to 127\t\t:7551123
  \t\t128 to 255\t\t:3313214
  \t\t256 to 511\t\t:2343774
  \t\t512 to 1023\t\t:652656
  \t\t1024 to 1518\t\t:10529208
 \t\tGiant\t\t\t:0
  
  Port Info\tPort NO.\t\t:5
  \t\tLink\t\t\t:1000M/F  
  \t\tStatus\t\t\t:FORWARDING
  \t\tLACP\t\t\t:Disabled
  \t\tTxPkts\t\t\t:46877947
  \t\tRxPkts\t\t\t:59312966
  \t\tErrors\t\t\t:0
  \t\tTx KBs/s\t\t:101.597
  \t\tRx KBs/s\t\t:8.143
  \t\tUp Time\t\t\t:100:12:47
  TX Packet\tTx Packets\t\t:46877947
  \t\tMulticast\t\t:1194050
  \t\tBroadcast\t\t:1650838
  \t\tPause\t\t\t:0
  \t\tTagged\t\t\t:220763
  RX Packet\tRx Packets\t\t:59312966
  \t\tMulticast\t\t:196791
  \t\tBroadcast\t\t:105848
  \t\tPause\t\t\t:0
  \t\tControl\t\t\t:0
  TX Collison\tSingle\t\t\t:0
 \t\tMultiple\t\t:0
  \t\tExcessive\t\t:0
  \t\tLate\t\t\t:0
  Error Packet\tRX CRC\t\t\t:0
  \t\tLength\t\t\t:0
  \t\tRunt\t\t\t:0
  Distribution\t64\t\t\t:26502152
  \t\t65 to 127\t\t:42831543
  \t\t128 to 255\t\t:2221267
  \t\t256 to 511\t\t:4256625
  \t\t512 to 1023\t\t:3401927
  \t\t1024 to 1518\t\t:26979663
  \t\tGiant\t\t\t:0
  
  Port Info\tPort NO.\t\t:6
  \t\tLink\t\t\t:1000M/F  
  \t\tStatus\t\t\t:FORWARDING
  \t\tLACP\t\t\t:Disabled
  \t\tTxPkts\t\t\t:310564500
  \t\tRxPkts\t\t\t:579000556
  \t\tErrors\t\t\t:0
  \t\tTx KBs/s\t\t:56.276
  \t\tRx KBs/s\t\t:143.222
 \t\tUp Time\t\t\t:129:10:07
  TX Packet\tTx Packets\t\t:310564500
  \t\tMulticast\t\t:1092644
  \t\tBroadcast\t\t:1676806
  \t\tPause\t\t\t:0
  \t\tTagged\t\t\t:220756
  RX Packet\tRx Packets\t\t:579000556
  \t\tMulticast\t\t:295772
  \t\tBroadcast\t\t:79821
  \t\tPause\t\t\t:0
  \t\tControl\t\t\t:0
  TX Collison\tSingle\t\t\t:0
  \t\tMultiple\t\t:0
  \t\tExcessive\t\t:0
  \t\tLate\t\t\t:0
  Error Packet\tRX CRC\t\t\t:0
  \t\tLength\t\t\t:0
  \t\tRunt\t\t\t:0
  Distribution\t64\t\t\t:53936149
  \t\t65 to 127\t\t:263231259
  \t\t128 to 255\t\t:12546372
  \t\t256 to 511\t\t:9333749
  \t\t512 to 1023\t\t:3827689
 \t\t1024 to 1518\t\t:546689838
  \t\tGiant\t\t\t:0
  
  Port Info\tPort NO.\t\t:7
  \t\tLink\t\t\t:Down  
  \t\tStatus\t\t\t:STOP
  \t\tLACP\t\t\t:Disabled
  \t\tTxPkts\t\t\t:0
  \t\tRxPkts\t\t\t:0
  \t\tErrors\t\t\t:0
  \t\tTx KBs/s\t\t:0.0
  \t\tRx KBs/s\t\t:0.0
  \t\tUp Time\t\t\t::00:00
  TX Packet\tTx Packets\t\t:0
  \t\tMulticast\t\t:0
  \t\tBroadcast\t\t:0
  \t\tPause\t\t\t:0
  \t\tTagged\t\t\t:0
  RX Packet\tRx Packets\t\t:0
  \t\tMulticast\t\t:0
  \t\tBroadcast\t\t:0
  \t\tPause\t\t\t:0
  \t\tControl\t\t\t:0
 TX Collison\tSingle\t\t\t:0
  \t\tMultiple\t\t:0
  \t\tExcessive\t\t:0
  \t\tLate\t\t\t:0
  Error Packet\tRX CRC\t\t\t:0
  \t\tLength\t\t\t:0
  \t\tRunt\t\t\t:0
  Distribution\t64\t\t\t:0
  \t\t65 to 127\t\t:0
  \t\t128 to 255\t\t:0
  \t\t256 to 511\t\t:0
  \t\t512 to 1023\t\t:0
  \t\t1024 to 1518\t\t:0
  \t\tGiant\t\t\t:0
  
  Port Info\tPort NO.\t\t:8
  \t\tLink\t\t\t:100M/F  
  \t\tStatus\t\t\t:FORWARDING
  \t\tLACP\t\t\t:Disabled
  \t\tTxPkts\t\t\t:102123736
  \t\tRxPkts\t\t\t:14474399
  \t\tErrors\t\t\t:0
  \t\tTx KBs/s\t\t:1.345
 \t\tRx KBs/s\t\t:0.102
  \t\tUp Time\t\t\t:554:03:42
  TX Packet\tTx Packets\t\t:102123736
  \t\tMulticast\t\t:15476450
  \t\tBroadcast\t\t:71173840
  \t\tPause\t\t\t:0
  \t\tTagged\t\t\t:102123736
  RX Packet\tRx Packets\t\t:14474399
  \t\tMulticast\t\t:1703
  \t\tBroadcast\t\t:2422
  \t\tPause\t\t\t:0
  \t\tControl\t\t\t:0
  TX Collison\tSingle\t\t\t:0
  \t\tMultiple\t\t:0
  \t\tExcessive\t\t:0
  \t\tLate\t\t\t:0
  Error Packet\tRX CRC\t\t\t:0
  \t\tLength\t\t\t:0
  \t\tRunt\t\t\t:0
  Distribution\t64\t\t\t:2835532
  \t\t65 to 127\t\t:92111592
  \t\t128 to 255\t\t:11261764
  \t\t256 to 511\t\t:4044059
 \t\t512 to 1023\t\t:3209303
  \t\t1024 to 1518\t\t:3133001
  \t\tGiant\t\t\t:0
  
  Port Info\tPort NO.\t\t:9
  \t\tLink\t\t\t:Down  
  \t\tStatus\t\t\t:STOP
  \t\tLACP\t\t\t:Disabled
  \t\tTxPkts\t\t\t:0
  \t\tRxPkts\t\t\t:0
  \t\tErrors\t\t\t:0
  \t\tTx KBs/s\t\t:0.0
  \t\tRx KBs/s\t\t:0.0
  \t\tUp Time\t\t\t::00:00
  TX Packet\tTx Packets\t\t:0
  \t\tMulticast\t\t:0
  \t\tBroadcast\t\t:0
  \t\tPause\t\t\t:0
  \t\tTagged\t\t\t:0
  RX Packet\tRx Packets\t\t:0
  \t\tMulticast\t\t:0
  \t\tBroadcast\t\t:0
  \t\tPause\t\t\t:0
 \t\tControl\t\t\t:0
  TX Collison\tSingle\t\t\t:0
  \t\tMultiple\t\t:0
  \t\tExcessive\t\t:0
  \t\tLate\t\t\t:0
  Error Packet\tRX CRC\t\t\t:0
  \t\tLength\t\t\t:0
  \t\tRunt\t\t\t:0
  Distribution\t64\t\t\t:0
  \t\t65 to 127\t\t:0
  \t\t128 to 255\t\t:0
  \t\t256 to 511\t\t:0
  \t\t512 to 1023\t\t:0
  \t\t1024 to 1518\t\t:0
  \t\tGiant\t\t\t:0
  
  Port Info\tPort NO.\t\t:10
  \t\tLink\t\t\t:Down  
  \t\tStatus\t\t\t:STOP
  \t\tLACP\t\t\t:Disabled
  \t\tTxPkts\t\t\t:0
  \t\tRxPkts\t\t\t:0
  \t\tErrors\t\t\t:0
 \t\tTx KBs/s\t\t:0.0
  \t\tRx KBs/s\t\t:0.0
  \t\tUp Time\t\t\t::00:00
  TX Packet\tTx Packets\t\t:0
  \t\tMulticast\t\t:0
  \t\tBroadcast\t\t:0
  \t\tPause\t\t\t:0
  \t\tTagged\t\t\t:0
  RX Packet\tRx Packets\t\t:0
  \t\tMulticast\t\t:0
  \t\tBroadcast\t\t:0
  \t\tPause\t\t\t:0
  \t\tControl\t\t\t:0
  TX Collison\tSingle\t\t\t:0
  \t\tMultiple\t\t:0
  \t\tExcessive\t\t:0
  \t\tLate\t\t\t:0
  Error Packet\tRX CRC\t\t\t:0
  \t\tLength\t\t\t:0
  \t\tRunt\t\t\t:0
  Distribution\t64\t\t\t:0
  \t\t65 to 127\t\t:0
  \t\t128 to 255\t\t:0
 \t\t256 to 511\t\t:0
  \t\t512 to 1023\t\t:0
  \t\t1024 to 1518\t\t:0
  \t\tGiant\t\t\t:0
  
  Port Info\tPort NO.\t\t:11
  \t\tLink\t\t\t:1000M/F SFP
  \t\tStatus\t\t\t:FORWARDING
  \t\tLACP\t\t\t:Disabled
  \t\tTxPkts\t\t\t:179797580
  \t\tRxPkts\t\t\t:103330930
  \t\tErrors\t\t\t:0
  \t\tTx KBs/s\t\t:40.802
  \t\tRx KBs/s\t\t:24.102
  \t\tUp Time\t\t\t:239:07:16
  TX Packet\tTx Packets\t\t:179797580
  \t\tMulticast\t\t:5794429
  \t\tBroadcast\t\t:56616593
  \t\tPause\t\t\t:0
  \t\tTagged\t\t\t:179797692
  RX Packet\tRx Packets\t\t:103330930
  \t\tMulticast\t\t:211808
  \t\tBroadcast\t\t:273511
 \t\tPause\t\t\t:0
  \t\tControl\t\t\t:0
  TX Collison\tSingle\t\t\t:0
  \t\tMultiple\t\t:0
  \t\tExcessive\t\t:0
  \t\tLate\t\t\t:0
  Error Packet\tRX CRC\t\t\t:0
  \t\tLength\t\t\t:0
  \t\tRunt\t\t\t:0
  Distribution\t64\t\t\t:4562401
  \t\t65 to 127\t\t:121222446
  \t\t128 to 255\t\t:91688077
  \t\t256 to 511\t\t:6818583
  \t\t512 to 1023\t\t:5866821
  \t\t1024 to 1518\t\t:13050751
  \t\tGiant\t\t\t:0
  
  Port Info\tPort NO.\t\t:12
  \t\tLink\t\t\t:1000M/F SFP
  \t\tStatus\t\t\t:FORWARDING
  \t\tLACP\t\t\t:Disabled
  \t\tTxPkts\t\t\t:1120431296
  \t\tRxPkts\t\t\t:969598920
 \t\tErrors\t\t\t:0
  \t\tTx KBs/s\t\t:381.239
  \t\tRx KBs/s\t\t:230.575
  \t\tUp Time\t\t\t:554:05:46
  TX Packet\tTx Packets\t\t:1120431296
  \t\tMulticast\t\t:1883140
  \t\tBroadcast\t\t:895092
  \t\tPause\t\t\t:0
  \t\tTagged\t\t\t:1119841798
  RX Packet\tRx Packets\t\t:969598920
  \t\tMulticast\t\t:21432039
  \t\tBroadcast\t\t:102159919
  \t\tPause\t\t\t:0
  \t\tControl\t\t\t:0
  TX Collison\tSingle\t\t\t:0
  \t\tMultiple\t\t:0
  \t\tExcessive\t\t:0
  \t\tLate\t\t\t:0
  Error Packet\tRX CRC\t\t\t:0
  \t\tLength\t\t\t:0
  \t\tRunt\t\t\t:0
  Distribution\t64\t\t\t:104038567
  \t\t65 to 127\t\t:761750087
 \t\t128 to 255\t\t:129268803
  \t\t256 to 511\t\t:34801170
  \t\t512 to 1023\t\t:27847911
  \t\t1024 to 1518\t\t:815628206
  \t\tGiant\t\t\t:0
  """, 
## 'show interface config 4'
'show interface config 4': """ show interface config 4
  Port Configurations:
  
  
  Port No \t:4
    Active \t:Yes
    Name  \t:
    PVID \t:15\t\tFlow Control \t:No
    Type \t:10/100/1000M\tSpeed/Duplex \t:auto
    BPDU \t:peer\t\t802.1p Priority :0
  """, 
## 'show interface config 3'
'show interface config 3': """ show interface config 3
  Port Configurations:
  
  
  Port No \t:3
    Active \t:Yes
    Name  \t:
    PVID \t:15\t\tFlow Control \t:No
    Type \t:10/100/1000M\tSpeed/Duplex \t:auto
    BPDU \t:peer\t\t802.1p Priority :0
  """, 
## 'show interface config 2'
'show interface config 2': """ show interface config 2
  Port Configurations:
  
  
  Port No \t:2
    Active \t:Yes
    Name  \t:
    PVID \t:15\t\tFlow Control \t:No
    Type \t:10/100/1000M\tSpeed/Duplex \t:auto
    BPDU \t:peer\t\t802.1p Priority :0
  """, 
## 'show interface config 1'
'show interface config 1': """ show interface config 1
  Port Configurations:
  
  
  Port No \t:1
    Active \t:Yes
    Name  \t:
    PVID \t:15\t\tFlow Control \t:No
    Type \t:10/100/1000M\tSpeed/Duplex \t:auto
    BPDU \t:peer\t\t802.1p Priority :0
  """, 
## 'show interface config 8'
'show interface config 8': """ show interface config 8
  Port Configurations:
  
  
  Port No \t:8
    Active \t:Yes
    Name  \t:
    PVID \t:1\t\tFlow Control \t:No
    Type \t:10/100/1000M\tSpeed/Duplex \t:100-full
    BPDU \t:peer\t\t802.1p Priority :0
  """, 
## 'show interface config 7'
'show interface config 7': """ show interface config 7
  Port Configurations:
  
  
  Port No \t:7
    Active \t:Yes
    Name  \t:
    PVID \t:15\t\tFlow Control \t:No
    Type \t:10/100/1000M\tSpeed/Duplex \t:auto
    BPDU \t:peer\t\t802.1p Priority :0
  """, 
## 'show interface config 10'
'show interface config 10': """ show interface config 10
  Port Configurations:
  
  
  Port No \t:10
    Active \t:Yes
    Name  \t:
    PVID \t:53\t\tFlow Control \t:No
    Type \t:10/100/1000M\tSpeed/Duplex \t:auto
    BPDU \t:peer\t\t802.1p Priority :0
  """, 
## 'show interface config *'
'show interface config *': """ show interface config *
  Port Configurations:
  
  
  Port No \t:1
    Active \t:Yes
    Name  \t:
    PVID \t:15\t\tFlow Control \t:No
    Type \t:10/100/1000M\tSpeed/Duplex \t:auto
    BPDU \t:peer\t\t802.1p Priority :0
  
  Port No \t:2
    Active \t:Yes
    Name  \t:
    PVID \t:15\t\tFlow Control \t:No
    Type \t:10/100/1000M\tSpeed/Duplex \t:auto
    BPDU \t:peer\t\t802.1p Priority :0
  
  Port No \t:3
    Active \t:Yes
    Name  \t:
    PVID \t:15\t\tFlow Control \t:No
    Type \t:10/100/1000M\tSpeed/Duplex \t:auto
    BPDU \t:peer\t\t802.1p Priority :0
 
  Port No \t:4
    Active \t:Yes
    Name  \t:
    PVID \t:15\t\tFlow Control \t:No
    Type \t:10/100/1000M\tSpeed/Duplex \t:auto
    BPDU \t:peer\t\t802.1p Priority :0
  
  Port No \t:5
    Active \t:Yes
    Name  \t:
    PVID \t:15\t\tFlow Control \t:No
    Type \t:10/100/1000M\tSpeed/Duplex \t:auto
    BPDU \t:peer\t\t802.1p Priority :0
  
  Port No \t:6
    Active \t:Yes
    Name  \t:
    PVID \t:15\t\tFlow Control \t:No
    Type \t:10/100/1000M\tSpeed/Duplex \t:auto
    BPDU \t:peer\t\t802.1p Priority :0
  
  Port No \t:7
   Active \t:Yes
    Name  \t:
    PVID \t:15\t\tFlow Control \t:No
    Type \t:10/100/1000M\tSpeed/Duplex \t:auto
    BPDU \t:peer\t\t802.1p Priority :0
  
  Port No \t:8
    Active \t:Yes
    Name  \t:
    PVID \t:1\t\tFlow Control \t:No
    Type \t:10/100/1000M\tSpeed/Duplex \t:100-full
    BPDU \t:peer\t\t802.1p Priority :0
  
  Port No \t:9
    Active \t:Yes
    Name  \t:
    PVID \t:1\t\tFlow Control \t:No
    Type \t:10/100/1000M\tSpeed/Duplex \t:auto
    BPDU \t:peer\t\t802.1p Priority :0
  
  Port No \t:10
    Active \t:Yes
    Name  \t:
   PVID \t:53\t\tFlow Control \t:No
    Type \t:10/100/1000M\tSpeed/Duplex \t:auto
    BPDU \t:peer\t\t802.1p Priority :0
  
  Port No \t:11
    Active \t:Yes
    Name  \t:
    PVID \t:1\t\tFlow Control \t:No
    Type \t:10/100/1000M\tSpeed/Duplex \t:auto
    BPDU \t:peer\t\t802.1p Priority :0
  
  Port No \t:12
    Active \t:Yes
    Name  \t:
    PVID \t:1\t\tFlow Control \t:No
    Type \t:10/100/1000M\tSpeed/Duplex \t:auto
    BPDU \t:peer\t\t802.1p Priority :0
  """, 
## 'show ip'
'show ip': """ show ip
Out-of-band Management IP Address = 172.16.16.222
Management IP Address
     IP[172.16.16.222], Netmask[255.255.255.0], VID[0]
IP Interface
     IP[10.8.5.131], Netmask[255.255.255.192], VID[95]
""", 
'show ip ospf interface':  ' show ip ospf interface\n  %Invalid command "ospf"\n', 
## 'show interface config 12'
'show interface config 12': """ show interface config 12
  Port Configurations:
  
  
  Port No \t:12
    Active \t:Yes
    Name  \t:
    PVID \t:1\t\tFlow Control \t:No
    Type \t:10/100/1000M\tSpeed/Duplex \t:auto
    BPDU \t:peer\t\t802.1p Priority :0
  """, 
## 'show interface config 5'
'show interface config 5': """ show interface config 5
  Port Configurations:
  
  
  Port No \t:5
    Active \t:Yes
    Name  \t:
    PVID \t:15\t\tFlow Control \t:No
    Type \t:10/100/1000M\tSpeed/Duplex \t:auto
    BPDU \t:peer\t\t802.1p Priority :0
  """, 
}
    snmp_get = {}
    snmp_getnext = {}
