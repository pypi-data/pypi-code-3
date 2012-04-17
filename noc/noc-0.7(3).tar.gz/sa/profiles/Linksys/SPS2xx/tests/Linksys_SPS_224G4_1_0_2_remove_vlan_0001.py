# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Linksys.SPS2xx.remove_vlan test
## Auto-generated by ./noc debug-script at 2011-11-21 15:24:06
##----------------------------------------------------------------------
## Copyright (C) 2007-2011 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

## NOC modules
from noc.lib.test import ScriptTestCase


class Linksys_SPS2xx_remove_vlan_Test(ScriptTestCase):
    script = "Linksys.SPS2xx.remove_vlan"
    vendor = "Linksys"
    platform = 'SPS-224G4'
    version = '1.0.2'
    input = {'vlan_id': 777}
    result = True
    motd = '*******\n\n'
    cli = {
'':  '\n', 
'end':  'end\n', 
'configure':  'configure\n', 
## 'show vlan'
'show vlan': """show vlan

Vlan       Name                   Ports                Type     Authorization 
---- ----------------- --------------------------- ------------ ------------- 
 1           1               g(3-4),ch(1-8)           other       Required    
 72   area_SmileLink         e(2-24),g(1-4)         permanent     Required    
111     commutators              g(3-4)             permanent     Required    
140       clients               e1,g(3-4)           permanent     Required    
777        Test                e(10-11),g1          permanent     Required    
""", 
'vlan database':  'vlan database\n', 
'no vlan 777':  'no vlan 777\n', 
'terminal datadump':  'terminal datadump\n', 
'copy running-config startup-config':  'copy running-config startup-config\nCopy succeeded\n', 
}
    snmp_get = {}
    snmp_getnext = {}
