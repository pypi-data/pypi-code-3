import os

import pyutilib.th as unittest
from pyutilib.misc.pyyaml_util import *
import pyutilib.common
import coopr.pyomo.scripting.pyomo as pyomo
import coopr.plugins
from nose.tools import nottest

currdir = os.path.dirname(os.path.abspath(__file__))
exdir = os.path.abspath(os.path.join(currdir, '..', '..', '..', '..', '..', 'examples', 'pyomo', 'diet'))

sqlite3_available = pyodbc_available = False
try:
    import sqlite3
    sqlite3_available = True
except ImportError:
    pass
try:
    import pyodbc
    pyodbc_available = True
except ImportError:
    pass

def glpk_available():
    try:
        glpk = coopr.plugins.solvers.GLPK(keepFiles=False)
        return (not glpk.executable() is None) and glpk.available(False)
    except pyutilib.common.ApplicationError:
        return False

@unittest.skipUnless(glpk_available(), "GLPK is not installed")
class Test(unittest.TestCase):

    @nottest
    def pyomo(self, *args, **kwargs):
        """
        Run Pyomo with the given arguments. `args` should be a list with
        one argument token per string item.
        """

        if isinstance(args, str):
            args = args.split()
        args = list(map(str, args))

        outputpath = kwargs.pop('outputpath', os.path.join(exdir, 'results.jsn'))
        args = ['--json', '-c', '--quiet', '--save-results', outputpath] + args
        print "Args:", ' '.join(args)

        old_path = os.getcwd()
        os.chdir(exdir)
        output = pyomo.run(args)
        os.chdir(old_path)

        return outputpath

    def test_pyomo_dat(self):
        results_file = self.pyomo(os.path.join(exdir, 'diet1.py'), os.path.join(exdir, 'diet.dat'), outputpath=os.path.join(currdir, 'pyomo_dat.jsn'))
        baseline_file = os.path.join(currdir, 'baselines', 'diet1_pyomo_dat.jsn')
        self.assertMatchesJsonBaseline(results_file, baseline_file)

    @unittest.skipUnless(pyodbc_available, "Requires PyODBC")
    def test_pyomo_mdb(self):
        results_file = self.pyomo(os.path.join(exdir, 'diet1.py'), os.path.join(exdir, 'diet1.db.dat'), outputpath=os.path.join(currdir, 'pyomo_mdb.jsn'))
        baseline_file = os.path.join(currdir, 'baselines', 'diet1_pyomo_mdb.jsn')
        self.assertMatchesJsonBaseline(results_file, baseline_file)

    @unittest.skipUnless(pyodbc_available, "Requires PyODBC")
    def test_mdb_equality(self):
        dat_results_file = self.pyomo(os.path.join(exdir, 'diet1.py'), os.path.join(exdir, 'diet.dat'), outputpath=os.path.join(currdir, 'dat_results.jsn'))
        mdb_results_file = self.pyomo(os.path.join(exdir, 'diet1.py'), os.path.join(exdir, 'diet1.db.dat'), outputpath=os.path.join(currdir, 'mdb_results.jsn'))
        self.assertMatchesJsonBaseline(dat_results_file, mdb_results_file)
        os.remove(mdb_results_file)

    @unittest.skipUnless(sqlite3_available, "Requires SQLite3")
    def test_pyomo_sqlite3(self):
        results_file = self.pyomo(os.path.join(exdir, 'diet1.py'), os.path.join(exdir, 'diet1.sqlite.dat'), outputpath=os.path.join(currdir, 'pyomo_sqlite3.jsn'))
        baseline_file = os.path.join(currdir, 'baselines', 'diet1_pyomo_sqlite3.jsn')
        self.assertMatchesJsonBaseline(results_file, baseline_file)

    @unittest.skipUnless(sqlite3_available, "Requires SQLite3")
    def test_sqlite_equality(self):
        dat_results_file = self.pyomo(os.path.join(exdir, 'diet1.py'), os.path.join(exdir, 'diet.dat'), outputpath=os.path.join(currdir, 'dat_results.jsn'))
        sqlite_results_file = self.pyomo(os.path.join(exdir, 'diet1.py'), os.path.join(exdir, 'diet1.sqlite.dat'), outputpath=os.path.join(currdir, 'sqlite_results.jsn'))
        self.assertMatchesJsonBaseline(dat_results_file, sqlite_results_file)
        os.remove(sqlite_results_file)

if __name__ == "__main__":
    unittest.main()

