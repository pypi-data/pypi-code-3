# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## DLink.DxS.get_chassis_id test
## Auto-generated by manage.py debug-script at 2011-03-29 12:15:58
##----------------------------------------------------------------------
## Copyright (C) 2007-2011 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------
from noc.lib.test import ScriptTestCase
class DLink_DxS_get_chassis_id_Test(ScriptTestCase):
    script="DLink.DxS.get_chassis_id"
    vendor="DLink"
    platform='DGS-3120-24TC'
    version='1.01.B033'
    input={}
    result='5C:D9:98:3F:A0:E9'
    motd='**********\n\n'
    cli={
## 'show switch'
'show switch': """show switch
Command: show switch

Device Type                : DGS-3120-24TC Gigabit Ethernet Switch
Unit ID                    : 1
MAC Address                : 5C-D9-98-3F-A0-E9
IP Address                 : 172.16.13.4 (Manual)
VLAN Name                  : srv_int
Subnet Mask                : 255.255.255.0
Default Gateway            : 172.16.13.1
Boot PROM Version          : Build 1.00.007
Firmware Version           : Build 1.01.B033
Hardware Version           : A1
Firmware Type              : EI
Serial Number              : P4UV1A9000301
System Name                : 
System Location            : 
System Uptime              : 28 days, 19 hours, 38 minutes, 34 seconds
System Contact             : 
Spanning Tree              : Disabled
GVRP                       : Disabled
IGMP Snooping              : Disabled
MLD Snooping               : Disabled
VLAN Trunk                 : Disabled
Telnet                     : Enabled (TCP 23)
Web                        : Disabled
SNMP                       : Disabled
SSL Status                 : Disabled
SSH Status                 : Disabled
802.1x                     : Disabled
Jumbo Frame                : Off
CLI Paging                 : Disabled
MAC Notification           : Disabled
Port Mirror                : Disabled
SNTP                       : Disabled
HOL Prevention State       : Enabled
Syslog Global State        : Disabled
Single IP Management       : Disabled
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
