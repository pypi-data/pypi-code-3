# Imports from Coopr and PyUtilib
from coopr.pyomo import *
from pyutilib.component.core import *
from coopr.opt import *


@plugin_factory(SolverFactory)
class MySolver(object):

    alias('greedy')

    # Declare that this is an IOptSolver plugin
    implements(IOptSolver)

    # Solve the specified problem and return
    # a SolverResults object
    def solve(self, instance, **kwds):
        print "Starting greedy heuristic"
        val, instance = self._greedy(instance)
        n = value(instance.N)
        # Setup results
        results = SolverResults()
        results.problem.name = instance.name
        results.problem.sense = ProblemSense.minimize
        results.problem.num_constraints = 1
        results.problem.num_variables = n
        results.problem.num_objectives = 1
        results.solver.status = SolverStatus.ok
        soln = results.solution.add()
        soln.value = val
        soln.status = SolutionStatus.feasible
        for j in xsequence(n):
            if instance.y[j].value is 1:
                soln.variable[instance.y[j].name] = {"Value" : 1, "Id" : j}
        return results

    # Perform a greedy search
    def _greedy(self, instance):
        p = value(instance.P)
        n = value(instance.N)
        m = value(instance.M)
        fixed=set()
        # Initialize
        for j in xsequence(n):
            instance.y[j].value=0
        # Greedily fix the next best facility
        for i in xsequence(p):
            best = None
            ndx=j
            for j in xsequence(n):
                if j in fixed:
                    continue
                instance.y[j].value=1
                # Compute value
                val = 0.0
                for kk in xsequence(m):
                    tmp=copy.copy(fixed)
                    tmp.add(j)
                    tbest = None
                    for jj in tmp:
                        if tbest is None or instance.d[jj,kk].value < tbest:
                            tbest = instance.d[jj,kk].value
                    val += tbest
                # Keep best greedy choice
                if best is None or val < best:
                    best=val
                    ndx=j
                instance.y[j].value=0
            fixed.add(ndx)
            instance.y[ndx].value=1
        return [best, instance]
