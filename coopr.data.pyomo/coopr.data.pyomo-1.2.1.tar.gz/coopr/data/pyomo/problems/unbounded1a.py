from coopr.pyomo import *

model = ConcreteModel()

model.x = Var()
model.y = Var()

model.o = Objective(expr=model.x+model.y)
