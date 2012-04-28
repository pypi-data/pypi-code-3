#  _________________________________________________________________________
#
#  Coopr: A COmmon Optimization Python Repository
#  Copyright (c) 2008 Sandia Corporation.
#  This software is distributed under the BSD License.
#  Under the terms of Contract DE-AC04-94AL85000 with Sandia Corporation,
#  the U.S. Government retains certain rights in this software.
#  For more information, see the Coopr README.txt file.
#  _________________________________________________________________________

import logging
import os
import re

from coopr.opt import *
#from coopr.opt.base import ProblemFormat as PF, ResultsFormat as RF
#from coopr.opt.results import ProblemSense as PS, SolverResults, \
                              #SolutionStatus, SolverStatus, TerminationCondition
from coopr.opt.solver import SystemCallSolver

from pyutilib.common import ApplicationError
import pyutilib.component.core
from pyutilib.misc import Bunch, Options
from pyutilib.services import register_executable, registered_executable
from pyutilib.services import TempfileManager

Logger = logging.getLogger('coopr.plugins')

glpk_file_flag=None

def configure_glpk():
    global glpk_file_flag
    if glpk_file_flag is not None:
        return
    glpk_file_flag = False
    if registered_executable("glpsol") is None:
        return
    errcode, results = pyutilib.subprocess.run(
        [registered_executable('glpsol').get_path(), "--version"])
    if errcode == 0:
        lines = results.split('\n') 
        if len(lines) == 0 or lines[0] == '':
            return
        m = re.search('(\d+)\.(\d+)', lines[0].split()[-1])
        if m:
            _version = tuple(int(i) for i in m.groups())
            glpk_file_flag = _version >= (4,42)


# Not sure how better to get these constants, but pulled from GLPK
# documentation and source code (include/glpk.h)

   # status of auxiliary / structural variables
GLP_BS = 1   # inactive constraint / basic variable
GLP_NL = 2   # active constraint or non-basic variable on lower bound
GLP_NU = 3   # active constraint or non-basic variable on upper bound
GLP_NF = 4   # active free row or non-basic free variable
GLP_NS = 5   # active equality constraint or non-basic fixed variable

   # solution status
GLP_UNDEF  = 1  # solution is undefined
GLP_FEAS   = 2  # solution is feasible
GLP_INFEAS = 3  # solution is infeasible
GLP_NOFEAS = 4  # no feasible solution exists
GLP_OPT    = 5  # solution is optimal
GLP_UNBND  = 6  # solution is unbounded


class GLPK(OptSolver):
    """The GLPK LP/MIP solver"""

    pyutilib.component.core.alias('glpk', doc='The GLPK MIP solver')

    def __new__(cls, *args, **kwds):
        try:
            mode = kwds['solver_io']
            if mode is None:
                mode = 'lp'
            del kwds['solver_io']
        except KeyError:
            mode = 'lp'
        #
        if mode  == 'lp':
            if glpk_file_flag:
                return SolverFactory('_glpk_shell', **kwds)
            else:
                return SolverFactory('_glpk_shell_old', **kwds)
        if mode == 'python':
            opt = SolverFactory('_glpk_direct', **kwds)
            if opt is None:
                logging.getLogger('coopr.plugins').error('Python API for GLPK is not installed')
                return
            return opt
        #
        if mode == 'os':
            opt = SolverFactory('_ossolver', **kwds)
        else:
            logging.getLogger('coopr.plugins').error('Unknown IO type: %s' % mode)
            return
        opt.set_options('solver=glpsol')
        return opt


class GLPKSHELL ( SystemCallSolver ):
    """Shell interface to the GLPK LP/MIP solver"""

    pyutilib.component.core.alias('_glpk_shell', doc='Shell interface to the GNU Linear Programming Kit')

    def __init__ ( self, **kwargs ):
        #
        # Call base constructor
        #
        kwargs['type'] = 'glpk'
        SystemCallSolver.__init__( self, **kwargs )
        #
        # Valid problem formats, and valid results for each format
        #
        self._valid_problem_formats = [ ProblemFormat.cpxlp, ProblemFormat.mps, ProblemFormat.mod ]
        self._valid_result_formats = {
          ProblemFormat.mod:   ResultsFormat.soln,
          ProblemFormat.cpxlp: ResultsFormat.soln,
          ProblemFormat.mps:   ResultsFormat.soln,
        }

        # Note: Undefined capabilities default to 'None'
        self._capabilities = Options()
        self._capabilities.linear = True
        self._capabilities.integer = True
        self._capabilities.sos1 = False
        self._capabilities.sos2 = False
        self._capabilities.sosn = False

    def executable ( self ):
        executable = registered_executable('glpsol')
        if executable is None:
            msg = "Could not locate the 'glpsol' executable, which is "          \
                  "required for solver '%s'"
            pyutilib.component.core.PluginGlobals.env().log.error(msg % self.name)
            self.enable = False
            return None

        return executable.get_path()


    def create_command_line ( self, executable, problem_files ):
        #
        # Define log file
        #
        if self.log_file is None:
            self.log_file = TempfileManager.create_tempfile(suffix='.glpk.log')

        #
        # Define solution file
        #
        if self.soln_file is None:
            self.soln_file = \
                 TempfileManager.create_tempfile(suffix='.glpk.soln')
        self._glpfile = TempfileManager.create_tempfile(suffix='.glpk.glp')
        self._rawfile = TempfileManager.create_tempfile(suffix='.glpk.raw')

        #
        # Define results file
        #
        if self._results_format is None or self._results_format == ResultsFormat.soln:
            self.results_file = self.soln_file

        #
        # Define command line
        #
        cmd = [executable]
        if self._timer:
            cmd.insert(0, self._timer)
        for key in self.options:
            opt = self.options[ key ]
            cmd.extend(["--%s" % key, str(opt)])
            #if isinstance(opt, basestring) and ' ' in opt:
            #    cmd.append('--%s "%s"' % (key, str(opt)) )
            #else:
            #    cmd.append('--%s %s' % (key, str(opt)) )

        if self._timelimit is not None and self._timelimit > 0.0:
            cmd.extend(['--tmlim', str(self._timelimit)])

        cmd.extend(['--write', self._rawfile])
        cmd.extend(['--wglp', self._glpfile])

        if self._problem_format == ProblemFormat.cpxlp:
            cmd.extend(['--cpxlp', problem_files[0]])
        elif self._problem_format == ProblemFormat.mps:
            cmd.extend(['--freemps', problem_files[0]])
        elif self._problem_format == ProblemFormat.mod:
            cmd.extend(['--math', problem_files[0]])
            for fname in problem_files[1:]:
                cmd.extend(['--data', fname])

        return Bunch(cmd=cmd, log_file=self.log_file, env=None)


    def process_logfile(self):
        """
        Process logfile
        """
        results = SolverResults()

          # For the lazy programmer, handle long variable names
        prob   = results.problem
        solv   = results.solver
        solv.termination_condition = TerminationCondition.unknown
        stats  = results.solver.statistics
        bbound = stats.branch_and_bound

        prob.upper_bound = float('inf')
        prob.lower_bound = float('-inf')
        bbound.number_of_created_subproblems = 0
        bbound.number_of_bounded_subproblems = 0

        with open( self.log_file, 'r' ) as output:
            for line in output:
                toks = line.split()
                if 'tree is empty' in line:
                    bbound.number_of_created_subproblems = toks[-1][:-1]
                    bbound.number_of_bounded_subproblems = toks[-1][:-1]
                elif len(toks) == 2 and toks[0] == "sys":
                    solv.system_time = toks[1]
                elif len(toks) == 2 and toks[0] == "user":
                    solv.user_time = toks[1]
                elif len(toks) > 2 and (toks[0], toks[2]) == ("TIME", "EXCEEDED;"):
                    solv.termination_condition = TerminationCondition.maxTimeLimit
                elif len(toks) > 5 and (toks[:6] == ['PROBLEM', 'HAS', 'NO', 'DUAL', 'FEASIBLE', 'SOLUTION']):
                    solv.termination_condition = TerminationCondition.unbounded
                elif len(toks) > 5 and (toks[:6] == ['PROBLEM', 'HAS', 'NO', 'PRIMAL', 'FEASIBLE', 'SOLUTION']):
                    solv.termination_condition = TerminationCondition.infeasible
                elif len(toks) > 4 and (toks[:5] == ['PROBLEM', 'HAS', 'NO', 'FEASIBLE', 'SOLUTION']):
                    solv.termination_condition = TerminationCondition.infeasible
                elif len(toks) > 6 and (toks[:7] == ['LP', 'RELAXATION', 'HAS', 'NO', 'DUAL', 'FEASIBLE', 'SOLUTION']):
                    solv.termination_condition = TerminationCondition.unbounded

        return results


    def _glpk_get_solution_status ( self, status ):
        if   GLP_OPT    == status: return SolutionStatus.optimal
        elif GLP_FEAS   == status: return SolutionStatus.feasible
        elif GLP_INFEAS == status: return SolutionStatus.infeasible
        elif GLP_NOFEAS == status: return SolutionStatus.infeasible
        elif GLP_UNBND  == status: return SolutionStatus.unbounded
        elif GLP_UNDEF  == status: return SolutionStatus.other
        raise RuntimeError, "Unknown solution status returned by GLPK solver"


    def process_soln_file ( self, results ):
        pdata = self._glpfile
        psoln = self._rawfile

        prob = results.problem
        solv = results.solver

        prob.name = 'unknown'   # will ostensibly get updated

        # Step 1: Make use of the GLPK's machine parseable format (--wglp) to
        #    collect variable and constraint names.
        glp_line_count = ' -- File not yet opened'

        # The trick for getting the variable names correctly matched to their
        # values is the note that the --wglp option outputs them in the same
        # order as the --write output.
        # Note that documentation for these formats is available from the GLPK
        # documentation of 'glp_read_prob' and 'glp_write_sol'
        variable_names = dict()    # cols
        constraint_names = dict()  # rows
        obj_name = 'objective'

        try:
            f = open( pdata, 'r')

            glp_line_count = 1
            pprob, ptype, psense, prows, pcols, pnonz = f.readline().split()
            prows = int( prows )  # fails if not a number; intentional
            pcols = int( pcols )  # fails if not a number; intentional
            pnonz = int( pnonz )  # fails if not a number; intentional

            if pprob != 'p' or \
               ptype not in ('lp', 'mip') or \
               psense not in ('max', 'min') or \
               prows < 0 or pcols < 0 or pnonz < 0:
                raise ValueError

            self.is_integer = ( 'mip' == ptype and True or False )
            prob.sense = 'min' == psense and ProblemSense.minimize or ProblemSense.maximize
            prob.number_of_constraints = prows
            prob.number_of_nonzeros    = pnonz
            prob.number_of_variables   = pcols

            extract_duals = False
            for suffix in self.suffixes:
                if re.match(suffix, "dual"):
                    if self.is_integer:
                        if suffix == 'dual':
                            raise RuntimeError, 'Request for duals of an integer problem.'
                    else:
                        extract_duals = True

            for line in f:
                glp_line_count += 1
                tokens = line.split()
                switch = tokens.pop(0)

                if switch in ('a', 'e', 'i', 'j'):
                    pass
                elif 'n' == switch:  # naming some attribute
                    ntype = tokens.pop(0)
                    name  = tokens.pop()
                    if 'i' == ntype:      # row
                        row = tokens.pop()
                        constraint_names[ int(row) ] = name
                        # --write order == --wglp order; store name w/ row no
                    elif 'j' == ntype:    # var
                        col = tokens.pop()
                        variable_names[ int(col) ] = name
                        # --write order == --wglp order; store name w/ col no
                    elif 'z' == ntype:    # objective
                        obj_name = name
                    elif 'p' == ntype:    # problem name
                        prob_name = name
                    else:                 # anything else is incorrect.
                        raise ValueError

                else:
                    raise ValueError

            f.close()
        except Exception, e:
            msg = "Error parsing solution description file, line %s: %s"
            raise ValueError, msg % (glp_line_count, str(e))


        # Step 2: Make use of the GLPK's machine parseable format (--write) to
        #    collect solution variable and constraint values.
        raw_line_count = ' -- File not yet opened'
        try:
            f = open( psoln, 'r')

            raw_line_count = 1
            prows, pcols = f.readline().split()
            prows = int( prows )  # fails if not a number; intentional
            pcols = int( pcols )  # fails if not a number; intentional

            raw_line_count = 2
            if self.is_integer:
                pstat, obj_val = f.readline().split()
            else:
                pstat, dstat, obj_val = f.readline().split()
                dstat = float( dstat ) # dual status of basic solution.  Ignored.
            #print "HERE", pstat, obj_val, self.is_integer

            pstat = float( pstat )       # fails if not a number; intentional
            obj_val = float( obj_val )   # fails if not a number; intentional
            soln_status = self._glpk_get_solution_status( pstat )

            #print "HEREZ", soln_status
            if soln_status is SolutionStatus.infeasible:
                solv.termination_condition = TerminationCondition.infeasible

            elif soln_status is SolutionStatus.unbounded:
                solv.termination_condition = TerminationCondition.unbounded

            elif soln_status is SolutionStatus.other:
                if solv.termination_condition == TerminationCondition.unknown:
                    solv.termination_condition = TerminationCondition.other

            elif soln_status in ( SolutionStatus.optimal, SolutionStatus.feasible ):
                soln   = results.solution.add()
                soln.status = soln_status

                prob.lower_bound = obj_val
                prob.upper_bound = obj_val

                # TODO: Does a 'feasible' status mean that we're optimal?
                soln.gap=0.0
                solv.termination_condition = TerminationCondition.optimal
                

                # I'd like to choose the correct answer rather than just doing
                # something like commenting the obj_name line.  The point is that
                # we ostensibly could or should make use of the user's choice in
                # objective name.  In that vein I'd like to set the objective value
                # to the objective name.  This would make parsing on the user end
                # less 'arbitrary', as in the yaml key 'f'.  Weird
                soln.objective[ obj_name ] = obj_val

                for mm in range( 1, prows +1 ):
                    raw_line_count += 1
                    if self.is_integer:
                        rprim = f.readline()   # should be a single number
                    else:
                        rstat, rprim, rdual = f.readline().split()
                        rstat = float( rstat )

                    cname = constraint_names[ mm ]
                    if 'ONE_VAR_CONSTANT' == cname[-16:]: continue
                    rprim = float( rprim )
                    soln.constraint[ cname ].value = rprim

                    #print "HERE", extract_duals, self.is_integer
                    if extract_duals and not self.is_integer:
                        rdual = float(rdual)
                        soln.constraint[ cname ].dual  = rdual

                for nn in range( 1, pcols +1 ):
                    raw_line_count += 1
                    if self.is_integer:
                        cprim = f.readline()      # should be a single number
                    else:
                        cstat, cprim, cdual = f.readline().split()
                        cstat = float( cstat )  # fails if not a number; intentional

                    vname = variable_names[ nn ]
                    if 'ONE_VAR_CONSTANT' == vname: continue
                    cprim = float( cprim )
                    soln.variable[ vname ] = {"Value" : cprim, "Id" : len(soln.variable)}

                    #if extract_duals and not self.is_integer:
                    #       cdual = float(cdual)
                    #       soln.variable[ vname ].dual  = cdual
                    #       GLPK reports a dual for variables, though Pyomo does not have
                    #       a place to put them

            f.close()
        except Exception, e:
            print e
            msg = "Error parsing solution data file, line %d" % raw_line_count
            raise ValueError, msg


#class MockGLPK(GLPK,mockmip.MockMIP):
#       """A Mock GLPK solver used for testing
#       """

#       pyutilib.component.core.alias('_mock_glpk')

#       def __init__(self, **kwds):
#               try:
#                  GLPK.__init__(self, **kwds)
#               except ApplicationError: #pragma:nocover
#                  pass                                         #pragma:nocover
#               mockmip.MockMIP.__init__(self,"glpk")
#
#       def available(self, exception_flag=True):
#               return GLPK.available(self,exception_flag)
#
#       def create_command_line(self,executable,problem_files):
#               command = GLPK.create_command_line(self,executable,problem_files)
#               mockmip.MockMIP.create_command_line(self,executable,problem_files)
#               return command
#
#       def executable(self):
#               return mockmip.MockMIP.executable(self)
#
#       def _execute_command(self,cmd):
#               return mockmip.MockMIP._execute_command(self,cmd)
#
#       def _convert_problem(self,args,pformat,valid_pformats):
#               if pformat in [ProblemFormat.mps,ProblemFormat.cpxlp]:
#                  return (args,pformat,None)
#               else:
#                  return (args,ProblemFormat.cpxlp,None)


register_executable( name='glpsol')
