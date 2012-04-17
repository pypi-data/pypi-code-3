# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Cisco.IOS.get_chassis_id test
## Auto-generated by manage.py debug-script at 2010-12-15 13:05:53
##----------------------------------------------------------------------
## Copyright (C) 2007-2010 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------
from noc.lib.test import ScriptTestCase
class Cisco_IOS_get_chassis_id_Test(ScriptTestCase):
    script="Cisco.IOS.get_chassis_id"
    vendor="Cisco"
    platform='s72033_rp'
    version='12.2(33)SXH2a'
    input={}
    result='00:19:07:DA:AC:00'
    motd=' \n\n'
    cli={
'show catalyst6000 chassis-mac-addresses':  'show catalyst6000 chassis-mac-addresses\n  chassis MAC addresses: 1024 addresses from 0019.07da.ac00 to 0019.07da.afff\n',
## 'show version'
'show version': """show version
Cisco IOS Software, s72033_rp Software (s72033_rp-ADVENTERPRISEK9_WAN-M), Version 12.2(33)SXH2a, RELEASE SOFTWARE (fc2)
Technical Support: http://www.cisco.com/techsupport
Copyright (c) 1986-2008 by Cisco Systems, Inc.
Compiled Fri 25-Apr-08 08:59 by prod_rel_team

ROM: System Bootstrap, Version 12.2(17r)S4, RELEASE SOFTWARE (fc1)

 c6509xxx uptime is 31 weeks, 2 days, 16 hours, 47 minutes
Uptime for this control processor is 31 weeks, 2 days, 16 hours, 54 minutes
Time since c6509eu1 switched to active is 31 weeks, 2 days, 16 hours, 52 minutes
System returned to ROM by s/w reset at 22:10:08 GMT Wed Feb 27 2008 (SP by bus error at PC 0x41183348, address 0x0)
System restarted at 17:12:47 GMT Sun May 9 2010
System image file is "disk0:s72033-adventerprisek9_wan-mz.122-33.SXH2a.bin"


This product contains cryptographic features and is subject to United
States and local country laws governing import, export, transfer and
use. Delivery of Cisco cryptographic products does not imply
third-party authority to import, export, distribute or use encryption.
Importers, exporters, distributors and users are responsible for
compliance with U.S. and local country laws. By using this product you
agree to comply with applicable laws and regulations. If you are unable
to comply with U.S. and local laws, return this product immediately.

A summary of U.S. laws governing Cisco cryptographic products may be found at:
http://www.cisco.com/wwl/export/crypto/tool/stqrg.html

If you require further assistance please contact us by sending email to
export@cisco.com.

cisco WS-C6509-E (R7000) processor (revision 1.3) with 983008K/65536K bytes of memory.
Processor board ID SMC10370038
SR71000 CPU at 600Mhz, Implementation 0x504, Rev 1.2, 512KB L2 Cache
Last reset from s/w reset
12 Virtual Ethernet interfaces
26 Gigabit Ethernet interfaces
12 Ten Gigabit Ethernet interfaces
1917K bytes of non-volatile configuration memory.
8192K bytes of packet buffer memory.

65536K bytes of Flash internal SIMM (Sector size 512K).
Configuration register is 0x2102
""",
'terminal length 0':  'terminal length 0\n',
}
    snmp_get={}
    snmp_getnext={}
