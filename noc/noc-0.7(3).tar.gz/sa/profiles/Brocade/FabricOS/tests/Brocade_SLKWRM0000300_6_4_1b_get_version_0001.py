# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Brocade.FabricOS.get_version test
## Auto-generated by ./noc debug-script at 2011-09-22 17:25:56
##----------------------------------------------------------------------
## Copyright (C) 2007-2011 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

## NOC modules
from noc.lib.test import ScriptTestCase


class Brocade_FabricOS_get_version_Test(ScriptTestCase):
    script = "Brocade.FabricOS.get_version"
    vendor = "Brocade"
    platform = 'SLKWRM0000300'
    version = '6.4.1b'
    input = {}
    result = {'platform': 'SLKWRM0000300', 'vendor': 'Brocade', 'version': '6.4.1b'}
    motd = '\n-----------------------------------------------------------------\n'
    cli = {
## 'version'
'version': """ version
Kernel:     2.6.14.2   
Fabric OS:  v6.4.1b
Made on:    Wed Mar 2 01:39:09 2011
Flash:\t    Fri Jun 24 14:07:45 2011
BootProm:   1.0.9""", 
## 'chassisshow'
'chassisshow': """ chassisshow

POWER SUPPLY  Unit: 1\t
Time Awake:            \t42 days

FAN  Unit: 1\t
Time Awake:            \t42 days

FAN  Unit: 2\t
Time Awake:            \t42 days

FAN  Unit: 3\t
Time Awake:            \t42 days

CHASSIS/WWN  Unit: 1
Header Version:       \t2
Factory Part Num:      \t40-1000165-14
Factory Serial Num:    \tALJ2525G012
Manufacture:           \tDay: 24  Month:  5  Year: 2011
Update:                \tDay: 21  Month:  9  Year: 2011
Time Alive:            \t44 days
Time Awake:            \t42 days
ID:           \t\tBRD0000CA
Part Num:     \t\tSLKWRM0000300
Serial Num:   \t\tALJ2525G012
""", 
}
    snmp_get = {}
    snmp_getnext = {}
