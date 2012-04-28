#  _________________________________________________________________________
#
#  Coopr: A COmmon Optimization Python Repository
#  Copyright (c) 2008 Sandia Corporation.
#  This software is distributed under the BSD License.
#  Under the terms of Contract DE-AC04-94AL85000 with Sandia Corporation,
#  the U.S. Government retains certain rights in this software.
#  For more information, see the Coopr README.txt file.
#  _________________________________________________________________________

__all__ = ['CBC', 'MockCBC']

import os
import re
import string
from coopr.opt.base import *
from coopr.opt.results import *
from coopr.opt.solver import *
import pyutilib.services
import pyutilib.misc
import pyutilib.common
import pyutilib.component.core
import pyutilib.subprocess
import mockmip
import logging

cbc_compiled_with_asl=None

def configure():
    global cbc_compiled_with_asl
    if cbc_compiled_with_asl is None:
        # manually look for the cbc executable to prevent the
        # CBC.execute() from logging an error when CBC is missing
        if pyutilib.services.registered_executable("cbc") is None:
            cbc_compiled_with_asl = False
        else:
            cbc_exec = CBC().executable()
            results = pyutilib.subprocess.run(
                [cbc_exec,"dummy","-AMPL","-stop"] )
            if cbc_compiled_with_asl is not None:
                raise IOError
            cbc_compiled_with_asl = not ('No match for AMPL' in results[1])


class CBC(OptSolver):
    """The CBC LP/MIP solver
    """

    pyutilib.component.core.alias('cbc', doc='The CBC MIP solver')

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
            return SolverFactory('_cbc_shell', **kwds)
        #
        if mode == 'nl':
            if cbc_compiled_with_asl:
                opt = SolverFactory('_asl', **kwds)
            else:
                logging.getLogger('coopr.plugins').error('CBC solver is not compiled with ASL interface.')
                return
        elif mode == 'os':
            opt = SolverFactory('_ossolver', **kwds)
        else:
            logging.getLogger('coopr.plugins').error('Unknown IO type: %s' % mode)
            return
        opt.set_options('solver=cbc')
        return opt


class CBCSHELL(SystemCallSolver):
    """Shell interface to the CBC LP/MIP solver
    """

    pyutilib.component.core.alias('_cbc_shell',  doc='Shell interface to the CBC LP/MIP solver')

    def __init__(self, **kwds):
        #
        # Call base constructor
        #
        kwds['type'] = 'cbc'
        SystemCallSolver.__init__(self, **kwds)

        #
        # Set up valid problem formats and valid results for each problem format
        #
#        self._valid_problem_formats=[ProblemFormat.nl, ProblemFormat.cpxlp, ProblemFormat.mps]
        self._valid_problem_formats=[ProblemFormat.cpxlp, ProblemFormat.mps]
        if cbc_compiled_with_asl:
            self._valid_problem_formats.append(ProblemFormat.nl)
        self._valid_result_formats={}
        self._valid_result_formats[ProblemFormat.cpxlp] = [ResultsFormat.soln]
        if cbc_compiled_with_asl:
            self._valid_result_formats[ProblemFormat.nl] = [ResultsFormat.sol]
        self._valid_result_formats[ProblemFormat.mps] = [ResultsFormat.soln]

        # Note: Undefined capabilities default to 'None'
        self._capabilities = pyutilib.misc.Options()
        self._capabilities.linear = True
        self._capabilities.integer = True

    def _presolve(self, *args, **kwds):

        # establish real "default" problem and results formats. these may be
        # over-ridden in the base class solve (via keywords), but we should
        # have real values by the time we're presolving.
        if self._problem_format is None:

            if cbc_compiled_with_asl and self._valid_problem_formats[0] is ProblemFormat.nl:
                self._problem_format = ProblemFormat.nl
            else:
                self._problem_format = ProblemFormat.cpxlp

        # in CBC, the results format is defined by the problem format;
        # you can't vary them independently.
        if cbc_compiled_with_asl and self._problem_format is ProblemFormat.nl:
            self._results_format = ResultsFormat.sol
        else:
            # this really means "CBC-specific" format - not drawing from the
            # log file itself (although additional information is contained there).
            self._results_format = ResultsFormat.soln

        # let the base class handle any remaining keywords/actions.
        SystemCallSolver._presolve(self, *args, **kwds)

    def executable(self):
        executable = pyutilib.services.registered_executable("cbc")
        if executable is None:
            pyutilib.component.core.PluginGlobals.env().log.error("Could not locate the 'cbc' executable, which is required for solver %s" % self.name)
            self.enable = False
            return None
        return executable.get_path()

    def create_command_line(self, executable, problem_files):
        #
        # Define the log file
        #
        if self.log_file is None:
            self.log_file = pyutilib.services.TempfileManager.create_tempfile(suffix=".cbc.log")

        #
        # Define the solution file
        #

        # the prefix of the problem filename is required because CBC has a specific
        # and automatic convention for generating the output solution filename.
        # the extracted prefix is the same name as the input filename, e.g., minus
        # the ".lp" extension.
        problem_filename_prefix = problem_files[0]
        if '.' in problem_filename_prefix:
            tmp = problem_filename_prefix.split('.')
            if len(tmp) > 2:
                problem_filename_prefix = '.'.join(tmp[:-1])
            else:
                problem_filename_prefix = tmp[0]

        #if not cbc_compiled_with_asl:
            #self._results_format = ResultsFormat.soln
            #self.results_reader = None
        if self._results_format is ResultsFormat.sol:
            self.soln_file = problem_filename_prefix+".sol"
        else:
            self.soln_file = problem_filename_prefix+".soln"

        #
        # Define the results file
        #
        # results in CBC are split across the log file (solver statistics) and
        # the solution file (solutions!)
        self.results_file = self.soln_file

        def _check_and_escape_options(options):
            for key, val in self.options.iteritems():
                tmp_k = str(key)
                _bad = ' ' in tmp_k

                tmp_v = str(val)
                if ' ' in tmp_v:
                    if '"' in tmp_v:
                        if "'" in tmp_v:
                            _bad = True
                        else:
                            tmp_v = "'" + tmp_v + "'"
                    else:
                        tmp_v = '"' + tmp_v + '"'

                if _bad:
                    raise ValueError("Unable to properly escape solver option:"
                                     "\n\t%s=%s" % (key, val) )
                yield (tmp_k, tmp_v)

        #
        # Define command line
        #
        cmd = [ executable ]
        if self._timer:
            cmd.append(self._timer)

        if self._problem_format == ProblemFormat.nl:
            cmd.append(problem_files[0])
            cmd.append('-AMPL')

            opts = ["stat=1", "printingOptions=all"]
            if self._timelimit is not None and self._timelimit > 0.0:
                opts.append("sec=%s" % (self._timelimit,))
            if "debug" in self.options:
                opts.append("log=5")
            for key, val in _check_and_escape_options(self.options):
                opts.append("%s=%s" % ( key, tmp ))

            env["CBC_options"] = " ".join(opts)            

        else:
            if self._timelimit is not None and self._timelimit > 0.0:
                cmd.extend(['-sec', str(self._timelimit)])
            if "debug" in self.options:
                cmd.extend(["-log","5"])
            for key, val in _check_and_escape_options(self.options):
                cmd.extend(['-'+key, tmp])
            cmd.extend(["-printingOptions", "all",
                        "-import", problem_files[0],
                        "-import",
                        "-stat", "1",
                        "-solve", 
                        "-solu", self.soln_file])

        return pyutilib.misc.Bunch(cmd=cmd, log_file=self.log_file, env=None)

    def process_logfile(self):
        """
        Process logfile
        """
        results = SolverResults()
        #
        # Initial values
        #
        soln = Solution()
        soln.objective['__default_objective__'].value = float('inf')
        #
        # Process logfile
        #
        OUTPUT = open(self.log_file)
        output = "".join(OUTPUT.readlines())
        OUTPUT.close()
        #
        # Parse logfile lines
        #
        results.problem.sense = ProblemSense.minimize
        results.problem.name = None
        for line in output.split("\n"):
            tokens = re.split('[ \t]+',line.strip())
            if len(tokens) == 10 and tokens[0] == "Current" and tokens[1] == "default" and tokens[2] == "(if" and results.problem.name is None:
                results.problem.name = tokens[-1]
                if '.' in results.problem.name:
                    parts = results.problem.name.split('.')
                    if len(parts) > 2:
                        results.problem.name = '.'.join(parts[:-1])
                    else:
                        results.problem.name = results.problem.name.split('.')[0]
                if '/' in results.problem.name:
                    results.problem.name = results.problem.name.split('/')[-1]
                if '\\' in results.problem.name:
                    results.problem.name = results.problem.name.split('\\')[-1]
            if len(tokens) ==11 and tokens[0] == "Presolve" and tokens[3] == "rows,":
                results.problem.number_of_variables = eval(tokens[4])-eval(tokens[5][1:-1])
                results.problem.number_of_constraints = eval(tokens[1])-eval(tokens[2][1:-1])
                results.problem.number_of_nonzeros = eval(tokens[8])-eval(tokens[9][1:-1])
                results.problem.number_of_objectives = "1"
            if len(tokens) >=9 and tokens[0] == "Problem" and tokens[2] == "has":
                results.problem.number_of_variables = eval(tokens[5])
                results.problem.number_of_constraints = eval(tokens[3])
                results.problem.number_of_nonzeros = eval(tokens[8])
                results.problem.number_of_objectives = "1"
            if len(tokens) == 5 and tokens[3] == "NAME":
                results.problem.name = tokens[4]
            if " ".join(tokens) == '### WARNING: CoinLpIO::readLp(): Maximization problem reformulated as minimization':
                results.problem.sense = ProblemSense.maximize
            if len(tokens) > 6 and tokens[0] == "Presolve" and tokens[6] == "infeasible":
                soln.status = SolutionStatus.infeasible
                soln.objective['__default_objective__'].value = None
            if len(tokens) > 3 and tokens[0] == "Optimal" and tokens[1] == "objective":
                soln.status = SolutionStatus.optimal
                soln.objective['__default_objective__'].value=eval(tokens[2])
            if len(tokens) > 6 and tokens[4] == "best" and tokens[5] == "objective":
                soln.objective['__default_objective__'].value=eval(tokens[6])
            if len(tokens) > 9 and tokens[7] == "(best" and tokens[8] == "possible":
                results.problem.lower_bound=tokens[9]
                results.problem.lower_bound = eval(results.problem.lower_bound.split(")")[0])
            if len(tokens) > 12 and tokens[10] == "best" and tokens[11] == "possible":
                results.problem.lower_bound=eval(tokens[12])
            if len(tokens) > 3 and tokens[0] == "Result" and tokens[2] == "Finished":
                soln.status = SolutionStatus.optimal
                soln.objective['__default_objective__'].value=eval(tokens[4])
            if len(tokens) > 10 and tokens[4] == "time" and tokens[9] == "nodes":
                results.solver.statistics.branch_and_bound.number_of_created_subproblems=eval(tokens[8])
                results.solver.statistics.branch_and_bound.number_of_bounded_subproblems=eval(tokens[8])
                if eval(results.solver.statistics.branch_and_bound.number_of_bounded_subproblems) > 0:
                    soln.objective['__default_objective__'].value=eval(tokens[6])
            if len(tokens) == 5 and tokens[1] == "Exiting" and tokens[4] == "time":
                soln.status = SolutionStatus.stoppedByLimit
            if len(tokens) > 8 and tokens[7] == "nodes":
                results.solver.statistics.branch_and_bound.number_of_created_subproblems=eval(tokens[6])
                results.solver.statistics.branch_and_bound.number_of_bounded_subproblems=eval(tokens[6])
            if len(tokens) == 2 and tokens[0] == "sys":
                results.solver.system_time=eval(tokens[1])
            if len(tokens) == 2 and tokens[0] == "user":
                results.solver.user_time=eval(tokens[1])
            results.solver.user_time=-1.0

        if soln.objective['__default_objective__'].value == "1e+50":
            if results.problem.sense == ProblemSense.minimize:
                soln.objective['__default_objective__'].value=float('inf')
            else:
                soln.objective['__default_objective__'].value=float('-inf')
        elif results.problem.sense == ProblemSense.maximize and soln.status != SolutionStatus.infeasible:
            soln.objective['__default_objective__'].value *= -1
        if soln.status is SolutionStatus.optimal:
            soln.gap=0.0
            results.problem.lower_bound = soln.objective['__default_objective__'].value
            results.problem.upper_bound = soln.objective['__default_objective__'].value

        if soln.status == SolutionStatus.optimal:
            results.solver.termination_condition = TerminationCondition.optimal
        elif soln.status == SolutionStatus.infeasible:
            results.solver.termination_condition = TerminationCondition.infeasible

        if results.problem.name is None:
            results.problem.name = 'unknown'

        if not results.solver.status is SolverStatus.error and \
            results.solver.termination_condition in [TerminationCondition.unknown,
                        #TerminationCondition.maxIterations,
                        #TerminationCondition.minFunctionValue,
                        #TerminationCondition.minStepLength,
                        TerminationCondition.globallyOptimal,
                        TerminationCondition.locallyOptimal,
                        TerminationCondition.optimal,
                        #TerminationCondition.maxEvaluations,
                        TerminationCondition.other]:
                results.solution.insert(soln)

        return results

    def process_soln_file(self, results):

        # the only suffixes that we extract from CBC are
        # constraint duals and variable reduced-costs. scan
        # through the solver suffix list and throw an
        # exception if the user has specified any others.
        extract_duals = False
        extract_reduced_costs = False
        for suffix in self.suffixes:
            flag=False
            if re.match(suffix, "dual"):
                extract_duals = True
                flag=True
            if re.match(suffix, "rc"):
                extract_reduced_costs = True
                flag=True
            if not flag:
                raise RuntimeError,"***CBC solver plugin cannot extract solution suffix="+suffix

        # if dealing with SOL format files, we've already read
        # this via the base class reader functionality.
        if self._results_format is ResultsFormat.sol:
            return

        # otherwise, go with the native CBC solution format.
        if len(results.solution) > 0:
            solution = results.solution(0)
        if results.solver.termination_condition is TerminationCondition.infeasible:
            # NOTE: CBC _does_ print a solution file.  However, I'm not
            # sure how to interpret it yet.
            return
        results.problem.number_of_objectives=1

        processing_constraints = None # None means header, True means constraints, False means variables.
        header_processed = False
        INPUT = open(self.soln_file,"r")
        for line in INPUT:
            tokens = re.split('[ \t]+',line.strip())
            # these are the only header entries CBC will generate (identified via browsing CbcSolver.cpp)

            if tokens[0] == "Optimal":
                solution.status = SolutionStatus.optimal
                solution.gap = 0.0
                solution.objective['__default_objective__'].value = eval(tokens[-1])
                if results.problem.sense == ProblemSense.maximize:
                    solution.objective['__default_objective__'].value *= -1

            elif tokens[0] == "Unbounded" or (len(tokens)>2 and tokens[0] == "Problem" and tokens[2] == 'unbounded') or (len(tokens)>1 and tokens[0] ==    'Dual' and tokens[1] == 'infeasible'):
                results.solver.termination_condition = TerminationCondition.unbounded
                solution.gap = None
                results.solution.delete(0)
                INPUT.close()
                return

            elif tokens[0] == "Infeasible" or tokens[0] == 'PrimalInfeasible' or (len(tokens)>1 and tokens[0] == 'Integer' and tokens[1] == 'infeasible'):
                results.solver.termination_condition = TerminationCondition.infeasible
                solution.gap = None
                results.solution.delete(0)
                INPUT.close()
                return

            elif tokens[0] in ("Optimal", "Infeasible", "Unbounded", "Stopped", "Integer", "Status"):
                print "***WARNING: CBC plugin currently not processing solution status="+tokens[0]+" correctly. Full status line is: "+string.strip(line)

            if tokens[0] in ("Optimal", "Infeasible", "Unbounded", "Stopped", "Integer", "Status"):
                header_processed = True

            elif tokens[0] == "0": # indicates section start.
                if processing_constraints is None:
                    processing_constraints = True
                elif processing_constraints is True:
                    processing_constraints = False
                else:
                    raise RuntimeError, "CBC plugin encountered unexpected line=("+line.strip()+") in solution file="+self.soln_file+"; constraint and variable sections already processed!"

            if (processing_constraints is True) and (extract_duals is True):
                if len(tokens) == 4:
                    pass
                elif (len(tokens) == 5) and tokens[0] == "**":
                    tokens = tokens[1:]
                else:
                    raise RuntimeError, "Unexpected line format encountered in CBC solution file - line="+line

                constraint = tokens[1]
                constraint_ax = eval(tokens[2]) # CBC reports the constraint row times the solution vector - not the slack.
                constraint_dual = eval(tokens[3])
                solution.constraint[constraint].dual = constraint_dual

            elif processing_constraints is False:
                if len(tokens) == 4:
                    pass
                elif (len(tokens) == 5) and tokens[0] == "**":
                    tokens = tokens[1:]
                else:
                    raise RuntimeError, "Unexpected line format encountered in CBC solution file - line="+line

                variable_name = tokens[1]
                variable_value = eval(tokens[2])
                variable = solution.variable[variable_name] = {"Value" : variable_value, "Id" : len(solution.variable)}
                if extract_reduced_costs is True:
                    variable_reduced_cost = eval(tokens[3]) # currently ignored.
                    variable["Rc"] = variable_reduced_cost

            elif header_processed is True:
                pass

            else:
                raise RuntimeError, "CBC plugin encountered unexpected line=("+line.strip()+") in solution file="+self.soln_file+"; expecting header, but found data!"

        INPUT.close()


class MockCBC(CBCSHELL,mockmip.MockMIP):
    """A Mock CBC solver used for testing
    """

    pyutilib.component.core.alias('_mock_cbc')

    def __init__(self, **kwds):
        try:
            CBCSHELL.__init__(self,**kwds)
        except pyutilib.common.ApplicationError: #pragma:nocover
            pass                        #pragma:nocover
        mockmip.MockMIP.__init__(self,"cbc")

    def available(self, exception_flag=True):
        return CBCSHELL.available(self,exception_flag)

    def create_command_line(self,executable,problem_files):
        command = CBCSHELL.create_command_line(self,executable,problem_files)
        mockmip.MockMIP.create_command_line(self,executable,problem_files)
        return command

    def executable(self):
        return mockmip.MockMIP.executable(self)

    def _execute_command(self,cmd):
        return mockmip.MockMIP._execute_command(self,cmd)

    def _convert_problem(self,args,pformat,valid_pformats):
        if pformat in [ProblemFormat.mps, ProblemFormat.cpxlp, ProblemFormat.nl]:
            return (args, pformat, None)
        else:
            return (args, ProblemFormat.mps, None)


pyutilib.services.register_executable(name="cbc")
