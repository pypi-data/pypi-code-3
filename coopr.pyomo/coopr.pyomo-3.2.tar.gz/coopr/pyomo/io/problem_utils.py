#  _________________________________________________________________________
#
#  Coopr: A COmmon Optimization Python Repository
#  Copyright (c) 2008 Sandia Corporation.
#  This software is distributed under the BSD License.
#  Under the terms of Contract DE-AC04-94AL85000 with Sandia Corporation,
#  the U.S. Government retains certain rights in this software.
#  For more information, see the Coopr README.txt file.
#  _________________________________________________________________________


import coopr.opt
from coopr.pyomo.base import expr, Var, Constraint, Objective
from coopr.pyomo.base.var import _VarData
from coopr.pyomo.base.param import _ParamData
from coopr.pyomo.base.expr import *
from coopr.pyomo.base.numvalue import *

class ProblemWriterUtils(coopr.opt.AbstractProblemWriter):
    """
    Class that contains utilities for organizing model data before
    the problem is written.

    WEH: Perhaps these should be moved into AbstractProblemWriter.
    We'll see how this code evolves...

    """

    def __init__(self, problem_format):
        coopr.opt.AbstractProblemWriter.__init__(self,problem_format)
        self._varmap={}

    def _name_fix(self, name):
        name = name.replace("\"","")
        name = name.replace("%","_")
        name = name.replace("[","_")
        name = name.replace("]","_")
        name = name.replace("(","_")
        name = name.replace(")","_")
        name = name.replace(" ","")
        name = name.replace(",","_")
        name = name.replace("-","_")
        name = name.replace("'","")
        name = name.replace("`","")
        return name

    #
    # Identify variables and confirm that the expression is linear
    #
    def _Collect1(self,exp):
        #
        # Expression
        #
        if isinstance(exp,expr.Expression):
            #
            # SumExpression
            #
            if isinstance(exp,expr._SumExpression):
                for i in xrange(len(exp._args)):
                    self._Collect1(exp._args[i])
            #
            # Identity
            #
            elif isinstance(exp,expr._IdentityExpression):
                self._Collect1(exp._args[0])
            #
            # Product
            #
            elif isinstance(exp,expr._ProductExpression):
                v = "0"
                for i in xrange(len(exp._args)):
                    e = exp._args[i]
                    if isinstance(e,Var):
                        if v != "0":
                            raise ValueError, "Two variables in ProductExpression:",e
                        e._varval[None]._sno = 0
                    elif isinstance(e,_VarData):
                        if v != "0":
                            raise ValueError, "Two variables in ProductExpression:",e
                        e._sno = 0
                    elif not isinstance(e,NumericConstant) and not isinstance(e,_ParamData):
                        print "ERROR: Unexpected item of type=" + e.__class__.__name__ + " encountered in product expression during simplification (_Collect1)"
                        print "Parent expression: "
                        exp.pprint()
                        print "Offending item: "
                        e.pprint()
                        raise ValueError, "Unexpected item in ProductExpression - failed to simplify expression"

            elif isinstance(exp,expr._MinusExpression):
                self._Collect1(exp._args[0])
                self._Collect1(exp._args[1])
            #
            # ERROR
            #
            else:
                raise ValueError, "Unsupported expression type: "+str(type(exp))
        #
        # Variable Value
        #
        elif isinstance(exp,_VarData):
            exp._sno = 0

        # "pure" (non-indexed) variables must be handled a bit differently,
        # forcing the "_sno" on the variable value explicitly.
        elif isinstance(exp,Var):
            exp._varval[None]._sno = 0
        #
        # If not a constant, then this is an error
        #
        elif not isinstance(exp,NumericConstant) and not isinstance(exp,_ParamData):
            #print "here",exp.value,dir(exp),exp._name,type(exp.value)
            raise ValueError, "ERROR: Unexpected expression type in _Collect1: " + str(exp)


    #
    # Identify variables and confirm that the expression is linear
    #
    def _Collect2(self, exp, x, scale=1.0):
        #
        # Expression
        #
        if isinstance(exp,expr.Expression):
                #
                # Sum
                #
            if isinstance(exp,expr._SumExpression):
                for i in xrange(len(exp._args)):
                    x = self._Collect2(exp._args[i], x, scale)
            #
            # Identity
            #
            elif isinstance(exp,expr._IdentityExpression):
                x = self._Collect2(exp._args[0], x, scale)
            #
            # Product
            #
            elif isinstance(exp,expr._ProductExpression):
                c = scale
                ve = v = "0"
                for i in xrange(len(exp._args)):
                    e = exp._args[i]
                    if isinstance(e,NumericConstant) or isinstance(e,_ParamData):
                        c *= e.value
                    elif isinstance(e,Var):
                        if v != "0":
                            raise ValueError, "ERROR: two variables in ProductExpression:",e
                        v = self._name_fix(e._varval[None].name)
                        ve = e._varval[None]
                    elif isinstance(e,_VarData):
                        if v != "0":
                            raise ValueError, "ERROR: two variables in ProductExpression:",e
                        v = self._name_fix(e.name)
                        ve = e
                    else:
                        raise ValueError, "ERROR: unexpected item in ProductExpression:"+str(e)
                if x.has_key(v):
                    xv = x[v]
                    x[v] = (xv[0]+c,xv[1])
                else:
                    x[v] = (c,ve)
            #
            # Minus
            #
            elif isinstance(exp,expr._MinusExpression):
                self._Collect2(exp._args[0], x, scale)
                self._Collect2(exp._args[1], x, -scale)
            #
            # ERROR
            #
            else:
                raise ValueError, "Unsupported expression type: "+str(exp)
        #
        # Constant
        #
        elif isinstance(exp,NumericConstant) or isinstance(exp, _ParamData):
            c = exp.value * scale
            if x.has_key("0"):
                xv = x["0"]
                x["0"] = (xv[0]+c,xv[1])
            else:
                x["0"] = (c,"0")
        #
        # Variable
        #
        elif isinstance(exp,_VarData) or isinstance(exp,Var):
            v = self._name_fix(exp.name)
            if x.has_key(v):
                xv = x[v]
                x[v] = (xv[0] + scale, xv[1])
            else:
                x[v] = (scale, exp)
        #
        # ERROR
        #
        else:
            raise ValueError, "Unexpected expression type in _Collect2:"+str(exp)
        return x


    def _Collect3(self, exp):
        x = self._Collect2(exp,{})
        y = {}
        for i in x:
            if x[i][0] != 0.:
                y[i] = x[i]
        return y


    def _Collect(self,model):
        Vars = model.active_components(Var)
        Con = model.active_components(Constraint)
        Obj = model.active_components(Objective)
        Con1 = []
        #
        # Indicate that all variables are unused
        #
        for var in Vars.values():
            for V in var._varval.keys():
                var._varval[V]._sno = -1
        #
        # Call _Collect1 to find the variables that are used in
        # the objective and constraints
        #
        for key in Obj.keys():
            for ondx in Obj[key]._expr:
                try:
                    self._Collect1(Obj[key]._expr[ondx])
                except ValueError, str:
                    print "ERROR: Detected issue during simplification of objective (method=ProblemWriterUtils::_Collect1)"
                    print ("ISSUE: " + `str`),
                    if ondx == None:
                        print ""
                    else:
                        print ", Index="+`ondx`
                    print "Expression=",
                    print Obj[key]._expr[ondx].pprint()
                    raise ValueError,""
        for key in Con.keys():
            C = Con[key]
            for cndx in C.keys():
                try:
                    self._Collect1(C._body[cndx])
                except ValueError, str:
                    print "ERROR: Detected issue during simplification of constraint="+C._name,
                    if cndx == None:
                        print ""
                    else:
                        print ", Index="+`cndx`
                    print "Expression=",
                    print C._body[cndx].pprint()
                    raise ValueError,""
        #
        # Count the number of variables, and order them
        #
        sno = 0
        for var in Vars.values():
            Vv = var._varval
            for V in Vv:
                if Vv[V]._sno != -1:
                    Vv[V]._sno = sno
                    self._varmap[self._name_fix(Vv[V].name)] = Vv[V]
                    sno += 1
        model.nsno = sno
        #
        # Collect the linear terms
        #
        for key in Obj.keys():
            Obj[key]._linterm = {}
            for ondx in Obj[key]._expr:
                Obj[key]._linterm[ondx] = self._Collect3(Obj[key]._expr[ondx])
        for key in Con.keys():
            C = Con[key]
            C._linterm = {}
            Cnz = []
            nt = 0
            for cndx in C.keys():
                t = C._linterm[cndx] = self._Collect3(C._body[cndx])
                lt = len(t)
                if lt > 0:
                    Cnz.append(cndx)
                    nt += 1
            if nt > 0:
                Con1.append(key)
            C._Cnz = Cnz
        model.Cnontriv = Con1
