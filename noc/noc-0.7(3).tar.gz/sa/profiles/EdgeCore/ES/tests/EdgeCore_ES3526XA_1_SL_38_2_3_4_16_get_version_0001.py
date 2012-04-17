# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## EdgeCore.ES35xx.get_version test
## Auto-generated by manage.py debug-script at 2010-09-24 17:11:36
##----------------------------------------------------------------------
## Copyright (C) 2007-2010 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------
from noc.lib.test import ScriptTestCase
class EdgeCore_ES35xx_get_version_Test(ScriptTestCase):
    script="EdgeCore.ES.get_version"
    vendor="EdgeCore"
    platform='ES3526XA-1-SL-38'
    version='2.3.4.16'
    input={}
    result={'platform': 'ES3526XA-1-SL-38', 'vendor': 'EdgeCore', 'version': '2.3.4.16'}
    motd=' \n\n      CLI session with the Standalone Intelligent Switch is opened.\n      To end the CLI session, enter [Exit].\n\n'
    cli={
## 'show version'
'show version': """show version
Unit 1
 Serial number:           A715028704
 Service tag:             
 Hardware version:        R01A1
 Module A type:           1000BaseT
 Module B type:           1000BaseT
 Number of ports:         26
 Main power status:       up
 Redundant power status   :not present

Agent (master)
 Unit ID:                 1
 Loader version:          2.2.1.4
 Boot ROM version:        2.3.0.0
 Operation code version:  2.3.4.16
""",
## 'show system'
'show system': """show system
System description: Layer2+ Fast Ethernet Standalone Switch ES3526XA
System OID string: 1.3.6.1.4.1.259.6.10.74
System information
 System Up time:          190 days, 11 hours, 33 minutes, and 2.92 seconds
 System Name:             sw023-006
 System Location:         [NONE]
 System Contact:          [NONE]
 MAC address:             00-12-CF-4C-01-80
 Web server:              enabled
 Web server port:         80
 Web secure server:       enabled
 Web secure server port:  443
 Telnet server          : enable
 Telnet port            : 23
 Authentication login:     TACACS local
 Jumbo Frame :            Disabled 
 POST result              
DUMMY Test 1.................PASS
UART LOOP BACK Test..........PASS
DRAM Test....................PASS
Timer Test...................PASS
RTC Initialization...........PASS
Switch Int Loopback Test.....PASS

Done All Pass.     """,
}
    snmp_get={}
    snmp_getnext={}
