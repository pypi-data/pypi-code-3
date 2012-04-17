# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Vyatta.Vyatta.get_arp test
## Auto-generated by manage.py debug-script at 2010-12-27 17:24:31
##----------------------------------------------------------------------
## Copyright (C) 2007-2010 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------
from noc.lib.test import ScriptTestCase
class Vyatta_Vyatta_get_arp_Test(ScriptTestCase):
    script="Vyatta.Vyatta.get_arp"
    vendor="Vyatta"
    platform='Vyatta'
    version='VC6.1-2010.10.16'
    input={}
    result=[{'interfae': 'bond0.910', 'ip': '172.18.142.8', 'mac': '00:60:08:33:2D:61'},
 {'interfae': 'bond0.902', 'ip': '214.113.108.65', 'mac': '00:14:5E:6B:AA:7C'},
 {'interfae': 'bond0.910', 'ip': '172.18.142.1', 'mac': '00:80:D3:F1:A1:5D'}]
    motd=' \nLinux host1234567 2.6.32-1-586-vyatta #1 SMP Thu Sep 23 12:42:33 PDT 2010 i686\nWelcome to Vyatta.\nThis system is open-source software. The exact distribution terms for \neach module comprising the full system are described in the individual \nfiles in /usr/share/doc/*/copyright.\nLast login: Mon Dec 27 14:20:31 2010 from noc.example.com\n'
    cli={
## 'show arp'
'show arp': """show arp
Address                  HWtype  HWaddress           Flags Mask            Iface
172.18.142.8             ether   00:60:08:33:2d:61   C                     bond0.910
214.113.108.65           ether   00:14:5e:6b:aa:7c   C                     bond0.902
172.18.142.1             ether   00:80:d3:f1:a1:5d   C                     bond0.910""",
'terminal length 0':  'terminal length 0\n',
}
    snmp_get={}
    snmp_getnext={}
