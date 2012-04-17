# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## 3Com.SuperStack.get_mac_address_table test
## Auto-generated by manage.py debug-script at 2010-11-23 12:17:34
##----------------------------------------------------------------------
## Copyright (C) 2007-2010 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------
from noc.lib.test import ScriptTestCase
class _3Com_SuperStack_get_mac_address_table_Test(ScriptTestCase):
    script="3Com.SuperStack.get_mac_address_table"
    vendor="3Com"
    platform='SuperStack 3 Switch 3300XM'
    version='2.72'
    input={'mac': '00:1C:F0:27:28:40'}
    result=[{'interfaces': ['24'], 'mac': '00:1C:F0:27:28:40', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['24'],
  'mac': '00:1C:F0:27:28:40',
  'type': 'D',
  'vlan_id': 2116},
 {'interfaces': ['24'],
  'mac': '00:1C:F0:27:28:40',
  'type': 'D',
  'vlan_id': 208},
 {'interfaces': ['24'],
  'mac': '00:1C:F0:27:28:40',
  'type': 'D',
  'vlan_id': 207},
 {'interfaces': ['24'],
  'mac': '00:1C:F0:27:28:40',
  'type': 'D',
  'vlan_id': 18},
 {'interfaces': ['24'],
  'mac': '00:1C:F0:27:28:40',
  'type': 'D',
  'vlan_id': 251},
 {'interfaces': ['24'],
  'mac': '00:1C:F0:27:28:40',
  'type': 'D',
  'vlan_id': 210},
 {'interfaces': ['24'],
  'mac': '00:1C:F0:27:28:40',
  'type': 'D',
  'vlan_id': 3980},
 {'interfaces': ['24'],
  'mac': '00:1C:F0:27:28:40',
  'type': 'D',
  'vlan_id': 202},
 {'interfaces': ['24'],
  'mac': '00:1C:F0:27:28:40',
  'type': 'D',
  'vlan_id': 2101},
 {'interfaces': ['24'],
  'mac': '00:1C:F0:27:28:40',
  'type': 'D',
  'vlan_id': 746},
 {'interfaces': ['24'],
  'mac': '00:1C:F0:27:28:40',
  'type': 'D',
  'vlan_id': 205},
 {'interfaces': ['24'],
  'mac': '00:1C:F0:27:28:40',
  'type': 'D',
  'vlan_id': 206},
 {'interfaces': ['24'],
  'mac': '00:1C:F0:27:28:40',
  'type': 'D',
  'vlan_id': 2103}]
    motd=' \n\nMenu options: -------------3Com SuperStack 3 Switch 3300XM--------------\n bridge             - Administer bridging/VLANS\n ethernet           - Administer Ethernet ports\n feature            - Administer system features\n ip                 - Administer IP\n logout             - Logout of the Command Line Interface\n snmp               - Administer SNMP\n system             - Administer system-level functions\n\nType ? for help.\n-----------------------------------Omsk-115/(1) (1)---------------------\n'
    cli={
## 'bridge port address find 00-1c-f0-27-28-40'
'bridge port address find 00-1c-f0-27-28-40': """ bridge port address find 00-1c-f0-27-28-40

Location\tVLAN ID\tPermanent
Unit 1 Port 24\t   1\t   No
Unit 1 Port 24\t   2116\t   No
Unit 1 Port 24\t   208\t   No
Unit 1 Port 24\t   207\t   No
Unit 1 Port 24\t   18\t   No
Unit 1 Port 24\t   251\t   No
Unit 1 Port 24\t   210\t   No
Unit 1 Port 24\t   3980\t   No
Unit 1 Port 24\t   202\t   No
Unit 1 Port 24\t   2101\t   No
Unit 1 Port 24\t   746\t   No
Unit 1 Port 24\t   205\t   No
Unit 1 Port 24\t   206\t   No
Unit 1 Port 24\t   2103\t   No
""",
}
    snmp_get={}
    snmp_getnext={}
