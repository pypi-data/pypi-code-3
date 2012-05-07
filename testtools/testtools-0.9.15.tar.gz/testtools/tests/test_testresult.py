# Copyright (c) 2008-2012 testtools developers. See LICENSE for details.

"""Test TestResults and related things."""

__metaclass__ = type

import codecs
import datetime
import doctest
import os
import shutil
import sys
import tempfile
import threading
import warnings

from testtools import (
    ExtendedToOriginalDecorator,
    MultiTestResult,
    PlaceHolder,
    Tagger,
    TestCase,
    TestResult,
    TestResultDecorator,
    TestByTestResult,
    TextTestResult,
    ThreadsafeForwardingResult,
    testresult,
    )
from testtools.compat import (
    _b,
    _get_exception_encoding,
    _r,
    _u,
    advance_iterator,
    str_is_unicode,
    StringIO,
    )
from testtools.content import (
    Content,
    content_from_stream,
    text_content,
    TracebackContent,
    )
from testtools.content_type import ContentType, UTF8_TEXT
from testtools.matchers import (
    DocTestMatches,
    Equals,
    MatchesException,
    Raises,
    )
from testtools.tests.helpers import (
    an_exc_info,
    FullStackRunTest,
    LoggingResult,
    run_with_stack_hidden,
    )
from testtools.testresult.doubles import (
    Python26TestResult,
    Python27TestResult,
    ExtendedTestResult,
    )
from testtools.testresult.real import (
    _details_to_str,
    _merge_tags,
    utc,
    )


def make_erroring_test():
    class Test(TestCase):
        def error(self):
            1/0
    return Test("error")


def make_failing_test():
    class Test(TestCase):
        def failed(self):
            self.fail("yo!")
    return Test("failed")


def make_mismatching_test():
    class Test(TestCase):
        def mismatch(self):
            self.assertEqual(1, 2)
    return Test("mismatch")


def make_unexpectedly_successful_test():
    class Test(TestCase):
        def succeeded(self):
            self.expectFailure("yo!", lambda: None)
    return Test("succeeded")


def make_test():
    class Test(TestCase):
        def test(self):
            pass
    return Test("test")


def make_exception_info(exceptionFactory, *args, **kwargs):
    try:
        raise exceptionFactory(*args, **kwargs)
    except:
        return sys.exc_info()


class Python26Contract(object):

    def test_fresh_result_is_successful(self):
        # A result is considered successful before any tests are run.
        result = self.makeResult()
        self.assertTrue(result.wasSuccessful())

    def test_addError_is_failure(self):
        # addError fails the test run.
        result = self.makeResult()
        result.startTest(self)
        result.addError(self, an_exc_info)
        result.stopTest(self)
        self.assertFalse(result.wasSuccessful())

    def test_addFailure_is_failure(self):
        # addFailure fails the test run.
        result = self.makeResult()
        result.startTest(self)
        result.addFailure(self, an_exc_info)
        result.stopTest(self)
        self.assertFalse(result.wasSuccessful())

    def test_addSuccess_is_success(self):
        # addSuccess does not fail the test run.
        result = self.makeResult()
        result.startTest(self)
        result.addSuccess(self)
        result.stopTest(self)
        self.assertTrue(result.wasSuccessful())


class Python27Contract(Python26Contract):

    def test_addExpectedFailure(self):
        # Calling addExpectedFailure(test, exc_info) completes ok.
        result = self.makeResult()
        result.startTest(self)
        result.addExpectedFailure(self, an_exc_info)

    def test_addExpectedFailure_is_success(self):
        # addExpectedFailure does not fail the test run.
        result = self.makeResult()
        result.startTest(self)
        result.addExpectedFailure(self, an_exc_info)
        result.stopTest(self)
        self.assertTrue(result.wasSuccessful())

    def test_addSkipped(self):
        # Calling addSkip(test, reason) completes ok.
        result = self.makeResult()
        result.startTest(self)
        result.addSkip(self, _u("Skipped for some reason"))

    def test_addSkip_is_success(self):
        # addSkip does not fail the test run.
        result = self.makeResult()
        result.startTest(self)
        result.addSkip(self, _u("Skipped for some reason"))
        result.stopTest(self)
        self.assertTrue(result.wasSuccessful())

    def test_addUnexpectedSuccess(self):
        # Calling addUnexpectedSuccess(test) completes ok.
        result = self.makeResult()
        result.startTest(self)
        result.addUnexpectedSuccess(self)

    def test_addUnexpectedSuccess_was_successful(self):
        # addUnexpectedSuccess does not fail the test run in Python 2.7.
        result = self.makeResult()
        result.startTest(self)
        result.addUnexpectedSuccess(self)
        result.stopTest(self)
        self.assertTrue(result.wasSuccessful())

    def test_startStopTestRun(self):
        # Calling startTestRun completes ok.
        result = self.makeResult()
        result.startTestRun()
        result.stopTestRun()


class TagsContract(Python27Contract):
    """Tests to ensure correct tagging behaviour.

    See the subunit docs for guidelines on how this is supposed to work.
    """

    def test_no_tags_by_default(self):
        # Results initially have no tags.
        result = self.makeResult()
        self.assertEqual(frozenset(), result.current_tags)

    def test_adding_tags(self):
        # Tags are added using 'tags' and thus become visible in
        # 'current_tags'.
        result = self.makeResult()
        result.tags(set(['foo']), set())
        self.assertEqual(set(['foo']), result.current_tags)

    def test_removing_tags(self):
        # Tags are removed using 'tags'.
        result = self.makeResult()
        result.tags(set(['foo']), set())
        result.tags(set(), set(['foo']))
        self.assertEqual(set(), result.current_tags)

    def test_startTestRun_resets_tags(self):
        # startTestRun makes a new test run, and thus clears all the tags.
        result = self.makeResult()
        result.tags(set(['foo']), set())
        result.startTestRun()
        self.assertEqual(set(), result.current_tags)

    def test_add_tags_within_test(self):
        # Tags can be added after a test has run.
        result = self.makeResult()
        result.startTestRun()
        result.tags(set(['foo']), set())
        result.startTest(self)
        result.tags(set(['bar']), set())
        self.assertEqual(set(['foo', 'bar']), result.current_tags)

    def test_tags_added_in_test_are_reverted(self):
        # Tags added during a test run are then reverted once that test has
        # finished.
        result = self.makeResult()
        result.startTestRun()
        result.tags(set(['foo']), set())
        result.startTest(self)
        result.tags(set(['bar']), set())
        result.addSuccess(self)
        result.stopTest(self)
        self.assertEqual(set(['foo']), result.current_tags)

    def test_tags_removed_in_test(self):
        # Tags can be removed during tests.
        result = self.makeResult()
        result.startTestRun()
        result.tags(set(['foo']), set())
        result.startTest(self)
        result.tags(set(), set(['foo']))
        self.assertEqual(set(), result.current_tags)

    def test_tags_removed_in_test_are_restored(self):
        # Tags removed during tests are restored once that test has finished.
        result = self.makeResult()
        result.startTestRun()
        result.tags(set(['foo']), set())
        result.startTest(self)
        result.tags(set(), set(['foo']))
        result.addSuccess(self)
        result.stopTest(self)
        self.assertEqual(set(['foo']), result.current_tags)


class DetailsContract(TagsContract):
    """Tests for the details API of TestResults."""

    def test_addExpectedFailure_details(self):
        # Calling addExpectedFailure(test, details=xxx) completes ok.
        result = self.makeResult()
        result.startTest(self)
        result.addExpectedFailure(self, details={})

    def test_addError_details(self):
        # Calling addError(test, details=xxx) completes ok.
        result = self.makeResult()
        result.startTest(self)
        result.addError(self, details={})

    def test_addFailure_details(self):
        # Calling addFailure(test, details=xxx) completes ok.
        result = self.makeResult()
        result.startTest(self)
        result.addFailure(self, details={})

    def test_addSkipped_details(self):
        # Calling addSkip(test, reason) completes ok.
        result = self.makeResult()
        result.startTest(self)
        result.addSkip(self, details={})

    def test_addUnexpectedSuccess_details(self):
        # Calling addUnexpectedSuccess(test) completes ok.
        result = self.makeResult()
        result.startTest(self)
        result.addUnexpectedSuccess(self, details={})

    def test_addSuccess_details(self):
        # Calling addSuccess(test) completes ok.
        result = self.makeResult()
        result.startTest(self)
        result.addSuccess(self, details={})


class FallbackContract(DetailsContract):
    """When we fallback we take our policy choice to map calls.

    For instance, we map unexpectedSuccess to an error code, not to success.
    """

    def test_addUnexpectedSuccess_was_successful(self):
        # addUnexpectedSuccess fails test run in testtools.
        result = self.makeResult()
        result.startTest(self)
        result.addUnexpectedSuccess(self)
        result.stopTest(self)
        self.assertFalse(result.wasSuccessful())


class StartTestRunContract(FallbackContract):
    """Defines the contract for testtools policy choices.

    That is things which are not simply extensions to unittest but choices we
    have made differently.
    """

    def test_startTestRun_resets_unexpected_success(self):
        result = self.makeResult()
        result.startTest(self)
        result.addUnexpectedSuccess(self)
        result.stopTest(self)
        result.startTestRun()
        self.assertTrue(result.wasSuccessful())

    def test_startTestRun_resets_failure(self):
        result = self.makeResult()
        result.startTest(self)
        result.addFailure(self, an_exc_info)
        result.stopTest(self)
        result.startTestRun()
        self.assertTrue(result.wasSuccessful())

    def test_startTestRun_resets_errors(self):
        result = self.makeResult()
        result.startTest(self)
        result.addError(self, an_exc_info)
        result.stopTest(self)
        result.startTestRun()
        self.assertTrue(result.wasSuccessful())


class TestTestResultContract(TestCase, StartTestRunContract):

    run_test_with = FullStackRunTest

    def makeResult(self):
        return TestResult()


class TestMultiTestResultContract(TestCase, StartTestRunContract):

    run_test_with = FullStackRunTest

    def makeResult(self):
        return MultiTestResult(TestResult(), TestResult())


class TestTextTestResultContract(TestCase, StartTestRunContract):

    run_test_with = FullStackRunTest

    def makeResult(self):
        return TextTestResult(StringIO())


class TestThreadSafeForwardingResultContract(TestCase, StartTestRunContract):

    run_test_with = FullStackRunTest

    def makeResult(self):
        result_semaphore = threading.Semaphore(1)
        target = TestResult()
        return ThreadsafeForwardingResult(target, result_semaphore)


class TestExtendedTestResultContract(TestCase, StartTestRunContract):

    def makeResult(self):
        return ExtendedTestResult()


class TestPython26TestResultContract(TestCase, Python26Contract):

    def makeResult(self):
        return Python26TestResult()


class TestAdaptedPython26TestResultContract(TestCase, FallbackContract):

    def makeResult(self):
        return ExtendedToOriginalDecorator(Python26TestResult())


class TestPython27TestResultContract(TestCase, Python27Contract):

    def makeResult(self):
        return Python27TestResult()


class TestAdaptedPython27TestResultContract(TestCase, DetailsContract):

    def makeResult(self):
        return ExtendedToOriginalDecorator(Python27TestResult())


class TestTestResultDecoratorContract(TestCase, StartTestRunContract):

    run_test_with = FullStackRunTest

    def makeResult(self):
        return TestResultDecorator(TestResult())


class TestTestResult(TestCase):
    """Tests for 'TestResult'."""

    run_tests_with = FullStackRunTest

    def makeResult(self):
        """Make an arbitrary result for testing."""
        return TestResult()

    def test_addSkipped(self):
        # Calling addSkip on a TestResult records the test that was skipped in
        # its skip_reasons dict.
        result = self.makeResult()
        result.addSkip(self, _u("Skipped for some reason"))
        self.assertEqual({_u("Skipped for some reason"):[self]},
            result.skip_reasons)
        result.addSkip(self, _u("Skipped for some reason"))
        self.assertEqual({_u("Skipped for some reason"):[self, self]},
            result.skip_reasons)
        result.addSkip(self, _u("Skipped for another reason"))
        self.assertEqual({_u("Skipped for some reason"):[self, self],
            _u("Skipped for another reason"):[self]},
            result.skip_reasons)

    def test_now_datetime_now(self):
        result = self.makeResult()
        olddatetime = testresult.real.datetime
        def restore():
            testresult.real.datetime = olddatetime
        self.addCleanup(restore)
        class Module:
            pass
        now = datetime.datetime.now(utc)
        stubdatetime = Module()
        stubdatetime.datetime = Module()
        stubdatetime.datetime.now = lambda tz: now
        testresult.real.datetime = stubdatetime
        # Calling _now() looks up the time.
        self.assertEqual(now, result._now())
        then = now + datetime.timedelta(0, 1)
        # Set an explicit datetime, which gets returned from then on.
        result.time(then)
        self.assertNotEqual(now, result._now())
        self.assertEqual(then, result._now())
        # go back to looking it up.
        result.time(None)
        self.assertEqual(now, result._now())

    def test_now_datetime_time(self):
        result = self.makeResult()
        now = datetime.datetime.now(utc)
        result.time(now)
        self.assertEqual(now, result._now())

    def test_traceback_formatting_without_stack_hidden(self):
        # During the testtools test run, we show our levels of the stack,
        # because we want to be able to use our test suite to debug our own
        # code.
        result = self.makeResult()
        test = make_erroring_test()
        test.run(result)
        self.assertThat(
            result.errors[0][1],
            DocTestMatches(
                'Traceback (most recent call last):\n'
                '  File "...testtools...runtest.py", line ..., in _run_user\n'
                '    return fn(*args, **kwargs)\n'
                '  File "...testtools...testcase.py", line ..., in _run_test_method\n'
                '    return self._get_test_method()()\n'
                '  File "...testtools...tests...test_testresult.py", line ..., in error\n'
                '    1/0\n'
                'ZeroDivisionError: ...\n',
                doctest.ELLIPSIS | doctest.REPORT_UDIFF))

    def test_traceback_formatting_with_stack_hidden(self):
        result = self.makeResult()
        test = make_erroring_test()
        run_with_stack_hidden(True, test.run, result)
        self.assertThat(
            result.errors[0][1],
            DocTestMatches(
                'Traceback (most recent call last):\n'
                '  File "...testtools...tests...test_testresult.py", line ..., in error\n'
                '    1/0\n'
                'ZeroDivisionError: ...\n',
                doctest.ELLIPSIS))

    def test_traceback_formatting_with_stack_hidden_mismatch(self):
        result = self.makeResult()
        test = make_mismatching_test()
        run_with_stack_hidden(True, test.run, result)
        self.assertThat(
            result.failures[0][1],
            DocTestMatches(
                'Traceback (most recent call last):\n'
                '  File "...testtools...tests...test_testresult.py", line ..., in mismatch\n'
                '    self.assertEqual(1, 2)\n'
                '...MismatchError: 1 != 2\n',
                doctest.ELLIPSIS))

    def test_exc_info_to_unicode(self):
        # subunit upcalls to TestResult._exc_info_to_unicode, so we need to
        # make sure that it's there.
        #
        # See <https://bugs.launchpad.net/testtools/+bug/929063>.
        test = make_erroring_test()
        exc_info = make_exception_info(RuntimeError, "foo")
        result = self.makeResult()
        text_traceback = result._exc_info_to_unicode(exc_info, test)
        self.assertEqual(
            TracebackContent(exc_info, test).as_text(), text_traceback)


class TestMultiTestResult(TestCase):
    """Tests for 'MultiTestResult'."""

    def setUp(self):
        super(TestMultiTestResult, self).setUp()
        self.result1 = LoggingResult([])
        self.result2 = LoggingResult([])
        self.multiResult = MultiTestResult(self.result1, self.result2)

    def assertResultLogsEqual(self, expectedEvents):
        """Assert that our test results have received the expected events."""
        self.assertEqual(expectedEvents, self.result1._events)
        self.assertEqual(expectedEvents, self.result2._events)

    def test_repr(self):
        self.assertEqual(
            '<MultiTestResult (%r, %r)>' % (
                ExtendedToOriginalDecorator(self.result1),
                ExtendedToOriginalDecorator(self.result2)),
            repr(self.multiResult))

    def test_empty(self):
        # Initializing a `MultiTestResult` doesn't do anything to its
        # `TestResult`s.
        self.assertResultLogsEqual([])

    def test_startTest(self):
        # Calling `startTest` on a `MultiTestResult` calls `startTest` on all
        # its `TestResult`s.
        self.multiResult.startTest(self)
        self.assertResultLogsEqual([('startTest', self)])

    def test_stopTest(self):
        # Calling `stopTest` on a `MultiTestResult` calls `stopTest` on all
        # its `TestResult`s.
        self.multiResult.stopTest(self)
        self.assertResultLogsEqual([('stopTest', self)])

    def test_addSkipped(self):
        # Calling `addSkip` on a `MultiTestResult` calls addSkip on its
        # results.
        reason = _u("Skipped for some reason")
        self.multiResult.addSkip(self, reason)
        self.assertResultLogsEqual([('addSkip', self, reason)])

    def test_addSuccess(self):
        # Calling `addSuccess` on a `MultiTestResult` calls `addSuccess` on
        # all its `TestResult`s.
        self.multiResult.addSuccess(self)
        self.assertResultLogsEqual([('addSuccess', self)])

    def test_done(self):
        # Calling `done` on a `MultiTestResult` calls `done` on all its
        # `TestResult`s.
        self.multiResult.done()
        self.assertResultLogsEqual([('done')])

    def test_addFailure(self):
        # Calling `addFailure` on a `MultiTestResult` calls `addFailure` on
        # all its `TestResult`s.
        exc_info = make_exception_info(AssertionError, 'failure')
        self.multiResult.addFailure(self, exc_info)
        self.assertResultLogsEqual([('addFailure', self, exc_info)])

    def test_addError(self):
        # Calling `addError` on a `MultiTestResult` calls `addError` on all
        # its `TestResult`s.
        exc_info = make_exception_info(RuntimeError, 'error')
        self.multiResult.addError(self, exc_info)
        self.assertResultLogsEqual([('addError', self, exc_info)])

    def test_startTestRun(self):
        # Calling `startTestRun` on a `MultiTestResult` forwards to all its
        # `TestResult`s.
        self.multiResult.startTestRun()
        self.assertResultLogsEqual([('startTestRun')])

    def test_stopTestRun(self):
        # Calling `stopTestRun` on a `MultiTestResult` forwards to all its
        # `TestResult`s.
        self.multiResult.stopTestRun()
        self.assertResultLogsEqual([('stopTestRun')])

    def test_stopTestRun_returns_results(self):
        # `MultiTestResult.stopTestRun` returns a tuple of all of the return
        # values the `stopTestRun`s that it forwards to.
        class Result(LoggingResult):
            def stopTestRun(self):
                super(Result, self).stopTestRun()
                return 'foo'
        multi_result = MultiTestResult(Result([]), Result([]))
        result = multi_result.stopTestRun()
        self.assertEqual(('foo', 'foo'), result)

    def test_tags(self):
        # Calling `tags` on a `MultiTestResult` calls `tags` on all its
        # `TestResult`s.
        added_tags = set(['foo', 'bar'])
        removed_tags = set(['eggs'])
        self.multiResult.tags(added_tags, removed_tags)
        self.assertResultLogsEqual([('tags', added_tags, removed_tags)])

    def test_time(self):
        # the time call is dispatched, not eaten by the base class
        self.multiResult.time('foo')
        self.assertResultLogsEqual([('time', 'foo')])


class TestTextTestResult(TestCase):
    """Tests for 'TextTestResult'."""

    def setUp(self):
        super(TestTextTestResult, self).setUp()
        self.result = TextTestResult(StringIO())

    def getvalue(self):
        return self.result.stream.getvalue()

    def test__init_sets_stream(self):
        result = TextTestResult("fp")
        self.assertEqual("fp", result.stream)

    def reset_output(self):
        self.result.stream = StringIO()

    def test_startTestRun(self):
        self.result.startTestRun()
        self.assertEqual("Tests running...\n", self.getvalue())

    def test_stopTestRun_count_many(self):
        test = make_test()
        self.result.startTestRun()
        self.result.startTest(test)
        self.result.stopTest(test)
        self.result.startTest(test)
        self.result.stopTest(test)
        self.result.stream = StringIO()
        self.result.stopTestRun()
        self.assertThat(self.getvalue(),
            DocTestMatches("\nRan 2 tests in ...s\n...", doctest.ELLIPSIS))

    def test_stopTestRun_count_single(self):
        test = make_test()
        self.result.startTestRun()
        self.result.startTest(test)
        self.result.stopTest(test)
        self.reset_output()
        self.result.stopTestRun()
        self.assertThat(self.getvalue(),
            DocTestMatches("\nRan 1 test in ...s\nOK\n", doctest.ELLIPSIS))

    def test_stopTestRun_count_zero(self):
        self.result.startTestRun()
        self.reset_output()
        self.result.stopTestRun()
        self.assertThat(self.getvalue(),
            DocTestMatches("\nRan 0 tests in ...s\nOK\n", doctest.ELLIPSIS))

    def test_stopTestRun_current_time(self):
        test = make_test()
        now = datetime.datetime.now(utc)
        self.result.time(now)
        self.result.startTestRun()
        self.result.startTest(test)
        now = now + datetime.timedelta(0, 0, 0, 1)
        self.result.time(now)
        self.result.stopTest(test)
        self.reset_output()
        self.result.stopTestRun()
        self.assertThat(self.getvalue(),
            DocTestMatches("... in 0.001s\n...", doctest.ELLIPSIS))

    def test_stopTestRun_successful(self):
        self.result.startTestRun()
        self.result.stopTestRun()
        self.assertThat(self.getvalue(),
            DocTestMatches("...\nOK\n", doctest.ELLIPSIS))

    def test_stopTestRun_not_successful_failure(self):
        test = make_failing_test()
        self.result.startTestRun()
        test.run(self.result)
        self.result.stopTestRun()
        self.assertThat(self.getvalue(),
            DocTestMatches("...\nFAILED (failures=1)\n", doctest.ELLIPSIS))

    def test_stopTestRun_not_successful_error(self):
        test = make_erroring_test()
        self.result.startTestRun()
        test.run(self.result)
        self.result.stopTestRun()
        self.assertThat(self.getvalue(),
            DocTestMatches("...\nFAILED (failures=1)\n", doctest.ELLIPSIS))

    def test_stopTestRun_not_successful_unexpected_success(self):
        test = make_unexpectedly_successful_test()
        self.result.startTestRun()
        test.run(self.result)
        self.result.stopTestRun()
        self.assertThat(self.getvalue(),
            DocTestMatches("...\nFAILED (failures=1)\n", doctest.ELLIPSIS))

    def test_stopTestRun_shows_details(self):
        def run_tests():
            self.result.startTestRun()
            make_erroring_test().run(self.result)
            make_unexpectedly_successful_test().run(self.result)
            make_failing_test().run(self.result)
            self.reset_output()
            self.result.stopTestRun()
        run_with_stack_hidden(True, run_tests)
        self.assertThat(self.getvalue(),
            DocTestMatches("""...======================================================================
ERROR: testtools.tests.test_testresult.Test.error
----------------------------------------------------------------------
Traceback (most recent call last):
  File "...testtools...tests...test_testresult.py", line ..., in error
    1/0
ZeroDivisionError:... divi... by zero...
======================================================================
FAIL: testtools.tests.test_testresult.Test.failed
----------------------------------------------------------------------
Traceback (most recent call last):
  File "...testtools...tests...test_testresult.py", line ..., in failed
    self.fail("yo!")
AssertionError: yo!
======================================================================
UNEXPECTED SUCCESS: testtools.tests.test_testresult.Test.succeeded
----------------------------------------------------------------------
...""", doctest.ELLIPSIS | doctest.REPORT_NDIFF))


class TestThreadSafeForwardingResult(TestCase):
    """Tests for `TestThreadSafeForwardingResult`."""

    def make_results(self, n):
        events = []
        target = LoggingResult(events)
        semaphore = threading.Semaphore(1)
        return [
            ThreadsafeForwardingResult(target, semaphore)
            for i in range(n)], events

    def test_nonforwarding_methods(self):
        # startTest and stopTest are not forwarded because they need to be
        # batched.
        [result], events = self.make_results(1)
        result.startTest(self)
        result.stopTest(self)
        self.assertEqual([], events)

    def test_tags_not_forwarded(self):
        # Tags need to be batched for each test, so they aren't forwarded
        # until a test runs.
        [result], events = self.make_results(1)
        result.tags(set(['foo']), set(['bar']))
        self.assertEqual([], events)

    def test_global_tags_simple(self):
        # Tags specified outside of a test result are global. When a test's
        # results are finally forwarded, we send through these global tags
        # *as* test specific tags, because as a multiplexer there should be no
        # way for a global tag on an input stream to affect tests from other
        # streams - we can just always issue test local tags.
        [result], events = self.make_results(1)
        result.tags(set(['foo']), set())
        result.time(1)
        result.startTest(self)
        result.time(2)
        result.addSuccess(self)
        self.assertEqual(
            [('time', 1),
             ('startTest', self),
             ('time', 2),
             ('tags', set(['foo']), set()),
             ('addSuccess', self),
             ('stopTest', self),
             ], events)

    def test_global_tags_complex(self):
        # Multiple calls to tags() in a global context are buffered until the
        # next test completes and are issued as part of of the test context,
        # because they cannot be issued until the output result is locked.
        # The sample data shows them being merged together, this is, strictly
        # speaking incidental - they could be issued separately (in-order) and
        # still be legitimate.
        [result], events = self.make_results(1)
        result.tags(set(['foo', 'bar']), set(['baz', 'qux']))
        result.tags(set(['cat', 'qux']), set(['bar', 'dog']))
        result.time(1)
        result.startTest(self)
        result.time(2)
        result.addSuccess(self)
        self.assertEqual(
            [('time', 1),
             ('startTest', self),
             ('time', 2),
             ('tags', set(['cat', 'foo', 'qux']), set(['dog', 'bar', 'baz'])),
             ('addSuccess', self),
             ('stopTest', self),
             ], events)

    def test_local_tags(self):
        # Any tags set within a test context are forwarded in that test
        # context when the result is finally forwarded.  This means that the
        # tags for the test are part of the atomic message communicating
        # everything about that test.
        [result], events = self.make_results(1)
        result.time(1)
        result.startTest(self)
        result.tags(set(['foo']), set([]))
        result.tags(set(), set(['bar']))
        result.time(2)
        result.addSuccess(self)
        self.assertEqual(
            [('time', 1),
             ('startTest', self),
             ('time', 2),
             ('tags', set(['foo']), set(['bar'])),
             ('addSuccess', self),
             ('stopTest', self),
             ], events)

    def test_local_tags_dont_leak(self):
        # A tag set during a test is local to that test and is not set during
        # the tests that follow.
        [result], events = self.make_results(1)
        a, b = PlaceHolder('a'), PlaceHolder('b')
        result.time(1)
        result.startTest(a)
        result.tags(set(['foo']), set([]))
        result.time(2)
        result.addSuccess(a)
        result.stopTest(a)
        result.time(3)
        result.startTest(b)
        result.time(4)
        result.addSuccess(b)
        result.stopTest(b)
        self.assertEqual(
            [('time', 1),
             ('startTest', a),
             ('time', 2),
             ('tags', set(['foo']), set()),
             ('addSuccess', a),
             ('stopTest', a),
             ('time', 3),
             ('startTest', b),
             ('time', 4),
             ('addSuccess', b),
             ('stopTest', b),
             ], events)

    def test_startTestRun(self):
        # Calls to startTestRun are not batched, because we are only
        # interested in sending tests atomically, not the whole run.
        [result1, result2], events = self.make_results(2)
        result1.startTestRun()
        result2.startTestRun()
        self.assertEqual(["startTestRun", "startTestRun"], events)

    def test_stopTestRun(self):
        # Calls to stopTestRun are not batched, because we are only
        # interested in sending tests atomically, not the whole run.
        [result1, result2], events = self.make_results(2)
        result1.stopTestRun()
        result2.stopTestRun()
        self.assertEqual(["stopTestRun", "stopTestRun"], events)

    def test_forward_addError(self):
        # Once we receive an addError event, we forward all of the events for
        # that test, as we now know that test is complete.
        [result], events = self.make_results(1)
        exc_info = make_exception_info(RuntimeError, 'error')
        start_time = datetime.datetime.utcfromtimestamp(1.489)
        end_time = datetime.datetime.utcfromtimestamp(51.476)
        result.time(start_time)
        result.startTest(self)
        result.time(end_time)
        result.addError(self, exc_info)
        self.assertEqual([
            ('time', start_time),
            ('startTest', self),
            ('time', end_time),
            ('addError', self, exc_info),
            ('stopTest', self),
            ], events)

    def test_forward_addFailure(self):
        # Once we receive an addFailure event, we forward all of the events
        # for that test, as we now know that test is complete.
        [result], events = self.make_results(1)
        exc_info = make_exception_info(AssertionError, 'failure')
        start_time = datetime.datetime.utcfromtimestamp(2.489)
        end_time = datetime.datetime.utcfromtimestamp(3.476)
        result.time(start_time)
        result.startTest(self)
        result.time(end_time)
        result.addFailure(self, exc_info)
        self.assertEqual([
            ('time', start_time),
            ('startTest', self),
            ('time', end_time),
            ('addFailure', self, exc_info),
            ('stopTest', self),
            ], events)

    def test_forward_addSkip(self):
        # Once we receive an addSkip event, we forward all of the events for
        # that test, as we now know that test is complete.
        [result], events = self.make_results(1)
        reason = _u("Skipped for some reason")
        start_time = datetime.datetime.utcfromtimestamp(4.489)
        end_time = datetime.datetime.utcfromtimestamp(5.476)
        result.time(start_time)
        result.startTest(self)
        result.time(end_time)
        result.addSkip(self, reason)
        self.assertEqual([
            ('time', start_time),
            ('startTest', self),
            ('time', end_time),
            ('addSkip', self, reason),
            ('stopTest', self),
            ], events)

    def test_forward_addSuccess(self):
        # Once we receive an addSuccess event, we forward all of the events
        # for that test, as we now know that test is complete.
        [result], events = self.make_results(1)
        start_time = datetime.datetime.utcfromtimestamp(6.489)
        end_time = datetime.datetime.utcfromtimestamp(7.476)
        result.time(start_time)
        result.startTest(self)
        result.time(end_time)
        result.addSuccess(self)
        self.assertEqual([
            ('time', start_time),
            ('startTest', self),
            ('time', end_time),
            ('addSuccess', self),
            ('stopTest', self),
            ], events)

    def test_only_one_test_at_a_time(self):
        # Even if there are multiple ThreadsafeForwardingResults forwarding to
        # the same target result, the target result only receives the complete
        # events for one test at a time.
        [result1, result2], events = self.make_results(2)
        test1, test2 = self, make_test()
        start_time1 = datetime.datetime.utcfromtimestamp(1.489)
        end_time1 = datetime.datetime.utcfromtimestamp(2.476)
        start_time2 = datetime.datetime.utcfromtimestamp(3.489)
        end_time2 = datetime.datetime.utcfromtimestamp(4.489)
        result1.time(start_time1)
        result2.time(start_time2)
        result1.startTest(test1)
        result2.startTest(test2)
        result1.time(end_time1)
        result2.time(end_time2)
        result2.addSuccess(test2)
        result1.addSuccess(test1)
        self.assertEqual([
            # test2 finishes first, and so is flushed first.
            ('time', start_time2),
            ('startTest', test2),
            ('time', end_time2),
            ('addSuccess', test2),
            ('stopTest', test2),
            # test1 finishes next, and thus follows.
            ('time', start_time1),
            ('startTest', test1),
            ('time', end_time1),
            ('addSuccess', test1),
            ('stopTest', test1),
            ], events)


class TestMergeTags(TestCase):

    def test_merge_unseen_gone_tag(self):
        # If an incoming "gone" tag isn't currently tagged one way or the
        # other, add it to the "gone" tags.
        current_tags = set(['present']), set(['missing'])
        changing_tags = set(), set(['going'])
        expected = set(['present']), set(['missing', 'going'])
        self.assertEqual(
            expected, _merge_tags(current_tags, changing_tags))

    def test_merge_incoming_gone_tag_with_current_new_tag(self):
        # If one of the incoming "gone" tags is one of the existing "new"
        # tags, then it overrides the "new" tag, leaving it marked as "gone".
        current_tags = set(['present', 'going']), set(['missing'])
        changing_tags = set(), set(['going'])
        expected = set(['present']), set(['missing', 'going'])
        self.assertEqual(
            expected, _merge_tags(current_tags, changing_tags))

    def test_merge_unseen_new_tag(self):
        current_tags = set(['present']), set(['missing'])
        changing_tags = set(['coming']), set()
        expected = set(['coming', 'present']), set(['missing'])
        self.assertEqual(
            expected, _merge_tags(current_tags, changing_tags))

    def test_merge_incoming_new_tag_with_current_gone_tag(self):
        # If one of the incoming "new" tags is currently marked as "gone",
        # then it overrides the "gone" tag, leaving it marked as "new".
        current_tags = set(['present']), set(['coming', 'missing'])
        changing_tags = set(['coming']), set()
        expected = set(['coming', 'present']), set(['missing'])
        self.assertEqual(
            expected, _merge_tags(current_tags, changing_tags))


class TestExtendedToOriginalResultDecoratorBase(TestCase):

    def make_26_result(self):
        self.result = Python26TestResult()
        self.make_converter()

    def make_27_result(self):
        self.result = Python27TestResult()
        self.make_converter()

    def make_converter(self):
        self.converter = ExtendedToOriginalDecorator(self.result)

    def make_extended_result(self):
        self.result = ExtendedTestResult()
        self.make_converter()

    def check_outcome_details(self, outcome):
        """Call an outcome with a details dict to be passed through."""
        # This dict is /not/ convertible - thats deliberate, as it should
        # not hit the conversion code path.
        details = {'foo': 'bar'}
        getattr(self.converter, outcome)(self, details=details)
        self.assertEqual([(outcome, self, details)], self.result._events)

    def get_details_and_string(self):
        """Get a details dict and expected string."""
        text1 = lambda: [_b("1\n2\n")]
        text2 = lambda: [_b("3\n4\n")]
        bin1 = lambda: [_b("5\n")]
        details = {'text 1': Content(ContentType('text', 'plain'), text1),
            'text 2': Content(ContentType('text', 'strange'), text2),
            'bin 1': Content(ContentType('application', 'binary'), bin1)}
        return (details,
                ("Binary content:\n"
                 "  bin 1 (application/binary)\n"
                 "\n"
                 "text 1: {{{\n"
                 "1\n"
                 "2\n"
                 "}}}\n"
                 "\n"
                 "text 2: {{{\n"
                 "3\n"
                 "4\n"
                 "}}}\n"))

    def check_outcome_details_to_exec_info(self, outcome, expected=None):
        """Call an outcome with a details dict to be made into exc_info."""
        # The conversion is a done using RemoteError and the string contents
        # of the text types in the details dict.
        if not expected:
            expected = outcome
        details, err_str = self.get_details_and_string()
        getattr(self.converter, outcome)(self, details=details)
        err = self.converter._details_to_exc_info(details)
        self.assertEqual([(expected, self, err)], self.result._events)

    def check_outcome_details_to_nothing(self, outcome, expected=None):
        """Call an outcome with a details dict to be swallowed."""
        if not expected:
            expected = outcome
        details = {'foo': 'bar'}
        getattr(self.converter, outcome)(self, details=details)
        self.assertEqual([(expected, self)], self.result._events)

    def check_outcome_details_to_string(self, outcome):
        """Call an outcome with a details dict to be stringified."""
        details, err_str = self.get_details_and_string()
        getattr(self.converter, outcome)(self, details=details)
        self.assertEqual([(outcome, self, err_str)], self.result._events)

    def check_outcome_details_to_arg(self, outcome, arg, extra_detail=None):
        """Call an outcome with a details dict to have an arg extracted."""
        details, _ = self.get_details_and_string()
        if extra_detail:
            details.update(extra_detail)
        getattr(self.converter, outcome)(self, details=details)
        self.assertEqual([(outcome, self, arg)], self.result._events)

    def check_outcome_exc_info(self, outcome, expected=None):
        """Check that calling a legacy outcome still works."""
        # calling some outcome with the legacy exc_info style api (no keyword
        # parameters) gets passed through.
        if not expected:
            expected = outcome
        err = sys.exc_info()
        getattr(self.converter, outcome)(self, err)
        self.assertEqual([(expected, self, err)], self.result._events)

    def check_outcome_exc_info_to_nothing(self, outcome, expected=None):
        """Check that calling a legacy outcome on a fallback works."""
        # calling some outcome with the legacy exc_info style api (no keyword
        # parameters) gets passed through.
        if not expected:
            expected = outcome
        err = sys.exc_info()
        getattr(self.converter, outcome)(self, err)
        self.assertEqual([(expected, self)], self.result._events)

    def check_outcome_nothing(self, outcome, expected=None):
        """Check that calling a legacy outcome still works."""
        if not expected:
            expected = outcome
        getattr(self.converter, outcome)(self)
        self.assertEqual([(expected, self)], self.result._events)

    def check_outcome_string_nothing(self, outcome, expected):
        """Check that calling outcome with a string calls expected."""
        getattr(self.converter, outcome)(self, "foo")
        self.assertEqual([(expected, self)], self.result._events)

    def check_outcome_string(self, outcome):
        """Check that calling outcome with a string works."""
        getattr(self.converter, outcome)(self, "foo")
        self.assertEqual([(outcome, self, "foo")], self.result._events)


class TestExtendedToOriginalResultDecorator(
    TestExtendedToOriginalResultDecoratorBase):

    def test_progress_py26(self):
        self.make_26_result()
        self.converter.progress(1, 2)

    def test_progress_py27(self):
        self.make_27_result()
        self.converter.progress(1, 2)

    def test_progress_pyextended(self):
        self.make_extended_result()
        self.converter.progress(1, 2)
        self.assertEqual([('progress', 1, 2)], self.result._events)

    def test_shouldStop(self):
        self.make_26_result()
        self.assertEqual(False, self.converter.shouldStop)
        self.converter.decorated.stop()
        self.assertEqual(True, self.converter.shouldStop)

    def test_startTest_py26(self):
        self.make_26_result()
        self.converter.startTest(self)
        self.assertEqual([('startTest', self)], self.result._events)

    def test_startTest_py27(self):
        self.make_27_result()
        self.converter.startTest(self)
        self.assertEqual([('startTest', self)], self.result._events)

    def test_startTest_pyextended(self):
        self.make_extended_result()
        self.converter.startTest(self)
        self.assertEqual([('startTest', self)], self.result._events)

    def test_startTestRun_py26(self):
        self.make_26_result()
        self.converter.startTestRun()
        self.assertEqual([], self.result._events)

    def test_startTestRun_py27(self):
        self.make_27_result()
        self.converter.startTestRun()
        self.assertEqual([('startTestRun',)], self.result._events)

    def test_startTestRun_pyextended(self):
        self.make_extended_result()
        self.converter.startTestRun()
        self.assertEqual([('startTestRun',)], self.result._events)

    def test_stopTest_py26(self):
        self.make_26_result()
        self.converter.stopTest(self)
        self.assertEqual([('stopTest', self)], self.result._events)

    def test_stopTest_py27(self):
        self.make_27_result()
        self.converter.stopTest(self)
        self.assertEqual([('stopTest', self)], self.result._events)

    def test_stopTest_pyextended(self):
        self.make_extended_result()
        self.converter.stopTest(self)
        self.assertEqual([('stopTest', self)], self.result._events)

    def test_stopTestRun_py26(self):
        self.make_26_result()
        self.converter.stopTestRun()
        self.assertEqual([], self.result._events)

    def test_stopTestRun_py27(self):
        self.make_27_result()
        self.converter.stopTestRun()
        self.assertEqual([('stopTestRun',)], self.result._events)

    def test_stopTestRun_pyextended(self):
        self.make_extended_result()
        self.converter.stopTestRun()
        self.assertEqual([('stopTestRun',)], self.result._events)

    def test_tags_py26(self):
        self.make_26_result()
        self.converter.tags(set([1]), set([2]))

    def test_tags_py27(self):
        self.make_27_result()
        self.converter.tags(set([1]), set([2]))

    def test_tags_pyextended(self):
        self.make_extended_result()
        self.converter.tags(set([1]), set([2]))
        self.assertEqual([('tags', set([1]), set([2]))], self.result._events)

    def test_time_py26(self):
        self.make_26_result()
        self.converter.time(1)

    def test_time_py27(self):
        self.make_27_result()
        self.converter.time(1)

    def test_time_pyextended(self):
        self.make_extended_result()
        self.converter.time(1)
        self.assertEqual([('time', 1)], self.result._events)


class TestExtendedToOriginalAddError(TestExtendedToOriginalResultDecoratorBase):

    outcome = 'addError'

    def test_outcome_Original_py26(self):
        self.make_26_result()
        self.check_outcome_exc_info(self.outcome)

    def test_outcome_Original_py27(self):
        self.make_27_result()
        self.check_outcome_exc_info(self.outcome)

    def test_outcome_Original_pyextended(self):
        self.make_extended_result()
        self.check_outcome_exc_info(self.outcome)

    def test_outcome_Extended_py26(self):
        self.make_26_result()
        self.check_outcome_details_to_exec_info(self.outcome)

    def test_outcome_Extended_py27(self):
        self.make_27_result()
        self.check_outcome_details_to_exec_info(self.outcome)

    def test_outcome_Extended_pyextended(self):
        self.make_extended_result()
        self.check_outcome_details(self.outcome)

    def test_outcome__no_details(self):
        self.make_extended_result()
        self.assertThat(
            lambda: getattr(self.converter, self.outcome)(self),
            Raises(MatchesException(ValueError)))


class TestExtendedToOriginalAddFailure(
    TestExtendedToOriginalAddError):

    outcome = 'addFailure'


class TestExtendedToOriginalAddExpectedFailure(
    TestExtendedToOriginalAddError):

    outcome = 'addExpectedFailure'

    def test_outcome_Original_py26(self):
        self.make_26_result()
        self.check_outcome_exc_info_to_nothing(self.outcome, 'addSuccess')

    def test_outcome_Extended_py26(self):
        self.make_26_result()
        self.check_outcome_details_to_nothing(self.outcome, 'addSuccess')



class TestExtendedToOriginalAddSkip(
    TestExtendedToOriginalResultDecoratorBase):

    outcome = 'addSkip'

    def test_outcome_Original_py26(self):
        self.make_26_result()
        self.check_outcome_string_nothing(self.outcome, 'addSuccess')

    def test_outcome_Original_py27(self):
        self.make_27_result()
        self.check_outcome_string(self.outcome)

    def test_outcome_Original_pyextended(self):
        self.make_extended_result()
        self.check_outcome_string(self.outcome)

    def test_outcome_Extended_py26(self):
        self.make_26_result()
        self.check_outcome_string_nothing(self.outcome, 'addSuccess')

    def test_outcome_Extended_py27_no_reason(self):
        self.make_27_result()
        self.check_outcome_details_to_string(self.outcome)

    def test_outcome_Extended_py27_reason(self):
        self.make_27_result()
        self.check_outcome_details_to_arg(self.outcome, 'foo',
            {'reason': Content(UTF8_TEXT, lambda:[_b('foo')])})

    def test_outcome_Extended_pyextended(self):
        self.make_extended_result()
        self.check_outcome_details(self.outcome)

    def test_outcome__no_details(self):
        self.make_extended_result()
        self.assertThat(
            lambda: getattr(self.converter, self.outcome)(self),
            Raises(MatchesException(ValueError)))


class TestExtendedToOriginalAddSuccess(
    TestExtendedToOriginalResultDecoratorBase):

    outcome = 'addSuccess'
    expected = 'addSuccess'

    def test_outcome_Original_py26(self):
        self.make_26_result()
        self.check_outcome_nothing(self.outcome, self.expected)

    def test_outcome_Original_py27(self):
        self.make_27_result()
        self.check_outcome_nothing(self.outcome)

    def test_outcome_Original_pyextended(self):
        self.make_extended_result()
        self.check_outcome_nothing(self.outcome)

    def test_outcome_Extended_py26(self):
        self.make_26_result()
        self.check_outcome_details_to_nothing(self.outcome, self.expected)

    def test_outcome_Extended_py27(self):
        self.make_27_result()
        self.check_outcome_details_to_nothing(self.outcome)

    def test_outcome_Extended_pyextended(self):
        self.make_extended_result()
        self.check_outcome_details(self.outcome)


class TestExtendedToOriginalAddUnexpectedSuccess(
    TestExtendedToOriginalResultDecoratorBase):

    outcome = 'addUnexpectedSuccess'
    expected = 'addFailure'

    def test_outcome_Original_py26(self):
        self.make_26_result()
        getattr(self.converter, self.outcome)(self)
        [event] = self.result._events
        self.assertEqual((self.expected, self), event[:2])

    def test_outcome_Original_py27(self):
        self.make_27_result()
        self.check_outcome_nothing(self.outcome)

    def test_outcome_Original_pyextended(self):
        self.make_extended_result()
        self.check_outcome_nothing(self.outcome)

    def test_outcome_Extended_py26(self):
        self.make_26_result()
        getattr(self.converter, self.outcome)(self)
        [event] = self.result._events
        self.assertEqual((self.expected, self), event[:2])

    def test_outcome_Extended_py27(self):
        self.make_27_result()
        self.check_outcome_details_to_nothing(self.outcome)

    def test_outcome_Extended_pyextended(self):
        self.make_extended_result()
        self.check_outcome_details(self.outcome)


class TestExtendedToOriginalResultOtherAttributes(
    TestExtendedToOriginalResultDecoratorBase):

    def test_other_attribute(self):
        class OtherExtendedResult:
            def foo(self):
                return 2
            bar = 1
        self.result = OtherExtendedResult()
        self.make_converter()
        self.assertEqual(1, self.converter.bar)
        self.assertEqual(2, self.converter.foo())


class TestNonAsciiResults(TestCase):
    """Test all kinds of tracebacks are cleanly interpreted as unicode

    Currently only uses weak "contains" assertions, would be good to be much
    stricter about the expected output. This would add a few failures for the
    current release of IronPython for instance, which gets some traceback
    lines muddled.
    """

    _sample_texts = (
        _u("pa\u026a\u03b8\u0259n"), # Unicode encodings only
        _u("\u5357\u7121"), # In ISO 2022 encodings
        _u("\xa7\xa7\xa7"), # In ISO 8859 encodings
        )
    
    _is_pypy = "__pypy__" in sys.builtin_module_names
    # Everything but Jython shows syntax errors on the current character
    _error_on_character = os.name != "java" and not _is_pypy

    def _run(self, stream, test):
        """Run the test, the same as in testtools.run but not to stdout"""
        result = TextTestResult(stream)
        result.startTestRun()
        try:
            return test.run(result)
        finally:
            result.stopTestRun()

    def _write_module(self, name, encoding, contents):
        """Create Python module on disk with contents in given encoding"""
        try:
            # Need to pre-check that the coding is valid or codecs.open drops
            # the file without closing it which breaks non-refcounted pythons
            codecs.lookup(encoding)
        except LookupError:
            self.skip("Encoding unsupported by implementation: %r" % encoding)
        f = codecs.open(os.path.join(self.dir, name + ".py"), "w", encoding)
        try:
            f.write(contents)
        finally:
            f.close()

    def _test_external_case(self, testline, coding="ascii", modulelevel="",
            suffix=""):
        """Create and run a test case in a seperate module"""
        self._setup_external_case(testline, coding, modulelevel, suffix)
        return self._run_external_case()

    def _setup_external_case(self, testline, coding="ascii", modulelevel="",
            suffix=""):
        """Create a test case in a seperate module"""
        _, prefix, self.modname = self.id().rsplit(".", 2)
        self.dir = tempfile.mkdtemp(prefix=prefix, suffix=suffix)
        self.addCleanup(shutil.rmtree, self.dir)
        self._write_module(self.modname, coding,
            # Older Python 2 versions don't see a coding declaration in a
            # docstring so it has to be in a comment, but then we can't
            # workaround bug: <http://ironpython.codeplex.com/workitem/26940>
            "# coding: %s\n"
            "import testtools\n"
            "%s\n"
            "class Test(testtools.TestCase):\n"
            "    def runTest(self):\n"
            "        %s\n" % (coding, modulelevel, testline))

    def _run_external_case(self):
        """Run the prepared test case in a seperate module"""
        sys.path.insert(0, self.dir)
        self.addCleanup(sys.path.remove, self.dir)
        module = __import__(self.modname)
        self.addCleanup(sys.modules.pop, self.modname)
        stream = StringIO()
        self._run(stream, module.Test())
        return stream.getvalue()

    def _silence_deprecation_warnings(self):
        """Shut up DeprecationWarning for this test only"""
        warnings.simplefilter("ignore", DeprecationWarning)
        self.addCleanup(warnings.filters.remove, warnings.filters[0])

    def _get_sample_text(self, encoding="unicode_internal"):
        if encoding is None and str_is_unicode:
           encoding = "unicode_internal"
        for u in self._sample_texts:
            try:
                b = u.encode(encoding)
                if u == b.decode(encoding):
                   if str_is_unicode:
                       return u, u
                   return u, b
            except (LookupError, UnicodeError):
                pass
        self.skip("Could not find a sample text for encoding: %r" % encoding)

    def _as_output(self, text):
        return text

    def test_non_ascii_failure_string(self):
        """Assertion contents can be non-ascii and should get decoded"""
        text, raw = self._get_sample_text(_get_exception_encoding())
        textoutput = self._test_external_case("self.fail(%s)" % _r(raw))
        self.assertIn(self._as_output(text), textoutput)

    def test_non_ascii_failure_string_via_exec(self):
        """Assertion via exec can be non-ascii and still gets decoded"""
        text, raw = self._get_sample_text(_get_exception_encoding())
        textoutput = self._test_external_case(
            testline='exec ("self.fail(%s)")' % _r(raw))
        self.assertIn(self._as_output(text), textoutput)

    def test_control_characters_in_failure_string(self):
        """Control characters in assertions should be escaped"""
        textoutput = self._test_external_case("self.fail('\\a\\a\\a')")
        self.expectFailure("Defense against the beeping horror unimplemented",
            self.assertNotIn, self._as_output("\a\a\a"), textoutput)
        self.assertIn(self._as_output(_u("\uFFFD\uFFFD\uFFFD")), textoutput)

    def test_os_error(self):
        """Locale error messages from the OS shouldn't break anything"""
        textoutput = self._test_external_case(
            modulelevel="import os",
            testline="os.mkdir('/')")
        if os.name != "nt" or sys.version_info < (2, 5):
            self.assertIn(self._as_output("OSError: "), textoutput)
        else:
            self.assertIn(self._as_output("WindowsError: "), textoutput)

    def test_assertion_text_shift_jis(self):
        """A terminal raw backslash in an encoded string is weird but fine"""
        example_text = _u("\u5341")
        textoutput = self._test_external_case(
            coding="shift_jis",
            testline="self.fail('%s')" % example_text)
        if str_is_unicode:
            output_text = example_text
        else:
            output_text = example_text.encode("shift_jis").decode(
                _get_exception_encoding(), "replace")
        self.assertIn(self._as_output("AssertionError: %s" % output_text),
            textoutput)

    def test_file_comment_iso2022_jp(self):
        """Control character escapes must be preserved if valid encoding"""
        example_text, _ = self._get_sample_text("iso2022_jp")
        textoutput = self._test_external_case(
            coding="iso2022_jp",
            testline="self.fail('Simple') # %s" % example_text)
        self.assertIn(self._as_output(example_text), textoutput)

    def test_unicode_exception(self):
        """Exceptions that can be formated losslessly as unicode should be"""
        example_text, _ = self._get_sample_text()
        exception_class = (
            "class FancyError(Exception):\n"
            # A __unicode__ method does nothing on py3k but the default works
            "    def __unicode__(self):\n"
            "        return self.args[0]\n")
        textoutput = self._test_external_case(
            modulelevel=exception_class,
            testline="raise FancyError(%s)" % _r(example_text))
        self.assertIn(self._as_output(example_text), textoutput)

    def test_unprintable_exception(self):
        """A totally useless exception instance still prints something"""
        exception_class = (
            "class UnprintableError(Exception):\n"
            "    def __str__(self):\n"
            "        raise RuntimeError\n"
            "    def __unicode__(self):\n"
            "        raise RuntimeError\n"
            "    def __repr__(self):\n"
            "        raise RuntimeError\n")
        textoutput = self._test_external_case(
            modulelevel=exception_class,
            testline="raise UnprintableError")
        self.assertIn(self._as_output(
            "UnprintableError: <unprintable UnprintableError object>\n"),
            textoutput)

    def test_string_exception(self):
        """Raise a string rather than an exception instance if supported"""
        if sys.version_info > (2, 6):
            self.skip("No string exceptions in Python 2.6 or later")
        elif sys.version_info > (2, 5):
            self._silence_deprecation_warnings()
        textoutput = self._test_external_case(testline="raise 'plain str'")
        self.assertIn(self._as_output("\nplain str\n"), textoutput)

    def test_non_ascii_dirname(self):
        """Script paths in the traceback can be non-ascii"""
        text, raw = self._get_sample_text(sys.getfilesystemencoding())
        textoutput = self._test_external_case(
            # Avoid bug in Python 3 by giving a unicode source encoding rather
            # than just ascii which raises a SyntaxError with no other details
            coding="utf-8",
            testline="self.fail('Simple')",
            suffix=raw)
        self.assertIn(self._as_output(text), textoutput)

    def test_syntax_error(self):
        """Syntax errors should still have fancy special-case formatting"""
        textoutput = self._test_external_case("exec ('f(a, b c)')")
        self.assertIn(self._as_output(
            '  File "<string>", line 1\n'
            '    f(a, b c)\n'
            + ' ' * self._error_on_character +
            '          ^\n'
            'SyntaxError: '
            ), textoutput)

    def test_syntax_error_malformed(self):
        """Syntax errors with bogus parameters should break anything"""
        textoutput = self._test_external_case("raise SyntaxError(3, 2, 1)")
        self.assertIn(self._as_output("\nSyntaxError: "), textoutput)

    def test_syntax_error_import_binary(self):
        """Importing a binary file shouldn't break SyntaxError formatting"""
        if sys.version_info < (2, 5):
            # Python 2.4 assumes the file is latin-1 and tells you off
            self._silence_deprecation_warnings()
        self._setup_external_case("import bad")
        f = open(os.path.join(self.dir, "bad.py"), "wb")
        try:
            f.write(_b("x\x9c\xcb*\xcd\xcb\x06\x00\x04R\x01\xb9"))
        finally:
            f.close()
        textoutput = self._run_external_case()
        self.assertIn(self._as_output("\nSyntaxError: "), textoutput)

    def test_syntax_error_line_iso_8859_1(self):
        """Syntax error on a latin-1 line shows the line decoded"""
        text, raw = self._get_sample_text("iso-8859-1")
        textoutput = self._setup_external_case("import bad")
        self._write_module("bad", "iso-8859-1",
            "# coding: iso-8859-1\n! = 0 # %s\n" % text)
        textoutput = self._run_external_case()
        self.assertIn(self._as_output(_u(
            #'bad.py", line 2\n'
            '    ! = 0 # %s\n'
            '    ^\n'
            'SyntaxError: ') %
            (text,)), textoutput)

    def test_syntax_error_line_iso_8859_5(self):
        """Syntax error on a iso-8859-5 line shows the line decoded"""
        text, raw = self._get_sample_text("iso-8859-5")
        textoutput = self._setup_external_case("import bad")
        self._write_module("bad", "iso-8859-5",
            "# coding: iso-8859-5\n%% = 0 # %s\n" % text)
        textoutput = self._run_external_case()
        self.assertIn(self._as_output(_u(
            #'bad.py", line 2\n'
            '    %% = 0 # %s\n'
            + ' ' * self._error_on_character +
            '   ^\n'
            'SyntaxError: ') %
            (text,)), textoutput)

    def test_syntax_error_line_euc_jp(self):
        """Syntax error on a euc_jp line shows the line decoded"""
        text, raw = self._get_sample_text("euc_jp")
        textoutput = self._setup_external_case("import bad")
        self._write_module("bad", "euc_jp",
            "# coding: euc_jp\n$ = 0 # %s\n" % text)
        textoutput = self._run_external_case()
        # pypy uses cpython's multibyte codecs so has their behavior here
        if self._is_pypy:
            self._error_on_character = True
        self.assertIn(self._as_output(_u(
            #'bad.py", line 2\n'
            '    $ = 0 # %s\n'
            + ' ' * self._error_on_character +
            '   ^\n'
            'SyntaxError: ') %
            (text,)), textoutput)

    def test_syntax_error_line_utf_8(self):
        """Syntax error on a utf-8 line shows the line decoded"""
        text, raw = self._get_sample_text("utf-8")
        textoutput = self._setup_external_case("import bad")
        self._write_module("bad", "utf-8", _u("\ufeff^ = 0 # %s\n") % text)
        textoutput = self._run_external_case()
        self.assertIn(self._as_output(_u(
            'bad.py", line 1\n'
            '    ^ = 0 # %s\n'
            + ' ' * self._error_on_character +
            '   ^\n'
            'SyntaxError: ') %
            text), textoutput)


class TestNonAsciiResultsWithUnittest(TestNonAsciiResults):
    """Test that running under unittest produces clean ascii strings"""

    def _run(self, stream, test):
        from unittest import TextTestRunner as _Runner
        return _Runner(stream).run(test)

    def _as_output(self, text):
        if str_is_unicode:
            return text
        return text.encode("utf-8")


class TestDetailsToStr(TestCase):

    def test_no_details(self):
        string = _details_to_str({})
        self.assertThat(string, Equals(''))

    def test_binary_content(self):
        content = content_from_stream(
            StringIO('foo'), content_type=ContentType('image', 'jpeg'))
        string = _details_to_str({'attachment': content})
        self.assertThat(
            string, Equals("""\
Binary content:
  attachment (image/jpeg)
"""))

    def test_single_line_content(self):
        content = text_content('foo')
        string = _details_to_str({'attachment': content})
        self.assertThat(string, Equals('attachment: {{{foo}}}\n'))

    def test_multi_line_text_content(self):
        content = text_content('foo\nbar\nbaz')
        string = _details_to_str({'attachment': content})
        self.assertThat(string, Equals('attachment: {{{\nfoo\nbar\nbaz\n}}}\n'))

    def test_special_text_content(self):
        content = text_content('foo')
        string = _details_to_str({'attachment': content}, special='attachment')
        self.assertThat(string, Equals('foo\n'))

    def test_multiple_text_content(self):
        string = _details_to_str(
            {'attachment': text_content('foo\nfoo'),
             'attachment-1': text_content('bar\nbar')})
        self.assertThat(
            string, Equals('attachment: {{{\n'
                           'foo\n'
                           'foo\n'
                           '}}}\n'
                           '\n'
                           'attachment-1: {{{\n'
                           'bar\n'
                           'bar\n'
                           '}}}\n'))

    def test_empty_attachment(self):
        string = _details_to_str({'attachment': text_content('')})
        self.assertThat(
            string, Equals("""\
Empty attachments:
  attachment
"""))

    def test_lots_of_different_attachments(self):
        jpg = lambda x: content_from_stream(
            StringIO(x), ContentType('image', 'jpeg'))
        attachments = {
            'attachment': text_content('foo'),
            'attachment-1': text_content('traceback'),
            'attachment-2': jpg('pic1'),
            'attachment-3': text_content('bar'),
            'attachment-4': text_content(''),
            'attachment-5': jpg('pic2'),
            }
        string = _details_to_str(attachments, special='attachment-1')
        self.assertThat(
            string, Equals("""\
Binary content:
  attachment-2 (image/jpeg)
  attachment-5 (image/jpeg)
Empty attachments:
  attachment-4

attachment: {{{foo}}}
attachment-3: {{{bar}}}

traceback
"""))


class TestByTestResultTests(TestCase):

    def setUp(self):
        super(TestByTestResultTests, self).setUp()
        self.log = []
        self.result = TestByTestResult(self.on_test)
        now = iter(range(5))
        self.result._now = lambda: advance_iterator(now)

    def assertCalled(self, **kwargs):
        defaults = {
            'test': self,
            'tags': set(),
            'details': None,
            'start_time': 0,
            'stop_time': 1,
            }
        defaults.update(kwargs)
        self.assertEqual([defaults], self.log)

    def on_test(self, **kwargs):
        self.log.append(kwargs)

    def test_no_tests_nothing_reported(self):
        self.result.startTestRun()
        self.result.stopTestRun()
        self.assertEqual([], self.log)

    def test_add_success(self):
        self.result.startTest(self)
        self.result.addSuccess(self)
        self.result.stopTest(self)
        self.assertCalled(status='success')

    def test_add_success_details(self):
        self.result.startTest(self)
        details = {'foo': 'bar'}
        self.result.addSuccess(self, details=details)
        self.result.stopTest(self)
        self.assertCalled(status='success', details=details)

    def test_global_tags(self):
        self.result.tags(['foo'], [])
        self.result.startTest(self)
        self.result.addSuccess(self)
        self.result.stopTest(self)
        self.assertCalled(status='success', tags=set(['foo']))

    def test_local_tags(self):
        self.result.tags(['foo'], [])
        self.result.startTest(self)
        self.result.tags(['bar'], [])
        self.result.addSuccess(self)
        self.result.stopTest(self)
        self.assertCalled(status='success', tags=set(['foo', 'bar']))

    def test_add_error(self):
        self.result.startTest(self)
        try:
            1/0
        except ZeroDivisionError:
            error = sys.exc_info()
        self.result.addError(self, error)
        self.result.stopTest(self)
        self.assertCalled(
            status='error',
            details={'traceback': TracebackContent(error, self)})

    def test_add_error_details(self):
        self.result.startTest(self)
        details = {"foo": text_content("bar")}
        self.result.addError(self, details=details)
        self.result.stopTest(self)
        self.assertCalled(status='error', details=details)

    def test_add_failure(self):
        self.result.startTest(self)
        try:
            self.fail("intentional failure")
        except self.failureException:
            failure = sys.exc_info()
        self.result.addFailure(self, failure)
        self.result.stopTest(self)
        self.assertCalled(
            status='failure',
            details={'traceback': TracebackContent(failure, self)})

    def test_add_failure_details(self):
        self.result.startTest(self)
        details = {"foo": text_content("bar")}
        self.result.addFailure(self, details=details)
        self.result.stopTest(self)
        self.assertCalled(status='failure', details=details)

    def test_add_xfail(self):
        self.result.startTest(self)
        try:
            1/0
        except ZeroDivisionError:
            error = sys.exc_info()
        self.result.addExpectedFailure(self, error)
        self.result.stopTest(self)
        self.assertCalled(
            status='xfail',
            details={'traceback': TracebackContent(error, self)})

    def test_add_xfail_details(self):
        self.result.startTest(self)
        details = {"foo": text_content("bar")}
        self.result.addExpectedFailure(self, details=details)
        self.result.stopTest(self)
        self.assertCalled(status='xfail', details=details)

    def test_add_unexpected_success(self):
        self.result.startTest(self)
        details = {'foo': 'bar'}
        self.result.addUnexpectedSuccess(self, details=details)
        self.result.stopTest(self)
        self.assertCalled(status='success', details=details)

    def test_add_skip_reason(self):
        self.result.startTest(self)
        reason = self.getUniqueString()
        self.result.addSkip(self, reason)
        self.result.stopTest(self)
        self.assertCalled(
            status='skip', details={'reason': text_content(reason)})

    def test_add_skip_details(self):
        self.result.startTest(self)
        details = {'foo': 'bar'}
        self.result.addSkip(self, details=details)
        self.result.stopTest(self)
        self.assertCalled(status='skip', details=details)

    def test_twice(self):
        self.result.startTest(self)
        self.result.addSuccess(self, details={'foo': 'bar'})
        self.result.stopTest(self)
        self.result.startTest(self)
        self.result.addSuccess(self)
        self.result.stopTest(self)
        self.assertEqual(
            [{'test': self,
              'status': 'success',
              'start_time': 0,
              'stop_time': 1,
              'tags': set(),
              'details': {'foo': 'bar'}},
             {'test': self,
              'status': 'success',
              'start_time': 2,
              'stop_time': 3,
              'tags': set(),
              'details': None},
             ],
            self.log)


class TestTagger(TestCase):

    def test_tags_tests(self):
        result = ExtendedTestResult()
        tagger = Tagger(result, set(['foo']), set(['bar']))
        test1, test2 = self, make_test()
        tagger.startTest(test1)
        tagger.addSuccess(test1)
        tagger.stopTest(test1)
        tagger.startTest(test2)
        tagger.addSuccess(test2)
        tagger.stopTest(test2)
        self.assertEqual(
            [('startTest', test1),
             ('tags', set(['foo']), set(['bar'])),
             ('addSuccess', test1),
             ('stopTest', test1),
             ('startTest', test2),
             ('tags', set(['foo']), set(['bar'])),
             ('addSuccess', test2),
             ('stopTest', test2),
             ], result._events)


def test_suite():
    from unittest import TestLoader
    return TestLoader().loadTestsFromName(__name__)
