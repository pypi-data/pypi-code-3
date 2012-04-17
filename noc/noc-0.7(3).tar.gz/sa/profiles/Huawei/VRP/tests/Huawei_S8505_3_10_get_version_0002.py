# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Huawei.VRP.get_version test
## Auto-generated by manage.py debug-script at 2011-06-12 17:21:54
##----------------------------------------------------------------------
## Copyright (C) 2007-2011 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------
from noc.lib.test import ScriptTestCase
class Huawei_VRP_get_version_Test(ScriptTestCase):
    script = "Huawei.VRP.get_version"
    vendor = "Huawei"
    platform = 'S8505'
    version = '3.10'
    input = {}
    result = {'platform': 'S8505', 'vendor': 'Huawei', 'version': '3.10'}
    motd = '\n'
    cli = {
'screen-length 0 temporary':  "screen-length 0 temporary\n                    ^\n % Unrecognized command found at '^' position.\n", 
}
    snmp_get = {'1.3.6.1.2.1.1.1.0': 'Huawei Versatile Routing Platform Software, Software Version 3.10, Release 1648P01\r\nQuidway S8505-EI \r\nCopyright(c) 1998-2008 Huawei Technologies Co., Ltd. All rights reserved.'}
    snmp_getnext = {}
