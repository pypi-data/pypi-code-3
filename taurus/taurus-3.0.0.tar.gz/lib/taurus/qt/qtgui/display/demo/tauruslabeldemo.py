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

"""This module provides a demo for the :class:`taurus.qt.qtgui.display.TaurusLabel`
widget """

__all__ = ["demo", "main"]

__docformat__ = 'restructuredtext'

from taurus.qt import Qt

def demo():
    import sys
    import taurus.qt.qtgui.application
    import taurus.qt.qtgui.display

    Application = taurus.qt.qtgui.application.TaurusApplication
    TaurusLabel = taurus.qt.qtgui.display.TaurusLabel
    
    app = Application.instance()
    owns_app = app is None
    
    if owns_app:
        import taurus.core.util.argparse
        app = Application()

    M = 2

    class TaurusLabelTestPanel(Qt.QWidget):
        
        def __init__(self, parent=None):
            Qt.QWidget.__init__(self, parent)
            panel_l = Qt.QVBoxLayout()
            self.setLayout(panel_l)
            panel_l.setContentsMargins(M, M, M, M)
            panel_l.setSpacing(M)

            w = TaurusLabel()
            display_panel = Qt.QGroupBox("Taurus Label Display")
            display_l = Qt.QHBoxLayout()
            display_l.setContentsMargins(M, M, M, M)
            display_l.setSpacing(M)
            display_panel.setLayout(display_l)
            #display_l.addStretch(1)
            display_l.addWidget(w)

            control_panel = Qt.QGroupBox("Control Panel")
            control_l = Qt.QFormLayout()
            control_l.setContentsMargins(M, M, M, M)
            control_l.setSpacing(M)
            control_panel.setLayout(control_l)
            model_widget = Qt.QLineEdit()
            model_index_widget = Qt.QLineEdit()
            fg_widget = Qt.QComboBox()
            bg_widget = Qt.QComboBox()
            prefix_widget = Qt.QLineEdit()
            suffix_widget = Qt.QLineEdit()
            control_l.addRow("model:", model_widget)
            control_l.addRow("model index:", model_index_widget)
            control_l.addRow("foreground role:", fg_widget)
            control_l.addRow("background role:", bg_widget)
            control_l.addRow("prefix text:", prefix_widget)
            control_l.addRow("suffix text:", suffix_widget)

            panel_l.addWidget(display_panel)
            panel_l.addWidget(control_panel)

            fg_widget.addItems(["value", "w_value", "state", "quality", "none"])
            bg_widget.addItems(["quality", "state", "none"])
            
            Qt.QObject.connect(model_widget, Qt.SIGNAL("textChanged(const QString &)"), w.setModel)
            Qt.QObject.connect(fg_widget, Qt.SIGNAL("currentIndexChanged(const QString &)"), w.setFgRole)
            Qt.QObject.connect(bg_widget, Qt.SIGNAL("currentIndexChanged(const QString &)"), w.setBgRole)
            Qt.QObject.connect(prefix_widget, Qt.SIGNAL("textChanged(const QString &)"), w.setPrefixText)
            Qt.QObject.connect(suffix_widget, Qt.SIGNAL("textChanged(const QString &)"), w.setSuffixText)
            Qt.QObject.connect(model_index_widget, Qt.SIGNAL("textChanged(const QString &)"), w.setModelIndex)
            
            model_widget.setText("sys/tg_test/1/double_scalar")
            fg_widget.setCurrentIndex(0)
            bg_widget.setCurrentIndex(0)
            
            self.w_label = w
            self.w_model = model_widget
            self.w_model_index = model_index_widget
            self.w_fg = fg_widget
            self.w_bg = bg_widget
            self.w_prefix = prefix_widget
            self.w_suffix = suffix_widget
    
    panel = Qt.QWidget()
    panel.setWindowTitle(app.applicationName())
    layout=Qt.QGridLayout()
    panel.setLayout(layout)
    layout.setContentsMargins(M, M, M, M)
    layout.setSpacing(M)
    p1 = TaurusLabelTestPanel()
    p1.w_model.setText("sys/tg_test/1/double_scalar")
    p2 = TaurusLabelTestPanel()
    p2.w_model.setText("sys/tg_test/1/double_scalar?configuration=label")
    p2.w_bg.setCurrentIndex(2)
    layout.addWidget(p1, 0, 0)
    layout.addWidget(p2, 0, 1)
    layout.addItem(Qt.QSpacerItem(10,10), 1, 0, 1, 2)
    layout.setRowStretch(1, 1)
    panel.show()
    if owns_app:
        sys.exit(app.exec_())
    else:
        return panel
    
def main():
    return demo()

if __name__ == "__main__":
    main()