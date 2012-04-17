# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## HP.ProCurve9xxx.get_version test
## Auto-generated by manage.py debug-script at 2011-02-16 16:59:55
##----------------------------------------------------------------------
## Copyright (C) 2007-2011 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------
from noc.lib.test import ScriptTestCase
class HP_ProCurve9xxx_get_version_Test(ScriptTestCase):
    script="HP.ProCurve9xxx.get_version"
    vendor="HP"
    platform='9304m'
    version='07.8.03T53'
    input={}
    result={'platform': 'HP9304', 'vendor': 'HP', 'version': '07.8.03T53'}
    motd=' \n'
    cli={
'terminal length 1000':  'terminal length 1000\n',
## 'show version'
'show version': """show version
  SW: Version 07.8.03T53 Hewlett-Packard Company
      Compiled on Mar 01 2007 at 16:39:49 labeled as H2R07803
      (3778944 bytes) from Primary H2R07803.bin
      J4139A HP ProCurve Routing Switch 9304M
  HW: ProCurve HP9304 Routing Switch, SYSIF version 21, Serial #: Non-exist
==========================================================================
SL 1: J4885A EP 8 port mini-GBIC Management Module, SYSIF 2 (Mini GBIC), M4, ACTIVE
      Serial #:   US06022256
 4096 KB BRAM, JetCore ASIC IGC version 49, BIA version 8a
32768 KB PRAM and 2M-Bit*1 CAM for IGC  0, version 0449
32768 KB PRAM and 2M-Bit*1 CAM for IGC  1, version 0449
==========================================================================
SL 2: J4895A EP 16-port 100/1000-T Module, SYSIF 2
      Serial #:   US06021802
 4096 KB BRAM, JetCore ASIC IGC version 49, BIA version 8a
32768 KB PRAM and 2M-Bit*1 CAM for IGC  4, version 0449
32768 KB PRAM and 2M-Bit*1 CAM for IGC  5, version 0449
32768 KB PRAM and 2M-Bit*1 CAM for IGC  6, version 0449
32768 KB PRAM and 2M-Bit*1 CAM for IGC  7, version 0449
==========================================================================
Active management module:
  466 MHz Power PC processor 750 (version 8/8302) 66 MHz bus
  512 KB boot flash memory
16384 KB code flash memory
  512 KB SRAM
  512 MB DRAM
The system uptime is 78 days 1 hours 33 minutes 23 seconds 
The system started at 15:26:49 GMT+03 Tue Nov 30 2010

The system : started=cold start   
""",
}
    snmp_get={}
    snmp_getnext={}
