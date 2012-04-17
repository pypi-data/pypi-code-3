# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## DLink.DVG.get_version test
## Auto-generated by ./noc debug-script at 2011-12-05 12:02:31
##----------------------------------------------------------------------
## Copyright (C) 2007-2011 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

## NOC modules
from noc.lib.test import ScriptTestCase


class DLink_DVG_get_version_Test(ScriptTestCase):
    script = "DLink.DVG.get_version"
    vendor = "DLink"
    platform = 'DVG-2102S'
    version = '1.02.38.39.1651'
    input = {}
    result = {'platform': 'DVG-2102S', 'vendor': 'DLink', 'version': '1.02.38.39.1651'}
    motd = ' \nPlease Wait ...\nSystem Ready\n\n<< Command Line Interface V 2.1.7.5 >>\n\nEnter HELP for usage\n\n[[/]]\n'
    cli = {
## 'GET STATUS HARDWARE'
'GET STATUS HARDWARE': """GET STATUS HARDWARE
==================== Hardware Status
Hardware [DSA]
Driver [0.10.37.1.118 16/Jun/2009]
DSP [481]
Software [GE_1.00 == Ver(1.02.38.39.1651 2009/07/07 14:14:18) PId(282.DLink.l2tp.DualAccess.MultiServer.NoPrefix.TR069.drtp) Drv(0.10.37.1) Hw(DSA) == ]
[[/]]""", 
}
    snmp_get = {}
    snmp_getnext = {}
