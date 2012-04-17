# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Juniper.JUNOS.get_version test
## Auto-generated by manage.py debug-script at 2010-09-23 00:26:34
##----------------------------------------------------------------------
## Copyright (C) 2007-2010 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------
from noc.lib.test import ScriptTestCase
class Juniper_JUNOS_get_version_Test(ScriptTestCase):
    script="Juniper.JUNOS.get_version"
    vendor="Juniper"
    platform='mx480'
    version='9.6R1.13'
    input={}
    result={'platform': 'mx480', 'vendor': 'Juniper', 'version': '9.6R1.13'}
    motd=' \n--- JUNOS 9.6R1.13 built 2009-08-01 09:02:46 UTC\n'
    cli={'set cli screen-length 0': ' set cli screen-length 0 \nScreen length set to 0\n\n',
 'show version': ' show version \nHostname: router1\nModel: mx480\nJUNOS Base OS boot [9.6R1.13]\nJUNOS Base OS Software Suite [9.6R1.13]\nJUNOS Kernel Software Suite [9.6R1.13]\nJUNOS Crypto Software Suite [9.6R1.13]\nJUNOS Packet Forwarding Engine Support (M/T Common) [9.6R1.13]\nJUNOS Packet Forwarding Engine Support (MX Common) [9.6R1.13]\nJUNOS Online Documentation [9.6R1.13]\nJUNOS Voice Services Container package [9.6R1.13]\nJUNOS Border Gateway Function package [9.6R1.13]\nJUNOS Services AACL Container package [9.6R1.13]\nJUNOS Services LL-PDF Container package [9.6R1.13]\nJUNOS Services Stateful Firewall [9.6R1.13]\nJUNOS AppId Services [9.6R1.13]\nJUNOS IDP Services [9.6R1.13]\nJUNOS Routing Software Suite [9.6R1.13]\n\n'}
    snmp_get={}
    snmp_getnext={}
        
