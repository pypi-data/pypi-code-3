# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Huawei.VRP.get_arp test
## Auto-generated by ./noc debug-script at 11.04.2012 11:49:38
##----------------------------------------------------------------------
## Copyright (C) 2007-2012 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

## NOC modules
from noc.lib.test import ScriptTestCase


class Huawei_VRP_get_arp_Test(ScriptTestCase):
    script = "Huawei.VRP.get_arp"
    vendor = "Huawei"
    platform = "S8512"
    version = "3.10"
    input = {}
    result = [{'interface': 'GigabitEthernet0/1/4',
  'ip': '172.29.245.162',
  'mac': '00:16:C8:BF:FF:80'},
 {'interface': 'GigabitEthernet0/1/23',
  'ip': '10.80.2.34',
  'mac': '00:E0:D8:13:9E:42'},
 {'interface': 'GigabitEthernet0/1/23',
  'ip': '10.80.2.37',
  'mac': '00:E0:D8:15:8B:84'},
 {'interface': 'GigabitEthernet0/1/23',
  'ip': '10.80.2.35',
  'mac': '00:E0:D8:13:9E:53'},
 {'interface': 'GigabitEthernet0/1/16',
  'ip': '172.29.239.74',
  'mac': '00:19:DB:69:55:35'},
 {'interface': 'GigabitEthernet0/1/9',
  'ip': '10.0.37.66',
  'mac': '00:30:48:34:C3:88'},
 {'interface': 'GigabitEthernet0/1/23',
  'ip': '172.29.245.218',
  'mac': '00:07:0E:07:FB:FE'},
 {'interface': 'GigabitEthernet0/1/15',
  'ip': '172.29.245.153',
  'mac': '00:18:82:3C:C4:55'},
 {'interface': 'GigabitEthernet5/1/2',
  'ip': '172.29.245.145',
  'mac': '00:0F:E2:7F:20:C8'},
 {'interface': 'GigabitEthernet5/1/1',
  'ip': '172.29.245.134',
  'mac': '00:0F:E2:7F:21:08'},
 {'interface': 'GigabitEthernet5/1/3',
  'ip': '172.29.245.129',
  'mac': '00:18:82:EF:C8:6A'},
 {'interface': 'GigabitEthernet0/1/23',
  'ip': '172.20.0.2',
  'mac': '00:24:C3:1B:80:43'},
 {'interface': 'GigabitEthernet0/1/5',
  'ip': '10.65.1.2',
  'mac': '00:1E:7A:6E:9B:18'},
 {'interface': 'GigabitEthernet0/1/5',
  'ip': '10.10.100.2',
  'mac': '00:12:CF:41:37:E0'},
 {'interface': 'GigabitEthernet0/1/5',
  'ip': '10.10.100.3',
  'mac': '00:21:59:C4:BD:80'},
 {'interface': 'GigabitEthernet0/1/5',
  'ip': '192.168.36.102',
  'mac': '00:24:1D:3C:0C:74'},
 {'interface': 'GigabitEthernet0/1/5',
  'ip': '192.168.36.101',
  'mac': '00:24:1D:38:8B:D5'},
 {'interface': 'GigabitEthernet0/1/5',
  'ip': '192.168.36.100',
  'mac': '00:24:1D:38:8D:97'},
 {'interface': 'GigabitEthernet0/1/5',
  'ip': '192.168.36.103',
  'mac': '00:1A:4D:FC:86:28'},
 {'interface': 'GigabitEthernet0/1/5',
  'ip': '10.64.1.2',
  'mac': '00:1D:46:87:78:98'},
 {'interface': 'GigabitEthernet0/1/23',
  'ip': '10.80.0.68',
  'mac': '00:17:31:E7:97:F6'},
 {'interface': 'GigabitEthernet0/1/23',
  'ip': '10.80.0.9',
  'mac': '00:12:CF:82:09:09'},
 {'interface': 'GigabitEthernet0/1/23',
  'ip': '10.80.0.54',
  'mac': '00:12:CF:41:3B:C0'},
 {'interface': 'GigabitEthernet0/1/23',
  'ip': '10.80.0.43',
  'mac': '00:12:CF:39:95:90'},
 {'interface': 'GigabitEthernet8/1/1',
  'ip': '10.80.0.50',
  'mac': '00:12:CF:A3:CB:3D'},
 {'interface': 'GigabitEthernet0/1/23',
  'ip': '10.80.0.10',
  'mac': '00:12:CF:71:45:A0'},
 {'interface': 'GigabitEthernet0/1/23',
  'ip': '10.80.0.20',
  'mac': '00:33:33:44:07:48'},
 {'interface': 'GigabitEthernet0/1/23',
  'ip': '10.80.0.61',
  'mac': '00:33:33:44:55:65'},
 {'interface': 'GigabitEthernet0/1/23',
  'ip': '10.80.0.49',
  'mac': '00:23:34:42:BB:42'},
 {'interface': 'GigabitEthernet0/1/23',
  'ip': '10.80.0.16',
  'mac': '00:09:E8:25:63:40'},
 {'interface': 'GigabitEthernet0/1/23',
  'ip': '10.80.0.21',
  'mac': '00:12:CF:14:F9:60'},
 {'interface': 'GigabitEthernet0/1/23',
  'ip': '10.80.0.23',
  'mac': '00:12:CF:14:F8:A0'},
 {'interface': 'GigabitEthernet0/1/23',
  'ip': '10.80.0.35',
  'mac': '00:16:32:C5:64:35'},
 {'interface': 'GigabitEthernet0/1/23',
  'ip': '10.80.0.60',
  'mac': '00:90:E8:1F:09:80'},
 {'interface': 'GigabitEthernet0/1/23',
  'ip': '10.80.0.65',
  'mac': '00:0A:F4:CB:AE:80'},
 {'interface': 'GigabitEthernet0/1/23',
  'ip': '10.80.0.66',
  'mac': '00:12:80:7E:25:40'},
 {'interface': 'GigabitEthernet0/1/23',
  'ip': '10.80.0.36',
  'mac': '00:12:CF:90:DA:20'},
 {'interface': 'GigabitEthernet0/1/23',
  'ip': '10.80.0.46',
  'mac': '00:12:CF:C7:FF:60'},
 {'interface': 'GigabitEthernet0/1/23',
  'ip': '10.80.0.18',
  'mac': '00:12:CF:87:D1:C0'},
 {'interface': 'GigabitEthernet0/1/23',
  'ip': '10.80.0.57',
  'mac': '00:12:CF:96:A7:20'},
 {'interface': 'GigabitEthernet0/1/23',
  'ip': '10.80.0.41',
  'mac': '00:12:CF:F2:98:80'},
 {'interface': 'GigabitEthernet0/1/23',
  'ip': '10.80.0.59',
  'mac': '00:26:5A:BF:C4:5D'},
 {'interface': 'GigabitEthernet0/1/23',
  'ip': '10.80.0.47',
  'mac': '00:12:CF:88:02:40'},
 {'interface': 'GigabitEthernet0/1/23',
  'ip': '10.80.0.44',
  'mac': '00:12:CF:C8:20:C0'},
 {'interface': 'GigabitEthernet0/1/23',
  'ip': '10.80.0.56',
  'mac': '00:12:CF:90:BD:A0'},
 {'interface': 'GigabitEthernet0/1/23',
  'ip': '10.80.0.45',
  'mac': '00:12:CF:C8:0E:80'},
 {'interface': 'GigabitEthernet0/1/23',
  'ip': '10.80.0.26',
  'mac': '00:12:CF:99:D2:40'},
 {'interface': 'GigabitEthernet0/1/23',
  'ip': '10.80.0.32',
  'mac': '00:12:CF:99:67:E0'},
 {'interface': 'GigabitEthernet0/1/23',
  'ip': '10.80.0.25',
  'mac': '00:12:CF:87:DF:60'},
 {'interface': 'GigabitEthernet0/1/23',
  'ip': '10.80.0.52',
  'mac': '00:12:CF:C8:05:A0'},
 {'interface': 'GigabitEthernet0/1/23',
  'ip': '10.80.0.22',
  'mac': '00:12:CF:90:82:A0'},
 {'interface': 'GigabitEthernet0/1/23',
  'ip': '10.80.0.37',
  'mac': '00:12:CF:87:D8:80'},
 {'interface': 'GigabitEthernet0/1/23',
  'ip': '10.80.0.63',
  'mac': '00:12:CF:C8:2A:A0'},
 {'interface': 'GigabitEthernet0/1/23',
  'ip': '10.80.0.34',
  'mac': '00:12:CF:99:74:E0'},
 {'interface': 'GigabitEthernet0/1/23',
  'ip': '10.80.0.29',
  'mac': '00:12:CF:99:75:E0'},
 {'interface': 'GigabitEthernet0/1/23',
  'ip': '10.80.0.27',
  'mac': '00:12:CF:99:D0:20'},
 {'interface': 'GigabitEthernet0/1/23',
  'ip': '10.80.0.55',
  'mac': '00:12:CF:90:DA:A0'},
 {'interface': 'GigabitEthernet0/1/23',
  'ip': '10.80.0.11',
  'mac': '00:12:CF:90:DC:20'},
 {'interface': 'GigabitEthernet0/1/23',
  'ip': '10.80.0.30',
  'mac': '00:12:CF:99:76:E0'},
 {'interface': 'GigabitEthernet0/1/23',
  'ip': '10.80.0.28',
  'mac': '00:12:CF:99:CF:E0'},
 {'interface': 'GigabitEthernet0/1/23',
  'ip': '10.80.0.31',
  'mac': '00:12:CF:99:68:E0'},
 {'interface': 'GigabitEthernet0/1/23',
  'ip': '10.80.0.15',
  'mac': '00:12:CF:87:C4:60'},
 {'interface': 'GigabitEthernet0/1/23',
  'ip': '10.80.0.17',
  'mac': '00:12:CF:87:D2:20'},
 {'interface': 'GigabitEthernet0/1/23',
  'ip': '10.80.0.33',
  'mac': '00:12:CF:90:F5:00'},
 {'interface': 'GigabitEthernet0/1/23',
  'ip': '10.80.0.40',
  'mac': '00:12:CF:4C:01:80'},
 {'interface': 'GigabitEthernet0/1/23',
  'ip': '10.80.0.13',
  'mac': '00:12:CF:4C:57:80'},
 {'interface': 'GigabitEthernet0/1/23',
  'ip': '10.80.0.3',
  'mac': '00:12:CF:4C:64:80'},
 {'interface': 'GigabitEthernet0/1/23',
  'ip': '10.80.0.7',
  'mac': '00:12:CF:4C:6B:C0'},
 {'interface': 'GigabitEthernet0/1/23',
  'ip': '10.80.0.8',
  'mac': '00:12:CF:41:37:C0'},
 {'interface': 'GigabitEthernet0/1/16',
  'ip': '10.0.32.5',
  'mac': '00:12:CF:82:09:09'}]
    motd = '\n'
    cli = {
'screen-length 0 temporary':  "screen-length 0 temporary\n                      ^\n % Unrecognized command found at '^' position.\n", 
## 'display arp'
'display arp': """display arp
            Type: S-Static   D-Dynamic
IP Address       MAC Address     VLAN ID  Port Name                   Aging Type
172.29.245.162   0016-c8bf-ff80  3201     GigabitEthernet0/1/4        18    D
10.80.2.34       00e0-d813-9e42  70       GigabitEthernet0/1/23       13    D
10.80.2.37       00e0-d815-8b84  70       GigabitEthernet0/1/23       17    D
10.80.2.35       00e0-d813-9e53  70       GigabitEthernet0/1/23       18    D
172.29.239.74    0019-db69-5535  6        GigabitEthernet0/1/16       18    D
10.0.37.66       0030-4834-c388  3400     GigabitEthernet0/1/9        20    D
172.29.245.218   0007-0e07-fbfe  2056     GigabitEthernet0/1/23       18    D
172.29.245.153   0018-823c-c455  2007     GigabitEthernet0/1/15       18    D
172.29.245.145   000f-e27f-20c8  2004     GigabitEthernet5/1/2        17    D
172.29.245.134   000f-e27f-2108  2001     GigabitEthernet5/1/1        17    D
172.29.245.129   0018-82ef-c86a  2000     GigabitEthernet5/1/3        11    D
172.20.0.2       0024-c31b-8043  800      GigabitEthernet0/1/23       18    D
10.65.1.2        001e-7a6e-9b18  576      GigabitEthernet0/1/5        18    D    enegromash-hub1
10.10.100.2      0012-cf41-37e0  576      GigabitEthernet0/1/5        18    D    enegromash-hub1
10.10.100.3      0021-59c4-bd80  576      GigabitEthernet0/1/5        19    D    enegromash-hub1
192.168.36.102   0024-1d3c-0c74  574      GigabitEthernet0/1/5        13    D    enegromash-branch7
192.168.36.101   0024-1d38-8bd5  574      GigabitEthernet0/1/5        18    D    enegromash-branch7
192.168.36.100   0024-1d38-8d97  574      GigabitEthernet0/1/5        19    D    enegromash-branch7
192.168.36.103   001a-4dfc-8628  574      GigabitEthernet0/1/5        20    D    enegromash-branch7
10.64.1.2        001d-4687-7898  565      GigabitEthernet0/1/5        18    D    enegromash-hub1
10.80.0.68       0017-31e7-97f6  69       GigabitEthernet0/1/23       12    D
10.80.0.9        0012-cf82-0909  69       GigabitEthernet0/1/23       13    D
10.80.0.54       0012-cf41-3bc0  69       GigabitEthernet0/1/23       16    D
                                          10.80.0.43       0012-cf39-9590  69       GigabitEthernet0/1/23       16    D
10.80.0.50       0012-cfa3-cb3d  69       GigabitEthernet8/1/1        17    D
10.80.0.10       0012-cf71-45a0  69       GigabitEthernet0/1/23       18    D
10.80.0.20       0033-3344-0748  69       GigabitEthernet0/1/23       18    D
10.80.0.61       0033-3344-5565  69       GigabitEthernet0/1/23       18    D
10.80.0.49       0023-3442-bb42  69       GigabitEthernet0/1/23       18    D
10.80.0.16       0009-e825-6340  69       GigabitEthernet0/1/23       18    D
10.80.0.21       0012-cf14-f960  69       GigabitEthernet0/1/23       18    D
10.80.0.23       0012-cf14-f8a0  69       GigabitEthernet0/1/23       19    D
10.80.0.35       0016-32c5-6435  69       GigabitEthernet0/1/23       19    D
10.80.0.60       0090-e81f-0980  69       GigabitEthernet0/1/23       19    D
10.80.0.65       000a-f4cb-ae80  69       GigabitEthernet0/1/23       19    D
10.80.0.66       0012-807e-2540  69       GigabitEthernet0/1/23       19    D
10.80.0.36       0012-cf90-da20  69       GigabitEthernet0/1/23       19    D
10.80.0.46       0012-cfc7-ff60  69       GigabitEthernet0/1/23       19    D
10.80.0.18       0012-cf87-d1c0  69       GigabitEthernet0/1/23       19    D
10.80.0.57       0012-cf96-a720  69       GigabitEthernet0/1/23       19    D
10.80.0.41       0012-cff2-9880  69       GigabitEthernet0/1/23       19    D
10.80.0.59       0026-5abf-c45d  69       GigabitEthernet0/1/23       19    D
10.80.0.47       0012-cf88-0240  69       GigabitEthernet0/1/23       19    D
10.80.0.44       0012-cfc8-20c0  69       GigabitEthernet0/1/23       19    D
10.80.0.56       0012-cf90-bda0  69       GigabitEthernet0/1/23       19    D
                                          10.80.0.45       0012-cfc8-0e80  69       GigabitEthernet0/1/23       19    D
10.80.0.26       0012-cf99-d240  69       GigabitEthernet0/1/23       19    D
10.80.0.32       0012-cf99-67e0  69       GigabitEthernet0/1/23       19    D
10.80.0.25       0012-cf87-df60  69       GigabitEthernet0/1/23       19    D
10.80.0.52       0012-cfc8-05a0  69       GigabitEthernet0/1/23       19    D
10.80.0.22       0012-cf90-82a0  69       GigabitEthernet0/1/23       19    D
10.80.0.37       0012-cf87-d880  69       GigabitEthernet0/1/23       19    D
10.80.0.63       0012-cfc8-2aa0  69       GigabitEthernet0/1/23       19    D
10.80.0.34       0012-cf99-74e0  69       GigabitEthernet0/1/23       19    D
10.80.0.29       0012-cf99-75e0  69       GigabitEthernet0/1/23       19    D
10.80.0.27       0012-cf99-d020  69       GigabitEthernet0/1/23       19    D
10.80.0.55       0012-cf90-daa0  69       GigabitEthernet0/1/23       19    D
10.80.0.11       0012-cf90-dc20  69       GigabitEthernet0/1/23       19    D
10.80.0.30       0012-cf99-76e0  69       GigabitEthernet0/1/23       19    D
10.80.0.28       0012-cf99-cfe0  69       GigabitEthernet0/1/23       19    D
10.80.0.31       0012-cf99-68e0  69       GigabitEthernet0/1/23       19    D
10.80.0.15       0012-cf87-c460  69       GigabitEthernet0/1/23       19    D
10.80.0.17       0012-cf87-d220  69       GigabitEthernet0/1/23       19    D
10.80.0.33       0012-cf90-f500  69       GigabitEthernet0/1/23       19    D
10.80.0.40       0012-cf4c-0180  69       GigabitEthernet0/1/23       19    D
10.80.0.13       0012-cf4c-5780  69       GigabitEthernet0/1/23       20    D
10.80.0.3        0012-cf4c-6480  69       GigabitEthernet0/1/23       20    D
                                          10.80.0.7        0012-cf4c-6bc0  69       GigabitEthernet0/1/23       20    D
10.80.0.8        0012-cf41-37c0  69       GigabitEthernet0/1/23       20    D
10.0.32.5        0012-cf82-0909  11       GigabitEthernet0/1/16       13    D

---   70 entries found   ---""", 
## 'display version'
'display version': """display version
Huawei Versatile Routing Platform Software
VRP software, Version 3.10, Release 1648P01
Copyright(c) 1998-2008 Huawei Technologies Co., Ltd. All rights reserved.
Quidway S8512 uptime is 28 weeks, 4 days, 15 hours, 36 minutes


LSB1SRP1N0 6:  uptime is 28 weeks,4 days,15 hours,36 minutes
Quidway S8500 with 1 MPC755 Processor
512M    bytes SDRAM
16384K  bytes Flash Memory
512K    bytes NVRAM Memory
PCB Version      :   Ver.B
BootROM Version  :   206
CPLD Version     :   001
Software Version :   S8500-VRP310-R1648P01

LSB1SRP1N0 7:  uptime is 28 weeks,4 days,14 hours,34 minutes
Quidway S8500 with 1 MPC755 Processor
512M    bytes SDRAM
16384K  bytes Flash Memory
512K    bytes NVRAM Memory
PCB Version      :   Ver.B
                                          BootROM Version  :   206
CPLD Version     :   001
Software Version :   S8500-VRP310-R1648P01

LSB1GP24CA0 0:  uptime is 28 weeks,4 days,14 hours,34 minutes
Quidway S8500 LPU with 1 MPC8245 Processor
256M    bytes SDRAM
0K      bytes NVRAM Memory
PCB Version      :   Ver.C
BootROM Version  :   109
CPLD Version     :   005
Software Version :   S8500-VRP310-R1648P01
  CPUCard   1
  PCB Ver        :   Ver.C
  CPLD Ver       :   001

LSB1GP24CA0 2:  uptime is 28 weeks,4 days,14 hours,34 minutes
Quidway S8500 LPU with 1 MPC8245 Processor
256M    bytes SDRAM
0K      bytes NVRAM Memory
PCB Version      :   Ver.C
BootROM Version  :   109
CPLD Version     :   005
                                          Software Version :   S8500-VRP310-R1648P01
  CPUCard   1
  PCB Ver        :   Ver.C
  CPLD Ver       :   001

LSB1XP4CA0 5:  uptime is 28 weeks,4 days,14 hours,33 minutes
Quidway S8500 LPU with 1 MPC8245 Processor
256M    bytes SDRAM
0K      bytes NVRAM Memory
PCB Version      :   Ver.E
BootROM Version  :   109
CPLD Version     :   003
Software Version :   S8500-VRP310-R1648P01
  CPUCard   1
  PCB Ver        :   Ver.C
  CPLD Ver       :   001
  SubCard   1
  PCB Ver        :   Ver.B
  CPLD Ver       :   NONE

LSB1XP2CA0 8:  uptime is 28 weeks,4 days,14 hours,34 minutes
Quidway S8500 LPU with 1 MPC8245 Processor
256M    bytes SDRAM
                                          0K      bytes NVRAM Memory
PCB Version      :   Ver.E
BootROM Version  :   109
CPLD Version     :   003
Software Version :   S8500-VRP310-R1648P01
  CPUCard   1
  PCB Ver        :   Ver.C
  CPLD Ver       :   001""", 
}
    snmp_get = {}
    snmp_getnext = {}
    http_get = {}
