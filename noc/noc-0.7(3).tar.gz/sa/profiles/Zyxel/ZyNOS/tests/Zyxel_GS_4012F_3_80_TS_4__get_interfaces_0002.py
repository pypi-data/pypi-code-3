# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Zyxel.ZyNOS.get_interfaces test
## Auto-generated by ./noc debug-script at 2011-10-20 15:39:52
##----------------------------------------------------------------------
## Copyright (C) 2007-2011 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

## NOC modules
from noc.lib.test import ScriptTestCase


class Zyxel_ZyNOS_get_interfaces_Test(ScriptTestCase):
    script = "Zyxel.ZyNOS.get_interfaces"
    vendor = "Zyxel"
    platform = 'GS-4012F'
    version = '3.80(TS.4)'
    input = {}
    result = [{'forwarding_instance': 'default',
  'interfaces': [{'admin_status': True,
                  'description': 'dom1',
                  'mac': '00:13:49:EA:6A:45',
                  'name': '1',
                  'oper_status': True,
                  'subinterfaces': [{'admin_status': True,
                                     'is_bridge': True,
                                     'name': '1',
                                     'oper_status': True,
                                     'tagged_vlans': [547,
                                                      2203,
                                                      2225,
                                                      2226,
                                                      2227,
                                                      2228,
                                                      2230,
                                                      2231,
                                                      3000,
                                                      3997,
                                                      4015,
                                                      4058]}],
                  'type': 'physical'},
                 {'admin_status': True,
                  'description': 'dom3',
                  'mac': '00:13:49:EA:6A:45',
                  'name': '2',
                  'oper_status': True,
                  'subinterfaces': [{'admin_status': True,
                                     'is_bridge': True,
                                     'name': '2',
                                     'oper_status': True,
                                     'tagged_vlans': [2204, 2231, 4015]}],
                  'type': 'physical'},
                 {'admin_status': True,
                  'mac': '00:13:49:EA:6A:45',
                  'name': '3',
                  'oper_status': False,
                  'subinterfaces': [{'admin_status': True,
                                     'is_bridge': True,
                                     'name': '3',
                                     'oper_status': False,
                                     'tagged_vlans': [2231]}],
                  'type': 'physical'},
                 {'admin_status': True,
                  'mac': '00:13:49:EA:6A:45',
                  'name': '4',
                  'oper_status': False,
                  'subinterfaces': [{'admin_status': True,
                                     'is_bridge': True,
                                     'name': '4',
                                     'oper_status': False,
                                     'tagged_vlans': [2231]}],
                  'type': 'physical'},
                 {'admin_status': True,
                  'mac': '00:13:49:EA:6A:45',
                  'name': '5',
                  'oper_status': False,
                  'subinterfaces': [{'admin_status': True,
                                     'is_bridge': True,
                                     'name': '5',
                                     'oper_status': False,
                                     'tagged_vlans': [2231]}],
                  'type': 'physical'},
                 {'admin_status': True,
                  'mac': '00:13:49:EA:6A:45',
                  'name': '6',
                  'oper_status': False,
                  'subinterfaces': [{'admin_status': True,
                                     'is_bridge': True,
                                     'name': '6',
                                     'oper_status': False,
                                     'tagged_vlans': [2231]}],
                  'type': 'physical'},
                 {'admin_status': True,
                  'mac': '00:13:49:EA:6A:45',
                  'name': '7',
                  'oper_status': False,
                  'subinterfaces': [{'admin_status': True,
                                     'is_bridge': True,
                                     'name': '7',
                                     'oper_status': False,
                                     'tagged_vlans': [2231]}],
                  'type': 'physical'},
                 {'admin_status': True,
                  'mac': '00:13:49:EA:6A:45',
                  'name': '8',
                  'oper_status': False,
                  'subinterfaces': [{'admin_status': True,
                                     'is_bridge': True,
                                     'name': '8',
                                     'oper_status': False,
                                     'tagged_vlans': [2231]}],
                  'type': 'physical'},
                 {'admin_status': True,
                  'mac': '00:13:49:EA:6A:45',
                  'name': '9',
                  'oper_status': False,
                  'subinterfaces': [{'admin_status': True,
                                     'is_bridge': True,
                                     'name': '9',
                                     'oper_status': False,
                                     'tagged_vlans': [2231]}],
                  'type': 'physical'},
                 {'admin_status': True,
                  'mac': '00:13:49:EA:6A:45',
                  'name': '10',
                  'oper_status': False,
                  'subinterfaces': [{'admin_status': True,
                                     'is_bridge': True,
                                     'name': '10',
                                     'oper_status': False,
                                     'tagged_vlans': [2231]}],
                  'type': 'physical'},
                 {'admin_status': True,
                  'description': 'dom5',
                  'mac': '00:13:49:EA:6A:45',
                  'name': '11',
                  'oper_status': True,
                  'subinterfaces': [{'admin_status': True,
                                     'is_bridge': True,
                                     'name': '11',
                                     'oper_status': True,
                                     'tagged_vlans': [515,
                                                      516,
                                                      523,
                                                      529,
                                                      2200,
                                                      2201,
                                                      2202,
                                                      2205,
                                                      2206,
                                                      2207,
                                                      2208,
                                                      2210,
                                                      2212,
                                                      2213,
                                                      2221,
                                                      2231,
                                                      4015]}],
                  'type': 'physical'},
                 {'admin_status': True,
                  'description': 'uplink',
                  'mac': '00:13:49:EA:6A:45',
                  'name': '12',
                  'oper_status': True,
                  'subinterfaces': [{'admin_status': True,
                                     'is_bridge': True,
                                     'name': '12',
                                     'oper_status': True,
                                     'tagged_vlans': [515,
                                                      516,
                                                      523,
                                                      529,
                                                      547,
                                                      2200,
                                                      2201,
                                                      2202,
                                                      2203,
                                                      2204,
                                                      2205,
                                                      2206,
                                                      2207,
                                                      2208,
                                                      2210,
                                                      2212,
                                                      2213,
                                                      2221,
                                                      2225,
                                                      2226,
                                                      2227,
                                                      2228,
                                                      2230,
                                                      2231,
                                                      3000,
                                                      4015,
                                                      4058]}],
                  'type': 'physical'},
                 {'admin_status': True,
                  'description': 'Outband management',
                  'mac': '00:13:49:EA:6A:45',
                  'name': 'Mgmt',
                  'oper_status': True,
                  'subinterfaces': [{'admin_status': True,
                                     'ipv4_adresses': ['192.168.0.1/24'],
                                     'is_ipv4': True,
                                     'name': 'Mgmt',
                                     'oper_status': True,
                                     'vlan_ids': []}],
                  'type': 'SVI'},
                 {'admin_status': True,
                  'description': 'vlan3997',
                  'mac': '00:13:49:EA:6A:45',
                  'name': 'vlan3997',
                  'oper_status': True,
                  'subinterfaces': [{'admin_status': True,
                                     'ipv4_adresses': ['10.254.172.16/24'],
                                     'is_ipv4': True,
                                     'is_ospf': True,
                                     'is_rip': True,
                                     'name': 'vlan3997',
                                     'oper_status': True,
                                     'vlan_ids': [3997]}],
                  'type': 'SVI'},
                 {'admin_status': True,
                  'description': 'vlan3000',
                  'mac': '00:13:49:EA:6A:45',
                  'name': 'vlan3000',
                  'oper_status': True,
                  'subinterfaces': [{'admin_status': True,
                                     'ipv4_adresses': ['10.254.119.3/29'],
                                     'is_ipv4': True,
                                     'name': 'vlan3000',
                                     'oper_status': True,
                                     'vlan_ids': [3000]}],
                  'type': 'SVI'}],
  'type': 'ip'}]
    motd = ' **********\nCopyright (c) 1994 - 2008 ZyXEL Communications Corp.\n'
    cli = {
## 'show vlan-stacking'
'show vlan-stacking': """ show vlan-stacking
Switch Vlan Stacking Configuration
Operation: inactive
STPID: 0x8100

Port\t\t Role\t\t SPVID\t\t Priority
01\t\t access\t\t 1\t\t 0
02\t\t access\t\t 1\t\t 0
03\t\t access\t\t 1\t\t 0
04\t\t access\t\t 1\t\t 0
05\t\t access\t\t 1\t\t 0
06\t\t access\t\t 1\t\t 0
07\t\t access\t\t 1\t\t 0
08\t\t access\t\t 1\t\t 0
09\t\t access\t\t 1\t\t 0
10\t\t access\t\t 1\t\t 0
11\t\t access\t\t 1\t\t 0
12\t\t access\t\t 1\t\t 0""", 
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
## 'show ip'
'show ip': """ show ip
Management IP Address
     IP[192.168.0.1], Netmask[255.255.255.0], VID[0]
IP Interface
     IP[10.254.172.16], Netmask[255.255.255.0], VID[3997]
     IP[10.254.119.3], Netmask[255.255.255.248], VID[3000]
""", 
## 'show system-information'
'show system-information': """ show system-information

System Name\t\t: sw-dom-5
System Contact\t\t: admin@someprovider.net
System Location\t\t: Dom, 5
Ethernet Address\t: 00:13:49:ea:6a:45
ZyNOS F/W Version\t: V3.80(TS.4) | 10/07/2008
RomRasSize\t\t: 3191378 
System up Time\t\t:  1298:29:16 (1bdccecf ticks)
Bootbase Version\t: V3.0 | 04/08/2005
ZyNOS CODE\t\t: RAS Oct  6 2008 17:28:42
Product Model\t\t: GS-4012F""", 
## 'show vlan'
'show vlan': """ show vlan
  The Number of VLAN :    29
  Idx.  VID   Status     Elap-Time    TagCtl                                 
  ----  ----  ---------  -----------  ---------------------------------------
  
     1     1     Static   1298:28:55  Untagged :
                                      Tagged   :
  
     2   515     Static   1298:28:55  Untagged :
                                      Tagged   :11-12
  
     3   516     Static   1298:28:55  Untagged :
                                      Tagged   :11-12
  
     4   523     Static   1298:28:55  Untagged :
                                      Tagged   :11-12
  
     5   529     Static   1298:28:55  Untagged :
                                      Tagged   :11-12
  
     6   547     Static   1298:28:55  Untagged :
                                      Tagged   :1,12
  
     7  2200     Static   1298:28:55  Untagged :
                                     Tagged   :11-12
  
     8  2201     Static   1298:28:55  Untagged :
                                      Tagged   :11-12
  
     9  2202     Static   1298:28:55  Untagged :
                                      Tagged   :11-12
  
    10  2203     Static   1298:28:55  Untagged :
                                      Tagged   :1,12
  
    11  2204     Static   1298:28:55  Untagged :
                                      Tagged   :2,12
  
    12  2205     Static   1298:28:55  Untagged :
                                      Tagged   :11-12
  
    13  2206     Static   1298:28:55  Untagged :
                                      Tagged   :11-12
  
    14  2207     Static   1298:28:55  Untagged :
                                      Tagged   :11-12
  
   15  2208     Static   1298:28:55  Untagged :
                                      Tagged   :11-12
  
    16  2210     Static   1298:28:55  Untagged :
                                      Tagged   :11-12
  
    17  2212     Static   1298:28:55  Untagged :
                                      Tagged   :11-12
  
    18  2213     Static   1298:28:55  Untagged :
                                      Tagged   :11-12
  
    19  2221     Static   1298:28:55  Untagged :
                                      Tagged   :11-12
  
    20  2225     Static   1298:28:55  Untagged :
                                      Tagged   :1,12
  
    21  2226     Static   1298:28:55  Untagged :
                                      Tagged   :1,12
  
    22  2227     Static   1298:28:55  Untagged :
                                      Tagged   :1,12
 
    23  2228     Static   1298:28:55  Untagged :
                                      Tagged   :1,12
  
    24  2230     Static   1298:28:55  Untagged :
                                      Tagged   :1,12
  
    25  2231     Static   1298:28:55  Untagged :
                                      Tagged   :1-12
  
    26  3000     Static   1298:28:55  Untagged :
                                      Tagged   :1,12
  
    27  3997     Static      0:13:59  Untagged :
                                      Tagged   :1
  
    28  4015     Static   1298:28:55  Untagged :
                                      Tagged   :1-2,11-12
  
    29  4058     Static   1298:28:55  Untagged :
                                      Tagged   :1,12""", 
## 'show router rip'
'show router rip': """ show router rip
  IP Address      Subnet Mask     Direction  Version
  --------------------------------------------------
  10.254.119.3    255.255.255.248 None       V1
  10.254.172.16   255.255.255.0   Both       V2B""", 
## 'show interface config *'
'show interface config *': """ show interface config *
  Port Configurations:
  
  
  Port No \t:1
    Active \t:Yes
    Name  \t:dom1
    PVID \t:1\t\tFlow Control \t:No
    Type \t:1000M\tSpeed/Duplex \t:auto
    BPDU \t:peer\t\t802.1p Priority :0
  
  Port No \t:2
    Active \t:Yes
    Name  \t:dom3
    PVID \t:1\t\tFlow Control \t:No
    Type \t:1000M\tSpeed/Duplex \t:auto
    BPDU \t:peer\t\t802.1p Priority :0
  
  Port No \t:3
    Active \t:Yes
    Name  \t:
    PVID \t:1\t\tFlow Control \t:No
    Type \t:1000M\tSpeed/Duplex \t:auto
    BPDU \t:peer\t\t802.1p Priority :0
 
  Port No \t:4
    Active \t:Yes
    Name  \t:
    PVID \t:1\t\tFlow Control \t:No
    Type \t:1000M\tSpeed/Duplex \t:auto
    BPDU \t:peer\t\t802.1p Priority :0
  
  Port No \t:5
    Active \t:Yes
    Name  \t:
    PVID \t:1\t\tFlow Control \t:No
    Type \t:1000M\tSpeed/Duplex \t:auto
    BPDU \t:peer\t\t802.1p Priority :0
  
  Port No \t:6
    Active \t:Yes
    Name  \t:
    PVID \t:1\t\tFlow Control \t:No
    Type \t:1000M\tSpeed/Duplex \t:auto
    BPDU \t:peer\t\t802.1p Priority :0
  
  Port No \t:7
   Active \t:Yes
    Name  \t:
    PVID \t:1\t\tFlow Control \t:No
    Type \t:1000M\tSpeed/Duplex \t:auto
    BPDU \t:peer\t\t802.1p Priority :0
  
  Port No \t:8
    Active \t:Yes
    Name  \t:
    PVID \t:1\t\tFlow Control \t:No
    Type \t:1000M\tSpeed/Duplex \t:auto
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
   PVID \t:1\t\tFlow Control \t:No
    Type \t:10/100/1000M\tSpeed/Duplex \t:auto
    BPDU \t:peer\t\t802.1p Priority :0
  
  Port No \t:11
    Active \t:Yes
    Name  \t:dom5
    PVID \t:1\t\tFlow Control \t:No
    Type \t:10/100/1000M\tSpeed/Duplex \t:auto
    BPDU \t:peer\t\t802.1p Priority :0
  
  Port No \t:12
    Active \t:Yes
    Name  \t:uplink
    PVID \t:1\t\tFlow Control \t:No
    Type \t:10/100/1000M\tSpeed/Duplex \t:auto
    BPDU \t:peer\t\t802.1p Priority :0
  """, 
## 'show ip ospf interface'
'show ip ospf interface': """ show ip ospf interface
swif4 is up, line protocol is up
  Internet Address 10.254.172.16/24, Area 0.0.0.0
  Router ID 10.254.119.3, Network Type BROADCAST, Cost: 15
  Transmit Delay is 1 sec, State DR, Priority 1
  Designated Router (ID) 10.254.119.3, Interface Address 10.254.172.16
  No backup designated router on this network
  Timer intervals configured, Hello 10, Dead 40, Wait 40, Retransmit 5
    Hello due in 00:00:08
  Neighbor Count is 0, Adjacent neighbor count is 0""", 
}
    snmp_get = {'1.3.6.1.2.1.1.1.0': 'GS-4012F',
 '1.3.6.1.2.1.2.2.1.7.1': '1',
 '1.3.6.1.2.1.2.2.1.7.10': '1',
 '1.3.6.1.2.1.2.2.1.7.11': '1',
 '1.3.6.1.2.1.2.2.1.7.12': '1',
 '1.3.6.1.2.1.2.2.1.7.2': '1',
 '1.3.6.1.2.1.2.2.1.7.3': '1',
 '1.3.6.1.2.1.2.2.1.7.4': '1',
 '1.3.6.1.2.1.2.2.1.7.5': '1',
 '1.3.6.1.2.1.2.2.1.7.6': '1',
 '1.3.6.1.2.1.2.2.1.7.7': '1',
 '1.3.6.1.2.1.2.2.1.7.8': '1',
 '1.3.6.1.2.1.2.2.1.7.9': '1',
 '1.3.6.1.4.1.890.1.5.8.20.1.1.0': '3',
 '1.3.6.1.4.1.890.1.5.8.20.1.2.0': '80',
 '1.3.6.1.4.1.890.1.5.8.20.1.3.0': 'TS',
 '1.3.6.1.4.1.890.1.5.8.20.1.4.0': '4'}
    snmp_getnext = {'1.3.6.1.2.1.2.2.1.8': [('1.3.6.1.2.1.2.2.1.8.1', '1'),
                         ('1.3.6.1.2.1.2.2.1.8.2', '1'),
                         ('1.3.6.1.2.1.2.2.1.8.3', '2'),
                         ('1.3.6.1.2.1.2.2.1.8.4', '2'),
                         ('1.3.6.1.2.1.2.2.1.8.5', '2'),
                         ('1.3.6.1.2.1.2.2.1.8.6', '2'),
                         ('1.3.6.1.2.1.2.2.1.8.7', '2'),
                         ('1.3.6.1.2.1.2.2.1.8.8', '2'),
                         ('1.3.6.1.2.1.2.2.1.8.9', '2'),
                         ('1.3.6.1.2.1.2.2.1.8.10', '2'),
                         ('1.3.6.1.2.1.2.2.1.8.11', '1'),
                         ('1.3.6.1.2.1.2.2.1.8.12', '1')],
 '1.3.6.1.2.1.31.1.1.1.1': [('1.3.6.1.2.1.31.1.1.1.1.1', 'swp00'),
                            ('1.3.6.1.2.1.31.1.1.1.1.2', 'swp01'),
                            ('1.3.6.1.2.1.31.1.1.1.1.3', 'swp02'),
                            ('1.3.6.1.2.1.31.1.1.1.1.4', 'swp03'),
                            ('1.3.6.1.2.1.31.1.1.1.1.5', 'swp04'),
                            ('1.3.6.1.2.1.31.1.1.1.1.6', 'swp05'),
                            ('1.3.6.1.2.1.31.1.1.1.1.7', 'swp06'),
                            ('1.3.6.1.2.1.31.1.1.1.1.8', 'swp07'),
                            ('1.3.6.1.2.1.31.1.1.1.1.9', 'swp08'),
                            ('1.3.6.1.2.1.31.1.1.1.1.10', 'swp09'),
                            ('1.3.6.1.2.1.31.1.1.1.1.11', 'swp10'),
                            ('1.3.6.1.2.1.31.1.1.1.1.12', 'swp11')]}
