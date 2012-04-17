# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Linksys.SPS2xx.get_mac_address_table test
## Auto-generated by ./noc debug-script at 2011-11-21 15:13:06
##----------------------------------------------------------------------
## Copyright (C) 2007-2011 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

## NOC modules
from noc.lib.test import ScriptTestCase


class Linksys_SPS2xx_get_mac_address_table_Test(ScriptTestCase):
    script = "Linksys.SPS2xx.get_mac_address_table"
    vendor = "Linksys"
    platform = 'SPS-224G4'
    version = '1.0.2'
    input = {'interface': 'g3', 'vlan': 72}
    result = [{'interfaces': ['g3'],
  'mac': '00:04:61:67:EF:BB',
  'type': 'D',
  'vlan_id': 72},
 {'interfaces': ['g3'],
  'mac': '00:15:6D:8E:89:B8',
  'type': 'D',
  'vlan_id': 72},
 {'interfaces': ['g3'],
  'mac': '00:15:6D:8E:8A:06',
  'type': 'D',
  'vlan_id': 72},
 {'interfaces': ['g3'],
  'mac': '00:1B:21:3B:4D:E6',
  'type': 'D',
  'vlan_id': 72},
 {'interfaces': ['g3'],
  'mac': '00:1B:B9:65:13:14',
  'type': 'D',
  'vlan_id': 72},
 {'interfaces': ['g3'],
  'mac': '00:1D:60:A7:11:E6',
  'type': 'D',
  'vlan_id': 72},
 {'interfaces': ['g3'],
  'mac': '00:24:54:A4:E8:5F',
  'type': 'D',
  'vlan_id': 72},
 {'interfaces': ['g3'],
  'mac': '00:25:11:C5:3B:F7',
  'type': 'D',
  'vlan_id': 72},
 {'interfaces': ['g3'],
  'mac': '00:25:22:28:72:34',
  'type': 'D',
  'vlan_id': 72},
 {'interfaces': ['g3'],
  'mac': '00:26:18:23:07:9F',
  'type': 'D',
  'vlan_id': 72},
 {'interfaces': ['g3'],
  'mac': '10:78:D2:81:B5:02',
  'type': 'D',
  'vlan_id': 72},
 {'interfaces': ['g3'],
  'mac': '1C:75:08:DC:93:EA',
  'type': 'D',
  'vlan_id': 72},
 {'interfaces': ['g3'],
  'mac': '1C:AF:F7:70:45:ED',
  'type': 'D',
  'vlan_id': 72},
 {'interfaces': ['g3'],
  'mac': '1C:AF:F7:70:72:56',
  'type': 'D',
  'vlan_id': 72},
 {'interfaces': ['g3'],
  'mac': '48:5B:39:D6:88:AB',
  'type': 'D',
  'vlan_id': 72},
 {'interfaces': ['g3'],
  'mac': 'E8:11:32:19:4F:13',
  'type': 'D',
  'vlan_id': 72}]
    motd = '*******\n\n'
    cli = {
'terminal datadump':  'terminal datadump\n', 
## 'show mac address-table vlan 72'
'show mac address-table vlan 72': """show mac address-table vlan 72
Aging time is 630 sec

  Vlan        Mac Address       Port     Type    
-------- --------------------- ------ ---------- 
   72      00:04:61:52:87:c3     e5    dynamic   
   72      00:04:61:5b:2b:de     e5    dynamic   
   72      00:04:61:67:ef:bb     g3    dynamic   
   72      00:15:6d:8e:89:b8     g3    dynamic   
   72      00:15:6d:8e:8a:06     g3    dynamic   
   72      00:1b:21:3b:4d:e6     g3    dynamic   
   72      00:1b:b9:65:13:14     g3    dynamic   
   72      00:1d:09:c3:e4:40     e5    dynamic   
   72      00:1d:60:20:80:2f     e5    dynamic   
   72      00:1d:60:76:1f:9e     e5    dynamic   
   72      00:1d:60:a7:11:e6     g3    dynamic   
   72      00:1e:8c:7f:23:c4     e5    dynamic   
   72      00:1e:90:ef:fc:42     e5    dynamic   
   72      00:24:54:a4:e8:5f     g3    dynamic   
   72      00:25:11:c0:95:0a     e5    dynamic   
   72      00:25:11:c5:3b:f7     g3    dynamic   
   72      00:25:22:13:2b:51     e5    dynamic   
   72      00:25:22:23:de:79     e5    dynamic   
   72      00:25:22:28:72:34     g3    dynamic   
   72      00:25:22:74:85:30     e5    dynamic   
   72      00:26:18:23:07:9f     g3    dynamic   
   72      00:26:18:ef:47:ac     e5    dynamic   
   72      00:e0:4c:a5:42:d9     e5    dynamic   
   72      10:78:d2:81:b5:02     g3    dynamic   
   72      1c:75:08:b3:70:07     e5    dynamic   
   72      1c:75:08:dc:93:ea     g3    dynamic   
   72      1c:af:f7:70:45:ed     g3    dynamic   
   72      1c:af:f7:70:72:56     g3    dynamic   
   72      48:5b:39:d6:88:ab     g3    dynamic   
   72      e8:11:32:19:4f:13     g3    dynamic   
""", 
}
    snmp_get = {}
    snmp_getnext = {}
