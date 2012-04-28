#
# Unit Tests for Utility Functions
#

import os
import sys
from os.path import abspath, dirname
sys.path.insert(0, dirname(dirname(abspath(__file__)))+"/../..")
currdir = dirname(abspath(__file__))+os.sep

import pyutilib.th as unittest
from coopr.pyomo import *
from nose.tools import nottest
import pickle

### Added for tests 5,6,7
from coopr.opt import SolverFactory
###

def obj_rule(model):
    return sum(model.x[a] + model.y[a] for a in model.A)
def constr_rule(model,a):
    return model.x[a] >= model.y[a]

class Test(pyutilib.th.TestCase):

    # tests the ability to pickle an abstract model prior to construction,
    # read it back it, and create an instance from it. validation is relatively
    # weak, in that it only tests the validity of an expression constructed
    # using the resulting model.
    def test_pickle1(self):
        model = AbstractModel()
        model.A = Set(initialize=[1,2,3])
        model.B = Param(model.A,initialize={1:100,2:200,3:300})
        model.x = Var(model.A)
        model.y = Var(model.A)
        model.obj = Objective(rule=obj_rule)
	model.constr = Constraint(model.A,rule=constr_rule)
        str = pickle.dumps(model)
        tmodel = pickle.loads(str)
        instance=tmodel.create()
        expr = dot_product(instance.x,instance.B,instance.y)
        OUTPUT=open(currdir+"test_expr1.out","w")
        expr.pprint(ostream=OUTPUT)
        OUTPUT.close()
        self.assertFileEqualsBaseline(currdir+"test_expr1.out",currdir+"test_expr1.txt")

    # same as above, but pickles the constructed AbstractModel and 
    # then operates on the unpickled instance.
    def test_pickle2(self):
        model = AbstractModel()
        model.A = Set(initialize=[1,2,3])
        model.B = Param(model.A,initialize={1:100,2:200,3:300})
        model.x = Var(model.A)
        model.y = Var(model.A)
        model.obj = Objective(rule=obj_rule)
	model.constr = Constraint(model.A,rule=constr_rule)
        tmp=model.create()
        str = pickle.dumps(tmp)
        instance = pickle.loads(str)
        expr = dot_product(instance.x,instance.B,instance.y)
        OUTPUT=open(currdir+"test_expr1.out","w")
        expr.pprint(ostream=OUTPUT)
        OUTPUT.close()
        self.assertFileEqualsBaseline(currdir+"test_expr1.out",currdir+"test_expr1.txt")

    # verifies that the use of lambda expressions as rules yields model instances
    # that are not pickle'able.
    @unittest.skipIf(sys.version_info[:2] < (2,6), "Skipping test because the sparse_dict repn is not supported")
    def test_pickle3(self):
        def rule1(model):
            return (1,model.x+model.y[1],2)
        def rule2(model, i):
            return (1,model.x+model.y[1]+i,2)

        model = AbstractModel()
        model.a = Set(initialize=[1,2,3])
        model.A = Param(initialize=1)
        model.B = Param(model.a, repn='sparse_dict')
        model.x = Var(initialize=1,within=Reals)
        model.y = Var(model.a, initialize=1,within=Reals)
        model.obj = Objective(rule=lambda model: model.x+model.y[1])
        model.obj2 = Objective(model.a,rule=lambda model,i: i+model.x+model.y[1])
        model.con = Constraint(rule=rule1)
        model.con2 = Constraint(model.a, rule=rule2)
        instance = model.create()
        try:
            str = pickle.dumps(instance)
            self.fail("Expected pickling error due to the use of lambda expressions - did not generate one!")
        except pickle.PicklingError:
            pass
        except TypeError:
            pass

    # verifies that we can print a constructed model and obtain identical results before and after 
    # pickling. introduced due to a test case by Gabe that illustrated __getstate__ of various 
    # modeling components was incorrectly and unexpectedly modifying object state.
    def test_pickle4(self):
    
        model = ConcreteModel()
        model.s = Set(initialize=[1,2])
        model.x = Var(within=NonNegativeReals)
        model.x_indexed = Var(model.s, within=NonNegativeReals)
        model.obj = Objective(expr=model.x + model.x_indexed[1] + model.x_indexed[2])
        model.con = Constraint(expr=model.x >= 1)
        model.con2 = Constraint(expr=model.x_indexed[1] + model.x_indexed[2] >= 4)

        inst = model.create()

        OUTPUT=open(currdir+"test_pickle4_baseline.out","w")
        inst.pprint(ostream=OUTPUT)
        OUTPUT.close()
        self.assertFileEqualsBaseline(currdir+"test_pickle4_baseline.out",currdir+"test_pickle4_baseline.txt")

        str = pickle.dumps(inst)

        OUTPUT=open(currdir+"test_pickle4_after.out","w")
        inst.pprint(ostream=OUTPUT)
        OUTPUT.close()
        self.assertFileEqualsBaseline(currdir+"test_pickle4_after.out",currdir+"test_pickle4_baseline.txt")

    # Test that an unpickled instance can be sent through the LP writer
    @nottest
    def has_cplex_lp():
        try:
            cplex = coopr.plugins.solvers.CPLEX(keepFiles=True)
            available = (not cplex.executable() is None) and cplex.available(False)
            return available
        except pyutilib.common.ApplicationError:
            return False

    @unittest.skipUnless(has_cplex_lp(), "Can't find cplex.")
    def test_pickel5(self):
        model = ConcreteModel()
        model.s = Set(initialize=[1,2])
        model.x = Var(within=NonNegativeReals)
        model.x_indexed = Var(model.s, within=NonNegativeReals)
        model.obj = Objective(expr=model.x + model.x_indexed[1] + model.x_indexed[2])
        model.con = Constraint(expr=model.x >= 1)
        model.con2 = Constraint(expr=model.x_indexed[1] + model.x_indexed[2] >= 4)

        inst = model.create()
        strng = pickle.dumps(inst)
        up_inst = pickle.loads(strng)
        opt = SolverFactory('cplex')
        up_inst.preprocess()        # see ticket 4349
        results = opt.solve(up_inst)
        up_inst.load(results)
        assert(abs(up_inst.x.value - 1.0) < .001)
        assert(abs(up_inst.x_indexed[1].value - 0.0) < .001)
        assert(abs(up_inst.x_indexed[2].value - 4.0) < .001)

    # Test that an unpickled instance can be sent through the NL writer
    @nottest
    def has_cplex_nl():
        try:
            cplex = coopr.plugins.solvers.CPLEX(keepFiles=True)
            available = (not cplex.executable() is None) and cplex.available(False)
            asl = coopr.plugins.solvers.ASL(keepFiles=True, options={'solver':'cplexamp'})
            return available and (not asl.executable() is None) and asl.available(False)
        except pyutilib.common.ApplicationError:
            return False
    @unittest.skipUnless(has_cplex_nl(), "Can't find cplexamp.")
    def test_pickel6(self):
        model = ConcreteModel()
        model.s = Set(initialize=[1,2])
        model.x = Var(within=NonNegativeReals)
        model.x_indexed = Var(model.s, within=NonNegativeReals)
        model.obj = Objective(expr=model.x + model.x_indexed[1] + model.x_indexed[2])
        model.con = Constraint(expr=model.x >= 1)
        model.con2 = Constraint(expr=model.x_indexed[1] + model.x_indexed[2] >= 4)

        inst = model.create()
        strng = pickle.dumps(inst)
        up_inst = pickle.loads(strng)
        up_inst.preprocess()        # see ticket 4349        
        opt = SolverFactory('cplexamp',solver_io='nl')
        results = opt.solve(up_inst)
        up_inst.load(results)
        assert(abs(up_inst.x.value - 1.0) < .001)
        assert(abs(up_inst.x_indexed[1].value - 0.0) < .001)
        assert(abs(up_inst.x_indexed[2].value - 4.0) < .001)

    # Test that an unpickled instance can be sent through the cplex python interface
    @nottest
    def module_available(module):
        try:
            __import__(module)
            return True
        except ImportError:
            return False
    @unittest.skipUnless(module_available('cplex'), "Can't cplex python interface.")
    def test_pickel7(self):
        model = ConcreteModel()
        model.s = Set(initialize=[1,2])
        model.x = Var(within=NonNegativeReals)
        model.x_indexed = Var(model.s, within=NonNegativeReals)
        model.obj = Objective(expr=model.x + model.x_indexed[1] + model.x_indexed[2])
        model.con = Constraint(expr=model.x >= 1)
        model.con2 = Constraint(expr=model.x_indexed[1] + model.x_indexed[2] >= 4)

        inst = model.create()
        strng = pickle.dumps(inst)
        up_inst = pickle.loads(strng)
        opt = SolverFactory('cplex',solver_io='python')        
        results = opt.solve(up_inst)
        up_inst.load(results)
        assert(abs(up_inst.x.value - 1.0) < .001)
        assert(abs(up_inst.x_indexed[1].value - 0.0) < .001)
        assert(abs(up_inst.x_indexed[2].value - 4.0) < .001)
        


if __name__ == "__main__":
    unittest.main()
