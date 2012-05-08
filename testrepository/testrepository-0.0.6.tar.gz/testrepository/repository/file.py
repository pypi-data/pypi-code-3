#
# Copyright (c) 2009, 2010 Testrepository Contributors
# 
# Licensed under either the Apache License, Version 2.0 or the BSD 3-clause
# license at the users choice. A copy of both licenses are available in the
# project source as Apache-2.0 and BSD. You may not use this file except in
# compliance with one of these two licences.
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under these licenses is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the
# license you chose for the specific language governing permissions and
# limitations under that license.

"""Persistent storage of test results."""

from cStringIO import StringIO
try:
    import anydbm as dbm
except ImportError:
    import dbm
import errno
import os.path
import sys
import tempfile

import subunit
from subunit import TestProtocolClient

from testrepository.repository import (
    AbstractRepository,
    AbstractRepositoryFactory,
    AbstractTestRun,
    RepositoryNotFound,
    )
from testrepository.utils import timedelta_to_seconds


def atomicish_rename(source, target):
    if os.name != "posix" and os.path.exists(target):
        os.remove(target)
    os.rename(source, target)


class RepositoryFactory(AbstractRepositoryFactory):

    def initialise(klass, url):
        """Create a repository at url/path."""
        base = os.path.join(os.path.expanduser(url), '.testrepository')
        os.mkdir(base)
        stream = file(os.path.join(base, 'format'), 'wb')
        try:
            stream.write('1\n')
        finally:
            stream.close()
        result = Repository(base)
        result._write_next_stream(0)
        return result

    def open(self, url):
        path = os.path.expanduser(url)
        base = os.path.join(path, '.testrepository')
        try:
            stream = file(os.path.join(base, 'format'), 'rb')
        except (IOError, OSError), e:
            if e.errno == errno.ENOENT:
                raise RepositoryNotFound(url)
            raise
        if '1\n' != stream.read():
            raise ValueError(url)
        return Repository(base)


class Repository(AbstractRepository):
    """Disk based storage of test results.
    
    This repository stores each stream it receives as a file in a directory.
    Indices are then built on top of this basic store.
    
    This particular disk layout is subject to change at any time, as its
    primarily a bootstrapping exercise at this point. Any changes made are
    likely to have an automatic upgrade process.
    """

    def __init__(self, base):
        """Create a file-based repository object for the repo at 'base'.

        :param base: The path to the repository.
        """
        self.base = base
    
    def _allocate(self):
        # XXX: lock the file. K?!
        value = self.count()
        self._write_next_stream(value + 1)
        return value

    def _next_stream(self):
        next_content = file(os.path.join(self.base, 'next-stream'), 'rb').read()
        try:
            return int(next_content)
        except ValueError:
            raise ValueError("Corrupt next-stream file: %r" % next_content)

    def count(self):
        return self._next_stream()

    def latest_id(self):
        result = self._next_stream() - 1
        if result < 0:
            raise KeyError("No tests in repository")
        return result
 
    def get_failing(self):
        try:
            run_subunit_content = file(
                os.path.join(self.base, "failing"), 'rb').read()
        except IOError:
            err = sys.exc_info()[1]
            if err.errno == errno.ENOENT:
                run_subunit_content = ''
            else:
                raise
        return _DiskRun(None, run_subunit_content)

    def get_test_run(self, run_id):
        run_subunit_content = file(
            os.path.join(self.base, str(run_id)), 'rb').read()
        return _DiskRun(run_id, run_subunit_content)

    def _get_inserter(self, partial):
        return _Inserter(self, partial)

    def _get_test_times(self, test_ids):
        # May be too slow, but build and iterate.
        # 'c' because an existing repo may be missing a file.
        db = dbm.open(self._path('times.dbm'), 'c')
        try:
            result = {}
            for test_id in test_ids:
                if type(test_id) != str:
                    test_id = test_id.encode('utf8')
                duration = db.get(test_id, None)
                if duration is not None:
                    result[test_id] = float(duration)
            return result
        finally:
            db.close()

    def _path(self, suffix):
        return os.path.join(self.base, suffix)

    def _write_next_stream(self, value):
        # Note that this is unlocked and not threadsafe : for now, shrug - single
        # user, repo-per-working-tree model makes this acceptable in the short
        # term. Likewise we don't fsync - this data isn't valuable enough to
        # force disk IO.
        prefix = self._path('next-stream')
        stream = file(prefix + '.new', 'wb')
        try:
            stream.write('%d\n' % value)
        finally:
            stream.close()
        atomicish_rename(prefix + '.new', prefix)


class _DiskRun(AbstractTestRun):
    """A test run that was inserted into the repository."""

    def __init__(self, run_id, subunit_content):
        """Create a _DiskRun with the content subunit_content."""
        self._run_id = run_id
        self._content = subunit_content

    def get_id(self):
        return self._run_id

    def get_subunit_stream(self):
        return StringIO(self._content)

    def get_test(self):
        return subunit.ProtocolTestCase(self.get_subunit_stream())


class _SafeInserter(TestProtocolClient):

    def __init__(self, repository, partial=False):
        # XXX: Perhaps should factor into a decorator and use an unaltered
        # TestProtocolClient.
        self._repository = repository
        fd, name = tempfile.mkstemp(dir=self._repository.base)
        self.fname = name
        stream = os.fdopen(fd, 'wb')
        self.partial = partial
        # The time take by each test, flushed at the end.
        self._times = {}
        self._test_start = None
        self._time = None
        TestProtocolClient.__init__(self, stream)

    def startTestRun(self):
        pass

    def stopTestRun(self):
        # TestProtocolClient.stopTestRun(self)
        self._stream.flush()
        self._stream.close()
        run_id = self._name()
        final_path = os.path.join(self._repository.base, str(run_id))
        atomicish_rename(self.fname, final_path)
        # May be too slow, but build and iterate.
        db = dbm.open(self._repository._path('times.dbm'), 'c')
        try:
            db_times = {}
            for key, value in self._times.items():
                if type(key) != str:
                    key = key.encode('utf8')
                db_times[key] = value
            db.update(db_times)
        finally:
            db.close()
        return run_id

    def _cancel(self):
        """Cancel an insertion."""
        self._stream.close()
        os.unlink(self.fname)

    def startTest(self, test):
        result = TestProtocolClient.startTest(self, test)
        self._test_start = self._time
        return result

    def stopTest(self, test):
        result = TestProtocolClient.stopTest(self, test)
        if None in (self._test_start, self._time):
            return result
        duration_seconds = timedelta_to_seconds(self._time - self._test_start)
        self._times[test.id()] = str(duration_seconds)
        return result

    def time(self, timestamp):
        result = TestProtocolClient.time(self, timestamp)
        self._time = timestamp
        return result


class _FailingInserter(_SafeInserter):
    """Insert a stream into the 'failing' file."""

    def _name(self):
        return "failing"


class _Inserter(_SafeInserter):

    def _name(self):
        return self._repository._allocate()

    def stopTestRun(self):
        run_id = _SafeInserter.stopTestRun(self)
        # XXX: locking (other inserts may happen while we update the failing
        # file).
        # Combine failing + this run : strip passed tests, add failures.
        # use memory repo to aggregate. a bit awkward on layering ;).
        import memory
        repo = memory.Repository()
        if self.partial:
            # Seed with current failing
            inserter = repo.get_inserter()
            inserter.startTestRun()
            failing = self._repository.get_failing()
            failing.get_test().run(inserter)
            inserter.stopTestRun()
        inserter= repo.get_inserter(partial=True)
        inserter.startTestRun()
        run = self._repository.get_test_run(run_id)
        run.get_test().run(inserter)
        inserter.stopTestRun()
        # and now write to failing
        inserter = _FailingInserter(self._repository)
        inserter.startTestRun()
        try:
            try:
                repo.get_failing().get_test().run(inserter)
            except:
                inserter._cancel()
                raise
        finally:
            inserter.stopTestRun()
        return run_id
