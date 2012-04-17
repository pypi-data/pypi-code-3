# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Eltex.MES.remove_vlan test
## Auto-generated by ./noc debug-script at 2011-10-31 16:54:59
##----------------------------------------------------------------------
## Copyright (C) 2007-2011 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

## NOC modules
from noc.lib.test import ScriptTestCase


class Eltex_MES_remove_vlan_Test(ScriptTestCase):
    script = "Eltex.MES.remove_vlan"
    vendor = "Eltex"
    platform = 'MES-3124F'
    version = '2.1.7'
    input = {'vlan_id': 777}
    result = True
    motd = '*****\n\n'
    cli = {
'':  '\n', 
'end':  'end\n', 
'configure':  'configure\n', 
## 'show vlan'
'show vlan': """show vlan

Vlan       Name                   Ports                Type     Authorization 
---- ----------------- --------------------------- ------------ ------------- 
 1           1              gi0/1-24,te0/1-4         Default      Required    
 53  area_Lermontova8       gi0/1-24,te0/1-4        permanent     Required    
111     commutators         gi0/1-24,te0/1-4        permanent     Required    
777        Test               gi0/13,te0/2          permanent     Required    
""", 
'vlan database':  'vlan database\n', 
'no vlan 777':  'no vlan 777\n', 
'terminal datadump':  'terminal datadump\n', 
'copy running-config startup-config':  'copy running-config startup-config\nOverwrite file [startup-config] ?....Copy succeeded\n', 
}
    snmp_get = {}
    snmp_getnext = {}
