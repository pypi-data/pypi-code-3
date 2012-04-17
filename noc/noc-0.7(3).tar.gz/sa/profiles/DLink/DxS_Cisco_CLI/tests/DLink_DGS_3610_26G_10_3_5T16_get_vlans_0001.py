# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## DLink.DxS_Cisco_CLI.get_vlans test
## Auto-generated by manage.py debug-script at 2011-02-09 15:38:34
##----------------------------------------------------------------------
## Copyright (C) 2007-2011 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------
from noc.lib.test import ScriptTestCase
class DLink_DxS_Cisco_CLI_get_vlans_Test(ScriptTestCase):
    script="DLink.DxS_Cisco_CLI.get_vlans"
    vendor="DLink"
    platform='DGS-3610-26G'
    version='10.3(5T16)'
    input={}
    result=[{'name': 'VLAN0001', 'vlan_id': 1}, {'name': 'vlan_2', 'vlan_id': 2}]
    motd='\n\n'
    cli={
'terminal length 0':  'terminal length 0\n',
## 'show vlan'
'show vlan': """show vlan
VLAN Name                             Status    Ports     
---- -------------------------------- --------- -----------------------------------
   1 VLAN0001                         STATIC    Gi0/1, Gi0/2, Gi0/3, Gi0/4            
                                                Gi0/5, Gi0/6, Gi0/7, Gi0/8            
                                                Gi0/9, Gi0/10, Gi0/11, Gi0/12         
                                                Gi0/13, Gi0/14, Gi0/15, Gi0/16        
                                                Gi0/17, Gi0/18, Gi0/19, Gi0/20        
                                                Gi0/21, Gi0/22, Gi0/23, Gi0/24        
   2 vlan_2                           STATIC    Gi0/23                                """,
}
    snmp_get={}
    snmp_getnext={}
