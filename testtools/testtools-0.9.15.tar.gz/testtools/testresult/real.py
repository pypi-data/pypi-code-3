# Copyright (c) 2008-2012 testtools developers. See LICENSE for details.

"""Test results and related things."""

__metaclass__ = type
__all__ = [
    'ExtendedToOriginalDecorator',
    'MultiTestResult',
    'Tagger',
    'TestResult',
    'TestResultDecorator',
    'ThreadsafeForwardingResult',
    ]

import datetime
import sys
import unittest

from testtools.compat import all, str_is_unicode, _u
from testtools.content import (
    text_content,
    TracebackContent,
    )
from testtools.tags import TagContext

# From http://docs.python.org/library/datetime.html
_ZERO = datetime.timedelta(0)

# A UTC class.

class UTC(datetime.tzinfo):
    """UTC"""

    def utcoffset(self, dt):
        return _ZERO

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return _ZERO

utc = UTC()


class TestResult(unittest.TestResult):
    """Subclass of unittest.TestResult extending the protocol for flexability.

    This test result supports an experimental protocol for providing additional
    data to in test outcomes. All the outcome methods take an optional dict
    'details'. If supplied any other detail parameters like 'err' or 'reason'
    should not be provided. The details dict is a mapping from names to
    MIME content objects (see testtools.content). This permits attaching
    tracebacks, log files, or even large objects like databases that were
    part of the test fixture. Until this API is accepted into upstream
    Python it is considered experimental: it may be replaced at any point
    by a newer version more in line with upstream Python. Compatibility would
    be aimed for in this case, but may not be possible.

    :ivar skip_reasons: A dict of skip-reasons -> list of tests. See addSkip.
    """

    def __init__(self):
        # startTestRun resets all attributes, and older clients don't know to
        # call startTestRun, so it is called once here.
        # Because subclasses may reasonably not expect this, we call the
        # specific version we want to run.
        TestResult.startTestRun(self)

    def addExpectedFailure(self, test, err=None, details=None):
        """Called when a test has failed in an expected manner.

        Like with addSuccess and addError, testStopped should still be called.

        :param test: The test that has been skipped.
        :param err: The exc_info of the error that was raised.
        :return: None
        """
        # This is the python 2.7 implementation
        self.expectedFailures.append(
            (test, self._err_details_to_string(test, err, details)))

    def addError(self, test, err=None, details=None):
        """Called when an error has occurred. 'err' is a tuple of values as
        returned by sys.exc_info().

        :param details: Alternative way to supply details about the outcome.
            see the class docstring for more information.
        """
        self.errors.append((test,
            self._err_details_to_string(test, err, details)))

    def addFailure(self, test, err=None, details=None):
        """Called when an error has occurred. 'err' is a tuple of values as
        returned by sys.exc_info().

        :param details: Alternative way to supply details about the outcome.
            see the class docstring for more information.
        """
        self.failures.append((test,
            self._err_details_to_string(test, err, details)))

    def addSkip(self, test, reason=None, details=None):
        """Called when a test has been skipped rather than running.

        Like with addSuccess and addError, testStopped should still be called.

        This must be called by the TestCase. 'addError' and 'addFailure' will
        not call addSkip, since they have no assumptions about the kind of
        errors that a test can raise.

        :param test: The test that has been skipped.
        :param reason: The reason for the test being skipped. For instance,
            u"pyGL is not available".
        :param details: Alternative way to supply details about the outcome.
            see the class docstring for more information.
        :return: None
        """
        if reason is None:
            reason = details.get('reason')
            if reason is None:
                reason = 'No reason given'
            else:
                reason = reason.as_text()
        skip_list = self.skip_reasons.setdefault(reason, [])
        skip_list.append(test)

    def addSuccess(self, test, details=None):
        """Called when a test succeeded."""

    def addUnexpectedSuccess(self, test, details=None):
        """Called when a test was expected to fail, but succeed."""
        self.unexpectedSuccesses.append(test)

    def wasSuccessful(self):
        """Has this result been successful so far?

        If there have been any errors, failures or unexpected successes,
        return False.  Otherwise, return True.

        Note: This differs from standard unittest in that we consider
        unexpected successes to be equivalent to failures, rather than
        successes.
        """
        return not (self.errors or self.failures or self.unexpectedSuccesses)

    def _err_details_to_string(self, test, err=None, details=None):
        """Convert an error in exc_info form or a contents dict to a string."""
        if err is not None:
            return TracebackContent(err, test).as_text()
        return _details_to_str(details, special='traceback')

    def _exc_info_to_unicode(self, err, test):
        # Deprecated.  Only present because subunit upcalls to it.  See
        # <https://bugs.launchpad.net/testtools/+bug/929063>.
        return TracebackContent(err, test).as_text()

    def _now(self):
        """Return the current 'test time'.

        If the time() method has not been called, this is equivalent to
        datetime.now(), otherwise its the last supplied datestamp given to the
        time() method.
        """
        if self.__now is None:
            return datetime.datetime.now(utc)
        else:
            return self.__now

    def startTestRun(self):
        """Called before a test run starts.

        New in Python 2.7. The testtools version resets the result to a
        pristine condition ready for use in another test run.  Note that this
        is different from Python 2.7's startTestRun, which does nothing.
        """
        super(TestResult, self).__init__()
        self.skip_reasons = {}
        self.__now = None
        self._tags = TagContext()
        # -- Start: As per python 2.7 --
        self.expectedFailures = []
        self.unexpectedSuccesses = []
        # -- End:   As per python 2.7 --

    def stopTestRun(self):
        """Called after a test run completes

        New in python 2.7
        """

    def startTest(self, test):
        super(TestResult, self).startTest(test)
        self._tags = TagContext(self._tags)

    def stopTest(self, test):
        self._tags = self._tags.parent
        super(TestResult, self).stopTest(test)

    @property
    def current_tags(self):
        """The currently set tags."""
        return self._tags.get_current_tags()

    def tags(self, new_tags, gone_tags):
        """Add and remove tags from the test.

        :param new_tags: A set of tags to be added to the stream.
        :param gone_tags: A set of tags to be removed from the stream.
        """
        self._tags.change_tags(new_tags, gone_tags)

    def time(self, a_datetime):
        """Provide a timestamp to represent the current time.

        This is useful when test activity is time delayed, or happening
        concurrently and getting the system time between API calls will not
        accurately represent the duration of tests (or the whole run).

        Calling time() sets the datetime used by the TestResult object.
        Time is permitted to go backwards when using this call.

        :param a_datetime: A datetime.datetime object with TZ information or
            None to reset the TestResult to gathering time from the system.
        """
        self.__now = a_datetime

    def done(self):
        """Called when the test runner is done.

        deprecated in favour of stopTestRun.
        """


class MultiTestResult(TestResult):
    """A test result that dispatches to many test results."""

    def __init__(self, *results):
        super(MultiTestResult, self).__init__()
        self._results = list(map(ExtendedToOriginalDecorator, results))

    def __repr__(self):
        return '<%s (%s)>' % (
            self.__class__.__name__, ', '.join(map(repr, self._results)))

    def _dispatch(self, message, *args, **kwargs):
        return tuple(
            getattr(result, message)(*args, **kwargs)
            for result in self._results)

    def startTest(self, test):
        super(MultiTestResult, self).startTest(test)
        return self._dispatch('startTest', test)

    def stopTest(self, test):
        super(MultiTestResult, self).stopTest(test)
        return self._dispatch('stopTest', test)

    def addError(self, test, error=None, details=None):
        return self._dispatch('addError', test, error, details=details)

    def addExpectedFailure(self, test, err=None, details=None):
        return self._dispatch(
            'addExpectedFailure', test, err, details=details)

    def addFailure(self, test, err=None, details=None):
        return self._dispatch('addFailure', test, err, details=details)

    def addSkip(self, test, reason=None, details=None):
        return self._dispatch('addSkip', test, reason, details=details)

    def addSuccess(self, test, details=None):
        return self._dispatch('addSuccess', test, details=details)

    def addUnexpectedSuccess(self, test, details=None):
        return self._dispatch('addUnexpectedSuccess', test, details=details)

    def startTestRun(self):
        super(MultiTestResult, self).startTestRun()
        return self._dispatch('startTestRun')

    def stopTestRun(self):
        return self._dispatch('stopTestRun')

    def tags(self, new_tags, gone_tags):
        super(MultiTestResult, self).tags(new_tags, gone_tags)
        return self._dispatch('tags', new_tags, gone_tags)

    def time(self, a_datetime):
        return self._dispatch('time', a_datetime)

    def done(self):
        return self._dispatch('done')

    def wasSuccessful(self):
        """Was this result successful?

        Only returns True if every constituent result was successful.
        """
        return all(self._dispatch('wasSuccessful'))


class TextTestResult(TestResult):
    """A TestResult which outputs activity to a text stream."""

    def __init__(self, stream):
        """Construct a TextTestResult writing to stream."""
        super(TextTestResult, self).__init__()
        self.stream = stream
        self.sep1 = '=' * 70 + '\n'
        self.sep2 = '-' * 70 + '\n'

    def _delta_to_float(self, a_timedelta):
        return (a_timedelta.days * 86400.0 + a_timedelta.seconds +
            a_timedelta.microseconds / 1000000.0)

    def _show_list(self, label, error_list):
        for test, output in error_list:
            self.stream.write(self.sep1)
            self.stream.write("%s: %s\n" % (label, test.id()))
            self.stream.write(self.sep2)
            self.stream.write(output)

    def startTestRun(self):
        super(TextTestResult, self).startTestRun()
        self.__start = self._now()
        self.stream.write("Tests running...\n")

    def stopTestRun(self):
        if self.testsRun != 1:
            plural = 's'
        else:
            plural = ''
        stop = self._now()
        self._show_list('ERROR', self.errors)
        self._show_list('FAIL', self.failures)
        for test in self.unexpectedSuccesses:
            self.stream.write(
                "%sUNEXPECTED SUCCESS: %s\n%s" % (
                    self.sep1, test.id(), self.sep2))
        self.stream.write("\nRan %d test%s in %.3fs\n" %
            (self.testsRun, plural,
             self._delta_to_float(stop - self.__start)))
        if self.wasSuccessful():
            self.stream.write("OK\n")
        else:
            self.stream.write("FAILED (")
            details = []
            details.append("failures=%d" % (
                sum(map(len, (
                    self.failures, self.errors, self.unexpectedSuccesses)))))
            self.stream.write(", ".join(details))
            self.stream.write(")\n")
        super(TextTestResult, self).stopTestRun()


class ThreadsafeForwardingResult(TestResult):
    """A TestResult which ensures the target does not receive mixed up calls.

    Multiple ``ThreadsafeForwardingResult``s can forward to the same target
    result, and that target result will only ever receive the complete set of
    events for one test at a time.

    This is enforced using a semaphore, which further guarantees that tests
    will be sent atomically even if the ``ThreadsafeForwardingResult``s are in
    different threads.

    ``ThreadsafeForwardingResult`` is typically used by
    ``ConcurrentTestSuite``, which creates one ``ThreadsafeForwardingResult``
    per thread, each of which wraps of the TestResult that
    ``ConcurrentTestSuite.run()`` is called with.

    target.startTestRun() and target.stopTestRun() are called once for each
    ThreadsafeForwardingResult that forwards to the same target. If the target
    takes special action on these events, it should take care to accommodate
    this.

    time() and tags() calls are batched to be adjacent to the test result and
    in the case of tags() are coerced into test-local scope, avoiding the
    opportunity for bugs around global state in the target.
    """

    def __init__(self, target, semaphore):
        """Create a ThreadsafeForwardingResult forwarding to target.

        :param target: A ``TestResult``.
        :param semaphore: A ``threading.Semaphore`` with limit 1.
        """
        TestResult.__init__(self)
        self.result = ExtendedToOriginalDecorator(target)
        self.semaphore = semaphore
        self._test_start = None
        self._global_tags = set(), set()
        self._test_tags = set(), set()

    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, self.result)

    def _any_tags(self, tags):
        return bool(tags[0] or tags[1])

    def _add_result_with_semaphore(self, method, test, *args, **kwargs):
        now = self._now()
        self.semaphore.acquire()
        try:
            self.result.time(self._test_start)
            self.result.startTest(test)
            self.result.time(now)
            if self._any_tags(self._global_tags):
                self.result.tags(*self._global_tags)
            if self._any_tags(self._test_tags):
                self.result.tags(*self._test_tags)
            self._test_tags = set(), set()
            try:
                method(test, *args, **kwargs)
            finally:
                self.result.stopTest(test)
        finally:
            self.semaphore.release()
        self._test_start = None

    def addError(self, test, err=None, details=None):
        self._add_result_with_semaphore(self.result.addError,
            test, err, details=details)

    def addExpectedFailure(self, test, err=None, details=None):
        self._add_result_with_semaphore(self.result.addExpectedFailure,
            test, err, details=details)

    def addFailure(self, test, err=None, details=None):
        self._add_result_with_semaphore(self.result.addFailure,
            test, err, details=details)

    def addSkip(self, test, reason=None, details=None):
        self._add_result_with_semaphore(self.result.addSkip,
            test, reason, details=details)

    def addSuccess(self, test, details=None):
        self._add_result_with_semaphore(self.result.addSuccess,
            test, details=details)

    def addUnexpectedSuccess(self, test, details=None):
        self._add_result_with_semaphore(self.result.addUnexpectedSuccess,
            test, details=details)

    def startTestRun(self):
        super(ThreadsafeForwardingResult, self).startTestRun()
        self.semaphore.acquire()
        try:
            self.result.startTestRun()
        finally:
            self.semaphore.release()

    def stopTestRun(self):
        self.semaphore.acquire()
        try:
            self.result.stopTestRun()
        finally:
            self.semaphore.release()

    def done(self):
        self.semaphore.acquire()
        try:
            self.result.done()
        finally:
            self.semaphore.release()

    def startTest(self, test):
        self._test_start = self._now()
        super(ThreadsafeForwardingResult, self).startTest(test)

    def wasSuccessful(self):
        return self.result.wasSuccessful()

    def tags(self, new_tags, gone_tags):
        """See `TestResult`."""
        super(ThreadsafeForwardingResult, self).tags(new_tags, gone_tags)
        if self._test_start is not None:
            self._test_tags = _merge_tags(
                self._test_tags, (new_tags, gone_tags))
        else:
            self._global_tags = _merge_tags(
                self._global_tags, (new_tags, gone_tags))


def _merge_tags(existing, changed):
    new_tags, gone_tags = changed
    result_new = set(existing[0])
    result_gone = set(existing[1])
    result_new.update(new_tags)
    result_new.difference_update(gone_tags)
    result_gone.update(gone_tags)
    result_gone.difference_update(new_tags)
    return result_new, result_gone


class ExtendedToOriginalDecorator(object):
    """Permit new TestResult API code to degrade gracefully with old results.

    This decorates an existing TestResult and converts missing outcomes
    such as addSkip to older outcomes such as addSuccess. It also supports
    the extended details protocol. In all cases the most recent protocol
    is attempted first, and fallbacks only occur when the decorated result
    does not support the newer style of calling.
    """

    def __init__(self, decorated):
        self.decorated = decorated
        self._tags = TagContext()

    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, self.decorated)

    def __getattr__(self, name):
        return getattr(self.decorated, name)

    def addError(self, test, err=None, details=None):
        self._check_args(err, details)
        if details is not None:
            try:
                return self.decorated.addError(test, details=details)
            except TypeError:
                # have to convert
                err = self._details_to_exc_info(details)
        return self.decorated.addError(test, err)

    def addExpectedFailure(self, test, err=None, details=None):
        self._check_args(err, details)
        addExpectedFailure = getattr(
            self.decorated, 'addExpectedFailure', None)
        if addExpectedFailure is None:
            return self.addSuccess(test)
        if details is not None:
            try:
                return addExpectedFailure(test, details=details)
            except TypeError:
                # have to convert
                err = self._details_to_exc_info(details)
        return addExpectedFailure(test, err)

    def addFailure(self, test, err=None, details=None):
        self._check_args(err, details)
        if details is not None:
            try:
                return self.decorated.addFailure(test, details=details)
            except TypeError:
                # have to convert
                err = self._details_to_exc_info(details)
        return self.decorated.addFailure(test, err)

    def addSkip(self, test, reason=None, details=None):
        self._check_args(reason, details)
        addSkip = getattr(self.decorated, 'addSkip', None)
        if addSkip is None:
            return self.decorated.addSuccess(test)
        if details is not None:
            try:
                return addSkip(test, details=details)
            except TypeError:
                # extract the reason if it's available
                try:
                    reason = details['reason'].as_text()
                except KeyError:
                    reason = _details_to_str(details)
        return addSkip(test, reason)

    def addUnexpectedSuccess(self, test, details=None):
        outcome = getattr(self.decorated, 'addUnexpectedSuccess', None)
        if outcome is None:
            try:
                test.fail("")
            except test.failureException:
                return self.addFailure(test, sys.exc_info())
        if details is not None:
            try:
                return outcome(test, details=details)
            except TypeError:
                pass
        return outcome(test)

    def addSuccess(self, test, details=None):
        if details is not None:
            try:
                return self.decorated.addSuccess(test, details=details)
            except TypeError:
                pass
        return self.decorated.addSuccess(test)

    def _check_args(self, err, details):
        param_count = 0
        if err is not None:
            param_count += 1
        if details is not None:
            param_count += 1
        if param_count != 1:
            raise ValueError("Must pass only one of err '%s' and details '%s"
                % (err, details))

    def _details_to_exc_info(self, details):
        """Convert a details dict to an exc_info tuple."""
        return (
            _StringException,
            _StringException(_details_to_str(details, special='traceback')),
            None)

    @property
    def current_tags(self):
        return getattr(
            self.decorated, 'current_tags', self._tags.get_current_tags())

    def done(self):
        try:
            return self.decorated.done()
        except AttributeError:
            return

    def progress(self, offset, whence):
        method = getattr(self.decorated, 'progress', None)
        if method is None:
            return
        return method(offset, whence)

    @property
    def shouldStop(self):
        return self.decorated.shouldStop

    def startTest(self, test):
        self._tags = TagContext(self._tags)
        return self.decorated.startTest(test)

    def startTestRun(self):
        self._tags = TagContext()
        try:
            return self.decorated.startTestRun()
        except AttributeError:
            return

    def stop(self):
        return self.decorated.stop()

    def stopTest(self, test):
        self._tags = self._tags.parent
        return self.decorated.stopTest(test)

    def stopTestRun(self):
        try:
            return self.decorated.stopTestRun()
        except AttributeError:
            return

    def tags(self, new_tags, gone_tags):
        method = getattr(self.decorated, 'tags', None)
        if method is not None:
            return method(new_tags, gone_tags)
        else:
            self._tags.change_tags(new_tags, gone_tags)

    def time(self, a_datetime):
        method = getattr(self.decorated, 'time', None)
        if method is None:
            return
        return method(a_datetime)

    def wasSuccessful(self):
        return self.decorated.wasSuccessful()


class TestResultDecorator(object):
    """General pass-through decorator.

    This provides a base that other TestResults can inherit from to
    gain basic forwarding functionality.
    """

    def __init__(self, decorated):
        """Create a TestResultDecorator forwarding to decorated."""
        self.decorated = decorated

    def startTest(self, test):
        return self.decorated.startTest(test)

    def startTestRun(self):
        return self.decorated.startTestRun()

    def stopTest(self, test):
        return self.decorated.stopTest(test)

    def stopTestRun(self):
        return self.decorated.stopTestRun()

    def addError(self, test, err=None, details=None):
        return self.decorated.addError(test, err, details=details)

    def addFailure(self, test, err=None, details=None):
        return self.decorated.addFailure(test, err, details=details)

    def addSuccess(self, test, details=None):
        return self.decorated.addSuccess(test, details=details)

    def addSkip(self, test, reason=None, details=None):
        return self.decorated.addSkip(test, reason, details=details)

    def addExpectedFailure(self, test, err=None, details=None):
        return self.decorated.addExpectedFailure(test, err, details=details)

    def addUnexpectedSuccess(self, test, details=None):
        return self.decorated.addUnexpectedSuccess(test, details=details)

    def progress(self, offset, whence):
        return self.decorated.progress(offset, whence)

    def wasSuccessful(self):
        return self.decorated.wasSuccessful()

    @property
    def current_tags(self):
        return self.decorated.current_tags

    @property
    def shouldStop(self):
        return self.decorated.shouldStop

    def stop(self):
        return self.decorated.stop()

    @property
    def testsRun(self):
        return self.decorated.testsRun

    def tags(self, new_tags, gone_tags):
        return self.decorated.tags(new_tags, gone_tags)

    def time(self, a_datetime):
        return self.decorated.time(a_datetime)


class Tagger(TestResultDecorator):
    """Tag each test individually."""

    def __init__(self, decorated, new_tags, gone_tags):
        """Wrap 'decorated' such that each test is tagged.

        :param new_tags: Tags to be added for each test.
        :param gone_tags: Tags to be removed for each test.
        """
        super(Tagger, self).__init__(decorated)
        self._new_tags = set(new_tags)
        self._gone_tags = set(gone_tags)

    def startTest(self, test):
        super(Tagger, self).startTest(test)
        self.tags(self._new_tags, self._gone_tags)


class TestByTestResult(TestResult):
    """Call something every time a test completes."""

    def __init__(self, on_test):
        """Construct a ``TestByTestResult``.

        :param on_test: A callable that take a test case, a status (one of
            "success", "failure", "error", "skip", or "xfail"), a start time
            (a ``datetime`` with timezone), a stop time, an iterable of tags,
            and a details dict. Is called at the end of each test (i.e. on
            ``stopTest``) with the accumulated values for that test.
        """
        super(TestByTestResult, self).__init__()
        self._on_test = on_test

    def startTest(self, test):
        super(TestByTestResult, self).startTest(test)
        self._start_time = self._now()
        # There's no supported (i.e. tested) behaviour that relies on these
        # being set, but it makes me more comfortable all the same. -- jml
        self._status = None
        self._details = None
        self._stop_time = None

    def stopTest(self, test):
        self._stop_time = self._now()
        tags = set(self.current_tags)
        super(TestByTestResult, self).stopTest(test)
        self._on_test(
            test=test,
            status=self._status,
            start_time=self._start_time,
            stop_time=self._stop_time,
            tags=tags,
            details=self._details)

    def _err_to_details(self, test, err, details):
        if details:
            return details
        return {'traceback': TracebackContent(err, test)}

    def addSuccess(self, test, details=None):
        super(TestByTestResult, self).addSuccess(test)
        self._status = 'success'
        self._details = details

    def addFailure(self, test, err=None, details=None):
        super(TestByTestResult, self).addFailure(test, err, details)
        self._status = 'failure'
        self._details = self._err_to_details(test, err, details)

    def addError(self, test, err=None, details=None):
        super(TestByTestResult, self).addError(test, err, details)
        self._status = 'error'
        self._details = self._err_to_details(test, err, details)

    def addSkip(self, test, reason=None, details=None):
        super(TestByTestResult, self).addSkip(test, reason, details)
        self._status = 'skip'
        if details is None:
            details = {'reason': text_content(reason)}
        elif reason:
            # XXX: What if details already has 'reason' key?
            details['reason'] = text_content(reason)
        self._details = details

    def addExpectedFailure(self, test, err=None, details=None):
        super(TestByTestResult, self).addExpectedFailure(test, err, details)
        self._status = 'xfail'
        self._details = self._err_to_details(test, err, details)

    def addUnexpectedSuccess(self, test, details=None):
        super(TestByTestResult, self).addUnexpectedSuccess(test, details)
        self._status = 'success'
        self._details = details


class _StringException(Exception):
    """An exception made from an arbitrary string."""

    if not str_is_unicode:
        def __init__(self, string):
            if type(string) is not unicode:
                raise TypeError("_StringException expects unicode, got %r" %
                    (string,))
            Exception.__init__(self, string)

        def __str__(self):
            return self.args[0].encode("utf-8")

        def __unicode__(self):
            return self.args[0]
    # For 3.0 and above the default __str__ is fine, so we don't define one.

    def __hash__(self):
        return id(self)

    def __eq__(self, other):
        try:
            return self.args == other.args
        except AttributeError:
            return False


def _format_text_attachment(name, text):
    if '\n' in text:
        return "%s: {{{\n%s\n}}}\n" % (name, text)
    return "%s: {{{%s}}}" % (name, text)


def _details_to_str(details, special=None):
    """Convert a details dict to a string.

    :param details: A dictionary mapping short names to ``Content`` objects.
    :param special: If specified, an attachment that should have special
        attention drawn to it. The primary attachment. Normally it's the
        traceback that caused the test to fail.
    :return: A formatted string that can be included in text test results.
    """
    empty_attachments = []
    binary_attachments = []
    text_attachments = []
    special_content = None
    # sorted is for testing, may want to remove that and use a dict
    # subclass with defined order for items instead.
    for key, content in sorted(details.items()):
        if content.content_type.type != 'text':
            binary_attachments.append((key, content.content_type))
            continue
        text = content.as_text().strip()
        if not text:
            empty_attachments.append(key)
            continue
        # We want the 'special' attachment to be at the bottom.
        if key == special:
            special_content = '%s\n' % (text,)
            continue
        text_attachments.append(_format_text_attachment(key, text))
    if text_attachments and not text_attachments[-1].endswith('\n'):
        text_attachments.append('')
    if special_content:
        text_attachments.append(special_content)
    lines = []
    if binary_attachments:
        lines.append('Binary content:\n')
        for name, content_type in binary_attachments:
            lines.append('  %s (%s)\n' % (name, content_type))
    if empty_attachments:
        lines.append('Empty attachments:\n')
        for name in empty_attachments:
            lines.append('  %s\n' % (name,))
    if (binary_attachments or empty_attachments) and text_attachments:
        lines.append('\n')
    lines.append('\n'.join(text_attachments))
    return _u('').join(lines)
