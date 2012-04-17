# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## DLink.DxS.get_mac_address_table test
## Auto-generated by manage.py debug-script at 2011-03-29 13:12:55
##----------------------------------------------------------------------
## Copyright (C) 2007-2011 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------
from noc.lib.test import ScriptTestCase
class DLink_DxS_get_mac_address_table_Test(ScriptTestCase):
    script="DLink.DxS.get_mac_address_table"
    vendor="DLink"
    platform='DGS-3120-24TC'
    version='1.01.B033'
    input={}
    result=[{'interfaces': ['1:6'],
  'mac': '00:0C:76:28:8F:F6',
  'type': 'D',
  'vlan_id': 2},
 {'interfaces': ['1:3'],
  'mac': '00:15:17:27:EA:72',
  'type': 'D',
  'vlan_id': 2},
 {'interfaces': ['1:4'],
  'mac': '00:15:17:27:EA:81',
  'type': 'D',
  'vlan_id': 2},
 {'interfaces': ['1:7'],
  'mac': '00:1E:8C:C1:01:98',
  'type': 'D',
  'vlan_id': 2},
 {'interfaces': ['1:1'],
  'mac': '00:30:48:90:2A:2B',
  'type': 'D',
  'vlan_id': 2},
 {'interfaces': ['1:9'],
  'mac': '00:30:48:90:2A:2D',
  'type': 'D',
  'vlan_id': 2},
 {'interfaces': ['1:10'],
  'mac': '00:30:48:FD:6D:F9',
  'type': 'D',
  'vlan_id': 2},
 {'interfaces': ['1:8'],
  'mac': '00:30:4F:5C:85:E3',
  'type': 'D',
  'vlan_id': 2},
 {'interfaces': ['1:5'],
  'mac': '00:50:8B:09:CC:37',
  'type': 'D',
  'vlan_id': 2},
 {'interfaces': ['1:6'],
  'mac': '00:0C:76:28:8F:F6',
  'type': 'D',
  'vlan_id': 3},
 {'interfaces': ['1:2'],
  'mac': '00:22:B0:BC:67:F9',
  'type': 'D',
  'vlan_id': 3},
 {'interfaces': ['CPU'],
  'mac': '5C:D9:98:3F:A0:E9',
  'type': 'S',
  'vlan_id': 3},
 {'interfaces': ['1:6'],
  'mac': '00:0C:76:28:8F:F6',
  'type': 'D',
  'vlan_id': 9},
 {'interfaces': ['1:2'],
  'mac': '00:24:01:FC:33:75',
  'type': 'D',
  'vlan_id': 9}]
    motd='**********\n\n'
    cli={
## 'disable clipaging'
'disable clipaging': """disable clipaging
Command: disable clipaging

Success.                                                          
""", 
## 'show fdb'
'show fdb': """show fdb
Command: show fdb

 Unicast MAC Address Aging Time  = 300

 VID  VLAN Name                        MAC Address       Port  Type    Status
 ---- -------------------------------- ----------------- ----- ------- -------
 2    srv_ext                          00-0C-76-28-8F-F6 1:6   Dynamic Forward 
 2    srv_ext                          00-15-17-27-EA-72 1:3   Dynamic Forward 
 2    srv_ext                          00-15-17-27-EA-81 1:4   Dynamic Forward 
 2    srv_ext                          00-1E-8C-C1-01-98 1:7   Dynamic Forward 
 2    srv_ext                          00-30-48-90-2A-2B 1:1   Dynamic Forward 
 2    srv_ext                          00-30-48-90-2A-2D 1:9   Dynamic Forward 
 2    srv_ext                          00-30-48-FD-6D-F9 1:10  Dynamic Forward 
 2    srv_ext                          00-30-4F-5C-85-E3 1:8   Dynamic Forward 
 2    srv_ext                          00-50-8B-09-CC-37 1:5   Dynamic Forward 
 3    srv_int                          00-0C-76-28-8F-F6 1:6   Dynamic Forward 
 3    srv_int                          00-22-B0-BC-67-F9 1:2   Dynamic Forward 
 3    srv_int                          5C-D9-98-3F-A0-E9 CPU   Self    Forward 
 9    bm18_swlink                      00-0C-76-28-8F-F6 1:6   Dynamic Forward 
 9    bm18_swlink                      00-24-01-FC-33-75 1:2   Dynamic Forward 

Total Entries: 14

""", 
}
    snmp_get={}
    snmp_getnext={}
