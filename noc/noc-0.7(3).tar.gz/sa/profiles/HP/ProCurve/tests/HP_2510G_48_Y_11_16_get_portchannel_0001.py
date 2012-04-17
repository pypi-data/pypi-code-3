# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## HP.ProCurve.get_portchannel test
## Auto-generated by manage.py debug-script at 2010-11-23 11:05:27
##----------------------------------------------------------------------
## Copyright (C) 2007-2010 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------
from noc.lib.test import ScriptTestCase
class HP_ProCurve_get_portchannel_Test(ScriptTestCase):
    script="HP.ProCurve.get_portchannel"
    vendor="HP"
    platform='2510G-48'
    version='Y.11.16'
    input={}
    result=[{'interface': 'Trk1', 'members': ['47', '48'], 'type': 'L'}]
    motd=' \nProCurve J9280A Switch 2510G-48\nSoftware revision Y.11.16\n\nCopyright (C) 1991-2009 Hewlett-Packard Co.  All Rights Reserved.\n\n                           RESTRICTED RIGHTS LEGEND\n\n Use, duplication, or disclosure by the Government is subject to restrictions\n as set forth in subdivision (b) (3) (ii) of the Rights in Technical Data and\n Computer Software clause at 52.227-7013.\n\n         HEWLETT-PACKARD COMPANY, 3000 Hanover St., Palo Alto, CA 94303\n\n'
    cli={
'terminal length 1000':  'terminal length ',
## 'show trunks'
'show trunks': """show trunks
 Load Balancing

  Port | Name                             Type      | Group Type 
  ---- + -------------------------------- --------- + ----- -----
  47   |                                  100/1000T | Trk1  LACP 
  48   |                                  100/1000T | Trk1  LACP 
 
""",
}
    snmp_get={}
    snmp_getnext={}
