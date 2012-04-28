#
# Unit Tests for coopr.plugins.solvers.ASL
#
#

import os
import sys
from os.path import abspath, dirname
sys.path.insert(0, dirname(dirname(abspath(__file__)))+"/../..")
cooprdir = dirname(abspath(__file__))+os.sep+".."+os.sep+".."+os.sep
currdir = dirname(abspath(__file__))+os.sep

from nose.tools import nottest
import pyutilib.th as unittest
import pyutilib.services
import pyutilib.common
import coopr.plugins.solvers
import coopr.opt
import coopr
import xml
from coopr.opt import ResultsFormat, ProblemFormat, ConverterError

pyutilib.services.register_executable('cplexamp')
coopr.opt.SolverResults.default_print_options.ignore_time = True
try:
    cplex = coopr.plugins.solvers.CPLEX(keepFiles=True)
    cplex_available = (not cplex.executable() is None) and cplex.available(False)
    asl = coopr.plugins.solvers.ASL(keepFiles=True, options={'solver':'cplexamp'})
    cplexamp_available= cplex_available and (not asl.executable() is None) and asl.available(False)
except pyutilib.common.ApplicationError:
    cplexamp_available=False

try:
    pico_convert =  pyutilib.services.registered_executable("pico_convert")
    pico_convert_available= (not pico_convert is None)
except pyutilib.common.ApplicationError:
    pico_convert_available=False


def filter_cplex(line):
    return line.startswith("Message:")

class mock_all(unittest.TestCase):

    def setUp(self):
        self.do_setup(False)

    def do_setup(self,flag):
        global tmpdir
        tmpdir = os.getcwd()
        os.chdir(currdir)
        pyutilib.services.TempfileManager.sequential_files(0)
        pyutilib.services.TempfileManager.tempdir = currdir
        if flag:
            self.asl = coopr.plugins.solvers.ASL(keepFiles=True, options={'solver':'cplexamp'})
        else:
            self.asl = coopr.plugins.solvers.MockASL(keepFiles=True, options={'solver':'cplexamp'})
        self.asl.suffixes=['.*']

    def tearDown(self):
        global tmpdir
        pyutilib.services.TempfileManager.clear_tempfiles()
        os.chdir(tmpdir)
        pyutilib.services.TempfileManager.unique_files()

    def test_path(self):
        """ Verify that the ASL path is what is expected """
        if type(self.asl) is 'ASL':
            self.assertEqual(self.asl.executable.split(os.sep)[-1],"ASL"+coopr.util.executable_extension)

    def Xtest_solve1(self):
        """ Test ASL - test1.mps """
        results = self.asl.solve(currdir+"test1.mps", logfile=currdir+"test_solve1.log")
        results.write(filename=currdir+"test_solve1.txt", times=False, format='json')
        self.assertMatchesJsonBaseline(currdir+"test_solve1.txt", currdir+"test1_asl.txt")
        #os.remove(currdir+"test_solve1.log")

    def Xtest_solve2a(self):
        """ Test ASL - test1.mps """
        results = self.asl.solve(currdir+"test1.mps", rformat=ResultsFormat.soln, logfile=currdir+"test_solve2a.log")
        results.write(filename=currdir+"test_solve2a.txt", times=False, format='json')
        self.assertMatchesJsonBaseline(currdir+"test_solve2a.txt", currdir+"test1_asl.txt")
        #os.remove(currdir+"test_solve2a.log")

    def Xtest_solve2b(self):
        """ Test ASL - test1.mps """
        results = self.asl.solve(currdir+"test1.mps", pformat=ProblemFormat.mps, rformat=ResultsFormat.soln, logfile=currdir+"test_solve2b.log")
        results.write(filename=currdir+"test_solve2b.txt", times=False, format='json')
        self.assertMatchesJsonBaseline(currdir+"test_solve2b.txt", currdir+"test1_asl.txt")
        #os.remove(currdir+"test_solve2b.log")

    def Xtest_solve3(self):
        """ Test ASL - test2.lp """
        results = self.asl.solve(currdir+"test2.lp", logfile=currdir+"test_solve3.log", keepFiles=True)
        results.write(filename=currdir+"test_solve3.txt", times=False, format='json')
        self.assertMatchesJsonBaseline(currdir+"test_solve3.txt", currdir+"test2_asl.txt")
        if os.path.exists(currdir+"test2.solution.dat"):
            os.remove(currdir+"test2.solution.dat")
        #os.remove(currdir+"test_solve3.log")

    def test_solve4(self):
        """ Test ASL - test4.nl """
        if pico_convert_available:
            results = self.asl.solve(currdir+"test4.nl", logfile=currdir+"test_solve4.log")
            results.write(filename=currdir+"test_solve4.txt", times=False, format='json')
            self.assertMatchesJsonBaseline(currdir+"test_solve4.txt", currdir+"test4_asl.txt", tolerance=1e-4)
        else:
            try:
                results = self.asl.solve(currdir+"test4.nl", logfile=currdir+"test_solve4.log")
            except ConverterError:
                return
        #os.remove(currdir+"test4.sol")
        #os.remove(currdir+"test_solve4.log")

    #
    # This test is disabled, but it's useful for interactively exercising
    # the option specifications of a solver
    #
    def Xtest_options(self):
        """ Test ASL options behavior """
        results = self.asl.solve(currdir+"bell3a.mps", logfile=currdir+"test_options.log", options="sec=0.1 foo=1 bar='a=b c=d' xx_zz=yy")
        results.write(filename=currdir+"test_options.txt",times=False)
        self.assertFileEqualsBaseline(currdir+"test_options.txt", currdir+  "test4_asl.txt")
        #os.remove(currdir+"test4.sol")
        #os.remove(currdir+"test_solve4.log")

    def Xtest_mock5(self):
        """ Mock Test ASL - test5.mps """
        if cplexamp_available:
            pass
        results = self.asl.solve(currdir+"test4.nl", logfile=currdir+"test_solve5.log", keepfiles=True)
        results.write(filename=currdir+"test_mock5.txt",times=False)
        self.assertFileEqualsBaseline(currdir+"test_mock5.txt", currdir+"test4_asl.txt")
        os.remove(currdir+"test4.sol")
        os.remove(currdir+"test_solve5.log")

    def test_error1(self):
        """ Bad results format """
        try:
            results = self.asl.solve(currdir+"test1.mps", format=ResultsFormat.sol)
            self.fail("test_error1")
        except ValueError:
            pass

    def test_error2(self):
        """ Bad solve option """
        try:
            results = self.asl.solve(currdir+"test1.mps", foo="bar")
            self.fail("test_error2")
        except ValueError:
            pass

    def test_error3(self):
        """ Bad solve option """
        try:
            results = self.asl.solve(currdir+"bad.mps", foo="bar")
            self.fail("test_error3")
        except ValueError:
            pass


@unittest.skipIf(not cplexamp_available, "The 'cplexamp' command is not available")
class mip_all(mock_all):

    def setUp(self):
        self.do_setup(True)


if __name__ == "__main__":
    unittest.main()
