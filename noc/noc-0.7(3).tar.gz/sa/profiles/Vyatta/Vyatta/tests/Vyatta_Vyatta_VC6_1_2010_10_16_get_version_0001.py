# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Vyatta.Vyatta.get_version test
## Auto-generated by manage.py debug-script at 2010-12-27 17:27:26
##----------------------------------------------------------------------
## Copyright (C) 2007-2010 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------
from noc.lib.test import ScriptTestCase
class Vyatta_Vyatta_get_version_Test(ScriptTestCase):
    script="Vyatta.Vyatta.get_version"
    vendor="Vyatta"
    platform='Vyatta'
    version='VC6.1-2010.10.16'
    input={}
    result={'platform': 'VC', 'vendor': 'Vyatta', 'version': 'VC6.1-2010.10.16'}
    motd=' \nLinux host1234567 2.6.32-1-586-vyatta #1 SMP Thu Sep 23 12:42:33 PDT 2010 i686\nWelcome to Vyatta.\nThis system is open-source software. The exact distribution terms for \neach module comprising the full system are described in the individual \nfiles in /usr/share/doc/*/copyright.\nLast login: Mon Dec 27 14:23:12 2010 from noc.example.com\n'
    cli={
## 'show version'
'show version': """show version
Version:      VC6.1-2010.10.16
Description:  Vyatta Core 6.1 2010.10.16
Copyright:    2006-2010 Vyatta, Inc.
Built by:     autobuild@vyatta.com
Built on:     Sat Oct 16 01:12:35 UTC 2010
Build ID:     1010160115-d310b15
Boot via:     image
Uptime:       14:26:10 up 5 days, 23:44,  2 users,  load average: 0.00, 0.00, 0.00

""",
'terminal length 0':  'terminal length 0\n',
}
    snmp_get={}
    snmp_getnext={}
