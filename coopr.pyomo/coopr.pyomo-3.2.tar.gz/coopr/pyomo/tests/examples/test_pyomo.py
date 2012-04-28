#
# Test the Pyomo command-line interface
#

import unittest
import os
import sys
from os.path import abspath, dirname
currdir = dirname(abspath(__file__))+os.sep
scriptdir = dirname(dirname(dirname(dirname(dirname(abspath(__file__))))))+os.sep

import coopr.pyomo
import pyutilib.services
import pyutilib.subprocess
import pyutilib.th as unittest
import coopr.pyomo.scripting.pyomo as main
import StringIO
from pyutilib.misc import setup_redirect, reset_redirect
import re

if os.path.exists(sys.exec_prefix+os.sep+'bin'+os.sep+'coverage'):
    executable=sys.exec_prefix+os.sep+'bin'+os.sep+'coverage -x '
else:
    executable=sys.executable

def filter_fn(line):
    return line.startswith('Disjunct') or line.startswith('DEPRECATION')


class Test(unittest.TestCase):

    def pyomo(self, cmd, **kwds):
        args=re.split('[ ]+',cmd)
        if 'root' in kwds:
            OUTPUT=kwds['root']+'.out'
            results=kwds['root']+'.jsn'
            self.ofile = OUTPUT
        else:
            OUTPUT=StringIO.StringIO()
            results='results.jsn'
        setup_redirect(OUTPUT)
        os.chdir(currdir)
        output = main.run(['--json', '--save-results=%s' % results] + list(args))
        reset_redirect()
        if not 'root' in kwds:
            return OUTPUT.getvalue()
        return output

    def setUp(self):
        self.ofile = None

    def tearDown(self):
        return
        if self.ofile and os.path.exists(self.ofile):
            return
            os.remove(self.ofile)
        if os.path.exists(currdir+'results.jsn'):
            return
            os.remove(currdir+'results.jsn')

    def run_pyomo(self, cmd, root=None):
        return pyutilib.subprocess.run('pyomo --json --save-results=%s.jsn ' % (root) +cmd, outfile=root+'.out')

    def test1(self):
        """Simple execution of 'pyomo'"""
        self.pyomo('pmedian.py pmedian.dat', root=currdir+'test1')
        self.assertMatchesJsonBaseline(currdir+"test1.jsn", currdir+"test1.txt")

    def test1a(self):
        """Simple execution of 'pyomo'"""
        self.run_pyomo('pmedian.py pmedian.dat', root=currdir+'test1a')
        self.assertMatchesJsonBaseline(currdir+"test1a.jsn", currdir+"test1.txt")

    def test2(self):
        """Run pyomo with bad --model-name option value"""
        self.pyomo('--model-name=dummy pmedian.py pmedian.dat', root=currdir+'test2')
        def filter(line):
            return line.startswith('[') or line.startswith('DEPRECATION')
        self.assertFileEqualsBaseline(currdir+"test2.out", currdir+"test2.txt", filter=filter)

    def test3(self):
        """Run pyomo with model that does not define model object"""
        self.pyomo('pmedian1.py pmedian.dat', root=currdir+'test3')
        def filter(line):
            return line.startswith('[') or line.startswith('DEPRECATION')
        self.assertFileEqualsBaseline(currdir+"test3.out", currdir+"test3.txt", filter=filter)

    def test4(self):
        """Run pyomo with good --model-name option value"""
        self.run_pyomo('-k -l --model-name=MODEL pmedian1.py pmedian.dat', root=currdir+'test4')
        self.assertMatchesJsonBaseline(currdir+"test4.jsn", currdir+"test1.txt")

    def test5(self):
        """Run pyomo with create_model function"""
        self.pyomo('pmedian2.py pmedian.dat', root=currdir+'test5')
        def filter(line):
            return line.startswith("Writingmodel") or line.startswith("Solverresultsfile") or \
                   line.startswith('[') or line.startswith('DEPRECATION')
        self.assertFileEqualsBaseline(currdir+"test5.out", currdir+"test5.txt", filter=filter)
        os.remove(currdir+'test5.jsn')

    def test6(self):
        """Run pyomo with help-components option"""
        self.pyomo('--help-components', root=currdir+'test6')
        self.assertFileEqualsBaseline(currdir+"test6.out", currdir+"test6.txt", filter=filter_fn)

    def Xtest7(self):
        """Run pyomo with help option"""
        self.pyomo('--help', root=currdir+'test7')
        self.assertMatchesJsonBaseline(currdir+"test7.jsn", currdir+"test7.txt")

    def test8(self):
        """Run pyomo with --instance-only option"""
        output = self.pyomo('--instance-only pmedian.py pmedian.dat', root=currdir+'test8')
        self.assertEqual(type(output.instance), coopr.pyomo.AbstractModel)
        # Check that the results file was NOT created
        self.assertRaises(OSError, lambda: os.remove(currdir+'test8.jsn'))

    def test9(self):
        """Run pyomo with --disable-gc option"""
        output = self.pyomo('--disable-gc pmedian.py pmedian.dat', root=currdir+'test9')
        self.assertEqual(type(output.instance), coopr.pyomo.AbstractModel)
        os.remove(currdir+'test9.jsn')

    def Xtest10(self):
        """Run pyomo with --verbose option"""
        def filter(line):
            return line.startswith("Writingmodel") or line.startswith("Solverresultsfile") or \
                   line.startswith('DEBUG:') or line.startswith('INFO:') or \
                   line.startswith('[') or line.endswith('cpxlp') or line.startswith('DEPRECATION') or \
                    line.startswith('WARNING')
        self.pyomo('-v pmedian.py pmedian.dat', root=currdir+'test10')
        self.assertFileEqualsBaseline(currdir+"test10.out", currdir+"test10.txt", filter)
        os.remove(currdir+'test10.jsn')

    def Xtest11(self):
        """Run pyomo with --debug=generate option"""
        self.pyomo('--debug=generate pmedian.py pmedian.dat', root=currdir+'test11')
        self.assertFileEqualsBaseline(currdir+"test11.jsn", currdir+"test11.txt")

    def test12(self):
        """Run pyomo with --output option"""
        def filter(line):
            #print "HERE",line
            return line.startswith("Writing") or line.startswith('DEPRECATION')
        self.pyomo('--output=%s pmedian.py pmedian.dat' % (currdir+'test12.log'), root=currdir+'test12')
        self.assertMatchesJsonBaseline(currdir+"test12.jsn", currdir+"test12.txt")
        os.remove(currdir+'test12.log')

    def test13(self):
        """Simple execution of 'pyomo' with implicit rules"""
        self.pyomo('pmedian3.py pmedian.dat', root=currdir+'test13')
        self.assertMatchesJsonBaseline(currdir+"test13.jsn", currdir+"test1.txt")

    def test14(self):
        """Simple execution of 'pyomo' with a concrete model and constraint lists"""
        self.pyomo('pmedian4.py', root=currdir+'test14')
        self.assertMatchesJsonBaseline(currdir+"test14.jsn", currdir+"test14.txt")


Test = unittest.skipIf(pyutilib.services.registered_executable("glpsol") is None, "The 'glpsol' executable is not available")(Test)

if __name__ == "__main__":
    unittest.main()
