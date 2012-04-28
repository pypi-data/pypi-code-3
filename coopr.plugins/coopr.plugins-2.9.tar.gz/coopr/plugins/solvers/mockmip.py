#  _________________________________________________________________________
#
#  Coopr: A COmmon Optimization Python Repository
#  Copyright (c) 2008 Sandia Corporation.
#  This software is distributed under the BSD License.
#  Under the terms of Contract DE-AC04-94AL85000 with Sandia Corporation,
#  the U.S. Government retains certain rights in this software.
#  For more information, see the Coopr README.txt file.
#  _________________________________________________________________________


import glob
import shutil
from os.path import join, basename, dirname, exists, isfile

class MockMIP(object):
    """Methods used to create a mock MIP solver used for testing
    """

    def __init__(self, mockdir):
        self.mock_subdir=mockdir

    def create_command_line(self,executable,problem_files):
        self._mock_problem = basename(problem_files[0]).split('.')[0]
        self._mock_dir = dirname(problem_files[0])

    def executable(self):
        return "mock"

    def _execute_command(self,cmd):
        mock_basename = join(self._mock_dir, self.mock_subdir, self._mock_problem)
        if self.soln_file is not None:
            # prefer .sol over .soln
            for ext in ( 'sol', 'soln' ):
                file = glob.glob(mock_basename + "*." + ext)
                if len(file):
                    if len(file) > 1:
                        raise RuntimeError, "Multiple .%s files found" % ext
                    shutil.copyfile(file[0],self.soln_file)
                    break
        for file in glob.glob(mock_basename + "*"):
            if file.split(".")[-1] != "out":
                shutil.copyfile(file, join(self._mock_dir, basename(file)))
        log=""
        fname = mock_basename + ".out"
        if not isfile(fname):
            raise ValueError, "Missing mock data file: "+fname
        INPUT=open(mock_basename + ".out")
        for line in INPUT:
            log = log+line
        INPUT.close()
        return [0,log]
