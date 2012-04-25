# Copyright (c) 2010-2012 Robin Jarry
#
# This file is part of EVE Corporation Management.
#
# EVE Corporation Management is free software:     you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation:     either version 3 of the License:     or (at your
# option) any later version.
#
# EVE Corporation Management is distributed in the hope that it will be useful:    
# but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# EVE Corporation Management. If not:     see <http:    //www.gnu.org/licenses/>.

__date__ = "2012 04 10"
__author__ = "tash"

COLOR_FORMAT = '<font class="%s">%s</font>'

ORDER_STATES = {
0 :    'open / active',
1 :    'closed',
2 :    'expired (or fulfilled)',
3 :    'cancelled',
4 :    'pending',
5 :    'character deleted',
}

REPORT_TYPES = {
0 :    'Income',
1 :    'Expenditure',
2 :    'Cash Flow',
}

FORMATED_ORDER_STATES = {
0 :    COLOR_FORMAT % ('contract-inprogress', ORDER_STATES[0]),
1 :    COLOR_FORMAT % ('contract-completed', ORDER_STATES[1]),
2 :    COLOR_FORMAT % ('contract-completed', ORDER_STATES[2]),
3 :    COLOR_FORMAT % ('contract-cancelled', ORDER_STATES[3]),
4 :    COLOR_FORMAT % ('contract-inprogress', ORDER_STATES[4]),
5 :    COLOR_FORMAT % ('contract-deleted', ORDER_STATES[5]),
}

FORMATED_CONTRACT_STATES = {
'Outstanding':             COLOR_FORMAT % ('contract-outstanding', 'Outstanding'),
'Deleted':                 COLOR_FORMAT % ('contract-deleted', 'Deleted'),
'Completed':               COLOR_FORMAT % ('contract-completed', 'Completed'),
'Failed':                  COLOR_FORMAT % ('contract-failed', 'Failed'),
'CompletedByIssuer':       COLOR_FORMAT % ('contract-completedbyissuer', 'CompletedByIssuer'),
'CompletedByContractor':   COLOR_FORMAT % ('contract-completedbycontractor', 'CompletedByContractor'),
'Cancelled':               COLOR_FORMAT % ('contract-cancelled', 'Cancelled'),
'Rejected':                COLOR_FORMAT % ('contract-rejected', 'Rejected'),
'Reversed':                COLOR_FORMAT % ('contract-reversed', 'Reversed'),
'InProgress':              COLOR_FORMAT % ('contract-inprogress', 'InProgress'),
}

REPACKAGED_VOLUMES = {
'Assault Ship' :	        2500,
'AuditLogSecureContainer' :	1000,
'Battlecruiser' :	        15000,
'Battleship' :	            50000,
'Black Ops' :	            50000,
'Capital Industrial Ship' :	1000000,
'Capsule' :	                500,
'Cargo Container' :	        1000,
'Carrier' :	                1000000,
'Combat ReconShip' :	    10000,
'Command Ship' :	        15000,
'Covert Ops' :	            2500,
'Cruiser' :	                10000,
'Destroyer' :	            5000,
'Dreadnought' :	            1000000,
'Electronic Attack Ships' :	2500,
'Elite Battleship' :	    50000,
'Exhumer' :	                3750,
'Force Recon Ship' :	    10000,
'Freight Container' :	    1000,
'Freighter' :	            1000000,
'Frigate' :	                2500,
'Heavy Assault Ship' :	    10000,
'Heavy Interdictors' :	    10000,
'Industrial' :	            20000,
'Industrial CommandShip' :	500000,
'Interceptor' :	            2500,
'Interdictor' :	            5000,
'Jump Freighter' :	        1000000,
'Logistics' :	            10000,
'Marauders' :	            50000,
'Mining Barge' :	        3750,
'Mission Container' :	    1000,
'Mothership' :	            1000000,
'Rookieship' :	            2500,
'Secure Cargo Container' :	1000,
'Shuttle' :	                500,
'Stealth Bomber' :	        2500,
'Strategic Cruiser' :	    5000,
'Titan' :	                10000000,
'Transport Ship' :	        20000,
}
