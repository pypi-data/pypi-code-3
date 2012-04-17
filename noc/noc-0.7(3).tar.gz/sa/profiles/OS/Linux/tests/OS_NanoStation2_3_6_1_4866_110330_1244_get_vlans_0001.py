# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## OS.Linux.get_vlans test
## Auto-generated by ./noc debug-script at 2011-11-02 19:29:14
##----------------------------------------------------------------------
## Copyright (C) 2007-2011 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

## NOC modules
from noc.lib.test import ScriptTestCase


class OS_Linux_get_vlans_Test(ScriptTestCase):
    script = "OS.Linux.get_vlans"
    vendor = "OS"
    platform = 'NanoStation2'
    version = '3.6.1.4866.110330.1244'
    input = {}
    result = [{'name': 'br998', 'vlan_id': 998},
 {'name': 'br111', 'vlan_id': 111},
 {'name': 'br140', 'vlan_id': 140},
 {'name': 'br146', 'vlan_id': 146}]
    motd = "\n\nBusyBox v1.01 (2011.03.30-09:47+0000) Built-in shell (ash)\nEnter 'help' for a list of built-in commands.\n\n"
    cli = {
## 'cat /proc/net/vlan/config'
'cat /proc/net/vlan/config': """cat /proc/net/vlan/config
VLAN Dev name\t | VLAN ID
Name-Type: VLAN_NAME_TYPE_RAW_PLUS_VID_NO_PAD
eth0.998       | 998  | eth0
eth0.111       | 111  | eth0
eth0.140       | 140  | eth0
eth0.146       | 146  | eth0
ath0.998       | 998  | ath0
ath0.111       | 111  | ath0
ath0.140       | 140  | ath0
ath0.146       | 146  | ath0""", 
'export LANG=en_GB.UTF-8':  'export LANG=en_GB.UTF-8\n', 
}
    snmp_get = {}
    snmp_getnext = {}
