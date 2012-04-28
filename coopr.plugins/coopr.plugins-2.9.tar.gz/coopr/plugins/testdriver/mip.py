#  _________________________________________________________________________
#
#  Coopr: A COmmon Optimization Python Repository
#  Copyright (c) 2008 Sandia Corporation.
#  This software is distributed under the BSD License.
#  Under the terms of Contract DE-AC04-94AL85000 with Sandia Corporation,
#  the U.S. Government retains certain rights in this software.
#  For more information, see the Coopr README.txt file.
#  _________________________________________________________________________

import os
import os.path
import pyutilib.autotest
import coopr.opt
from pyutilib.component.core import *
import pyutilib.services
from pyutilib.misc import Options

class CooprMIPTestDriver(Plugin):

    implements(pyutilib.autotest.ITestDriver)
    alias('coopr.mip')

    def setUpClass(self, cls, options):
        try:
            cls.pico_convert =  pyutilib.services.registered_executable("pico_convert")
            cls.pico_convert_available= (not cls.pico_convert is None)
        except pyutilib.common.ApplicationError:
            cls.pico_convert_available=False

    def tearDownClass(self, cls, options):
        pass

    def setUp(self, testcase, options):
        global tmpdir
        tmpdir = os.getcwd()
        os.chdir(options.currdir)
        pyutilib.services.TempfileManager.sequential_files(0)
        pyutilib.services.TempfileManager.tempdir = options.currdir
        #
        if ':' in options.solver:
            solver, sub_solver = options.solver.split(':')
            if options.solver_options is None:
                _options = Options()
            else:
                _options = options.solver_options
            _options.solver = sub_solver
            testcase.opt = coopr.opt.SolverFactory(solver, options=_options)
        else:
            testcase.opt = coopr.opt.SolverFactory(options.solver, options=options.solver_options)
        if testcase.opt is None or not testcase.opt.available(False):
            testcase.skipTest('Solver %s is not available' % options.solver)
        else:
            testcase.opt.suffixes = ['.*']

    def tearDown(self, testcase, options):
        global tmpdir
        pyutilib.services.TempfileManager.clear_tempfiles()
        os.chdir(tmpdir)
        pyutilib.services.TempfileManager.unique_files()

    def run_test(self, testcase, name, options):
        # TODO dirty hack for broken GLPK MIP solve - more elegant solution?
        if 'glpk_test1' in name:
            import subprocess
            try:
                p = subprocess.Popen(['glpsol', '--version'], stdout=subprocess.PIPE)
                stdoutdata, stderrdata = p.communicate()
                vstr = stdoutdata.split("\n")[0].split(" ")[-1]
                if vstr == '4.40':
                    testcase.skipTest("Bug in GLPK 4.40 for MIP solving on this test case")
            except OSError:
                pass # Couldn't find glpsol; ignore, since we're (probably) using mock glpk
        if options.verbose or options.debug:
            print "Test %s - Running coopr.opt solver with %s" % (name, str(options))
        if not options.use_pico_convert or (options.use_pico_convert and testcase.pico_convert_available):
            try:
                if options.results_format:
                    if options.verbose or options.debug:
                        print "Running with results format %s" % options.results_format
                    results = testcase.opt.solve(options.currdir+options.files, rformat=coopr.opt.ResultsFormat(options.results_format), logfile=options.currdir+name+".log")
                else:
                    if options.verbose or options.debug:
                        print "Running with default results format"
                    results = testcase.opt.solve(options.currdir+options.files, logfile=options.currdir+name+".log")
                    if options.verbose or options.debug:
                        print "-----------------------------------------------------------------"
                        print "Results: %s" % results
                        print "-----------------------------------------------------------------"
            except coopr.opt.ConverterError:
                testcase.skipTest('Cannot convert problem files: %s' % options.files)
            baseline = pyutilib.misc.load_json( pyutilib.misc.extract_subtext( options.baseline ) )
            if options.tolerance is None:
                tol = 1e-7
            else:
                tol = options.tolerance
            pyutilib.misc.compare_json_repn( baseline, results.json_repn(), tolerance=tol, exact=False)
        else:
            try:
                if options.results_format:
                    results = testcase.opt.solve(options.currdir+options.files, rformat=coopr.opt.ResultsFormat(options.results_format), logfile=options.currdir+name+".log")
                else:
                    results = testcase.opt.solve(options.currdir+options.files, logfile=options.currdir+name+".log")
            except coopr.opt.ConverterError:
                testcase.skipTest('Cannot convert problem files: %s' % options.files)
        if (os.path.exists(options.currdir+name+".log") is True) and (not options.debug):
            os.remove(options.currdir+name+".log")
        else:
            print "Solver log file saved in %s" % options.currdir+name+".log"
