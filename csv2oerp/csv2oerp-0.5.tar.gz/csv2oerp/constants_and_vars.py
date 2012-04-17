#!/usr/bin/env python
# -*- coding: utf8 -*-
##############################################################################
#
# Copyright (c) 2008 OSIELL SARL. (http://osiell.com) All Rights Reserved.
#                    Eric Flaux <contact@osiell.com>
# 
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
# 
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
# 
##############################################################################
"""
csv2oerp Constants ans variables.

"""

EXIT_OK = 0
EXIT_WARNING = 1
EXIT_ERROR = 2
EXIT_UNKNOWN = 3
LOGGER = None
STATS = {
    'importfile': None,
    'actual_line': 0,
    'line_num': 0, # Incrémenteur du nombre de line
    'errors': 0,
    'warnings': 0,
    'line_skipped': 0,
    'line_done': 0,
    'object_skipped': 0,
    'object_created': 0,
    'object_written': 0,
    'objects': {
        }
    }
FORMAT='%(asctime)-15s %(name)s[%(line_num)7s] %(levelname)-5s %(message)s'

ACTION_PATTERN = {
    'skip': 'SKIP',
    'replace': 'REPLACE',
    'ignore': 'IGNORE',
    'noupdate': 'NO_UPDATE',
    'unique': 'UNIQUE',
    'required': 'REQUIRED',
    }

NOISE = {
        u'e': (u'é', u'è', u'ê', u'ë', ),
        u'a': (      u'à', u'â', u'ä', ),
        u'i': (            u'î', u'ï', ),
        u'u': (      u'ù', u'û', u'ü', ),
        u'o': (            u'ô', u'ö', ),
        u'':  (u'--', u'_',
              u'{', u'}', u'[', u']', u'(', u')',
              u'?', u'!',
              u'#',
              u';', u'.', u',', u':',
              u'-', u'+', u'=', u'%', '*',
              u'\'s', u'\'r', u'\'n', u'\'r\'n', u'\'t',
            ),
        u'et': (u'&'),
        }

OERP = None
HOST = 'localhost'
PORT = 8069
USER = 'admin'
UID = None
PWD = 'admin'
DB = None

