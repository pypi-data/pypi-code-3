#!/usr/bin/env python

########################################################################
##                                                                    ##
##  Copyright 2009-2012 Lucas Heitzmann Gabrielli                     ##
##                                                                    ##
##  This file is part of gdspy.                                       ##
##                                                                    ##
##  gdspy is free software: you can redistribute it and/or modify it  ##
##  under the terms of the GNU General Public License as published    ##
##  by the Free Software Foundation, either version 3 of the          ##
##  License, or any later version.                                    ##
##                                                                    ##
##  gdspy is distributed in the hope that it will be useful, but      ##
##  WITHOUT ANY WARRANTY; without even the implied warranty of        ##
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the     ##
##  GNU General Public License for more details.                      ##
##                                                                    ##
##  You should have received a copy of the GNU General Public         ##
##  License along with gdspy.  If not, see                            ##
##  <http://www.gnu.org/licenses/>.                                   ##
##                                                                    ##
########################################################################

import os
if os.sys.version_info >= (3,):
    from distutils.command.build_py import build_py_2to3 as build_py
else:
    from distutils.command.build_py import build_py
import distutils.command.build_ext

from distutils.core import setup, Extension

class my_build(distutils.command.build_ext.build_ext):
    def run(self):
        distutils.command.build_ext.build_ext.run(self)
        for p in [self.build_lib, self.build_temp]:
            f = p + os.sep + 'gdspy' + os.sep + 'boolext.py'
            if os.path.isfile(f): os.unlink(f)

setup(name='gdspy',
      version='0.3a',
      author='Lucas Heitzmann Gabrielli',
      author_email='heitzmann@gmail.com',
      license='GNU General Public License (GPL)',
      url='https://sourceforge.net/projects/gdspy/',
      description='A Python GDSII exporter',
      long_description='Module for creating GDSII stream files. It also allows the geometry created to be visualized.',
      packages = ['gdspy'],
      package_dir = {'gdspy': 'src'},
      ext_modules = [Extension('gdspy.boolext', ['src/boolext.c'])],
      zip_safe = True,
      provides=['gdspy'],
      requires=['numpy'],
      platforms='OS Independent',
      classifiers=['Development Status :: 4 - Beta',
                   'Environment :: Console',
                   'Intended Audience :: Developers',
                   'Intended Audience :: Science/Research',
                   'License :: OSI Approved :: GNU General Public License (GPL)',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Scientific/Engineering'],
      cmdclass={'build_py': build_py, 'build_ext':my_build})
