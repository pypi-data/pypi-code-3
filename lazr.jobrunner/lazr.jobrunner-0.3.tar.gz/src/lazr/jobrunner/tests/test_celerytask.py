 # Copyright 2012 Canonical Ltd. All rights reserved.
#
# This file is part of lazr.jobrunner
#
# lazr.jobrunner is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# lazr.jobrunner is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public
# License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with lazr.jobrunner. If not, see <http://www.gnu.org/licenses/>.

__metaclass__ = type


import contextlib
import errno
import json
import os
import os.path
from resource import (
    getrlimit,
    RLIMIT_AS,
    )
import shutil
import subprocess
import tempfile
from time import sleep
from unittest import TestCase
import urllib2

os.environ.setdefault('CELERY_CONFIG_MODULE', 'lazr.jobrunner.celeryconfig')

from celery.exceptions import SoftTimeLimitExceeded

from lazr.jobrunner.celerytask import RunJob
from lazr.jobrunner.jobrunner import (
    JobStatus,
    )
from lazr.jobrunner.tests.test_jobrunner import (
    FakeJob,
    )


def get_root():
    import lazr.jobrunner
    root = os.path.join(os.path.dirname(lazr.jobrunner.__file__), '../../../')
    return os.path.normpath(root)


@contextlib.contextmanager
def running(cmd_name, cmd_args, env=None, cwd=None):
    proc = subprocess.Popen((cmd_name,) + cmd_args, env=env,
                            stderr=subprocess.PIPE, cwd=cwd)
    try:
        yield proc
    finally:
        proc.terminate()
        proc.wait()


def celeryd(config_module, file_job_dir, queue='celery'):
    cmd_args = ('--config', config_module, '--queue', queue)
    environ = dict(os.environ)
    environ['FILE_JOB_DIR'] = file_job_dir
    return running('bin/celeryd', cmd_args, environ, cwd=get_root())


@contextlib.contextmanager
def tempdir():
    dirname = tempfile.mkdtemp()
    try:
        yield dirname
    finally:
        shutil.rmtree(dirname)


class FakeJobSource:

    memory_limit = None

    def __init__(self):
        self.jobs = {}

    def get(self, job_id):
        return self.jobs[job_id]


class FileJob(FakeJob):

    def __init__(self, job_source, job_id, output=None,
                 status=JobStatus.WAITING, exception=None, sleep=None):
        super(FileJob, self).__init__(job_id)
        self.job_source = job_source
        self.output = output
        self.status = status
        self.exception = exception
        self.sleep = sleep

    def save(self):
        self.job_source.set(self)

    def queue(self, manage_transaction=False, abort_transaction=False):
        self.job_source.set_output(
            self, 'queue(manage_transaction=%s, abort_transaction=%s)\n'
            % (manage_transaction, abort_transaction))
        self.status = JobStatus.WAITING

    def run(self):
        super(FileJob, self).run()
        if self.sleep is not None:
            sleep(self.sleep)
        if self.exception is not None:
            raise Exception(self.exception)
        if self.output is not None:
            self.job_source.set_output(self, self.output)


class FileJobSource:

    memory_limit = None

    def __init__(self, root):
        self.root = root
        self.job_root = os.path.join(self.root, 'job')
        self.output_root = os.path.join(self.root, 'output')

        def ensure_dir(path):
            try:
                os.mkdir(path)
            except OSError, e:
                if e.errno != errno.EEXIST:
                    raise
        ensure_dir(self.job_root)
        ensure_dir(self.output_root)

    def _job_file(self, job_id, mode):
        return open(os.path.join(self.job_root, str(job_id)), mode)

    def _job_output_file(self, job_id, mode):
        return open(os.path.join(self.output_root, str(job_id)), mode)

    def get(self, job_id):
        with self._job_file(job_id, 'r') as job_file:
            job_data = json.load(job_file)
            job_data['status'] = JobStatus.by_value[job_data['status']]
            return FileJob(self, **job_data)

    def set(self, job):
        with self._job_file(job.job_id, 'w') as job_file:
            job_info = {
                'job_id': job.job_id,
                'output': job.output,
                'status': job.status.value,
                'exception': job.exception,
                'sleep': job.sleep,
            }
            json.dump(job_info, job_file)

    def get_output(self, job):
        try:
            with self._job_output_file(job.job_id, 'r') as job_output_file:
                    return job_output_file.read()
        except IOError, e:
            if e.errno == errno.ENOENT:
                return None
            raise

    def set_output(self, job, output):
        with self._job_output_file(job.job_id, 'a') as job_output_file:
            job_output_file.write(output)


class RunFileJob(RunJob):

    name = 'run_file_job'

    file_job_dir = None

    @property
    def job_source(self):
        return FileJobSource(self.file_job_dir)


class RunFileJobNoResult(RunFileJob):

    ignore_result = True

    name = 'run_file_job_no_result'


class TestRunJob(TestCase):

    @staticmethod
    def makeFakeJobSource(job=None):
        js = FakeJobSource()
        if job is None:
            job = FakeJob(10)
        js.jobs[job.job_id] = job
        return js

    @staticmethod
    def runJob(js):
        task = RunJob()
        task.job_source = js
        task.run(10)

    def test_run(self):
        js = self.makeFakeJobSource()
        self.assertTrue(js.jobs[10].unrun)
        self.runJob(js)
        self.assertFalse(js.jobs[10].unrun)

    def test_memory_limit(self):

        class MemoryCheckJob(FakeJob):

            def run(self):
                super(MemoryCheckJob, self).run()
                self.current_memory_limit = getrlimit(RLIMIT_AS)[0]

        start_limits = getrlimit(RLIMIT_AS)
        js = FakeJobSource()
        job = MemoryCheckJob(10)
        js.jobs[10] = job
        js.memory_limit = 1024 ** 3
        task = RunJob()
        task.job_source = js
        task.run(10)
        self.assertEqual(1024 ** 3, job.current_memory_limit)
        self.assertEqual(start_limits, getrlimit(RLIMIT_AS))

    def test_acquires_lease(self):
        js = self.makeFakeJobSource()
        self.assertFalse(js.jobs[10].lease_held)
        self.runJob(js)
        self.assertTrue(js.jobs[10].lease_held)

    def test_skips_failed_acquisition(self):
        js = self.makeFakeJobSource()
        js.jobs[10].acquireLease()
        self.runJob(js)
        self.assertTrue(js.jobs[10].unrun)


class TestCeleryD(TestCase):

    def getQueueInfo(self):
        auth_handler = urllib2.HTTPBasicAuthHandler()
        auth_handler.add_password(
            realm='Management: Web UI', user='guest', passwd='guest',
            uri='http://localhost:55672/api/queues')
        opener = urllib2.build_opener(auth_handler)
        info = opener.open('http://localhost:55672/api/queues').read()
        info = json.loads(info)
        # info is a list of dictionaries with details about the queues.
        # We are only interested in the name of the queues and the
        # number of messages they hold.
        info = [(item['name'], item['messages']) for item in info]
        return dict(info)

    def setUp(self):
        super(TestCeleryD, self).setUp()
        try:
            self.queue_status_during_setup = self.getQueueInfo()
        except urllib2.URLError:
            # The rabbitmq-management package is currently broken
            # on Precise, so the RabbitMQ management interface may
            # not be available.
            pass

    def tearDown(self):
        try:
            current_queue_status = self.getQueueInfo()
        except urllib2.URLError:
            # See setUp()
            return
        bad_queues = []
        for name in current_queue_status:
            old_value = self.queue_status_during_setup.get(name)
            new_value = current_queue_status[name]
            if old_value is not None:
                if old_value != new_value:
                    bad_queues.append(
                        'number of messages in queue %s changed from %i to %i'
                        % (name, old_value, new_value))
            elif new_value != 0:
                bad_queues.append(
                    'new queue %s with %r messages' % (name, new_value))
            else:
                # We have the same number of messages in an existing
                # queue. That is probably fine.
                pass
        if bad_queues:
            error = (
                'Test left message queues in a different state:\n%s'
                % '\n'.join(bad_queues))
            self.fail(error)

    def test_run_job(self):
        with tempdir() as temp_dir:
            js = FileJobSource(temp_dir)
            job = FileJob(js, 10, 'my_output')
            job.save()
            result = RunFileJob.delay(10)
            self.assertIs(None, js.get_output(job))
            self.assertEqual(JobStatus.WAITING, job.status)
            with celeryd('lazr.jobrunner.tests.config1', temp_dir):
                result.wait(10)
            job = js.get(job.job_id)
            self.assertEqual('my_output', js.get_output(job))
            self.assertEqual(JobStatus.COMPLETED, job.status)

    def run_file_job(self, temp_dir, config='lazr.jobrunner.tests.config1',
                     queue='celery', **kwargs):
        js = FileJobSource(temp_dir)
        job = FileJob(js, 10, **kwargs)
        job.save()
        result = RunFileJob.apply_async(args=(10, ), queue=queue)
        with celeryd(config, temp_dir, queue) as proc:
            try:
                result.wait(10)
            except SoftTimeLimitExceeded:
                pass
        job = js.get(job.job_id)
        return job, js, proc

    def run_file_job_ignore_result(self, temp_dir, wait_time,
                                   config='lazr.jobrunner.tests.config1',
                                   queue='celery', **kwargs):
        # If a timeout occurs when Task.ignore_results == True,
        # two messages are sent, a call of result.wait() will
        # consume the first message; the second message will stay in
        # the result message queue.
        js = FileJobSource(temp_dir)
        job = FileJob(js, 10, **kwargs)
        job.save()
        RunFileJobNoResult.apply_async(args=(10, ), queue=queue)
        with celeryd(config, temp_dir, queue) as proc:
            sleep(wait_time)
        job = js.get(job.job_id)
        return job, js, proc

    def test_run_job_emits_oopses(self):
        with tempdir() as temp_dir:
            job, js, proc = self.run_file_job(
                temp_dir, exception='Catch me if you can!')
            err = proc.stderr.read()
            self.assertEqual(JobStatus.FAILED, job.status)
            self.assertIs(None, job.job_source.get_output(job))
            self.assertIn(
                "OOPS while executing job 10: [] Exception(u'Catch me if you"
                " can!',)", err)

    def test_timeout_long(self):
        """Raises exception when a job exceeds the configured time limit."""
        with tempdir() as temp_dir:
            job, js, proc = self.run_file_job_ignore_result(
                temp_dir, wait_time=2,
                config='lazr.jobrunner.tests.time_limit_config',
                sleep=3)
        self.assertEqual(JobStatus.FAILED, job.status)
        err = proc.stderr.read()
        self.assertIn(
            'OOPS while executing job 10: [] SoftTimeLimitExceeded', err)

    def test_timeout_in_fast_lane_passes_in_slow_lane(self):
        # If a fast and a slow lane are configured, jobs which time out
        # in the fast lane are queued again in the slow lane.
        with tempdir() as temp_dir:
            with celeryd(
                'lazr.jobrunner.tests.time_limit_config_slow_lane',
                temp_dir, queue='standard_slow'):
                # The fast lane times out after one second; the job
                # is then queued again in the slow lane, where it runs
                # three seconds. Wait five seconds to check the result.
                job, js, proc = self.run_file_job_ignore_result(
                    temp_dir, wait_time=5,
                    config='lazr.jobrunner.tests.time_limit_config_fast_lane',
                    queue='standard', sleep=3)
            job = js.get(job.job_id)
            job_output = js.get_output(job)
            self.assertEqual(
                'queue(manage_transaction=True, abort_transaction=True)\n',
                job_output)

        self.assertEqual(JobStatus.COMPLETED, job.status)

    def test_timeout_in_fast_lane_and_slow_lane(self):
        # If a fast and a slow lane are configured, jobs which time out
        # in the fast lane are queued again in the slow lane.
        with tempdir() as temp_dir:
            with celeryd(
                'lazr.jobrunner.tests.time_limit_config_slow_lane',
                temp_dir, queue='standard_slow'):
                # The fast lane times out after one second; the job
                # is then queued again in the slow lane, where it times
                # out again after five seconds. Wait seven seconds to
                # check the result.
                job, js, proc = self.run_file_job_ignore_result(
                    temp_dir, wait_time=7,
                    config='lazr.jobrunner.tests.time_limit_config_fast_lane',
                    queue='standard', sleep=7)
            job = js.get(job.job_id)
            job_output = js.get_output(job)
            self.assertEqual(
                'queue(manage_transaction=True, abort_transaction=True)\n',
                job_output)

        self.assertEqual(JobStatus.FAILED, job.status)
