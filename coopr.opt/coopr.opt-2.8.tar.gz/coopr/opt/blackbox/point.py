#  _________________________________________________________________________
#
#  Coopr: A COmmon Optimization Python Repository
#  Copyright (c) 2008 Sandia Corporation.
#  This software is distributed under the BSD License.
#  Under the terms of Contract DE-AC04-94AL85000 with Sandia Corporation,
#  the U.S. Government retains certain rights in this software.
#  For more information, see the Coopr README.txt file.
#  _________________________________________________________________________

"""
Define COLIN point types
"""

__all__ = ['MixedIntVars', 'RealVars']

import copy
import re
import xml.dom.minidom
from pyutilib.misc import get_xml_text


class MixedIntVars(object):
    """
    A class that defines a domain type for mixed-integer variables
    """

    def __init__(self, nreal=0, nint=0, nbinary=0):
        self.reals = [0.0]*nreal
        self.ints = [0]*nint
        self.bits = [0]*nbinary

    def set_variables(self, vlist):
        i = 0
        #
        nreals = len(self.reals)
        self.reals = []
        for j in xrange(nreals):
            self.reals.append( vlist[i] )
            i += 1
        #
        nints = len(self.ints)
        self.ints = []
        for j in xrange(nints):
            self.ints.append( vlist[i] )
            i += 1
        #
        nbits = len(self.bits)
        self.bits = []
        for j in xrange(nbits):
            self.bits.append( vlist[i] )
            i += 1

    def display(self):
        print "Reals",
        for val in self.reals:
            print val,
        print ""
        print "Integers",
        for val in self.ints:
            print val,
        print ""
        print "Binary",
        for val in self.bits:
            print val,
        print ""

    def process(self,node):
        self.reals=[]
        self.ints=[]
        self.bits=[]
        for child in node.childNodes:
            if child.nodeType == node.ELEMENT_NODE:
                child_text = get_xml_text(child)
                child_text.strip()
                if child_text == "":
                    continue
                if child.nodeName == "Real":
                    for val in re.split('[\t ]+',child_text):
                        self.reals.append(1.0*eval(val))
                elif child.nodeName == "Integer":
                    for val in re.split('[\t ]+',child_text):
                        self.ints.append(eval(val))
                elif child.nodeName == "Binary":
                    tmp = child_text.replace(' ', '')
                    for val in tmp:
                        if val == '1':
                            self.bits.append(1)
                        elif val == '0':
                            self.bits.append(0)
        return self



class RealVars(object):
    """
    A class that defines a domain type for real variables
    """

    def __init__(self, nreal=0):
        self.vars = [0.0]*nreal

    def set_variables(self, vlist):
        self.vars = copy.copy(vlist)

    def display(self):
        for val in self.vars:
            print val,
        print ""

    def process(self,node):
        self.vars = []
        for child in node.childNodes:
            if child.nodeType == node.ELEMENT_NODE:
                child_text = get_xml_text(child)
                if child_text == "":                #pragma:nocover
                    continue
                if child.nodeName == "Real":
                    for val in re.split('[\t ]+',child_text):
                        self.vars.append(1.0*eval(val))
        return self


