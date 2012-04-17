# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## DLink.DxS.get_version test
## Auto-generated by manage.py debug-script at 2010-11-19 18:19:54
##----------------------------------------------------------------------
## Copyright (C) 2007-2010 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------
from noc.lib.test import ScriptTestCase
class DLink_DxS_get_version_Test(ScriptTestCase):
   script="DLink.DxS.get_version"
   vendor="DLink"
   platform='DES-3528'
   version='2.11.B020'
   input={}
   result={'attributes': {'Boot PROM': '1.00.B007',
                 'HW version': 'A1',
                 'Serial Number': 'P1UM188000211'},
'platform': 'DES-3528', 'vendor': 'DLink', 'version': '2.11.B020'}
   motd=' \n\n                        DES-3528 Fast Ethernet Switch\n Command Line Interface\n\n Firmware: Build 2.11.B020\n           Copyright(C) 2008 D-Link Corporation. All rights reserved.\n\n'
   cli={
## 'show switch'
'show switch': """show switch
Command: show switch

Device Type       : DES-3528 Fast Ethernet Switch
MAC Address       : 00-21-91-B0-30-50
IP Address        : 10.109.28.1 (Manual)
VLAN Name         : nik_sh
Subnet Mask       : 255.255.252.0
Default Gateway   : 10.109.28.2
Boot PROM Version : Build 1.00.B007
Firmware Version  : Build 2.11.B020
Hardware Version  : A1
Serial Number     : P1UM188000211
System Name       :
System Location   : Nick. Shosse
System Contact    :
Spanning Tree     : Disabled
GVRP              : Disabled
IGMP Snooping     : Disabled
MLD Snooping      : Disabled
VLAN Trunk        : Disabled
TELNET            : Disabled
WEB               : Enabled (TCP 80)
SNMP              : Enabled
SSL Status        : Disabled
SSH Status        : Enabled
802.1x            : Disabled
Jumbo Frame       : Off
Clipaging         : Disabled
MAC Notification  : Disabled
Port Mirror       : Disabled
SNTP              : Enabled
HOL Prevention State : Enabled
Syslog Global State  : Enabled
Single IP Management : Disabled
Dual Image           : Supported
Password Encryption Status : Enabled
""",
## 'disable clipaging'
'disable clipaging': """disable clipaging
Command: disable clipaging

Success.
""",
}
   snmp_get={}
   snmp_getnext={}
