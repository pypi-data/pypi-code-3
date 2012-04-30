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

"""This module provides base widget that displays a Qt view widget envolved
by a toolbar and a status bar (optional)"""

__all__ = ["QBaseModelWidget", "TaurusBaseModelWidget",
           "BaseToolBar", "FilterToolBar", "EditorToolBar", "SelectionToolBar",
           "RefreshToolBar", "PerspectiveToolBar"]

__docformat__ = 'restructuredtext'

from taurus.qt import Qt

from taurus.qt.qtcore.model import *
from taurus.qt.qtgui.util import ActionFactory
from taurus.qt.qtgui.resource import getIcon, getThemeIcon
from taurus.qt.qtgui.base import TaurusBaseWidget

class BaseToolBar(Qt.QToolBar):

    def __init__(self, name=None, view=None, parent=None, designMode=False):
        if name is None:
            name = "Base toolbar"
        self._viewWidget = view or parent
        Qt.QToolBar.__init__(self, name, parent)
        self.setIconSize(Qt.QSize(16, 16))
        self.setFloatable(False)
        self.setMovable(False)

    def viewWidget(self):
        return self._viewWidget


class FilterToolBar(BaseToolBar):
    """Internal widget providing quick filter to be placed in a _QToolArea"""
    
    def __init__(self, view=None, parent=None, designMode=False):
        BaseToolBar.__init__(self, name="Taurus filter toolbar", view=view,
                             parent=parent, designMode=designMode)
        filterLineEdit = self._filterLineEdit = Qt.QLineEdit(self)
        filterLineEdit.setSizePolicy(Qt.QSizePolicy(Qt.QSizePolicy.Preferred,
                                                    Qt.QSizePolicy.Preferred))
        filterLineEdit.setToolTip("Quick filter")
        Qt.QObject.connect(filterLineEdit,
                           Qt.SIGNAL("textChanged(const QString &)"),
                           self.onFilterChanged)
        self.addWidget(filterLineEdit)

        af = ActionFactory()
        self._clearFilterAction = af.createAction(self, "Clear",
                                          icon=getThemeIcon("edit-clear"),
                                          tip="Clears the filter",
                                          triggered=self.onClearFilter)
        self.addAction(self._clearFilterAction)

    def filterLineEdit(self):
        return self._filterLineEdit
        
    def onClearFilter(self):
        self.filterLineEdit().setText("")
        self.emit(Qt.SIGNAL("clearFilterTriggered"))
        
    def onFilterChanged(self, text=None):
        text = text or self.filterLineEdit().text()
        self.emit(Qt.SIGNAL("filterChanged"), text)


class EditorToolBar(BaseToolBar):
    """Internal widget to be placed in a _QToolArea providing buttons for
    moving, adding and removing items from a view based widget"""
    
    def __init__(self, view=None, parent=None, designMode=False):
        BaseToolBar.__init__(self, name="Taurus editor toolbar", view=view,
                             parent=parent, designMode=designMode)
        
        af = ActionFactory()
        self._addAction = af.createAction(self, "New item",
                                          icon=getThemeIcon("list-add"),
                                          tip="Add new item",
                                          triggered=self.onAdd)
        self._removeAction = af.createAction(self, "Remove item",
                                             icon=getThemeIcon("list-remove"),
                                             tip="Remove item",
                                             triggered=self.onRemove)
        self._moveTopAction = af.createAction(self, "To top",
                                              icon=getThemeIcon("go-top"),
                                              tip="Move selected item to top",
                                              triggered=self.onMoveTop)
        self._moveUpAction = af.createAction(self, "Move up",
                                             icon=getThemeIcon("go-up"),
                                             tip="Move selected item up one level",
                                             triggered=self.onMoveUp)
        self._moveDownAction = af.createAction(self, "Move down",
                                               icon=getThemeIcon("go-down"),
                                               tip="Move selected item down one level",
                                               triggered=self.onMoveDown)
        self._moveBottomAction = af.createAction(self, "To bottom",
                                                 icon=getThemeIcon("go-bottom"),
                                                 tip="Move selected item to bottom",
                                                 triggered=self.onMoveBottom)
        self.addAction(self._addAction)
        self.addAction(self._removeAction)
        self.addAction(self._moveTopAction)
        self.addAction(self._moveUpAction)
        self.addAction(self._moveDownAction)
        self.addAction(self._moveBottomAction)
        #self.setStyleSheet("QWidget {background : red; }")
    
    def onAdd(self):
        self.emit(Qt.SIGNAL("addTriggered"))

    def onRemove(self):
        self.emit(Qt.SIGNAL("removeTriggered"))

    def onMoveTop(self):
        self.emit(Qt.SIGNAL("moveTopTriggered"))
    
    def onMoveUp(self):
        self.emit(Qt.SIGNAL("moveUpTriggered"))

    def onMoveDown(self):
        self.emit(Qt.SIGNAL("moveDownTriggered"))

    def onMoveBottom(self):
        self.emit(Qt.SIGNAL("moveBottomTriggered"))


class SelectionToolBar(BaseToolBar):
    
    def __init__(self, view=None, parent=None, designMode=False):
        BaseToolBar.__init__(self, name="Taurus selection toolbar", view=view,
                             parent=parent, designMode=designMode)

        af = ActionFactory()
        self._selectAllAction = af.createAction(self, "Select All",
                                                icon=getThemeIcon("edit-select-all"),
                                                tip="Select all items",
                                                triggered=self.onSelectAll)
        self._clearSelectionAction = af.createAction(self, "Clear selection",
                                                     icon=getThemeIcon("edit-clear"),
                                                     tip="Clears current selection",
                                                     triggered=self.onclearSelection)

        self.addAction(self._selectAllAction)
        self.addAction(self._clearSelectionAction)
    
    def onSelectAll(self):
        self.emit(Qt.SIGNAL("selectAllTriggered"))

    def onclearSelection(self):
        self.emit(Qt.SIGNAL("clearSelectionTriggered"))


class RefreshToolBar(BaseToolBar):
    
    def __init__(self, view=None, parent=None, designMode=False):
        BaseToolBar.__init__(self, name="Taurus refresh toolbar", view=view,
                             parent=parent, designMode=designMode)

        af = ActionFactory()
        self._refreshAction = af.createAction(self, "Refresh",
                                              icon=getThemeIcon("view-refresh"),
                                              tip="Refresh view",
                                              triggered=self.onRefresh)
        self.addAction(self._refreshAction)
    
    def onRefresh(self):
        self.emit(Qt.SIGNAL("refreshTriggered"))


class PerspectiveToolBar(BaseToolBar):
    
    def __init__(self, perspective, view=None, parent=None, designMode=False):
        BaseToolBar.__init__(self, name="Taurus refresh toolbar", view=view,
                             parent=parent, designMode=designMode)
        self._perspective = perspective
        view = self.viewWidget()
        b = self._perspective_button = Qt.QToolButton(self)
        b.setToolTip("Perspective selection")
        b.setPopupMode(Qt.QToolButton.InstantPopup)
        b.setToolButtonStyle(Qt.Qt.ToolButtonTextBesideIcon)
        
        menu = Qt.QMenu("Perspective", b)
        b.setMenu(menu)
        af = ActionFactory()
        for persp, persp_data in view.KnownPerspectives.items():
            label = persp_data["label"]
            icon = getIcon(persp_data["icon"])
            tip = persp_data["tooltip"]
            action = af.createAction(self, label, icon=icon, tip=tip,
                                     triggered=self.onSwitchPerspective)
            action.perspective = persp
            menu.addAction(action)
            if persp == perspective:
                b.setDefaultAction(action)
        
        self._perspectiveAction = self.addWidget(b)

    def switchPerspectiveButton(self):
        """Returns the QToolButton that handles the switch perspective.
        
        :return: (PyQt4.QtGui.QToolButton) the switch perspective tool button
        """
        return self._perspective_button
    
    def onSwitchPerspective(self):
        action = self.sender()
        self._perspective = action.perspective
        self._perspective_button.setDefaultAction(action)
        self.emit(Qt.SIGNAL("perspectiveChanged"), action.perspective)

    def perspective(self):
        return self._perspective


class QBaseModelWidget(Qt.QMainWindow):
    """A pure Qt widget designed to display a Qt view widget (QTreeView for
    example), envolved by optional toolbar and statusbar.
    The Qt model associated with the internal Qt view widget should be a
    :class:`taurus.qt.qtcore.model.TaurusBaseModel`"""
    
    def __init__(self, parent=None, designMode=False, with_filter_widget=True):
        Qt.QMainWindow.__init__(self, parent)
        self.setWindowFlags(Qt.Qt.Widget)
        self._baseQModel = None
        self._toolBars = []
        self._with_filter_widget = with_filter_widget
        
        toolBars = self.createToolArea()
        self._viewWidget = self.createViewWidget()
        statusbar = self.createStatusBar()
        
        for toolBar in toolBars:
            toolBar.addSeparator()
            self.addToolBar(toolBar)
        self.setContentsMargins(0, 0, 0, 0)
        self.setCentralWidget(self._viewWidget)
        self.setStatusBar(statusbar)
    
    def createViewWidget(self):
        raise NotImplementedError
    
    def createStatusBar(self):
        sb = Qt.QStatusBar()
        sb.setSizeGripEnabled(False)
        return sb
    
    def createToolArea(self):
        tb = [] # tb = self._toolArea = QToolArea(self)
        if self._with_filter_widget:
            f_bar = self._filterBar = FilterToolBar(view=self, parent=self)
            Qt.QObject.connect(f_bar, Qt.SIGNAL("filterChanged"),
                               self.onFilterChanged)
            tb.append(f_bar)
        else:
            self._filterBar = None

        s_bar = self._selectionBar = SelectionToolBar(view=self, parent=self)
        Qt.QObject.connect(s_bar, Qt.SIGNAL("selectAllTriggered"),
                           self.onSelectAll)
        Qt.QObject.connect(s_bar, Qt.SIGNAL("clearSelectionTriggered"),
                           self.onClearSelection)
        tb.append(s_bar)
        
        r_bar = self._selectionBar = RefreshToolBar(view=self, parent=self)
        Qt.QObject.connect(r_bar, Qt.SIGNAL("refreshTriggered"),
                           self.onRefreshModel)
        tb.append(r_bar)
        
        return tb

    def onRefreshModel(self):
        self.getQModel().refresh(True)

    def onSelectAll(self):
        view = self.viewWidget()
        view.selectAll()

    def onClearSelection(self):
        view = self.viewWidget()
        view.clearSelection()

    def _onClicked (self, index):
        '''Emits an "itemClicked" signal with with the clicked item and column
        as arguments'''
        item = self._mapToSource(index).internalPointer()
        self.emit(Qt.SIGNAL('itemClicked'),item, index.column())
        
    def _onDoubleClicked (self, index):
        '''Emits an "itemDoubleClicked" signal with the clicked item and column
        as arguments'''
        item = self._mapToSource(index).internalPointer()
        self.emit(Qt.SIGNAL('itemDoubleClicked'),item, index.column())

    def viewWidget(self):
        return self._viewWidget
    
    def getQModel(self):
        return self.viewWidget().model()

    def getBaseQModel(self):
        return self._baseQModel

    def usesProxyQModel(self):
        return isinstance(self.getQModel(), Qt.QAbstractProxyModel)

    def _mapToSource(self, index):
        if not self.usesProxyQModel():
            return index
        model = self.getQModel()
        while isinstance(model, Qt.QAbstractProxyModel):
            index = model.mapToSource(index)
            model = model.sourceModel()
        return index

    def setQModel(self, qmodel):
        
        self._baseQModel = qmodel
        while isinstance(self._baseQModel, Qt.QAbstractProxyModel):
            self._baseQModel = self._baseQModel.sourceModel()
        
        view = self.viewWidget()
        old_selection_model = view.selectionModel()
        CC = 'currentChanged(const QModelIndex &,const QModelIndex &)'
        SC = 'selectionChanged(QItemSelection &, QItemSelection &)'
        if old_selection_model is not None:
            Qt.QObject.disconnect(old_selection_model, Qt.SIGNAL(CC),
                                  self.viewCurrentIndexChanged)
            Qt.QObject.disconnect(old_selection_model, Qt.SIGNAL(SC),
                                  self.viewSelectionChanged)
        view.setModel(qmodel)
        new_selection_model = view.selectionModel()
        if new_selection_model is not None:
            Qt.QObject.connect(new_selection_model, Qt.SIGNAL(CC),
                               self.viewCurrentIndexChanged)
            Qt.QObject.connect(new_selection_model, Qt.SIGNAL(SC),
                               self.viewSelectionChanged)
        view.setCurrentIndex(view.rootIndex())
        self._updateToolBar()
    
    def viewSelectionChanged(self, selected, deselected):
        self.emit(Qt.SIGNAL("itemSelectionChanged"))
    
    def viewCurrentIndexChanged(self, current, previous):
        # if there is a proxy model we have to translate the selection
        base_current = self._mapToSource(current)
        base_previous = self._mapToSource(previous)
        
        self._updateToolBar(current)
        
        if base_current.isValid():
            currentTaurusTreeItem = base_current.internalPointer()
        else:
            currentTaurusTreeItem = None
            
        if base_previous.isValid():
            previousTaurusTreeItem = base_previous.internalPointer()
        else:
            previousTaurusTreeItem = None
        self.emit(Qt.SIGNAL("currentItemChanged"), currentTaurusTreeItem,
                  previousTaurusTreeItem)
    
    def _updateToolBar(self, current=None, previous=None):
        pass
    
    def selectedItems(self):
        """Returns a list of all selected non-hidden items
        
        :return: (list<TaurusTreeItem>)
        """
        view = self.viewWidget()
        return [self._mapToSource(index).internalPointer() for index in view.selectedIndexes()]
    
    def onFilterChanged(self, filter):
        if not self.usesProxyQModel():
            return
        proxy_model = self.getQModel()
        if len(filter) > 0 and filter[0] != '^':
            filter = '^' + filter
        proxy_model.setFilterRegExp(filter)
        #proxy_model.setFilterFixedString(filter)
        #proxy_model.setFilterWildcard(filter)
        #self.update()
    
    def refresh(self):
        self.getQModel().refresh()

    #-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-
    # QMainWindow overwriting
    #-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-
    def addToolBar(self, toolbar):
        Qt.QMainWindow.addToolBar(self, toolbar)
        self._toolBars.append(toolbar)
    
    def insertToolBar(self, before, toolbar):
        if isinstance(before, Qt.QToolBar):
            index = self._toolBars.index(before)
        else:
            index = before
            before = self._toolBars[before]
        Qt.QMainWindow.insertToolBar(self, before, toolbar)
        self._toolBars.insert(index, toolbar)


class TaurusBaseModelWidget(TaurusBaseWidget):
    """A class:`taurus.qt.qtgui.base.TaurusBaseWidget` that connects to a
    taurus model. It must be used together with class:`taurus.qt.qtgui.base.QBaseModelWidget`"""
    
    KnownPerspectives = { }
    DftPerspective = None

    def __init__(self, designMode=False, perspective=None, proxy=None):
        name = self.__class__.__name__
        self._proxyModel = proxy
        self.call__init__(TaurusBaseWidget, name, designMode=designMode)
        if perspective is None:
            perspective = self.DftPerspective
        
        if len(self.KnownPerspectives) > 1:
            p_bar = self._perspectiveBar = PerspectiveToolBar(perspective, view=self, parent=self)
            self.connect(p_bar, Qt.SIGNAL("perspectiveChanged"), self.onSwitchPerspective)
            self.addToolBar(p_bar)
        else:
            self._perspectiveBar = None
        self._setPerspective(perspective)

    def perspective(self):
        return self._perspectiveBar.perspective()
    
    def onSwitchPerspective(self, perspective):
        self._setPerspective(perspective)
    
    def _setPerspective(self, perspective):
        qmodel_classes = self.KnownPerspectives[perspective]["model"]
        qmodel_class, qmodel_proxy_classes = qmodel_classes[-1], qmodel_classes[:-1]
        qmodel_proxy_classes.reverse()
        qmodel = qmodel_class(self, self.getModelObj())
        qmodel_source = qmodel
        if self._proxyModel is None:
            for qmodel_proxy_class in qmodel_proxy_classes:
                qproxy = qmodel_proxy_class(self)
                qproxy.setSourceModel(qmodel_source)
                qmodel_source = qproxy
        else:
            self._proxyModel.setSourceModel(qmodel_source)
            qmodel_source = self._proxyModel
        self.setQModel(qmodel_source)
    

    #-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-
    # TaurusBaseWidget overwriting
    #-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-

    def setModel(self, m):
        TaurusBaseWidget.setModel(self, m)

        view, modelObj = self.viewWidget(), self.getModelObj()
        model = view.model()
        if model is None: return
        model.setDataSource(modelObj)
    
    #-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-
    # QT property definition
    #-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-
    
    #: This property holds the unique URI string representing the model name 
    #: with which this widget will get its data from. The convention used for 
    #: the string can be found :ref:`here <model-concept>`.
    #: 
    #: In case the property :attr:`useParentModel` is set to True, the model 
    #: text must start with a '/' followed by the attribute name.
    #:
    #: **Access functions:**
    #:
    #:     * :meth:`TaurusBaseWidget.getModel`
    #:     * :meth:`TaurusBaseWidget.setModel`
    #:     * :meth:`TaurusBaseWidget.resetModel`
    #:
    #: .. seealso:: :ref:`model-concept`
    model = Qt.pyqtProperty("QString", TaurusBaseWidget.getModel, setModel,
                            TaurusBaseWidget.resetModel)