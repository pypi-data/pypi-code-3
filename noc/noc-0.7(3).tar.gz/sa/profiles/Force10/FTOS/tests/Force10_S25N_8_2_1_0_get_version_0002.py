# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Force10.FTOS.get_version test
## Auto-generated by manage.py debug-script at 2010-09-22 23:31:21
##----------------------------------------------------------------------
## Copyright (C) 2007-2010 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------
from noc.lib.test import ScriptTestCase
class Force10_FTOS_get_version_Test(ScriptTestCase):
    script="Force10.FTOS.get_version"
    vendor="Force10"
    platform='S25N'
    version='8.2.1.0'
    input={}
    result={'platform': 'S25N', 'vendor': 'Force10', 'version': '8.2.1.0'}
    motd=' \n'
    cli={'show version': 'show version\nForce10 Networks Real Time Operating System Software\nForce10 Operating System Version: 1.0\nForce10 Application Software Version: 8.2.1.0\nCopyright (c) 1999-2009 by Force10 Networks, Inc.\nBuild Time: Mon Jun 29 15:01:22 PDT 2009\nBuild Path: /sites/sjc/work/sw/build/build4/E8-2-1/SW/SRC\nsw-16-ti uptime is 43 week(s), 1 day(s), 8 hour(s), 13 minute(s)\n\nSystem Type: S25N \nControl Processor: Freescale MPC8541E with 252616704 bytes of memory.\n\n32M bytes of boot flash memory.\n\n  1 24-port E/FE/GE (SB)\n 24 GigabitEthernet/IEEE 802.3 interface(s)\n',
 'terminal length 0': 'terminal length 0\n'}
    snmp_get={'1.3.6.1.2.1.1.1.0': 'Force10 Networks Real Time Operating System Software\r\nForce10 Operating System Version: 1.0\r\nForce10 Application Software Version: 8.2.1.0\r\nCopyright (c) 1999-2009 by Force10 Networks, Inc.\r\nBuild Time: Mon Jun 29 15:01:22 PDT 2009',
 '1.3.6.1.4.1.6027.3.1.1.1.1.0': ''}
    snmp_getnext={}
        