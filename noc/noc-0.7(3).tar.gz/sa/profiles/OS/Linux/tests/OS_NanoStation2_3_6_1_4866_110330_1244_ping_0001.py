# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## OS.Linux.ping test
## Auto-generated by ./noc debug-script at 2011-11-02 19:27:46
##----------------------------------------------------------------------
## Copyright (C) 2007-2011 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

## NOC modules
from noc.lib.test import ScriptTestCase


class OS_Linux_ping_Test(ScriptTestCase):
    script = "OS.Linux.ping"
    vendor = "OS"
    platform = 'NanoStation2'
    version = '3.6.1.4866.110330.1244'
    input = {'address': '10.8.4.19'}
    result = {'avg': '1.2', 'count': 5, 'max': '1.5', 'min': '1.1', 'success': 5}
    motd = "\n\nBusyBox v1.01 (2011.03.30-09:47+0000) Built-in shell (ash)\nEnter 'help' for a list of built-in commands.\n\n"
    cli = {
## 'ping -q -c 5 10.8.4.19'
'ping -q -c 5 10.8.4.19': """ping -q -c 5 10.8.4.19
PING 10.8.4.19 (10.8.4.19): 56 data bytes

--- 10.8.4.19 ping statistics ---
5 packets transmitted, 5 packets received, 0% packet loss
round-trip min/avg/max = 1.1/1.2/1.5 ms""", 
'export LANG=en_GB.UTF-8':  'export LANG=en_GB.UTF-8\n', 
}
    snmp_get = {}
    snmp_getnext = {}
