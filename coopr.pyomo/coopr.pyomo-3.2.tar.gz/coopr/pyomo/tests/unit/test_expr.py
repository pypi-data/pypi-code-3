#
# Unit Tests for expression generation
#
#

import os
import sys
from os.path import abspath, dirname
sys.path.insert(0, dirname(dirname(abspath(__file__)))+"/../..")
currdir = dirname(abspath(__file__))+os.sep

import copy
import StringIO

import pyutilib.th as unittest
from coopr.pyomo import *
from coopr.pyomo.base.expr import *
from coopr.pyomo.base.expr import _SumExpression, _ProductExpression, \
     _IntrinsicFunctionExpression, _PowExpression
from coopr.pyomo.base.var import _VarElement
from coopr.pyomo.base.intrinsic_functions import generate_intrinsic_function_expression
from nose.tools import nottest


class Expression_EvaluateNumericConstant(unittest.TestCase):

    def setUp(self):
        # Do we expect arithmetic operations to return expressions?
        self.expectExpression = False
        # Do we expect relational tests to return constant expressions?
        self.expectConstExpression = True

    def tearDown(self):
        pass

    def create(self,val,domain):
        return NumericConstant(None,domain,val)

    @nottest
    def value_test(self, exp, val, expectExpression=None):
        if expectExpression is None:
            expectExpression = self.expectExpression
        self.assertEqual(isinstance(exp,Expression), expectExpression)
        self.assertEqual(exp(), val)

    @nottest
    def relation_test(self, exp, val, expectConstExpression=None):
        if expectConstExpression is None:
            expectConstExpression = self.expectConstExpression
        # This had better be a expression
        self.assertTrue(isinstance(exp, Expression))
        self.assertEqual(exp.is_relational(), True)
        # Check that the expression evaluates correctly
        self.assertEqual(exp(), val)
        # Check that the expression evaluates correctly in a Boolean context
        if expectConstExpression:
            self.assertEqual(bool(exp), val)
            self.assertIsNone(generate_relational_expression.chainedInequality)
        else:
            self.assertEqual(bool(exp), True)
            self.assertIs(exp,generate_relational_expression.chainedInequality)
            generate_relational_expression.chainedInequality = None

    def test_valid_value(self):
        """Check that values can be validated"""
        a=self.create(1.3, Reals)
        self.assertTrue(a._valid_value(a.value))

        b = self.create(1.3, Integers)
        self.assertRaises(ValueError, b._valid_value, b.value)
        self.assertEqual(b._valid_value(b.value, False), False)

    def Xtest_getattr(self):
        """Check that attributes can be retrieved"""
        a=self.create(1.3,Reals)
        self.assertRaises(AttributeError, a.__getattr__, "_x")
        self.assertRaises(AttributeError, a.__getattr__, "x")

    def Xtest_setattr(self):
        """Check that attributes can be set"""
        a=self.create(1.3,Reals)
        try:
            a.x=1
        except AttributeError:
            pass
        else:
            self.fail("test_setattr")
        a._x=1
        tmp=a._x
        a._standard_attr.add("x")
        a.x=1

    def test_lt(self):
        a=self.create(1.3,Reals)
        b=self.create(2.0,Reals)
        self.relation_test(a<b,True)
        self.relation_test(a<a,False)
        self.relation_test(b<a,False)
        self.relation_test(a<2.0,True)
        self.relation_test(a<1.3,False)
        self.relation_test(b<1.3,False)
        self.relation_test(1.3<b,True)
        self.relation_test(1.3<a,False)
        self.relation_test(2.0<a,False)

    def test_gt(self):
        a=self.create(1.3,Reals)
        b=self.create(2.0,Reals)
        self.relation_test(a>b,False)
        self.relation_test(a>a,False)
        self.relation_test(b>a,True)
        self.relation_test(a>2.0,False)
        self.relation_test(a>1.3,False)
        self.relation_test(b>1.3,True)
        self.relation_test(1.3>b,False)
        self.relation_test(1.3>a,False)
        self.relation_test(2.0>a,True)

    def test_eq(self):
        a=self.create(1.3,Reals)
        b=self.create(2.0,Reals)
        self.relation_test(a==b,False,True)
        self.relation_test(a==a,True,True)
        self.relation_test(b==a,False,True)
        self.relation_test(a==2.0,False,True)
        self.relation_test(a==1.3,True,True)
        self.relation_test(b==1.3,False,True)
        self.relation_test(1.3==b,False,True)
        self.relation_test(1.3==a,True,True)
        self.relation_test(2.0==a,False,True)

    def test_arithmetic(self):
        a=self.create(-0.5,Reals)
        b=self.create(2.0,Reals)
        self.value_test(a-b,-2.5)
        self.value_test(a+b,1.5)
        self.value_test(a*b,-1.0)
        self.value_test(b/a,-4.0)
        self.value_test(a**b,0.25,True)

        self.value_test(a-2.0,-2.5)
        self.value_test(a+2.0,1.5)
        self.value_test(a*2.0,-1.0)
        self.value_test(b/(0.5),4.0)
        self.value_test(a**2.0,0.25,True)

        self.value_test(0.5-b,-1.5)
        self.value_test(0.5+b,2.5)
        self.value_test(0.5*b,1.0)
        self.value_test(2.0/a,-4.0)
        self.value_test((0.5)**b,0.25,True)

        self.value_test(-a,0.5)
        self.value_test(+a,-0.5,False)
        self.value_test(abs(-a),0.5,True)

    # FIXME: This doesn't belong here: we need to create a test_numvalue.py
    def test_asnum(self):
        try:
            as_numeric(None)
            self.fail("test_asnum - expected ValueError")
        except ValueError:
            pass


class Expression_EvaluateVarData(Expression_EvaluateNumericConstant):

    def setUp(self):
        import coopr.pyomo.base.var
        #
        # Create Model
        #
        Expression_EvaluateNumericConstant.setUp(self)
        #
        # Create model instance
        #
        self.expectExpression = True
        self.expectConstExpression = False

    def create(self,val,domain):
        tmp=coopr.pyomo.base.var._VarData("unknown", domain, None)
        tmp.value=val
        return tmp


class Expression_EvaluateVar(Expression_EvaluateNumericConstant):

    def setUp(self):
        import coopr.pyomo.base.var
        #
        # Create Model
        #
        Expression_EvaluateNumericConstant.setUp(self)
        #
        # Create model instance
        #
        self.expectExpression = True
        self.expectConstExpression = False

    def create(self,val,domain):
        tmp=Var(name="unknown",domain=domain)
        tmp.value=val
        return tmp


class Expression_EvaluateFixedVar(Expression_EvaluateNumericConstant):

    def setUp(self):
        import coopr.pyomo.base.var
        #
        # Create Model
        #
        Expression_EvaluateNumericConstant.setUp(self)
        #
        # Create model instance
        #
        self.expectExpression = True
        self.expectConstExpression = True

    def create(self,val,domain):
        tmp=Var(name="unknown",domain=domain)
        tmp.fixed=True
        tmp.value=val
        return tmp


class Expression_EvaluateParam(Expression_EvaluateNumericConstant):

    def setUp(self):
        import coopr.pyomo.base.var
        #
        # Create Model
        #
        Expression_EvaluateNumericConstant.setUp(self)
        #
        # Create model instance
        #
        self.expectExpression = True
        self.expectConstExpression = True

    def create(self,val,domain):
        tmp=Param(within=domain)
        tmp.value = val
        return tmp


class TestNumericValue(pyutilib.th.TestCase):

    def test_vals(self):
        # the following aspect of this test is being removed due to the
        # check seminatics of a numeric constant requiring far too much
        # run-time, especially when involved in expression tree
        # construction. if the user specifies a constant, we're assuming
        # it is correct.

        #try:
        #    NumericConstant(None,None,value='a')
        #    self.fail("Cannot initialize a constant with a non-numeric value")
        #except ValueError:
        #    pass

        a = NumericConstant(None,None,1.1)
        b = float(a)
        self.assertEqual(b,1.1)
        b = int(a)
        self.assertEqual(b,1)

    def Xtest_getattr1(self):
        a = NumericConstant(None,None,1.1)
        try:
            a.model
            self.fail("Expected error")
        except AttributeError:
            pass

    def test_ops(self):
        a = NumericConstant(None,None,1.1)
        b = NumericConstant(None,None,2.2)
        c = NumericConstant(None,None,-2.2)
        a <= b
        self.assertEqual(a() <= b(), True)
        self.assertEqual(a() >= b(), False)
        self.assertEqual(a() == b(), False)
        self.assertEqual(abs(a() + b()-3.3) <= 1e-7, True)
        self.assertEqual(abs(b() - a()-1.1) <= 1e-7, True)
        self.assertEqual(abs(b() * 3-6.6) <= 1e-7, True)
        self.assertEqual(abs(b() / 2-1.1) <= 1e-7, True)
        self.assertEqual(abs(abs(-b())-2.2) <= 1e-7, True)
        self.assertEqual(abs(c()), 2.2)
        self.assertEqual(str(c), "-2.2")



class Generate_SumExpression(pyutilib.th.TestCase):
    def test_simpleSum(self):
        m = AbstractModel()
        m.a = Var()
        m.b = Var()
        e = m.a + m.b
        self.assertIs(type(e), _SumExpression)
        self.assertEqual(e._const, 0)
        self.assertEqual(len(e._args), 2)
        self.assertIs(e._args[0], m.a)
        self.assertIs(e._args[1], m.b)
        self.assertEqual(len(e._coef), 2)
        self.assertEqual(e._coef[0], 1)
        self.assertEqual(e._coef[1], 1)

    def test_constSum(self):
        m = AbstractModel()
        m.a = Var()
        e = m.a + 5
        self.assertIs(type(e), _SumExpression)
        self.assertEqual(e._const, 5)
        self.assertEqual(len(e._args), 1)
        self.assertIs(e._args[0], m.a)
        self.assertEqual(len(e._coef), 1)
        self.assertEqual(e._coef[0], 1)

        e = 5 + m.a
        self.assertIs(type(e), _SumExpression)
        self.assertEqual(e._const, 5)
        self.assertEqual(len(e._args), 1)
        self.assertIs(e._args[0], m.a)
        self.assertEqual(len(e._coef), 1)
        self.assertEqual(e._coef[0], 1)

    def test_nestedSum(self):
        m = AbstractModel()
        m.a = Var()
        m.b = Var()
        m.c = Var()
        m.d = Var()
        e1 = m.a + m.b
        e = e1 + 5
        self.assertIs(type(e), _SumExpression)
        self.assertEqual(e._const, 5)
        self.assertEqual(len(e._args), 2)
        self.assertIs(e._args[0], m.a)
        self.assertIs(e._args[1], m.b)
        self.assertEqual(len(e._coef), 2)
        self.assertEqual(e._coef[0], 1)
        self.assertEqual(e._coef[1], 1)

        e = 5 + e1
        self.assertIs(type(e), _SumExpression)
        self.assertEqual(e._const, 5)
        self.assertEqual(len(e._args), 2)
        self.assertIs(e._args[0], m.a)
        self.assertIs(e._args[1], m.b)
        self.assertEqual(len(e._coef), 2)
        self.assertEqual(e._coef[0], 1)
        self.assertEqual(e._coef[1], 1)

        e = e1 + m.c
        self.assertIs(type(e), _SumExpression)
        self.assertEqual(e._const, 0)
        self.assertEqual(len(e._args), 3)
        self.assertIs(e._args[0], m.a)
        self.assertIs(e._args[1], m.b)
        self.assertIs(e._args[2], m.c)
        self.assertEqual(len(e._coef), 3)
        self.assertEqual(e._coef[0], 1)
        self.assertEqual(e._coef[1], 1)
        self.assertEqual(e._coef[1], 1)

        e = m.c + e1
        self.assertIs(type(e), _SumExpression)
        self.assertEqual(e._const, 0)
        self.assertEqual(len(e._args), 3)
        self.assertIs(e._args[0], m.c)
        self.assertIs(e._args[1], m.a)
        self.assertIs(e._args[2], m.b)
        self.assertEqual(len(e._coef), 3)
        self.assertEqual(e._coef[0], 1)
        self.assertEqual(e._coef[1], 1)
        self.assertEqual(e._coef[2], 1)

        e2 = m.c + m.d
        e = e1 + e2
        self.assertIs(type(e), _SumExpression)
        self.assertEqual(e._const, 0)
        self.assertEqual(len(e._args), 4)
        self.assertIs(e._args[0], m.a)
        self.assertIs(e._args[1], m.b)
        self.assertIs(e._args[2], m.c)
        self.assertIs(e._args[3], m.d)
        self.assertEqual(len(e._coef), 4)
        self.assertEqual(e._coef[0], 1)
        self.assertEqual(e._coef[1], 1)
        self.assertEqual(e._coef[2], 1)
        self.assertEqual(e._coef[3], 1)

    def test_trivialSum(self):
        m = AbstractModel()
        m.a = Var()
        e = m.a + 0
        self.assertIs(type(e), type(m.a))
        self.assertIs(e, m.a)

        e = 0 + m.a
        self.assertIs(type(e), type(m.a))
        self.assertIs(e, m.a)

    def test_sumOf_nestedTrivialProduct(self):
        m = AbstractModel()
        m.a = Var()
        m.b = Var()
        m.c = Var()
        e1 = m.a * 5
        e = e1 + m.b
        self.assertIs(type(e), _SumExpression)
        self.assertEqual(e._const, 0)
        self.assertEqual(len(e._args), 2)
        self.assertIs(e._args[0], m.a)
        self.assertIs(e._args[1], m.b)
        self.assertEqual(len(e._coef), 2)
        self.assertEqual(e._coef[0], 5)
        self.assertEqual(e._coef[1], 1)

        e = m.b + e1
        self.assertIs(type(e), _SumExpression)
        self.assertEqual(e._const, 0)
        self.assertEqual(len(e._args), 2)
        self.assertIs(e._args[0], m.b)
        self.assertIs(e._args[1], m.a)
        self.assertEqual(len(e._coef), 2)
        self.assertEqual(e._coef[0], 1)
        self.assertEqual(e._coef[1], 5)

        e2 = m.b + m.c
        e = e1 + e2
        self.assertIs(type(e), _SumExpression)
        self.assertEqual(e._const, 0)
        self.assertEqual(len(e._args), 3)
        self.assertIs(e._args[0], m.a)
        self.assertIs(e._args[1], m.b)
        self.assertIs(e._args[2], m.c)
        self.assertEqual(len(e._coef), 3)
        self.assertEqual(e._coef[0], 5)
        self.assertEqual(e._coef[1], 1)
        self.assertEqual(e._coef[2], 1)

        e2 = m.b + m.c
        e = e2 + e1
        self.assertIs(type(e), _SumExpression)
        self.assertEqual(e._const, 0)
        self.assertEqual(len(e._args), 3)
        self.assertIs(e._args[0], m.b)
        self.assertIs(e._args[1], m.c)
        self.assertIs(e._args[2], m.a)
        self.assertEqual(len(e._coef), 3)
        self.assertEqual(e._coef[0], 1)
        self.assertEqual(e._coef[1], 1)
        self.assertEqual(e._coef[2], 5)


    def test_simpleDiff(self):
        m = AbstractModel()
        m.a = Var()
        m.b = Var()
        e = m.a - m.b
        self.assertIs(type(e), _SumExpression)
        self.assertEqual(e._const, 0)
        self.assertEqual(len(e._args), 2)
        self.assertIs(e._args[0], m.a)
        self.assertIs(e._args[1], m.b)
        self.assertEqual(len(e._coef), 2)
        self.assertEqual(e._coef[0], 1)
        self.assertEqual(e._coef[1], -1)

    def test_constDiff(self):
        m = AbstractModel()
        m.a = Var()
        e = m.a - 5
        self.assertIs(type(e), _SumExpression)
        self.assertEqual(e._const, -5)
        self.assertEqual(len(e._args), 1)
        self.assertIs(e._args[0], m.a)
        self.assertEqual(len(e._coef), 1)
        self.assertEqual(e._coef[0], 1)

        e = 5 - m.a
        self.assertIs(type(e), _SumExpression)
        self.assertEqual(e._const, 5)
        self.assertEqual(len(e._args), 1)
        self.assertIs(e._args[0], m.a)
        self.assertEqual(len(e._coef), 1)
        self.assertEqual(e._coef[0], -1)

    def test_nestedDiff(self):
        m = AbstractModel()
        m.a = Var()
        m.b = Var()
        m.c = Var()
        m.d = Var()
        e1 = m.a - m.b
        e = e1 - 5
        self.assertIs(type(e), _SumExpression)
        self.assertEqual(e._const, -5)
        self.assertEqual(len(e._args), 2)
        self.assertIs(e._args[0], m.a)
        self.assertIs(e._args[1], m.b)
        self.assertEqual(len(e._coef), 2)
        self.assertEqual(e._coef[0], 1)
        self.assertEqual(e._coef[1], -1)

        e = 5 - e1
        self.assertIs(type(e), _SumExpression)
        self.assertEqual(e._const, 5)
        self.assertEqual(len(e._args), 2)
        self.assertIs(e._args[0], m.a)
        self.assertIs(e._args[1], m.b)
        self.assertEqual(len(e._coef), 2)
        self.assertEqual(e._coef[0], -1)
        self.assertEqual(e._coef[1], 1)

        e = e1 - m.c
        self.assertIs(type(e), _SumExpression)
        self.assertEqual(e._const, 0)
        self.assertEqual(len(e._args), 3)
        self.assertIs(e._args[0], m.a)
        self.assertIs(e._args[1], m.b)
        self.assertIs(e._args[2], m.c)
        self.assertEqual(len(e._coef), 3)
        self.assertEqual(e._coef[0], 1)
        self.assertEqual(e._coef[1], -1)
        self.assertEqual(e._coef[1], -1)

        e = m.c - e1
        self.assertIs(type(e), _SumExpression)
        self.assertEqual(e._const, 0)
        self.assertEqual(len(e._args), 3)
        self.assertIs(e._args[0], m.c)
        self.assertIs(e._args[1], m.a)
        self.assertIs(e._args[2], m.b)
        self.assertEqual(len(e._coef), 3)
        self.assertEqual(e._coef[0], 1)
        self.assertEqual(e._coef[1], -1)
        self.assertEqual(e._coef[2], 1)

        e2 = m.c - m.d
        e = e1 - e2
        self.assertIs(type(e), _SumExpression)
        self.assertEqual(e._const, 0)
        self.assertEqual(len(e._args), 4)
        self.assertIs(e._args[0], m.a)
        self.assertIs(e._args[1], m.b)
        self.assertIs(e._args[2], m.c)
        self.assertIs(e._args[3], m.d)
        self.assertEqual(len(e._coef), 4)
        self.assertEqual(e._coef[0], 1)
        self.assertEqual(e._coef[1], -1)
        self.assertEqual(e._coef[2], -1)
        self.assertEqual(e._coef[3], 1)

        e = e2 - e1
        self.assertIs(type(e), _SumExpression)
        self.assertEqual(e._const, 0)
        self.assertEqual(len(e._args), 4)
        self.assertIs(e._args[0], m.c)
        self.assertIs(e._args[1], m.d)
        self.assertIs(e._args[2], m.a)
        self.assertIs(e._args[3], m.b)
        self.assertEqual(len(e._coef), 4)
        self.assertEqual(e._coef[0], 1)
        self.assertEqual(e._coef[1], -1)
        self.assertEqual(e._coef[2], -1)
        self.assertEqual(e._coef[3], 1)


    def test_trivialDiff(self):
        m = AbstractModel()
        m.a = Var()
        e = m.a - 0
        self.assertIs(type(e), type(m.a))
        self.assertIs(e, m.a)

        e = 0 - m.a
        self.assertIs(type(e), _SumExpression)
        self.assertEqual(e._const, 0)
        self.assertEqual(len(e._args), 1)
        self.assertIs(e._args[0], m.a)
        self.assertEqual(len(e._coef), 1)
        self.assertEqual(e._coef[0], -1)

    def test_sumOf_nestedTrivialProduct(self):
        m = AbstractModel()
        m.a = Var()
        m.b = Var()
        m.c = Var()
        e1 = m.a * 5
        e = e1 - m.b
        self.assertIs(type(e), _SumExpression)
        self.assertEqual(e._const, 0)
        self.assertEqual(len(e._args), 2)
        self.assertIs(e._args[0], m.a)
        self.assertIs(e._args[1], m.b)
        self.assertEqual(len(e._coef), 2)
        self.assertEqual(e._coef[0], 5)
        self.assertEqual(e._coef[1], -1)

        e = m.b - e1
        self.assertIs(type(e), _SumExpression)
        self.assertEqual(e._const, 0)
        self.assertEqual(len(e._args), 2)
        self.assertIs(e._args[0], m.b)
        self.assertIs(e._args[1], m.a)
        self.assertEqual(len(e._coef), 2)
        self.assertEqual(e._coef[0], 1)
        self.assertEqual(e._coef[1], -5)

        e2 = m.b - m.c
        e = e1 - e2
        self.assertIs(type(e), _SumExpression)
        self.assertEqual(e._const, 0)
        self.assertEqual(len(e._args), 3)
        self.assertIs(e._args[0], m.a)
        self.assertIs(e._args[1], m.b)
        self.assertIs(e._args[2], m.c)
        self.assertEqual(len(e._coef), 3)
        self.assertEqual(e._coef[0], 5)
        self.assertEqual(e._coef[1], -1)
        self.assertEqual(e._coef[2], 1)

        e = e2 - e1
        self.assertIs(type(e), _SumExpression)
        self.assertEqual(e._const, 0)
        self.assertEqual(len(e._args), 3)
        self.assertIs(e._args[0], m.b)
        self.assertIs(e._args[1], m.c)
        self.assertIs(e._args[2], m.a)
        self.assertEqual(len(e._coef), 3)
        self.assertEqual(e._coef[0], 1)
        self.assertEqual(e._coef[1], -1)
        self.assertEqual(e._coef[2], -5)


class Generate_ProductExpression(pyutilib.th.TestCase):
    def test_simpleProduct(self):
        m = AbstractModel()
        m.a = Var()
        m.b = Var()
        e = m.a * m.b
        self.assertIs(type(e), _ProductExpression)
        self.assertIsNone(e._args)
        self.assertEqual(e.coef, 1)
        self.assertEqual(len(e._numerator), 2)
        self.assertEqual(len(e._denominator), 0)
        self.assertIs(e._numerator[0], m.a)
        self.assertIs(e._numerator[1], m.b)

    def test_constProduct(self):
        m = AbstractModel()
        m.a = Var()
        e = m.a * 5
        self.assertIs(type(e), _ProductExpression)
        self.assertIsNone(e._args)
        self.assertEqual(e.coef, 5)
        self.assertEqual(len(e._numerator), 1)
        self.assertEqual(len(e._denominator), 0)
        self.assertIs(e._numerator[0], m.a)

        e = 5 * m.a
        self.assertIs(type(e), _ProductExpression)
        self.assertIsNone(e._args)
        self.assertEqual(e.coef, 5)
        self.assertEqual(len(e._numerator), 1)
        self.assertEqual(len(e._denominator), 0)
        self.assertIs(e._numerator[0], m.a)

    def test_nestedProduct(self):
        m = AbstractModel()
        m.a = Var()
        m.b = Var()
        m.c = Var()
        m.d = Var()
        e1 = m.a * m.b
        e = e1 * 5
        self.assertIs(type(e), _ProductExpression)
        self.assertIsNone(e._args)
        self.assertEqual(e.coef, 5)
        self.assertEqual(len(e._numerator), 2)
        self.assertEqual(len(e._denominator), 0)
        self.assertIs(e._numerator[0], m.a)
        self.assertIs(e._numerator[1], m.b)

        e = 5 * e1
        self.assertIs(type(e), _ProductExpression)
        self.assertIsNone(e._args)
        self.assertEqual(e.coef, 5)
        self.assertEqual(len(e._numerator), 2)
        self.assertEqual(len(e._denominator), 0)
        self.assertIs(e._numerator[0], m.a)
        self.assertIs(e._numerator[1], m.b)

        e = e1 * m.c
        self.assertIs(type(e), _ProductExpression)
        self.assertIsNone(e._args)
        self.assertEqual(e.coef, 1)
        self.assertEqual(len(e._numerator), 3)
        self.assertEqual(len(e._denominator), 0)
        self.assertIs(e._numerator[0], m.a)
        self.assertIs(e._numerator[1], m.b)
        self.assertIs(e._numerator[2], m.c)

        e = m.c * e1
        self.assertIs(type(e), _ProductExpression)
        self.assertIsNone(e._args)
        self.assertEqual(e.coef, 1)
        self.assertEqual(len(e._numerator), 3)
        self.assertEqual(len(e._denominator), 0)
        self.assertIs(e._numerator[0], m.c)
        self.assertIs(e._numerator[1], m.a)
        self.assertIs(e._numerator[2], m.b)

        e2 = m.c * m.d
        e = e1 * e2
        self.assertIs(type(e), _ProductExpression)
        self.assertIsNone(e._args)
        self.assertEqual(e.coef, 1)
        self.assertEqual(len(e._numerator), 4)
        self.assertEqual(len(e._denominator), 0)
        self.assertIs(e._numerator[0], m.a)
        self.assertIs(e._numerator[1], m.b)
        self.assertIs(e._numerator[2], m.c)
        self.assertIs(e._numerator[3], m.d)

    def test_trivialProduct(self):
        m = AbstractModel()
        m.a = Var()
        e = m.a * 0
        self.assertIs(type(e), NumericConstant)
        self.assertEqual(e(), 0)

        e = 0 * m.a
        self.assertIs(type(e), NumericConstant)
        self.assertEqual(e(), 0)

        e = m.a * 1
        self.assertIs(type(e), type(m.a))
        self.assertIs(e, m.a)

        e = 1 * m.a
        self.assertIs(type(e), type(m.a))
        self.assertIs(e, m.a)

        e = NumericConstant(None,None,3) * NumericConstant(None,None,2)
        self.assertIs(type(e), NumericConstant)
        self.assertEqual(e(), 6)


    def test_simpleDivision(self):
        m = AbstractModel()
        m.a = Var()
        m.b = Var()
        e = m.a / m.b
        self.assertIs(type(e), _ProductExpression)
        self.assertIsNone(e._args)
        self.assertEqual(e.coef, 1)
        self.assertEqual(len(e._numerator), 1)
        self.assertEqual(len(e._denominator), 1)
        self.assertIs(e._numerator[0], m.a)
        self.assertIs(e._denominator[0], m.b)

    def test_constDivision(self):
        m = AbstractModel()
        m.a = Var()
        e = m.a / 5
        self.assertIs(type(e), _ProductExpression)
        self.assertIsNone(e._args)
        self.assertEqual(e.coef, 1./5.)
        self.assertEqual(len(e._numerator), 1)
        self.assertEqual(len(e._denominator), 0)
        self.assertIs(e._numerator[0], m.a)

        e = 5 / m.a
        self.assertIs(type(e), _ProductExpression)
        self.assertIsNone(e._args)
        self.assertEqual(e.coef, 5)
        self.assertEqual(len(e._numerator), 0)
        self.assertEqual(len(e._denominator), 1)
        self.assertIs(e._denominator[0], m.a)

    def test_nestedDivision(self):
        m = AbstractModel()
        m.a = Var()
        m.b = Var()
        m.c = Var()
        m.d = Var()
        e1 = m.a / m.b
        e = e1 / 5
        self.assertIs(type(e), _ProductExpression)
        self.assertIsNone(e._args)
        self.assertEqual(e.coef, 1./5.)
        self.assertEqual(len(e._numerator), 1)
        self.assertEqual(len(e._denominator), 1)
        self.assertIs(e._numerator[0], m.a)
        self.assertIs(e._denominator[0], m.b)

        e = 5 / e1
        self.assertIs(type(e), _ProductExpression)
        self.assertIsNone(e._args)
        self.assertEqual(e.coef, 5)
        self.assertEqual(len(e._numerator), 1)
        self.assertEqual(len(e._denominator), 1)
        self.assertIs(e._numerator[0], m.b)
        self.assertIs(e._denominator[0], m.a)

        e = e1 / m.c
        self.assertIs(type(e), _ProductExpression)
        self.assertIsNone(e._args)
        self.assertEqual(e.coef, 1)
        self.assertEqual(len(e._numerator), 1)
        self.assertEqual(len(e._denominator), 2)
        self.assertIs(e._numerator[0], m.a)
        self.assertIs(e._denominator[0], m.b)
        self.assertIs(e._denominator[1], m.c)

        e = m.c / e1
        self.assertIs(type(e), _ProductExpression)
        self.assertIsNone(e._args)
        self.assertEqual(e.coef, 1)
        self.assertEqual(len(e._numerator), 2)
        self.assertEqual(len(e._denominator), 1)
        self.assertIs(e._numerator[0], m.c)
        self.assertIs(e._numerator[1], m.b)
        self.assertIs(e._denominator[0], m.a)

        e2 = m.c / m.d
        e = e1 / e2
        self.assertIs(type(e), _ProductExpression)
        self.assertIsNone(e._args)
        self.assertEqual(e.coef, 1)
        self.assertEqual(len(e._numerator), 2)
        self.assertEqual(len(e._denominator), 2)
        self.assertIs(e._numerator[0], m.a)
        self.assertIs(e._numerator[1], m.d)
        self.assertIs(e._denominator[0], m.b)
        self.assertIs(e._denominator[1], m.c)

    def test_trivialDivision(self):
        m = AbstractModel()
        m.a = Var()
        self.assertRaises(ZeroDivisionError, m.a.__div__, 0)

        e = 0 / m.a
        self.assertIs(type(e), NumericConstant)
        self.assertAlmostEqual(e(), 0.0)

        e = m.a / 1
        self.assertIs(type(e), type(m.a))
        self.assertIs(e, m.a)

        e = 1 / m.a
        self.assertIs(type(e), _ProductExpression)
        self.assertIsNone(e._args)
        self.assertEqual(e.coef, 1)
        self.assertEqual(len(e._numerator), 0)
        self.assertEqual(len(e._denominator), 1)
        self.assertIs(e._denominator[0], m.a)

        e = NumericConstant(None,None,3) / NumericConstant(None,None,2)
        self.assertIs(type(e), NumericConstant)
        self.assertEqual(e(), 1.5)


class Generate_RelationalExpression(pyutilib.th.TestCase):
    def setUp(self):
        m = AbstractModel()
        m.I = Set()
        m.a = Var()
        m.b = Var()
        m.c = Var()
        m.x = Var(m.I)
        self.m = m

    def test_simpleEquality(self):
        m = self.m
        e = m.a == m.b
        self.assertIs(type(e), _EqualityExpression)
        self.assertEqual(len(e._args), 2)
        self.assertIs(e._args[0], m.a)
        self.assertIs(e._args[1], m.b)

    def test_equalityErrors(self):
        m = self.m
        e = m.a == m.b
        # Python 2.7 supports better testing of exceptions
        if sys.hexversion >= 0x02070000:
            self.assertRaisesRegexp(TypeError, "EqualityExpression .*"
                                   "sub-expressions is a relational",
                                   e.__eq__, m.a)
            self.assertRaisesRegexp(TypeError, "EqualityExpression .*"
                                   "sub-expressions is a relational",
                                   m.a.__eq__, e)

            # NB: cannot test the reverse here: _VarArray (correctly)
            # does not define __eq__
            self.assertRaisesRegexp(TypeError, "Argument .*"
                                    "is an indexed numeric value",
                                    m.a.__eq__, m.x)
        else:
            self.assertRaises(TypeError, e.__eq__, m.a)
            self.assertRaises(TypeError, m.a.__eq__, e)
            self.assertRaises(TypeError, m.a.__eq__, m.x)

        try:
            e == m.a
            self.fail("expected nested equality expression to raise TypeError")
        except TypeError:
            pass

        try:
            m.a == e
            self.fail("expected nested equality expression to raise TypeError")
        except TypeError:
            pass

        try:
            m.x == m.a
            self.fail("expected use of indexed variable to raise TypeError")
        except TypeError:
            pass

        try:
            m.a == m.x
            self.fail("expected use of indexed variable to raise TypeError")
        except TypeError:
            pass

    def test_simpleInequality(self):
        m = self.m
        e = m.a < m.b
        self.assertIs(type(e), _InequalityExpression)
        self.assertEqual(len(e._args), 2)
        self.assertIs(e._args[0], m.a)
        self.assertIs(e._args[1], m.b)
        self.assertEqual(len(e._strict), 1)
        self.assertEqual(e._strict[0], True)

        e = m.a <= m.b
        self.assertIs(type(e), _InequalityExpression)
        self.assertEqual(len(e._args), 2)
        self.assertIs(e._args[0], m.a)
        self.assertIs(e._args[1], m.b)
        self.assertEqual(len(e._strict), 1)
        self.assertEqual(e._strict[0], False)

        e = m.a > m.b
        self.assertIs(type(e), _InequalityExpression)
        self.assertEqual(len(e._args), 2)
        self.assertIs(e._args[0], m.b)
        self.assertIs(e._args[1], m.a)
        self.assertEqual(len(e._strict), 1)
        self.assertEqual(e._strict[0], True)

        e = m.a >= m.b
        self.assertIs(type(e), _InequalityExpression)
        self.assertEqual(len(e._args), 2)
        self.assertIs(e._args[0], m.b)
        self.assertIs(e._args[1], m.a)
        self.assertEqual(len(e._strict), 1)
        self.assertEqual(e._strict[0], False)


    def test_compoundInequality(self):
        m = self.m
        e = m.a < m.b < m.c
        self.assertIs(type(e), _InequalityExpression)
        self.assertEqual(len(e._args), 3)
        self.assertIs(e._args[0], m.a)
        self.assertIs(e._args[1], m.b)
        self.assertIs(e._args[2], m.c)
        self.assertEqual(len(e._strict), 2)
        self.assertEqual(e._strict[0], True)
        self.assertEqual(e._strict[1], True)

        e = m.a <= m.b <= m.c
        self.assertIs(type(e), _InequalityExpression)
        self.assertEqual(len(e._args), 3)
        self.assertIs(e._args[0], m.a)
        self.assertIs(e._args[1], m.b)
        self.assertIs(e._args[2], m.c)
        self.assertEqual(len(e._strict), 2)
        self.assertEqual(e._strict[0], False)
        self.assertEqual(e._strict[1], False)

        e = m.a > m.b > m.c
        self.assertIs(type(e), _InequalityExpression)
        self.assertEqual(len(e._args), 3)
        self.assertIs(e._args[0], m.c)
        self.assertIs(e._args[1], m.b)
        self.assertIs(e._args[2], m.a)
        self.assertEqual(len(e._strict), 2)
        self.assertEqual(e._strict[0], True)
        self.assertEqual(e._strict[1], True)

        e = m.a >= m.b >= m.c
        self.assertIs(type(e), _InequalityExpression)
        self.assertEqual(len(e._args), 3)
        self.assertIs(e._args[0], m.c)
        self.assertIs(e._args[1], m.b)
        self.assertIs(e._args[2], m.a)
        self.assertEqual(len(e._strict), 2)
        self.assertEqual(e._strict[0], False)
        self.assertEqual(e._strict[1], False)

        e = 0 <= m.a < 1
        self.assertIs(type(e), _InequalityExpression)
        self.assertEqual(len(e._args), 3)
        self.assertEqual(e._args[0](), 0)
        self.assertIs(e._args[1], m.a)
        self.assertEqual(e._args[2](), 1)
        self.assertEqual(len(e._strict), 2)
        self.assertEqual(e._strict[0], False)
        self.assertEqual(e._strict[1], True)

        e = 0 <= 1 < m.a
        self.assertIs(type(e), _InequalityExpression)
        self.assertEqual(len(e._args), 2)
        self.assertEqual(e._args[0](), 1)
        self.assertIs(e._args[1], m.a)
        self.assertEqual(len(e._strict), 1)
        self.assertEqual(e._strict[0], True)

        e = m.a <= 0 <= 1
        self.assertIs(type(e), bool)
        self.assertEqual(e, True)
        self.assertIsNotNone(generate_relational_expression.chainedInequality)
        try:
            m.a == m.b
            self.fail("expected construction of relational expression to "
                      "generate a chainedInequality TypeError")
        except TypeError:
            pass

    def test_inequalityErrors(self):
        m = self.m
        e = m.a <= m.b <= m.c
        e1 = m.a == m.b
        # Python 2.7 supports better testing of exceptions
        if sys.hexversion >= 0x02070000:
            self.assertRaisesRegexp(TypeError, "Argument .*"
                                    "is an indexed numeric value",
                                    m.a.__lt__, m.x)
            self.assertRaisesRegexp(TypeError, "Argument .*"
                                    "is an indexed numeric value",
                                    m.a.__gt__, m.x)

            self.assertRaisesRegexp(ValueError, "InequalityExpression .*"
                                   "more than 3 terms",
                                   e.__lt__, m.c)
            self.assertRaisesRegexp(ValueError, "InequalityExpression .*"
                                   "more than 3 terms",
                                   e.__gt__, m.c)

            self.assertRaisesRegexp(TypeError, "InequalityExpression .*"
                                   "both sub-expressions are also relational",
                                   e.__lt__, m.a < m.b)

            self.assertRaisesRegexp(TypeError, "InequalityExpression .*"
                                   "sub-expressions is an equality",
                                   m.a.__lt__, e1)
            self.assertRaisesRegexp(TypeError, "InequalityExpression .*"
                                   "sub-expressions is an equality",
                                   m.a.__gt__, e1)
        else:
            self.assertRaises(TypeError, m.a.__lt__, m.x)
            self.assertRaises(TypeError, m.a.__gt__, m.x)
            self.assertRaises(ValueError, e.__lt__, m.c)
            self.assertRaises(ValueError, e.__gt__, m.c)
            self.assertRaises(TypeError, e.__lt__, m.a < m.b)
            self.assertRaises(TypeError, m.a.__lt__, e1)
            self.assertRaises(TypeError, m.a.__gt__, e1)

        try:
            m.x < m.a
            self.fail("expected use of indexed variable to raise TypeError")
        except TypeError:
            pass

        try:
            m.a < m.x
            self.fail("expected use of indexed variable to raise TypeError")
        except TypeError:
            pass

        try:
            e < m.c
            self.fail("expected 4-term inequality to raise ValueError")
        except ValueError:
            pass

        try:
            m.c < e
            self.fail("expected 4-term inequality to raise ValueError")
        except ValueError:
            pass

        try:
            e1 = m.a < m.b
            e < e1
            self.fail("expected inequality of inequalities to raise TypeError")
        except TypeError:
            pass

        try:
            m.a < (m.a == m.b)
            self.fail("expected equality within inequality to raise TypeError")
        except TypeError:
            pass

        try:
            m.a > (m.a == m.b)
            self.fail("expected equality within inequality to raise TypeError")
        except TypeError:
            pass


class PrettyPrinter(pyutilib.th.TestCase):
    def test_sum(self):
        model = ConcreteModel()
        model.a = Var()

        expr = 5 + model.a + model.a
        buf = StringIO.StringIO()
        expr.pprint(ostream=buf)
        self.assertEqual("sum( 5.0 , a , a ) \n", buf.getvalue())

        expr += 5
        buf = StringIO.StringIO()
        expr.pprint(ostream=buf)
        self.assertEqual("sum( 10.0 , a , a ) \n", buf.getvalue())

    def test_prod(self):
        model = ConcreteModel()
        model.a = Var()

        expr = 5 * model.a * model.a
        buf = StringIO.StringIO()
        expr.pprint(ostream=buf)
        self.assertEqual("prod( num=( 5.0 , a , a ) ) \n", buf.getvalue())

        expr = expr*0
        buf = StringIO.StringIO()
        expr.pprint(ostream=buf)
        self.assertEqual("0.0", buf.getvalue())

        expr = 5 * model.a / model.a
        buf = StringIO.StringIO()
        expr.pprint(ostream=buf)
        self.assertEqual( "prod( num=( 5.0 , a ) , denom=( a ) ) \n",
                          buf.getvalue() )

        expr = expr / model.a
        buf = StringIO.StringIO()
        expr.pprint(ostream=buf)
        self.assertEqual( "prod( num=( 5.0 , a ) , denom=( a , a ) ) \n",
                          buf.getvalue() )

    def test_inequality(self):
        model = ConcreteModel()
        model.a = Var()

        expr = 5 < model.a
        buf = StringIO.StringIO()
        expr.pprint(ostream=buf)
        self.assertEqual( "5.0  <  a \n", buf.getvalue() )

        expr = model.a >= 5
        buf = StringIO.StringIO()
        expr.pprint(ostream=buf)
        self.assertEqual( "5.0  <=  a \n", buf.getvalue() )

        expr = expr < 10
        buf = StringIO.StringIO()
        expr.pprint(ostream=buf)
        self.assertEqual( "5.0  <=  a  <  10.0 \n", buf.getvalue() )

        expr = 5 <= model.a + 5
        buf = StringIO.StringIO()
        expr.pprint(ostream=buf)
        self.assertEqual( "5.0  <=  sum( 5.0 , a ) \n", buf.getvalue() )

        expr = expr < 10
        buf = StringIO.StringIO()
        expr.pprint(ostream=buf)
        self.assertEqual( "5.0  <=  sum( 5.0 , a )  <  10.0 \n", buf.getvalue() )

    def test_equality(self):
        model = ConcreteModel()
        model.a = Var()
        model.b = Param(initialize=5)

        expr = model.a == model.b
        buf = StringIO.StringIO()
        expr.pprint(ostream=buf)
        self.assertEqual( "a  ==  b \n", buf.getvalue() )

        expr = model.b == model.a
        buf = StringIO.StringIO()
        expr.pprint(ostream=buf)
        self.assertEqual( "b  ==  a \n", buf.getvalue() )

        # NB: since there is no "reverse equality" operator, explicit
        # constants will always show up second.
        expr = 5 == model.a
        buf = StringIO.StringIO()
        expr.pprint(ostream=buf)
        self.assertEqual( "a  ==  5.0 \n", buf.getvalue() )

        expr = model.a == 10
        buf = StringIO.StringIO()
        expr.pprint(ostream=buf)
        self.assertEqual( "a  ==  10.0 \n", buf.getvalue() )

        expr = 5 == model.a + 5
        buf = StringIO.StringIO()
        expr.pprint(ostream=buf)
        self.assertEqual( "sum( 5.0 , a )  ==  5.0 \n", buf.getvalue() )

        expr = model.a + 5 == 5
        buf = StringIO.StringIO()
        expr.pprint(ostream=buf)
        self.assertEqual( "sum( 5.0 , a )  ==  5.0 \n", buf.getvalue() )

    def test_small_expression(self):
        model = AbstractModel()
        model.a = Var()
        model.b = Param(initialize=2)
        instance=model.create()
        expr = instance.a+1
        expr = expr-1
        expr = expr*instance.a
        expr = expr/instance.a
        expr = expr**instance.b
        expr = 1-expr
        expr = 1+expr
        expr = 2*expr
        expr = 2/expr
        expr = 2**expr
        expr = - expr
        expr = + expr
        expr = abs(expr)
        OUTPUT=open(currdir+"expr.out","w")
        expr.pprint(ostream=OUTPUT)
        OUTPUT.close()
        self.assertFileEqualsBaseline(currdir+"expr.out",currdir+"expr.txt")

    def test_large_expression(self):
        def c1_rule(model):
            return (1.0,model.b[1],None)
        def c2_rule(model):
            return (None,model.b[1],0.0)
        def c3_rule(model):
            return (0.0,model.b[1],1.0)
        def c4_rule(model):
            return (3.0,model.b[1])
        def c5_rule(model, i):
            return (model.b[i],0.0)

        def c6a_rule(model):
            return 0.0 <= model.c
        def c7a_rule(model):
            return model.c <= 1.0
        def c7b_rule(model):
            return model.c < 1.0
        def c8_rule(model):
            return model.c == 2.0
        def c9a_rule(model):
            return model.A+model.A <= model.c
        def c9b_rule(model):
            return model.A+model.A < model.c
        def c10a_rule(model):
            return model.c <= model.B+model.B
        def c11_rule(model):
            return model.c == model.A+model.B
        def c15a_rule(model):
            return model.A <= model.A*model.d
        def c16a_rule(model):
            return model.A*model.d <= model.B

        def c12_rule(model):
            return model.c == model.d
        def c13a_rule(model):
            return model.c <= model.d
        def c14a_rule(model):
            return model.c >= model.d

        def cl_rule(model, i):
            if i > 10:
                return ConstraintList.End
            return i* model.c > model.d

        def o2_rule(model, i):
            return model.b[i]
        model=AbstractModel()
        model.a = Set(initialize=[1,2,3])
        model.b = Var(model.a,initialize=1.1,within=PositiveReals)
        model.c = Var(initialize=2.1, within=PositiveReals)
        model.d = Var(initialize=3.1, within=PositiveReals)
        model.e = Var(initialize=4.1, within=PositiveReals)
        model.A = Param(default=-1)
        model.B = Param(default=-2)
        #model.o1 = Objective()
        model.o2 = Objective(model.a,rule=o2_rule)
        model.o3 = Objective(model.a,model.a)
        model.c1 = Constraint(rule=c1_rule)
        model.c2 = Constraint(rule=c2_rule)
        model.c3 = Constraint(rule=c3_rule)
        model.c4 = Constraint(rule=c4_rule)
        model.c5 = Constraint(model.a,rule=c5_rule)

        model.c6a = Constraint(rule=c6a_rule)
        model.c7a = Constraint(rule=c7a_rule)
        model.c7b = Constraint(rule=c7b_rule)
        model.c8 = Constraint(rule=c8_rule)
        model.c9a = Constraint(rule=c9a_rule)
        model.c9b = Constraint(rule=c9b_rule)
        model.c10a = Constraint(rule=c10a_rule)
        model.c11 = Constraint(rule=c11_rule)
        model.c15a = Constraint(rule=c15a_rule)
        model.c16a = Constraint(rule=c16a_rule)

        model.c12 = Constraint(rule=c12_rule)
        model.c13a = Constraint(rule=c13a_rule)
        model.c14a = Constraint(rule=c14a_rule)

        model.cl = ConstraintList(rule=cl_rule)

        instance=model.create()
        OUTPUT=open(currdir+"varpprint.out","w")
        instance.pprint(ostream=OUTPUT)
        OUTPUT.close()
        self.assertFileEqualsBaseline( currdir+"varpprint.out",
                                       currdir+"varpprint.txt" )


class InplaceExpressionGeneration(pyutilib.th.TestCase):
    def setUp(self):
        m = AbstractModel()
        m.a = Var()
        m.b = Var()
        self.m = m

    def test_iadd(self):
        m = self.m
        x = 0

        count = generate_expression.clone_counter
        x += m.a
        self.assertIs(type(x), _VarElement)
        self.assertEqual(generate_expression.clone_counter, count)

        count = generate_expression.clone_counter
        x += m.a
        self.assertIs(type(x), _SumExpression)
        self.assertEqual(len(x._args), 2)
        self.assertEqual(generate_expression.clone_counter, count)

        count = generate_expression.clone_counter
        x += m.a
        self.assertIs(type(x), _SumExpression)
        self.assertEqual(len(x._args), 3)
        self.assertEqual(generate_expression.clone_counter, count)

        # If someone else holds a reference to the expression, we still
        # need to clone it:
        count = generate_expression.clone_counter
        y = x
        x += m.a
        self.assertIs(type(x), _SumExpression)
        self.assertEqual(len(x._args), 4)
        self.assertEqual(len(y._args), 3)
        self.assertEqual(generate_expression.clone_counter, count+1)


    def test_isub(self):
        m = self.m
        x = 0

        count = generate_expression.clone_counter
        x -= m.a
        self.assertIs(type(x), _SumExpression)
        self.assertEqual(len(x._args), 1)
        self.assertEqual(generate_expression.clone_counter, count)

        count = generate_expression.clone_counter
        x -= m.a
        self.assertIs(type(x), _SumExpression)
        self.assertEqual(len(x._args), 2)
        self.assertEqual(generate_expression.clone_counter, count)

        count = generate_expression.clone_counter
        x -= m.a
        self.assertIs(type(x), _SumExpression)
        self.assertEqual(len(x._args), 3)
        self.assertEqual(generate_expression.clone_counter, count)

        # If someone else holds a reference to the expression, we still
        # need to clone it:
        count = generate_expression.clone_counter
        y = x
        x -= m.a
        self.assertIs(type(x), _SumExpression)
        self.assertEqual(len(x._args), 4)
        self.assertEqual(len(y._args), 3)
        self.assertEqual(generate_expression.clone_counter, count+1)

    def test_imul(self):
        m = self.m
        x = 1

        count = generate_expression.clone_counter
        x *= m.a
        self.assertIs(type(x), _VarElement)
        self.assertEqual(generate_expression.clone_counter, count)

        count = generate_expression.clone_counter
        x *= m.a
        self.assertIs(type(x), _ProductExpression)
        self.assertEqual(len(x._numerator), 2)
        self.assertEqual(len(x._denominator), 0)
        self.assertEqual(generate_expression.clone_counter, count)

        count = generate_expression.clone_counter
        x *= m.a
        self.assertIs(type(x), _ProductExpression)
        self.assertEqual(len(x._numerator), 3)
        self.assertEqual(len(x._denominator), 0)
        self.assertEqual(generate_expression.clone_counter, count)

        # If someone else holds a reference to the expression, we still
        # need to clone it:
        count = generate_expression.clone_counter
        y = x
        x *= m.a
        self.assertIs(type(x), _ProductExpression)
        self.assertEqual(len(x._numerator), 4)
        self.assertEqual(len(y._numerator), 3)
        self.assertEqual(generate_expression.clone_counter, count+1)

    def test_idiv(self):
        m = self.m
        x = 1

        count = generate_expression.clone_counter
        x /= m.a
        self.assertIs(type(x), _ProductExpression)
        self.assertEqual(len(x._numerator), 0)
        self.assertEqual(len(x._denominator), 1)
        self.assertEqual(generate_expression.clone_counter, count)

        count = generate_expression.clone_counter
        x /= m.a
        self.assertIs(type(x), _ProductExpression)
        self.assertEqual(len(x._numerator), 0)
        self.assertEqual(len(x._denominator), 2)
        self.assertEqual(generate_expression.clone_counter, count)

        count = generate_expression.clone_counter
        x /= m.a
        self.assertIs(type(x), _ProductExpression)
        self.assertEqual(len(x._numerator), 0)
        self.assertEqual(len(x._denominator), 3)
        self.assertEqual(generate_expression.clone_counter, count)

        # If someone else holds a reference to the expression, we still
        # need to clone it:
        count = generate_expression.clone_counter
        y = x
        x /= m.a
        self.assertIs(type(x), _ProductExpression)
        self.assertEqual(len(x._denominator), 4)
        self.assertEqual(len(y._denominator), 3)
        self.assertEqual(generate_expression.clone_counter, count+1)

    def test_ipow(self):
        m = self.m
        x = 1

        count = generate_expression.clone_counter
        x **= m.a
        self.assertIs(type(x), _PowExpression)
        self.assertEqual(len(x._args), 2)
        self.assertEqual(x._args[0](), 1)
        self.assertIs(x._args[1], m.a)
        self.assertEqual(generate_expression.clone_counter, count)

        count = generate_expression.clone_counter
        x **= m.b
        self.assertIs(type(x), _PowExpression)
        self.assertEqual(len(x._args), 2)
        self.assertIs(type(x._args[0]), _PowExpression)
        self.assertIs(x._args[1], m.b)
        self.assertEqual(len(x._args), 2)
        self.assertEqual(x._args[0]._args[0](), 1)
        self.assertIs(x._args[0]._args[1], m.a)
        self.assertEqual(generate_expression.clone_counter, count)

        # If someone else holds a reference to the expression, we still
        # need to clone it:
        count = generate_expression.clone_counter
        x = 1 ** m.a
        y = x
        x **= m.b
        self.assertIs(type(y), _PowExpression)
        self.assertEqual(len(y._args), 2)
        self.assertEqual(y._args[0](), 1)
        self.assertIs(y._args[1], m.a)

        self.assertIs(type(x), _PowExpression)
        self.assertEqual(len(x._args), 2)
        self.assertIs(type(x._args[0]), _PowExpression)
        self.assertIs(x._args[1], m.b)
        self.assertEqual(len(x._args), 2)
        self.assertEqual(x._args[0]._args[0](), 1)
        self.assertIs(x._args[0]._args[1], m.a)
        self.assertEqual(generate_expression.clone_counter, count+1)


class GeneralExpressionGeneration(pyutilib.th.TestCase):

    def test_invalidIndexing(self):
        m = AbstractModel()
        m.A = Set()
        m.p = Param(m.A)
        m.x = Var(m.A)
        m.z = Var()

        try:
            m.p * 2
            self.fail("Expected m.p*2 to raise a TypeError")
        except TypeError:
            pass

        try:
            m.x * 2
            self.fail("Expected m.x*2 to raise a TypeError")
        except TypeError:
            pass

        try:
            2 * m.p
            self.fail("Expected 2*m.p to raise a TypeError")
        except TypeError:
            pass

        try:
            2 * m.x
            self.fail("Expected 2*m.x to raise a TypeError")
        except TypeError:
            pass

        try:
            m.z * m.p
            self.fail("Expected m.z*m.p to raise a TypeError")
        except TypeError:
            pass

        try:
            m.z * m.x
            self.fail("Expected m.z*m.x to raise a TypeError")
        except TypeError:
            pass

    def test_negation(self):
        m = AbstractModel()
        m.a = Var()
        m.b = Var()

        e = -m.a
        self.assertIs(type(e), _ProductExpression)
        self.assertEqual(e.coef, -1)
        self.assertEqual(len(e._numerator), 1)
        self.assertEqual(len(e._denominator), 0)
        self.assertIs(e._numerator[0], m.a)

        e1 = m.a - m.b
        e = -e1
        self.assertIs(type(e), _SumExpression)
        self.assertEqual(e._const, 0)
        self.assertEqual(len(e._args), 2)
        self.assertIs(e._args[0], m.a)
        self.assertIs(e._args[1], m.b)
        self.assertEqual(len(e._coef), 2)
        self.assertEqual(e._coef[0], -1)
        self.assertEqual(e._coef[1], 1)

        e1 = m.a * m.b
        e = -e1
        self.assertIs(type(e), _ProductExpression)
        self.assertEqual(e.coef, -1)
        self.assertEqual(len(e._numerator), 2)
        self.assertEqual(len(e._denominator), 0)
        self.assertIs(e._numerator[0], m.a)
        self.assertIs(e._numerator[1], m.b)

        e1 = sin(m.a)
        e = -e1
        self.assertIs(type(e), _ProductExpression)
        self.assertEqual(e.coef, -1)
        self.assertEqual(len(e._numerator), 1)
        self.assertEqual(len(e._denominator), 0)
        self.assertIs(type(e._numerator[0]), _IntrinsicFunctionExpression)

    def test_genericExpression_notImplemented(self):
        m = AbstractModel()
        m.a = Var()
        m.b = Var()
        e = Expression("dummy", 2, [m.a, m.b])
        self.assertRaises(NotImplementedError, e.clone)
        self.assertRaises(NotImplementedError, e)




class ExprConditionalContext(unittest.TestCase):
    def checkCondition(self, expr, expectedValue):
        try:
            if expr:
                if expectedValue != True:
                    self.fail("__nonzero__ returned the wrong condition value")
            else:
                if expectedValue != False:
                    self.fail("__nonzero__ returned the wrong condition value")
            if expectedValue is None:
                self.fail("Expected ValueError because component was undefined")
        except ValueError:
            if expectedValue is not None:
                raise
        generate_relational_expression.chainedInequality = None

    def tearDown(self):
        # Make sure errors here don't bleed over to other tests
        generate_relational_expression.chainedInequality = None

    def test_paramConditional(self):
        model = AbstractModel()
        model.p = Param(initialize=1.0)
        self.checkCondition(model.p > 0, None)
        self.checkCondition(model.p >= 0, None)
        self.checkCondition(model.p < 1, None)
        self.checkCondition(model.p <= 1, None)
        self.checkCondition(model.p == 0, None)

        instance = model.create()
        self.checkCondition(instance.p > 0, True)
        self.checkCondition(instance.p > 2, False)
        self.checkCondition(instance.p >= 1, True)
        self.checkCondition(instance.p >= 2, False)
        self.checkCondition(instance.p < 2, True)
        self.checkCondition(instance.p < 0, False)
        self.checkCondition(instance.p <= 1, True)
        self.checkCondition(instance.p <= 0, False)
        self.checkCondition(instance.p == 1, True)
        self.checkCondition(instance.p == 2, False)

    def test_paramConditional_reversed(self):
        model = AbstractModel()
        model.p = Param(initialize=1.0)
        self.checkCondition(0 < model.p, None)
        self.checkCondition(0 <= model.p, None)
        self.checkCondition(1 > model.p, None)
        self.checkCondition(1 >= model.p, None)
        self.checkCondition(0 == model.p, None)

        instance = model.create()
        self.checkCondition(0 < instance.p, True)
        self.checkCondition(2 < instance.p, False)
        self.checkCondition(1 <= instance.p, True)
        self.checkCondition(2 <= instance.p, False)
        self.checkCondition(2 > instance.p, True)
        self.checkCondition(0 > instance.p, False)
        self.checkCondition(1 >= instance.p, True)
        self.checkCondition(0 >= instance.p, False)
        self.checkCondition(1 == instance.p, True)
        self.checkCondition(2 == instance.p, False)

    def test_varConditional(self):
        model = AbstractModel()
        model.v = Var(initialize=1.0)
        self.checkCondition(model.v > 0, True)
        self.checkCondition(model.v >= 0, True)
        self.checkCondition(model.v < 1, True)
        self.checkCondition(model.v <= 1, True)
        self.checkCondition(model.v == 0, None)

        instance = model.create()
        self.checkCondition(instance.v > 0, True)
        self.checkCondition(instance.v > 2, True)
        self.checkCondition(instance.v >= 1, True)
        self.checkCondition(instance.v >= 2, True)
        self.checkCondition(instance.v < 2, True)
        self.checkCondition(instance.v < 0, True)
        self.checkCondition(instance.v <= 1, True)
        self.checkCondition(instance.v <= 0, True)
        self.checkCondition(instance.v == 1, True)
        self.checkCondition(instance.v == 2, False)

    def test_varConditional_reversed(self):
        model = AbstractModel()
        model.v = Var(initialize=1.0)
        self.checkCondition(0 < model.v, True)
        self.checkCondition(0 <= model.v, True)
        self.checkCondition(1 > model.v, True)
        self.checkCondition(1 >= model.v, True)
        self.checkCondition(0 == model.v, None)

        instance = model.create()
        self.checkCondition(0 < instance.v, True)
        self.checkCondition(2 < instance.v, True)
        self.checkCondition(1 <= instance.v, True)
        self.checkCondition(2 <= instance.v, True)
        self.checkCondition(2 > instance.v, True)
        self.checkCondition(0 > instance.v, True)
        self.checkCondition(1 >= instance.v, True)
        self.checkCondition(0 >= instance.v, True)
        self.checkCondition(1 == instance.v, True)
        self.checkCondition(2 == instance.v, False)

    def test_eval_sub_varConditional(self):
        model = AbstractModel()
        model.v = Var(initialize=1.0)
        try:
            self.checkCondition(value(model.v) > 0, None)
            self.fail("Expected ValueError because component was undefined")
        except ValueError:
            pass
        try:
            self.checkCondition(value(model.v) >= 0, None)
            self.fail("Expected ValueError because component was undefined")
        except ValueError:
            pass
        try:
            self.checkCondition(value(model.v) < 1, None)
            self.fail("Expected ValueError because component was undefined")
        except ValueError:
            pass
        try:
            self.checkCondition(value(model.v) <= 1, None)
            self.fail("Expected ValueError because component was undefined")
        except ValueError:
            pass
        try:
            self.checkCondition(value(model.v) == 0, None)
            self.fail("Expected ValueError because component was undefined")
        except ValueError:
            pass

        instance = model.create()
        self.checkCondition(value(instance.v) > 0, True)
        self.checkCondition(value(instance.v) > 2, False)
        self.checkCondition(value(instance.v) >= 1, True)
        self.checkCondition(value(instance.v) >= 2, False)
        self.checkCondition(value(instance.v) < 2, True)
        self.checkCondition(value(instance.v) < 0, False)
        self.checkCondition(value(instance.v) <= 1, True)
        self.checkCondition(value(instance.v) <= 0, False)
        self.checkCondition(value(instance.v) == 1, True)
        self.checkCondition(value(instance.v) == 2, False)

    def test_eval_sub_varConditional_reversed(self):
        model = AbstractModel()
        model.v = Var(initialize=1.0)
        try:
            self.checkCondition(0 < value(model.v), None)
            self.fail("Expected ValueError because component was undefined")
        except ValueError:
            pass
        try:
            self.checkCondition(0 <= value(model.v), None)
            self.fail("Expected ValueError because component was undefined")
        except ValueError:
            pass
        try:
            self.checkCondition(1 > value(model.v), None)
            self.fail("Expected ValueError because component was undefined")
        except ValueError:
            pass
        try:
            self.checkCondition(1 >= value(model.v), None)
            self.fail("Expected ValueError because component was undefined")
        except ValueError:
            pass
        try:
            self.checkCondition(0 == value(model.v), None)
            self.fail("Expected ValueError because component was undefined")
        except ValueError:
            pass

        instance = model.create()
        self.checkCondition(0 < value(instance.v), True)
        self.checkCondition(2 < value(instance.v), False)
        self.checkCondition(1 <= value(instance.v), True)
        self.checkCondition(2 <= value(instance.v), False)
        self.checkCondition(2 > value(instance.v), True)
        self.checkCondition(0 > value(instance.v), False)
        self.checkCondition(1 >= value(instance.v), True)
        self.checkCondition(0 >= value(instance.v), False)
        self.checkCondition(1 == value(instance.v), True)
        self.checkCondition(2 == value(instance.v), False)

    def test_eval_varConditional(self):
        model = AbstractModel()
        model.v = Var(initialize=1.0)
        try:
            self.checkCondition(value(model.v > 0), None)
            self.fail("Expected ValueError because component was undefined")
        except ValueError:
            pass
        try:
            self.checkCondition(value(model.v >= 0), None)
            self.fail("Expected ValueError because component was undefined")
        except ValueError:
            pass
        try:
            self.checkCondition(value(model.v == 0), None)
            self.fail("Expected ValueError because component was undefined")
        except ValueError:
            pass

        instance = model.create()
        self.checkCondition(value(instance.v > 0), True)
        self.checkCondition(value(instance.v > 2), False)
        self.checkCondition(value(instance.v >= 1), True)
        self.checkCondition(value(instance.v >= 2), False)
        self.checkCondition(value(instance.v == 1), True)
        self.checkCondition(value(instance.v == 2), False)

    def test_eval_varConditional_reversed(self):
        model = AbstractModel()
        model.v = Var(initialize=1.0)
        try:
            self.checkCondition(value(0 < model.v), None)
            self.fail("Expected ValueError because component was undefined")
        except ValueError:
            pass
        try:
            self.checkCondition(value(0 <= model.v), None)
            self.fail("Expected ValueError because component was undefined")
        except ValueError:
            pass
        try:
            self.checkCondition(value(0 == model.v), None)
            self.fail("Expected ValueError because component was undefined")
        except ValueError:
            pass

        instance = model.create()
        self.checkCondition(value(0 < instance.v), True)
        self.checkCondition(value(2 < instance.v), False)
        self.checkCondition(value(1 <= instance.v), True)
        self.checkCondition(value(2 <= instance.v), False)
        self.checkCondition(value(1 == instance.v), True)
        self.checkCondition(value(2 == instance.v), False)


class PolynomialDegree(pyutilib.th.TestCase):

    def setUp(self):
        def d_fn(model):
            return model.c+model.c
        self.model=AbstractModel()
        self.model.a = Var(initialize=1.0)
        self.model.b = Var(initialize=2.0)
        self.model.c = Param(initialize=0)
        self.model.d = Param(initialize=d_fn)
        self.instance= self.model.create()

    def test_param(self):
        self.assertEqual(self.model.d.polynomial_degree(), 0)

    def test_var(self):
        save = self.model.a.fixed
        self.model.a.fixed = False
        self.assertEqual(self.model.a.polynomial_degree(), 1)
        self.model.a.fixed = True
        self.assertEqual(self.model.a.polynomial_degree(), 0)
        self.model.a.fixed = save

    def test_simple_sum(self):
        expr = self.model.c + self.model.d
        self.assertEqual(expr.polynomial_degree(), 0)

        expr = self.model.a + self.model.b
        self.assertEqual(expr.polynomial_degree(), 1)
        self.model.a.fixed = True
        self.assertEqual(expr.polynomial_degree(), 1)
        self.model.a.fixed = False

        expr = self.model.a + self.model.c
        self.assertEqual(expr.polynomial_degree(), 1)
        self.model.a.fixed = True
        self.assertEqual(expr.polynomial_degree(), 0)
        self.model.a.fixed = False

    def test_relational_ops(self):
        expr = self.model.c < self.model.d
        self.assertEqual(expr.polynomial_degree(), 0)

        expr = self.model.a <= self.model.d
        self.assertEqual(expr.polynomial_degree(), 1)

        expr = self.model.a * self.model.a >= self.model.b
        self.assertEqual(expr.polynomial_degree(), 2)
        self.model.a.fixed = True
        self.assertEqual(expr.polynomial_degree(), 1)
        self.model.a.fixed = False

        expr = self.model.a > self.model.a * self.model.b
        self.assertEqual(expr.polynomial_degree(), 2)
        self.model.b.fixed = True
        self.assertEqual(expr.polynomial_degree(), 1)
        self.model.b.fixed = False

    def test_simple_product(self):
        expr = self.model.c * self.model.d
        self.assertEqual(expr.polynomial_degree(), 0)

        expr = self.model.a * self.model.b
        self.assertEqual(expr.polynomial_degree(), 2)

        expr = self.model.a * self.model.c
        self.assertEqual(expr.polynomial_degree(), 1)
        self.model.a.fixed = True
        self.assertEqual(expr.polynomial_degree(), 0)
        self.model.a.fixed = False

        expr = self.model.a / self.model.c
        self.assertEqual(expr.polynomial_degree(), 1)

        expr = self.model.c / self.model.a
        self.assertEqual(expr.polynomial_degree(), None)
        self.model.a.fixed = True
        self.assertEqual(expr.polynomial_degree(), 0)
        self.model.a.fixed = False

    def test_nested_expr(self):
        expr1 = self.model.c * self.model.d
        expr2 = expr1 + expr1
        self.assertEqual(expr2.polynomial_degree(), 0)

        expr1 = self.model.a * self.model.b
        expr2 = expr1 + expr1
        self.assertEqual(expr2.polynomial_degree(), 2)
        self.model.a.fixed = True
        self.assertEqual(expr2.polynomial_degree(), 1)
        self.model.a.fixed = False

        expr1 = self.model.c + self.model.d
        expr2 = expr1 * expr1
        self.assertEqual(expr2.polynomial_degree(), 0)

        expr1 = self.model.a + self.model.b
        expr2 = expr1 * expr1
        self.assertEqual(expr2.polynomial_degree(), 2)
        self.model.a.fixed = True
        self.assertEqual(expr2.polynomial_degree(), 2)
        self.model.b.fixed = True
        self.assertEqual(expr2.polynomial_degree(), 0)
        self.model.b.fixed = False
        self.model.a.fixed = False

    def test_misc_operators(self):
        expr = -(self.model.a * self.model.b)
        self.assertEqual(expr.polynomial_degree(), 2)

    def test_nonpolynomial(self):
        expr1 = abs(self.model.a * self.model.b)
        self.assertEqual(expr1.polynomial_degree(), None)

        expr2 = self.model.a + self.model.b * abs(self.model.b)
        self.assertEqual(expr2.polynomial_degree(), None)

        expr3 = self.model.a * ( self.model.b + abs(self.model.b) )
        self.assertEqual(expr3.polynomial_degree(), None)

        # NB: Currently we do not check for special polynomial cases of
        # the pow() function (arg[0] is polynomial and arg[1] is a
        # non-negative integer)
        expr = pow(self.model.a, 2)
        self.assertEqual(expr.polynomial_degree(), None)

        # fixing variables should turn intrinsic functions into constants
        self.model.a.fixed = True
        self.assertEqual(expr1.polynomial_degree(), None)
        self.assertEqual(expr2.polynomial_degree(), None)
        self.assertEqual(expr3.polynomial_degree(), None)

        self.model.b.fixed = True
        self.assertEqual(expr1.polynomial_degree(), 0)
        self.assertEqual(expr2.polynomial_degree(), 0)
        self.assertEqual(expr3.polynomial_degree(), 0)

        self.model.a.fixed = False
        self.assertEqual(expr1.polynomial_degree(), None)
        self.assertEqual(expr2.polynomial_degree(), 1)
        self.assertEqual(expr3.polynomial_degree(), 1)




class CloneIfNeeded(pyutilib.th.TestCase):

    def setUp(self):
        def d_fn(model):
            return model.c+model.c
        model=ConcreteModel()
        model.I = Set(initialize=range(4))
        model.J = Set(initialize=range(1))
        model.a = Var()
        model.b = Var(model.I)
        model.c = Param(initialize=1)
        model.d = Param(initialize=d_fn)
        self.model = model
        self.refCount = []

    def tearDown(self):
        generate_expression.clone_if_needed_callback = None
        generate_intrinsic_function_expression.clone_if_needed_callback = None
        generate_relational_expression.clone_if_needed_callback = None

    def trapCloneIfNeeded(self, count):
        self.refCount.append(count)

    def test_operator_UNREFERENCED_EXPR_COUNT(self):
        generate_expression.clone_if_needed_callback = \
            lambda x: self.trapCloneIfNeeded(x)

        expr1 = abs(self.model.a+self.model.a)
        self.assertEqual( self.refCount, [0] )

        expr2 = expr1 + self.model.a
        self.assertEqual( self.refCount, [0,1] )

    def test_intrinsic_UNREFERENCED_EXPR_COUNT(self):
        generate_intrinsic_function_expression.clone_if_needed_callback = \
            lambda x: self.trapCloneIfNeeded(x)

        val1 = cos(0)
        self.assertTrue( type(val1) is float )
        self.assertEqual( val1, 1 )
        self.assertEqual( self.refCount, [] )

        expr1 = cos(self.model.a+self.model.a)
        self.assertEqual( self.refCount, [0] )

        expr2 = sin(expr1)
        self.assertEqual( self.refCount, [0,1] )

    def test_relational_UNREFERENCED_EXPR_COUNT(self):
        generate_relational_expression.clone_if_needed_callback = \
            lambda x: self.trapCloneIfNeeded(x)

        expr1 = self.model.c < self.model.a + self.model.b[1]
        self.assertEqual( self.refCount, [0] )

        expr2 = expr1 < 5
        self.assertEqual( self.refCount, [0,1] )


    def test_cloneCount_simple(self):
        # simple expression
        count = generate_expression.clone_counter
        expr = self.model.a * self.model.a
        self.assertEqual(generate_expression.clone_counter, count)

        # expression based on another expression
        count = generate_expression.clone_counter
        expr = expr + self.model.a
        self.assertEqual(generate_expression.clone_counter, count + 1)

    def test_cloneCount_sumVars(self):
        # sum over variable using generators
        count = generate_expression.clone_counter
        expr = sum(self.model.b[i] for i in self.model.I)
        self.assertEqual(generate_expression.clone_counter, count)

        # sum over variable using list comprehension
        count = generate_expression.clone_counter
        expr = sum([self.model.b[i] for i in self.model.I])
        self.assertEqual(generate_expression.clone_counter, count)

    def test_cloneCount_sumExpr_singleTerm(self):
        # sum over expression using generators (single element)
        count = generate_expression.clone_counter
        expr = sum(self.model.b[i]*self.model.b[i] for i in self.model.J)
        self.assertEqual(generate_expression.clone_counter, count)

        # sum over expression using list comprehension (single element)
        count = generate_expression.clone_counter
        expr = sum([self.model.b[i]*self.model.b[i] for i in self.model.J])
        self.assertEqual(generate_expression.clone_counter, count+1)

        # sum over expression using list (single element)
        count = generate_expression.clone_counter
        l = [self.model.b[i]*self.model.b[i] for i in self.model.J]
        expr = sum(l)
        self.assertEqual(generate_expression.clone_counter, count+1)

    def test_cloneCount_sumExpr_multiTerm(self):
        # sum over expression using generators
        count = generate_expression.clone_counter
        expr = sum(self.model.b[i]*self.model.b[i] for i in self.model.I)
        self.assertEqual(generate_expression.clone_counter, count)

        # sum over expression using list comprehension
        count = generate_expression.clone_counter
        expr = sum([self.model.b[i]*self.model.b[i] for i in self.model.I])
        self.assertEqual(generate_expression.clone_counter, count+4)

        # sum over expression using list
        count = generate_expression.clone_counter
        l = [self.model.b[i]*self.model.b[i] for i in self.model.I]
        expr = sum(l)
        self.assertEqual(generate_expression.clone_counter, count+4)

        # generate a new expression from a complex one
        count = generate_expression.clone_counter
        expr1 = expr + 1
        self.assertEqual(generate_expression.clone_counter, count+1)

    def test_cloneCount_sumExpr_complexExpr(self):
        # sum over complex expression using generators
        count = generate_expression.clone_counter
        expr = sum( value(self.model.c)*(1+self.model.b[i])**2
                    for i in self.model.I )
        self.assertEqual(generate_expression.clone_counter, count)

        # sum over complex expression using list comprehension
        count = generate_expression.clone_counter
        expr = sum([ value(self.model.c)*(1+self.model.b[i])**2
                     for i in self.model.I ])
        self.assertEqual(generate_expression.clone_counter, count+4)

        # sum over complex expression using list
        count = generate_expression.clone_counter
        l = [ value(self.model.c)*(1+self.model.b[i])**2
              for i in self.model.I ]
        expr = sum(l)
        self.assertEqual(generate_expression.clone_counter, count+4)


    def test_cloneCount_intrinsicFunction(self):
        # intrinsicFunction of a simple expression
        count = generate_intrinsic_function_expression.clone_counter
        expr = log(self.model.c + self.model.a)
        self.assertEqual( generate_intrinsic_function_expression.clone_counter,
                          count )

        # intrinsicFunction of a referenced expression
        count = generate_intrinsic_function_expression.clone_counter
        expr = self.model.c + self.model.a
        expr1 = log(expr)
        self.assertEqual( generate_intrinsic_function_expression.clone_counter,
                          count+1 )


    def test_cloneCount_relationalExpression_simple(self):
        # relational expression of simple vars
        count = generate_relational_expression.clone_counter
        expr = self.model.c < self.model.a
        self.assertEqual(len(expr._args), 2)
        self.assertEqual( generate_relational_expression.clone_counter,
                          count )

        # relational expression of simple expressions
        count = generate_relational_expression.clone_counter
        expr = 2*self.model.c < 2*self.model.a
        self.assertEqual(len(expr._args), 2)
        self.assertEqual( generate_relational_expression.clone_counter,
                          count )

        # relational expression of a referenced expression
        count = generate_relational_expression.clone_counter
        expr = self.model.c + self.model.a
        expr1 = expr < self.model.d
        self.assertEqual(len(expr._args), 2)
        self.assertEqual( generate_relational_expression.clone_counter,
                          count + 1 )

    def test_cloneCount_relationalExpression_compound(self):
        # relational expression of a compound expression (simple vars)
        count = generate_relational_expression.clone_counter
        expr = self.model.c < self.model.a < self.model.d
        expr.pprint()
        self.assertEqual(len(expr._args), 3)
        self.assertEqual( generate_relational_expression.clone_counter,
                          count )

        # relational expression of a compound expression
        # (non-expression common term)
        count = generate_relational_expression.clone_counter
        expr = 2*self.model.c < self.model.a < 2*self.model.d
        expr.pprint()
        self.assertEqual(len(expr._args), 3)
        self.assertEqual( generate_relational_expression.clone_counter,
                          count )

        # relational expression of a compound expression
        # (expression common term)
        count = generate_relational_expression.clone_counter
        expr = self.model.c < 2 * self.model.a < self.model.d
        expr.pprint()
        self.assertEqual(len(expr._args), 3)
        self.assertEqual( generate_relational_expression.clone_counter,
                          count + 1 )

        # relational expression of a referenced compound expression (1)
        count = generate_relational_expression.clone_counter
        expr = self.model.c < self.model.a
        expr1 = expr < self.model.d
        expr1.pprint()
        self.assertEqual(len(expr1._args), 3)
        self.assertEqual( generate_relational_expression.clone_counter,
                          count + 1)

        # relational expression of a referenced compound expression (2)
        count = generate_relational_expression.clone_counter
        expr = 2*self.model.c < 2*self.model.a
        expr1 = self.model.d < expr
        expr1.pprint()
        self.assertEqual(len(expr1._args), 3)
        self.assertEqual( generate_relational_expression.clone_counter,
                          count + 1)

    def test_cloneCount_relationalExpression_compound_reversed(self):
        # relational expression of a compound expression (simple vars)
        count = generate_relational_expression.clone_counter
        expr = self.model.c < self.model.a > self.model.d
        expr.pprint()
        self.assertEqual(len(expr._args), 3)
        self.assertEqual( generate_relational_expression.clone_counter,
                          count )

        # relational expression of a compound expression
        # (non-expression common term)
        count = generate_relational_expression.clone_counter
        expr = 2*self.model.c < self.model.a > 2*self.model.d
        expr.pprint()
        self.assertEqual(len(expr._args), 3)
        self.assertEqual( generate_relational_expression.clone_counter,
                          count )

        # relational expression of a compound expression
        # (expression common term)
        count = generate_relational_expression.clone_counter
        expr = self.model.c < 2 * self.model.a > self.model.d
        expr.pprint()
        self.assertEqual(len(expr._args), 3)
        self.assertEqual( generate_relational_expression.clone_counter,
                          count + 1 )

        # relational expression of a referenced compound expression (1)
        count = generate_relational_expression.clone_counter
        expr = self.model.c < self.model.a
        expr1 = expr > self.model.d
        expr1.pprint()
        self.assertEqual(len(expr1._args), 3)
        self.assertEqual( generate_relational_expression.clone_counter,
                          count + 1)

        # relational expression of a referenced compound expression (2)
        count = generate_relational_expression.clone_counter
        expr = 2*self.model.c < 2*self.model.a
        expr1 = self.model.d > expr
        expr1.pprint()
        self.assertEqual(len(expr1._args), 3)
        self.assertEqual( generate_relational_expression.clone_counter,
                          count + 1)

class CloneExpression(pyutilib.th.TestCase):
    def setUp(self):
        self.m = ConcreteModel()
        self.m.a = Var(initialize=5)
        self.m.b = Var(initialize=10)
        self.m.expr = self.m.a + self.m.b

    def test_IdentityExpression(self):
        expr1 = _IdentityExpression(self.m.a)
        expr2 = expr1.clone()
        self.assertEqual( expr1(), 5 )
        self.assertEqual( expr2(), 5 )
        self.assertNotEqual( id(expr1._args), id(expr2._args) )
        self.assertEqual( id(expr1._args[0]), id(expr2._args[0]) )
        expr1._args = (self.m.b, )
        self.assertEqual( expr1(), 10 )
        self.assertEqual( expr2(), 5 )
        self.assertNotEqual( id(expr1._args), id(expr2._args) )
        self.assertNotEqual( id(expr1._args[0]), id(expr2._args[0]) )

        expr1 = _IdentityExpression(self.m.a + self.m.b)
        expr2 = expr1.clone()
        self.assertEqual( expr1(), 15 )
        self.assertEqual( expr2(), 15 )
        self.assertNotEqual( id(expr1._args), id(expr2._args) )
        self.assertNotEqual( id(expr1._args[0]), id(expr2._args[0]) )
        self.assertEqual( id(expr1._args[0]._args[0]),
                          id(expr2._args[0]._args[0]) )
        self.assertEqual( id(expr1._args[0]._args[1]),
                          id(expr2._args[0]._args[1]) )
        expr1._args = (expr1._args[0] + self.m.b,)
        self.assertEqual( expr1(), 25 )
        self.assertEqual( expr2(), 15 )
        self.assertNotEqual( id(expr1._args), id(expr2._args) )
        self.assertNotEqual( id(expr1._args[0]), id(expr2._args[0]) )

    def test_SumExpression(self):
        expr1 = self.m.a + self.m.b
        expr2 = expr1.clone()
        self.assertEqual( expr1(), 15 )
        self.assertEqual( expr2(), 15 )
        self.assertNotEqual( id(expr1._args), id(expr2._args) )
        self.assertEqual( id(expr1._args[0]), id(expr2._args[0]) )
        self.assertEqual( id(expr1._args[1]), id(expr2._args[1]) )
        expr1._args[0] = self.m.b
        self.assertEqual( expr1(), 20 )
        self.assertEqual( expr2(), 15 )
        self.assertNotEqual( id(expr1._args), id(expr2._args) )
        self.assertNotEqual( id(expr1._args[0]), id(expr2._args[0]) )
        self.assertEqual( id(expr1._args[1]), id(expr2._args[1]) )

        expr1 = self.m.a + self.m.b
        expr2 = expr1.clone()
        self.assertEqual( expr1(), 15 )
        self.assertEqual( expr2(), 15 )
        self.assertNotEqual( id(expr1._args), id(expr2._args) )
        self.assertEqual( id(expr1._args[0]), id(expr2._args[0]) )
        self.assertEqual( id(expr1._args[1]), id(expr2._args[1]) )
        expr1 += self.m.b
        self.assertEqual( expr1(), 25 )
        self.assertEqual( expr2(), 15 )
        self.assertNotEqual( id(expr1._args), id(expr2._args) )
        self.assertEqual( id(expr1._args[0]), id(expr2._args[0]) )
        self.assertEqual( id(expr1._args[1]), id(expr2._args[1]) )

    def test_ProductExpression_mult(self):
        expr1 = self.m.a * self.m.b
        expr2 = expr1.clone()
        self.assertEqual( expr1(), 50 )
        self.assertEqual( expr2(), 50 )
        self.assertNotEqual(id(expr1._numerator),    id(expr2._numerator))
        self.assertNotEqual(id(expr1._denominator),  id(expr2._denominator))
        self.assertEqual   (id(expr1._numerator[0]), id(expr2._numerator[0]))
        self.assertEqual   (id(expr1._numerator[1]), id(expr2._numerator[1]))
        expr1._numerator[0] = self.m.b
        self.assertEqual( expr1(), 100 )
        self.assertEqual( expr2(), 50 )
        self.assertNotEqual(id(expr1._numerator),    id(expr2._numerator))
        self.assertNotEqual(id(expr1._denominator),  id(expr2._denominator))
        self.assertNotEqual(id(expr1._numerator[0]), id(expr2._numerator[0]))
        self.assertEqual   (id(expr1._numerator[1]), id(expr2._numerator[1]))

        expr1 = self.m.a * self.m.b
        expr2 = expr1.clone()
        self.assertEqual( expr1(), 50 )
        self.assertEqual( expr2(), 50 )
        self.assertNotEqual(id(expr1._numerator),    id(expr2._numerator))
        self.assertNotEqual(id(expr1._denominator),  id(expr2._denominator))
        self.assertEqual   (id(expr1._numerator[0]), id(expr2._numerator[0]))
        self.assertEqual   (id(expr1._numerator[1]), id(expr2._numerator[1]))
        expr1 *= self.m.b
        self.assertEqual( expr1(), 500 )
        self.assertEqual( expr2(), 50 )
        self.assertNotEqual(id(expr1._numerator),    id(expr2._numerator))
        self.assertNotEqual(id(expr1._denominator),  id(expr2._denominator))
        self.assertEqual   (id(expr1._numerator[0]), id(expr2._numerator[0]))
        self.assertEqual   (id(expr1._numerator[1]), id(expr2._numerator[1]))

    def test_ProductExpression_div(self):
        expr1 = self.m.a / self.m.b
        expr2 = expr1.clone()
        self.assertEqual( expr1(), 0.5 )
        self.assertEqual( expr2(), 0.5 )
        self.assertNotEqual(id(expr1._numerator),   id(expr2._numerator))
        self.assertNotEqual(id(expr1._denominator), id(expr2._denominator))
        self.assertEqual(id(expr1._numerator[0]),   id(expr2._numerator[0]))
        self.assertEqual(id(expr1._denominator[0]), id(expr2._denominator[0]))
        expr1._denominator[0] = self.m.a
        self.assertEqual( expr1(), 1 )
        self.assertEqual( expr2(), 0.5 )
        self.assertNotEqual(id(expr1._numerator),    id(expr2._numerator))
        self.assertNotEqual(id(expr1._denominator),  id(expr2._denominator))
        self.assertEqual   (id(expr1._numerator[0]), id(expr2._numerator[0]))
        self.assertNotEqual( id(expr1._denominator[0]),
                             id(expr2._denominator[0]) )

        expr1 = self.m.a / self.m.b
        expr2 = expr1.clone()
        self.assertEqual( expr1(), 0.5 )
        self.assertEqual( expr2(), 0.5 )
        self.assertNotEqual(id(expr1._numerator),   id(expr2._numerator))
        self.assertNotEqual(id(expr1._denominator), id(expr2._denominator))
        self.assertEqual(id(expr1._numerator[0]),   id(expr2._numerator[0]))
        self.assertEqual(id(expr1._denominator[0]), id(expr2._denominator[0]))
        expr1 /= self.m.b
        self.assertEqual( expr1(), 0.05 )
        self.assertEqual( expr2(), 0.5 )
        self.assertNotEqual(id(expr1._numerator),   id(expr2._numerator))
        self.assertNotEqual(id(expr1._denominator), id(expr2._denominator))
        self.assertEqual(id(expr1._numerator[0]),   id(expr2._numerator[0]))
        self.assertEqual(id(expr1._denominator[0]), id(expr2._denominator[0]))

    def test_sumOfExpressions(self):
        expr1 = self.m.a * self.m.b + self.m.a * self.m.a
        expr2 = expr1.clone()
        self.assertEqual(expr1(), 75)
        self.assertEqual(expr2(), 75)
        self.assertNotEqual(id(expr1._args), id(expr2._args))
        self.assertEqual(expr1._args[0](), expr2._args[0]())
        self.assertEqual(expr1._args[1](), expr2._args[1]())
        self.assertNotEqual(id(expr1._args[0]), id(expr2._args[0]))
        self.assertNotEqual(id(expr1._args[1]), id(expr2._args[1]))
        expr1 += self.m.b
        self.assertEqual(expr1(), 85)
        self.assertEqual(expr2(), 75)
        self.assertNotEqual(id(expr1._args), id(expr2._args))
        self.assertEqual(len(expr1._args), 3)
        self.assertEqual(len(expr2._args), 2)
        self.assertEqual(expr1._args[0](), expr2._args[0]())
        self.assertEqual(expr1._args[1](), expr2._args[1]())
        self.assertNotEqual(id(expr1._args[0]), id(expr2._args[0]))
        self.assertNotEqual(id(expr1._args[1]), id(expr2._args[1]))

    def test_productOfExpressions(self):
        expr1 = (self.m.a + self.m.b) * (self.m.a + self.m.a)
        expr2 = expr1.clone()
        self.assertEqual(expr1(), 150)
        self.assertEqual(expr2(), 150)
        self.assertNotEqual(id(expr1._numerator), id(expr2._numerator))
        self.assertNotEqual(id(expr1._denominator), id(expr2._denominator))
        self.assertEqual(expr1._numerator[0](), expr2._numerator[0]())
        self.assertEqual(expr1._numerator[1](), expr2._numerator[1]())
        self.assertNotEqual(id(expr1._numerator[0]), id(expr2._numerator[0]))
        self.assertNotEqual(id(expr1._numerator[1]), id(expr2._numerator[1]))
        expr1 *= self.m.b
        self.assertEqual(expr1(), 1500)
        self.assertEqual(expr2(), 150)
        self.assertNotEqual(id(expr1._numerator), id(expr2._numerator))
        self.assertNotEqual(id(expr1._denominator), id(expr2._denominator))
        self.assertEqual(len(expr1._numerator), 3)
        self.assertEqual(len(expr2._numerator), 2)
        self.assertEqual(len(expr1._denominator), 0)
        self.assertEqual(len(expr2._denominator), 0)
        self.assertEqual(expr1._numerator[0](), expr2._numerator[0]())
        self.assertEqual(expr1._numerator[1](), expr2._numerator[1]())
        self.assertNotEqual(id(expr1._numerator[0]), id(expr2._numerator[0]))
        self.assertNotEqual(id(expr1._numerator[1]), id(expr2._numerator[1]))

    def test_productOfExpressions_div(self):
        expr1 = (self.m.a + self.m.b) / (self.m.a + self.m.a)
        expr2 = expr1.clone()
        self.assertEqual(expr1(), 1.5)
        self.assertEqual(expr2(), 1.5)
        self.assertNotEqual(id(expr1._numerator), id(expr2._numerator))
        self.assertNotEqual(id(expr1._denominator), id(expr2._denominator))
        self.assertEqual(expr1._numerator[0](), expr2._numerator[0]())
        self.assertEqual(expr1._denominator[0](), expr2._denominator[0]())
        self.assertNotEqual(id(expr1._numerator[0]),id(expr2._numerator[0]))
        self.assertNotEqual(id(expr1._denominator[0]),id(expr2._denominator[0]))
        expr1 /= self.m.b
        self.assertEqual(expr1(), .15)
        self.assertEqual(expr2(), 1.5)
        self.assertNotEqual(id(expr1._numerator), id(expr2._numerator))
        self.assertNotEqual(id(expr1._denominator), id(expr2._denominator))
        self.assertEqual(len(expr1._numerator), 1)
        self.assertEqual(len(expr2._numerator), 1)
        self.assertEqual(len(expr1._denominator), 2)
        self.assertEqual(len(expr2._denominator), 1)
        self.assertEqual(expr1._numerator[0](), expr2._numerator[0]())
        self.assertEqual(expr1._denominator[0](), expr2._denominator[0]())
        self.assertNotEqual(id(expr1._numerator[0]), id(expr2._numerator[0]))
        self.assertNotEqual(id(expr1._denominator[0]),id(expr2._denominator[0]))


if __name__ == "__main__":
    unittest.main()
