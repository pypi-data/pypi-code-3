# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Zyxel.ZyNOS.ping test
## Auto-generated by ./noc debug-script at 2011-12-27 14:54:39
##----------------------------------------------------------------------
## Copyright (C) 2007-2011 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

## NOC modules
from noc.lib.test import ScriptTestCase


class Zyxel_ZyNOS_ping_Test(ScriptTestCase):
    script = "Zyxel.ZyNOS.ping"
    vendor = "Zyxel"
    platform = 'ES-2108-G'
    version = '3.80(ABL.0)'
    input = {'address': '91.90.32.241', 'size': 1250}
    result = {'avg': 0, 'count': 6, 'max': 10, 'min': 0, 'success': 6}
    motd = ' ********\nCopyright (c) 1994 - 2007 ZyXEL Communications Corp.\n'
    cli = {
## 'ping 91.90.32.241 size 1250'
'ping 91.90.32.241 size 1250': """ ping 91.90.32.241 size 1250
Resolving 91.90.32.241... 91.90.32.241
 sent  rcvd  rate    rtt     avg    mdev     max     min  reply from
    1     1  100       0       0       0       0       0  91.90.32.241
    2     2  100      10       1       3      10       0  91.90.32.241
    3     3  100       0       1       3      10       0  91.90.32.241""", 
}
    snmp_get = {}
    snmp_getnext = {}
