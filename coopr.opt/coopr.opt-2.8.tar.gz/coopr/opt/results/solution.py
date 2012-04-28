#  _________________________________________________________________________
#
#  Coopr: A COmmon Optimization Python Repository
#  Copyright (c) 2008 Sandia Corporation.
#  This software is distributed under the BSD License.
#  Under the terms of Contract DE-AC04-94AL85000 with Sandia Corporation,
#  the U.S. Government retains certain rights in this software.
#  _________________________________________________________________________

__all__ = ['SolutionStatus', 'Solution', 'SolutionMap']

import math
from container import *
from pyutilib.misc import Bunch
from pyutilib.enum import Enum
from pyutilib.math import as_number

default_print_options = Bunch(schema=False, sparse=True, num_solutions=None, ignore_time=False, ignore_defaults=False)

SolutionStatus = Enum(
  'bestSoFar',
  'error',
  'feasible',
  'globallyOptimal',
  'infeasible',
  'locallyOptimal',
  'optimal',
  'other',
  'stoppedByLimit',
  'unbounded',
  'unknown',
  'unsure',
)


class SolutionMap(MapContainer):

    def __init__(self, sparse=True):
        MapContainer.__init__(self)
        self._sparse=sparse
        self._names = {}
        self._prefix='x'
        self._option = default_print_options

    def __getitem__(self, name):
        tmp = self._convert(name)
        try:
            return self.__dict__[tmp]
        except:
            pass
        if type(name) in (int,long):
            self.declare_item(tmp-1)
        else:
            self.declare_item(tmp)
        if type(tmp) is int:
            tmp = self._names[tmp-1]
        item = dict.__getitem__(self, tmp)
        if isinstance(item,ListContainer) or isinstance(item,MapContainer):
            return item
        return item.value

    def _set_value(self, name, val):
        if isinstance(name,basestring):
            self.declare_item(name)
        elif type(name) is int:
            self.declare_item(name-1)
        if type(name) is int:
            name = self._names[name-1]
        dict.__getitem__(self, name).value = as_number(val)

    def declare(self, name, **kwds):
        if type(name) is int:
            return
        self.declare_item(name)

    def declare_item(self, name, id=None):
        self._active=True
        if name in self:
            return
        if type(name) is int:
            id = name
            try:
                name = self._names[name]
            except:
                name = self._prefix+str(name)
        else:
            if id is None:
                id = len(self._names)
        if name in self:
            return
        MapContainer.declare(self, name, value=MapContainer())
        dict.__getitem__(self, name).id = id
        self._names[id] = name
        #
        # If the name has the format x(1,a) or x[3,4,5]
        # then create a dictionary attribute 'x', which maps
        # the tuple values to the corresponding value.
        #
        if isinstance(name, basestring):
            if '[' in name:
                pieces = name.split('[')
                varname = pieces[0]
                rest = None
                # when a variable is indexed by more than one parameter, you will
                # see identifiers of the form "x((a,b))" instead of the "x(a)"
                # one-dimensional form. this is due to the process of "stringifying"
                # the name, which is fine. it just requires a bit of ugliness in
                # the string splitting process.
                if name.count("]") == 2:
                    rest = pieces[2]
                else:
                    rest = pieces[1]
                # we're always taking the first part of the name,
                # so even in the two (or greater) dimensional case
                # such as "x((a,b))", the first piece is what we want.
                tpl = rest.split(']')[0]
                tokens = tpl.split(',')
                for i in xrange(len(tokens)):
                    tokens[i] = as_number(tokens[i])
                try:
                    var = self.__dict__[varname]
                    #var = dict.__getitem__(self, varname)
                except Exception, err:
                    self.__dict__[varname]={}
                    var = self.__dict__[varname]
                    #dict.__setitem__(self, varname, {})
                    #var = dict.__getitem__(self, varname)
                if len(tokens) == 1:
                    var[ tokens[0] ] = dict.__getitem__(self, name)
                else:
                    var[ tuple(tokens) ] = dict.__getitem__(self, name)
            #else:
                #self.__dict__[name]=dict.__getitem__(self, name)

    def _convert(self, name):

        # conversion disabled - originally only munged names by
        # replacing () for []. that functionality is no longer needed.
        return name

    def _repn_(self, option):
        #print "SOLUTION",self._active,self._required
        if not option.schema and not self._active and not self._required:
            return ignore
        if option.schema:
            self[0] = 1.0
            self[1] = 2.0
            self[2] = 3.0
            #print dict.keys(self)
            #print self.keys()
        tmp = {}
        keys = self._names.keys()
        keys.sort()
        for i in keys:
            key = self._names[i]
            rep = dict.__getitem__(self, key)._repn_(option)
            #print "HERE",type(dict.__getitem__(self, key))
            #print "HERE",repr(dict.__getitem__(self, key))
            #print "HERE",rep
            if not rep == ignore:
                if option.sparse and self._sparse:
                    trep = {}
                    for tkey in rep:
                        if tkey == 'Id':
                            trep[tkey] = rep[tkey]
                            continue
                        if not type(rep[tkey]) in (float,int,long) or math.fabs(rep[tkey]) > 1e-16:
                            trep[tkey] = rep[tkey]
                    if len(trep.keys()) > 1:
                        tmp[key] = trep
                else:
                    tmp[key] = rep
        if tmp == {}:
            return "No nonzero values"
        return tmp

    def pprint(self, ostream, option, from_list=False, prefix="", repn=None):
        if isinstance(repn,basestring):
            print >>ostream, repn
        else:
            MapContainer.pprint(self, ostream, option, from_list=from_list, prefix=prefix, repn=repn)

    def load(self, repn):
        if isinstance(repn, basestring) or repn is None:
            return
        index = {}
        for key in repn:
            index[repn[key]['Id']] = key
        keys = index.keys()
        keys.sort()
        for key in keys:
            self.declare_item(index[key], id=key)
            for elt in repn[index[key]]:
                if elt == 'Id':
                    continue
                dict.__getitem__(self, index[key])[elt] = repn[index[key]][elt]


class Solution(MapContainer):

    def __init__(self):
        MapContainer.__init__(self)

        self.declare('gap')
        self.declare('status', value=SolutionStatus.unknown)
        self.declare('message')

        self.declare('objective', value=SolutionMap(sparse=False), active=False)
        self.declare('variable', value={})
        self.declare('constraint', value=SolutionMap())

        self._option = default_print_options

    def load(self, repn):
        # delete key from dictionary, call base class load, handle variable loading.
        if repn.has_key("Variable"):
            var_dict = repn["Variable"]
            del repn["Variable"]
            self.variable = var_dict
        MapContainer.load(self,repn)


class SolutionSet(ListContainer):

    def __init__(self):
        ListContainer.__init__(self,Solution)
        self._option = default_print_options

    def _repn_(self, option):
        if not option.schema and not self._active and not self._required:
            return ignore
        if option.schema and len(self) == 0:
            self.add()
            self.add()
        if option.num_solutions is None:
            num = len(self)
        else:
            num = min(num, len(self))
        i=0
        tmp = []
        for item in self._list:
            tmp.append( item._repn_(option) )
            i=i+1
            if i == num:
                break
        return [{'number of solutions':len(self), 'number of solutions displayed':num}]+ tmp

    def __len__(self):
        return len(self._list)

    def __call__(self, i=1):
        return self._list[i-1]

    def pprint(self, ostream, option, prefix="", repn=None):
        if not option.schema and not self._active and not self._required:
            return ignore
        print >>ostream, ""
        print >>ostream, prefix+"-",
        spaces=""
        for key in repn[0]:
            print >>ostream, prefix+spaces+key+":",repn[0][key]
            spaces="  "
        i=0
        for i in xrange(len(self._list)):
            item = self._list[i]
            print >>ostream, prefix+'-',
            item.pprint(ostream, option, from_list=True, prefix=prefix+"  ", repn=repn[i+1])

    def load(self, repn):
        #
        # Note: we ignore the first element of the repn list, since
        # it was generated on the fly by the SolutionSet object.
        #
        for data in repn[1:]: # repn items 1 through N are individual solutions.
            item = self.add()
            item.load(data)
