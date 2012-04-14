#!/usr/bin/env python
import os
import glob
from distutils.core import setup

def get_dir(d):
    return glob.glob('%s/*' % d)


ldesc = """IdleX is a collection of over 20 extensions for the Python IDLE environment."""

setup(name='idlex',
      version='0.9',
      description='IDLE Extensions for Python',
      author='Roger D. Serwy',
      author_email='serwy@illinois.edu',
      url='http://idlex.sourceforge.net',
      packages=['idlexlib',
                'idlexlib.extensions'],
      package_dir = {'idlexlib': 'idlexlib'},
      data_files = [('scripts', get_dir('scripts')),
                    ],
      scripts = ['scripts/idlex'],
      license='NCSA License',
      long_description=ldesc,
      classifiers = [
          'Development Status :: 4 - Beta',
          'Framework :: IDLE',
          'Intended Audience :: Developers',
          'Intended Audience :: Education',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: University of Illinois/NCSA Open Source License',
          'License :: OSI Approved :: Python Software Foundation License',
          'Topic :: Text Editors :: Integrated Development Environments (IDE)',
          'Operating System :: OS Independent',
        ],
     )
