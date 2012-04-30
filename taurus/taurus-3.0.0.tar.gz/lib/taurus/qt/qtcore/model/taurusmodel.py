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

"""This module provides base taurus tree item and a base tree model"""

__all__ = ["TaurusBaseTreeItem", "TaurusBaseModel", "TaurusBaseProxyModel"]

__docformat__ = 'restructuredtext'

from taurus.qt import Qt
from taurus.core.util import Logger

class TaurusBaseTreeItem(object):
    """A generic node"""
    
    DisplayFunc = str

    def __init__(self, model, data, parent = None):
        self._model = model
        self._itemData = data
        self._parentItem = parent
        self._childItems = []
        self._depth = self._calcDepth()
        
    def itemData(self):
        """The internal itemData object
        
        :return: (object) object holding the data of this item
        """
        return self._itemData
        
    def depth(self):
        """Depth of the node in the hierarchy
        
        :return: (int) the node depth
        """
        return self._depth
    
    def appendChild(self, child):
        """Adds a new child node
        
        :param child: (TaurusTreeBaseItem) child to be added
        """
        self._childItems.append(child)
    
    def child(self, row):
        """Returns the child in the given row
        
        :return: (TaurusTreeBaseItem) the child node for the given row"""
        return self._childItems[row]
    
    def childCount(self):
        """Returns the number of childs for this node
        
        :return: (int) number of childs for this node
        """
        return len(self._childItems)
    
    def hasChildren(self):
        return len(self._childItems) > 0
    
    def data(self, index):
        """Returns the data of this node for the given index
        
        :return: (object) the data for the given index
        """
        return self._itemData[index.column()]
    
    def icon(self, index):
        return None
    
    def toolTip(self, index):
        return self.data(index)
    
    def setData(self, index, data):
        """Sets the node data
        
        :param data: (object) the data to be associated with this node
        """
        self._itemData = data
    
    def parent(self):
        """Returns the parent node or None if no parent exists
        
        :return: (TaurusTreeBaseItem) the parent node
        """
        return self._parentItem
    
    def row(self):
        """Returns the row for this node
        
        :return: (int) row number for this node
        """
        if self._parentItem is None:
            return 0
        return self._parentItem._childItems.index(self)

    def _calcDepth(self):
        d = 0
        n = self.parent()
        while n is not None:
            n = n.parent()
            d += 1
        return d
    
    def display(self):
        """Returns the display string for this node
        
        :return: (str) the node's display string"""
        if not hasattr(self, "_display"):
            if self._itemData is None:
                return None
            self._display = self.DisplayFunc(self._itemData)
        return self._display

    def qdisplay(self):
        """Returns the display QString for this node
        
        :return: (Qt.QString) the node's display string"""
        if not hasattr(self, "_qdisplay"):
            d = self.display()
            if d is None:
                return None
            self._qdisplay = Qt.QString(d)
        return self._qdisplay

    def mimeData(self, index):
        return self.data(index)

    def role(self):
        """Returns the prefered role for the item.
        This implementation returns taurus.core.TaurusElementType.Unknown
        
        This method should be able to return any kind of python object as long
        as the model that is used is compatible.
        
        :return: (taurus.core.TaurusElementType) the role in form of element type"""
        return ElemType.Unknown

    def __str__(self):
        return self.display()


class TaurusBaseModel(Qt.QAbstractItemModel, Logger):
    """The base class for all Taurus Qt models."""
    
    ColumnNames = ()
    ColumnRoles = (),
    
    DftFont = Qt.QFont("Mono", 8)
    
    def __init__(self, parent=None, data=None):
        Qt.QAbstractItemModel.__init__(self, parent)
        Logger.__init__(self)
        # if qt < 4.6, beginResetModel and endResetModel don't exist. In this
        # case we set beginResetModel to be an empty function and endResetModel
        # to be reset.
        if not hasattr(Qt.QAbstractItemModel, "beginResetModel"):
            self.beginResetModel = lambda : None
            self.endResetModel = self.reset
        self._data_src = None
        self._rootItem = None
        self._filters = []
        self._selectables = [ self.ColumnRoles[0][-1] ]
        self.setDataSource(data)
    
    def __getattr__(self, name):
        return getattr(self.dataSource(), name)
    
    def createNewRootItem(self):
        return TaurusTreeBaseItem(self, self.ColumnNames)
    
    def refresh(self, refresh_source=False):
        self.beginResetModel()
        self._rootItem = self.createNewRootItem()
        self.setupModelData(self.dataSource())
        self.endResetModel()
    
    def setupModelData(self, data):
        raise NotImplementedError("setupModelData must be implemented "
                                  "in %s" % self.__class__.__name__)
    
    def roleIcon(self, role):
        raise NotImplementedError("roleIcon must be implemented "
                                  "in %s" % self.__class__.__name__)

    def roleSize(self, role):
        raise NotImplementedError("roleSize must be implemented "
                                  "in %s" % self.__class__.__name__)
    
    def roleToolTip(self, role):
        raise NotImplementedError("roleToolTip must be implemented "
                                  "in %s" % self.__class__.__name__)
    
    def setDataSource(self, data_src):
        self._data_src = data_src
        self.refresh()
    
    def dataSource(self):
        return self._data_src
    
    def setSelectables(self, seq_elem_types):
        self._selectables = seq_elem_types
    
    def selectables(self):
        return self._selectables

    def role(self, column, depth=0):
        cr = self.ColumnRoles
        if column == 0:
            return cr[0][depth]
        return self.ColumnRoles[column]
    
    def columnCount(self, parent = Qt.QModelIndex()):
        return len(self.ColumnRoles)
    
    def columnIcon(self, column):
        return self.roleIcon(self.role(column))
    
    def columnToolTip(self, column):
        return self.roleToolTip(self.role(column))
    
    def columnSize(self, column):
        role = self.role(column)
        s = self.roleSize(role)
        return s
    
    def pyData(self, index, role=Qt.Qt.DisplayRole):
        if not index.isValid():
            return None
        
        item = index.internalPointer()
        
        ret = None
        if role == Qt.Qt.DisplayRole or role == Qt.Qt.EditRole:
            ret = item.data(index)
#        elif role == Qt.Qt.CheckStateRole:
#            data = item.data(index)
#            if type(data) != bool:
#                data = str(data).lower() == 'true'
#            ret = Qt.Qt.Unchecked
#            if data == True:
#                ret = Qt.Qt.Checked
        elif role == Qt.Qt.DecorationRole:
            ret = item.icon(index)
        elif role == Qt.Qt.ToolTipRole:
            ret = item.toolTip(index)
        #elif role == Qt.Qt.SizeHintRole:
        #    ret = self.columnSize(column)
        elif role == Qt.Qt.FontRole:
            ret = self.DftFont
        elif role == Qt.Qt.UserRole:
            ret = Qt.QVariant(item)
        return ret
    
    def data(self, index, role=Qt.Qt.DisplayRole):
        ret = self.pyData(index, role)
        if ret is None:
            ret = Qt.QVariant()
        else:
            ret = Qt.QVariant(ret)
        return ret

    def _setData(self, index, qvalue, role=Qt.Qt.EditRole):
        item = index.internalPointer()
        pyobj = qvalue.toPyObject()
        if pyobj is NotImplemented:
            self.warning("Failed attempt to convert a QValue. Maybe it is due to Qt<4.6")
        item.setData(index, pyobj)
        return True

    def flags(self, index):
        if not index.isValid():
            return 0
        
        ret = Qt.Qt.ItemIsEnabled | Qt.Qt.ItemIsDragEnabled
        
        item = index.internalPointer()
        column, depth = index.column(), item.depth()
        taurus_role = self.role(column, depth)
        
        if taurus_role in self.selectables():
            ret |= Qt.Qt.ItemIsSelectable
        return ret
    
    def headerData(self, section, orientation, role=Qt.Qt.DisplayRole):
        ret = None
        if orientation == Qt.Qt.Horizontal:
            if role == Qt.Qt.TextAlignmentRole:
                ret = int(Qt.Qt.AlignLeft | Qt.Qt.AlignVCenter)
            elif role == Qt.Qt.DisplayRole:
                ret = self.ColumnNames[section]
            elif role == Qt.Qt.SizeHintRole:
                ret = Qt.QSize(self.columnSize(section))
                ret.setHeight(24)
            elif role == Qt.Qt.ToolTipRole:
                ret = self.columnToolTip(section)
            elif role == Qt.Qt.DecorationRole:
                ret = self.columnIcon(section)
                
        return Qt.QVariant(ret)

    def index(self, row, column, parent = Qt.QModelIndex()):
        if not self.hasIndex(row, column, parent):
            return Qt.QModelIndex()
        if not parent.isValid():
            parentItem = self._rootItem
        else:
            parentItem = parent.internalPointer()
        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        return Qt.QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return Qt.QModelIndex()
        
        childItem = index.internalPointer()
        parentItem = childItem.parent()
        
        if parentItem is None or parentItem == self._rootItem:
            return Qt.QModelIndex()
        
        return self.createIndex(parentItem.row(), 0, parentItem)

    def rowCount(self, parent = Qt.QModelIndex()):
        if parent.column() > 0:
            return 0
        
        if not parent.isValid():
            parentItem = self._rootItem
        else:
            parentItem = parent.internalPointer()
        if parentItem is None:
            return 0
        return parentItem.childCount()

    def hasChildren(self, parent = Qt.QModelIndex()):
        if parent.column() > 0:
            return 0
        if not parent.isValid():
            parentItem = self._rootItem
        else:
            parentItem = parent.internalPointer()
        
        if parentItem is None:
            return False
        return parentItem.hasChildren()


class TaurusBaseProxyModel(Qt.QSortFilterProxyModel):
    """A taurus database base Qt filter & sort model"""
     
    def __init__(self, parent=None):
        Qt.QSortFilterProxyModel.__init__(self, parent)
        
        # filter configuration
        self.setFilterCaseSensitivity(Qt.Qt.CaseInsensitive)
        self.setFilterKeyColumn(0)
        self.setFilterRole(Qt.Qt.DisplayRole)
        
        # sort configuration
        self.setSortCaseSensitivity(Qt.Qt.CaseInsensitive)
        self.setSortRole(Qt.Qt.DisplayRole)
        
        # general configuration
        self.sort(0, Qt.Qt.AscendingOrder)
        
    def __getattr__(self, name):
        return getattr(self.sourceModel(), name)
