# -*- coding: utf-8 -*-
# #START_LICENSE###########################################################
#
#
# This file is part of the Environment for Tree Exploration program
# (ETE).  http://ete.cgenomics.org
#  
# ETE is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#  
# ETE is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
# License for more details.
#  
# You should have received a copy of the GNU General Public License
# along with ETE.  If not, see <http://www.gnu.org/licenses/>.
#
# 
#                     ABOUT THE ETE PACKAGE
#                     =====================
# 
# ETE is distributed under the GPL copyleft license (2008-2011).  
#
# If you make use of ETE in published work, please cite:
#
# Jaime Huerta-Cepas, Joaquin Dopazo and Toni Gabaldon.
# ETE: a python Environment for Tree Exploration. Jaime BMC
# Bioinformatics 2010,:24doi:10.1186/1471-2105-11-24
#
# Note that extra references to the specific methods implemented in 
# the toolkit are available in the documentation. 
# 
# More info at http://ete.cgenomics.org
#
# 
# #END_LICENSE#############################################################
__VERSION__="ete2-2.1rev498" 
from sys import stdout
import _orthoxml as main
from _orthoxml import * 

_orthoxml.Orthoxml.subclass = Orthoxml

class Orthoxml(_orthoxml.Phyloxml):
    def __repr__(self):
        return "Orthoxml dataset <%s>" %hex(hash(self))

    def __init__(self, *args, **kargs):
        super(Orthoxml, self).__init__(outfile=outfile, level=level)
        
    def build_from_file(self, fname):
        doc = _orthoxml.parsexml_(fname)
        rootNode = doc.getroot()
        rootTag, rootClass = _orthoxml.get_root_tag(rootNode)
        if rootClass is None:
            rootTag = 'phyloxml'
            rootClass = self.__class__
        self.build(rootNode)

    def export(self, outfile=stdout, level=0):
        return super(Orthoxml, self).export(outfile=outfile, level=level)


__all__ = _orthoxml.__all__ + ["Orthoxml"]
