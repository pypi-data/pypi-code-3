from __future__ import absolute_import
from __future__ import with_statement

import os

from celery.bin.base import Command
from celery.tests.utils import AppCase, override_stdouts


class Object(object):
    pass


class MyApp(object):
    pass

APP = MyApp()  # <-- Used by test_with_custom_app


class MockCommand(Command):
    mock_args = ("arg1", "arg2", "arg3")

    def parse_options(self, prog_name, arguments):
        options = Object()
        options.foo = "bar"
        options.prog_name = prog_name
        return options, self.mock_args

    def run(self, *args, **kwargs):
        return args, kwargs


class test_Command(AppCase):

    def test_get_options(self):
        cmd = Command()
        cmd.option_list = (1, 2, 3)
        self.assertTupleEqual(cmd.get_options(), (1, 2, 3))

    def test_run_interface(self):
        with self.assertRaises(NotImplementedError):
            Command().run()

    def test_execute_from_commandline(self):
        cmd = MockCommand()
        args1, kwargs1 = cmd.execute_from_commandline()     # sys.argv
        self.assertTupleEqual(args1, cmd.mock_args)
        self.assertDictContainsSubset({"foo": "bar"}, kwargs1)
        self.assertTrue(kwargs1.get("prog_name"))
        args2, kwargs2 = cmd.execute_from_commandline(["foo"])   # pass list
        self.assertTupleEqual(args2, cmd.mock_args)
        self.assertDictContainsSubset({"foo": "bar", "prog_name": "foo"},
                                      kwargs2)

    def test_with_bogus_args(self):
        cmd = MockCommand()
        cmd.supports_args = False
        with override_stdouts() as (_, stderr):
            with self.assertRaises(SystemExit):
                cmd.execute_from_commandline(argv=["--bogus"])
        self.assertTrue(stderr.getvalue())
        self.assertIn("Unrecognized", stderr.getvalue())

    def test_with_custom_config_module(self):
        prev = os.environ.pop("CELERY_CONFIG_MODULE", None)
        try:
            cmd = MockCommand()
            cmd.setup_app_from_commandline(["--config=foo.bar.baz"])
            self.assertEqual(os.environ.get("CELERY_CONFIG_MODULE"),
                             "foo.bar.baz")
        finally:
            if prev:
                os.environ["CELERY_CONFIG_MODULE"] = prev

    def test_with_custom_app(self):
        cmd = MockCommand()
        app = ".".join([__name__, "APP"])
        cmd.setup_app_from_commandline(["--app=%s" % (app, ),
                                        "--loglevel=INFO"])
        self.assertIs(cmd.app, APP)

    def test_with_cmdline_config(self):
        cmd = MockCommand()
        cmd.enable_config_from_cmdline = True
        cmd.namespace = "celeryd"
        rest = cmd.setup_app_from_commandline(argv=[
            "--loglevel=INFO", "--", "broker.host=broker.example.com",
            ".prefetch_multiplier=100"])
        self.assertEqual(cmd.app.conf.BROKER_HOST, "broker.example.com")
        self.assertEqual(cmd.app.conf.CELERYD_PREFETCH_MULTIPLIER, 100)
        self.assertListEqual(rest, ["--loglevel=INFO"])
