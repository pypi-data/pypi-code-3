#  _________________________________________________________________________
#
#  Coopr: A COmmon Optimization Python Repository
#  Copyright (c) 2008 Sandia Corporation.
#  This software is distributed under the BSD License.
#  Under the terms of Contract DE-AC04-94AL85000 with Sandia Corporation,
#  the U.S. Government retains certain rights in this software.
#  For more information, see the Coopr README.txt file.
#  _________________________________________________________________________


import argparse
from coopr.opt.base import SolverFactory
from coopr.opt.parallel import SolverManagerFactory
from pyutilib.misc import Options, Container

try:
    from pympler import muppy
    from pympler.muppy import summary
    from pympler.muppy import tracker
    from pympler.asizeof import *
    pympler_available = True
except ImportError:
    pympler_available = False

import util


def add_model_group(parser):
    group = parser.add_argument_group('Model Options')

    group.add_argument('--preprocess', '--load',
        help='Specify a Python module that gets immediately executed (before '\
             'the optimization model is setup).  If this option is specified '\
             'multiple times, then the modules are executed in the specified '\
             'order.',
        action='append',
        dest='preprocess',
        default=[])
    group.add_argument('--model-name',
        help='The name of the model object that is created in the specified.' \
             'Pyomo module',
        action='store',
        dest='model_name',
        default='model')
    group.add_argument('--model-options',
        help='Options passed into a create_model() function to construct the '\
             'model.',
        action='append',
        dest='model_options',
        default=[])
    group.add_argument("--flatten-expressions", "--linearize-expressions",
        help="EXPERIMENTAL: An option intended for use on linear or mixed-integer models " \
             "in which expression trees in a model (constraints or objectives) are compacted " \
             "into a more memory-efficient and concise form. The expression trees themselves are eliminated. ",
        action="store_true",
        dest="linearize_expressions",
        default=False)
    group.add_argument("--skip-canonical-repn",
            help="Do not create the canonical representation. This is not necessary for solvers (e.g., ASL-based) that do not require it.",
            action="store_true",
            dest="skip_canonical_repn",
            default=False)
    group.add_argument('--save-model',
        help='Specify the filename to which the model is saved.  The suffix ' \
             'of this filename specifies the file format.  If debugging is '  \
             "on, then this defaults to writing the file 'unknown.lp'.",
        action='store',
        dest='save_model',
        default=None)
    group.add_argument('--ns', '--namespace',
        help='Specify a namespace that is used to select data in Pyomo data files.  If this is specified multiple '\
            'times then the union of the data in these namespaces is used to create the model instance.',
        action='append',
        dest='namespaces',
        default=[])
    return group


def add_logging_group(parser):
    group = parser.add_argument_group('Logging Options')

    group.add_argument('-q','--quiet',
        help='Disable all log messages except for those that refer to errors.',
        action='store_true',
        dest='quiet',
        default=False)
    group.add_argument('-w','--warning',
        help='Enable warning log messages for coopr and pyutilib.',
        action='store_true',
        dest='warning',
        default=False)
    group.add_argument('-i','--info',
        help='Enable informative log messages for coopr and pyutilib.',
        action='store_true',
        dest='info',
        default=False)
    group.add_argument('-v','--verbose',
        help="Indicate that debugging log messages should be printed.  This option can be specified multiple times to add log messages for other parts of coopr and pyutilib.",
        action='count',
        dest='verbose',
        default=0)
    group.add_argument('-d', '--debug',
        help='This option indicates that debugging is performed.  This implies the verbose flag, but it also allows exceptions to trigger a failure in which the program stack is printed.',
        action='store_true',
        dest='debug',
        default=False)
    #group.add_argument('--logfile',
        #help='Print log messages to the specified file.',
        #action='store',
        #dest='logfile',
        #default=None)
    return group


def add_solver_group(parser):
    solver_help=\
        "This option specifies the type of solver that is used "\
        "to optimize the Pyomo model instance.  Use the --help-solvers "\
        "option to get detailed information concerning how solvers are "\
        "executed."
#"This option can specify the name"\
#        "of an optimizer on the user's path, The following solver "\
#        "types are are currently supported:"
#    solver_list = SolverFactory.services()
#    solver_list = sorted( filter(lambda x: '_' != x[0], solver_list) )
#    solver_help += " %s." % ', '.join(solver_list)

    parser.add_argument('--help-solvers',
        help='Print information about the solvers can be used to solve Pyomo models.',
        action='store_true',
        dest='help_solvers',
        default=False)

    group = parser.add_argument_group('Solver Options')

    group.add_argument('--solver',
        help=solver_help,
        action='store',
        dest='solver',
        #choices=solver_list,
        default='glpk')
    group.add_argument('--solver-io',
        help='The type of IO used to execute the solver.  Different solvers support different types of IO, but the following are common options: lp - generate LP files, nl - generate NL files, python - direct Python interface, os - generate OSiL XML files.',
        action='store',
        dest='solver_io',
        #choices=['lp', 'nl', 'python', 'os'],
        default=None)
    group.add_argument('--solver-manager',
        help='Specify the technique that is used to manage solver executions.',
        action='store',
        dest='smanager_type',
        #type='choice',
        choices=SolverManagerFactory.services(),
        default='serial')
    group.add_argument('--solver-options',
        help='Options passed into the solver.',
        action='append',
        dest='solver_options',
        default=[])
    group.add_argument('--solver-suffixes',
        help='One or more solution suffixes to be extracted by the solver (e.g., rc, dual, or slack). Multiple options are specified by supplying the keyword options multiple times.',
        action='append',
        dest='solver_suffixes',
        default=[])
    group.add_argument('--timelimit',
        help='Limit to the number of seconds that the solver is run.',
        action='store',
        dest='timelimit',
        type=int,
        default=0)
    group.add_argument('--stream-solver',
        help='Stream the solver output to provide information about the '     \
             "solver's progress.",
        action='store_true',
        dest='tee',
        default=False)
    return group


def add_postsolve_group(parser):
    group = parser.add_argument_group('Post-Solve Options')

    group.add_argument('--postprocess',
        help='Specify a Python module that gets executed after optimization. ' \
             'If this option is specified multiple times, then the modules '  \
             'are executed in the specified order.',
        action='append',
        dest='postprocess',
        default=[])
    group.add_argument('-l','--log',
        help='Print the solver logfile after performing optimization.',
        action='store_true',
        dest='log',
        default=False)
    group.add_argument('--save-results',
        help='Specify the filename to which the results are saved.',
        action='store',
        dest='save_results',
        default=None)
    group.add_argument('--show-results',
        help='Print the results object after optimization.',
        action='store_true',
        dest='show_results',
        default=False)
    group.add_argument('--json',
        help='Print results in JSON format.  The default is YAML, if the PyYAML utility is available',
        action='store_true',
        dest='json',
        default=False)
    group.add_argument('-s','--summary',
        help='Summarize the final solution after performing optimization.',
        action='store_true',
        dest='summary',
        default=False)
    return group


def add_misc_group(parser):
    parser.add_argument('--help-components',
        help='Print information about modeling components supported by Pyomo',
        action='store_true',
        dest='help_components',
        default=False)

    group = parser.add_argument_group('Miscellaneous Options')

    group.add_argument('--output',
        help='Redirect output to the specified file.',
        action='store',
        dest='output',
        default=None)
    group.add_argument('-c', '--catch-errors',
        help='This option allows exceptions to trigger a failure in which the program stack is printed.',
        action='store_true',
        dest='catch',
        default=False)
    #group.add_argument('--logfile',
    group.add_argument('--disable-gc',
        help='Disable the garbage collecter.',
        action='store_true',
        dest='disable_gc',
        default=False)
    group.add_argument('--interactive',
        help='After executing Pyomo, launch an interactive Python shell.  If IPython is installed, this shell is an IPython shell.',
        action='store_true',
        dest='interactive',
        default=False)
    group.add_argument('-k','--keepfiles',
        help='Keep temporary files.',
        action='store_true',
        dest='keepfiles',
        default=False)
    group.add_argument('--path',
        help='Give a path that is used to find the Pyomo python files.',
        action='store',
        dest='path',
        default='.')
    group.add_argument('--profile',
        help='Enable profiling of Python code.  The value of this option is ' \
             'the number of functions that are summarized.',
        action='store',
        dest='profile',
        type=int,
        default=0)
    if pympler_available is True:
        group.add_argument("--profile-memory",
                             help="If Pympler is available, report memory usage statistics for the generated instance and any associated processing steps. A value of 0 indicates disabled. A value of 1 forces the print of the total memory after major stages of the pyomo script. A value of 2 forces summary memory statistics after major stages of the pyomo script. A value of 3 forces detailed memory statistics during instance creation and various steps of preprocessing. Values equal to 4 and higher currently provide no additional information. Higher values automatically enable all functionality associated with lower values, e.g., 3 turns on detailed and summary statistics.",
                             action="store",
                             dest="profile_memory",
                             type=int,
                             default=0)

    group.add_argument('--tempdir',
        help='Specify the directory where temporary files are generated.',
        action='store',
        dest='tempdir',
        default=None)
    return group


def create_parser():
    #
    #
    # Setup command-line options
    #
    #
    parser = argparse.ArgumentParser(
                usage = '%(prog)s [options] <model_file> [<data_files>]'
                )
    group = add_model_group(parser)
    group.add_argument('--instance-only',
        help='Generate a model instance, and then return.',
        action='store_true',
        dest='only_instance',
        default=False)
    add_solver_group(parser)
    add_postsolve_group(parser)
    add_logging_group(parser)
    add_misc_group(parser)
    parser.add_argument('model_file', action='store', nargs='?', default='', help='A Python module that defines a Pyomo model')
    parser.add_argument('data_files', action='store', nargs='*', default=[], help='Pyomo data files that defined data used to create a model instance')
    return parser


def run_pyomo(options=Options(), parser=None):
    data = Options(options=options)
    if options.help_solvers:
        util.print_solver_help(data)
        return Container()
    #
    if options.help_components:
        util.print_components(data)
        return Container()
    #
    util.setup_environment(data)
    #
    util.apply_preprocessing(data, parser=parser)
    if data.error:
        return Container()                                   #pragma:nocover
    #
    model_data = util.create_model(data)
    if (not options.debug and options.save_model) or options.only_instance:
        return Container(instance=model_data.instance)
    #
    opt_data = util.apply_optimizer(data, instance=model_data.instance)

    # this is hack-ish, and carries the following justification.
    # symbol maps are not pickle'able, and as a consequence, results
    # coming back from a pyro solver manager don't have a symbol map.
    # however, you need a symbol map to load the result into an 
    # instance. so, if it isn't there, construct it!
    if opt_data.results._symbol_map is None:
        from coopr.opt.base.symbol_map import symbol_map_from_instance
        results._symbol_map = symbol_map_from_instance(model_data.instance)

    #
    util.process_results(data, instance=model_data.instance, results=opt_data.results, opt=opt_data.opt)
    #return Container(instance=model_data.instance, results=results) #pragma:nocover
    #
    util.apply_postprocessing(data, instance=model_data.instance, results=opt_data.results)
    #
    util.finalize(data, model=model_data.model, instance=model_data.instance, results=opt_data.results)
    #
    return Container(options=options, instance=model_data.instance, results=opt_data.results)


def run(args=None):
    result = util.run_command(command=run_pyomo, parser=create_parser(), args=args, name='pyomo')
    return result.retval

def main(args=None):
    ans = run(args)
    if ans is None:
        return 0
    return 1

