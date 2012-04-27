#!/usr/bin/env python
#
# # Protool - Python class for manipulating protein structures
# Copyright (C) 2010 Jens Erik Nielsen
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Contact information: 
# Email: Jens.Nielsen_at_gmail.com
# Normal mail:
# Jens Nielsen
# SBBS, Conway Institute
# University College Dublin
# Dublin 4, Ireland

import os
if os.environ.has_key('HOST'):
    if os.environ['HOST']=='chemcca30' or os.environ['HOST']=='chemcca30.ucsd.edu':
        DSSP='/u1/jnielsen/whatif/dssp/DSSP.EXE'
        RASMOL='/usr/bin/X11/rasmol'
    else:
        DDSP='/net/linux/src/whatif_unstable/dssp/DSSP.EXE'
        RASMOL=None
else:
    DDSP='/net/linux/src/whatif_unstable/dssp/DSSP.EXE'
    RASMOL=None
    
    
