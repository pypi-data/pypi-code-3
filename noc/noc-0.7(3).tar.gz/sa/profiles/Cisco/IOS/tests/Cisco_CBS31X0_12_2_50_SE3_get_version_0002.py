# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Cisco.IOS.get_version test
## Auto-generated by manage.py debug-script at 2010-09-22 23:47:37
##----------------------------------------------------------------------
## Copyright (C) 2007-2010 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------
from noc.lib.test import ScriptTestCase
class Cisco_IOS_get_version_Test(ScriptTestCase):
    script="Cisco.IOS.get_version"
    vendor="Cisco"
    platform='CBS31X0'
    version='12.2(50)SE3'
    input={}
    result={'attributes': {'image': 'CBS31X0-UNIVERSALK9-M'},
 'platform': 'CBS31X0',
 'vendor': 'Cisco',
 'version': '12.2(50)SE3'}
    motd=' \nC\nThe system is a property of Acme INC.\nPlease disconnect immediately if you are not authorized staff\n\n'
    cli={'terminal length 0': 'terminal length 0\n'}
    snmp_get={'1.3.6.1.2.1.1.1.0': 'Cisco IOS Software, CBS31X0 Software (CBS31X0-UNIVERSALK9-M), Version 12.2(50)SE3, RELEASE SOFTWARE (fc1)\r\nTechnical Support: http://www.cisco.com/techsupport\r\nCopyright (c) 1986-2009 by Cisco Systems, Inc.\r\nCompiled Wed 22-Jul-09 09:10 by prod_rel_team'}
    snmp_getnext={}
        
