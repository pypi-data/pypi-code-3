# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/tmp/tmpSE27_q.ui'
#
# Created: Mon Apr 16 15:17:09 2012
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_ExpDescriptionEditor(object):
    def setupUi(self, ExpDescriptionEditor):
        ExpDescriptionEditor.setObjectName("ExpDescriptionEditor")
        ExpDescriptionEditor.resize(733, 411)
        self.verticalLayout_3 = QtGui.QVBoxLayout(ExpDescriptionEditor)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.tabWidget = QtGui.QTabWidget(ExpDescriptionEditor)
        self.tabWidget.setObjectName("tabWidget")
        self.mntGrpTab = QtGui.QWidget()
        self.mntGrpTab.setObjectName("mntGrpTab")
        self.verticalLayout = QtGui.QVBoxLayout(self.mntGrpTab)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtGui.QLabel(self.mntGrpTab)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.activeMntGrpCB = QtGui.QComboBox(self.mntGrpTab)
        self.activeMntGrpCB.setObjectName("activeMntGrpCB")
        self.horizontalLayout.addWidget(self.activeMntGrpCB)
        self.createMntGrpBT = QtGui.QToolButton(self.mntGrpTab)
        self.createMntGrpBT.setObjectName("createMntGrpBT")
        self.horizontalLayout.addWidget(self.createMntGrpBT)
        self.deleteMntGrpBT = QtGui.QToolButton(self.mntGrpTab)
        self.deleteMntGrpBT.setObjectName("deleteMntGrpBT")
        self.horizontalLayout.addWidget(self.deleteMntGrpBT)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.channelEditor = MntGrpChannelEditor(self.mntGrpTab)
        self.channelEditor.setObjectName("channelEditor")
        self.verticalLayout.addWidget(self.channelEditor)
        self.tabWidget.addTab(self.mntGrpTab, "")
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.tab_2)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.splitter = QtGui.QSplitter(self.tab_2)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.tabWidget_2 = QtGui.QTabWidget(self.splitter)
        self.tabWidget_2.setObjectName("tabWidget_2")
        self.tab_4 = QtGui.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.tab_4)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.sardanaElementTree = SardanaElementTreeWidget(self.tab_4)
        self.sardanaElementTree.setObjectName("sardanaElementTree")
        self.verticalLayout_5.addWidget(self.sardanaElementTree)
        self.tabWidget_2.addTab(self.tab_4, "")
        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.tab)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.taurusModelTree = TaurusModelSelectorTree(self.tab)
        self.taurusModelTree.setObjectName("taurusModelTree")
        self.verticalLayout_4.addWidget(self.taurusModelTree)
        self.tabWidget_2.addTab(self.tab, "")
        self.layoutWidget = QtGui.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_5 = QtGui.QLabel(self.layoutWidget)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_2.addWidget(self.label_5)
        self.preScanList = TaurusModelList(self.layoutWidget)
        self.preScanList.setObjectName("preScanList")
        self.verticalLayout_2.addWidget(self.preScanList)
        self.verticalLayout_6.addWidget(self.splitter)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.formLayout = QtGui.QFormLayout(self.tab_3)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.label_3 = QtGui.QLabel(self.tab_3)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_3)
        self.filenameLE = QtGui.QLineEdit(self.tab_3)
        self.filenameLE.setObjectName("filenameLE")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.filenameLE)
        self.label_2 = QtGui.QLabel(self.tab_3)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_2)
        self.widget = QtGui.QWidget(self.tab_3)
        self.widget.setObjectName("widget")
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pathLE = QtGui.QLineEdit(self.widget)
        self.pathLE.setObjectName("pathLE")
        self.horizontalLayout_2.addWidget(self.pathLE)
        self.choosePathBT = QtGui.QToolButton(self.widget)
        self.choosePathBT.setObjectName("choosePathBT")
        self.horizontalLayout_2.addWidget(self.choosePathBT)
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.widget)
        self.label_4 = QtGui.QLabel(self.tab_3)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_4)
        self.compressionCB = QtGui.QComboBox(self.tab_3)
        self.compressionCB.setObjectName("compressionCB")
        self.compressionCB.addItem(QtCore.QString())
        self.compressionCB.addItem(QtCore.QString())
        self.compressionCB.addItem(QtCore.QString())
        self.compressionCB.addItem(QtCore.QString())
        self.compressionCB.addItem(QtCore.QString())
        self.formLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.compressionCB)
        self.tabWidget.addTab(self.tab_3, "")
        self.verticalLayout_3.addWidget(self.tabWidget)
        self.buttonBox = QtGui.QDialogButtonBox(ExpDescriptionEditor)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.NoButton)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_3.addWidget(self.buttonBox)

        self.retranslateUi(ExpDescriptionEditor)
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget_2.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(ExpDescriptionEditor)

    def retranslateUi(self, ExpDescriptionEditor):
        ExpDescriptionEditor.setWindowTitle(QtGui.QApplication.translate("ExpDescriptionEditor", "Experiment Configuration", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("ExpDescriptionEditor", "Active Measurement Group", None, QtGui.QApplication.UnicodeUTF8))
        self.activeMntGrpCB.setToolTip(QtGui.QApplication.translate("ExpDescriptionEditor", "Selects the active Measurement Group", None, QtGui.QApplication.UnicodeUTF8))
        self.createMntGrpBT.setToolTip(QtGui.QApplication.translate("ExpDescriptionEditor", "Create a new Measurement Group", None, QtGui.QApplication.UnicodeUTF8))
        self.createMntGrpBT.setText(QtGui.QApplication.translate("ExpDescriptionEditor", "+", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteMntGrpBT.setToolTip(QtGui.QApplication.translate("ExpDescriptionEditor", "Delete the current Measurement Group", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteMntGrpBT.setText(QtGui.QApplication.translate("ExpDescriptionEditor", "-", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.mntGrpTab), QtGui.QApplication.translate("ExpDescriptionEditor", "Measurement Group", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_4), QtGui.QApplication.translate("ExpDescriptionEditor", "Sardana Elements", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab), QtGui.QApplication.translate("ExpDescriptionEditor", "External (Tango)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("ExpDescriptionEditor", "(Drag elements from the above selectors and drop them at the bottom list)", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("ExpDescriptionEditor", "Snapshot Group", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setToolTip(QtGui.QApplication.translate("ExpDescriptionEditor", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">comma separated list of file names in which to store the results of the scans. Use .h5 extension for NeXus files (preferred) and .dat for spec format (note: SPEC format is <span style=\" font-weight:600;\">not </span>supported)</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("ExpDescriptionEditor", "File Name(s)", None, QtGui.QApplication.UnicodeUTF8))
        self.filenameLE.setToolTip(QtGui.QApplication.translate("ExpDescriptionEditor", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">comma separated list of file names in which to store the results of the scans. Use .h5 extension for NeXus files (preferred) and .dat for spec format (note: SPEC format is <span style=\" font-weight:600;\">not </span>supported)</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("ExpDescriptionEditor", "Path", None, QtGui.QApplication.UnicodeUTF8))
        self.choosePathBT.setText(QtGui.QApplication.translate("ExpDescriptionEditor", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("ExpDescriptionEditor", "Data compression", None, QtGui.QApplication.UnicodeUTF8))
        self.compressionCB.setItemText(0, QtGui.QApplication.translate("ExpDescriptionEditor", "nowhere", None, QtGui.QApplication.UnicodeUTF8))
        self.compressionCB.setItemText(1, QtGui.QApplication.translate("ExpDescriptionEditor", "for all datasets", None, QtGui.QApplication.UnicodeUTF8))
        self.compressionCB.setItemText(2, QtGui.QApplication.translate("ExpDescriptionEditor", "for datasets of rank 1 or more", None, QtGui.QApplication.UnicodeUTF8))
        self.compressionCB.setItemText(3, QtGui.QApplication.translate("ExpDescriptionEditor", "for datasets of rank 2 or more", None, QtGui.QApplication.UnicodeUTF8))
        self.compressionCB.setItemText(4, QtGui.QApplication.translate("ExpDescriptionEditor", "for datasets of rank 3 or more", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QtGui.QApplication.translate("ExpDescriptionEditor", "Storage", None, QtGui.QApplication.UnicodeUTF8))

from taurus.qt.qtgui.panel import TaurusModelList, TaurusModelSelectorTree
from taurus.qt.qtgui.extra_sardana import SardanaElementTreeWidget, MntGrpChannelEditor
