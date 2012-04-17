# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## EdgeCore.ES.get_version test
## Auto-generated by manage.py debug-script at 2011-03-01 18:36:08
##----------------------------------------------------------------------
## Copyright (C) 2007-2011 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------
from noc.lib.test import ScriptTestCase
class EdgeCore_ES_get_version_Test(ScriptTestCase):
    script="EdgeCore.ES.get_version"
    vendor="EdgeCore"
    platform='ES4626-SFP'
    version='6.0.220.33'
    input={}
    result={'platform': 'ES4626-SFP', 'vendor': 'EdgeCore', 'version': '6.0.220.33'}
    motd='********\n'
    cli={
}
    snmp_get={'1.3.6.1.2.1.1.1.0': 'ES4626-SFP Device, Compiled Apr 23 14:41:49 2010\n SoftWare Version ES4626-SFP_6.0.220.33\n BootRom Version ES4626-SFP_1.7.0\n HardWare Version 3.0\n Copyright (C) 2001-2007 by Accton Technology Corp.\n All rights reserved\n',
 '1.3.6.1.2.1.1.2.0': '(1, 3, 6, 1, 4, 1, 259, 8, 1, 3)',
 '1.3.6.1.4.1.259.8.1.3.1.1.3.1.6.1': '',
 '1.3.6.1.4.1.259.8.1.3.100.1.3.0': '6.0.220.33'}
    snmp_getnext={}
