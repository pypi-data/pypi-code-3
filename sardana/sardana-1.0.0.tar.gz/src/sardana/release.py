#!/usr/bin/env python
# -*- coding: utf-8 -*-

##############################################################################
##
## This file is part of Sardana
## 
## http://www.tango-controls.org/static/sardana/latest/doc/html/index.html
##
## Copyright 2011 CELLS / ALBA Synchrotron, Bellaterra, Spain
## 
## Sardana is free software: you can redistribute it and/or modify
## it under the terms of the GNU Lesser General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
## 
## Sardana is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU Lesser General Public License for more details.
## 
## You should have received a copy of the GNU Lesser General Public License
## along with Sardana.  If not, see <http://www.gnu.org/licenses/>.
##
##############################################################################

__docformat__ = "restructuredtext"

"""
Release data for the taurus project. It contains the following members:

    - version : (str) version string
    - description : (str) brief description
    - long_description : (str) a long description
    - license : (str) license
    - authors : (dict<str, tuple<str,str>>) the list of authors
    - url : (str) the project url
    - download_url : (str) the project download url
    - platforms : list<str> list of supported platforms
    - keywords : list<str> list of keywords
"""

#: Name of the package for release purposes.  This is the name which labels
#: the tarballs and RPMs made by distutils, so it's best to lowercase it.
name = 'sardana'

#: For versions with substrings (like 0.6.16.svn), use an extra . to separate
#: the new substring. We have to avoid using either dashes or underscores,
#: because bdist_rpm does not accept dashes (an RPM) convention, and
#: bdist_deb does not accept underscores (a Debian convention).
version_info = (1,0,0,'final', '$Rev$')
version = '.'.join(map(str, version_info[:3]))

#: svn revision number
revision = str(version_info[4])

description = "Sardana is a generic program for control applications in large and small installations"

long_description = """Produce a modular, high performance, robust and generic user environment 
for control applications in large and small installations. 
Make Sardana the generic user environment distributed in the TANGO project 
and the standard basis of collaborations in control."""

license = 'LGPL'

authors = {'Tiago'          : ('Tiago Coutinho','tcoutinho@cells.es') }

url = 'http://packages.python.org/sardana'

download_url = 'http://pypi.python.org/packages/source/s/sardana'

platforms = ['Linux','Windows XP/2000/NT','Windows 95/98/ME']

keywords = ['Sardana', 'Tango', 'Python', 'Control System']
