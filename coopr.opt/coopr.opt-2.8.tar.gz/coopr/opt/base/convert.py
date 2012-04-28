#  _________________________________________________________________________
#
#  Coopr: A COmmon Optimization Python Repository
#  Copyright (c) 2008 Sandia Corporation.
#  This software is distributed under the BSD License.
#  Under the terms of Contract DE-AC04-94AL85000 with Sandia Corporation,
#  the U.S. Government retains certain rights in this software.
#  For more information, see the Coopr README.txt file.
#  _________________________________________________________________________

__all__ = ['IProblemConverter', 'convert_problem']

import copy
import os
from formats import ProblemFormat, guess_format
from error import *
from pyutilib.component.core import *


class IProblemConverter(Interface):

    def can_convert(self, from_type, to_type):
        """Returns true if this object supports the specified conversion"""

    def convert(self, from_type, to_type):
        """Convert an instance of one type into another"""

    def apply(self, *args, **kwargs):
        """Convert an instance of one type into another"""


def convert_problem( args, target_problem_type, valid_problem_types,
                     has_capability=lambda x: False ):
    """
    Convert a problem, defined by the 'args' tuple, into another problem.
    """
    #print "HERE",args,target_problem_type,valid_problem_types
    if len(valid_problem_types) == 0:
        raise ConverterError, "No valid problem types"

    if not (target_problem_type is None or \
             target_problem_type in valid_problem_types):
        msg = "Problem type '%s' is not valid"
        raise ConverterError, msg % str( target_problem_type )

    if len(args) == 0:
        raise ConverterError, "Empty argument list"

    #
    # Setup list of source problem types
    #
    tmp = args[0]
    if isinstance(tmp,basestring):
        fname = tmp.split(os.sep)[-1]
        if os.sep in fname:   #pragma:nocover
            fname = tmp.split(os.sep)[-1]
        source_ptype = [guess_format(fname)]
        if source_ptype is [None]:
            raise ConverterError, "Unknown suffix type: "+suffix
    else:
        source_ptype = args[0].valid_problem_types()

    #
    # Setup list of valid problem types
    #
    valid_ptypes = copy.copy(valid_problem_types)
    if target_problem_type is not None:
        valid_ptypes.remove(target_problem_type)
        valid_ptypes = [target_problem_type]  + valid_ptypes
    if source_ptype[0] in valid_ptypes:
        ##print "HERE",source_ptype, valid_ptypes
        valid_ptypes.remove(source_ptype[0])
        valid_ptypes = [source_ptype[0]]  + valid_ptypes

    #
    # Iterate over the valid problem types, starting with the target type
    #
    # Apply conversion and return for first match
    #
    for ptype in valid_ptypes:
        for s_ptype in source_ptype:
        #print "HERE",str(s_ptype),str(ptype),args[0]
        #
        # If the source and target types are equal, then simply the return
        # the args (return just the first element of the tuple if it has length
        # one.
        #
            if s_ptype == ptype:
                return (args,ptype,None)
            #
            # Otherwise, try to convert
            #
            for converter in ExtensionPoint(IProblemConverter):
            #print "HERE",converter,s_ptype,ptype
                if converter.can_convert(s_ptype,ptype):
                    tmp = [s_ptype,ptype] + list(args)
                    tmp = tuple(tmp)
                    tmpkw = {'capabilities':has_capability}
                    problem_files, symbol_map = converter.apply(*tmp, **tmpkw)
                    return problem_files, ptype, symbol_map

    msg = 'No conversion possible.  Source problem type: %s.  Valid target '  \
          'types: %s'
    raise ConverterError, msg % (str(source_ptype[0]), map(str,valid_ptypes))
