# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/PoolMotorSlim.ui'
#
# Created: Thu Nov 11 19:30:23 2010
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_PoolMotorSlim(object):
    def setupUi(self, PoolMotorSlim):
        PoolMotorSlim.setObjectName("PoolMotorSlim")
        PoolMotorSlim.resize(487, 61)
        self.gridLayout_2 = QtGui.QGridLayout(PoolMotorSlim)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.motorGroupBox = TaurusGroupBox(PoolMotorSlim)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.motorGroupBox.sizePolicy().hasHeightForWidth())
        self.motorGroupBox.setSizePolicy(sizePolicy)
        self.motorGroupBox.setProperty("showText", QtCore.QVariant(False))
        self.motorGroupBox.setObjectName("motorGroupBox")
        self.gridLayout = QtGui.QGridLayout(self.motorGroupBox)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.taurusValueContainer = QtGui.QWidget(self.motorGroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.taurusValueContainer.sizePolicy().hasHeightForWidth())
        self.taurusValueContainer.setSizePolicy(sizePolicy)
        self.taurusValueContainer.setObjectName("taurusValueContainer")
        self.gridLayout.addWidget(self.taurusValueContainer, 0, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btnMin = QtGui.QPushButton(self.motorGroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnMin.sizePolicy().hasHeightForWidth())
        self.btnMin.setSizePolicy(sizePolicy)
        self.btnMin.setMaximumSize(QtCore.QSize(20, 16777215))
        self.btnMin.setAutoDefault(True)
        self.btnMin.setFlat(False)
        self.btnMin.setObjectName("btnMin")
        self.horizontalLayout.addWidget(self.btnMin)
        self.btnGoToNeg = QtGui.QPushButton(self.motorGroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnGoToNeg.sizePolicy().hasHeightForWidth())
        self.btnGoToNeg.setSizePolicy(sizePolicy)
        self.btnGoToNeg.setMaximumSize(QtCore.QSize(20, 16777215))
        self.btnGoToNeg.setDefault(False)
        self.btnGoToNeg.setFlat(False)
        self.btnGoToNeg.setObjectName("btnGoToNeg")
        self.horizontalLayout.addWidget(self.btnGoToNeg)
        self.btnGoToNegPress = QtGui.QPushButton(self.motorGroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnGoToNegPress.sizePolicy().hasHeightForWidth())
        self.btnGoToNegPress.setSizePolicy(sizePolicy)
        self.btnGoToNegPress.setMaximumSize(QtCore.QSize(20, 16777215))
        self.btnGoToNegPress.setObjectName("btnGoToNegPress")
        self.horizontalLayout.addWidget(self.btnGoToNegPress)
        self.btnGoToNegInc = QtGui.QPushButton(self.motorGroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnGoToNegInc.sizePolicy().hasHeightForWidth())
        self.btnGoToNegInc.setSizePolicy(sizePolicy)
        self.btnGoToNegInc.setMaximumSize(QtCore.QSize(20, 16777215))
        self.btnGoToNegInc.setObjectName("btnGoToNegInc")
        self.horizontalLayout.addWidget(self.btnGoToNegInc)
        self.inc = QtGui.QDoubleSpinBox(self.motorGroupBox)
        self.inc.setMaximumSize(QtCore.QSize(80, 16777215))
        self.inc.setMaximum(1e+100)
        self.inc.setProperty("value", QtCore.QVariant(1.0))
        self.inc.setObjectName("inc")
        self.horizontalLayout.addWidget(self.inc)
        self.btnGoToPosInc = QtGui.QPushButton(self.motorGroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnGoToPosInc.sizePolicy().hasHeightForWidth())
        self.btnGoToPosInc.setSizePolicy(sizePolicy)
        self.btnGoToPosInc.setMaximumSize(QtCore.QSize(20, 16777215))
        self.btnGoToPosInc.setObjectName("btnGoToPosInc")
        self.horizontalLayout.addWidget(self.btnGoToPosInc)
        self.btnGoToPosPress = QtGui.QPushButton(self.motorGroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnGoToPosPress.sizePolicy().hasHeightForWidth())
        self.btnGoToPosPress.setSizePolicy(sizePolicy)
        self.btnGoToPosPress.setMaximumSize(QtCore.QSize(20, 16777215))
        self.btnGoToPosPress.setObjectName("btnGoToPosPress")
        self.horizontalLayout.addWidget(self.btnGoToPosPress)
        self.btnGoToPos = QtGui.QPushButton(self.motorGroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnGoToPos.sizePolicy().hasHeightForWidth())
        self.btnGoToPos.setSizePolicy(sizePolicy)
        self.btnGoToPos.setMaximumSize(QtCore.QSize(20, 16777215))
        self.btnGoToPos.setObjectName("btnGoToPos")
        self.horizontalLayout.addWidget(self.btnGoToPos)
        self.btnMax = QtGui.QPushButton(self.motorGroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnMax.sizePolicy().hasHeightForWidth())
        self.btnMax.setSizePolicy(sizePolicy)
        self.btnMax.setMaximumSize(QtCore.QSize(20, 16777215))
        self.btnMax.setAutoDefault(False)
        self.btnMax.setObjectName("btnMax")
        self.horizontalLayout.addWidget(self.btnMax)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 1, 1, 1)
        self.btnStop = QtGui.QPushButton(self.motorGroupBox)
        self.btnStop.setMaximumSize(QtCore.QSize(30, 16777215))
        self.btnStop.setObjectName("btnStop")
        self.gridLayout.addWidget(self.btnStop, 0, 2, 1, 1)
        self.btnHome = QtGui.QPushButton(self.motorGroupBox)
        self.btnHome.setMaximumSize(QtCore.QSize(30, 16777215))
        self.btnHome.setObjectName("btnHome")
        self.gridLayout.addWidget(self.btnHome, 0, 3, 1, 1)
        self.btnCfg = TaurusLauncherButton(self.motorGroupBox)
        self.btnCfg.setMaximumSize(QtCore.QSize(30, 16777215))
        self.btnCfg.setObjectName("btnCfg")
        self.gridLayout.addWidget(self.btnCfg, 0, 4, 1, 1)
        self.lblStatus = TaurusValueLabel(self.motorGroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblStatus.sizePolicy().hasHeightForWidth())
        self.lblStatus.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(7)
        self.lblStatus.setFont(font)
        self.lblStatus.setStyleSheet("""TaurusValueLabel {
            border-style: outset;
            border-width: 2px;
            border-color: rgba(255,255,255,128);
            background-color: transparent; color:black; }""")
        self.lblStatus.setFrameShape(QtGui.QFrame.StyledPanel)
        self.lblStatus.setLineWidth(0)
        self.lblStatus.setProperty("model", QtCore.QVariant(QtGui.QApplication.translate("PoolMotorSlim", "/Status", None, QtGui.QApplication.UnicodeUTF8)))
        self.lblStatus.setProperty("useParentModel", QtCore.QVariant(True))
        self.lblStatus.setProperty("showQuality", QtCore.QVariant(False))
        self.lblStatus.setObjectName("lblStatus")
        self.gridLayout.addWidget(self.lblStatus, 1, 0, 1, 5)
        self.gridLayout_2.addWidget(self.motorGroupBox, 0, 0, 1, 1)

        self.retranslateUi(PoolMotorSlim)
        QtCore.QMetaObject.connectSlotsByName(PoolMotorSlim)

    def retranslateUi(self, PoolMotorSlim):
        PoolMotorSlim.setWindowTitle(QtGui.QApplication.translate("PoolMotorSlim", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.btnMin.setToolTip(QtGui.QApplication.translate("PoolMotorSlim", "Negative limit", None, QtGui.QApplication.UnicodeUTF8))
        self.btnMin.setText(QtGui.QApplication.translate("PoolMotorSlim", "-", None, QtGui.QApplication.UnicodeUTF8))
        self.btnGoToNeg.setToolTip(QtGui.QApplication.translate("PoolMotorSlim", "Moves the motor towards negative limit", None, QtGui.QApplication.UnicodeUTF8))
        self.btnGoToNeg.setText(QtGui.QApplication.translate("PoolMotorSlim", "|<", None, QtGui.QApplication.UnicodeUTF8))
        self.btnGoToNegPress.setToolTip(QtGui.QApplication.translate("PoolMotorSlim", "Moves the motor towards negative limit while pressed", None, QtGui.QApplication.UnicodeUTF8))
        self.btnGoToNegPress.setText(QtGui.QApplication.translate("PoolMotorSlim", "«", None, QtGui.QApplication.UnicodeUTF8))
        self.btnGoToNegInc.setToolTip(QtGui.QApplication.translate("PoolMotorSlim", "Decrements motor position <inc> units", None, QtGui.QApplication.UnicodeUTF8))
        self.btnGoToNegInc.setText(QtGui.QApplication.translate("PoolMotorSlim", "<", None, QtGui.QApplication.UnicodeUTF8))
        self.btnGoToPosInc.setToolTip(QtGui.QApplication.translate("PoolMotorSlim", "Increments motor position <inc> units", None, QtGui.QApplication.UnicodeUTF8))
        self.btnGoToPosInc.setText(QtGui.QApplication.translate("PoolMotorSlim", ">", None, QtGui.QApplication.UnicodeUTF8))
        self.btnGoToPosPress.setToolTip(QtGui.QApplication.translate("PoolMotorSlim", "Moves the motor towards positive limit while pressed", None, QtGui.QApplication.UnicodeUTF8))
        self.btnGoToPosPress.setText(QtGui.QApplication.translate("PoolMotorSlim", "»", None, QtGui.QApplication.UnicodeUTF8))
        self.btnGoToPos.setToolTip(QtGui.QApplication.translate("PoolMotorSlim", "Moves the motor towards positive limit", None, QtGui.QApplication.UnicodeUTF8))
        self.btnGoToPos.setText(QtGui.QApplication.translate("PoolMotorSlim", ">|", None, QtGui.QApplication.UnicodeUTF8))
        self.btnMax.setToolTip(QtGui.QApplication.translate("PoolMotorSlim", "Positive limit", None, QtGui.QApplication.UnicodeUTF8))
        self.btnMax.setText(QtGui.QApplication.translate("PoolMotorSlim", "+", None, QtGui.QApplication.UnicodeUTF8))
        self.btnStop.setToolTip(QtGui.QApplication.translate("PoolMotorSlim", "Stops the motor", None, QtGui.QApplication.UnicodeUTF8))
        self.btnStop.setText(QtGui.QApplication.translate("PoolMotorSlim", "S", None, QtGui.QApplication.UnicodeUTF8))
        self.btnHome.setToolTip(QtGui.QApplication.translate("PoolMotorSlim", "Goes Home", None, QtGui.QApplication.UnicodeUTF8))
        self.btnHome.setText(QtGui.QApplication.translate("PoolMotorSlim", "H", None, QtGui.QApplication.UnicodeUTF8))
        self.btnCfg.setToolTip(QtGui.QApplication.translate("PoolMotorSlim", "Configures the motor", None, QtGui.QApplication.UnicodeUTF8))
        self.btnCfg.setText(QtGui.QApplication.translate("PoolMotorSlim", "Cfg", None, QtGui.QApplication.UnicodeUTF8))

from taurus.qt.qtgui.display import TaurusValueLabel
from taurus.qt.qtgui.container import TaurusGroupBox
from taurus.qt.qtgui.button import TaurusLauncherButton

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    PoolMotorSlim = QtGui.QDialog()
    ui = Ui_PoolMotorSlim()
    ui.setupUi(PoolMotorSlim)
    PoolMotorSlim.show()
    sys.exit(app.exec_())

