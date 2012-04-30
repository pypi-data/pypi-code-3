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

"""This module contains a set of useful logging elements based on python's 
:mod:`logging` system."""

__all__ = ["LogIt", "TraceIt", "DebugIt", "InfoIt", "WarnIt", "ErrorIt",
           "CriticalIt", "MemoryLogHandler", "LogExceptHook", "Logger",
           "LogFilter"]

__docformat__ = "restructuredtext"

import os
import sys
import logging.handlers
import weakref
import warnings
import traceback
import inspect
import functools
import threading

from object import Object
from excepthook import BaseExceptHook

TRACE = 5
logging.addLevelName(TRACE, "TRACE")

class LogIt(object):
    """A function designed to be a decorator of any method of a Logger subclass.
    The idea is to log the entrance and exit of any decorated method of a Logger
    subclass.
    Example::
    
        from taurus.core.util import *
        
        class Example(Logger):
            
            @LogIt(Logger.Debug)
            def go(self):
                print "Hello world "
    
    This will generate two log messages of Debug level, one before the function
    go is called and another when go finishes. Example output::
        
        MainThread     DEBUG    2010-11-15 15:36:11,440 Example: -> go
        Hello world of mine
        MainThread     DEBUG    2010-11-15 15:36:11,441 Example: <- go
    
    This decorator can receive two optional arguments **showargs** and **showret**
    which are set to False by default. Enabling them will had verbose infomation
    about the parameters and return value. The following example::

        from taurus.core.util import *
        
        class Example(Logger):
            
            @LogIt(Logger.Debug, showargs=True, showret=True)
            def go(self, msg):
                msg = "Hello world",msg
                print msg
                return msg
                 
    would generate an output like::

        MainThread     DEBUG    2010-11-15 15:42:02,353 Example: -> go('of mine',)
        Hello world of mine
        MainThread     DEBUG    2010-11-15 15:42:02,353 Example: <- go = Hello world of mine
    
    .. note:: 
        it may happen that in these examples that the output of the method
        appears before or after the log messages. This is because log
        messages are, by default, written to the *stardard error* while the print
        message inside the go method outputs to the *standard ouput*. On many
        systems these two targets are not synchronized.
    """
    
    def __init__(self, level=logging.DEBUG, showargs=False, showret=False, col_limit=0):
        self._level = level
        self._showargs = showargs
        self._showret = showret
        self._col_limit = col_limit
        
    def __call__(self, f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            f_self = args[0]
            if f_self.log_level > self._level:
                return f(*args, **kwargs)
            
            has_log = hasattr(f_self, "log")
            fname = f.func_name
            log_obj = f_self
            if not has_log:
                log_obj = logging.getLogger()
                try:
                    fname = "%s.%s" % (f_self.__class__.__name__, fname)
                except:
                    pass
            in_msg = "-> %s" % fname
            if self._showargs:
                if len(args) > 1: in_msg += str(args[1:])
                if len(kwargs):   in_msg += str(kwargs)
            if self._col_limit and len(in_msg) > self._col_limit: in_msg = "%s [...]" % in_msg[:self._col_limit-6]
            log_obj.log(self._level, in_msg)
            out_msg = "<-"
            try:
                ret = f(*args, **kwargs)
            except Exception, e:
                exc_info = sys.exc_info()
                out_msg += " (with %s) %s" % (e.__class__.__name__, fname)
                log_obj.log(self._level, out_msg, exc_info=exc_info)
                raise
            out_msg += " %s" % fname
            if not ret is None and self._showret:
                out_msg += " = %s" % str(ret)
            if self._col_limit and len(out_msg) > self._col_limit:
                out_msg = "%s [...]" % out_msg[:self._col_limit-6]
            log_obj.log(self._level, out_msg)
            return ret
        return wrapper


class TraceIt(LogIt):
    """Specialization of LogIt for trace level messages.
    Example::
    
        from taurus.core.util import TraceIt
        class Example(Logger):
            
            @TraceIt()
            def go(self):
                print "Hello world"
    
    .. seealso:: :class:`LogIt`"""
    def __init__(self, showargs=False, showret=False):
        LogIt.__init__(self, level=TRACE, showargs=showargs, showret=showret)


class DebugIt(LogIt):
    """Specialization of LogIt for debug level messages.
    Example::
    
        from taurus.core.util import DebugIt
        class Example(Logger):
            
            @DebugIt()
            def go(self):
                print "Hello world"
                
    .. seealso:: :class:`LogIt`"""
    def __init__(self, showargs=False, showret=False):
        LogIt.__init__(self, level=logging.DEBUG, showargs=showargs, showret=showret)


class InfoIt(LogIt):
    """Specialization of LogIt for info level messages.
    Example::
    
        from taurus.core.util import InfoIt
        class Example(Logger):
            
            @InfoIt()
            def go(self):
                print "Hello world"
    
    .. seealso:: :class:`LogIt`"""
    def __init__(self, showargs=False, showret=False):
        LogIt.__init__(self, level=logging.INFO, showargs=showargs, showret=showret)


class WarnIt(LogIt):
    """Specialization of LogIt for warn level messages.
    Example::
    
        from taurus.core.util import WarnIt
        class Example(Logger):
            
            @WarnIt()
            def go(self):
                print "Hello world"
    
    .. seealso:: :class:`LogIt`"""
    def __init__(self, showargs=False, showret=False):
        LogIt.__init__(self, level=logging.WARN, showargs=showargs, showret=showret)


class ErrorIt(LogIt):
    """Specialization of LogIt for error level messages.
    Example::
    
        from taurus.core.util import ErrorIt
        class Example(Logger):
            
            @ErrorIt()
            def go(self):
                print "Hello world"
    
    .. seealso:: :class:`LogIt`"""
    def __init__(self, showargs=False, showret=False):
        LogIt.__init__(self, level=logging.ERROR, showargs=showargs, showret=showret)


class CriticalIt(LogIt):
    """Specialization of LogIt for critical level messages.
    Example::
    
        from taurus.core.util import CriticalIt
        class Example(Logger):
            
            @CriticalIt()
            def go(self):
                print "Hello world"
    
    .. seealso:: :class:`LogIt`"""
    def __init__(self, showargs=False, showret=False):
        LogIt.__init__(self, level=logging.CRITICAL, showargs=showargs, showret=showret)


class MemoryLogHandler(list, logging.handlers.BufferingHandler):
    """An experimental log handler that stores temporary records in memory.
       When flushed it passes the records to another handler"""
       
    def __init__(self, capacity=1000):
        list.__init__(self)
        logging.handlers.BufferingHandler.__init__(self, capacity=capacity)
        self._handler_list_changed = False
    
    def shouldFlush(self, record):
        """Determines if the given record should trigger the flush
        
           :param record: (logging.LogRecord) a log record
           :return: (bool) wheter or not the handler should be flushed
        """
        return (len(self.buffer) >= self.capacity) or \
                (record.levelno >= Logger.getLogLevel()) or \
                self._handler_list_changed
    
    def flush(self):
        """Flushes this handler"""
        for record in self.buffer:
            for handler in self:
                handler.handle(record)
        self.buffer = []

    def close(self):
        """Closes this handler"""
        self.flush()
        del self[:]
        BufferingHandler.close(self)


class LogExceptHook(BaseExceptHook):
    """A callable class that acts as an excepthook that logs the exception in
    the python logging system.
    
    :param hook_to: callable excepthook that will be called at the end of
                    this hook handling [default: None]
    :type hook_to: callable
    :param name: logger name [default: None meaning use class name]
    :type name: str
    :param level: log level [default: logging.ERROR]
    :type level: int"""
    
    def __init__(self, hook_to=None, name=None, level=logging.ERROR):
        BaseExceptHook.__init__(self, hook_to=hook_to)
        name = name or self.__class__.__name__
        self._level = level
        self._log = Logger(name=name)
        
    def report(self, *exc_info):
        text = "".join(traceback.format_exception(*exc_info))
        if text[-1] == '\n':
            text = text[:-1]
        self._log.log(self._level, "Unhandled exception:\n%s", text)


class Logger(Object):
    """The taurus logger class. All taurus pertinent classes should inherit
    directly or indirectly from this class if they need taurus logging
    facilities."""
    
    #: Internal usage
    root_inited    = False
    
    #: Internal usage
    root_init_lock = threading.Lock()
    
    #: Critical message level (constant)
    Critical = logging.CRITICAL
    
    #: Error message level (constant)
    Error    = logging.ERROR
    
    #: Warning message level (constant)
    Warning  = logging.WARNING
    
    #: Info message level (constant)
    Info     = logging.INFO
    
    #: Debug message level (constant)
    Debug    = logging.DEBUG
    
    #: Trace message level (constant)
    Trace    = TRACE
    
    #: Default log level (constant)
    DftLogLevel = Info
    
    #: Default log format (constant)
    DftLogFormat = logging.Formatter('%(threadName)-14s %(levelname)-8s %(asctime)s %(name)s: %(message)s')
    
    #: Current global log level
    log_level = DftLogLevel
    
    #: Default log message format
    log_format = DftLogFormat
    
    #: the main stream handler
    stream_handler = None
    
    
    def __init__(self, name='', parent=None, format=None):
        """The Logger constructor
        
        :param name: (str) the logger name (default is empty string)
        :param parent: (Logger) the parent logger or None if no parent exists (default is None)
        :param format: (str) the log message format or None to use the default log format (default is None)
        """
        self.call__init__(Object)
        
        if format: self.log_format = format
        Logger.initRoot()
        
        if name is None or len(name) == 0:
            name = self.__class__.__name__
        self.log_name = name
        if parent is not None:
            self.log_full_name = '%s.%s' % (parent.log_full_name, name)
        else:
            self.log_full_name = name

        self.log_obj = logging.getLogger(self.log_full_name)
        self.log_handlers = []

        self.log_parent = None
        self.log_children = {}
        if parent is not None:
            self.log_parent = weakref.ref(parent)
            parent.addChild(self)

    def cleanUp(self):
        """The cleanUp. Default implementation does nothing
           Overwrite when necessary
        """
        pass

    @classmethod
    def initRoot(cls):
        """Class method to initialize the root logger. Do **NOT** call this
           method directly in your code
        """
        if cls.root_inited:
            return cls._getRootLog()
        
        try:
            cls.root_init_lock.acquire()
            root_logger = cls._getRootLog()
            logging.addLevelName(cls.Trace, "TRACE")
            cls.stream_handler = logging.StreamHandler(sys.__stderr__)
            cls.stream_handler.setFormatter(cls.log_format)
            root_logger.addHandler(cls.stream_handler)
            
            console_log_level = os.environ.get("TAURUSLOGLEVEL", None)
            if console_log_level is not None:
                console_log_level = console_log_level.capitalize()
                if hasattr(cls, console_log_level):
                    cls.log_level = getattr(cls, console_log_level)
            root_logger.setLevel(cls.log_level)
            Logger.root_inited = True
        finally:
            cls.root_init_lock.release()
        return root_logger

    @classmethod
    def addRootLogHandler(cls, h):
        """Adds a new handler to the root logger
        
           :param h: (logging.Handler) the new log handler
        """
        h.setFormatter(cls.getLogFormat())
        cls.initRoot().addHandler(h)
        
    @classmethod
    def removeRootLogHandler(cls, h):
        """Removes the given handler from the root logger
        
           :param h: (logging.Handler) the handler to be removed
        """
        cls.initRoot().removeHandler(h)

    @classmethod
    def enableLogOutput(cls):
        """Enables the :class:`logging.StreamHandler` which dumps log records,
           by default, to the stderr.
        """
        cls.initRoot().addHandler(cls.stream_handler)

    @classmethod
    def disableLogOutput(cls):
        """Disables the :class:`logging.StreamHandler` which dumps log records,
           by default, to the stderr.
        """
        cls.initRoot().removeHandler(cls.stream_handler)

    @classmethod
    def setLogLevel(cls,level):
        """sets the new log level (the root log level)
        
           :param level: (int) the new log level
        """
        cls.log_level = level
        cls.initRoot().setLevel(level)
    
    @classmethod
    def getLogLevel(cls):
        """Retuns the current log level (the root log level)
        
           :return: (int) a number representing the log level
        """
        return cls.log_level
    
    @classmethod
    def setLogFormat(cls,format):
        """sets the new log message format
        
           :param level: (str) the new log message format
        """
        cls.log_format = logging.Formatter(format)
        root_logger = cls.initRoot()
        for h in root_logger.handlers:
            h.setFormatter(cls.log_format)

    @classmethod
    def getLogFormat(cls):
        """Retuns the current log message format (the root log format)
        
           :return: (str) the log message format
        """
        return cls.log_format
    
    @classmethod
    def resetLogLevel(cls):
        """Resets the log level (the root log level)"""
        cls.setLogLevel(cls.DftLogLevel)

    @classmethod
    def resetLogFormat(cls):
        """Resets the log message format (the root log format)"""
        cls.setLogFormat(cls.DftLogFormat)
            
    @classmethod
    def addLevelName(cls, level_no, level_name):
        """Registers a new log level
           
           :param level_no: (int) the level number
           :param level_name: (str) the corresponding name
        """
        logging.addLevelName(level_no, level_name)
        level_name = level_name.capitalize()
        if not hasattr(cls, level_name):
            setattr(cls, level_name, level_no)
    
    @classmethod
    def getRootLog(cls):
        """Retuns the root logger
        
           :return: (logging.Logger) the root logger
        """
        cls.initRoot()
        return cls._getRootLog()

    @classmethod
    def _getRootLog(cls):
        return logging.getLogger()
    
    def getLogObj(self):
        """Returns the log object for this object
        
           :return: (logging.Logger) the log object
        """
        return self.log_obj
    
    def getParent(self):
        """Returns the log parent for this object or None if no parent exists
        
           :return: (logging.Logger or None) the log parent for this object
        """
        if self.log_parent is None:
            return None
        return self.log_parent()

    def getChildren(self):
        """Returns the log children for this object
           
           :return: (sequence<logging.Logger) the list of log children
        """
        children = []
        for _, ref in self.log_children.iteritems():
            child = ref()
            if child is not None:
                children.append(child)
        return children
        
    def addChild(self, child):
        """Adds a new logging child
           
           :param child: (logging.Logger) the new child
        """
        if not self.log_children.get(id(child)):
            self.log_children[id(child)]=weakref.ref(child)

    def addLogHandler(self, handler):
        """Registers a new handler in this object's logger
        
           :param handler: (logging.Handler) the new handler to be added
        """
        self.log_obj.addHandler(handler)
        self.log_handlers.append(handler)

    def copyLogHandlers(self, other):
        """Copies the log handlers of other object to this object
           
           :param other: (object) object which contains 'log_handlers'
        """
        for handler in other.log_handlers:
            self.addLogHandler(handler)
            
    def trace(self, msg, *args, **kw):
        """Record a trace message in this object's logger. Accepted *args* and
           *kwargs* are the same as :meth:`logging.Logger.log`.
        
           :param msg: (str) the message to be recorded
           :param args: list of arguments
           :param kw: list of keyword arguments
        """
        self.log_obj.log(self.Trace, msg, *args, **kw)
    
    def traceback(self, level=Trace, extended=True):
        """Log the usual traceback information, followed by a listing of all the
           local variables in each frame.
        
           :param level: (int) the log level assigned to the traceback record
           :param extended: (bool) if True, the log record message will have multiple lines
           
           :return: (str) The traceback string representation
        """
        out = traceback.format_exc()
        if extended:
            out += "\n"
            out += self._format_trace()
            
        self.log_obj.log(level, out)
        return out

    def stack(self, target=Trace):
        """Log the usual stack information, followed by a listing of all the
           local variables in each frame.
           
           :param target: (int) the log level assigned to the record
           
           :return: (str) The stack string representation
        """
        out = self._format_stack()
        self.log_obj.log(target, out)
        return out
    
    def _format_trace(self):
        return self._format_stack(inspect.trace)
    
    def _format_stack(self, stack_func=inspect.stack):
        line_count = 3
        stack = stack_func(line_count)
        out = ''
        for frame_record in stack:
            out += '\n\t' + 60*'-'
            frame, filename, line, funcname, lines, index = frame_record
            #out += '\n\t    depth = %d' % frame[5]
            out += '\n\t filename = %s' % filename
            out += '\n\t function = %s' % funcname
            if lines is None:
                code = '<code could not be found>'
                out += '\n\t     line = [%d]: %s' % (line, code)
            else:
                lines, line_nb = [ s.strip(' \n') for s in lines ], len(lines)
                if line_nb >= 3:
                    out += '\n\t     line = [%d]: %s' % (line-1, lines[0])
                    out += '\n\t  -> line = [%d]: %s' % (line, lines[1])
                    out += '\n\t     line = [%d]: %s' % (line+1, lines[2])
                elif line_nb > 0:
                    out += '\n\t  -> line = [%d]: %s' % (line, lines[0])
            if frame:
                out += '\n\t   locals = '
                for k,v in frame.f_locals.items():
                    out += '\n\t\t%20s = ' % k
                    try:
                        cut = False
                        v = str(v)
                        i = v.find('\n')
                        if i == -1: 
                            i = 80
                        else:
                            i = min(i, 80)
                            cut = True
                        if len(v) > 80: cut = True
                        out += v[:i]
                        if cut: out += '[...]'
                    except:
                        out += '<could not find suitable string representation>'
        return out
    
    def log(self, level, msg, *args, **kw):
        """Record a log message in this object's logger. Accepted *args* and
           *kwargs* are the same as :meth:`logging.Logger.log`.
        
           :param level: (int) the record level
           :param msg: (str) the message to be recorded
           :param args: list of arguments
           :param kw: list of keyword arguments
        """
        self.log_obj.log(level, msg, *args, **kw)
    
    def debug(self, msg, *args, **kw):
        """Record a debug message in this object's logger. Accepted *args* and
           *kwargs* are the same as :meth:`logging.Logger.debug`.
        
           :param msg: (str) the message to be recorded
           :param args: list of arguments
           :param kw: list of keyword arguments
        """
        self.log_obj.debug(msg, *args, **kw)

    def info(self, msg, *args, **kw):
        """Record an info message in this object's logger. Accepted *args* and
           *kwargs* are the same as :meth:`logging.Logger.info`.
        
           :param msg: (str) the message to be recorded
           :param args: list of arguments
           :param kw: list of keyword arguments
        """
        self.log_obj.info(msg, *args, **kw)

    def warning(self, msg, *args, **kw):
        """Record a warning message in this object's logger. Accepted *args* and
           *kwargs* are the same as :meth:`logging.Logger.warning`.
        
           :param msg: (str) the message to be recorded
           :param args: list of arguments
           :param kw: list of keyword arguments
        """
        self.log_obj.warning(msg, *args, **kw)

    def deprecated(self, msg, *args, **kw):
        """Record a deprecated warning message in this object's logger. Accepted *args* and
           *kwargs* are the same as :meth:`logging.Logger.warning`.
        
           :param msg: (str) the message to be recorded
           :param args: list of arguments
           :param kw: list of keyword arguments
        """
        filename, lineno, func = self.log_obj.findCaller()
        depr_msg = warnings.formatwarning(msg, DeprecationWarning, filename, lineno)
        self.log_obj.warning(depr_msg, *args, **kw)

    def error(self, msg, *args, **kw):
        """Record an error message in this object's logger. Accepted *args* and
           *kwargs* are the same as :meth:`logging.Logger.error`.
        
           :param msg: (str) the message to be recorded
           :param args: list of arguments
           :param kw: list of keyword arguments
        """
        self.log_obj.error(msg, *args, **kw)

    def critical(self, msg, *args, **kw):
        """Record a critical message in this object's logger. Accepted *args* and
           *kwargs* are the same as :meth:`logging.Logger.critical`.
        
           :param msg: (str) the message to be recorded
           :param args: list of arguments
           :param kw: list of keyword arguments
        """
        self.log_obj.critical(msg, *args, **kw)
    
    def exception(self, msg, *args):
        """Log a message with severity 'ERROR' on the root logger, with 
           exception information.. Accepted *args* are the same as 
           :meth:`logging.Logger.exception`.
        
           :param msg: (str) the message to be recorded
           :param args: list of arguments
        """
        self.log_obj.exception(msg, *args)
    
    def flushOutput(self):
        """Flushes the log output"""
        self.syncLog()

    def syncLog(self):
        """Synchronises the log output"""
        logger = self
        synced = []
        while logger is not None:
            for handler in logger.log_handlers:
                if handler in synced:
                    continue
                try:
                    sync = getattr(handler, 'sync')
                except:
                    continue
                sync()
                synced.append(handler)
            logger = logger.getParent()
        
    def getLogName(self):
        """Gets the log name for this object
        
           :return: (str) the log name
        """
        return self.log_name
    
    def getLogFullName(self):
        """Gets the full log name for this object
        
           :return: (str) the full log name
        """
        return self.log_full_name

    def changeLogName(self,name):
        """Change the log name for this object.
        
           :param name: (str) the new log name
        """ 
        self.log_name = name
        p = self.getParent()
        if p is not None:
            self.log_full_name = '%s.%s' % (p.log_full_name, name)
        else:
            self.log_full_name = name
        
        self.log_obj = logging.getLogger(self.log_full_name)
        for handler in self.log_handlers:
            self.log_obj.addHandler(handler)
        
        for child in self.getChildren():
            child.changeLogName(child.log_name)


class LogFilter(logging.Filter):
    """Experimental log filter"""
    
    def __init__(self, level):
        self.filter_level = level
        logging.Filter.__init__(self)

    def filter(self, record):
        ok = (record.levelno == self.filter_level)
        return ok
