# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## OS.Linux.ping test
## Auto-generated by ./noc debug-script at 2011-11-02 19:21:51
##----------------------------------------------------------------------
## Copyright (C) 2007-2011 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

## NOC modules
from noc.lib.test import ScriptTestCase


class OS_Linux_ping_Test(ScriptTestCase):
    script = "OS.Linux.ping"
    vendor = "OS"
    platform = 'RG-14xx'
    version = '1.0'
    input = {'address': '10.8.4.9'}
    result = {'count': 5, 'success': 0}
    motd = " \n\n\nBusyBox v1.4.2 (2011-02-01 17:34:38 NOVT) Built-in shell (ash)\nEnter 'help' for a list of built-in commands.\n\n  _______                     ________        __\n |       |.-----.-----.-----.|  |  |  |.----.|  |_\n |   -   ||  _  |  -__|     ||  |  |  ||   _||   _|\n |_______||   __|_____|__|__||________||__|  |____|\n          |__| W I R E L E S S   F R E E D O M\n\n M I N D S P E E D  Technologies - Build v6.0 for Comcerto\n  _____   _     _____   _____  __  __\n |  ___| | |   |_   _| |  ___| \\ \\/ /\n |  ___| | |__   | |   |  ___|  \n |_____| |____|  |_|   |_____| /_/\\_\\\n \n TAU-4/8.IP software is based on OpenWRT\n ---------------------------------------------------\n"
    cli = {
'export LANG=en_GB.UTF-8':  'export LANG=en_GB.UTF-8\n', 
## 'ping -q -c 5 10.8.4.9'
'ping -q -c 5 10.8.4.9': """ping -q -c 5 10.8.4.9
PING 10.8.4.9 (10.8.4.9): 56 data bytes

--- 10.8.4.9 ping statistics ---
5 packets transmitted, 0 packets received, 100% packet loss""", 
}
    snmp_get = {}
    snmp_getnext = {}
