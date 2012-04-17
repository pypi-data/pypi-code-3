# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## OS.FreeBSD.get_fqdn test
## Auto-generated by manage.py debug-script at 2011-01-18 14:54:45
##----------------------------------------------------------------------
## Copyright (C) 2007-2011 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------
from noc.lib.test import ScriptTestCase
class OS_FreeBSD_get_fqdn_Test(ScriptTestCase):
    script="OS.FreeBSD.get_fqdn"
    vendor="OS"
    platform='amd64'
    version='8.2-PRERELEASE'
    input={}
    result="['noc.cabletv.dp.ua']"
    motd='\n'
    cli={
'hostname':  ' hostname\nnoc.cabletv.dp.ua\n',
}
    snmp_get={}
    snmp_getnext={}
