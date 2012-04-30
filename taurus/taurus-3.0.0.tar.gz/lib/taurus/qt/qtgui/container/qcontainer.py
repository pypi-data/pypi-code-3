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

"""This module provides basic pure Qt container widgets"""

__all__ = ["QGroupWidget"]

__docformat__ = 'restructuredtext'

import copy
import sys

from taurus.qt import Qt
from taurus.qt.qtgui.resource import getThemePixmap, getThemeIcon, getStandardIcon

_TitleBarStyleExpanded = """.QFrame {{
border-width: 0px;
border-style: solid;
border-color: {stop_color};
border-top-left-radius: {border_radius};
border-top-right-radius: {border_radius};
border-bottom-left-radius: 0px;
border-bottom-right-radius: 0px;
background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                  stop: 0 {start_color}, stop: 1 {stop_color});
}}"""

_TitleBarStyleCollapsed = """.QFrame {{
border-width: 0px;
border-style: solid;
border-color: {stop_color};
border-top-left-radius: {border_radius};
border-top-right-radius: {border_radius};
border-bottom-left-radius: {border_radius};
border-bottom-right-radius: {border_radius};
background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                  stop: 0 {start_color}, stop: 1 {stop_color});
}}"""

_TitleLabelStyle = """.QLabel {{ color : {font_color}; }}"""

_ContentBarStyleWithTitle = """.QFrame {{
border-top-width: 0px;
border-left-width: 1px;
border-right-width: 1px;
border-bottom-width: 1px;
border-style: solid;
border-color: {border_color};
border-top-left-radius: 0px;
border-top-right-radius: 0px;
border-bottom-left-radius: {border_radius};
border-bottom-right-radius: {border_radius};
background-color: qlineargradient(x1: 0, y1: 0, x2: 1.0, y2: 1.0,
                                  stop: 0 {start_color}, stop: 1 {stop_color});
/*
  background-position: center center;
*/
}}"""

_ContentBarStyleWithoutTitle = """.QFrame {{
border-width: 1px;
border-style: solid;
border-color: {border_color};
border-top-left-radius: {border_radius};
border-top-right-radius: {border_radius};
border-bottom-left-radius: {border_radius};
border-bottom-right-radius: {border_radius};
background-color: qlineargradient(x1: 0, y1: 0, x2: 1.0, y2: 1.0,
                                  stop: 0 {start_color}, stop: 1 {stop_color});
/*
  background-position: center center;
*/
}}"""


class QGroupWidget(Qt.QWidget):
    """An expandable/collapsible composite widget"""
    
    DefaultTitleBarVisible = True
    DefaultTitleBarHeight = 16
    DefaultTitleBarStyle = {
        'start_color'  : 'rgb(60, 150, 255)',
        'stop_color'   : 'rgb(0, 65, 200)',
        'font_color'   : 'white',
        'border_radius': '4px',
    }

    DefaultContentVisible = True
    DefaultContentStyle = {
        'start_color' : 'rgb(224, 224, 224)',
        'stop_color'  : 'rgb(255, 255, 255)',
        'border_color' : 'rgb(0, 85, 227)',
        'border_radius': '4px',
    }

    def __init__(self, parent=None, designMode=False):
        Qt.QWidget.__init__(self, parent)
        self._titleVisible = self.DefaultTitleBarVisible
        self._contentVisible = self.DefaultContentVisible
        self._titleBarStyle = self.DefaultTitleBarStyle
        self._contentStyle = self.DefaultContentStyle
        self.__init()
        self._updateStyle()
        self.resetContentVisible()
        self.resetTitleHeight()
        self.resetTitleVisible()
        
    def __init(self):
        panelLayout = Qt.QVBoxLayout()
        panelLayout.setSpacing(0)
        panelLayout.setMargin(0)
        self.setLayout(panelLayout)
        
        self._titleBar = titleBar = Qt.QFrame()
        panelLayout.addWidget(titleBar, 0)
        
        l = Qt.QHBoxLayout()
        l.setMargin(2)
        l.setSpacing(2)
        self._titleBar.setLayout(l)
        
        self._titleButton = Qt.QToolButton()
        self._titleButton.setStyleSheet("border: 0px")
        styleOption = Qt.QStyleOption()
        styleOption.initFrom(self._titleButton)
        style = Qt.QApplication.style()
        icon = style.standardIcon(Qt.QStyle.SP_DesktopIcon, styleOption, self._titleButton)
        self._titleButton.setIcon(icon)
        self._titleLabel = Qt.QLabel()
        self._upDownButton = Qt.QToolButton()
        self._upDownButton.setStyleSheet("border: 0px")
        Qt.QObject.connect(self._upDownButton, Qt.SIGNAL("clicked()"), self.switchContentVisible)
        l.addWidget(self._titleButton, 0)
        l.addWidget(self._titleLabel, 1)
        l.addWidget(self._upDownButton, 0)
        
        self._content = content = Qt.QFrame()
        panelLayout.addWidget(content, 1)
    
    def _updateStyle(self):
        """Internal method that updates the style """
        if self.contentVisible:
            ts = _TitleBarStyleExpanded
        else:
            ts = _TitleBarStyleCollapsed
        fullTitleBarStyle = ts.format(**self._titleBarStyle)
        fullTitleLabelStyle = _TitleLabelStyle.format(**self._titleBarStyle)
        if self.titleVisible:
            contentStyleTemplate = _ContentBarStyleWithTitle
        else:
            contentStyleTemplate = _ContentBarStyleWithoutTitle
        
        contentStyle = self._contentStyle.copy()
        contentStyle['border_color'] = self._titleBarStyle['stop_color']
        fullContentStyle = contentStyleTemplate.format(**contentStyle)
        self._titleBar.setStyleSheet(fullTitleBarStyle)
        self._titleLabel.setStyleSheet(fullTitleLabelStyle)
        self._content.setStyleSheet(fullContentStyle)

    @classmethod
    def getQtDesignerPluginInfo(cls):
        return { 'module'    : 'taurus.qt.qtgui.container',
                 'group'     : 'Taurus Containers',
                 'icon'      : ":/designer/groupwidget.png",
                 'container' : True }
        
        ret = TaurusBaseContainer.getQtDesignerPluginInfo()
        ret['icon'] = ":/designer/groupwidget.png"
        ret['container'] = cls is QGroupWidget
        return ret
        
    def content(self):
        """Returns the contents widget
        
        :return: (Qt.QFrame) the content widget"""
        return self._content
    
    def titleBar(self):
        """Returns the title bar widget
        
        :return: (Qt.QFrame) the title bar widget"""
        return self._titleBar

    def titleButton(self):
        """Returns the title button widget
        
        :return: (Qt.QToolButton) the title button widget"""
        return self._titleButton

    def collapseButton(self):
        """Returns the collapse button widget
        
        :return: (Qt.QToolButton) the collapse button widget"""
        return self._upDownButton

    def setTitle(self, title):
        """Sets this widget's title
        
        :param title: (str) the new widget title"""
        self._titleLabel.setText(title)
        
    def getTitle(self):
        """Returns this widget's title
        
        :return: (str) this widget's title"""
        return self._titleLabel.text()

    def setTitleIcon(self, icon):
        """Sets this widget's title icon
        
        :param icon: (Qt.QIcon) the new widget title icon"""
        self._titleButton.setIcon(icon)
        
    def getTitleIcon(self):
        """Returns this widget's title icon
        
        :return: (Qt.QIcon) this widget's title icon"""
        return self._titleButton.icon()

    def switchContentVisible(self):
        """Switches this widget's contents visibility"""
        self.setContentVisible(not self.isContentVisible())
        
    def isContentVisible(self):
        """Returns this widget's contents visibility
        
        :return: (bool) this widget's contents visibility"""
        return self._contentVisible
    
    def resetContentVisible(self):
        """Resets this widget's contents visibility"""
        self.setContentVisible(self.DefaultContentVisible)
        
    def setContentVisible(self, show):
        """Sets this widget's contents visibility
        
        :param show: (bool) the new widget contents visibility"""
        self._contentVisible = show
        self._updateStyle()
        
        #if show: icon_name = "go-previous"
        #else: icon_name = "go-down"
        #icon = getThemeIcon(icon_name)
        
        if show: icon_name = Qt.QStyle.SP_TitleBarShadeButton
        else: icon_name = Qt.QStyle.SP_TitleBarUnshadeButton
        icon = getStandardIcon(icon_name, self._upDownButton)
        
        self._upDownButton.setIcon(icon)
        self._content.setVisible(show)
        self.adjustSize()
    
    def isTitleVisible(self):
        """Returns this widget's title visibility
        
        :return: (bool) this widget's title visibility"""
        return self._titleVisible
    
    def resetTitleVisible(self):
        """Resets this widget's title visibility"""
        self.setTitleVisible(self.DefaultTitleBarVisible)

    def setTitleVisible(self, show):
        """Sets this widget's title visibility
        
        :param icon: (bool) the new widget title visibility"""
        self._titleVisible = show
        self._titleBar.setVisible(show)
        self._updateStyle()
    
    def getTitleHeight(self):
        """Returns this widget's title height
        
        :return: (bool) this widget's title height"""
        return self.titleButton().iconSize().height()
    
    def setTitleHeight(self, h):
        """Sets this widget's title height
        
        :param icon: (bool) the new widget title height"""
        s = Qt.QSize(h, h)
        self.titleButton().setIconSize(s)
        self.collapseButton().setIconSize(s)
    
    def resetTitleHeight(self):
        """Resets this widget's title height"""
        self.setTitleHeight(self.DefaultTitleBarHeight)

    def getTitleStyle(self):
        """Returns this widget's title style
        
        :return: (dict) this widget's title style"""
        return self._titleBarStyle

    def setTitleStyle(self, style_map):
        """Sets this widget's title style
        Used key/values for style_map:
        - 'start_color'  : brush (Ex.: '#E0E0E0', 'rgb(0,0,0)', 'white')
        - 'stop_color'   : brush (Ex.: '#E0E0E0', 'rgb(0,0,0)', 'white')
        - 'font_color'   : brush (Ex.: '#E0E0E0', 'rgb(0,0,0)', 'white')
        - 'border_radius': radius (Ex.: '5px', '5px,2px')
            
        :param style_map: (dict) the new widget title style"""
        style = self.DefaultTitleBarStyle.copy()
        style.update(style_map)
        self._titleBarStyle = style
        self._updateStyle()

    def resetTitleStyle(self):
        """Resets this widget's title style"""
        self.setTitleStyle({})

    def getContentStyle(self):
        """Returns this widget's content style
        
        :return: (dict) this widget's content style"""
        return self._contentStyle

    def setContentStyle(self, style_map):
        """Sets this widget's content style
        Used key/values for style_map:
        - 'start_color'  : brush (Ex.: '#E0E0E0', 'rgb(0,0,0)', 'white')
        - 'stop_color'   : brush (Ex.: '#E0E0E0', 'rgb(0,0,0)', 'white')
        
        :param style_map: (dict) the new widget content style"""
        style = self.DefaultContentStyle.copy()
        style.update(style_map)
        self._contentStyle = style
        self._updateStyle()
    
    def resetContentStyle(self):
        """Resets this widget's content style"""
        self.setContentStyle({})
        
    #: This property contains the widget's title
    #:
    #: **Access functions:**
    #:
    #:     * :meth:`taurus.qt.qtgui.container.QGroupWidget.getTitle`
    #:     * :meth:`taurus.qt.qtgui.container.QGroupWidget.setTitle`
    title = Qt.pyqtProperty("QString", getTitle, setTitle)

    #: This property contains the widget's title icon
    #:
    #: **Access functions:**
    #:
    #:     * :meth:`taurus.qt.qtgui.container.QGroupWidget.getTitleIcon`
    #:     * :meth:`taurus.qt.qtgui.container.QGroupWidget.setTitleIcon`
    titleIcon = Qt.pyqtProperty("QIcon", getTitleIcon, setTitleIcon)

    #: This property contains the widget's title height
    #:
    #: **Access functions:**
    #:
    #:     * :meth:`taurus.qt.qtgui.container.QGroupWidget.getTitleHeight`
    #:     * :meth:`taurus.qt.qtgui.container.QGroupWidget.setTitleHeight`
    #:     * :meth:`taurus.qt.qtgui.container.QGroupWidget.resetTitleHeight`
    titleHeight = Qt.pyqtProperty("int", getTitleHeight, setTitleHeight, resetTitleHeight)

    #: This property contains the widget's title visibility
    #:
    #: **Access functions:**
    #:
    #:     * :meth:`taurus.qt.qtgui.container.QGroupWidget.isTitleVisible`
    #:     * :meth:`taurus.qt.qtgui.container.QGroupWidget.setTitleVisible`
    titleVisible = Qt.pyqtProperty("bool", isTitleVisible, setTitleVisible)

    ##: This property contains the widget's title style
    ##:
    ##: **Access functions:**
    ##:
    ##:     * :meth:`taurus.qt.qtgui.container.QGroupWidget.getTitleStyle`
    ##:     * :meth:`taurus.qt.qtgui.container.QGroupWidget.setTitleStyle`
    ##:     * :meth:`taurus.qt.qtgui.container.QGroupWidget.resetTitleStyle`
    #titleStyle = Qt.pyqtProperty("QMap", getTitleStyle, setTitleStyle, resetTitleStyle)

    #: This property contains the widget's content's visibility
    #:
    #: **Access functions:**
    #:
    #:     * :meth:`taurus.qt.qtgui.container.QGroupWidget.isContentVisible`
    #:     * :meth:`taurus.qt.qtgui.container.QGroupWidget.setContentVisible`
    #:     * :meth:`taurus.qt.qtgui.container.QGroupWidget.resetContentVisible`
    contentVisible = Qt.pyqtProperty("bool", isContentVisible, setContentVisible, resetContentVisible)
   
    ##: This property contains the widget's content style
    ##:
    ##: **Access functions:**
    ##:
    ##:     * :meth:`taurus.qt.qtgui.container.QGroupWidget.getContentStyle`
    ##:     * :meth:`taurus.qt.qtgui.container.QGroupWidget.setContentStyle`
    ##:     * :meth:`taurus.qt.qtgui.container.QGroupWidget.resetContentStyle`
    #contentStyle = Qt.pyqtProperty("QMap", getContentStyle, setContentStyle, resetContentStyle)


def demo():
    "QGroup Widget"
    w = Qt.QWidget()
    l = Qt.QVBoxLayout()
    w.setLayout(l)
    
    panel = QGroupWidget()
    panel.title = "Database"
    contentLayout = Qt.QFormLayout()
    panel.content().setLayout(contentLayout)
    contentLayout.addRow("&Host", Qt.QLineEdit())
    contentLayout.addRow("&Port", Qt.QLineEdit())
    l.addWidget(panel,0)

    panel = QGroupWidget()
    panel.title = "Hello world"
    panel.titleIcon = getThemeIcon("video-x-generic")
    panel.setTitleStyle({
        'start_color' : 'rgb(255, 60, 60)',
        'stop_color'  : 'rgb(200, 0, 0)',
        'font_color'  : 'rgb(140, 0, 0)',
        'border_radius': '10px',
    })
    panel.setContentStyle({
        'border_radius': '0px',
    })
    contentLayout = Qt.QFormLayout()
    panel.content().setLayout(contentLayout)
    contentLayout.addRow("State", Qt.QPushButton("Press here"))
    contentLayout.addRow("Status", Qt.QLineEdit())
    contentLayout.addRow("Coment", Qt.QLineEdit())
    contentLayout.addRow("Build", Qt.QCheckBox())
    contentLayout.addRow("Upper limit", Qt.QSpinBox())
    contentLayout.addRow("Lower limit", Qt.QSpinBox())
    l.addWidget(panel,0)

    panel = QGroupWidget()
    panel.title = "Hello world 2"
    panel.titleIcon = getThemeIcon("network-server")
    panel.titleVisible = False
    contentLayout = Qt.QFormLayout()
    panel.content().setLayout(contentLayout)
    contentLayout.addRow("Something", Qt.QLineEdit())
    contentLayout.addRow("More", Qt.QLineEdit())
    l.addWidget(panel,0)

    panel = QGroupWidget()
    panel.title = "5"
    panel.titleIcon = getThemeIcon("folder")
    contentLayout = Qt.QVBoxLayout()
    panel.content().setLayout(contentLayout)
    panel2 = QGroupWidget()
    panel2.title = "5.1"
    panel2.titleIcon = getThemeIcon("folder")
    panel2.titleHeight = 48
    contentLayout2 = Qt.QFormLayout()
    panel2.content().setLayout(contentLayout2)
    contentLayout2.addRow("Something", Qt.QLineEdit())
    contentLayout2.addRow("More", Qt.QLineEdit())
    contentLayout.addWidget(panel2, 0)
    l.addWidget(panel,0)

    l.addStretch(1)
    
    w.show()
    w.adjustSize()
    return w

def main():
    import sys
    import taurus.qt.qtgui.application
    Application = taurus.qt.qtgui.application.TaurusApplication
    
    app = Application.instance()
    owns_app = app is None
    
    if owns_app:
        app = Application(app_name="Group widget demo", app_version="1.0",
                          org_domain="Taurus", org_name="Tango community")
        
    w = demo()
    w.show()
    
    if owns_app:
        sys.exit(app.exec_())
    else:
        return w

if __name__ == '__main__':
    main()

