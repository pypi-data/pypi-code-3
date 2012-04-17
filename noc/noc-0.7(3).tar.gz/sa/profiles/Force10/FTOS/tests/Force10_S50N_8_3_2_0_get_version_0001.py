# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Force10.FTOS.get_version test
## Auto-generated by manage.py debug-script at 2010-09-22 23:30:41
##----------------------------------------------------------------------
## Copyright (C) 2007-2010 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------
from noc.lib.test import ScriptTestCase
class Force10_FTOS_get_version_Test(ScriptTestCase):
    script="Force10.FTOS.get_version"
    vendor="Force10"
    platform='S50N'
    version='8.3.2.0'
    input={}
    result={'platform': 'S50N', 'vendor': 'Force10', 'version': '8.3.2.0'}
    motd=' \n'
    cli={'show version': 'show version\nForce10 Networks Real Time Operating System Software\nForce10 Operating System Version: 1.0\nForce10 Application Software Version: 8.3.2.0\nCopyright (c) 1999-2010 by Force10 Networks, Inc.\nBuild Time: Wed Jul 7 18:35:25 PDT 2010\nBuild Path: /sites/sjc/work/build/buildSpaces/build12/E8-3-2/SW/SRC\nsw-18-ti uptime is 5 week(s), 2 day(s), 13 hour(s), 27 minute(s)\n\nSystem Type: S50N \nControl Processor: Freescale MPC8541E with 268435456 bytes of memory.\n\n32M bytes of boot flash memory.\n\n  1 48-port E/FE/GE (SB)\n 48 GigabitEthernet/IEEE 802.3 interface(s)\n',
 'terminal length 0': 'terminal length 0\n'}
    snmp_get={}
    snmp_getnext={}
        