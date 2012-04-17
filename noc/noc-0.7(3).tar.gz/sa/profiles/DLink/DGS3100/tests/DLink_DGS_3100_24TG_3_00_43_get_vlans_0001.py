# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## DLink.DGS3100.get_vlans test
## Auto-generated by ./noc debug-script at 2011-10-14 12:42:05
##----------------------------------------------------------------------
## Copyright (C) 2007-2011 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

## NOC modules
from noc.lib.test import ScriptTestCase


class DLink_DGS3100_get_vlans_Test(ScriptTestCase):
    script = "DLink.DGS3100.get_vlans"
    vendor = "DLink"
    platform = 'DGS-3100-24TG'
    version = '3.00.43'
    input = {}
    result = [{'name': 'default', 'vlan_id': 1},
 {'name': 'users', 'vlan_id': 13},
 {'name': 'sv_upr', 'vlan_id': 14},
 {'name': 'privat', 'vlan_id': 254},
 {'name': 'upr', 'vlan_id': 256}]
    motd = '******\n\n'
    cli = {
## 'show vlan'
'show vlan': """ show vlan

VID             : 1            VLAN Name    : default
VLAN TYPE       : other       
Member ports    : 1:(2-24),2:(1-24)
Static ports    : 1:(2-24),2:(1-24)
Untagged ports  : 1:(2-24),2:(1-24)
Forbidden ports : 

VID             : 13           VLAN Name    : users
VLAN TYPE       : static      
Member ports    : 1:(1-24),2:(1-24)
Static ports    : 1:(1-24),2:(1-24)
Untagged ports  : 
Forbidden ports : 

VID             : 14           VLAN Name    : sv_upr
VLAN TYPE       : static      
Member ports    : 1:(1-8,10-24),2:(1-24)
Static ports    : 1:(1-8,10-24),2:(1-24)
Untagged ports  : 1:1
Forbidden ports : 

                                                                                                                    VID             : 254          VLAN Name    : privat
VLAN TYPE       : static      
Member ports    : 1:(2,9,15)
Static ports    : 1:(2,9,15)
Untagged ports  : 
Forbidden ports : 

VID             : 256          VLAN Name    : upr
VLAN TYPE       : static      
Member ports    : 1:9
Static ports    : 1:9
Untagged ports  : 
Forbidden ports : 

Total Entries : 5
""", 
}
    snmp_get = {}
    snmp_getnext = {}
