# -*- coding: utf-8 -*-
#
# File: CMFPlomino.py
#
# Copyright (c) 2008 by ['Eric BREHAULT']
# Generator: ArchGenXML Version 2.0
#            http://plone.org/products/archgenxml
#
# Zope Public License (ZPL)
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL). A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

__author__ = """Eric BREHAULT <eric.brehault@makina-corpus.org>"""
__docformat__ = 'plaintext'


# There are three ways to inject custom code here:
#
#   - To set global configuration variables, create a file AppConfig.py.
#       This will be imported in config.py, which in turn is imported in
#       each generated class and in this file.
#   - To perform custom initialisation after types have been registered,
#       use the protected code section at the bottom of initialize().

import logging
logger = logging.getLogger('CMFPlomino')
logger.debug('Installing Product')

import os
import os.path
from Products.Archetypes import listTypes
from Products.Archetypes.atapi import *
from Products.Archetypes.utils import capitalize
from Products.CMFCore import DirectoryView
from Products.CMFCore import permissions as cmfpermissions
from Products.CMFCore import utils as cmfutils
from Products.CMFPlone.utils import ToolInit
from config import *

DirectoryView.registerDirectory('skins', product_globals)

from AccessControl.Permission import registerPermissions
from Products.PythonScripts.Utility import allow_module
from zope import component
import interfaces
from zope.interface import implements

class isPlomino(object):

    def __call__(self):
        return hasattr(self.context, 'getParentDatabase')

class isDesignMode(object):

    def __call__(self):
        if not hasattr(self.context, 'getParentDatabase'):
            return False
        return self.context.hasDesignPermission()

class PlominoCoreUtils:
    implements(interfaces.IPlominoUtils)
    
    module = "Products.CMFPlomino.PlominoUtils"
    methods = ['DateToString',
               'StringToDate',
               'DateRange',
               'sendMail',
               'userFullname',
               'userInfo',
               'htmlencode',
               'Now',
               'asList',
               'urlencode',
               'csv_to_array',
               'MissingValue',
               'open_url',
               'asUnicode',
               'array_to_csv',
               'isDocument',
               'cgi_escape',
               'json_dumps',
               'json_loads']

component.provideUtility(PlominoCoreUtils, interfaces.IPlominoUtils)

def get_utils():
    utils = {}
    for plugin_utils in component.getUtilitiesFor(interfaces.IPlominoUtils):
        module = plugin_utils[1].module
        utils[module] = plugin_utils[1].methods
    return utils

allow_module("Products.CMFPlomino.PlominoUtils")

def initialize(context):
    """initialize product (called by zope)"""
    ##code-section custom-init-top #fill in your manual code here
    registerPermissions([(ADD_DESIGN_PERMISSION, []),
                         (ADD_CONTENT_PERMISSION, []),
                         (READ_PERMISSION, []),
                         (EDIT_PERMISSION, []),
                         (CREATE_PERMISSION, []),
                         (REMOVE_PERMISSION, []),
                         (DESIGN_PERMISSION, []),
                         (ACL_PERMISSION, [])])
    ##/code-section custom-init-top

    # imports packages and types for registration

    import PlominoDatabase
    import PlominoAction
    import PlominoForm
    import PlominoField
    import PlominoView
    import PlominoColumn
    import PlominoDocument
    import PlominoHidewhen
    import PlominoAgent
    import PlominoCache
    from PlominoDocument import addPlominoDocument

    # Initialize portal content
    all_content_types, all_constructors, all_ftis = process_types(
        listTypes(PROJECTNAME),
        PROJECTNAME)
    
    all_content_types += (PlominoDocument.PlominoDocument,)
    all_constructors += (addPlominoDocument,)
    all_ftis += ({
                'meta_type': 'PlominoDocument',
                'allowed_content_types':[],
                'allow_discussion': 0,
                'immediate_view':'checkBeforeOpenDocument',
                'global_allow':0,
                'filter_content_types':1,
                },)
#EXAMPLE: {'factory': 'addPlominoAction', 'product': 'CMFPlomino', 'immediate_view': 'base_edit', 'content_icon': 'document_icon.gif', 'global_allow': True, 'filter_content_types': False, 'actions': ({'action': <Products.CMFCore.Expression.Expression object at 0x6bee8c0>, 'title': 'View', 'id': 'view', 'permissions': ('View',)}, {'action': <Products.CMFCore.Expression.Expression object at 0x6bee758>, 'title': 'Edit', 'id': 'edit', 'condition': <Products.CMFCore.Expression.Expression object at 0x6e247d0>, 'permissions': ('Modify portal content',)}, {'action': <Products.CMFCore.Expression.Expression object at 0x6d9dd70>, 'title': 'Properties', 'id': 'metadata', 'permissions': ('Modify portal content',)}), 'fti_meta_type': 'Factory-based Type Information with dynamic views', 'default_view': 'base_view', 'meta_type': 'PlominoAction', 'allow_discussion': False, 'view_methods': ('base_view',), 'aliases': {'sharing': 'folder_localrole_form', 'gethtml': '', '(Default)': '(dynamic view)', 'edit': 'base_edit', 'mkdir': '', 'properties': 'base_metadata', 'view': '(selected layout)'}, 'id': 'PlominoAction', 'description': '\n    '}

    cmfutils.ContentInit(
        PROJECTNAME + ' Content',
        content_types      = all_content_types,
        permission         = DEFAULT_ADD_CONTENT_PERMISSION,
        extra_constructors = all_constructors,
        fti                = all_ftis,
        ).initialize(context)
    
    # Give it some extra permissions to control them on a per class limit
    for i in range(0,len(all_content_types)):
        klassname=all_content_types[i].__name__
        if not klassname in ADD_CONTENT_PERMISSIONS:
            continue

        context.registerClass(meta_type   = all_ftis[i]['meta_type'],
                              constructors= (all_constructors[i],),
                              permission  = ADD_CONTENT_PERMISSIONS[klassname])

