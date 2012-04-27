#  _________________________________________________________________________
#
#  PyUtilib: A Python utility library.
#  Copyright (c) 2008 Sandia Corporation.
#  This software is distributed under the BSD License.
#  Under the terms of Contract DE-AC04-94AL85000 with Sandia Corporation,
#  the U.S. Government retains certain rights in this software.
#  _________________________________________________________________________

"""
Setup for PyUtilib package
"""

import os
from setuptools import setup


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


setup(name="PyUtilib",
    version='4.0.2807',
    maintainer='William E. Hart',
    maintainer_email='wehart@sandia.gov',
    url = 'https://software.sandia.gov/trac/pyutilib',
    license = 'BSD',
    platforms = ["any"],
    description = 'PyUtilib: A collection of Python utilities',
    long_description = read('README.txt'),
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Unix Shell',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Software Development :: Libraries :: Python Modules'],
      packages=['pyutilib'],
      keywords=['utility'],
      namespace_packages=['pyutilib'],
      install_requires=[
            'pyutilib.autotest>=2.0',
            'pyutilib.common>=3.0.7',
            'pyutilib.component.app>=3.2', 
            'pyutilib.component.config>=3.4',
            'pyutilib.component.core>=4.5.1',
            'pyutilib.component.doc>=1.0.1',
            'pyutilib.component.executables>=3.5',
            'pyutilib.component.loader>=3.4',
            'pyutilib.dev>=2.0',
            'pyutilib.enum>=1.1',
            'pyutilib.excel>=3.1',
            'pyutilib.math>=3.3',
            'pyutilib.misc>=5.3.1',
            'pyutilib.ply>=3.0.6',
            'pyutilib.pyro>=3.5',
            'pyutilib.R>=3.1',
            'pyutilib.services>=3.4',
            'pyutilib.subprocess>=3.5.1',
            'pyutilib.svn>=1.3',
            'pyutilib.th>=5.3',
            'pyutilib.virtualenv>=3.0',
            'pyutilib.workflow>=3.2',
            'argparse',
            'nose',
            'unittest2'
      ]
      )

