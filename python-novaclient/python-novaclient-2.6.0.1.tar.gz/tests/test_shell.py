
import os
import mock
import httplib2

from novaclient.shell import OpenStackComputeShell
from novaclient import exceptions
from tests import utils


class ShellTest(utils.TestCase):

    # Patch os.environ to avoid required auth info.
    def setUp(self):
        global _old_env
        fake_env = {
            'NOVA_USERNAME': 'username',
            'NOVA_API_KEY': 'password',
            'NOVA_PROJECT_ID': 'project_id',
        }
        _old_env, os.environ = os.environ, fake_env.copy()

        # Make a fake shell object, a helping wrapper to call it, and a quick way
        # of asserting that certain API calls were made.
        global shell, _shell, assert_called, assert_called_anytime
        _shell = OpenStackComputeShell()
        shell = lambda cmd: _shell.main(cmd.split())

    def tearDown(self):
        global _old_env
        os.environ = _old_env

    def test_help_unknown_command(self):
        self.assertRaises(exceptions.CommandError, shell, 'help foofoo')

    def test_debug(self):
        httplib2.debuglevel = 0
        shell('--debug help')
        assert httplib2.debuglevel == 1
