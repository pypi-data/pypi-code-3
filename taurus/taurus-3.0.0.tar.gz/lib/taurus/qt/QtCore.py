#!/usr/bin/env python

#############################################################################
##
## This file is part of Taurus, a Tango User Interface Library
## 
## http://www.tango-controls.org/static/taurus/latest/doc/html/index.html
##
## Copyright 2011 CELLS / ALBA Synchrotron, Bellaterra, Spain
## 
## Taurus is free software: you can redistribute it and/or modify
## it under the terms of the GNU Lesser General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
## 
## Taurus is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU Lesser General Public License for more details.
## 
## You should have received a copy of the GNU Lesser General Public License
## along with Taurus.  If not, see <http://www.gnu.org/licenses/>.
##
#############################################################################

"""This module exposes PyQt4.QtCore module"""

from taurusqtoptions import QT_API, QT_API_PYQT, QT_API_PYSIDE

# Now peform the imports.
if QT_API == QT_API_PYQT:
    from PyQt4 import QtCore as __QtCore
    from PyQt4.QtCore import *

    # Alias PyQt-specific functions for PySide compatibility.
    if hasattr(__QtCore, "pyqtSignal"):
        Signal = pyqtSignal
    if hasattr(__QtCore, "pyqtSlot"):
        Slot = pyqtSlot
    if hasattr(__QtCore, "pyqtProperty"):
        Property = pyqtProperty
    __version__ = QT_VERSION_STR
elif QT_API == QT_API_PYSIDE:
    from PySide.QtCore import *