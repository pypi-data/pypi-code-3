# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## DLink.DES21xx.get_interface_status test
## Auto-generated by ./noc debug-script at 2011-12-16 11:03:48
##----------------------------------------------------------------------
## Copyright (C) 2007-2011 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

## NOC modules
from noc.lib.test import ScriptTestCase


class DLink_DES21xx_get_interface_status_Test(ScriptTestCase):
    script = "DLink.DES21xx.get_interface_status"
    vendor = "DLink"
    platform = 'DES-2108'
    version = '5.01.00'
    input = {}
    result = [{'interface': '1', 'status': True},
 {'interface': '2', 'status': True},
 {'interface': '3', 'status': True},
 {'interface': '4', 'status': True},
 {'interface': '5', 'status': True},
 {'interface': '6', 'status': False},
 {'interface': '7', 'status': False},
 {'interface': '8', 'status': True}]
    motd = ''
    cli = {
## 'show ports '
'show ports ': """show ports 
Command:  show ports 


PORT STATUS:
ID       Speed    Flow_Control       QOS    Link_Status
-------------------------------------------------------
01        Auto         Disable    Medium      100M Full
02        Auto         Disable    Medium      100M Full
03        Auto         Disable    Medium      100M Full
04        Auto         Disable    Medium       10M Full
05        Auto         Disable    Medium      100M Full
06        Auto         Disable    Medium           Down
07        Auto         Disable    Medium           Down
08        Auto         Disable    Medium      100M Full
""", 
}
    snmp_get = {}
    snmp_getnext = {}
    http_get = {}
