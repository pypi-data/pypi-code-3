# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Ericsson.SEOS.get_version test
## Auto-generated by ./noc debug-script at 2011-08-07 09:53:20
##----------------------------------------------------------------------
## Copyright (C) 2007-2011 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

## NOC modules
from noc.lib.test import ScriptTestCase


class Ericsson_SEOS_get_version_Test(ScriptTestCase):
    script = "Ericsson.SEOS.get_version"
    vendor = "Ericsson"
    platform = 'SEOS'
    version = '6.4.1.3'
    input = {}
    result = {'platform': 'SEOS', 'vendor': 'Ericsson', 'version': '6.4.1.3'}
    motd = ''
    cli = {
## 'show version'
'show version': """show version

Redback Networks SmartEdge OS Version SEOS-6.4.1.3-Release
Built by sysbuild@SWB-node17 Thu Mar 17 23:36:10 PDT 2011
Copyright (C) 1998-2011, Redback Networks Inc. All rights reserved.
System Bootstrap version is Mips,rev2.0.2.45
Installed minikernel version is 11.7
Router Up Time -   51 days, 5 hours 50 minutes 31 secs""", 
'terminal length 0':  'terminal length 0\n', 
}
    snmp_get = {}
    snmp_getnext = {}
