# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Cisco.IOS.get_copper_tdr_diag test
## Auto-generated by ./noc debug-script at 2012-02-22 14:51:03
##----------------------------------------------------------------------
## Copyright (C) 2007-2012 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

## NOC modules
from noc.lib.test import ScriptTestCase


class Cisco_IOS_get_copper_tdr_diag_Test(ScriptTestCase):
    script = "Cisco.IOS.get_copper_tdr_diag"
    vendor = "Cisco"
    platform = 'C3560'
    version = '12.2(44)SE2'
    input = {'interface': 'gigabitEthernet 0/4'}
    result = [{'interface': 'Gi 0/4',
  'pairs': [{'distance_cm': 700,
             'pair': 1,
             'status': 'T',
             'variance_cm': 400},
            {'distance_cm': 700,
             'pair': 2,
             'status': 'T',
             'variance_cm': 400},
            {'distance_cm': 800,
             'pair': 3,
             'status': 'S',
             'variance_cm': 400},
            {'distance_cm': 800,
             'pair': 4,
             'status': 'S',
             'variance_cm': 400}]}]
    motd = ''
    cli = {
## 'test cable-diagnostics tdr interface Gi 0/4'
'test cable-diagnostics tdr interface Gi 0/4': """test cable-diagnostics tdr interface Gi 0/4
Link state may be affected during TDR test
TDR test started on interface Gi0/4
A TDR test can take a few seconds to run on an interface
Use 'show cable-diagnostics tdr' to read the TDR results.""", 
'terminal length 0':  'terminal length 0\n', 
## 'show cable-diagnostics tdr interface Gi 0/4'
'show cable-diagnostics tdr interface Gi 0/4': """show cable-diagnostics tdr interface Gi 0/4
TDR test last run on: February 22 15:10:52

Interface Speed Local pair Pair length        Remote pair Pair status
--------- ----- ---------- ------------------ ----------- --------------------
Gi0/4     auto  Pair A     7    +/- 4  meters Pair A      Normal              
                Pair B     7    +/- 4  meters Pair B      Normal              
                Pair C     8    +/- 4  meters Pair C      Short               
                Pair D     8    +/- 4  meters Pair D      Short               """, 
}
    snmp_get = {}
    snmp_getnext = {}
    http_get = {}
