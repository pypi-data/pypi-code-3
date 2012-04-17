# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## DLink.DES21xx.remove_vlan test
## Auto-generated by ./noc debug-script at 2011-12-16 11:18:52
##----------------------------------------------------------------------
## Copyright (C) 2007-2011 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

## NOC modules
from noc.lib.test import ScriptTestCase


class DLink_DES21xx_remove_vlan_Test(ScriptTestCase):
    script = "DLink.DES21xx.remove_vlan"
    vendor = "DLink"
    platform = 'DES-2108'
    version = '3.00.04'
    input = {'vlan_id': 777}
    result = True
    motd = ''
    cli = {
## 'delete vlan tag 777'
'delete vlan tag 777': """delete vlan tag 777
Command:  delete vlan tag 777

SUCCESS.
""", 
## 'save'
'save': """save
Command:  save


SUCCESS
""", 
}
    snmp_get = {}
    snmp_getnext = {}
    http_get = {}
