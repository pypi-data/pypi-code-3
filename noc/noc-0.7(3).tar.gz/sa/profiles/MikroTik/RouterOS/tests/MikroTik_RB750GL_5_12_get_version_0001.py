# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## MikroTik.RouterOS.get_version test
## Auto-generated by ./noc debug-script at 2012-02-09 12:44:28
##----------------------------------------------------------------------
## Copyright (C) 2007-2012 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

## NOC modules
from noc.lib.test import ScriptTestCase


class MikroTik_RouterOS_get_version_Test(ScriptTestCase):
    script = "MikroTik.RouterOS.get_version"
    vendor = "MikroTik"
    platform = 'RB750GL'
    version = '5.12'
    input = {}
    result = {'attributes': {'Boot PROM': '2.35', 'Serial Number': '2CF901577F74'},
 'platform': 'RB750GL',
 'vendor': 'MikroTik',
 'version': '5.12'}
    motd = ''
    cli = {
## 'system resource print'
'system resource print': """system resource print
                   uptime: 1h42m17s
                  version: 5.12
              free-memory: 49996KiB
             total-memory: 62196KiB
                      cpu: MIPS 24Kc V7.4
                cpu-count: 1
            cpu-frequency: 400MHz
                 cpu-load: 8%
           free-hdd-space: 30888KiB
          total-hdd-space: 61440KiB
  write-sect-since-reboot: 756
         write-sect-total: 119023
               bad-blocks: 0%
        architecture-name: mipsbe
               board-name: RB750GL
                 platform: MikroTik""", 
## 'system routerboard print'
'system routerboard print': """system routerboard print
       routerboard: yes
             model: 750GL
     serial-number: 2CF901577F74
  current-firmware: 2.35
  upgrade-firmware: 2.38""", 
}
    snmp_get = {}
    snmp_getnext = {}
    http_get = {}
