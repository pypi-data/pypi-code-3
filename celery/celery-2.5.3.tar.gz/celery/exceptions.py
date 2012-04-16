# -*- coding: utf-8 -*-
"""
    celery.exceptions
    ~~~~~~~~~~~~~~~~~

    This module contains Celery-specific exceptions.

    :copyright: (c) 2009 - 2012 by Ask Solem.
    :license: BSD, see LICENSE for more details.

"""
from __future__ import absolute_import

UNREGISTERED_FMT = """\
Task of kind %s is not registered, please make sure it's imported.\
"""


class SecurityError(Exception):
    """Security related exceptions.

    Handle with care.

    """


class SystemTerminate(SystemExit):
    """Signals that the worker should terminate."""


class QueueNotFound(KeyError):
    """Task routed to a queue not in CELERY_QUEUES."""


class TimeLimitExceeded(Exception):
    """The time limit has been exceeded and the job has been terminated."""


class SoftTimeLimitExceeded(Exception):
    """The soft time limit has been exceeded. This exception is raised
    to give the task a chance to clean up."""


class WorkerLostError(Exception):
    """The worker processing a job has exited prematurely."""


class ImproperlyConfigured(Exception):
    """Celery is somehow improperly configured."""


class NotRegistered(KeyError):
    """The task is not registered."""

    def __repr__(self):
        return UNREGISTERED_FMT % str(self)


class AlreadyRegistered(Exception):
    """The task is already registered."""


class TimeoutError(Exception):
    """The operation timed out."""


class MaxRetriesExceededError(Exception):
    """The tasks max restart limit has been exceeded."""


class RetryTaskError(Exception):
    """The task is to be retried later."""

    def __init__(self, message, exc, *args, **kwargs):
        self.exc = exc
        Exception.__init__(self, message, exc, *args, **kwargs)


class TaskRevokedError(Exception):
    """The task has been revoked, so no result available."""


class NotConfigured(UserWarning):
    """Celery has not been configured, as no config module has been found."""


class AlwaysEagerIgnored(UserWarning):
    """send_task ignores CELERY_ALWAYS_EAGER option"""


class InvalidTaskError(Exception):
    """The task has invalid data or is not properly constructed."""


class CPendingDeprecationWarning(PendingDeprecationWarning):
    pass


class CDeprecationWarning(DeprecationWarning):
    pass
