# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Cisco.IOS.get_mac_address_table test
## Auto-generated by manage.py debug-script at 2010-09-29 01:35:24
##----------------------------------------------------------------------
## Copyright (C) 2007-2010 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------
from noc.lib.test import ScriptTestCase
class Cisco_IOS_get_mac_address_table_Test(ScriptTestCase):
    script="Cisco.IOS.get_mac_address_table"
    vendor="Cisco"
    platform='s72033_rp'
    version='12.2(33)SXH2a'
    input={}
    result=[
        {'mac': '00:14:4F:D2:44:2E', 'type': 'D', 'interfaces': ['Te 1/1'], 'vlan_id': 2},
        {'mac': '00:1B:24:93:37:09', 'type': 'D', 'interfaces': ['Te 1/1'], 'vlan_id': 3},
        {'mac': '00:16:36:E0:7F:C4', 'type': 'D', 'interfaces': ['Te 1/1'], 'vlan_id': 3},
        {'mac': '00:1E:68:2F:47:4A', 'type': 'D', 'interfaces': ['Te 1/1'], 'vlan_id': 4},
        {'mac': '00:14:4F:9E:69:C6', 'type': 'D', 'interfaces': ['Te 1/1'], 'vlan_id': 5},
        {'mac': '00:14:4F:9A:7A:08', 'type': 'D', 'interfaces': ['Te 1/1'], 'vlan_id': 6},
        {'mac': '00:0D:93:9E:3E:BA', 'type': 'D', 'interfaces': ['Te 1/1'], 'vlan_id': 6},
        {'mac': '00:14:4F:D2:55:0A', 'type': 'D', 'interfaces': ['Te 1/1'], 'vlan_id': 7},
        {'mac': '00:14:4F:01:FE:06', 'type': 'D', 'interfaces': ['Te 1/1'], 'vlan_id': 7},
        {'mac': '00:14:4F:9E:FB:3E', 'type': 'D', 'interfaces': ['Te 1/1'], 'vlan_id': 8},
        {'mac': '00:01:D7:81:46:13', 'type': 'D', 'interfaces': ['Po 2'], 'vlan_id': 14},
        {'mac': '00:21:28:6A:D8:EC', 'type': 'D', 'interfaces': ['Te 1/1'], 'vlan_id': 21}] 
    motd=' \n\n'
    cli={
## 'show mac address-table'
'show mac address-table': """show mac address-table
Legend: * - primary entry
        age - seconds since last seen
        n/a - not available

  vlan   mac address     type    learn     age              ports
------+----------------+--------+-----+----------+--------------------------
*    2  0014.4fd2.442e   dynamic  Yes        155   Te1/1
*    3  001b.2493.3709   dynamic  Yes          5   Te1/1
*    3  0016.36e0.7fc4   dynamic  Yes          0   Te1/1
*    4  001e.682f.474a   dynamic  Yes          0   Te1/1
*    5  0014.4f9e.69c6   dynamic  Yes        210   Te1/1
*    6  0014.4f9a.7a08   dynamic  Yes          0   Te1/1
*    6  000d.939e.3eba   dynamic  Yes          0   Te1/1
*    7  0014.4fd2.550a   dynamic  Yes        230   Te1/1
*    7  0014.4f01.fe06   dynamic  Yes          0   Te1/1
*    8  0014.4f9e.fb3e   dynamic  Yes        145   Te1/1
*    9  3333.0000.0016    static  Yes          -   Switch,Stby-Switch
*   10  3333.0000.0016    static  Yes          -   Switch,Stby-Switch
*   11  3333.0000.0016    static  Yes          -   Switch,Stby-Switch
*   12  3333.0000.0016    static  Yes          -   Switch,Stby-Switch
*   13  0019.07da.ac00    static  No           -   Router
*   14  0001.d781.4613   dynamic  Yes          0   Po2
*   15  3333.0000.000d    static  Yes          -   Te1/1,Te1/3,Te1/4,Te2/1
                                                   Gi7/2,Gi7/3,Gi7/5,Gi7/6
                                                   Gi7/13,Gi7/14,Gi7/15,Gi7/16
                                                   Gi7/17,Gi7/18,Po2,Po3,Po5
                                                   Router,Switch
*   16  3333.0000.000d    static  Yes          -   Te1/1,Te1/3,Te1/4,Te2/1
                                                   Gi7/2,Gi7/3,Gi7/5,Gi7/6
                                                   Gi7/13,Gi7/14,Gi7/15,Gi7/16
                                                   Gi7/17,Gi7/18,Po2,Po3,Po5
                                                   Router,Switch
*   17  3333.0000.0016    static  Yes          -   Switch,Stby-Switch
*   18  3333.0000.0016    static  Yes          -   Switch,Stby-Switch
*   19  3333.0000.0016    static  Yes          -   Switch,Stby-Switch
*   20  3333.0000.0016    static  Yes          -   Switch,Stby-Switch
*   21  0021.286a.d8ec   dynamic  Yes         15   Te1/1
""",
'terminal length 0':  'terminal length 0\n',
}
    snmp_get={}
    snmp_getnext={}
