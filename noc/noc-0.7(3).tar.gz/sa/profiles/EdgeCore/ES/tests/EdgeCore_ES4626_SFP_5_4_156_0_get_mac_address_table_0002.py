# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## EdgeCore.ES.get_mac_address_table test
## Auto-generated by manage.py debug-script at 2011-02-03 13:21:12
##----------------------------------------------------------------------
## Copyright (C) 2007-2011 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------
from noc.lib.test import ScriptTestCase
class EdgeCore_ES_get_mac_address_table_Test(ScriptTestCase):
    script="EdgeCore.ES.get_mac_address_table"
    vendor="EdgeCore"
    platform='ES4626-SFP'
    version='5.4.156.0'
    input={}
    result=[{'interfaces': ['Ethernet1/2'],
  'mac': '00:23:34:42:BB:08',
  'type': 'D',
  'vlan_id': 1},
 {'interfaces': ['Port-Channel1'],
  'mac': '00:30:48:DD:8B:28',
  'type': 'D',
  'vlan_id': 1},
 {'interfaces': ['Ethernet1/25'],
  'mac': '00:0F:E2:6A:CF:40',
  'type': 'D',
  'vlan_id': 69},
 {'interfaces': ['Ethernet1/25'],
  'mac': '00:12:CF:39:95:90',
  'type': 'D',
  'vlan_id': 69},
 {'interfaces': ['Ethernet1/25'],
  'mac': '00:12:CF:41:37:C0',
  'type': 'D',
  'vlan_id': 69},
 {'interfaces': ['Ethernet1/25'],
  'mac': '00:12:CF:4C:01:80',
  'type': 'D',
  'vlan_id': 69},
 {'interfaces': ['Ethernet1/25'],
  'mac': '00:12:CF:4C:57:80',
  'type': 'D',
  'vlan_id': 69},
 {'interfaces': ['Ethernet1/25'],
  'mac': '00:12:CF:4C:64:80',
  'type': 'D',
  'vlan_id': 69},
 {'interfaces': ['Ethernet1/25'],
  'mac': '00:12:CF:4C:6B:C0',
  'type': 'D',
  'vlan_id': 69},
 {'interfaces': ['Ethernet1/25'],
  'mac': '00:12:CF:90:F5:00',
  'type': 'D',
  'vlan_id': 69},
 {'interfaces': ['CPU'],
  'mac': '00:12:CF:A3:CB:3D',
  'type': 'S',
  'vlan_id': 69},
 {'interfaces': ['Ethernet1/25'],
  'mac': '00:0F:E2:6A:CF:40',
  'type': 'D',
  'vlan_id': 2076},
 {'interfaces': ['Ethernet1/2'],
  'mac': '00:0C:29:CD:9E:F6',
  'type': 'D',
  'vlan_id': 3000},
 {'interfaces': ['CPU'],
  'mac': '00:12:CF:A3:CB:3D',
  'type': 'S',
  'vlan_id': 3000},
 {'interfaces': ['Port-Channel3'],
  'mac': '00:1B:21:4B:D8:F8',
  'type': 'D',
  'vlan_id': 3000},
 {'interfaces': ['Port-Channel3'],
  'mac': '00:1B:21:4B:D8:F8',
  'type': 'D',
  'vlan_id': 3100},
 {'interfaces': ['Ethernet1/25'],
  'mac': '00:26:88:70:90:00',
  'type': 'D',
  'vlan_id': 3100},
 {'interfaces': ['Port-Channel1'],
  'mac': '00:30:48:DD:A2:54',
  'type': 'D',
  'vlan_id': 3100},
 {'interfaces': ['CPU'],
  'mac': '00:12:CF:A3:CB:3D',
  'type': 'S',
  'vlan_id': 3101},
 {'interfaces': ['Port-Channel3'],
  'mac': '00:1B:21:4B:D8:F8',
  'type': 'D',
  'vlan_id': 3101},
 {'interfaces': ['Port-Channel1'],
  'mac': '00:30:48:DD:A2:54',
  'type': 'D',
  'vlan_id': 3101},
 {'interfaces': ['Ethernet1/25'],
  'mac': '00:12:CF:82:08:D7',
  'type': 'D',
  'vlan_id': 3103},
 {'interfaces': ['Port-Channel3'],
  'mac': '00:1B:21:4B:D8:F8',
  'type': 'D',
  'vlan_id': 3103},
 {'interfaces': ['Port-Channel1'],
  'mac': '00:30:48:DD:A2:54',
  'type': 'D',
  'vlan_id': 3103},
 {'interfaces': ['Port-Channel3'],
  'mac': '00:1B:21:4B:D8:F8',
  'type': 'D',
  'vlan_id': 3104},
 {'interfaces': ['Ethernet1/25'],
  'mac': '00:23:9C:1F:E9:C0',
  'type': 'D',
  'vlan_id': 3104},
 {'interfaces': ['Port-Channel1'],
  'mac': '00:30:48:DD:A2:54',
  'type': 'D',
  'vlan_id': 3104},
 {'interfaces': ['Port-Channel3'],
  'mac': '00:1B:21:4B:D8:F8',
  'type': 'D',
  'vlan_id': 3105},
 {'interfaces': ['Ethernet1/25'],
  'mac': '00:23:9C:06:8E:80',
  'type': 'D',
  'vlan_id': 3105},
 {'interfaces': ['Port-Channel1'],
  'mac': '00:30:48:DD:A2:54',
  'type': 'D',
  'vlan_id': 3105},
 {'interfaces': ['Ethernet1/25'],
  'mac': '00:12:CF:41:37:C0',
  'type': 'D',
  'vlan_id': 3106},
 {'interfaces': ['Ethernet1/25'],
  'mac': '00:12:CF:82:09:09',
  'type': 'D',
  'vlan_id': 3106},
 {'interfaces': ['Port-Channel3'],
  'mac': '00:1B:21:4B:D8:F8',
  'type': 'D',
  'vlan_id': 3106},
 {'interfaces': ['Ethernet1/25'],
  'mac': '00:24:C3:1B:80:45',
  'type': 'D',
  'vlan_id': 3106},
 {'interfaces': ['Port-Channel1'],
  'mac': '00:30:48:DD:A2:54',
  'type': 'D',
  'vlan_id': 3106}]
    motd='********\n'
    cli={
## 'show mac-address-table'
'show mac-address-table': """show mac-address-table
Read mac address table....
Vlan Mac Address                 Type    Creator   Ports
---- --------------------------- ------- -------------------------------------
1    00-23-34-42-bb-08           DYNAMIC Hardware Ethernet1/2
1    00-30-48-dd-8b-28           DYNAMIC Hardware Port-Channel1
69   00-0f-e2-6a-cf-40           DYNAMIC Hardware Ethernet1/25
69   00-12-cf-39-95-90           DYNAMIC Hardware Ethernet1/25
69   00-12-cf-41-37-c0           DYNAMIC Hardware Ethernet1/25
69   00-12-cf-4c-01-80           DYNAMIC Hardware Ethernet1/25
69   00-12-cf-4c-57-80           DYNAMIC Hardware Ethernet1/25
69   00-12-cf-4c-64-80           DYNAMIC Hardware Ethernet1/25
69   00-12-cf-4c-6b-c0           DYNAMIC Hardware Ethernet1/25
69   00-12-cf-90-f5-00           DYNAMIC Hardware Ethernet1/25
69   00-12-cf-a3-cb-3d           STATIC  System   CPU
2076 00-0f-e2-6a-cf-40           DYNAMIC Hardware Ethernet1/25
3000 00-0c-29-cd-9e-f6           DYNAMIC Hardware Ethernet1/2
3000 00-12-cf-a3-cb-3d           STATIC  System   CPU
3000 00-1b-21-4b-d8-f8           DYNAMIC Hardware Port-Channel3
3100 00-1b-21-4b-d8-f8           DYNAMIC Hardware Port-Channel3
3100 00-26-88-70-90-00           DYNAMIC Hardware Ethernet1/25
3100 00-30-48-dd-a2-54           DYNAMIC Hardware Port-Channel1
3101 00-12-cf-a3-cb-3d           STATIC  System   CPU
3101 00-1b-21-4b-d8-f8           DYNAMIC Hardware Port-Channel3
 3101 00-26-88-70-7f-00           DYNAMIC Hardware Ethernet1/25
3101 00-30-48-dd-a2-54           DYNAMIC Hardware Port-Channel1
3103 00-12-cf-82-08-d7           DYNAMIC Hardware Ethernet1/25
3103 00-1b-21-4b-d8-f8           DYNAMIC Hardware Port-Channel3
3103 00-30-48-dd-a2-54           DYNAMIC Hardware Port-Channel1
3104 00-1b-21-4b-d8-f8           DYNAMIC Hardware Port-Channel3
3104 00-23-9c-1f-e9-c0           DYNAMIC Hardware Ethernet1/25
3104 00-30-48-dd-a2-54           DYNAMIC Hardware Port-Channel1
3105 00-1b-21-4b-d8-f8           DYNAMIC Hardware Port-Channel3
3105 00-23-9c-06-8e-80           DYNAMIC Hardware Ethernet1/25
3105 00-30-48-dd-a2-54           DYNAMIC Hardware Port-Channel1
3106 00-12-cf-41-37-c0           DYNAMIC Hardware Ethernet1/25
3106 00-12-cf-82-09-09           DYNAMIC Hardware Ethernet1/25
3106 00-1b-21-4b-d8-f8           DYNAMIC Hardware Port-Channel3
3106 00-24-c3-1b-80-45           DYNAMIC Hardware Ethernet1/25
3106 00-30-48-dd-a2-54           DYNAMIC Hardware Port-Channel1""",
}
    snmp_get={}
    snmp_getnext={}
