# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Cisco.IOS.get_mac_address_table test
## Auto-generated by manage.py debug-script at 2010-09-29 01:41:17
##----------------------------------------------------------------------
## Copyright (C) 2007-2010 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------
from noc.lib.test import ScriptTestCase
class Cisco_IOS_get_mac_address_table_Test(ScriptTestCase):
    script="Cisco.IOS.get_mac_address_table"
    vendor="Cisco"
    platform='s72033_rp'
    version='12.2(18)SXF14'
    input={}
    result=[
        {'mac': '00:14:4F:D2:44:2E', 'type': 'D', 'interfaces': ['Te 9/1'], 'vlan_id': 166},
        {'mac': '00:14:4F:49:E1:72', 'type': 'D', 'interfaces': ['Gi 11/20'], 'vlan_id': 105},
        {'mac': '00:1B:24:93:37:09', 'type': 'D', 'interfaces': ['Te 10/3'], 'vlan_id': 126},
        {'mac': '00:14:4F:49:DB:32', 'type': 'D', 'interfaces': ['Te 10/1'], 'vlan_id': 111},
        {'mac': '00:16:36:E0:7F:C4', 'type': 'D', 'interfaces': ['Te 10/4'], 'vlan_id': 136},
        {'mac': '00:1E:68:2F:47:4A', 'type': 'D', 'interfaces': ['Te 9/1'], 'vlan_id': 136},
        {'mac': '00:14:4F:9E:69:C6', 'type': 'D', 'interfaces': ['Gi 11/12'], 'vlan_id': 107},
        {'mac': '00:14:4F:9A:7A:08', 'type': 'D', 'interfaces': ['Te 10/3'], 'vlan_id': 110},
        {'mac': '00:0D:93:9E:3E:BA', 'type': 'D', 'interfaces': ['Gi 11/14'], 'vlan_id': 117},
        {'mac': '00:14:4F:D2:55:0A', 'type': 'D', 'interfaces': ['Te 9/1'], 'vlan_id': 164},
        {'mac': '00:14:4F:9E:F9:99', 'type': 'D', 'interfaces': ['Gi 11/12'], 'vlan_id': 144},
        {'mac': '00:14:4F:EE:0D:18', 'type': 'D', 'interfaces': ['Te 9/1'], 'vlan_id': 114},
        {'mac': '00:14:4F:CD:85:39', 'type': 'D', 'interfaces': ['Te 9/1'], 'vlan_id': 140},
        {'mac': '00:14:4F:CD:B1:03', 'type': 'D', 'interfaces': ['Te 9/1'], 'vlan_id': 159},
        {'mac': '00:15:17:A6:3E:16', 'type': 'D', 'interfaces': ['Te 9/2'], 'vlan_id': 112}]
    motd=' \n\n'
    cli={
## 'show mac-address-table'
'show mac-address-table': """show mac-address-table
Legend: * - primary entry
        age - seconds since last seen
        n/a - not available

  vlan   mac address     type    learn     age              ports
------+----------------+--------+-----+----------+--------------------------
*  166  0014.4fd2.442e   dynamic  Yes          0   Te9/1
*  105  0014.4f49.e172   dynamic  Yes          0   Gi11/20
*  126  001b.2493.3709   dynamic  Yes          0   Te10/3
*  111  0014.4f49.db32   dynamic  Yes          0   Te10/1
*  136  0016.36e0.7fc4   dynamic  Yes          0   Te10/4
*  136  001e.682f.474a   dynamic  Yes          0   Te9/1
*  107  0014.4f9e.69c6   dynamic  Yes         50   Gi11/12
*  110  0014.4f9a.7a08   dynamic  Yes          0   Te10/3
*  117  000d.939e.3eba   dynamic  Yes          0   Gi11/14
*  164  0014.4fd2.550a   dynamic  Yes         35   Te9/1
*  144  0014.4f9e.f999   dynamic  Yes         55   Gi11/12
*  114  0014.4fee.0d18   dynamic  Yes          0   Te9/1
*  140  0014.4fcd.8539   dynamic  Yes        120   Te9/1
*  159  0014.4fcd.b103   dynamic  Yes          0   Te9/1
*  101  3333.0000.0001    static  Yes          -   Switch,Stby-Switch
*  100  3333.0000.0001    static  Yes          -   Switch,Stby-Switch
*  103  3333.0000.0001    static  Yes          -   Switch,Stby-Switch
*  102  3333.0000.0001    static  Yes          -   Switch,Stby-Switch
*  103  3333.0000.000d    static  Yes          -   Gi1/1,Gi1/2,Gi1/3,Gi1/4
                                                   Gi2/1,Gi2/2,Gi2/3,Gi2/4
                                                   Gi2/5,Gi2/6,Te9/1,Te9/2
                                                   Te10/1,Te10/2,Te10/3,Te10/4
                                                   Gi11/3,Gi11/4,Gi11/5,Gi11/6
                                                   Gi11/7,Gi11/8,Gi11/11,Gi11/12
                                                   Gi11/13,Gi11/14,Gi11/15
                                                   Gi11/16,Gi11/17,Gi11/19
                                                   Gi11/20,Gi11/21,Gi11/22
                                                   Gi11/23,Gi11/24,Gi11/25
                                                   Gi11/26,Gi11/27,Gi11/28
                                                   Gi11/29,Gi11/30,Gi11/31
                                                   Gi11/32,Gi11/34,Gi11/36
                                                   Gi11/37,Gi11/38,Gi11/39
                                                   Gi11/40,Gi11/41,Gi11/42
                                                   Gi11/43,Gi11/44,Gi11/45
                                                   Gi11/46,Gi11/47,Po271,Po257
                                                   Router,Switch
*  112  0015.17a6.3e16   dynamic  Yes          0   Te9/2
*   53  3333.0000.0016    static  Yes          -   Switch,Stby-Switch
*   50  3333.0000.0016    static  Yes          -   Switch,Stby-Switch
*   51  3333.0000.0016    static  Yes          -   Switch,Stby-Switch

""",
## 'show mac address-table'
'show mac address-table': """show mac address-table
                   ^
% Invalid input detected at '^' marker.
""",
'terminal length 0':  'terminal length 0\n',
}
    snmp_get={}
    snmp_getnext={}
