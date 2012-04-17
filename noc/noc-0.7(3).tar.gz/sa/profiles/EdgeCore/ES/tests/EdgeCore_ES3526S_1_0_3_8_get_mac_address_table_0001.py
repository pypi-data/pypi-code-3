# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## EdgeCore.ES.get_mac_address_table test
## Auto-generated by manage.py debug-script at 2010-12-24 18:21:01
##----------------------------------------------------------------------
## Copyright (C) 2007-2010 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------
from noc.lib.test import ScriptTestCase
class EdgeCore_ES_get_mac_address_table_Test(ScriptTestCase):
    script="EdgeCore.ES.get_mac_address_table"
    vendor="EdgeCore"
    platform='ES3526S'
    version='1.0.3.8'
    input={}
    result=[{'interfaces': ['Eth 1/2'],
  'mac': '00:12:CF:5C:A3:B9',
  'type': 'D',
  'vlan_id': 1},
 {'interfaces': ['Eth 1/2'],
  'mac': '00:12:CF:5C:A3:A0',
  'type': 'D',
  'vlan_id': 99},
 {'interfaces': ['Eth 1/2'],
  'mac': '00:17:31:0E:0F:36',
  'type': 'D',
  'vlan_id': 600},
 {'interfaces': ['Eth 1/2'],
  'mac': '00:24:8C:63:72:F8',
  'type': 'D',
  'vlan_id': 600},
 {'interfaces': ['Eth 1/4'],
  'mac': '00:12:CF:5C:AA:D9',
  'type': 'D',
  'vlan_id': 1},
 {'interfaces': ['Eth 1/4'],
  'mac': '00:12:CF:5C:AA:C0',
  'type': 'D',
  'vlan_id': 99},
 {'interfaces': ['Eth 1/4'],
  'mac': '00:1E:8C:DB:7B:96',
  'type': 'D',
  'vlan_id': 600},
 {'interfaces': ['Eth 1/4'],
  'mac': '00:1F:C6:EE:01:E9',
  'type': 'D',
  'vlan_id': 600},
 {'interfaces': ['Eth 1/6'],
  'mac': '00:12:CF:5C:AE:19',
  'type': 'D',
  'vlan_id': 1},
 {'interfaces': ['Eth 1/6'],
  'mac': '00:12:CF:5C:AE:00',
  'type': 'D',
  'vlan_id': 99},
 {'interfaces': ['Eth 1/6'],
  'mac': '00:02:02:16:A9:63',
  'type': 'D',
  'vlan_id': 100},
 {'interfaces': ['Eth 1/6'],
  'mac': '00:02:02:16:A9:F6',
  'type': 'D',
  'vlan_id': 100},
 {'interfaces': ['Eth 1/6'],
  'mac': '00:1D:60:AD:FF:B6',
  'type': 'D',
  'vlan_id': 600},
 {'interfaces': ['Eth 1/8'],
  'mac': '00:12:CF:5C:78:79',
  'type': 'D',
  'vlan_id': 1},
 {'interfaces': ['Eth 1/8'],
  'mac': '00:12:CF:5C:78:60',
  'type': 'D',
  'vlan_id': 99},
 {'interfaces': ['Eth 1/8'],
  'mac': '00:1F:33:28:7D:BE',
  'type': 'D',
  'vlan_id': 600},
 {'interfaces': ['Eth 1/9'],
  'mac': '00:12:CF:5C:AC:79',
  'type': 'D',
  'vlan_id': 1},
 {'interfaces': ['Eth 1/9'],
  'mac': '00:12:CF:5C:AC:60',
  'type': 'D',
  'vlan_id': 99},
 {'interfaces': ['Eth 1/9'],
  'mac': '00:02:02:16:A8:A1',
  'type': 'D',
  'vlan_id': 100},
 {'interfaces': ['Eth 1/9'],
  'mac': '00:02:02:16:A9:E3',
  'type': 'D',
  'vlan_id': 100},
 {'interfaces': ['Eth 1/11'],
  'mac': '00:12:CF:5C:E8:99',
  'type': 'D',
  'vlan_id': 1},
 {'interfaces': ['Eth 1/11'],
  'mac': '00:12:CF:5C:E8:80',
  'type': 'D',
  'vlan_id': 99},
 {'interfaces': ['Eth 1/11'],
  'mac': '00:02:02:16:A9:CF',
  'type': 'D',
  'vlan_id': 100},
 {'interfaces': ['Eth 1/11'],
  'mac': '00:02:02:16:AA:1F',
  'type': 'D',
  'vlan_id': 100},
 {'interfaces': ['Eth 1/11'],
  'mac': '00:18:F3:45:2E:3A',
  'type': 'D',
  'vlan_id': 600},
 {'interfaces': ['Eth 1/13'],
  'mac': '00:19:CB:55:DD:31',
  'type': 'D',
  'vlan_id': 99},
 {'interfaces': ['Eth 1/13'],
  'mac': '00:02:02:18:42:14',
  'type': 'D',
  'vlan_id': 100},
 {'interfaces': ['Eth 1/13'],
  'mac': '00:02:02:18:5E:24',
  'type': 'D',
  'vlan_id': 100},
 {'interfaces': ['Eth 1/13'],
  'mac': '00:19:CB:55:DD:31',
  'type': 'D',
  'vlan_id': 100},
 {'interfaces': ['Eth 1/13'],
  'mac': '00:22:15:48:86:38',
  'type': 'D',
  'vlan_id': 600},
 {'interfaces': ['Eth 1/14'],
  'mac': '00:12:CF:5C:AC:D9',
  'type': 'D',
  'vlan_id': 1},
 {'interfaces': ['Eth 1/14'],
  'mac': '00:12:CF:5C:AC:C0',
  'type': 'D',
  'vlan_id': 99},
 {'interfaces': ['Eth 1/14'],
  'mac': '00:02:02:16:A9:6F',
  'type': 'D',
  'vlan_id': 100},
 {'interfaces': ['Eth 1/14'],
  'mac': '00:24:1D:D8:B9:72',
  'type': 'D',
  'vlan_id': 600},
 {'interfaces': ['Eth 1/15'],
  'mac': '00:12:CF:5C:A9:99',
  'type': 'D',
  'vlan_id': 1},
 {'interfaces': ['Eth 1/15'],
  'mac': '00:12:CF:5C:A9:80',
  'type': 'D',
  'vlan_id': 99},
 {'interfaces': ['Eth 1/15'],
  'mac': '00:11:11:4F:A0:16',
  'type': 'D',
  'vlan_id': 600},
 {'interfaces': ['Eth 1/16'],
  'mac': '00:12:CF:5C:94:79',
  'type': 'D',
  'vlan_id': 1},
 {'interfaces': ['Eth 1/16'],
  'mac': '00:12:CF:5C:94:60',
  'type': 'D',
  'vlan_id': 99},
 {'interfaces': ['Eth 1/16'],
  'mac': '00:02:02:18:5B:5C',
  'type': 'D',
  'vlan_id': 100},
 {'interfaces': ['Eth 1/16'],
  'mac': '00:12:CF:04:55:F7',
  'type': 'D',
  'vlan_id': 600},
 {'interfaces': ['Eth 1/16'],
  'mac': '00:12:CF:5C:AE:40',
  'type': 'D',
  'vlan_id': 600},
 {'interfaces': ['Eth 1/16'],
  'mac': '00:12:CF:77:2E:D0',
  'type': 'D',
  'vlan_id': 600},
 {'interfaces': ['Eth 1/19'],
  'mac': '00:12:CF:5C:AD:99',
  'type': 'D',
  'vlan_id': 1},
 {'interfaces': ['Eth 1/19'],
  'mac': '00:12:CF:5C:AD:80',
  'type': 'D',
  'vlan_id': 99},
 {'interfaces': ['Eth 1/19'],
  'mac': '00:1B:FC:89:E5:28',
  'type': 'D',
  'vlan_id': 600},
 {'interfaces': ['Eth 1/20'],
  'mac': '00:12:CF:53:18:D9',
  'type': 'D',
  'vlan_id': 1},
 {'interfaces': ['Eth 1/21'],
  'mac': '00:12:CF:5C:AA:59',
  'type': 'D',
  'vlan_id': 1},
 {'interfaces': ['Eth 1/21'],
  'mac': '00:12:CF:5C:AA:40',
  'type': 'D',
  'vlan_id': 99},
 {'interfaces': ['Eth 1/22'],
  'mac': '00:02:02:18:41:10',
  'type': 'D',
  'vlan_id': 100},
 {'interfaces': ['Eth 1/22'],
  'mac': '00:19:CB:55:DB:5A',
  'type': 'D',
  'vlan_id': 100},
 {'interfaces': ['Eth 1/23'],
  'mac': '00:12:CF:5C:7A:B9',
  'type': 'D',
  'vlan_id': 1},
 {'interfaces': ['Eth 1/23'],
  'mac': '00:12:CF:5C:7A:A0',
  'type': 'D',
  'vlan_id': 99},
 {'interfaces': ['Eth 1/23'],
  'mac': '00:02:02:16:A8:14',
  'type': 'D',
  'vlan_id': 100},
 {'interfaces': ['Eth 1/23'],
  'mac': '00:02:02:18:42:6C',
  'type': 'D',
  'vlan_id': 100},
 {'interfaces': ['Eth 1/24'],
  'mac': '00:12:CF:5C:77:99',
  'type': 'D',
  'vlan_id': 1},
 {'interfaces': ['Eth 1/24'],
  'mac': '00:12:CF:5C:77:80',
  'type': 'D',
  'vlan_id': 99},
 {'interfaces': ['Eth 1/24'],
  'mac': '00:1D:0F:FD:B9:09',
  'type': 'D',
  'vlan_id': 600},
 {'interfaces': ['Eth 1/26'],
  'mac': '00:12:CF:5C:AA:A0',
  'type': 'D',
  'vlan_id': 99},
 {'interfaces': ['Eth 1/26'],
  'mac': '00:17:CB:DD:7A:45',
  'type': 'D',
  'vlan_id': 99},
 {'interfaces': ['Eth 1/26'],
  'mac': '00:19:CB:8A:36:9D',
  'type': 'D',
  'vlan_id': 99},
 {'interfaces': ['Eth 1/26'],
  'mac': '00:02:02:18:41:5B',
  'type': 'D',
  'vlan_id': 100},
 {'interfaces': ['Eth 1/26'],
  'mac': '00:02:02:18:5E:A4',
  'type': 'D',
  'vlan_id': 100},
 {'interfaces': ['Eth 1/26'],
  'mac': '00:17:CB:DD:7A:45',
  'type': 'D',
  'vlan_id': 100},
 {'interfaces': ['Eth 1/26'],
  'mac': '00:19:CB:8A:36:9D',
  'type': 'D',
  'vlan_id': 100},
 {'interfaces': ['Eth 1/26'],
  'mac': '00:0E:0C:85:65:79',
  'type': 'D',
  'vlan_id': 600},
 {'interfaces': ['Eth 1/26'],
  'mac': '00:16:EA:01:52:10',
  'type': 'D',
  'vlan_id': 600},
 {'interfaces': ['Eth 1/26'],
  'mac': '00:19:CB:8A:36:9D',
  'type': 'D',
  'vlan_id': 600},
 {'interfaces': ['Eth 1/26'],
  'mac': '00:1B:FC:90:C4:A1',
  'type': 'D',
  'vlan_id': 600},
 {'interfaces': ['Eth 1/26'],
  'mac': '00:1B:FC:90:D2:8C',
  'type': 'D',
  'vlan_id': 600},
 {'interfaces': ['Eth 1/26'],
  'mac': '00:1C:F9:E0:A8:1A',
  'type': 'D',
  'vlan_id': 600},
 {'interfaces': ['Eth 1/26'],
  'mac': '00:1F:D0:69:B3:FF',
  'type': 'D',
  'vlan_id': 600}]
    motd=' \n\n      CLI session with the ES3526S is opened.\n      To end the CLI session, enter [Exit].\n\n'
    cli={
## 'show mac-address-table'
'show mac-address-table': """show mac-address-table
 Interface Mac Address       Vlan Type
 --------- ----------------- ---- -----------------
  Eth 1/ 2 00-12-CF-5C-A3-B9    1 Learned
  Eth 1/ 2 00-12-CF-5C-A3-A0   99 Learned
  Eth 1/ 2 00-17-31-0E-0F-36  600 Learned
  Eth 1/ 2 00-24-8C-63-72-F8  600 Learned
  Eth 1/ 4 00-12-CF-5C-AA-D9    1 Learned
  Eth 1/ 4 00-12-CF-5C-AA-C0   99 Learned
  Eth 1/ 4 00-1E-8C-DB-7B-96  600 Learned
  Eth 1/ 4 00-1F-C6-EE-01-E9  600 Learned
  Eth 1/ 6 00-12-CF-5C-AE-19    1 Learned
  Eth 1/ 6 00-12-CF-5C-AE-00   99 Learned
  Eth 1/ 6 00-02-02-16-A9-63  100 Learned
  Eth 1/ 6 00-02-02-16-A9-F6  100 Learned
  Eth 1/ 6 00-1D-60-AD-FF-B6  600 Learned
  Eth 1/ 8 00-12-CF-5C-78-79    1 Learned
  Eth 1/ 8 00-12-CF-5C-78-60   99 Learned
  Eth 1/ 8 00-1F-33-28-7D-BE  600 Learned
  Eth 1/ 9 00-12-CF-5C-AC-79    1 Learned
  Eth 1/ 9 00-12-CF-5C-AC-60   99 Learned
  Eth 1/ 9 00-02-02-16-A8-A1  100 Learned
  Eth 1/ 9 00-02-02-16-A9-E3  100 Learned
  Eth 1/11 00-12-CF-5C-E8-99    1 Learned
Eth 1/11 00-12-CF-5C-E8-80   99 Learned
  Eth 1/11 00-02-02-16-A9-CF  100 Learned
  Eth 1/11 00-02-02-16-AA-1F  100 Learned
  Eth 1/11 00-18-F3-45-2E-3A  600 Learned
  Eth 1/13 00-19-CB-55-DD-31   99 Learned
  Eth 1/13 00-02-02-18-42-14  100 Learned
  Eth 1/13 00-02-02-18-5E-24  100 Learned
  Eth 1/13 00-19-CB-55-DD-31  100 Learned
  Eth 1/13 00-22-15-48-86-38  600 Learned
  Eth 1/14 00-12-CF-5C-AC-D9    1 Learned
  Eth 1/14 00-12-CF-5C-AC-C0   99 Learned
  Eth 1/14 00-02-02-16-A9-6F  100 Learned
  Eth 1/14 00-24-1D-D8-B9-72  600 Learned
  Eth 1/15 00-12-CF-5C-A9-99    1 Learned
  Eth 1/15 00-12-CF-5C-A9-80   99 Learned
  Eth 1/15 00-11-11-4F-A0-16  600 Learned
  Eth 1/16 00-12-CF-5C-94-79    1 Learned
  Eth 1/16 00-12-CF-5C-94-60   99 Learned
  Eth 1/16 00-02-02-18-5B-5C  100 Learned
  Eth 1/16 00-12-CF-04-55-F7  600 Learned
  Eth 1/16 00-12-CF-5C-AE-40  600 Learned
  Eth 1/16 00-12-CF-77-2E-D0  600 Learned
  Eth 1/19 00-12-CF-5C-AD-99    1 Learned
Eth 1/19 00-12-CF-5C-AD-80   99 Learned
  Eth 1/19 00-1B-FC-89-E5-28  600 Learned
  Eth 1/20 00-12-CF-53-18-D9    1 Learned
  Eth 1/21 00-12-CF-5C-AA-59    1 Learned
  Eth 1/21 00-12-CF-5C-AA-40   99 Learned
  Eth 1/22 00-02-02-18-41-10  100 Learned
  Eth 1/22 00-19-CB-55-DB-5A  100 Learned
  Eth 1/23 00-12-CF-5C-7A-B9    1 Learned
  Eth 1/23 00-12-CF-5C-7A-A0   99 Learned
  Eth 1/23 00-02-02-16-A8-14  100 Learned
  Eth 1/23 00-02-02-18-42-6C  100 Learned
  Eth 1/24 00-12-CF-5C-77-99    1 Learned
  Eth 1/24 00-12-CF-5C-77-80   99 Learned
  Eth 1/24 00-1D-0F-FD-B9-09  600 Learned
  Eth 1/26 00-12-CF-5C-AA-A0   99 Learned
  Eth 1/26 00-17-CB-DD-7A-45   99 Learned
  Eth 1/26 00-19-CB-8A-36-9D   99 Learned
  Eth 1/26 00-02-02-18-41-5B  100 Learned
  Eth 1/26 00-02-02-18-5E-A4  100 Learned
  Eth 1/26 00-17-CB-DD-7A-45  100 Learned
  Eth 1/26 00-19-CB-8A-36-9D  100 Learned
  Eth 1/26 00-0E-0C-85-65-79  600 Learned
  Eth 1/26 00-16-EA-01-52-10  600 Learned
Eth 1/26 00-19-CB-8A-36-9D  600 Learned
  Eth 1/26 00-1B-FC-90-C4-A1  600 Learned
  Eth 1/26 00-1B-FC-90-D2-8C  600 Learned
  Eth 1/26 00-1C-F9-E0-A8-1A  600 Learned
  Eth 1/26 00-1F-D0-69-B3-FF  600 Learned""",
}
    snmp_get={}
    snmp_getnext={}
