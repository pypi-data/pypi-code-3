### -*- coding: utf-8 -*- ####################################################
##############################################################################
#
# Copyright (c) 2008-2010 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################

__docformat__ = "restructuredtext"

# import standard packages
import logging
logger = logging.getLogger('ztfy.scheduler')

import codecs
import traceback

from cStringIO import StringIO
from datetime import datetime, timedelta
from persistent import Persistent
from persistent.list import PersistentList

# import Zope3 interfaces
from transaction.interfaces import ITransactionManager
from zope.annotation.interfaces import IAnnotations
from zope.container.interfaces import IObjectRemovedEvent
from zope.dublincore.interfaces import IZopeDublinCore
from zope.intid.interfaces import IIntIds
from zope.location.interfaces import ISite
from zope.sendmail.interfaces import IMailDelivery

# import local interfaces
from ztfy.scheduler.interfaces import ISchedulerTask, ISchedulerTaskHistoryInfo, \
                                      IScheduledTaskEvent, IUnscheduledTaskEvent, \
                                      ISchedulerTaskSchedulingMode, \
                                      ISchedulerCronTaskInfo, ISchedulerCronTask, \
                                      ISchedulerDateTaskInfo, ISchedulerDateTask, \
                                      ISchedulerLoopTaskInfo, ISchedulerLoopTask

# import Zope3 packages
from ZEO import ClientStorage
from ZODB import DB
from zope.app.publication.zopepublication import ZopePublication
from zope.component import adapter, queryUtility, getUtility
from zope.component.interfaces import ObjectEvent
from zope.container.contained import Contained
from zope.event import notify
from zope.interface import implements, implementer, alsoProvides, noLongerProvides
from zope.location import locate, Location
from zope.schema import getFields, getFieldNames
from zope.schema.fieldproperty import FieldProperty
from zope.site import hooks
from zope.traversing import api as traversing_api

# import local packages
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.simple import SimpleTrigger
from ztfy.mail.message import TextMessage
from ztfy.utils.date import getDuration
from ztfy.utils.property import cached_property
from ztfy.utils.timezone import tztime
from ztfy.utils.traversing import getParent

from ztfy.scheduler import _


class ScheduledTaskEvent(ObjectEvent):

    implements(IScheduledTaskEvent)

    def __init__(self, object, job):
        self.object = object
        self.job = job


class UnscheduledTaskEvent(ObjectEvent):

    implements(IUnscheduledTaskEvent)


class TaskHistoryItem(Persistent, Contained):
    """Task history item"""

    implements(ISchedulerTaskHistoryInfo)

    date = FieldProperty(ISchedulerTaskHistoryInfo['date'])
    status = FieldProperty(ISchedulerTaskHistoryInfo['status'])
    report = FieldProperty(ISchedulerTaskHistoryInfo['report'])


class TaskHistoryContainer(PersistentList, Location):
    """Task history container"""


class BaseTask(Persistent, Location):
    """Scheduler tasks management class"""

    _title = FieldProperty(ISchedulerTask['title'])
    _schedule_mode = FieldProperty(ISchedulerTask['schedule_mode'])
    server_name = FieldProperty(ISchedulerTask['server_name'])
    server_port = FieldProperty(ISchedulerTask['server_port'])
    server_storage = FieldProperty(ISchedulerTask['server_storage'])
    server_username = FieldProperty(ISchedulerTask['server_username'])
    server_password = FieldProperty(ISchedulerTask['server_password'])
    server_realm = FieldProperty(ISchedulerTask['server_realm'])
    report_source = FieldProperty(ISchedulerTask['report_source'])
    report_target = FieldProperty(ISchedulerTask['report_target'])
    report_mailer = FieldProperty(ISchedulerTask['report_mailer'])
    report_errors_only = FieldProperty(ISchedulerTask['report_errors_only'])
    _history_length = FieldProperty(ISchedulerTask['history_length'])

    def __init__(self):
        history = self.history = TaskHistoryContainer()
        locate(history, self, '++history++')

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value
        IZopeDublinCore(self).title = value

    @property
    def schedule_mode(self):
        return self._schedule_mode

    @schedule_mode.setter
    def schedule_mode(self, value):
        if self._schedule_mode is not None:
            mode = queryUtility(ISchedulerTaskSchedulingMode, self._schedule_mode)
            if (mode is not None) and mode.marker_interface.providedBy(self):
                noLongerProvides(self, mode.marker_interface)
        self._schedule_mode = value
        if value:
            mode = getUtility(ISchedulerTaskSchedulingMode, value)
            alsoProvides(self, mode.marker_interface)
            mode.schema(self).active = False
            self.reset()

    @property
    def history_length(self):
        return self._history_length

    @history_length.setter
    def history_length(self, value):
        self._history_length = value
        if value < len(self.history):
            history = self.history
            while value < len(history):
                del history[0]
            self.history = history

    @cached_property
    def internal_id(self):
        intids = getUtility(IIntIds)
        return intids.register(self)

    @property
    def runnable(self):
        mode = queryUtility(ISchedulerTaskSchedulingMode, self.schedule_mode)
        if mode is None:
            return False
        info = mode.schema(self, None)
        if info is None:
            return False
        return info.active

    def getTrigger(self):
        mode = queryUtility(ISchedulerTaskSchedulingMode, self.schedule_mode)
        if mode is None:
            return None
        return mode.getTrigger(self)

    def getSchedulingInfo(self):
        mode = queryUtility(ISchedulerTaskSchedulingMode, self.schedule_mode)
        if mode is None:
            return None
        return mode.schema(self, None)

    def schedule(self):
        scheduler_util = traversing_api.getParent(self)
        scheduler = scheduler_util.getScheduler()
        if scheduler is None:
            return
        notify(UnscheduledTaskEvent(self))
        active = False
        mode = queryUtility(ISchedulerTaskSchedulingMode, self.schedule_mode)
        if mode is None:
            return
        info = mode.schema(self, None)
        if info is None:
            return
        if info.active:
            fields = getFields(mode.schema)
            for name in getFieldNames(mode.schema):
                if getattr(info, name) != fields[name].default:
                    active = True
                    break
        if active:
            trigger = mode.getTrigger(self)
            try:
                job = scheduler.add_job(trigger, self, name=str("%s::%d" % (traversing_api.getName(self), self.internal_id)),
                                        args=None, kwargs=None, jobstore='scheduler_%d' % scheduler_util.internal_id, max_runs=info.max_runs)
            except ValueError:
                self._logException(None, "Can't schedule task %s" % self.title)
            else:
                locate(job, scheduler)
                notify(ScheduledTaskEvent(self, job))

    def reset(self):
        self.schedule()

    def __call__(self):
        report = codecs.getwriter('utf-8')(StringIO())
        self._run(report)

    def _run(self, report):
        """Task execution
        
        Base class is responsible of all transaction management
        """
        root = self.getRoot()
        try:
            task = self.getRealTask(root)
            site = getParent(task, ISite)
            hooks.setSite(site)
            scheduler = traversing_api.getParent(task)
            if task.runnable:
                lock = scheduler.getLock(task)
                if not lock:
                    return
                try:
                    manager = ITransactionManager(task)
                    try:
                        manager.begin()
                        start = datetime.utcnow()
                        task.run(self._v_db, root, site, report)
                        report.write('\n\nTask duration: ' + getDuration(start) + '\n')
                        status = 'OK'
                    except:
                        status = 'Error'
                        task._logException(report, "An error occurred during execution of task %s" % task.title)
                    # Use transaction manager to handle conflict errors
                    for attempt in manager.attempts():
                        with attempt as t:
                            task.storeReport(report, status)
                            task.sendReport(report, status)
                        if t.status == 'Committed':
                            break
                finally:
                    if isinstance(lock, tuple):
                        locker, lock = lock
                        locker.releaseLock(lock)
        except:
            self._logException(None, "Can't execute scheduled job %s" % self.title)
        # Don't write anything in our main transaction
        ITransactionManager(self).abort()

    def getRoot(self, db=None):
        if db is None:
            db = self.connect()
        self._v_conn = getattr(self, '_v_conn', None) or db.open()
        return self._v_conn.root()[ZopePublication.root_name]

    def getRealTask(self, root=None, db=None):
        if root is None:
            root = self.getRoot(db)
        return traversing_api.traverse(root, traversing_api.getPath(self))

    def connect(self):
        self._v_storage = getattr(self, '_v_storage', None) or \
                          ClientStorage.ClientStorage((str(self.server_name), self.server_port),
                                                      storage=self.server_storage,
                                                      username=self.server_username or '',
                                                      password=self.server_password or '',
                                                      realm=self.server_realm,
                                                      wait=False)
        self._v_db = getattr(self, '_v_db', None) or DB(self._v_storage)
        return self._v_db

    def resetConnection(self):
        if hasattr(self, '_v_conn'):
            delattr(self, '_v_conn')
        if hasattr(self, '_v_db'):
            self._v_db.close()
            try:
                delattr(self, '_v_db')
            except:
                pass
        if hasattr(self, '_v_storage'):
            delattr(self, '_v_storage')

    def run(self, db, root, site, report):
        raise NotImplementedError, _("The 'run' method must be implemented by BaseTask subclasses")

    def _logReport(self, report, message, add_timestamp=True, level=logging.INFO):
        if add_timestamp:
            message = '%s - %s' % (tztime(datetime.utcnow()).strftime('%c'), message)
        if report is not None:
            report.write(message + '\n')
        logger.log(level, message)

    def _logException(self, report, message=None):
        message = '%s - %s' % (tztime(datetime.utcnow()).strftime('%c'), message or "An error occurred")
        if report is not None:
            report.write(message + '\n\n')
            report.write(traceback.format_exc() + '\n')
        logger.exception(message)

    def storeReport(self, report, status):
        """Store execution report in task's history and send it by mail"""
        item = TaskHistoryItem()
        item.date = tztime(datetime.utcnow())
        item.status = status
        item.report = unicode(codecs.decode(report.getvalue(), 'utf-8'))
        if len(self.history) >= self.history_length:
            history = self.history
            while len(history) >= self.history_length:
                del history[0]
            self.history = history
        if self.history_length:
            self.history.append(item)
            locate(item, self.history)

    def sendReport(self, report, status):
        if self.report_target and ((status != 'OK') or (not self.report_errors_only)):
            mailer = queryUtility(IMailDelivery, self.report_mailer)
            if mailer is not None:
                if status == 'Error':
                    subject = "[SCHEDULER ERROR] " + self.title
                else:
                    subject = "[scheduler] " + self.title
                message = TextMessage(subject=subject,
                                      fromaddr=self.report_source,
                                      toaddr=(self.report_target,),
                                      text=report.getvalue())
                mailer.send(self.report_source, (self.report_target,), message.as_string())


#
# Cron-style scheduling mode
#

class CronTaskScheduler(object):
    """Cron-style task class"""

    implements(ISchedulerTaskSchedulingMode)

    marker_interface = ISchedulerCronTask
    schema = ISchedulerCronTaskInfo

    def getTrigger(self, task):
        if not self.marker_interface.providedBy(task):
            raise Exception(_("Task is not configured for cron-style schduling !"))
        info = self.schema(task)
        return CronTrigger(year=info.year or u'*',
                           month=info.month or u'*',
                           day=info.day or u'*',
                           week=info.week or u'*',
                           day_of_week=info.day_of_week or u'*',
                           hour=info.hour or u'*',
                           minute=info.minute or u'*',
                           second=info.second or u'0',
                           start_date=info.start_date and info.start_date.replace(tzinfo=None) or None)

CronTaskScheduler = CronTaskScheduler()


SCHEDULER_TASK_CRON_KEY = 'ztfy.scheduler.mode.cron'

@adapter(ISchedulerCronTask)
@implementer(ISchedulerCronTaskInfo)
def SchedulerTaskCronInfoFactory(context):
    """Scheduler task cron info adapter factory"""
    annotations = IAnnotations(context)
    info = annotations.get(SCHEDULER_TASK_CRON_KEY)
    if info is None:
        info = annotations[SCHEDULER_TASK_CRON_KEY] = SchedulerTaskCronInfo()
    return info


class SchedulerTaskCronInfo(Persistent):
    """Scheduler task cron info"""

    implements(ISchedulerCronTaskInfo)

    active = FieldProperty(ISchedulerCronTaskInfo['active'])
    max_runs = FieldProperty(ISchedulerCronTaskInfo['max_runs'])
    start_date = FieldProperty(ISchedulerCronTaskInfo['start_date'])
    year = FieldProperty(ISchedulerCronTaskInfo['year'])
    month = FieldProperty(ISchedulerCronTaskInfo['month'])
    day = FieldProperty(ISchedulerCronTaskInfo['day'])
    week = FieldProperty(ISchedulerCronTaskInfo['week'])
    day_of_week = FieldProperty(ISchedulerCronTaskInfo['day_of_week'])
    hour = FieldProperty(ISchedulerCronTaskInfo['hour'])
    minute = FieldProperty(ISchedulerCronTaskInfo['minute'])
    second = FieldProperty(ISchedulerCronTaskInfo['second'])


#
# Date-style scheduling mode
#

class DateTaskScheduler(object):
    """Date-style task class"""

    implements(ISchedulerTaskSchedulingMode)

    marker_interface = ISchedulerDateTask
    schema = ISchedulerDateTaskInfo

    def getTrigger(self, task):
        if not self.marker_interface.providedBy(task):
            raise Exception(_("Task is not configured for date-style scheduling !"))
        info = self.schema(task)
        return SimpleTrigger(run_date=info.start_date.replace(tzinfo=None))

DateTaskScheduler = DateTaskScheduler()


SCHEDULER_TASK_DATE_KEY = 'ztfy.scheduler.mode.date'

@adapter(ISchedulerDateTask)
@implementer(ISchedulerDateTaskInfo)
def SchedulerTaskDateInfoFactory(context):
    """Scheduler task date info adapter"""
    annotations = IAnnotations(context)
    info = annotations.get(SCHEDULER_TASK_DATE_KEY)
    if info is None:
        info = annotations[SCHEDULER_TASK_DATE_KEY] = SchedulerTaskDateInfo()
    return info


class SchedulerTaskDateInfo(Persistent):
    """Scheduler task date info"""

    implements(ISchedulerDateTaskInfo)

    active = FieldProperty(ISchedulerDateTaskInfo['active'])
    max_runs = FieldProperty(ISchedulerDateTaskInfo['max_runs'])
    start_date = FieldProperty(ISchedulerDateTaskInfo['start_date'])


#
# Loop-style scheduling mode
#

class LoopTaskScheduler(object):
    """Interval-based task class"""

    implements(ISchedulerTaskSchedulingMode)

    marker_interface = ISchedulerLoopTask
    schema = ISchedulerLoopTaskInfo

    def getTrigger(self, task):
        if not self.marker_interface.providedBy(task):
            raise Exception(_("Task is not configured for loop-style scheduling !"))
        info = self.schema(task)
        return IntervalTrigger(timedelta(weeks=info.weeks,
                                         days=info.days,
                                         hours=info.hours,
                                         minutes=info.minutes,
                                         seconds=info.seconds),
                               start_date=info.start_date and info.start_date.replace(tzinfo=None) or None)

LoopTaskScheduler = LoopTaskScheduler()


SCHEDULER_TASK_LOOP_KEY = 'ztfy.scheduler.mode.loop'

@adapter(ISchedulerLoopTask)
@implementer(ISchedulerLoopTaskInfo)
def SchedulerTaskLoopInfoFactory(context):
    """Scheduler task loop info adapter"""
    annotations = IAnnotations(context)
    info = annotations.get(SCHEDULER_TASK_LOOP_KEY)
    if info is None:
        info = annotations[SCHEDULER_TASK_LOOP_KEY] = SchedulerTaskLoopInfo()
    return info


class SchedulerTaskLoopInfo(Persistent):
    """Scheduler task loop info"""

    implements(ISchedulerLoopTaskInfo)

    active = FieldProperty(ISchedulerLoopTaskInfo['active'])
    max_runs = FieldProperty(ISchedulerLoopTaskInfo['max_runs'])
    start_date = FieldProperty(ISchedulerLoopTaskInfo['start_date'])
    weeks = FieldProperty(ISchedulerLoopTaskInfo['weeks'])
    days = FieldProperty(ISchedulerLoopTaskInfo['days'])
    hours = FieldProperty(ISchedulerLoopTaskInfo['hours'])
    minutes = FieldProperty(ISchedulerLoopTaskInfo['minutes'])
    seconds = FieldProperty(ISchedulerLoopTaskInfo['seconds'])


#
# Scheduler task event subscriber
#

@adapter(ISchedulerTask, IObjectRemovedEvent)
def handleRemovedTask(task, event):
    notify(UnscheduledTaskEvent(task))
