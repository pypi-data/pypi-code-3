# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Cisco.IOS.get_version test
## Auto-generated by manage.py debug-script at 2010-09-23 19:47:57
##----------------------------------------------------------------------
## Copyright (C) 2007-2010 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------
from noc.lib.test import ScriptTestCase
class Cisco_IOS_get_version_Test(ScriptTestCase):
    script="Cisco.IOS.get_version"
    vendor="Cisco"
    platform='2800'
    version='12.4(25c)'
    input={}
    result={'attributes': {'image': 'C2800NM-ADVENTERPRISEK9-M'},
 'platform': '2800',
 'vendor': 'Cisco',
 'version': '12.4(25c)'}
    motd=''
    cli={'terminal length 0': 'terminal length 0\n', 'show version': 'show version\nCisco IOS Software, 2800 Software (C2800NM-ADVENTERPRISEK9-M), Version 12.4(25c), RELEASE SOFTWARE (fc2)\nTechnical Support: http://www.cisco.com/techsupport\nCopyright (c) 1986-2010 by Cisco Systems, Inc.\nCompiled Thu 11-Feb-10 23:55 by prod_rel_team\n\nROM: System Bootstrap, Version 12.4(1r) [hqluong 1r], RELEASE SOFTWARE (fc1)\n\nRouter1 uptime is 4 weeks, 2 days, 23 hours, 36 minutes\nSystem returned to ROM by reload at 20:08:49 MSD Mon Aug 23 2010\nSystem restarted at 19:01:49 MSD Mon Aug 23 2010\nSystem image file is "flash:c2800nm-adventerprisek9-mz.124-25c.bin"\n\n\nThis product contains cryptographic features and is subject to United\nStates and local country laws governing import, export, transfer and\nuse. Delivery of Cisco cryptographic products does not imply\nthird-party authority to import, export, distribute or use encryption.\nImporters, exporters, distributors and users are responsible for\ncompliance with U.S. and local country laws. By using this product you\nagree to comply with applicable laws and regulations. If you are unable\nto comply with U.S. and local laws, return this product immediately.\n\nA summary of U.S. laws governing Cisco cryptographic products may be found at:\nhttp://www.cisco.com/wwl/export/crypto/tool/stqrg.html\n\nIf you require further assistance please contact us by sending email to\nexport@cisco.com.\n\nCisco 2811 (revision 53.51) with 247808K/14336K bytes of memory.\nProcessor board ID FCZ104670RJ\n2 FastEthernet interfaces\n31 Serial interfaces\n8 terminal lines\n1 Channelized E1/PRI port\n1 Virtual Private Network (VPN) Module\nDRAM configuration is 64 bits wide with parity enabled.\n239K bytes of non-volatile configuration memory.\n62720K bytes of ATA CompactFlash (Read/Write)\n\nConfiguration register is 0x2102\n\n'}
    snmp_get={}
    snmp_getnext={}

