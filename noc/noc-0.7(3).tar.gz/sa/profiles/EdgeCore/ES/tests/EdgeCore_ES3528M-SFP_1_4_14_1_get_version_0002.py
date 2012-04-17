# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## EdgeCore.ES.get_version test
## Auto-generated by ./noc debug-script at 2012-02-23 21:48:59
##----------------------------------------------------------------------
## Copyright (C) 2007-2012 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

## NOC modules
from noc.lib.test import ScriptTestCase


class EdgeCore_ES_get_version_Test(ScriptTestCase):
    script = "EdgeCore.ES.get_version"
    vendor = "EdgeCore"
    platform = 'ES3528M-SFP'
    version = '1.4.14.1'
    input = {}
    result = {'platform': 'ES3528M-SFP', 'vendor': 'EdgeCore', 'version': '1.4.14.1'}
    motd = ' \n\n      CLI session with the ES3528M-SFP is opened.\n      To end the CLI session, enter [Exit].\n\nNo configured settings for reloading.\n'
    cli = {
'terminal length 0':  'terminal length 0\n', 
}
    snmp_get = {'1.3.6.1.2.1.1.1.0': 'ES3528M-SFP',
 '1.3.6.1.2.1.1.2.0': '1.3.6.1.4.1.259.8.2.4',
 '1.3.6.1.4.1.259.8.1.4.1.1.3.1.6.1': '1.4.14.1'}
    snmp_getnext = {}
    http_get = {}
