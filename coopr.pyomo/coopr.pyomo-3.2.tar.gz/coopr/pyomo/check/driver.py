import argparse
import coopr.misc.coopr_parser
import os.path

class EnableDisableAction(argparse.Action):
    def add_package(self, namespace, package):
        if namespace.checkers.get(package, None) is None:
            namespace.checkers[package] = []
        for c in coopr.pyomo.check.ModelCheckRunner._checkers(all=True):
            if c._checkerPackage() == package:
                namespace.checkers[package].append(c._checkerName())

    def remove_package(self, namespace, package):
        if package in namespace.checkers:
            del namespace.checkers[package]

    def add_checker(self, namespace, checker):
        for c in coopr.pyomo.check.ModelCheckRunner._checkers(all=True):
            if c._checkerName() == checker:
                if namespace.checkers.get(c._checkerPackage(), None) is None:
                    namespace.checkers[c._checkerPackage()] = []
                if c._checkerName() not in namespace.checkers[c._checkerPackage()]:
                    namespace.checkers[c._checkerPackage()].append(c._checkerName())

    def remove_checker(self, namespace, checker):
        for c in coopr.pyomo.check.ModelCheckRunner._checkers(all=True):
            if c._checkerName() == checker:
                if namespace.checkers.get(c._checkerPackage(), None) is not None:
                    for i in range(namespace.checkers[c._checkerPackage()].count(c._checkerName())):
                        namespace.checkers[c._checkerPackage()].remove(c._checkerName())

    def add_default_checkers(self, namespace):
        self.add_package(namespace, 'pyomo')
        self.add_package(namespace, 'py3k')

    def __call__(self, parser, namespace, values, option_string=None):
        if 'checkers' not in dir(namespace):
            setattr(namespace, 'checkers', {})
            self.add_default_checkers(namespace)
        
        if option_string == '-c':
            self.add_checker(namespace, values)
        elif option_string == '-C':
            self.add_package(namespace, values)
        elif option_string == '-x':
            self.remove_checker(namespace, values)
        elif option_string == '-X':
            self.remove_package(namespace, values)

def setup_parser(parser):
    parser.add_argument("script", metavar="SCRIPT", default=None,
                        help="a Pyomo script that is checked")
    parser.add_argument("-v", "--verbose", action="store_true", dest="verbose",
                        default=False, help="enable additional output messages")
    parser.add_argument("-c", "--enable-checker", action=EnableDisableAction, 
                        help="activate a specific checker")
    parser.add_argument("-C", "--enable-package", action=EnableDisableAction,
                        help="activate an entire checker package")
    parser.add_argument("-x", "--disable-checker", action=EnableDisableAction,
                        help="disable a specific checker")
    parser.add_argument("-X", "--disable-package", action=EnableDisableAction,
                        help="disable an entire checker package")
    parser.add_argument("-s", "--show-checkers", action="store_true",
                        dest="show_checkers", help="show enabled checkers")


def main_exec(options):
    import coopr.pyomo.check as check

    if options.script is None:
        raise IOError, "Must specify a model script!"
    if not os.path.exists(options.script):
        raise IOError, "Model script '%s' does not exist!" % options.script

    # force default checkers
    if getattr(options, 'checkers', None) is None:
        EnableDisableAction(None, None)(None, options, None, None)

    runner = check.ModelCheckRunner()
    runner.run(**vars(options))

#
# Add a subparser for the check command
#
setup_parser(
    coopr.misc.coopr_parser.add_subparser('check',
        func=main_exec, 
        help='Check a model for errors.',
        description='This coopr subcommand is used to check a model script for errors.',
        epilog='The default behavior of this command is to assume that the model script is a simple Pyomo model.  Eventually, this script will support options that allow other Coopr models to be checked.'
        ))
