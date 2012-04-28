#  _________________________________________________________________________
#
#  Coopr: A COmmon Optimization Python Repository
#  Copyright (c) 2008 Sandia Corporation.
#  This software is distributed under the BSD License.
#  Under the terms of Contract DE-AC04-94AL85000 with Sandia Corporation,
#  the U.S. Government retains certain rights in this software.
#  For more information, see the Coopr README.txt file.
#  _________________________________________________________________________

# TODO: pass in variable/function name information into the
# optimizer.  This will require an augmented point and request
# specification.

"""
Define the plugin for DAKOTA TEXT IO
"""

import re
from pyutilib.component.core import *
from problem_io import *
from pyutilib.math import as_number

class DakotaTextIO(SingletonPlugin):
    """The reader/writer for the DAKOTA TEXT IO Formats"""

    implements(IBlackBoxOptProblemIO)

    def __init__(self):
        SingletonPlugin.__init__(self)
        self.name = 'dakota'

    def read(self, filename, point):
        """
        Read a point and request information.
        This method returns a tuple: point, requests
        """
        self.varname = []
        self.funcname = []
        vars = []
        requests = {}
        INPUT = open(filename,'r')
        #
        # Process variables
        #
        line = INPUT.readline()
        nvars = as_number(re.split('[ \t]+',line.strip())[0])
        for i in range(nvars):
            line = INPUT.readline()
            tokens = re.split('[ \t]+',line.strip())
            vars.append( as_number(tokens[0]) )
            if len(tokens) > 1:
                self.varname.append(tokens[1])
        #
        # Process requests
        #
        line = INPUT.readline()
        nfunctions = int(as_number(re.split('[ \t]+',line.strip())[0]))
        for i in range(nfunctions):
            line = INPUT.readline()
            tokens = re.split('[ \t]+',line.strip())
            asv = as_number(tokens[0])
            if len(tokens) > 1:
                self.funcname.append(tokens[1])
            if asv & 1:
                requests['FunctionValue'] = ''
                requests['FunctionValues'] = ''
                requests['NonlinearConstraintValues'] = ''
            if asv & 2:
                requests['Gradient'] = ''
            if asv & 4:
                requests['Hessian'] = ''
        point.set_variables(vars)
        return point, requests

    def write(self, filename, response):
        """
        Write response information to a file.
        """
        OUTPUT = open(filename,"w")
        fno = 0
        if 'FunctionValue' in response:
            print >>OUTPUT, response['FunctionValue'], self.funcname[fno]
            fno += 1
        elif 'FunctionValues' in response:
            for val in response['FunctionValues']:
                print >>OUTPUT, val, self.funcname[fno]
                fno += 1
        if 'NonlinearConstraintValues' in response and type(response['NonlinearConstraintValues']) is list:
            for val in response['NonlinearConstraintValues']:
                print >>OUTPUT, val, self.funcname[fno]
                fno += 1
        if 'Gradient' in response and type(response['NonlinearConstraintValues']) is list:
            for val in response['Gradient']:
                print >>OUTPUT, val,
            print >>OUTPUT, ""
        if 'Jacobian' in response and type(response['NonlinearConstraintValues']) is list:
            for grad in response['Jacobian']:
                for val in grad:
                    print >>OUTPUT, val,
                print >>OUTPUT, ""
        if 'Hessian' in response and type(response['NonlinearConstraintValues']) is list:
            print >>OUTPUT, "# ERROR: cannot print Hessian information"
        OUTPUT.close()
