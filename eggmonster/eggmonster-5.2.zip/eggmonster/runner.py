import subprocess
import importlib
import argparse
import os

import yaml
try:
    import IPython.Shell
except ImportError:
    pass

import eggmonster.config
from eggmonster.packages import load_dependencies
from eggmonster import emenv
from eggmonster.control._common import getjson

INTERACT_BANNER = """
Eggmonster interactive prompt.

env: Eggmonster environment object.
monster_run(): Exits interactive mode and runs application.
startup(): Will import the module %(pkgname)s.etc.startup, if it exists.
"""

def main(config_path, app, update=False, interact=False, num=None,
        spawn_app=None, prog_args=[]):
    eggmonster._set_managed_env()
    if update:
        subprocess.Popen([
            'python', 'setup.py', 'develop',
            ] + emenv.get_easy_install_params())

    cfg = _load_config(config_path)

    # Pull the appropriate environment from the configuration.
    pkgname, __sep, entry_point = app.rpartition('.')
    try:
        entry_point, env, pkginfo, options = cfg.apps[app]
    except KeyError:
        # No configuration mentioned? OK, well we can still run the
        # application as long as it is a valid entry point (we'll
        # verify it further down.
        try:
            env, pkginfo = cfg.packages[pkgname]
        except KeyError:
            raise SystemExit('ERROR: No such package: "%s"' % pkgname)

    # We only need the original entry point for pulling out a configuration,
    # we can refer to the spawned application directly now.
    entry_point = spawn_app or entry_point

    if num is not None:
        from eggmonster.client import _em_emi
        env = _em_emi.fill_config_placeholders(env, num)
    eggmonster.update_locals(env)
    pkg = load_dependencies(pkginfo or pkgname)

    if entry_point is None:
        # caller supplied pkgname, but not appname. In this case, we just
        # initialize the env and return.
        return

    # Verify the entry point exists.
    if pkg.get_entry_info('eggmonster.applications', entry_point) is None:
        raise SystemExit('ERROR: No such application: "%s"' % app)

    run_app_func = True
    if interact:

        from eggmonster import env as the_env

        # Try to use iPython for the prompt if possible.
        runner = (start_ipython_shell if 'IPython' in globals() else
            start_python_shell)
        run_app_func = runner(the_env, pkgname)

        if run_app_func:
            print 'Exiting console, executing application.'

    # Load the entry point after interactive mode so that the user can
    # modify the environment dictionary before any module
    # imports grab values out of it.
    if run_app_func:
        app_func = pkg.load_entry_point('eggmonster.applications', entry_point)

        if can_take_app_args(app_func):
            app_func(entry_point, prog_args)
        elif prog_args:
            raise RuntimeError('the application "%s" does '
                'not take arguments (app needs "progname", '
                '"argv" signature)' % entry_point)
        else:
            app_func()

class FakeMonster(object):
    def __init__(self):
        self.start(*self.parse_args())

    @classmethod
    def run(cls):
        cls()

    def parse_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('app')
        parser.add_argument('--config-path', default='settings.yaml')
        parser.add_argument('--config-path-env', dest='config_path',
            type=self.resolve_env)
        args = parser.parse_args()
        return args.app, args.config_path

    def resolve_env(self, key):
        return os.environ[key]

    def start(self, app, config_path):
        """
        Simply run the app with a flat config loaded into eggmonster.env
        """
        eggmonster._set_managed_env()
        with open(config_path) as in_file:
            eggmonster.update_locals(yaml.load(in_file))
        package_name, _, app_name = app.partition('.')
        pkg = load_dependencies(package_name)
        app_func = pkg.load_entry_point('eggmonster.applications', app_name)
        args = (app_name, []) if can_take_app_args(app_func) else ()
        return app_func(*args)


def _load_config(config_path):
    """
    Given a config path, load the ClusterConfig from it.

    In addition to a file-system path, `config_path` may also take two special
    forms:

     - "REMOTE" means load the configuration from the eggmonster master
       (as defined in environment variables).
     - "ENVIRONMENT" means get the configuration path from the environment
       variable "EGGMONSTER_CONFIG_PATH". One may override the environment var
       name with "ENVIRONMENT:<var name>".
    """
    if config_path == 'REMOTE':
        # Grab the configuration settings from the Eggmonster master.
        return eggmonster.config.ClusterConfig.from_yaml(getjson('config')[1])

    if config_path.startswith('ENVIRONMENT'):
        key, sep, env_var = config_path.partition(':')
        if not env_var:
            env_var = 'EGGMONSTER_CONFIG_PATH'
        config_path = os.environ[env_var]
    return eggmonster.config.ClusterConfig.from_file(config_path)


def can_take_app_args(app_func):
    # Let's see if we pass args across or not.
    import inspect
    args, varargs, varkw, defaults = inspect.getargspec(app_func)

    # Basically - we only pass argv across, if:
    #   1) The function takes an argument called "progname" at position 0.
    #   2) The function takes an argument called "argv" at position 1.
    #   3) All other arguments (if any) are non-mandatory.
    #
    # progname and argv can have default arguments.
    default_len = len(defaults) if defaults else 0
    if args[:2] == ['progname', 'argv'] and (len(args) - default_len <= 2):
        return True
    else:
        return False

def start_ipython_shell(env, pkgname):
    monster_run_help = [False, None]

    def monster_run():
        # Terminate the shell and note we want to continue execution.
        monster_run_help[0] = True
        monster_run_help[1].IP.exit_now = True

    def startup():
        try:
            importlib.import_module(pkgname + '.etc.startup')
        except ImportError:
            print 'Unable to import startup module.'

    the_shell = IPython.Shell.IPShellEmbed(argv=[], user_ns={
            'monster_run': monster_run, 'env': env, 'startup': startup})
    monster_run_help[1] = the_shell

    the_shell(header=INTERACT_BANNER % vars())
    return monster_run_help[0]

def start_python_shell(env, pkgname):
    monster_run_help = [False]

    def exit_and_run_the_app():
        monster_run_help[0] = True
        raise SystemExit(0)

    def startup():
        try:
            importlib.import_module(pkgname + '.etc.startup')
        except ImportError:
            print 'Unable to import startup module.'

    the_locals = {
        "__name__": "__console__",
        "__doc__": None,
        "monster_run": exit_and_run_the_app,
        "env": env,
        "startup": startup,
    }

    import code
    try:
        code.interact(INTERACT_BANNER % vars(), local=the_locals)
    except SystemExit:
        pass

    return monster_run_help[0]
