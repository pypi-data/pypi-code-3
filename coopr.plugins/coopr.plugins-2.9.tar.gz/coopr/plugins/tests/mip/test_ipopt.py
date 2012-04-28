#
# Unit Tests for coopr.plugins.solvers.ASL
#
#

import os
import sys
import fileinput
import subprocess
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
from coopr.pyomo import *

try:
    ipopt = coopr.plugins.solvers.ASL(keepFiles=True, options={'solver':'ipopt'})
    if (ipopt.executable() is not None) and (ipopt.available(False) is True):
        ipopt_available = True
    else:
        ipopt_available = False
except pyutilib.common.ApplicationError:
    ipopt_available=False

class test_ipopt(unittest.TestCase):

    def setUp(self):
        self.do_setup()

    def do_setup(self):
        global tmpdir
        tmpdir = os.getcwd()
        os.chdir(currdir)
        pyutilib.services.TempfileManager.sequential_files(0)
        pyutilib.services.TempfileManager.tempdir = currdir

        self.asl = coopr.plugins.solvers.ASL(keepFiles=True, options={'solver':'ipopt'})
        self.asl.suffixes=['.*']

        ver = subprocess.Popen(['ipopt','-v'],stdout=subprocess.PIPE).communicate()[0].split()[1]
        if ver != '3.9.3':
            for line in fileinput.input(currdir+"test_solve_from_nl.baseline",inplace=1):
                    print line.replace('3.9.3',ver)
            for line in fileinput.input(currdir+"test_solve_from_instance.baseline",inplace=1):
                    print line.replace('3.9.3',ver)

        # The sisser CUTEr instance
        # Formulated in Pyomo by Carl D. Laird, Daniel P. Word, Brandon C. Barrera and Saumyajyoti Chaudhuri
        # Taken from:

        # AMPL Model by Hande Y. Benson
        #
        # Copyright (C) 2001 Princeton University
        # All Rights Reserved
        #
        # Permission to use, copy, modify, and distribute this software and
        # its documentation for any purpose and without fee is hereby
        # granted, provided that the above copyright notice appear in all
        # copies and that the copyright notice and this
        # permission notice appear in all supporting documentation.

        #   Source:
        #   F.S. Sisser,
        #   "Elimination of bounds in optimization problems by transforming
        #   variables",
        #   Mathematical Programming 20:110-121, 1981.

        #   See also Buckley#216 (p. 91)

        #   SIF input: Ph. Toint, Dec 1989.

        #   classification OUR2-AN-2-0

        sisser_instance = ConcreteModel()

        sisser_instance.N = RangeSet(1,2)
        sisser_instance.xinit = Param(sisser_instance.N, initialize={ 1 : 1.0, 2 : 0.1})

        def fa(model, i):
            return value(model.xinit[i])
        sisser_instance.x = Var(sisser_instance.N,initialize=fa)

        def f(model):
            return 3*model.x[1]**4 - 2*(model.x[1]*model.x[2])**2 + 3*model.x[2]**4
        sisser_instance.f = Objective(rule=f,sense=minimize)

        # need to flag variables as used!!!
        sisser_instance.preprocess()

        self.sisser_instance = sisser_instance

    def tearDown(self):
        global tmpdir
        pyutilib.services.TempfileManager.clear_tempfiles()
        os.chdir(tmpdir)
        pyutilib.services.TempfileManager.unique_files()

    @unittest.skipIf(not ipopt_available, "The 'ipopt' executable is not available")
    def test_solve_from_nl(self):
        """ Test ipopt solve from nl file """
        results = self.asl.solve(currdir+"sisser.pyomo.nl", logfile=currdir+"test_solve_from_nl.log")
        results.write(filename=currdir+"test_solve_from_nl.txt", times=False, format='json')
        self.assertMatchesJsonBaseline(currdir+"test_solve_from_nl.txt", currdir+"test_solve_from_nl.baseline", tolerance=1e-7)

    @unittest.skipIf(not ipopt_available, "The 'ipopt' executable is not available")
    def test_solve_from_instance(self):
        """ Test ipopt solve from a pyomo instance and load the solution """
        results = self.asl.solve(self.sisser_instance)
        results.write(filename=currdir+"test_solve_from_instance.txt", times=False, format='json')
        self.assertMatchesJsonBaseline(currdir+"test_solve_from_instance.txt", currdir+"test_solve_from_instance.baseline", tolerance=1e-7)
        self.sisser_instance.load(results)

if __name__ == "__main__":
    unittest.main()
