import runpy
import unittest
import simple_db_migrate
import os
from StringIO import StringIO
from mock import patch, call, Mock, MagicMock
from simple_db_migrate.config import Config

class RunTest(unittest.TestCase):

    def setUp(self):
        config_file = '''
HOST = os.getenv('DB_HOST') or 'localhost'
USERNAME = os.getenv('DB_USERNAME') or 'root'
PASSWORD = os.getenv('DB_PASSWORD') or ''
DATABASE = os.getenv('DB_DATABASE') or 'migration_example'
ENV1_DATABASE = 'migration_example_env1'
MIGRATIONS_DIR = os.getenv('MIGRATIONS_DIR') or 'example'
UTC_TIMESTAMP = os.getenv("UTC_TIMESTAMP") or True
DATABASE_ANY_CUSTOM_VARIABLE = 'Some Value'
SOME_ENV_DATABASE_ANY_CUSTOM_VARIABLE = 'Other Value'
DATABASE_OTHER_CUSTOM_VARIABLE = 'Value'
'''
        f = open('sample.conf', 'w')
        f.write(config_file)
        f.close()

    def tearDown(self):
        os.remove('sample.conf')

    def test_it_should_define_a_version_string(self):
        self.assertTrue(isinstance(simple_db_migrate.SIMPLE_DB_MIGRATE_VERSION, str))

    @patch.object(simple_db_migrate.cli.CLI, 'parse')
    def test_it_should_use_cli_to_parse_arguments(self, parse_mock):
        parse_mock.return_value = (Mock(simple_db_migrate_version=True), [])
        try:
            simple_db_migrate.run()
        except SystemExit, e:
            pass

        parse_mock.assert_called_with(None)

    @patch('sys.stdout', new_callable=StringIO)
    def test_it_should_print_simple_db_migrate_version_and_exit(self, stdout_mock):
        try:
            simple_db_migrate.run(["-v"])
        except SystemExit, e:
            self.assertEqual(0, e.code)

        self.assertEqual('simple-db-migrate v%s\n\n' % simple_db_migrate.SIMPLE_DB_MIGRATE_VERSION, stdout_mock.getvalue())

    @patch.object(simple_db_migrate.cli.CLI, 'show_colors')
    def test_it_should_activate_use_of_colors(self, show_colors_mock):
        try:
            simple_db_migrate.run(["--color"])
        except SystemExit, e:
            pass

        self.assertEqual(1, show_colors_mock.call_count)

    @patch.object(simple_db_migrate.cli.CLI, 'parse')
    @patch('sys.stdout', new_callable=StringIO)
    def test_it_should_print_message_and_exit_when_user_interrupt_execution(self, stdout_mock, parse_mock):
        parse_mock.side_effect = KeyboardInterrupt()
        try:
            simple_db_migrate.run(["-v"])
        except SystemExit, e:
            self.assertEqual(0, e.code)

        self.assertEqual('\nExecution interrupted by user...\n\n', stdout_mock.getvalue())

    @patch.object(simple_db_migrate.cli.CLI, 'parse')
    @patch('sys.stdout', new_callable=StringIO)
    def test_it_should_print_message_and_exit_when_user_an_error_happen(self, stdout_mock, parse_mock):
        parse_mock.side_effect = Exception('occur an error')
        try:
            simple_db_migrate.run(["-v"])
        except SystemExit, e:
            self.assertEqual(1, e.code)

        self.assertEqual('[ERROR] occur an error\n\n', stdout_mock.getvalue())

    @patch.object(simple_db_migrate.main.Main, 'execute')
    @patch.object(simple_db_migrate.main.Main, '__init__', return_value=None)
    @patch.object(simple_db_migrate.config.FileConfig, '_import_file', return_value = {'HOST':'host', 'USERNAME': 'root', 'PASSWORD':'', 'DATABASE':'database', 'MIGRATIONS_DIR':'.'})
    def test_it_should_read_configuration_file_using_fileconfig_class_and_execute_with_default_configuration(self, import_file_mock, main_mock, execute_mock):
        simple_db_migrate.run(["-c", os.path.abspath('sample.conf')])

        import_file_mock.assert_called_with(os.path.abspath('sample.conf'))

        self.assertEqual(1, execute_mock.call_count)
        execute_mock.assert_called_with()

        self.assertEqual(1, main_mock.call_count)
        config_used = main_mock.call_args[0][0]
        self.assertEqual('mysql', config_used.get('db_engine'))
        self.assertEqual('root', config_used.get('db_user'))
        self.assertEqual('', config_used.get('db_password'))
        self.assertEqual('database', config_used.get('db_name'))
        self.assertEqual('host', config_used.get('db_host'))
        self.assertEqual(False, config_used.get('utc_timestamp'))
        self.assertEqual('__db_version__', config_used.get('db_version_table'))
        self.assertEqual([os.path.abspath('.')], config_used.get('migrations_dir'))
        self.assertEqual(None, config_used.get('schema_version'))
        self.assertEqual(False, config_used.get('show_sql'))
        self.assertEqual(False, config_used.get('show_sql_only'))
        self.assertEqual(None, config_used.get('new_migration'))
        self.assertEqual(False, config_used.get('drop_db_first'))
        self.assertEqual(False, config_used.get('paused_mode'))
        self.assertEqual(None, config_used.get('log_dir'))
        self.assertEqual(None, config_used.get('label_version'))
        self.assertEqual(False, config_used.get('force_use_files_on_down'))
        self.assertEqual(False, config_used.get('force_execute_old_migrations_versions'))
        self.assertEqual(1, config_used.get('log_level'))

    @patch.object(simple_db_migrate.main.Main, 'execute')
    @patch.object(simple_db_migrate.main.Main, '__init__', return_value=None)
    @patch.object(simple_db_migrate.config.FileConfig, '_import_file', return_value = {'HOST':'host', 'USERNAME': 'root', 'PASSWORD':'', 'DATABASE':'database', 'MIGRATIONS_DIR':'.'})
    def test_it_should_use_log_level_as_specified(self, import_file_mock, main_mock, execute_mock):
        simple_db_migrate.run(["-c", os.path.abspath('sample.conf'), '--log-level', 4])
        config_used = main_mock.call_args[0][0]
        self.assertEqual(4, config_used.get('log_level'))

    @patch.object(simple_db_migrate.main.Main, 'execute')
    @patch.object(simple_db_migrate.main.Main, '__init__', return_value=None)
    @patch.object(simple_db_migrate.config.FileConfig, '_import_file', return_value = {'HOST':'host', 'USERNAME': 'root', 'PASSWORD':'', 'DATABASE':'database', 'MIGRATIONS_DIR':'.'})
    def test_it_should_use_log_level_as_2_when_in_paused_mode(self, import_file_mock, main_mock, execute_mock):
        simple_db_migrate.run(["-c", os.path.abspath('sample.conf'), '--pause'])
        config_used = main_mock.call_args[0][0]
        self.assertEqual(2, config_used.get('log_level'))

    @patch('sys.stdout', new_callable=StringIO)
    @patch.object(simple_db_migrate.main.Main, 'execute')
    @patch.object(simple_db_migrate.main.Main, '__init__', return_value=None)
    @patch.object(simple_db_migrate.config.FileConfig, '_import_file', return_value = {'HOST':'host', 'USERNAME': 'root', 'PASSWORD':'<<ask_me>>', 'DATABASE':'database', 'MIGRATIONS_DIR':'.'})
    def test_it_should_ask_for_password_when_configuration_is_as_ask_me(self, import_file_mock, main_mock, execute_mock, stdout_mock):
        getpass_mock = Mock(return_value = 'password_asked')
        simple_db_migrate.run(["-c", os.path.abspath('sample.conf')], getpass=getpass_mock)
        config_used = main_mock.call_args[0][0]
        self.assertEqual('password_asked', config_used.get('db_password'))
        self.assertEqual('\nPlease inform password to connect to database "root@host:database"\n', stdout_mock.getvalue())

    @patch.object(simple_db_migrate.main.Main, 'execute')
    @patch.object(simple_db_migrate.main.Main, '__init__', return_value=None)
    @patch.object(simple_db_migrate.config.FileConfig, '_import_file', return_value = {'HOST':'host', 'USERNAME': 'root', 'PASSWORD':'<<ask_me>>', 'DATABASE':'database', 'MIGRATIONS_DIR':'.'})
    def test_it_should_use_password_from_command_line_when_configuration_is_as_ask_me(self, import_file_mock, main_mock, execute_mock):
        simple_db_migrate.run(["-c", os.path.abspath('sample.conf'), '--password', 'xpto_pass'])
        config_used = main_mock.call_args[0][0]
        self.assertEqual('xpto_pass', config_used.get('db_password'))

    @patch.object(simple_db_migrate.main.Main, 'execute')
    @patch.object(simple_db_migrate.main.Main, '__init__', return_value=None)
    @patch.object(simple_db_migrate.config.FileConfig, '_import_file', return_value = {'force_execute_old_migrations_versions':True, 'label_version':'label', 'HOST':'host', 'USERNAME': 'root', 'PASSWORD':'', 'DATABASE':'database', 'MIGRATIONS_DIR':'.'})
    def test_it_should_use_values_from_config_file_in_replacement_for_command_line(self, import_file_mock, main_mock, execute_mock):
        simple_db_migrate.run(["-c", os.path.abspath('sample.conf')])
        config_used = main_mock.call_args[0][0]
        self.assertEqual('label', config_used.get('label_version'))
        self.assertEqual(True, config_used.get('force_execute_old_migrations_versions'))

if __name__ == '__main__':
    unittest.main()
