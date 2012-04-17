# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Zyxel.ZyNOS.get_vlans test
## Auto-generated by manage.py debug-script at 2011-06-09 19:01:43
##----------------------------------------------------------------------
## Copyright (C) 2007-2011 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------
from noc.lib.test import ScriptTestCase
class Zyxel_ZyNOS_get_vlans_Test(ScriptTestCase):
    script = "Zyxel.ZyNOS.get_vlans"
    vendor = "Zyxel"
    platform = 'ES-2024A'
    version = '3.80(TX.0)'
    input = {}
    result = [{'name': 'default', 'vlan_id': 1},
 {'name': 'Management', 'vlan_id': 2360},
 {'name': 'pppoe', 'vlan_id': 2603},
 {'name': 'dhcp', 'vlan_id': 4014}]
    motd = ' ********\nCopyright (c) 1994 - 2007 ZyXEL Communications Corp.\n'
    cli = {
## 'show vlan 2603'
'show vlan 2603': """ show vlan 2603
  802.1Q VLAN ID : 2603
  Name \t\t:pppoe
  Status \t : Static
  Elapsed Time   : 3055:32:11
  
  Port Information Mode
  ---------------- ----
     2             Untagged
     4             Untagged
    10             Untagged
    12             Untagged
    14             Untagged
    15             Untagged
    19             Untagged
    21             Untagged
    22             Untagged
    23             Untagged
    24             Untagged
    25             Tagged
    26             Tagged""", 
## 'show vlan 2360'
'show vlan 2360': """ show vlan 2360
  802.1Q VLAN ID : 2360
  Name \t\t:Management
  Status \t : Static
  Elapsed Time   : 7890:33:17
  
  Port Information Mode
  ---------------- ----
    25             Tagged
    26             Tagged
  
Default Management IP : 10.254.112.67 255.255.255.224
  
Default Gateway : 10.254.112.65""", 
## 'show vlan 1'
'show vlan 1': """ show vlan 1
  802.1Q VLAN ID : 1
  Name \t\t:default
  Status \t : Static
  Elapsed Time   : 7890:33:16
  
  Port Information Mode
  ---------------- ----""", 
## 'show vlan 4014'
'show vlan 4014': """ show vlan 4014
  802.1Q VLAN ID : 4014
  Name \t\t:dhcp
  Status \t : Static
  Elapsed Time   : 3055:17:37
  
  Port Information Mode
  ---------------- ----
     1             Untagged
     2             Untagged
     3             Untagged
     5             Untagged
     6             Untagged
     7             Untagged
     8             Untagged
     9             Untagged
    11             Untagged
    13             Untagged
    16             Untagged
    17             Untagged
    18             Untagged
    20             Untagged
    25             Tagged
    26             Tagged
 
IP Address\tSubnet Mask
  ---------------------------
  10.172.53.4\t255.255.255.0""", 
## 'show vlan'
'show vlan': """ show vlan
  The Number of VLAN :     4
  Idx.  VID   Status     Elap-Time    TagCtl                                 
  ----  ----  ---------  -----------  ---------------------------------------
  
     1     1     Static   7890:33:15  Untagged :
                                      Tagged   :
  
     2  2360     Static   7890:33:15  Untagged :
                                      Tagged   :25-26
  
     3  2603     Static   3055:32:08  Untagged :2,4,10,12,14-15,19,21-24
                                      Tagged   :25-26
  
     4  4014     Static   3055:17:33  Untagged :1-3,5-9,11,13,16-18,20
                                      Tagged   :25-26""", 
}
    snmp_get = {}
    snmp_getnext = {}
