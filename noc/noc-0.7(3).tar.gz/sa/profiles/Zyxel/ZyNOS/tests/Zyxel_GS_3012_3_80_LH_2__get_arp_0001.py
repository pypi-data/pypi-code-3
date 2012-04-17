# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Zyxel.ZyNOS.get_arp test
## Auto-generated by ./noc debug-script at 2011-07-01 17:07:55
##----------------------------------------------------------------------
## Copyright (C) 2007-2011 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

## NOC modules
from noc.lib.test import ScriptTestCase


class Zyxel_ZyNOS_get_arp_Test(ScriptTestCase):
    script = "Zyxel.ZyNOS.get_arp"
    vendor = "Zyxel"
    platform = 'GS-3012'
    version = '3.80(LH.2)'
    input = {}
    result = [{'interface': '100', 'ip': '127.0.0.1', 'mac': '00:A0:C5:FB:53:CA'},
 {'interface': '100', 'ip': '192.168.25.129', 'mac': '00:1B:11:1C:23:41'}]
    motd = ' ****\nCopyright (c) 1994 - 2008 ZyXEL Communications Corp.\n'
    cli = {
## 'show ip arp'
'show ip arp': """ show ip arp
  Index   IP               MAC                VLAN  Age(s)  Type
     1    127.0.0.1        00:a0:c5:fb:53:ca   100   295    dynamic
     2    192.168.25.129   00:1b:11:1c:23:41   100   300    dynamic""", 
}
    snmp_get = {}
    snmp_getnext = {}
