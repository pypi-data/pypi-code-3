import sys
import os
from os.path import abspath, dirname
sys.path.insert(0, dirname(dirname(dirname(abspath(__file__))))+os.sep+"coopr")
sys.path.append(".."+os.sep+"..")

from distutils.core import setup
import py2exe

setup(console=['../../bin/pysos'])
