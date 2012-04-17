# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Force10.FTOS.get_version test
## Auto-generated by manage.py debug-script at 2010-09-22 23:29:32
##----------------------------------------------------------------------
## Copyright (C) 2007-2010 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------
from noc.lib.test import ScriptTestCase
class Force10_FTOS_get_version_Test(ScriptTestCase):
    script="Force10.FTOS.get_version"
    vendor="Force10"
    platform='C300'
    version='8.3.2.0'
    input={}
    result={'platform': 'C300', 'vendor': 'Force10', 'version': '8.3.2.0'}
    motd=' \n'
    cli={'show version': 'show version\nForce10 Networks Real Time Operating System Software\nForce10 Operating System Version: 1.0\nForce10 Application Software Version: 8.3.2.0\nCopyright (c) 1999-2010 by Force10 Networks, Inc.\nBuild Time: Wed Jul 7 19:27:13 PDT 2010\nBuild Path: /sites/sjc/work/build/buildSpaces/build12/E8-3-2/SW/SRC\nsw-3-ti uptime is 2 week(s), 1 day(s), 5 hour(s), 34 minute(s)\n\nSystem image file is "flash://FTOS-CB-8.3.2.0.bin"\n\nChassis Type: C300 \nControl Processor: IBM PowerPC 750FX (Rev D2.2) with 1090519040 bytes of memory.\n\n128K bytes of non-volatile configuration memory.\n\n  2 Route Processor/Switch Fabric Module\n  2 36-port GE 10/100/1000Base-T with RJ45 - 8-port FE/GE with SFP - 2-port 10GE with SFP+\n  3 48-port GE 10/100/1000Base-T line card with RJ45 interfaces (CB)\n  2 FastEthernet/IEEE 802.3 interface(s)\n232 GigabitEthernet/IEEE 802.3 interface(s)\n  4 Ten GigabitEthernet/IEEE 802.3 interface(s)\n',
 'terminal length 0': 'terminal length 0\n'}
    snmp_get={}
    snmp_getnext={}
        