# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## EdgeCore.ES.get_vlans test
## Auto-generated by manage.py debug-script at 2011-03-17 12:06:49
##----------------------------------------------------------------------
## Copyright (C) 2007-2011 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------
from noc.lib.test import ScriptTestCase
class EdgeCore_ES_get_vlans_Test(ScriptTestCase):
    script="EdgeCore.ES.get_vlans"
    vendor="EdgeCore"
    platform='ES4626-SFP'
    version='5.4.156.0'
    input={}
    result=[{'name': 'default', 'vlan_id': 1},
 {'name': 'test_BRAS', 'vlan_id': 2},
 {'name': 'test_bras', 'vlan_id': 3},
 {'name': 'MA5200G-RADIUS', 'vlan_id': 10},
 {'name': 'Management', 'vlan_id': 69},
 {'name': 'NE-4626-LB-1', 'vlan_id': 71},
 {'name': 'NE-4626-LB-2', 'vlan_id': 72},
 {'name': 'NE-4626-LB-3', 'vlan_id': 73},
 {'name': 'NE-4626-LB-4', 'vlan_id': 74},
 {'name': 'VLAN1006', 'vlan_id': 1006},
 {'name': 'MA5200G-S8512', 'vlan_id': 2076},
 {'name': 'to_3560_NATS', 'vlan_id': 3000}]
    motd='********\n'
    cli={
}
    snmp_get={}
    snmp_getnext={'1.3.6.1.2.1.17.7.1.4.2.1.3': [('1.3.6.1.2.1.17.7.1.4.2.1.3.0.1', '1'),
                                ('1.3.6.1.2.1.17.7.1.4.2.1.3.0.2', '2'),
                                ('1.3.6.1.2.1.17.7.1.4.2.1.3.0.3', '3'),
                                ('1.3.6.1.2.1.17.7.1.4.2.1.3.0.10', '10'),
                                ('1.3.6.1.2.1.17.7.1.4.2.1.3.0.69', '69'),
                                ('1.3.6.1.2.1.17.7.1.4.2.1.3.0.71', '71'),
                                ('1.3.6.1.2.1.17.7.1.4.2.1.3.0.72', '72'),
                                ('1.3.6.1.2.1.17.7.1.4.2.1.3.0.73', '73'),
                                ('1.3.6.1.2.1.17.7.1.4.2.1.3.0.74', '74'),
                                ('1.3.6.1.2.1.17.7.1.4.2.1.3.0.1006', '1006'),
                                ('1.3.6.1.2.1.17.7.1.4.2.1.3.0.2076', '2076'),
                                ('1.3.6.1.2.1.17.7.1.4.2.1.3.0.3000', '3000')],
 '1.3.6.1.2.1.17.7.1.4.3.1.1': [('1.3.6.1.2.1.17.7.1.4.3.1.1.1',
                                 'default\x00'),
                                ('1.3.6.1.2.1.17.7.1.4.3.1.1.2',
                                 'test_BRAS\x00'),
                                ('1.3.6.1.2.1.17.7.1.4.3.1.1.3',
                                 'test_bras\x00'),
                                ('1.3.6.1.2.1.17.7.1.4.3.1.1.10',
                                 'MA5200G-RADIUS\x00'),
                                ('1.3.6.1.2.1.17.7.1.4.3.1.1.69',
                                 'Management\x00'),
                                ('1.3.6.1.2.1.17.7.1.4.3.1.1.71',
                                 'NE-4626-LB-1\x00'),
                                ('1.3.6.1.2.1.17.7.1.4.3.1.1.72',
                                 'NE-4626-LB-2\x00'),
                                ('1.3.6.1.2.1.17.7.1.4.3.1.1.73',
                                 'NE-4626-LB-3\x00'),
                                ('1.3.6.1.2.1.17.7.1.4.3.1.1.74',
                                 'NE-4626-LB-4\x00'),
                                ('1.3.6.1.2.1.17.7.1.4.3.1.1.1006',
                                 'VLAN1006\x00'),
                                ('1.3.6.1.2.1.17.7.1.4.3.1.1.2076',
                                 'MA5200G-S8512\x00'),
                                ('1.3.6.1.2.1.17.7.1.4.3.1.1.3000',
                                 'to_3560_NATS\x00')]}
