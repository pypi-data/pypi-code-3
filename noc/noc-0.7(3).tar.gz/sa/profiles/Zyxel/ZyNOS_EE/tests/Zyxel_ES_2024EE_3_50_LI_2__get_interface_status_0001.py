# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Zyxel.ZyNOS_EE.get_interface_status test
## Auto-generated by ./noc debug-script at 2011-11-29 18:19:57
##----------------------------------------------------------------------
## Copyright (C) 2007-2011 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

## NOC modules
from noc.lib.test import ScriptTestCase


class Zyxel_ZyNOS_EE_get_interface_status_Test(ScriptTestCase):
    script = "Zyxel.ZyNOS_EE.get_interface_status"
    vendor = "Zyxel"
    platform = 'ES-2024EE'
    version = '3.50(LI.2)'
    input = {'interface': '25'}
    result = [{'interface': '25', 'status': True}]
    motd = '****\nCopyright (c) 1994 - 2004 ZyXEL Communications Corp.\n'
    cli = {
## 'sys sw portstatus'
'sys sw portstatus': """sys sw portstatus
PORT  EN  LINK  SPEED/DUPLEX  AUTO    FLWCTRL
 1    1   1     100/FULL      AUTO    -------
 2    1   1     100/FULL      AUTO    -------
 3    1   1     100/FULL      AUTO    -------
 4    1   0     100/FULL      AUTO    -------
 5    1   0     100/FULL      AUTO    -------
 6    1   0     100/FULL      AUTO    -------
 7    1   0     100/FULL      AUTO    -------
 8    0   0     100/FULL      AUTO    -------
 9    1   1     100/FULL      AUTO    -------
10    1   0     100/FULL      AUTO    -------
11    1   0     100/FULL      AUTO    -------
12    1   1     100/FULL      AUTO    -------
13    1   1     100/FULL      AUTO    -------
14    1   1     100/FULL      AUTO    -------
15    1   0     100/FULL      AUTO    -------
16    1   0     100/FULL      AUTO    -------
17    1   0     100/FULL      AUTO    -------
18    1   0     100/FULL      AUTO    -------
19    1   0     100/FULL      AUTO    -------
20    1   0     100/FULL      AUTO    -------
21    1   0     100/FULL      AUTO    -------
22    1   0     100/FULL      AUTO    -------
23    1   0     100/FULL      AUTO    -------
24    1   0     100/FULL      AUTO    -------
25    1   1     1000/FULL     FORCE   -------
26    0   0     100/FULL      AUTO    -------""", 
}
    snmp_get = {}
    snmp_getnext = {}
