# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/eoyilmaz/Documents/development/oyProjectManager/oyProjectManager/ui/project_properties.ui'
#
# Created: Mon Feb 27 17:05:59 2012
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(638, 574)
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tabWidget = QtGui.QTabWidget(Dialog)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.tab)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.name_label = QtGui.QLabel(self.tab)
        self.name_label.setText(QtGui.QApplication.translate("Dialog", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.name_label.setObjectName(_fromUtf8("name_label"))
        self.gridLayout.addWidget(self.name_label, 0, 0, 1, 1)
        self.name_lineEdit = QtGui.QLineEdit(self.tab)
        self.name_lineEdit.setObjectName(_fromUtf8("name_lineEdit"))
        self.gridLayout.addWidget(self.name_lineEdit, 0, 1, 1, 1)
        self.code_label = QtGui.QLabel(self.tab)
        self.code_label.setText(QtGui.QApplication.translate("Dialog", "Code", None, QtGui.QApplication.UnicodeUTF8))
        self.code_label.setObjectName(_fromUtf8("code_label"))
        self.gridLayout.addWidget(self.code_label, 1, 0, 1, 1)
        self.code_lineEdit = QtGui.QLineEdit(self.tab)
        self.code_lineEdit.setObjectName(_fromUtf8("code_lineEdit"))
        self.gridLayout.addWidget(self.code_lineEdit, 1, 1, 1, 1)
        self.resolution_label = QtGui.QLabel(self.tab)
        self.resolution_label.setText(QtGui.QApplication.translate("Dialog", "Resolution", None, QtGui.QApplication.UnicodeUTF8))
        self.resolution_label.setObjectName(_fromUtf8("resolution_label"))
        self.gridLayout.addWidget(self.resolution_label, 2, 0, 1, 1)
        self.resolution_comboBox = QtGui.QComboBox(self.tab)
        self.resolution_comboBox.setObjectName(_fromUtf8("resolution_comboBox"))
        self.gridLayout.addWidget(self.resolution_comboBox, 2, 1, 1, 1)
        self.fps_label = QtGui.QLabel(self.tab)
        self.fps_label.setText(QtGui.QApplication.translate("Dialog", "Fps", None, QtGui.QApplication.UnicodeUTF8))
        self.fps_label.setObjectName(_fromUtf8("fps_label"))
        self.gridLayout.addWidget(self.fps_label, 3, 0, 1, 1)
        self.fps_spinBox = QtGui.QSpinBox(self.tab)
        self.fps_spinBox.setObjectName(_fromUtf8("fps_spinBox"))
        self.gridLayout.addWidget(self.fps_spinBox, 3, 1, 1, 1)
        self.active_checkBox = QtGui.QCheckBox(self.tab)
        self.active_checkBox.setText(QtGui.QApplication.translate("Dialog", "Active", None, QtGui.QApplication.UnicodeUTF8))
        self.active_checkBox.setObjectName(_fromUtf8("active_checkBox"))
        self.gridLayout.addWidget(self.active_checkBox, 4, 1, 1, 1)
        self.verticalLayout_4.addLayout(self.gridLayout)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem)
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.tab_2)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.shot_number_prefix_label = QtGui.QLabel(self.tab_2)
        self.shot_number_prefix_label.setText(QtGui.QApplication.translate("Dialog", "Shot Number Prefix", None, QtGui.QApplication.UnicodeUTF8))
        self.shot_number_prefix_label.setObjectName(_fromUtf8("shot_number_prefix_label"))
        self.gridLayout_2.addWidget(self.shot_number_prefix_label, 0, 0, 1, 1)
        self.revision_number_prefix_label = QtGui.QLabel(self.tab_2)
        self.revision_number_prefix_label.setText(QtGui.QApplication.translate("Dialog", "Revision Number Prefix", None, QtGui.QApplication.UnicodeUTF8))
        self.revision_number_prefix_label.setObjectName(_fromUtf8("revision_number_prefix_label"))
        self.gridLayout_2.addWidget(self.revision_number_prefix_label, 2, 0, 1, 1)
        self.version_number_prefix_label = QtGui.QLabel(self.tab_2)
        self.version_number_prefix_label.setText(QtGui.QApplication.translate("Dialog", "Version Number Prefix", None, QtGui.QApplication.UnicodeUTF8))
        self.version_number_prefix_label.setObjectName(_fromUtf8("version_number_prefix_label"))
        self.gridLayout_2.addWidget(self.version_number_prefix_label, 4, 0, 1, 1)
        self.shot_number_padding_label = QtGui.QLabel(self.tab_2)
        self.shot_number_padding_label.setText(QtGui.QApplication.translate("Dialog", "Shot Number Padding", None, QtGui.QApplication.UnicodeUTF8))
        self.shot_number_padding_label.setObjectName(_fromUtf8("shot_number_padding_label"))
        self.gridLayout_2.addWidget(self.shot_number_padding_label, 1, 0, 1, 1)
        self.revision_number_padding_label = QtGui.QLabel(self.tab_2)
        self.revision_number_padding_label.setText(QtGui.QApplication.translate("Dialog", "Revision Number Padding", None, QtGui.QApplication.UnicodeUTF8))
        self.revision_number_padding_label.setObjectName(_fromUtf8("revision_number_padding_label"))
        self.gridLayout_2.addWidget(self.revision_number_padding_label, 3, 0, 1, 1)
        self.version_number_padding_label = QtGui.QLabel(self.tab_2)
        self.version_number_padding_label.setText(QtGui.QApplication.translate("Dialog", "Version Number Padding", None, QtGui.QApplication.UnicodeUTF8))
        self.version_number_padding_label.setObjectName(_fromUtf8("version_number_padding_label"))
        self.gridLayout_2.addWidget(self.version_number_padding_label, 5, 0, 1, 1)
        self.shot_number_prefix_lineEdit = QtGui.QLineEdit(self.tab_2)
        self.shot_number_prefix_lineEdit.setObjectName(_fromUtf8("shot_number_prefix_lineEdit"))
        self.gridLayout_2.addWidget(self.shot_number_prefix_lineEdit, 0, 1, 1, 1)
        self.revision_number_prefix_lineEdit = QtGui.QLineEdit(self.tab_2)
        self.revision_number_prefix_lineEdit.setObjectName(_fromUtf8("revision_number_prefix_lineEdit"))
        self.gridLayout_2.addWidget(self.revision_number_prefix_lineEdit, 2, 1, 1, 1)
        self.version_number_prefix_lineEdit = QtGui.QLineEdit(self.tab_2)
        self.version_number_prefix_lineEdit.setObjectName(_fromUtf8("version_number_prefix_lineEdit"))
        self.gridLayout_2.addWidget(self.version_number_prefix_lineEdit, 4, 1, 1, 1)
        self.shot_number_padding_spinBox = QtGui.QSpinBox(self.tab_2)
        self.shot_number_padding_spinBox.setObjectName(_fromUtf8("shot_number_padding_spinBox"))
        self.gridLayout_2.addWidget(self.shot_number_padding_spinBox, 1, 1, 1, 1)
        self.revision_number_padding_spinBox = QtGui.QSpinBox(self.tab_2)
        self.revision_number_padding_spinBox.setObjectName(_fromUtf8("revision_number_padding_spinBox"))
        self.gridLayout_2.addWidget(self.revision_number_padding_spinBox, 3, 1, 1, 1)
        self.version_number_padding_spinBox = QtGui.QSpinBox(self.tab_2)
        self.version_number_padding_spinBox.setObjectName(_fromUtf8("version_number_padding_spinBox"))
        self.gridLayout_2.addWidget(self.version_number_padding_spinBox, 5, 1, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout_2)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(-1, 10, -1, -1)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.structure_label = QtGui.QLabel(self.tab_2)
        self.structure_label.setText(QtGui.QApplication.translate("Dialog", "Structure Code", None, QtGui.QApplication.UnicodeUTF8))
        self.structure_label.setObjectName(_fromUtf8("structure_label"))
        self.verticalLayout_2.addWidget(self.structure_label)
        self.structure_textEdit = QtGui.QTextEdit(self.tab_2)
        self.structure_textEdit.setObjectName(_fromUtf8("structure_textEdit"))
        self.verticalLayout_2.addWidget(self.structure_textEdit)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.verticalLayout.addWidget(self.tabWidget)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("Dialog", "Basic", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("Dialog", "Advanced", None, QtGui.QApplication.UnicodeUTF8))

