# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## H3C.VRP.get_version test
## Auto-generated by manage.py debug-script at 2011-03-11 09:51:29
##----------------------------------------------------------------------
## Copyright (C) 2007-2011 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------
from noc.lib.test import ScriptTestCase
class H3C_VRP_get_version_Test(ScriptTestCase):
    script="H3C.VRP.get_version"
    vendor="H3C"
    platform='4500G'
    version='5.02.00s56p12'
    input={}
    result={'platform': '4500G 24-Port', 'vendor': 'H3C', 'version': '5.02.00s56p12'}
    motd='\n'
    cli={
## 'display version'
'display version': """display version
3Com Corporation
3Com Switch 4500G 24-Port Software Version 3Com OS V5.02.00s56p12
Copyright (c) 2004-2009 3Com Corp. and its licensors. All rights reserved.
3Com Switch 4500G 24-Port uptime is 41 weeks, 2 days, 5 hours, 10 minutes

3Com Switch 4500G 24-Port with 1 Processor
128M    bytes SDRAM
16384K  bytes Flash Memory

Hardware Version is REV.B
CPLD Version is 007
Bootrom Version is 503
[SubSlot 0] 24GE+4SFP Hardware Version is REV.B
""",
}
    snmp_get={}
    snmp_getnext={}
