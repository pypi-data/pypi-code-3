# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## DLink.DES21xx.get_mac_address_table test
## Auto-generated by ./noc debug-script at 2011-12-16 11:06:09
##----------------------------------------------------------------------
## Copyright (C) 2007-2011 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

## NOC modules
from noc.lib.test import ScriptTestCase


class DLink_DES21xx_get_mac_address_table_Test(ScriptTestCase):
    script = "DLink.DES21xx.get_mac_address_table"
    vendor = "DLink"
    platform = 'DES-2110'
    version = '3.00.18'
    input = {}
    result = [{'interfaces': ['9'], 'mac': '00:05:1A:99:6B:98', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:0F:6A:85:79:81', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:11:58:ED:BA:A1', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:11:58:EE:B7:21', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:11:95:E0:E8:3C', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:11:95:EB:87:83', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:11:95:EB:88:D5', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:11:95:EB:8C:2B', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:11:95:F5:CD:2F', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:11:95:F5:CD:7E', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:11:95:F5:D0:F0', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:13:46:65:7E:97', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:13:46:65:7E:9E', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:13:46:65:83:2A', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:13:46:71:D3:DD', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:13:46:71:DD:CF', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:13:49:BA:A5:41', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:13:49:BA:A5:42', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:13:49:BA:A5:43', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:13:49:BA:A5:44', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:13:49:BA:A5:45', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:13:49:DA:FB:B3', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:13:49:FA:7E:5C', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:13:49:FD:F5:3B', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:13:49:FD:F5:45', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:13:49:FD:F5:48', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:13:49:FD:F5:49', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:13:49:FD:F5:4A', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:14:69:31:89:C0', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:15:77:9B:9E:58', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:15:E8:D3:B9:C1', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:5B:73:57:BA', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:5B:73:57:BB', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:0A:D8:A2', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:0A:D8:A3', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:0A:D8:A4', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:0A:D8:A6', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:0A:D8:A7', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:0A:D8:A8', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:16:B5:86', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:16:B5:8F', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:16:B5:90', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:1F:5A:B8', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:1F:5A:BA', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:1F:5A:BC', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:1F:5A:BD', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:1F:5A:BE', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:1F:5A:BF', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:1F:5A:CE', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:1F:5A:E1', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:1F:5A:E2', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:1F:5A:E3', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:1F:5A:E4', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:1F:5A:E5', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:1F:5A:E6', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:1F:5A:E7', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:1F:5B:A9', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:1F:5B:AC', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:1F:5B:AE', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:1F:5B:AF', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:33:4E:DA', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:33:4E:DB', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:33:4E:E1', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:3B:CE:3F', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:3B:CE:43', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:3B:CE:47', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:3B:CE:48', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:3B:CE:52', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:3B:CE:53', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:3B:CE:54', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:3B:CE:55', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:3B:CE:58', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:3B:CE:5B', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:3B:CE:5C', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:3B:CE:5D', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:3B:CE:5E', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:3B:CE:5F', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:3B:CE:60', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:3C:86:0A', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:3C:86:0B', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:3C:86:0E', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:3C:86:0F', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:3C:86:B0', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:3C:86:B1', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:3C:86:B5', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:45:E3:DD', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:45:E4:0B', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:45:E4:0D', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:45:E4:11', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:45:F1:D7', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:45:F1:D8', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:45:F2:54', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:4B:25:CA', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:4B:25:CD', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:4B:25:EA', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:4B:25:EB', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:4B:25:EC', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:4B:25:ED', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:4B:25:EE', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:4B:25:EF', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:4B:25:F0', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:4B:25:F1', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:4B:26:45', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:4B:26:EB', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:4B:26:ED', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:4B:26:EE', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:4B:26:F0', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:4B:26:F1', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:4B:26:F2', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:4B:27:3D', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:4B:27:3F', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:51:E7:CD', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:51:E7:D0', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:51:E7:D4', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:51:E7:D6', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:51:E7:D8', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:51:E7:DA', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:55:DC:76', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:55:DC:78', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:55:DC:7D', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:55:DC:80', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:B6:17:49', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:B6:17:4A', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:B6:17:4D', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:19:CB:B6:17:6B', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:1B:11:6F:E5:7E', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:21:1B:EF:A0:94', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:26:5A:E4:1C:18', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '1C:AF:F7:C9:92:75', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '1C:AF:F7:C9:92:76', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '1C:AF:F7:C9:92:77', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '1C:AF:F7:C9:92:F1', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '1C:AF:F7:C9:A2:D9', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '88:74:43:90:00:01', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '88:74:43:C8:00:01', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '88:74:45:08:00:01', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': 'F0:7D:68:B4:18:36', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': 'F0:7D:68:B4:18:37', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': 'F0:7D:68:B4:18:3A', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': 'F0:7D:68:B4:18:79', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': 'F0:7D:68:B4:18:7B', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': 'F0:7D:68:B8:CC:01', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': 'F0:7D:68:B8:CC:02', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': 'F0:7D:68:B8:CC:43', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': 'F0:7D:68:B8:CC:46', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': 'F0:7D:68:B8:D2:7D', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': 'F0:7D:68:B8:D2:7E', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': 'F0:7D:68:B8:D2:80', 'type': 'D', 'vlan_id': 1},
 {'interfaces': ['9'], 'mac': '00:04:61:AF:31:91', 'type': 'D', 'vlan_id': 29},
 {'interfaces': ['9'], 'mac': '00:0C:42:59:40:8B', 'type': 'D', 'vlan_id': 29},
 {'interfaces': ['9'], 'mac': '00:13:A9:83:59:29', 'type': 'D', 'vlan_id': 29},
 {'interfaces': ['9'], 'mac': '00:15:E9:3D:35:4A', 'type': 'D', 'vlan_id': 29},
 {'interfaces': ['9'], 'mac': '00:17:31:A3:A3:24', 'type': 'D', 'vlan_id': 29},
 {'interfaces': ['9'], 'mac': '00:1B:38:46:1C:98', 'type': 'D', 'vlan_id': 29},
 {'interfaces': ['9'], 'mac': '00:21:1B:EF:A0:94', 'type': 'D', 'vlan_id': 29},
 {'interfaces': ['9'], 'mac': '00:22:B0:3E:7B:24', 'type': 'D', 'vlan_id': 29},
 {'interfaces': ['9'], 'mac': '00:24:1D:C0:49:85', 'type': 'D', 'vlan_id': 29},
 {'interfaces': ['9'], 'mac': '00:30:48:93:58:01', 'type': 'D', 'vlan_id': 29},
 {'interfaces': ['3'], 'mac': '00:26:5A:9E:69:33', 'type': 'S', 'vlan_id': 29},
 {'interfaces': ['4'], 'mac': 'C8:0A:A9:00:CC:4F', 'type': 'S', 'vlan_id': 29},
 {'interfaces': ['1'], 'mac': '00:0B:5D:52:8A:B3', 'type': 'S', 'vlan_id': 29},
 {'interfaces': ['2'], 'mac': '00:1C:F0:9E:45:33', 'type': 'S', 'vlan_id': 29},
 {'interfaces': ['5'], 'mac': '00:E0:91:02:93:4C', 'type': 'S', 'vlan_id': 29},
 {'interfaces': ['1'], 'mac': 'F0:B4:79:04:5D:98', 'type': 'S', 'vlan_id': 29},
 {'interfaces': ['6'], 'mac': '6C:62:6D:28:32:7E', 'type': 'S', 'vlan_id': 29}]
    motd = ''
    cli = {
## 'show fdb port 9'
'show fdb port 9': """show fdb port 9
Command:  show fdb port 9


DYNAMIC MAC SEARCH LIST:
Idx   Port    VID    MAC Address
-----------------------------------
001    9         1    00051a996b98
002    9         1    000f6a857981
003    9         1    001158edbaa1
004    9         1    001158eeb721
005    9         1    001195e0e83c
006    9         1    001195eb8783
007    9         1    001195eb88d5
008    9         1    001195eb8c2b
009    9         1    001195f5cd2f
010    9         1    001195f5cd7e
011    9         1    001195f5d0f0
012    9         1    001346657e97
013    9         1    001346657e9e
014    9         1    00134665832a
015    9         1    00134671d3dd
016    9         1    00134671ddcf
017    9         1    001349baa541
018    9         1    001349baa542
019    9         1    001349baa543
020    9         1    001349baa544
021    9         1    001349baa545
022    9         1    001349dafbb3
023    9         1    001349fa7e5c
024    9         1    001349fdf53b
025    9         1    001349fdf545
026    9         1    001349fdf548
027    9         1    001349fdf549
028    9         1    001349fdf54a
029    9         1    0014693189c0
030    9         1    0015779b9e58
031    9         1    0015e8d3b9c1
032    9         1    00195b7357ba
033    9         1    00195b7357bb
034    9         1    0019cb0ad8a2
035    9         1    0019cb0ad8a3
036    9         1    0019cb0ad8a4
037    9         1    0019cb0ad8a6
038    9         1    0019cb0ad8a7
039    9         1    0019cb0ad8a8
040    9         1    0019cb16b586
041    9         1    0019cb16b58f
042    9         1    0019cb16b590
043    9         1    0019cb1f5ab8
044    9         1    0019cb1f5aba
045    9         1    0019cb1f5abc
046    9         1    0019cb1f5abd
047    9         1    0019cb1f5abe
048    9         1    0019cb1f5abf
049    9         1    0019cb1f5ace
050    9         1    0019cb1f5ae1
051    9         1    0019cb1f5ae2
052    9         1    0019cb1f5ae3
053    9         1    0019cb1f5ae4
054    9         1    0019cb1f5ae5
055    9         1    0019cb1f5ae6
056    9         1    0019cb1f5ae7
057    9         1    0019cb1f5ba9
058    9         1    0019cb1f5bac
059    9         1    0019cb1f5bae
060    9         1    0019cb1f5baf
061    9         1    0019cb334eda
062    9         1    0019cb334edb
063    9         1    0019cb334ee1
064    9         1    0019cb3bce3f
065    9         1    0019cb3bce43
066    9         1    0019cb3bce47
067    9         1    0019cb3bce48
068    9         1    0019cb3bce52
069    9         1    0019cb3bce53
070    9         1    0019cb3bce54
071    9         1    0019cb3bce55
072    9         1    0019cb3bce58
073    9         1    0019cb3bce5b
074    9         1    0019cb3bce5c
075    9         1    0019cb3bce5d
076    9         1    0019cb3bce5e
077    9         1    0019cb3bce5f
078    9         1    0019cb3bce60
079    9         1    0019cb3c860a
080    9         1    0019cb3c860b
081    9         1    0019cb3c860e
082    9         1    0019cb3c860f
083    9         1    0019cb3c86b0
084    9         1    0019cb3c86b1
085    9         1    0019cb3c86b5
086    9         1    0019cb45e3dd
087    9         1    0019cb45e40b
088    9         1    0019cb45e40d
089    9         1    0019cb45e411
090    9         1    0019cb45f1d7
091    9         1    0019cb45f1d8
092    9         1    0019cb45f254
093    9         1    0019cb4b25ca
094    9         1    0019cb4b25cd
095    9         1    0019cb4b25ea
096    9         1    0019cb4b25eb
097    9         1    0019cb4b25ec
098    9         1    0019cb4b25ed
099    9         1    0019cb4b25ee
100    9         1    0019cb4b25ef
101    9         1    0019cb4b25f0
102    9         1    0019cb4b25f1
103    9         1    0019cb4b2645
104    9         1    0019cb4b26eb
105    9         1    0019cb4b26ed
106    9         1    0019cb4b26ee
107    9         1    0019cb4b26f0
108    9         1    0019cb4b26f1
109    9         1    0019cb4b26f2
110    9         1    0019cb4b273d
111    9         1    0019cb4b273f
112    9         1    0019cb51e7cd
113    9         1    0019cb51e7d0
114    9         1    0019cb51e7d4
115    9         1    0019cb51e7d6
116    9         1    0019cb51e7d8
117    9         1    0019cb51e7da
118    9         1    0019cb55dc76
119    9         1    0019cb55dc78
120    9         1    0019cb55dc7d
121    9         1    0019cb55dc80
122    9         1    0019cbb61749
123    9         1    0019cbb6174a
124    9         1    0019cbb6174d
125    9         1    0019cbb6176b
126    9         1    001b116fe57e
127    9         1    00211befa094
128    9         1    00265ae41c18
129    9         1    1caff7c99275
130    9         1    1caff7c99276
131    9         1    1caff7c99277
132    9         1    1caff7c992f1
133    9         1    1caff7c9a2d9
134    9         1    887443900001
135    9         1    887443c80001
136    9         1    887445080001
137    9         1    f07d68b41836
138    9         1    f07d68b41837
139    9         1    f07d68b4183a
140    9         1    f07d68b41879
141    9         1    f07d68b4187b
142    9         1    f07d68b8cc01
143    9         1    f07d68b8cc02
144    9         1    f07d68b8cc43
145    9         1    f07d68b8cc46
146    9         1    f07d68b8d27d
147    9         1    f07d68b8d27e
148    9         1    f07d68b8d280
149    9        29    000461af3191
150    9        29    000c4259408b
151    9        29    0013a9835929
152    9        29    0015e93d354a
153    9        29    001731a3a324
154    9        29    001b38461c98
155    9        29    00211befa094
156    9        29    0022b03e7b24
157    9        29    00241dc04985
158    9        29    003048935801
""", 
## 'show fdb port 8'
'show fdb port 8': """show fdb port 8
Command:  show fdb port 8


DYNAMIC MAC SEARCH LIST:
Idx   Port    VID    MAC Address
-----------------------------------
""", 
## 'show fdb port 3'
'show fdb port 3': """show fdb port 3
Command:  show fdb port 3


DYNAMIC MAC SEARCH LIST:
Idx   Port    VID    MAC Address
-----------------------------------
""", 
## 'show fdb port 2'
'show fdb port 2': """show fdb port 2
Command:  show fdb port 2


DYNAMIC MAC SEARCH LIST:
Idx   Port    VID    MAC Address
-----------------------------------
""", 
## 'show fdb port 1'
'show fdb port 1': """show fdb port 1
Command:  show fdb port 1


DYNAMIC MAC SEARCH LIST:
Idx   Port    VID    MAC Address
-----------------------------------
""", 
## 'show fdb port 7'
'show fdb port 7': """show fdb port 7
Command:  show fdb port 7


DYNAMIC MAC SEARCH LIST:
Idx   Port    VID    MAC Address
-----------------------------------
""", 
## 'show fdb port 6'
'show fdb port 6': """show fdb port 6
Command:  show fdb port 6


DYNAMIC MAC SEARCH LIST:
Idx   Port    VID    MAC Address
-----------------------------------
""", 
## 'show fdb port 5'
'show fdb port 5': """show fdb port 5
Command:  show fdb port 5


DYNAMIC MAC SEARCH LIST:
Idx   Port    VID    MAC Address
-----------------------------------
""", 
## 'show fdb port 4'
'show fdb port 4': """show fdb port 4
Command:  show fdb port 4


DYNAMIC MAC SEARCH LIST:
Idx   Port    VID    MAC Address
-----------------------------------
""", 
## 'show smac'
'show smac': """show smac
Command:  show smac

STATIC MAC Function: Enable

STATIC MAC LIST:
ID    Port    VID    MAC Address
-----------------------------------
01     3       29    00265a9e6933
02     4       29    c80aa900cc4f
03     1       29    000b5d528ab3
04     2       29    001cf09e4533
05     5       29    00e09102934c
06     1       29    f0b479045d98
07     6       29    6c626d28327e
""", 
## 'show fdb port 10'
'show fdb port 10': """show fdb port 10
Command:  show fdb port 10


DYNAMIC MAC SEARCH LIST:
Idx   Port    VID    MAC Address
-----------------------------------
""", 
## 'show ports '
'show ports ': """show ports 
Command:  show ports 


PORT STATUS:
ID       Speed    Flow_Control       QOS    Link_Status
-------------------------------------------------------
01        Auto         Disable    Normal      100M Full
02        Auto         Disable    Normal      100M Full
03        Auto         Disable    Normal           Down
04        Auto         Disable    Normal      100M Full
05        Auto         Disable    Normal      100M Full
06        Auto         Disable    Normal      100M Full
07        Auto         Disable    Normal           Down
08        Auto         Disable    Normal           Down
09        Auto         Disable    Normal      100M Full
10        Auto         Disable    Normal           Down
""", 
}
    snmp_get = {}
    snmp_getnext = {}
    http_get = {}
