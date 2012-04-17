# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Juniper.JUNOS.get_version test
## Auto-generated by ./noc debug-script at 2011-10-25 00:06:32
##----------------------------------------------------------------------
## Copyright (C) 2007-2011 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

## NOC modules
from noc.lib.test import ScriptTestCase


class Juniper_JUNOS_get_version_Test(ScriptTestCase):
    script = "Juniper.JUNOS.get_version"
    vendor = "Juniper"
    platform = 'mx80'
    version = '11.1R3.5'
    input = {}
    result = {'platform': 'mx80', 'vendor': 'Juniper', 'version': '11.1R3.5'}
    motd = '--- JUNOS 11.1R3.5 built 2011-06-25 01:24:42 UTC\n'
    cli = {
'set cli screen-length 0':  ' set cli screen-length 0 \nScreen length set to 0\n\n', 
## 'show version'
'show version': """ show version 
Model: mx80
JUNOS Base OS boot [11.1R3.5]
JUNOS Base OS Software Suite [11.1R3.5]
JUNOS Kernel Software Suite [11.1R3.5]
JUNOS Crypto Software Suite [11.1R3.5]
JUNOS Packet Forwarding Engine Support (MX80) [11.1R3.5]
JUNOS Online Documentation [11.1R3.5]
JUNOS Routing Software Suite [11.1R3.5]
""", 
}
    snmp_get = {}
    snmp_getnext = {}
