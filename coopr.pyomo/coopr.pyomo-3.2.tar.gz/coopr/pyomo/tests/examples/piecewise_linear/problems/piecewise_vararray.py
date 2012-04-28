"""
       / 2x          , 0 <= x <= 1
       | (1/2)x+(3/2), 1 <= x <= 3
f(x) = | -3x+12      , 3 <= x <= 5
       \ 2x-13       , 5 <= x <= 6
"""

from coopr.pyomo import *

INDEX_SET = [1,2,3,4] # There will be two copies of this function
DOMAIN_PTS = dict([(t,[float(i) for i in [0,1,3,5,6]]) for t in INDEX_SET])
RANGE_PTS = {0.0:0.0, 1.0:2.0, 3.0:3.0, 5.0:-3.0, 6.0:-1.0}

def F(model,t,x):
    return RANGE_PTS[x]*model.p[t]

def define_model(**kwds):

    model = ConcreteModel()

    model.x = Var(INDEX_SET) # domain variable
    model.Fx = Var(INDEX_SET) # range variable
    model.p = Var(INDEX_SET, initialize=1.0)

    model.obj = Objective(expr=summation(model.Fx), sense=kwds.pop('sense',maximize))

    model.piecewise = Piecewise(INDEX_SET,model.Fx,model.x,
                                  pw_pts=DOMAIN_PTS,
                                  f_rule=F, **kwds)

    #Fix the answer for testing purposes
    model.set_answer_constraint1 = Constraint(expr= model.x[1] == 0.0)
    model.set_answer_constraint2 = Constraint(expr= model.x[2] == 3.0)
    model.set_answer_constraint3 = Constraint(expr= model.x[3] == 5.5)
    model.set_answer_constraint4 = Constraint(expr= model.x[4] == 6.0)
    
    return model
