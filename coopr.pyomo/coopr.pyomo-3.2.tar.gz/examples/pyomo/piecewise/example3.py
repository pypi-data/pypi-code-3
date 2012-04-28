# A strictly affine piecewise example
#
#        / (1/3)X - (2/3), -1 <= X <= 2
# Z(X) = | -2X + 4       ,  2 <= X <= 6
#        \ 5X - 38       ,  6 <= X <= 10

from coopr.pyomo import *

# Define the function
# Just like in Pyomo constraint rules, a Pyomo model object
# must be the first argument for the function rule
RANGE_POINTS = {-1.0:-1.0, 2.0:0.0, 6.0:-8.0, 10.0:12.0}
def f(model,x):
    return RANGE_POINTS[x]

model = ConcreteModel()

model.X = Var()
model.Z = Var()
model.p = Var(within = NonNegativeReals)
model.n = Var(within = NonNegativeReals)

# See documentation on Piecewise component by typing
# help(Piecewise) in a python terminal after importing coopr.pyomo
# Using BigM constraints with binary variables to represent the piecwise constraints
model.con = Piecewise(model.Z,model.X, # range and domain variables
                      pw_pts=[-1.0,2.0,6.0,10.0],
                      pw_constr_type='EQ',
                      pw_repn='DCC', 
                      f_rule=f)

# minimize the 1-norm distance of Z to 7.0, i.e., |Z-7|
model.pn_con = Constraint(expr= model.Z - 7.0 == model.p - model.n)
model.obj = Objective(rule = lambda model: model.p+model.n , sense=minimize)
