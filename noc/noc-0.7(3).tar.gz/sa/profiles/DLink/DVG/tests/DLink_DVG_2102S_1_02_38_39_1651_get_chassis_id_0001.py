# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## DLink.DVG.get_chassis_id test
## Auto-generated by ./noc debug-script at 2011-12-05 12:06:53
##----------------------------------------------------------------------
## Copyright (C) 2007-2011 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

## NOC modules
from noc.lib.test import ScriptTestCase


class DLink_DVG_get_chassis_id_Test(ScriptTestCase):
    script = "DLink.DVG.get_chassis_id"
    vendor = "DLink"
    platform = 'DVG-2102S'
    version = '1.02.38.39.1651'
    input = {}
    result = '00:24:01:54:E1:0D'
    motd = ' \nPlease Wait ...\nSystem Ready\n\n<< Command Line Interface V 2.1.7.5 >>\n\nEnter HELP for usage\n\n[[/]]\n'
    cli = {
## 'GET STATUS WAN'
'GET STATUS WAN': """GET STATUS WAN
WAN MAC [00240154E10D]
WAN IP [10.8.7.41]
WAN Netmask [255.255.255.0]
WAN Default Gateway [10.8.7.1]
WAN Primary DNS [80.237.81.250]
WAN Secondary DNS [62.33.189.250]
[[/]]""", 
}
    snmp_get = {}
    snmp_getnext = {}
