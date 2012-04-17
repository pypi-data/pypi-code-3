# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## EdgeCore.ES.get_arp test
## Auto-generated by manage.py debug-script at 2011-02-03 12:10:29
##----------------------------------------------------------------------
## Copyright (C) 2007-2011 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------
from noc.lib.test import ScriptTestCase
class EdgeCore_ES_get_arp_Test(ScriptTestCase):
    script="EdgeCore.ES.get_arp"
    vendor="EdgeCore"
    platform='ES4626-SFP'
    version='6.0.220.33'
    input={}
    result=[{'interface': 'Vlan624', 'ip': '10.50.24.64', 'mac': '00:1F:C6:33:73:D8'},
 {'interface': 'Vlan624', 'ip': '10.50.24.65', 'mac': '00:16:17:D5:18:45'},
 {'interface': 'Vlan624', 'ip': '10.50.24.69', 'mac': '00:16:17:99:BA:B1'},
 {'interface': 'Vlan624', 'ip': '10.50.24.71', 'mac': '00:26:5A:A3:00:71'},
 {'interface': 'Vlan624', 'ip': '10.50.24.80', 'mac': '00:11:6B:1E:86:0F'},
 {'interface': 'Vlan624', 'ip': '10.50.24.83', 'mac': '00:1B:38:25:2B:37'},
 {'interface': 'Vlan624', 'ip': '10.50.24.89', 'mac': '00:90:F5:8D:9D:F7'},
 {'interface': 'Vlan624', 'ip': '10.50.24.102', 'mac': '00:1E:EC:2B:2B:0C'},
 {'interface': 'Vlan624', 'ip': '10.50.24.126', 'mac': '1C:BD:B9:93:D5:93'},
 {'interface': 'Vlan624', 'ip': '10.50.24.130', 'mac': '00:18:F3:33:23:6D'},
 {'interface': 'Vlan624', 'ip': '10.50.24.199', 'mac': '00:1F:C6:A7:8A:6E'},
 {'interface': 'Vlan624', 'ip': '10.50.24.207', 'mac': '00:1C:F0:E3:79:44'},
 {'interface': 'Vlan624', 'ip': '10.50.25.20', 'mac': '00:26:18:08:CC:7C'},
 {'interface': 'Vlan624', 'ip': '10.50.27.247', 'mac': '00:13:46:26:B5:76'},
 {'interface': 'Vlan624', 'ip': '10.50.27.251', 'mac': '00:30:4F:46:57:25'},
 {'interface': 'Vlan100', 'ip': '10.228.160.4', 'mac': '00:15:E9:41:87:79'},
 {'interface': 'Vlan100', 'ip': '10.228.160.10', 'mac': '6C:F0:49:E3:18:7A'},
 {'interface': 'Vlan100', 'ip': '10.228.160.65', 'mac': '00:22:15:D9:4B:60'},
 {'interface': 'Vlan100', 'ip': '10.228.160.66', 'mac': '90:E6:BA:3B:87:B1'},
 {'interface': 'Vlan100', 'ip': '10.228.160.70', 'mac': '90:E6:BA:EF:9E:B6'},
 {'interface': 'Vlan100', 'ip': '10.228.160.77', 'mac': '00:1F:16:AA:36:6A'},
 {'interface': 'Vlan101', 'ip': '10.228.161.4', 'mac': '00:11:5B:71:67:F5'},
 {'interface': 'Vlan101', 'ip': '10.228.161.11', 'mac': '00:16:E6:5F:71:23'},
 {'interface': 'Vlan101', 'ip': '10.228.161.51', 'mac': '20:CF:30:3A:59:AF'},
 {'interface': 'Vlan101', 'ip': '10.228.161.55', 'mac': '00:0F:EA:5F:3C:B4'},
 {'interface': 'Vlan101', 'ip': '10.228.161.56', 'mac': '00:23:54:73:3A:A9'},
 {'interface': 'Vlan101', 'ip': '10.228.161.62', 'mac': '00:04:61:4B:4D:51'},
 {'interface': 'Vlan101', 'ip': '10.228.161.63', 'mac': '00:24:1D:8C:FA:19'},
 {'interface': 'Vlan101', 'ip': '10.228.161.68', 'mac': '40:61:86:C3:AD:5B'},
 {'interface': 'Vlan101', 'ip': '10.228.161.71', 'mac': '00:1A:80:F0:71:1F'},
 {'interface': 'Vlan102', 'ip': '10.228.162.8', 'mac': '00:1D:09:49:17:12'},
 {'interface': 'Vlan102', 'ip': '10.228.162.16', 'mac': '00:17:31:14:13:ED'},
 {'interface': 'Vlan102', 'ip': '10.228.162.52', 'mac': '00:26:18:0F:C9:DA'},
 {'interface': 'Vlan102', 'ip': '10.228.162.56', 'mac': '00:90:F5:8C:D0:CD'},
 {'interface': 'Vlan102', 'ip': '10.228.162.62', 'mac': '48:5B:39:44:B1:BA'},
 {'interface': 'Vlan102', 'ip': '10.228.162.64', 'mac': '00:16:D4:16:A5:7E'},
 {'interface': 'Vlan102', 'ip': '10.228.162.66', 'mac': '00:15:C5:6E:88:E8'},
 {'interface': 'Vlan102', 'ip': '10.228.162.69', 'mac': '00:19:DB:64:33:8E'},
 {'interface': 'Vlan102', 'ip': '10.228.162.71', 'mac': '00:24:1D:C8:CB:8D'},
 {'interface': 'Vlan102', 'ip': '10.228.162.72', 'mac': '00:0D:61:97:44:5B'},
 {'interface': 'Vlan102', 'ip': '10.228.162.73', 'mac': '20:CF:30:2E:AC:00'},
 {'interface': 'Vlan103', 'ip': '10.228.163.19', 'mac': '00:1E:8C:38:AC:5A'},
 {'interface': 'Vlan103', 'ip': '10.228.163.20', 'mac': '00:1E:58:AF:3F:B7'},
 {'interface': 'Vlan103', 'ip': '10.228.163.55', 'mac': '00:17:31:7E:CF:21'},
 {'interface': 'Vlan103', 'ip': '10.228.163.66', 'mac': '00:11:2F:B2:7E:77'},
 {'interface': 'Vlan103', 'ip': '10.228.163.67', 'mac': '00:E0:4D:07:A4:92'},
 {'interface': 'Vlan104', 'ip': '10.228.164.51', 'mac': '00:1E:58:AA:AA:9A'},
 {'interface': 'Vlan104', 'ip': '10.228.164.54', 'mac': '00:22:15:01:16:25'},
 {'interface': 'Vlan104', 'ip': '10.228.164.55', 'mac': '40:61:86:33:AA:F0'},
 {'interface': 'Vlan104', 'ip': '10.228.164.59', 'mac': '00:22:15:61:2E:08'},
 {'interface': 'Vlan105', 'ip': '10.228.165.52', 'mac': '00:1F:D0:24:E7:85'},
 {'interface': 'Vlan105', 'ip': '10.228.165.54', 'mac': '48:5B:39:A6:68:42'},
 {'interface': 'Vlan105', 'ip': '10.228.165.57', 'mac': '00:18:F3:AA:66:8C'},
 {'interface': 'Vlan105', 'ip': '10.228.165.59', 'mac': '00:11:6B:18:4B:0B'},
 {'interface': 'Vlan105', 'ip': '10.228.165.71', 'mac': '00:1E:8C:02:16:79'},
 {'interface': 'Vlan105', 'ip': '10.228.165.75', 'mac': '00:22:B0:50:EE:D2'},
 {'interface': 'Vlan105', 'ip': '10.228.165.77', 'mac': '00:26:22:49:25:B3'},
 {'interface': 'Vlan105', 'ip': '10.228.165.78', 'mac': '90:E6:BA:1E:06:B2'},
 {'interface': 'Vlan105', 'ip': '10.228.165.80', 'mac': '00:24:01:C6:CA:59'},
 {'interface': 'Vlan105', 'ip': '10.228.165.84', 'mac': '00:1A:92:B0:E3:A1'},
 {'interface': 'Vlan105', 'ip': '10.228.165.93', 'mac': '00:1A:92:63:49:38'},
 {'interface': 'Vlan105', 'ip': '10.228.165.95', 'mac': 'C8:0A:A9:82:7E:BC'},
 {'interface': 'Vlan105', 'ip': '10.228.165.96', 'mac': '00:26:22:21:E2:27'},
 {'interface': 'Vlan105', 'ip': '10.228.165.97', 'mac': '00:02:B3:4C:DB:76'},
 {'interface': 'Vlan106', 'ip': '10.228.166.2', 'mac': '00:1C:F0:E0:89:9B'},
 {'interface': 'Vlan106', 'ip': '10.228.166.51', 'mac': '00:1E:8C:7C:72:18'},
 {'interface': 'Vlan106', 'ip': '10.228.166.52', 'mac': '00:01:6C:11:FA:CB'},
 {'interface': 'Vlan106', 'ip': '10.228.166.54', 'mac': '00:13:77:6B:4B:A8'},
 {'interface': 'Vlan106', 'ip': '10.228.166.59', 'mac': '00:04:61:AF:42:7D'},
 {'interface': 'Vlan106', 'ip': '10.228.166.63', 'mac': '00:18:F3:08:AD:26'},
 {'interface': 'Vlan106', 'ip': '10.228.166.65', 'mac': '00:18:DE:9E:53:62'},
 {'interface': 'Vlan106', 'ip': '10.228.166.66', 'mac': '54:42:49:0A:78:E1'},
 {'interface': 'Vlan106', 'ip': '10.228.166.68', 'mac': '00:17:9A:67:8B:54'},
 {'interface': 'Vlan109', 'ip': '10.228.169.27', 'mac': '00:1B:FC:89:D5:A1'},
 {'interface': 'Vlan109', 'ip': '10.228.169.34', 'mac': '00:21:85:73:A1:02'},
 {'interface': 'Vlan109', 'ip': '10.228.169.58', 'mac': '00:21:5D:0E:EB:28'},
 {'interface': 'Vlan109', 'ip': '10.228.169.61', 'mac': 'E0:CB:4E:E4:D2:3C'},
 {'interface': 'Vlan109', 'ip': '10.228.169.63', 'mac': '00:19:5B:E9:AB:A5'},
 {'interface': 'Vlan109', 'ip': '10.228.169.66', 'mac': '00:22:15:22:4C:40'},
 {'interface': 'Vlan109', 'ip': '10.228.169.79', 'mac': '00:11:09:83:F8:EF'},
 {'interface': 'Vlan109', 'ip': '10.228.169.120', 'mac': '00:23:8B:EE:A7:B3'},
 {'interface': 'Vlan109', 'ip': '10.228.169.169', 'mac': '00:13:46:E7:CC:A4'},
 {'interface': 'Vlan110', 'ip': '10.228.170.15', 'mac': '00:25:22:0C:22:E1'},
 {'interface': 'Vlan110', 'ip': '10.228.170.20', 'mac': '00:0F:B0:08:93:81'},
 {'interface': 'Vlan110', 'ip': '10.228.170.43', 'mac': '00:A0:CC:78:FD:5D'},
 {'interface': 'Vlan110', 'ip': '10.228.170.52', 'mac': '00:24:8C:95:97:A7'},
 {'interface': 'Vlan110', 'ip': '10.228.170.53', 'mac': '00:50:8D:5A:A3:CC'},
 {'interface': 'Vlan110', 'ip': '10.228.170.54', 'mac': '00:04:61:98:AC:25'},
 {'interface': 'Vlan110', 'ip': '10.228.170.55', 'mac': '00:E0:4D:01:F6:43'},
 {'interface': 'Vlan110', 'ip': '10.228.170.56', 'mac': '00:1A:4D:58:67:6D'},
 {'interface': 'Vlan110', 'ip': '10.228.170.63', 'mac': '00:E0:4C:81:5C:56'},
 {'interface': 'Vlan110', 'ip': '10.228.170.64', 'mac': '00:01:6C:EC:D6:79'},
 {'interface': 'Vlan110', 'ip': '10.228.170.67', 'mac': '00:19:DB:C4:34:3A'},
 {'interface': 'Vlan110', 'ip': '10.228.170.245', 'mac': '00:0E:A6:CB:A5:E0'},
 {'interface': 'Vlan111', 'ip': '10.228.171.9', 'mac': '00:1D:60:24:96:96'},
 {'interface': 'Vlan111', 'ip': '10.228.171.55', 'mac': '00:13:8F:38:B6:9D'},
 {'interface': 'Vlan111', 'ip': '10.228.171.59', 'mac': '00:16:D4:D0:D1:3F'},
 {'interface': 'Vlan111', 'ip': '10.228.171.63', 'mac': '00:16:E6:67:C1:50'},
 {'interface': 'Vlan111', 'ip': '10.228.171.66', 'mac': 'E0:CB:4E:56:95:E1'},
 {'interface': 'Vlan112', 'ip': '10.228.172.7', 'mac': '00:1C:25:0E:5C:38'},
 {'interface': 'Vlan112', 'ip': '10.228.172.9', 'mac': '00:16:76:C2:6A:29'},
 {'interface': 'Vlan112', 'ip': '10.228.172.11', 'mac': '00:1E:8C:70:35:2A'},
 {'interface': 'Vlan112', 'ip': '10.228.172.13', 'mac': '00:19:DB:66:8A:23'},
 {'interface': 'Vlan112', 'ip': '10.228.172.14', 'mac': '1C:AF:F7:AB:B8:41'},
 {'interface': 'Vlan112', 'ip': '10.228.172.55', 'mac': '00:15:58:47:A3:22'},
 {'interface': 'Vlan112', 'ip': '10.228.172.246', 'mac': '00:1D:7E:FB:8D:21'},
 {'interface': 'Vlan112', 'ip': '10.228.172.250', 'mac': '00:16:76:C2:6A:29'},
 {'interface': 'Vlan112', 'ip': '10.228.172.253', 'mac': '00:19:E3:37:E5:0B'},
 {'interface': 'Vlan112', 'ip': '10.228.172.254', 'mac': '00:13:46:26:EE:53'},
 {'interface': 'Vlan113', 'ip': '10.228.173.52', 'mac': '74:EA:3A:A9:7E:C5'},
 {'interface': 'Vlan113', 'ip': '10.228.173.53', 'mac': 'F0:7D:68:45:72:51'},
 {'interface': 'Vlan114', 'ip': '10.228.174.53', 'mac': '00:1E:68:5B:8C:5E'},
 {'interface': 'Vlan114', 'ip': '10.228.174.55', 'mac': '00:19:66:98:DE:B3'},
 {'interface': 'Vlan114', 'ip': '10.228.174.59', 'mac': '00:1A:4D:57:15:B4'},
 {'interface': 'Vlan114', 'ip': '10.228.174.62', 'mac': '60:EB:69:46:C4:FB'},
 {'interface': 'Vlan116', 'ip': '10.228.176.58', 'mac': '00:21:27:C4:A7:29'},
 {'interface': 'Vlan116', 'ip': '10.228.176.61', 'mac': '00:11:95:CB:FB:5A'},
 {'interface': 'Vlan116', 'ip': '10.228.176.64', 'mac': '00:15:58:8C:4B:AF'},
 {'interface': 'Vlan116', 'ip': '10.228.176.65', 'mac': '00:1D:09:4E:42:8B'},
 {'interface': 'Vlan116', 'ip': '10.228.176.66', 'mac': '6C:F0:49:0D:08:48'},
 {'interface': 'Vlan116', 'ip': '10.228.176.67', 'mac': '00:24:01:AD:18:90'},
 {'interface': 'Vlan116', 'ip': '10.228.176.68', 'mac': '00:1E:EC:4A:C5:74'},
 {'interface': 'Vlan803', 'ip': '172.16.1.17', 'mac': '00:12:CF:95:00:03'},
 {'interface': 'Vlan900', 'ip': '172.16.68.2', 'mac': '00:12:CF:87:DD:80'},
 {'interface': 'Vlan900', 'ip': '172.16.68.3', 'mac': '00:12:CF:87:96:E0'},
 {'interface': 'Vlan900', 'ip': '172.16.68.4', 'mac': '00:12:CF:88:01:00'},
 {'interface': 'Vlan900', 'ip': '172.16.68.5', 'mac': '00:12:CF:87:CE:00'},
 {'interface': 'Vlan900', 'ip': '172.16.68.6', 'mac': '00:12:CF:90:C4:C0'},
 {'interface': 'Vlan900', 'ip': '172.16.68.7', 'mac': '00:12:CF:90:C7:00'},
 {'interface': 'Vlan900', 'ip': '172.16.68.8', 'mac': '00:12:CF:90:C5:40'},
 {'interface': 'Vlan900', 'ip': '172.16.68.11', 'mac': '00:12:CF:90:CB:40'},
 {'interface': 'Vlan900', 'ip': '172.16.68.13', 'mac': '00:12:CF:90:89:60'},
 {'interface': 'Vlan900', 'ip': '172.16.68.14', 'mac': '00:12:CF:90:8B:A0'},
 {'interface': 'Vlan900', 'ip': '172.16.68.15', 'mac': '00:12:CF:90:85:A0'},
 {'interface': 'Vlan900', 'ip': '172.16.68.16', 'mac': '00:12:CF:F7:E0:20'},
 {'interface': 'Vlan900', 'ip': '172.16.68.17', 'mac': '00:12:CF:F2:98:20'},
 {'interface': 'Vlan900', 'ip': '172.16.68.19', 'mac': '00:12:CF:90:D5:20'},
 {'interface': 'Vlan900', 'ip': '172.16.68.20', 'mac': '00:12:CF:4C:EE:80'},
 {'interface': 'Vlan900', 'ip': '172.16.68.21', 'mac': '00:12:CF:90:CB:A0'},
 {'interface': 'Vlan900', 'ip': '172.16.68.22', 'mac': '00:12:CF:99:99:40'},
 {'interface': 'Vlan900', 'ip': '172.16.68.23', 'mac': '00:12:CF:99:85:40'},
 {'interface': 'Vlan900', 'ip': '172.16.68.25', 'mac': '00:12:CF:90:90:20'},
 {'interface': 'Vlan900', 'ip': '172.16.68.26', 'mac': '00:12:CF:87:B7:A0'},
 {'interface': 'Vlan900', 'ip': '172.16.68.27', 'mac': '00:12:CF:87:C9:00'},
 {'interface': 'Vlan900', 'ip': '172.16.68.28', 'mac': '00:12:CF:4C:D7:20'},
 {'interface': 'Vlan900', 'ip': '172.16.68.29', 'mac': '00:12:CF:99:D1:A0'},
 {'interface': 'Vlan900', 'ip': '172.16.68.30', 'mac': '00:12:CF:8A:EF:F0'},
 {'interface': 'Vlan900', 'ip': '172.16.68.31', 'mac': '00:1B:11:6F:EC:29'},
 {'interface': 'Vlan900', 'ip': '172.16.68.32', 'mac': '00:1B:11:6F:E4:0F'},
 {'interface': 'Vlan900', 'ip': '172.16.68.33', 'mac': '00:1B:11:6F:EA:5F'},
 {'interface': 'Vlan900', 'ip': '172.16.68.34', 'mac': '00:1B:11:6F:E4:83'},
 {'interface': 'Vlan900', 'ip': '172.16.68.35', 'mac': '00:1B:11:6F:E9:DC'},
 {'interface': 'Vlan900', 'ip': '172.16.68.36', 'mac': '00:12:CF:87:D8:60'},
 {'interface': 'Vlan900', 'ip': '172.16.68.37', 'mac': '00:12:CF:87:FC:00'},
 {'interface': 'Vlan900', 'ip': '172.16.68.38', 'mac': '00:12:CF:C5:F1:20'},
 {'interface': 'Vlan900', 'ip': '172.16.68.125', 'mac': '00:E0:D8:13:9E:D2'},
 {'interface': 'Vlan900', 'ip': '172.16.68.126', 'mac': '00:E0:D8:13:9D:85'}]
    motd='********\n'
    cli={
## 'show version 1'
'show version 1': """show version 1
  ES4626-SFP Device, Compiled on Apr 23 14:41:49 2010
  SoftWare Version ES4626-SFP_6.0.220.33
  BootRom Version ES4626-SFP_1.7.0
  HardWare Version 3.0
  Copyright (C) 2001-2007 by Accton Technology Corp.
  All rights reserved
  Uptime is 6 weeks, 5 days, 16 hours, 24 minutes""",
## 'show arp'
'show arp': """show arp
ARP Unicast Items: 248, Valid: 157, Matched: 157, Verifying: 0, Incomplete: 1, Failed: 88, None: 0
Address          Hardware Addr      Interface     Port            Flag      Age-time(sec)
10.50.24.64      00-1f-c6-33-73-d8  Vlan624       Ethernet1/23    Dynamic   784       
10.50.24.65      00-16-17-d5-18-45  Vlan624       Ethernet1/23    Dynamic   329       
10.50.24.69      00-16-17-99-ba-b1  Vlan624       Ethernet1/23    Dynamic   573       
10.50.24.71      00-26-5a-a3-00-71  Vlan624       Ethernet1/23    Dynamic   183       
10.50.24.80      00-11-6b-1e-86-0f  Vlan624       Ethernet1/23    Dynamic   243       
10.50.24.83      00-1b-38-25-2b-37  Vlan624       Ethernet1/23    Dynamic   183       
10.50.24.89      00-90-f5-8d-9d-f7  Vlan624       Ethernet1/23    Dynamic   1114      
10.50.24.102     00-1e-ec-2b-2b-0c  Vlan624       Ethernet1/23    Dynamic   647       
10.50.24.126     1c-bd-b9-93-d5-93  Vlan624       Ethernet1/23    Dynamic   3         
10.50.24.130     00-18-f3-33-23-6d  Vlan624       Ethernet1/23    Dynamic   874       
10.50.24.199     00-1f-c6-a7-8a-6e  Vlan624       Ethernet1/23    Dynamic   1103      
10.50.24.207     00-1c-f0-e3-79-44  Vlan624       Ethernet1/23    Dynamic   904       
10.50.25.20      00-26-18-08-cc-7c  Vlan624       Ethernet1/23    Dynamic   1193      
10.50.27.247     00-13-46-26-b5-76  Vlan624       Ethernet1/23    Dynamic   423       
10.50.27.251     00-30-4f-46-57-25  Vlan624       Ethernet1/23    Dynamic   303       
10.228.160.4     00-15-e9-41-87-79  Vlan100       Ethernet1/18    Dynamic   757       
10.228.160.10    6c-f0-49-e3-18-7a  Vlan100       Ethernet1/18    Dynamic   153       
10.228.160.65    00-22-15-d9-4b-60  Vlan100       Ethernet1/18    Dynamic   603       
10.228.160.66    90-e6-ba-3b-87-b1  Vlan100       Ethernet1/18    Dynamic   754       
10.228.160.70    90-e6-ba-ef-9e-b6  Vlan100       Ethernet1/18    Dynamic   633       
10.228.160.77    00-1f-16-aa-36-6a  Vlan100       Ethernet1/18    Dynamic   373       
10.228.161.4     00-11-5b-71-67-f5  Vlan101       Ethernet1/19    Dynamic   1144      
10.228.161.11    00-16-e6-5f-71-23  Vlan101       Ethernet1/19    Dynamic   1161      
10.228.161.51    20-cf-30-3a-59-af  Vlan101       Ethernet1/19    Dynamic   670       
10.228.161.55    00-0f-ea-5f-3c-b4  Vlan101       Ethernet1/19    Dynamic   24        
10.228.161.56    00-23-54-73-3a-a9  Vlan101       Ethernet1/19    Dynamic   543       
10.228.161.62    00-04-61-4b-4d-51  Vlan101       Ethernet1/19    Dynamic   575       
10.228.161.63    00-24-1d-8c-fa-19  Vlan101       Ethernet1/19    Dynamic   543       
10.228.161.68    40-61-86-c3-ad-5b  Vlan101       Ethernet1/19    Dynamic   543       
10.228.161.71    00-1a-80-f0-71-1f  Vlan101       Ethernet1/19    Dynamic   123       
10.228.162.8     00-1d-09-49-17-12  Vlan102       Ethernet1/9     Dynamic   603       
10.228.162.16    00-17-31-14-13-ed  Vlan102       Ethernet1/9     Dynamic   1023      
10.228.162.52    00-26-18-0f-c9-da  Vlan102       Ethernet1/9     Dynamic   3         
10.228.162.56    00-90-f5-8c-d0-cd  Vlan102       Ethernet1/9     Dynamic   213       
10.228.162.62    48-5b-39-44-b1-ba  Vlan102       Ethernet1/9     Dynamic   393       
10.228.162.64    00-16-d4-16-a5-7e  Vlan102       Ethernet1/9     Dynamic   814       
10.228.162.66    00-15-c5-6e-88-e8  Vlan102       Ethernet1/9     Dynamic   543       
10.228.162.69    00-19-db-64-33-8e  Vlan102       Ethernet1/9     Dynamic   844       
10.228.162.71    00-24-1d-c8-cb-8d  Vlan102       Ethernet1/9     Dynamic   1024      
10.228.162.72    00-0d-61-97-44-5b  Vlan102       Ethernet1/9     Dynamic   33        
10.228.162.73    20-cf-30-2e-ac-00  Vlan102       Ethernet1/9     Dynamic   123       
10.228.163.19    00-1e-8c-38-ac-5a  Vlan103       Ethernet1/4     Dynamic   874       
10.228.163.20    00-1e-58-af-3f-b7  Vlan103       Ethernet1/4     Dynamic   633       
10.228.163.55    00-17-31-7e-cf-21  Vlan103       Ethernet1/4     Dynamic   663       
10.228.163.66    00-11-2f-b2-7e-77  Vlan103       Ethernet1/4     Dynamic   1024      
10.228.163.67    00-e0-4d-07-a4-92  Vlan103       Ethernet1/4     Dynamic   1054      
10.228.164.51    00-1e-58-aa-aa-9a  Vlan104       Ethernet1/5     Dynamic   93        
10.228.164.54    00-22-15-01-16-25  Vlan104       Ethernet1/5     Dynamic   784       
10.228.164.55    40-61-86-33-aa-f0  Vlan104       Ethernet1/5     Dynamic   954       
10.228.164.59    00-22-15-61-2e-08  Vlan104       Ethernet1/5     Dynamic   573       
10.228.165.52    00-1f-d0-24-e7-85  Vlan105       Ethernet1/6     Dynamic   123       
10.228.165.54    48-5b-39-a6-68-42  Vlan105       Ethernet1/6     Dynamic   934       
10.228.165.57    00-18-f3-aa-66-8c  Vlan105       Ethernet1/6     Dynamic   1174      
10.228.165.59    00-11-6b-18-4b-0b  Vlan105       Ethernet1/6     Dynamic   573       
10.228.165.71    00-1e-8c-02-16-79  Vlan105       Ethernet1/6     Dynamic   363       
10.228.165.75    00-22-b0-50-ee-d2  Vlan105       Ethernet1/6     Dynamic   1133      
10.228.165.77    00-26-22-49-25-b3  Vlan105       Ethernet1/6     Dynamic   784       
10.228.165.78    90-e6-ba-1e-06-b2  Vlan105       Ethernet1/6     Dynamic   183       
10.228.165.80    00-24-01-c6-ca-59  Vlan105       Ethernet1/6     Dynamic   1144      
10.228.165.84    00-1a-92-b0-e3-a1  Vlan105       Ethernet1/6     Dynamic   333       
10.228.165.93    00-1a-92-63-49-38  Vlan105       Ethernet1/6     Dynamic   1135      
10.228.165.95    c8-0a-a9-82-7e-bc  Vlan105       Ethernet1/6     Dynamic   453       
10.228.165.96    00-26-22-21-e2-27  Vlan105       Ethernet1/6     Dynamic   904       
10.228.165.97    00-02-b3-4c-db-76  Vlan105       Ethernet1/6     Dynamic   573       
10.228.166.2     00-1c-f0-e0-89-9b  Vlan106       Ethernet1/20    Dynamic   183       
10.228.166.51    00-1e-8c-7c-72-18  Vlan106       Ethernet1/20    Dynamic   393       
10.228.166.52    00-01-6c-11-fa-cb  Vlan106       Ethernet1/20    Dynamic   603       
10.228.166.54    00-13-77-6b-4b-a8  Vlan106       Ethernet1/20    Dynamic   453       
10.228.166.59    00-04-61-af-42-7d  Vlan106       Ethernet1/20    Dynamic   1035      
10.228.166.63    00-18-f3-08-ad-26  Vlan106       Ethernet1/20    Dynamic   573       
10.228.166.65    00-18-de-9e-53-62  Vlan106       Ethernet1/20    Dynamic   1187      
10.228.166.66    54-42-49-0a-78-e1  Vlan106       Ethernet1/20    Dynamic   453       
10.228.166.68    00-17-9a-67-8b-54  Vlan106       Ethernet1/20    Dynamic   1193      
10.228.169.27    00-1b-fc-89-d5-a1  Vlan109       Ethernet1/10    Dynamic   1159      
10.228.169.34    00-21-85-73-a1-02  Vlan109       Ethernet1/10    Dynamic   724       
10.228.169.58    00-21-5d-0e-eb-28  Vlan109       Ethernet1/10    Dynamic   964       
10.228.169.61    e0-cb-4e-e4-d2-3c  Vlan109       Ethernet1/10    Dynamic   934       
10.228.169.63    00-19-5b-e9-ab-a5  Vlan109       Ethernet1/10    Dynamic   927       
10.228.169.66    00-22-15-22-4c-40  Vlan109       Ethernet1/10    Dynamic   874       
10.228.169.79    00-11-09-83-f8-ef  Vlan109       Ethernet1/10    Dynamic   694       
10.228.169.120   00-23-8b-ee-a7-b3  Vlan109       Ethernet1/10    Dynamic   1024      
10.228.169.169   00-13-46-e7-cc-a4  Vlan109       Ethernet1/10    Dynamic   423       
10.228.170.15    00-25-22-0c-22-e1  Vlan110       Ethernet1/11    Dynamic   510       
10.228.170.20    00-0f-b0-08-93-81  Vlan110       Ethernet1/11    Dynamic   1153      
10.228.170.43    00-a0-cc-78-fd-5d  Vlan110       Ethernet1/11    Dynamic   663       
10.228.170.52    00-24-8c-95-97-a7  Vlan110       Ethernet1/11    Dynamic   363       
10.228.170.53    00-50-8d-5a-a3-cc  Vlan110       Ethernet1/11    Dynamic   212       
10.228.170.54    00-04-61-98-ac-25  Vlan110       Ethernet1/11    Dynamic   603       
10.228.170.55    00-e0-4d-01-f6-43  Vlan110       Ethernet1/11    Dynamic   1170      
10.228.170.56    00-1a-4d-58-67-6d  Vlan110       Ethernet1/11    Dynamic   1161      
10.228.170.63    00-e0-4c-81-5c-56  Vlan110       Ethernet1/11    Dynamic   453       
10.228.170.64    00-01-6c-ec-d6-79  Vlan110       Ethernet1/11    Dynamic   1024      
10.228.170.67    00-19-db-c4-34-3a  Vlan110       Ethernet1/11    Dynamic   633       
10.228.170.245   00-0e-a6-cb-a5-e0  Vlan110       Ethernet1/11    Dynamic   1186      
10.228.171.9     00-1d-60-24-96-96  Vlan111       Ethernet1/12    Dynamic   663       
10.228.171.55    00-13-8f-38-b6-9d  Vlan111       Ethernet1/12    Dynamic   1197      
10.228.171.59    00-16-d4-d0-d1-3f  Vlan111       Ethernet1/12    Dynamic   33        
10.228.171.63    00-16-e6-67-c1-50  Vlan111       Ethernet1/12    Dynamic   363       
10.228.171.66    e0-cb-4e-56-95-e1  Vlan111       Ethernet1/12    Dynamic   994       
10.228.172.7     00-1c-25-0e-5c-38  Vlan112       Ethernet1/13    Dynamic   33        
10.228.172.9     00-16-76-c2-6a-29  Vlan112       Ethernet1/13    Dynamic   543       
10.228.172.11    00-1e-8c-70-35-2a  Vlan112       Ethernet1/13    Dynamic   874       
10.228.172.13    00-19-db-66-8a-23  Vlan112       Ethernet1/13    Dynamic   1191      
10.228.172.14    1c-af-f7-ab-b8-41  Vlan112       Ethernet1/13    Dynamic   333       
10.228.172.55    00-15-58-47-a3-22  Vlan112       Ethernet1/13    Dynamic   123       
10.228.172.246   00-1d-7e-fb-8d-21  Vlan112       Ethernet1/13    Dynamic   994       
10.228.172.250   00-16-76-c2-6a-29  Vlan112       Ethernet1/13    Dynamic   603       
10.228.172.253   00-19-e3-37-e5-0b  Vlan112       Ethernet1/13    Dynamic   844       
10.228.172.254   00-13-46-26-ee-53  Vlan112       Ethernet1/13    Dynamic   964       
10.228.173.52    74-ea-3a-a9-7e-c5  Vlan113       Ethernet1/16    Dynamic   934       
10.228.173.53    f0-7d-68-45-72-51  Vlan113       Ethernet1/16    Dynamic   1154      
10.228.174.53    00-1e-68-5b-8c-5e  Vlan114       Ethernet1/23    Dynamic   1122      
10.228.174.55    00-19-66-98-de-b3  Vlan114       Ethernet1/23    Dynamic   453       
10.228.174.59    00-1a-4d-57-15-b4  Vlan114       Ethernet1/21    Dynamic   844       
10.228.174.62    60-eb-69-46-c4-fb  Vlan114       Ethernet1/23    Dynamic   1183      
10.228.176.58    00-21-27-c4-a7-29  Vlan116       Ethernet1/17    Dynamic   1024      
10.228.176.61    00-11-95-cb-fb-5a  Vlan116       Ethernet1/17    Dynamic   814       
10.228.176.64    00-15-58-8c-4b-af  Vlan116       Ethernet1/17    Dynamic   663       
10.228.176.65    00-1d-09-4e-42-8b  Vlan116       Ethernet1/17    Dynamic   386       
10.228.176.66    6c-f0-49-0d-08-48  Vlan116       Ethernet1/17    Dynamic   63        
10.228.176.67    00-24-01-ad-18-90  Vlan116       Ethernet1/17    Dynamic   33        
10.228.176.68    00-1e-ec-4a-c5-74  Vlan116       Ethernet1/17    Dynamic   1185      
172.16.1.17      00-12-cf-95-00-03  Vlan803       Ethernet1/24    Dynamic   1198      
172.16.68.2      00-12-cf-87-dd-80  Vlan900       Ethernet1/18    Dynamic   393       
172.16.68.3      00-12-cf-87-96-e0  Vlan900       Ethernet1/19    Dynamic   633       
172.16.68.4      00-12-cf-88-01-00  Vlan900       Ethernet1/9     Dynamic   3         
172.16.68.5      00-12-cf-87-ce-00  Vlan900       Ethernet1/4     Dynamic   964       
172.16.68.6      00-12-cf-90-c4-c0  Vlan900       Ethernet1/5     Dynamic   633       
172.16.68.7      00-12-cf-90-c7-00  Vlan900       Ethernet1/6     Dynamic   814       
172.16.68.8      00-12-cf-90-c5-40  Vlan900       Ethernet1/20    Dynamic   1174      
172.16.68.11     00-12-cf-90-cb-40  Vlan900       Ethernet1/10    Dynamic   213       
172.16.68.13     00-12-cf-90-89-60  Vlan900       Ethernet1/12    Dynamic   1024      
172.16.68.14     00-12-cf-90-8b-a0  Vlan900       Ethernet1/13    Dynamic   1024      
172.16.68.15     00-12-cf-90-85-a0  Vlan900       Ethernet1/13    Dynamic   964       
172.16.68.16     00-12-cf-f7-e0-20  Vlan900       Ethernet1/16    Dynamic   1144      
172.16.68.17     00-12-cf-f2-98-20  Vlan900       Ethernet1/23    Dynamic   754       
172.16.68.19     00-12-cf-90-d5-20  Vlan900       Ethernet1/10    Dynamic   1054      
172.16.68.20     00-12-cf-4c-ee-80  Vlan900       Ethernet1/10    Dynamic   994       
172.16.68.21     00-12-cf-90-cb-a0  Vlan900       Ethernet1/18    Dynamic   754       
172.16.68.22     00-12-cf-99-99-40  Vlan900       Ethernet1/17    Dynamic   363       
172.16.68.23     00-12-cf-99-85-40  Vlan900       Ethernet1/4     Dynamic   1054      
172.16.68.25     00-12-cf-90-90-20  Vlan900       Ethernet1/10    Dynamic   964       
172.16.68.26     00-12-cf-87-b7-a0  Vlan900       Ethernet1/11    Dynamic   3         
172.16.68.27     00-12-cf-87-c9-00  Vlan900       Ethernet1/6     Dynamic   874       
172.16.68.28     00-12-cf-4c-d7-20  Vlan900       Ethernet1/23    Dynamic   1145      
172.16.68.29     00-12-cf-99-d1-a0  Vlan900       Ethernet1/10    Dynamic   1024      
172.16.68.30     00-12-cf-8a-ef-f0  Vlan900       Ethernet1/23    Dynamic   633       
172.16.68.31     00-1b-11-6f-ec-29  Vlan900       Ethernet1/23    Dynamic   543       
172.16.68.32     00-1b-11-6f-e4-0f  Vlan900       Ethernet1/23    Dynamic   1158      
172.16.68.33     00-1b-11-6f-ea-5f  Vlan900       Ethernet1/23    Dynamic   1157      
172.16.68.34     00-1b-11-6f-e4-83  Vlan900       Ethernet1/23    Dynamic   1114      
172.16.68.35     00-1b-11-6f-e9-dc  Vlan900       Ethernet1/23    Dynamic   153       
172.16.68.36     00-12-cf-87-d8-60  Vlan900       Ethernet1/11    Dynamic   1174      
172.16.68.37     00-12-cf-87-fc-00  Vlan900       Ethernet1/11    Dynamic   573       
172.16.68.38     00-12-cf-c5-f1-20  Vlan900       Ethernet1/21    Dynamic   784       
172.16.68.125    00-e0-d8-13-9e-d2  Vlan900       Ethernet1/10    Dynamic   934       
172.16.68.126    00-e0-d8-13-9d-85  Vlan900       Ethernet1/7     Dynamic   1179      """,
## 'show system'
'show system': """show system
                   ^
% Invalid input detected at '^' marker.
""",
}
    snmp_get={}
    snmp_getnext={}
