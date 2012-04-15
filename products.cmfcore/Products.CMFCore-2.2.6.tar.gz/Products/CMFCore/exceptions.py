##############################################################################
#
# Copyright (c) 2003 Zope Foundation and Contributors.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
""" CMFCore product exceptions. """

from AccessControl import ModuleSecurityInfo
from AccessControl import Unauthorized as AccessControl_Unauthorized
from OFS.CopySupport import CopyError
from webdav.Lockable import ResourceLockedError
from zExceptions import BadRequest
from zExceptions import NotFound
from zExceptions import Unauthorized as zExceptions_Unauthorized


security = ModuleSecurityInfo('Products.CMFCore.exceptions')

# Use AccessControl_Unauthorized to raise Unauthorized errors and
# zExceptions_Unauthorized to catch them all.

security.declarePublic('AccessControl_Unauthorized')
security.declarePublic('BadRequest')
security.declarePublic('CopyError')
security.declarePublic('NotFound')
security.declarePublic('ResourceLockedError')
security.declarePublic('zExceptions_Unauthorized')


security.declarePublic('SkinPathError')
class SkinPathError(Exception):
    """ Invalid skin path error.
    """
