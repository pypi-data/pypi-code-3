#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

"""This module provides a taurus QPushButton based widgets"""

__all__ = ["TaurusLauncherButton", "TaurusCommandButton", "TaurusLockButton"]

__docformat__ = 'restructuredtext'

import PyTango

from taurus.qt import Qt
from taurus.core import TaurusDevice, LockStatus, TaurusLockInfo
from taurus.qt.qtgui.base import TaurusBaseWidget
from taurus.core.util import eventfilters
from taurus.core.util import Enumeration
from taurus.qt.qtgui.resource import getIcon
from taurus.qt.qtgui.dialog import TaurusMessageBox

class _ButtonDialog(Qt.QDialog):
    _widget = None
    deleteWidgetOnClose = False
    def __init__(self, parent=None):
        Qt.QDialog.__init__(self, parent, Qt.Qt.WindowTitleHint)
        l = Qt.QVBoxLayout()
        self.setLayout(l)
        
    def setWidget(self, widget):
        oldWidget = self.widget()
        if oldWidget is not None:
            try:
                self._widget.setModel(None)
            except:
                pass
            oldWidget.hide()
            oldWidget.setParent(None)
            oldWidget.deleteLater()
        if widget is not None:
            self.layout().addWidget(widget)
        self._widget = widget
    
    def widget(self):
        return self._widget
        
    def closeEvent(self, event):
        if self.deleteWidgetOnClose:
            self.setWidget(None)
        Qt.QDialog.closeEvent(self, event)

class TaurusLauncherButton(Qt.QPushButton, TaurusBaseWidget):
    '''This class provides a button that launches a modeless dialog containing
    a specified Taurus widget which gets the same model as the button.
    The button does not use the model directly. Instead it passes it to the
    associated widget.
    
    Code examples::
        
        # a button that launches a TaurusAttrForm when clicked
        button =  TaurusLauncherButton(widget = TaurusAttrForm())
        button.setModel('a/b/c') #a device name, which will be given to the TaurusAttrForm when clicking
        
        # a button that launches a taurusValueLabel (whose model is an attribute: 'a/b/c/attrname')
        button =  TaurusLauncherButton(widget = TaurusValueLabel())
        button.setModel('a/b/c/attrname') #a device name, which will be given to the TaurusValueLabel when clicking
        
        #same as the previous one, but using the parent model and putting a custom text and icon:
        button =  TaurusLauncherButton(widget = TaurusValueLabel(), text='click me', icon=':/taurus.png')
        button.setUseParentModel(True)  #let's assume that the button's parent has a model of type "/a/b/c"
        button.setModel('/attrname')
    
    '''
    
    _widgetClassName = ''
    _args = []
    _kwargs = {}
    _deleteWidgetOnClose = True
    _icon = None
    _text = None
    
    def __init__(self, parent = None, designMode = False, widget=None, icon=None, text = None):
        '''Constructor
        
        :param parent: (Qt.QWidget or None) parent of this widget
        :param designMode: (bool) flag for Qt designer
        :param widget: (Qt.QWidget) a QWidget that will be shown when clicking
                       in the button
        :param icon: (Qt.QIcon) icon for the button
        :param text: (str) the button text (if None passed, the widget's class name
                     is used) '''

        name = self.__class__.__name__
        self.call__init__wo_kw(Qt.QPushButton, parent)
        self.call__init__(TaurusBaseWidget, name, designMode=designMode)
        if icon is None and self._icon is not None:
            icon = getIcon(self._icon)
        if icon is not None: 
            self.setIcon(Qt.QIcon(icon))
        if text is None: text = self._text
        self._text = text
        self.setText(self.getDisplayValue())
        self._dialog = _ButtonDialog(self)
        self.setWidget(widget)
        self.connect(self, Qt.SIGNAL('clicked()'), self.onClicked)
        self.setDefault(False)
        self.setAutoDefault(False)
        self.insertEventFilter(eventfilters.IGNORE_CHANGE_AND_PERIODIC) #no need to listen to change events!
        
    def getModelClass(self):
        '''see :meth:`TaurusBaseComponent.getModelClass`. Note that in the case of
        :class:`TaurusLauncherButton`, the class is completely dependent on the
        widget's class'''
        try:
            return self.widget().getModelClass()
        except:
            #return None  #@TODO: Uncommenting this avoids the exception when TaurusBaseWidget.getModelClass chokes with relative classes. But the thing should be solved at TaurusBaseWidget.getModelClass level
            return TaurusBaseWidget.getModelClass(self)
    
    def setText(self, text):
        '''Sets the text of the button. see :meth:`Qt.QPushButton.setText`'''
        self._text = text
        Qt.QPushButton.setText(self, text)
    
    def getWidgetClassName(self):
        return self._widgetClassName
        
    def setWidgetClassName(self, className, args=None, kwargs=None):
        self._widgetClassName = str(className)
        if args is not None: self._args = args
        if kwargs is not None: self._kwargs = kwargs
        
    def resetWidgetClassName(self, className, args=None, kwargs=None):
        self.setWidgetClassName(self.__class__._widgetClassName)
    
    def createWidget(self):
        from taurus.qt.qtgui.util import TaurusWidgetFactory
        klass = TaurusWidgetFactory().getWidgetClass(self._widgetClassName)
        widget = klass(*self._args, **self._kwargs)
        self.setWidget(widget)
    
    def widget(self):
        return self._dialog.widget()
    
    def setWidget(self, widget):
        '''sets the widget that will be shown when clicking the button
        
        :param widget: (Qt.QWidget)
        '''
        self._dialog.setWidget(widget)
        if self._text is None and self.self.widget() is not None:
            self._text = self.widget().__class__.__name__
        
    def displayValue(self,v):
        '''see :meth:`TaurusBaseComponent.displayValue`'''
        if self._text is not None: return self._text #make sure the text is not changed once set
        TaurusBaseWidget.displayValue(self,v)
        
    def getDisplayValue(self):
        '''see :meth:`TaurusBaseComponent.getDisplayValue`'''
        if self._text is not None: return self._text
        modelobj = self.getModelObj()
        if modelobj is None:
            return '---'
        config = modelobj.getConfig()
        if config.isSpectrum():
            return 'Spect[%i]' % modelobj.read().dim_x
        elif config.isImage():
            return 'Imag[%ix%i]'%(modelobj.read().dim_x,modelobj.read().dim_y)
        else:
            self.debug('Unknown model type for TaurusLauncherButton')
            return '---'
        
    def onClicked(self):
        '''
        Slot called when the button is clicked.
        Note that the dialog will only be created once. Subsequent clicks on
        the button will only raise the existing dialog'''
        if self.widget() is None:
            self.createWidget()
        self.widget().setModel(self.getModelName())
        self._dialog.deleteWidgetOnClose = self._deleteWidgetOnClose
        #dialog.resize(400,300)

        # It's always necessary to set the title since the model could have changed
        self._dialog.setWindowTitle(str(self.getModelName()))
        
        self._dialog.show()
        self._dialog.raise_()

    @classmethod
    def getQtDesignerPluginInfo(cls):
        return { 
            'group'     : 'Taurus Buttons',
            'icon'      : ':/designer/pushbutton.png',
            'module'    : 'taurus.qt.qtgui.button',
            'container' : False }
            
    ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    #                      Qt Properties                        #
    ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    Model = Qt.pyqtProperty("QString", TaurusBaseWidget.getModel, TaurusBaseWidget.setModel, TaurusBaseWidget.resetModel)    
    UseParentModel = Qt.pyqtProperty("bool", TaurusBaseWidget.getUseParentModel, TaurusBaseWidget.setUseParentModel, TaurusBaseWidget.resetUseParentModel)
    widgetClassName = Qt.pyqtProperty("QString", getWidgetClassName, setWidgetClassName, resetWidgetClassName)


class TaurusCommandButton(Qt.QPushButton, TaurusBaseWidget):
    '''This class provides a button that executes a tango command on its device.
    
    Code examples::
        
        # a button that executes the "status" command for the 'a/b/c' device server
        button =  TaurusCommandButton(command = 'Status', icon=':/taurus.png')
        button.setModel('a/b/c')
        
        #  a button that executes the "exec" command for the 'a/b/c' device server with one parameter
        button =  TaurusCommandButton(command = 'Status', parameters=['2+2'],icon=':/taurus.png')
        button.setModel('a/b/c')
        
    .. seealso:: :class:`TaurusCommandsForm` provides a good example of use of
                 TaurusCommandButton (including managing the return value) '''
    __pyqtSignals__ = ("commandExecuted()",)
    def __init__(self, parent=None, designMode=False, command=None, parameters=None, icon=None, text=None):
        '''Constructor

        :param parent: (Qt.QWidget or None) parent of this widget
        :param designMode: (bool) flag for Qt designer
        :param command: (str) the name of the command to be executed
        :param parameters: (sequence<str>) the list of parameteres. Default value is None meaning no parameters 
        :param icon: (Qt.QIcon) icon for the button
        :param text: (str) the button text (if None passed, `command` is used)
        '''
        name = self.__class__.__name__
        if command is None: command = ""
        if parameters is None: parameters = []
        if text is None: text = ""
        self._command = command
        self._parameters = parameters
        self.call__init__wo_kw(Qt.QPushButton, parent)
        self.call__init__(TaurusBaseWidget, name, designMode=designMode)
        if icon is not None: self.setIcon(Qt.QIcon(icon))
        self.setCustomText(text)
        self.setDefault(False)
        self.setAutoDefault(False)
        self.connect(self, Qt.SIGNAL('clicked()'), self.onClicked)
        
    def getDisplayValue(self):
        '''see :meth:`TaurusBaseComponent.displayValue`'''
        if len(self._customText) > 0:
            return self._customText
        if len(self._command) == 0:
            return '---'
        modelobj = self.getModelObj()
        if modelobj is None or not hasattr(modelobj, self._command):
            return '---'
        return self._command
    
    import taurus.qt.qtgui.dialog
    
    @taurus.qt.qtgui.dialog.ProtectTaurusMessageBox(title="Unexpected error when executing command")
    def onClicked(self):
        '''Slot called when the button is clicked. It executes the command with
        parameters. It may issue a warning if the command is flagged as
        dangerous. On successful execution, it returns the command result and it
        emits a "commandExecuted" signal with the result as well.
        
        :return: The result of the command. The type depends on the command. It
                 may be None.
        
        .. seealso:: :meth:`setCommand`, :meth:`setParameters`, :meth:`TaurusBaseComponent.isDangerous`
        '''
        
        self.debug("launch command %s"%str(self._command))
        if len(self._command) == 0:
            return
        modelobj = self.getModelObj()
        if modelobj is None or not hasattr(modelobj, self._command):
            self.warning('Device %s does not implement command %s'%(modelobj, self._command))
            return
        
        if self.isDangerous() and not self.getForceDangerousOperations():
            result = Qt.QMessageBox.question(self, "Potentially dangerous action",
                                         "%s\nProceed?"%self.getDangerMessage(),
                                         Qt.QMessageBox.Ok|Qt.QMessageBox.Cancel,
                                         Qt.QMessageBox.Ok)
            if result != Qt.QMessageBox.Ok:
                return
        #After all the checks, we can finally do the action
        try:
            result = modelobj.command_inout(self._command, self._castParameters(self._parameters, self._command, modelobj))
        except Exception, e:
            self.error('Unexpected error when executing command %s of %s: %s'%(self._command, modelobj.getNormalName(), str(e)))
            raise
        self.emit(Qt.SIGNAL('commandExecuted'), result)
        return result
    
    def _castParameters(self, parameters=None, command=None, dev=None):
        '''Internal method used to cast the command paramters to the appropriate
        type required for the given command
        
        :param parameters: (sequence) a sequence of parameters. If None is
                           passed, the currently set parameters are used.
        :param command: (str) the command name. If None is passed, the currently
                        set command is used.
        :param dev: (taurus.core.TaurusDevice) the device on which the command is
                    executed. If None is passed, the current model is used.
        
        :return: (sequence or scalar) a sequence of parameters (or a scalar if only one parameter)
        '''
        if parameters is None: parameters = self._parameters
        if command is None: command = self._command
        if dev is None: dev = self.getModelObj()
        
        try:
            param_type = dev.command_query(command).in_type
        except Exception, e:
            self.warning('Cannot get parameters info for command %s:%s'%(command, str(e)))
            return parameters
        if param_type == PyTango.CmdArgType.DevVoid: return None
        if PyTango.is_int_type(param_type, True): cast_type = int
        elif PyTango.is_float_type(param_type, True): cast_type = float
        elif param_type == PyTango.CmdArgType.DevVarStringArray or param_type == PyTango.CmdArgType.DevString:cast_type = str 
        elif param_type == PyTango.CmdArgType.DevVarBooleanArray or param_type == PyTango.CmdArgType.DevBoolean:cast_type = bool
        else:
            self.info('Unsupported parameters type (%s). Casting to "str"'%str(param_type))
            cast_type = str
        if PyTango.is_scalar_type(param_type):
            if parameters: return cast_type(parameters[0])
            else: return parameters
        else:
            return map(cast_type,parameters)
        
    def setCommand(self, commandName):
        '''sets the command to be executed when the button is clicked
        
        :param commandName: (str or None) the command name
        '''
        if commandName is None:
            self._command = ""
        else:
            self._command = str(commandName)
        self._setText(self.getDisplayValue())
    
    def getCommand(self):
        '''returns the command name to be executed when the button is clicked
        
        :return: (str or None) the command name
        '''
        return self._command
    
    def resetCommand(self):
        '''equivalent to self.setCommand(None)'''
        self.setCommand("")
    
    def setParameters(self, parameters):
        '''
        Sets the parameters to be used on command execution.
        
        :param parameters: (sequence) a sequence of parameters. If the
                           elements of the sequence are not of the right type
                           required for the parameter, an automatic conversion
                           will be attempted on execution time. As a special
                           case, if parameters is a string, it will be splitted
                           on whitespace to obtain a sequence of parameters.
        '''
        if isinstance(parameters,(basestring, Qt.QString)): parameters = str(parameters).split()
        self._parameters = parameters
    
    def getParameters(self):
        '''returns the parameters to be used on command execution
        
        :param parameters: (sequence)
        '''
        return self._parameters
    
    def resetParameters(self):
        '''Equivalent to setParameters(None)
        '''
        self.setParameters([])
        
    def setCustomText(self, customText=None):
        '''Sets a custom text for the button (by default it is the command name)
        
        :param customText: (str or None) the custom text. If None passed, it
                           will use the command name
        '''
        if customText is None:
            customText = ""
        self._customText = customText
        self._setText(self.getDisplayValue())
    
    def getCustomText(self):
        '''Returns the custom text of the buttom, or None if no custom text is
        used
        '''
        return self._customText
    
    def resetCustomText(self):
        '''Equivalent to setCustomText(None)'''
        self.setCustomText(None)

    @classmethod
    def getQtDesignerPluginInfo(cls):
        return { 
            'group'     : 'Taurus Buttons',
            'icon'      : ':/designer/pushbutton.png',
            'module'    : 'taurus.qt.qtgui.button',
            'container' : False }
        
    ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    #                      Qt Properties                        #
    ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    
    Model = Qt.pyqtProperty("QString", TaurusBaseWidget.getModel, TaurusBaseWidget.setModel, TaurusBaseWidget.resetModel)
    
    UseParentModel = Qt.pyqtProperty("bool", TaurusBaseWidget.getUseParentModel, TaurusBaseWidget.setUseParentModel, TaurusBaseWidget.resetUseParentModel)
    
    Command = Qt.pyqtProperty("QString", getCommand, setCommand, resetCommand)
    
    Parameters = Qt.pyqtProperty("QStringList", getParameters, setParameters, resetParameters)  
    
    DangerMessage = Qt.pyqtProperty("QString", TaurusBaseWidget.getDangerMessage, TaurusBaseWidget.setDangerMessage, TaurusBaseWidget.resetDangerMessage)
    
    CustomText = Qt.pyqtProperty("QString", getCustomText, setCustomText, resetCustomText)  


class TaurusLockButton(Qt.QPushButton, TaurusBaseWidget):

    _LOCK_MAP = { LockStatus.Unlocked : ":/lock_unlocked.svg",
                  LockStatus.Locked   : ":/lock_locked_unpreviledged.svg",
                  LockStatus.LockedMaster : ":/lock_locked.svg",
                  LockStatus.Unknown: ":/lock_unknown.svg" }

    def __init__(self, parent = None, designMode = False):
        self._lock_info = TaurusLockInfo()
        name = self.__class__.__name__
        self.call__init__wo_kw(Qt.QPushButton, parent)
        self.call__init__(TaurusBaseWidget, name, designMode=designMode)
        self.connect(self, Qt.SIGNAL("toggled(bool)"), self.on_toggle)
        self.setCheckable(True)
        self.setAutoTooltip(False)
        self.insertEventFilter(eventfilters.IGNORE_ALL)
        self.update_button()
        
    @classmethod
    def getQtDesignerPluginInfo(cls):
        return { 
            'group'     : 'Taurus Buttons',
            'icon'      : ':/designer/pushbutton.png',
            'module'    : 'taurus.qt.qtgui.button',
            'container' : False }

    def getModelClass(self):
        return TaurusDevice
    
    def setModel(self, model):
        TaurusBaseWidget.setModel(self, model)
        self.update_button()
        
    def get_lock_info(self, cache=False):
        dev = self.getModelObj()
        if dev is not None:
            self._lock_info = dev.getLockInfo(cache=cache)
        return self._lock_info
    
    def update_button(self, lock_info=None):
        if lock_info is None:
            lock_info = self.get_lock_info()
        status = lock_info.status
        self.setIcon(getIcon(self._LOCK_MAP[status]))
        self.setDown(status in (LockStatus.Locked, LockStatus.LockedMaster))
        self.setToolTip(lock_info.status_msg)
        self.update()
        return lock_info
    
    def _on_toggle(self, down):
        dev = self.getModelObj()
        if down:
            dev.lock()
        else:
            dev.unlock()
        self.update_button()
        
    def on_toggle(self, down):
        try:
            self._on_toggle(down)
        except:
            import sys
            msgbox = TaurusMessageBox(*sys.exc_info())
            msgbox.setWindowTitle("Error locking device")
            if self.update_button().status == LockStatus.Locked:
                msgbox.setText(self._lock_info.status_msg)
            msgbox.exec_()
        
    model = Qt.pyqtProperty("QString", TaurusBaseWidget.getModel, setModel,
                            TaurusBaseWidget.resetModel)
  
#if __name__ == "__main__":
#    import sys
#    from taurus.widget.qwt import TaurusPlot, TaurusArrayEditor
#    #from taurus.widget import TaurusAttrForm
#    import taurus.widget.resources.qrc_taurusdesigner_icons
#    
#    app = Qt.QApplication(sys.argv)
#    
#    ##Uncomment the following for testing TaurusLauncherButton
#    w=TaurusArrayEditor()
#    form = TaurusLauncherButton(parent=None, designMode=False, widget = w, icon=':/taurus.png', text = 'show')
#    form.setModel('bl97/pc/dummy-03/waveform')
#    #form.setModel('bl97/pc/dummy-03')
#    #form.setModel('bl97/pyattributeprocessor/1/a|bl97/pyattributeprocessor/1/b')
#    
#    ##Uncomment the following for testing TaurusCommandButton
#    ##form = TaurusCommandButton(parent=None, designMode=False, command = 'Exec', parameters=['2+2'], icon=':/taurus.png', text = None)
#    #form = TaurusCommandButton(parent=None, designMode=False, command = 'Status', parameters=None, icon=':/taurus.png', text = None)
#    #form.setModel('bl97/pc/dummy-03')
#    #form.setDangerMessage('Booo scary command!!\n Maybe you should think twice!')
#    #def f(*a):print a
#    #form.connect(form, Qt.SIGNAL('commandExecuted'),f)
#    form.show()
#    
#    sys.exit(app.exec_())
#
#

def demo():
    lock_button = TaurusLockButton()
    lock_button.model = "sys/tg_test/1"
    return lock_button

def main():
    import sys
    import taurus.qt.qtgui.application
    Application = taurus.qt.qtgui.application.TaurusApplication
    
    app = Application.instance()
    owns_app = app is None
    
    if owns_app:
        import taurus.core.util.argparse
        parser = taurus.core.util.argparse.get_taurus_parser()
        parser.usage = "%prog [options] <full_attribute_name(s)>"
        app = Application(sys.argv, cmd_line_parser=parser, 
                          app_name="Taurus lock button demo", app_version="1.0",
                          org_domain="Taurus", org_name="Tango community")
        
    args = app.get_command_line_args()

    if len(args) == 0:
        w = demo()
    else:
        models = map(str.lower, args)

        w = Qt.QWidget()
        layout = Qt.QGridLayout()
        w.setLayout(layout)
        for model in models:
            lock_button = TaurusLockButton()
            lock_button.model = model
            layout.addWidget(lock_button)
    w.show()
    
    if owns_app:
        sys.exit(app.exec_())
    else:
        return w

if __name__ == '__main__':
    main()
