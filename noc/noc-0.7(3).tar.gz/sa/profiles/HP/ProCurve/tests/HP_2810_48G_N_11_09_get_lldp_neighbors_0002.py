# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## HP.ProCurve.get_lldp_neighbors test
## Auto-generated by manage.py debug-script at 2010-11-24 13:53:27
##----------------------------------------------------------------------
## Copyright (C) 2007-2010 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------
from noc.lib.test import ScriptTestCase
class HP_ProCurve_get_lldp_neighbors_Test(ScriptTestCase):
    script="HP.ProCurve.get_lldp_neighbors"
    vendor="HP"
    platform='2810-48G'
    version='N.11.09'
    input={}
    result=[{'local_interface': '23',
  'local_interface_id': 23,
  'neighbors': [{'remote_capabilities': 4,
                 'remote_chassis_id': '00:1F:FE:E6:52:40',
                 'remote_chassis_id_subtype': 4,
                 'remote_port': '48',
                 'remote_port_subtype': 5,
                 'remote_system_name': 'sw000000001'}]},
 {'local_interface': '24',
  'local_interface_id': 24,
  'neighbors': [{'remote_capabilities': 4,
                 'remote_chassis_id': '00:1F:FE:E6:52:40',
                 'remote_chassis_id_subtype': 4,
                 'remote_port': '47',
                 'remote_port_subtype': 5,
                 'remote_system_name': 'sw000000001'}]},
 {'local_interface': '47',
  'local_interface_id': 47,
  'neighbors': [{'remote_capabilities': 4,
                 'remote_chassis_id': '00:1C:2E:BB:34:40',
                 'remote_chassis_id_subtype': 4,
                 'remote_port': '45',
                 'remote_port_subtype': 5,
                 'remote_system_name': 'sw00000002'}]},
 {'local_interface': '48',
  'local_interface_id': 48,
  'neighbors': [{'remote_capabilities': 4,
                 'remote_chassis_id': '00:1C:2E:BB:34:40',
                 'remote_chassis_id_subtype': 4,
                 'remote_port': '46',
                 'remote_port_subtype': 5,
                 'remote_system_name': 'sw00000002'}]}]
    motd=' \nProCurve J9022A Switch 2810-48G\nSoftware revision N.11.09\n\nCopyright (C) 1991-2008 Hewlett-Packard Co.  All Rights Reserved.\n\n                           RESTRICTED RIGHTS LEGEND\n\n Use, duplication, or disclosure by the Government is subject to restrictions\n as set forth in subdivision (b) (3) (ii) of the Rights in Technical Data and\n Computer Software clause at 52.227-7013.\n\n         HEWLETT-PACKARD COMPANY, 3000 Hanover St., Palo Alto, CA 94303\n\n'
    cli={
## 'show lldp info remote-device'
'show lldp info remote-device': """show lldp info remote-device
 LLDP Remote Devices Information

  LocalPort | ChassisId                 PortId PortDescr SysName               
  --------- + ------------------------- ------ --------- ----------------------
  23        | 00 1f fe e6 52 40         48     48        sw000000001           
  24        | 00 1f fe e6 52 40         47     47        sw000000001           
  47        | 00 1c 2e bb 34 40         45     45        sw00000002            
  48        | 00 1c 2e bb 34 40         46     46        sw00000002            
 
""",
## 'show lldp info local-device'
'show lldp info local-device': """show lldp info local-device
 LLDP Local Device Information

  Chassis Type : mac-address
  Chassis Id   : 00 1d b3 b2 cb 40        
  System Name  : sw0000000012                  
  System Description : ProCurve J9022A Switch 2810-48G, revision N.11.09, R...
  System Capabilities Supported:bridge
  System Capabilities Enabled:bridge

  Management Address  :
     Type:ipv4
     Address:172.16.13.132
     Type:ipv4
     Address:172.18.82.13

 LLDP Port Information

  Port     | PortType PortId   PortDesc
  -------- + -------- -------- --------
  1        | local    1        1       
  2        | local    2        2       
  3        | local    3        3       
  4        | local    4        4       
  5        | local    5        5       
  6        | local    6        6       
  7        | local    7        7       
  8        | local    8        8       
  9        | local    9        9       
  10       | local    10       10      
  11       | local    11       11      
  12       | local    12       12      
  13       | local    13       13      
  14       | local    14       14      
  15       | local    15       15      
  16       | local    16       16      
  17       | local    17       17      
  18       | local    18       18      
  19       | local    19       19      
  20       | local    20       20      
  21       | local    21       21      
  22       | local    22       22      
  23       | local    23       23      
  24       | local    24       24      
  25       | local    25       25      
  26       | local    26       26      
  27       | local    27       27      
  28       | local    28       28      
  29       | local    29       29      
  30       | local    30       30      
  31       | local    31       31      
  32       | local    32       32      
  33       | local    33       33      
  34       | local    34       34      
  35       | local    35       35      
  36       | local    36       36      
  37       | local    37       37      
  38       | local    38       38      
  39       | local    39       39      
  40       | local    40       40      
  41       | local    41       41      
  42       | local    42       42      
  43       | local    43       43      
  44       | local    44       44      
  45       | local    45       45      
  46       | local    46       46      
  47       | local    47       47      
  48       | local    48       48      
 """,
## 'show lldp info remote-device 47'
'show lldp info remote-device 47': """show lldp info remote-device 47
 LLDP Remote Device Information Detail

  Local Port   : 47
  ChassisType  : mac-address         
  ChassisId    : 00 1c 2e bb 34 40        
  PortType     : local  
  PortId       : 45                       
  SysName      : sw00000002                    
  System Descr : ProCurve J9022A Switch 2810-48G, revision N.11.09, ROM N....
  PortDescr    : 45                                                          

  System Capabilities Supported  : bridge
  System Capabilities Enabled    : bridge

  Remote Management Address
     Type    : ipv4
     Address : 172.16.13.130

""",
## 'show lldp info remote-device 48'
'show lldp info remote-device 48': """show lldp info remote-device 48
 LLDP Remote Device Information Detail

  Local Port   : 48
  ChassisType  : mac-address         
  ChassisId    : 00 1c 2e bb 34 40        
  PortType     : local  
  PortId       : 46                       
  SysName      : sw00000002                    
  System Descr : ProCurve J9022A Switch 2810-48G, revision N.11.09, ROM N....
  PortDescr    : 46                                                          

  System Capabilities Supported  : bridge
  System Capabilities Enabled    : bridge

  Remote Management Address
     Type    : ipv4
     Address : 172.16.13.130

""",
'terminal length 1000':  'terminal length ',
## 'show lldp info remote-device 23'
'show lldp info remote-device 23': """show lldp info remote-device 23
 LLDP Remote Device Information Detail

  Local Port   : 23
  ChassisType  : mac-address         
  ChassisId    : 00 1f fe e6 52 40        
  PortType     : local  
  PortId       : 48                       
  SysName      : sw000000001                   
  System Descr : ProCurve J9022A Switch 2810-48G, revision N.11.09, ROM N....
  PortDescr    : 48                                                          

  System Capabilities Supported  : bridge
  System Capabilities Enabled    : bridge

  Remote Management Address
     Type    : ipv4
     Address : 172.16.13.131

""",
## 'show lldp info remote-device 24'
'show lldp info remote-device 24': """show lldp info remote-device 24
 LLDP Remote Device Information Detail

  Local Port   : 24
  ChassisType  : mac-address         
  ChassisId    : 00 1f fe e6 52 40        
  PortType     : local  
  PortId       : 47                       
  SysName      : sw000000001                   
  System Descr : ProCurve J9022A Switch 2810-48G, revision N.11.09, ROM N....
  PortDescr    : 47                                                          

  System Capabilities Supported  : bridge
  System Capabilities Enabled    : bridge

  Remote Management Address
     Type    : ipv4
     Address : 172.16.13.131

""",
}
    snmp_get={}
    snmp_getnext={}
