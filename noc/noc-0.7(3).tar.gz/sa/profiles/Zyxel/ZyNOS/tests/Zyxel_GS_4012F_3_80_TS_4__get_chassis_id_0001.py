# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Zyxel.ZyNOS.get_chassis_id test
## Auto-generated by manage.py debug-script at 2010-10-11 10:36:00
##----------------------------------------------------------------------
## Copyright (C) 2007-2010 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------
from noc.lib.test import ScriptTestCase
class Zyxel_ZyNOS_get_chassis_id_Test(ScriptTestCase):
    script="Zyxel.ZyNOS.get_chassis_id"
    vendor="Zyxel"
    platform='GS-4012F'
    version='3.80(TS.4)'
    input={}
    result='00:13:49:F2:AD:27'
    motd=' **********\nCopyright (c) 1994 - 2008 ZyXEL Communications Corp.\n'
    cli={
## 'show system-information'
'show system-information': """ show system-information

System Name\t\t: Switch1
System Contact\t\t: root@example.com
System Location\t\t: Location1
Ethernet Address\t: 00:13:49:f2:ad:27
ZyNOS F/W Version\t: V3.80(TS.4) | 10/07/2008
RomRasSize\t\t: 3191378 
System up Time\t\t:  1415:04:00 (1e5d31a3 ticks)
Bootbase Version\t: V3.0 | 04/08/2005
ZyNOS CODE\t\t: RAS Oct  6 2008 17:28:42
Product Model\t\t: GS-4012F""",
}
    snmp_get={}
    snmp_getnext={}
