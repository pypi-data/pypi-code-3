# A simple example illustrating a piecewise
# representation of the function Z(X)
# 
#          / -X+2 , -5 <= X <= 1
#  Z(X) >= |
#          \  X ,  1 <= X <= 5
#

from coopr.pyomo import *

# Define the function
# Just like in Pyomo constraint rules, a Pyomo model object
# must be the first argument for the function rule
def f(model,x):
    return abs(x-1)+1.0

model = ConcreteModel()

model.X = Var()
model.Z = Var()

# See documentation on Piecewise component by typing
# help(Piecewise) in a python terminal after importing coopr.pyomo
model.con = Piecewise(model.Z,model.X, # range and domain variables
                      pw_pts=[-5,1,5] ,
                      pw_constr_type='LB',
                      f_rule=f)

# The default piecewise representation implemented by Piecewise is SOS2.
# Note, however, that no SOS2 variables will be generated since the 
# check for convexity within Piecewise automatically simplifies the constraints
# when a lower bounding convex function is supplied. Adding 'force_pw=True'
# to the Piecewise argument list will cause the original piecewise constraints
# to be used even when simplifications can be applied.
model.obj = Objective(expr=model.Z, sense=minimize)
