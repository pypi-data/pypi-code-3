#  _________________________________________________________________________
#
#  Coopr: A COmmon Optimization Python Repository
#  Copyright (c) 2008 Sandia Corporation.
#  This software is distributed under the BSD License.
#  Under the terms of Contract DE-AC04-94AL85000 with Sandia Corporation,
#  the U.S. Government retains certain rights in this software.
#  For more information, see the Coopr README.txt file.
#  _________________________________________________________________________

import gc
import logging
import os
import sys
import textwrap
import traceback
import types
import time
from coopr.core import coopr_api

try:
    import yaml
    yaml_available=True
except ImportError:
    yaml_available=False
try:
    import cProfile as profile
except ImportError:
    import profile
try:
    import pstats
    pstats_available=True
except ImportError:
    pstats_available=False

try:
    import IPython
    IPython_available=True
    from IPython.Shell import IPShellEmbed
except:
    IPython_available=False
else:
    ipshell = IPShellEmbed([''],
                banner = '\n# Dropping into Python interpreter',
                exit_msg = '\n# Leaving Interpreter, back to Pyomo\n')

from pyutilib.misc import Options
try:
    from pympler import muppy
    from pympler.muppy import summary
    from pympler.muppy import tracker
    from pympler.asizeof import *
    pympler_available = True
except ImportError:
    pympler_available = False
memory_tracker = None
memory_data = Options()

from coopr.pyomo import *
from coopr.opt import ProblemFormat
from coopr.opt.base import SolverFactory
from coopr.opt.parallel import SolverManagerFactory
import pyutilib.misc
from pyutilib.component.core import ExtensionPoint, Plugin, implements
from pyutilib.services import TempfileManager

from coopr.pyomo.expr.linear_repn import linearize_model_expressions

filter_excepthook=False
modelapi = {    'pyomo_create_model':IPyomoScriptCreateModel,
                'pyomo_create_modeldata':IPyomoScriptCreateModelData,
                'pyomo_print_model':IPyomoScriptPrintModel,
                'pyomo_modify_instance':IPyomoScriptModifyInstance,
                'pyomo_print_instance':IPyomoScriptPrintInstance,
                'pyomo_save_instance':IPyomoScriptSaveInstance,
                'pyomo_print_results':IPyomoScriptPrintResults,
                'pyomo_save_results':IPyomoScriptSaveResults,
                'pyomo_postprocess':IPyomoScriptPostprocess}


logger = logging.getLogger('coopr.pyomo')
start_time = 0.0


@coopr_api(namespace='pyomo.script')
def print_components(data):
    """
    Print information about modeling components supported by Pyomo.
    """
    print ""
    print "----------------------------------------------------------------"
    print "Pyomo Model Components:"
    print "----------------------------------------------------------------"
    components = pyomo.model_components()
    index = pyutilib.misc.sort_index(components)
    for i in index:
        print ""
        print " "+components[i][0]
        for line in textwrap.wrap(components[i][1], 59):
            print "    "+line
    print ""
    print "----------------------------------------------------------------"
    print "Pyomo Virtual Sets:"
    print "----------------------------------------------------------------"
    pyomo_sets = pyomo.predefined_sets()
    index = pyutilib.misc.sort_index(pyomo_sets)
    for i in index:
        print ""
        print " "+pyomo_sets[i][0]
        print "    "+pyomo_sets[i][1]

@coopr_api(namespace='pyomo.script')
def print_solver_help(data):
    """
    Print information about the solvers that are available.
    """
    wrapper = textwrap.TextWrapper(replace_whitespace=False)
    print wrapper.fill("The --solver option can specify two classes of solvers:  the names of command-line executables that are on the user's path, and predefined solver interfaces.  Command-line executables are assumed to support the 'nl' solver I/O type.  Thus, Pyomo models can be optimized with any solver that employs the AMPL solver library.  The following solver interfaces are recognized by Pyomo:")
    print ""
    solver_list = SolverFactory.services()
    solver_list = sorted( filter(lambda x: '_' != x[0], solver_list) )
    n = max(map(len, solver_list))
    wrapper = textwrap.TextWrapper(subsequent_indent=' '*(n+9))
    for s in solver_list:
        format = '    %-'+str(n)+'s  %s'
        print wrapper.fill(format % (s , SolverFactory.doc(s)))
    print ""
    wrapper = textwrap.TextWrapper(subsequent_indent='')
    print wrapper.fill('These solver interfaces generally support multiple solver I/O types.  The default solver is glpk.')
    print ""
    print wrapper.fill('Subsolver options can be specified by with the solver name followed by colon and then the subsolver.  For example, the following specifies that the asl solver will be used:')
    print '   --asl:PICO'
    print wrapper.fill('This indicates that the asl solver will launch the PICO executable to perform optimization. Currently, no other solver supports this syntax.')


@coopr_api(namespace='pyomo.script')
def setup_environment(data):
    """
    Setup Pyomo execution environment
    """
    #
    if data.options.json or not yaml_available:
        data.options.results_format='json'
    else:
        data.options.results_format='yaml'
    #
    global start_time
    start_time = time.time()
    if not data.options.quiet:
        sys.stdout.write('[%8.2f] Setting up Pyomo environment\n' % 0.0)
        sys.stdout.flush()
    #
    # Setup memory tracker
    #
    if (pympler_available is True) and (data.options.profile_memory >= 1):
        global memory_tracker
        memory_tracker = tracker.SummaryTracker()
    #
    # Disable garbage collection
    #
    if data.options.disable_gc:
        gc.disable()
    #
    # Setup management for temporary files
    #
    if not data.options.tempdir is None:
        if not os.path.exists(data.options.tempdir):
            msg =  'Directory for temporary files does not exist: %s'
            raise ValueError, msg % data.options.tempdir
        TempfileManager.tempdir = data.options.tempdir

    #
    # Configure exception management
    #
    def pyomo_excepthook(etype,value,tb):
        """
        This exception hook gets called when debugging is on. Otherwise,
        run_command in this module is called.
        """
        global filter_excepthook
        if len(data.options.model_file) > 0:
            name = "model " + data.options.model_file
        else:
            name = "model"


        if filter_excepthook:
            action = "loading"
        else:
            action = "running"

        msg = "Unexpected exception while %s %s\n" % (action, name)

        #
        # This handles the case where the error is propagated by a KeyError.
        # KeyError likes to pass raw strings that don't handle newlines
        # (they translate "\n" to "\\n"), as well as tacking on single
        # quotes at either end of the error message. This undoes all that.
        #
        if etype == KeyError:
            valueStr = str(value).replace("\\n","\n")[1:-1]
        else:
            valueStr = str(value)

        logger.error(msg+valueStr)

        tb_list = traceback.extract_tb(tb,None)
        i = 0
        if not logger.isEnabledFor(logging.DEBUG) and filter_excepthook:
            while i < len(tb_list):
                #print "Y",model,tb_list[i][0]
                if data.options.model_file in tb_list[i][0]:
                    break
                i += 1
            if i == len(tb_list):
                i = 0
        print "\nTraceback (most recent call last):"
        for item in tb_list[i:]:
            print "  File \""+item[0]+"\", line "+str(item[1])+", in "+item[2]
            if item[3] is not None:
                print "    "+item[3]
        sys.exit(1)
    sys.excepthook = pyomo_excepthook


@coopr_api(namespace='pyomo.script')
def apply_preprocessing(data, parser=None):
    """
    Execute preprocessing files

    Required:
        parser: Command line parser object

    Returned:
        error: This is true if an error has occurred.
    """
    #
    if not data.options.quiet:
        sys.stdout.write('[%8.2f] Applying Pyomo preprocessing actions\n' % (time.time()-start_time))
        sys.stdout.flush()
    #
    global filter_excepthook
    #
    #
    # Setup solver and model
    #
    #
    if len(data.options.model_file) == 0:
        parser.print_help()
        data.error = True
        return data
    #
    if not data.options.preprocess is None:
        for file in data.options.preprocess:
            preprocess = pyutilib.misc.import_file(file)
    #
    for ep in ExtensionPoint(IPyomoScriptPreprocess):
        ep.apply( options=data.options )
    #
    # Verify that files exist
    #
    for file in [data.options.model_file]+data.options.data_files:
        if not os.path.exists(file):
            raise IOError, "File "+file+" does not exist!"
    #
    filter_excepthook=True
    data.options.usermodel = pyutilib.misc.import_file(data.options.model_file)
    filter_excepthook=False

    usermodel_dir = dir(data.options.usermodel)
    data.options._usermodel_plugins = []
    for key in modelapi:
        if key in usermodel_dir:
            class TMP(Plugin):
                implements(modelapi[key])
                def __init__(self):
                    self.fn = getattr(data.options.usermodel, key)
                def apply(self,**kwds):
                    return self.fn(**kwds)
            data.options._usermodel_plugins.append( TMP() )

    if 'pyomo_preprocess' in usermodel_dir:
        if data.options.model_name in usermodel_dir:
            msg = "Preprocessing function 'pyomo_preprocess' defined in file" \
                  " '%s', but model is already constructed!"
            raise SystemExit, msg % data.options.model_file
        getattr(data.options.usermodel, 'pyomo_preprocess')( options=data.options )
    #
    return data

@coopr_api(namespace='pyomo.script')
def create_model(data):
    """
    Create instance of Pyomo model.
    
    Return:
        model:      Model object.
        instance:   Problem instance.
        symbol_map: Symbol map created when writing model to a file.
        filename:    Filename that a model instance was written to.
    """
    #
    if not data.options.quiet:
        sys.stdout.write('[%8.2f] Creating model\n' % (time.time()-start_time))
        sys.stdout.flush()
    #
    if (pympler_available is True) and (data.options.profile_memory >= 1):
        global memory_data
        objects_before_instance_creation = muppy.get_objects()
        memory_data.summary_before_instance_creation = summary.summarize(objects_before_instance_creation)
        print "Initial set of objects"
        mem_used = muppy.get_size(objects_before_instance_creation)
        data.options.max_memory = mem_used
        print "   Total memory used: ",mem_used
        if data.options.profile_memory > 1:
            summary.print_(memory_data.summary_before_instance_creation,limit=50)
    #
    # Create Model
    #
    ep = ExtensionPoint(IPyomoScriptCreateModel)
    model_name = 'model'
    if data.options.model_name is not None: model_name = data.options.model_name

    if model_name in dir(data.options.usermodel):
        if len(ep) > 0:
            msg = "Model construction function 'create_model' defined in "    \
                  "file '%s', but model is already constructed!"
            raise SystemExit, msg % data.options.model_file
        model = getattr(data.options.usermodel, model_name)

        if model is None:
            msg = "'%s' object is 'None' in module %s"
            raise SystemExit, msg % (model_name, data.options.model_file)
            sys.exit(0)

    else:
        if len(ep) == 0:
            msg = "Neither '%s' nor 'pyomo_create_model' are available in "    \
                  'module %s'
            raise SystemExit, msg % ( model_name, data.options.model_file )
        elif len(ep) > 1:
            msg = 'Multiple model construction plugins have been registered!'
            raise SystemExit, msg
        else:
            model_options = data.options.model_options
            if model_options is None:
                model_options = []
            model = ep.service().apply( options=pyutilib.misc.Container(*model_options) )
    #
    for ep in ExtensionPoint(IPyomoScriptPrintModel):
        ep.apply( options=data.options, model=model )

    #
    # Disable canonical repn for ASL solvers, and if the user has specified as such (in which case, we assume they know what they are doing!).
    #
    # Likely we need to change the framework so that canonical repn
    # is not assumed to be required by all solvers?
    #
    if not data.options.solver is None and data.options.solver.startswith('asl'):
        model.skip_canonical_repn = True
    elif data.options.skip_canonical_repn is True:
        model.skip_canonical_repn = True

    #
    # Create Problem Instance
    #
    ep = ExtensionPoint(IPyomoScriptCreateModelData)
    if len(ep) > 1:
        msg = 'Multiple model data construction plugins have been registered!'
        raise SystemExit, msg

    if len(ep) == 1:
        modeldata = ep.service().apply( options=data.options, model=model )
    else:
        modeldata = ModelData()

    if len(data.options.data_files) > 1:
        #
        # Load a list of *.dat files
        #
        for file in data.options.data_files:
            suffix = (file).split(".")[-1]
            if suffix != "dat":
                msg = 'When specifiying multiple data files, they must all '  \
                      'be *.dat files.  File specified: %s'
                raise SystemExit, msg % str( file )

            modeldata.add(file)

        modeldata.read(model)

        if not data.options.profile_memory is None:
            instance = model.create(modeldata, namespaces=data.options.namespaces, profile_memory=data.options.profile_memory-1)
        else:
            instance = model.create(modeldata, namespaces=data.options.namespaces)

    elif len(data.options.data_files) == 1:
        #
        # Load a *.dat file or process a *.py data file
        #
        suffix = (data.options.data_files[0]).split(".")[-1]
        if suffix == "dat":
            if not data.options.profile_memory is None:
                instance = model.create(data.options.data_files[0], namespaces=data.options.namespaces, profile_memory=data.options.profile_memory-1)
            else:
                instance = model.create(data.options.data_files[0], namespaces=data.options.namespaces)
        elif suffix == "py":
            userdata = pyutilib.misc.import_file(data.options.data_files[0])
            if "modeldata" in dir(userdata):
                if len(ep) == 1:
                    msg = "Cannot apply 'pyomo_create_modeldata' and use the" \
                          " 'modeldata' object that is provided in the model"
                    raise SystemExit, msg

                if userdata.modeldata is None:
                    msg = "'modeldata' object is 'None' in module %s"
                    raise SystemExit, msg % str( data.options.data_files[0] )

                modeldata=userdata.modeldata

            else:
                if len(ep) == 0:
                    msg = "Neither 'modeldata' nor 'pyomo_create_model_data"  \
                          'is defined in module %s'
                    raise SystemExit, msg % str( data.options.data_files[0] )

            modeldata.read(model)
            if not data.options.profile_memory is None:
                instance = model.create(modeldata, namespaces=data.options.namespaces, profile_memory=data.options.profile_memory-1)
            else:
                instance = model.create(modeldata, namespaces=data.options.namespaces)
        else:
            raise ValueError, "Unknown data file type: "+data.options.data_files[0]
    else:
        if not data.options.profile_memory is None:
            instance = model.create(modeldata, namespaces=data.options.namespaces, profile_memory=data.options.profile_memory-1)
        else:
            instance = model.create(modeldata, namespaces=data.options.namespaces)

    if data.options.linearize_expressions is True:
        linearize_model_expressions(instance)

    #
    ep = ExtensionPoint(IPyomoScriptModifyInstance)
    for ep in ExtensionPoint(IPyomoScriptModifyInstance):
        ep.apply( options=data.options, model=model, instance=instance )
    #
    if logger.isEnabledFor(logging.DEBUG):
        print "MODEL INSTANCE"
        instance.pprint()
        print ""

    for ep in ExtensionPoint(IPyomoScriptPrintInstance):
        ep.apply( options=data.options, instance=instance )

    fname=None
    symbol_map=None
    #if options.save_model is None and options.debug:
        #options.save_model = 'unknown.lp'
    if not data.options.save_model is None:
        if data.options.save_model == True:
            if data.options.format in (ProblemFormat.cpxlp, ProblemFormat.lpxlp):
                fname = (data.options.data_files[0])[:-3]+'lp'
            else:
                fname = (data.options.data_files[0])[:-3]+str(data.options.format)
            format=data.options.format
        else:
            fname = data.options.save_model
            format=None
        (fname, symbol_map) = instance.write(filename=fname, format=format)
        if not data.options.quiet:
            if not os.path.exists(fname):
                print "ERROR: file "+fname+" has not been created!"
            else:
                print "Model written to file '"+str(fname)+"'"
    for ep in ExtensionPoint(IPyomoScriptSaveInstance):
        ep.apply( options=data.options, instance=instance )

    if (pympler_available is True) and (data.options.profile_memory >= 1):
        objects_after_instance_creation = muppy.get_objects()
        memory_data.summary_after_instance_creation = summary.summarize(objects_after_instance_creation)
        print "\nObjects created during Pyomo instance creation"
        mem_used = muppy.get_size(objects_after_instance_creation)
        if mem_used > data.options.max_memory:
            data.options.max_memory = mem_used
        print "   Total memory used: ",mem_used
        if data.options.profile_memory > 1:
            memory_tracker.print_diff(
                    summary1=memory_data.summary_before_instance_creation,
                    summary2=memory_data.summary_after_instance_creation)

    return pyutilib.misc.Options(
                    model=model, instance=instance,
                    symbol_map=symbol_map, filename=fname )

@coopr_api(namespace='pyomo.script')
def apply_optimizer(data, instance=None):
    """
    Perform optimization with a concrete instance

    Required:
        instance:   Problem instance.

    Returned:
        results:    Optimization results. 
        opt:        Optimizer object.
    """
    #
    if not data.options.quiet:
        sys.stdout.write('[%8.2f] Applying solver\n' % (time.time()-start_time))
        sys.stdout.flush()
    #
    #
    # Create Solver and Perform Optimization
    #
    solver = data.options.solver
    if solver is None:
        raise ValueError, "Problem constructing solver:  no solver specified"

    opt = SolverFactory( solver, solver_io=data.options.solver_io )
    if opt is None:
        raise ValueError, "Problem constructing solver `%s`" % str(solver)

    opt.keepFiles=data.options.keepfiles or data.options.log
    if data.options.timelimit == 0:
        data.options.timelimit=None

    if not data.options.solver_suffixes is None:
        if 'all' in data.options.solver_suffixes:
            opt.suffixes = ['.*']
        else:
            opt.suffixes = []
            for suffix in data.options.solver_suffixes:
                if suffix[0] in ['"', "'"]:
                    opt.suffixes.append(suffix[1:-1])
                else:
                    opt.suffixes.append(suffix)

    if not data.options.solver_options is None:
        opt.set_options(" ".join(data.options.solver_options))

    if data.options.smanager_type is None:
        solver_mngr = SolverManagerFactory( 'serial' )
    else:
        solver_mngr = SolverManagerFactory( data.options.smanager_type )

    if solver_mngr is None:
        msg = "Problem constructing solver manager '%s'"
        raise ValueError, msg % str( data.options.smanager_type )

    results = solver_mngr.solve( instance, opt=opt, tee=data.options.tee, timelimit=data.options.timelimit )

    if results == None:
        raise ValueError, "opt.solve returned None"

    if (pympler_available is True) and (data.options.profile_memory >= 1):
        global memory_data
        objects_after_optimization = muppy.get_objects()
        memory_data.summary_after_optimization = summary.summarize(objects_after_optimization)
        print "\nObjects created during optimization"
        mem_used = muppy.get_size(objects_after_optimization)
        if mem_used > data.options.max_memory:
            data.options.max_memory = mem_used
        print "   Total memory used: ",mem_used
        if data.options.profile_memory > 1:
            memory_tracker.print_diff(
                    summary1=memory_data.summary_after_instance_creation,
                    summary2=memory_data.summary_after_optimization)

    return pyutilib.misc.Options(results=results, opt=opt)


@coopr_api(namespace='pyomo.script')
def process_results(data, instance=None, results=None, opt=None):
    """
    Process optimization results.

    Required:
        instance:   Problem instance.
        results:    Optimization results object.
        opt:        Optimizer object.
    """
    #
    if not data.options.quiet:
        sys.stdout.write('[%8.2f] Processing results\n' % (time.time()-start_time))
        sys.stdout.flush()
    #
    if data.options.log:
        print ""
        print "=========================================================="
        print "Solver Logfile:",opt.log_file
        print "=========================================================="
        print ""
        INPUT = open(opt.log_file, "r")
        for line in INPUT:
            print line,
        INPUT.close()
    #
    # JDS: FIXME: This is a HACK for the ASL.  The SOL file does not
    # actually contain the objective values, so we must calculate them
    # ourselves.  Ideally, this should be done as part of the ASL solver
    # (i.e., part of reading in a SOL file), however, given the current
    # workflow structure, the necessary information is not present
    # (i.e., results reading is supposed to be independent of the
    # instance and the symbol_map).  This should be revisited as part of
    # any workflow overhaul.
    if instance is not None and results is not None and \
           results._symbol_map is not None:
        # We need the symbol map in order to translate the strings
        # coming back in the results object to the actual varvalues in
        # the instance
        _symbolMap = results._symbol_map

        # This is a lot of work to get the flattened list of objectives
        # (especially since all the solvers are single-objective)...
        # But this is safe for multi-objective use (both multiple
        # objectives and indexed objectives)
        _objectives = []
        for obj in instance.components.components(Objective).itervalues():
            _objectives.extend(obj.values())
        _nObj = len(_objectives)

        labeler = None
        for _result in xrange(len(results.solution)):
            _soln = results.solution[_result] 
            # Nothing to do if the objectives are already present
            if len(_soln.objective) == _nObj:
                continue

            if labeler is None:
                from coopr.pyomo.io.cpxlp import CPXLP_text_labeler
                labeler = CPXLP_text_labeler()

            # Save the original instance values... that way the original
            # instance does not change "unexpectedly"
            _orig_val_map = {}

            # We need to map the symbols returned by the solver results
            # to their "official" symbols.  This is because the ASL
            # actually returns *aliases* as the names in the results
            # object <sigh>.
            _results_name_map = {}
            for var in _soln.variable.iterkeys():
                # dangerous: this assumes that all results from the solver
                # actually went through the symbol map
                _name = _symbolMap.getSymbol(_symbolMap.getObject(var), None)
                _results_name_map[_name] = var

            # Pull the variables out of the objective, override them
            # with the results from the solver, and evaluate each
            # objective
            for obj in _objectives:
                for var in coopr.pyomo.base.expr.identify_variables \
                        ( obj.expr, False ):
                    # dangerous: this assumes that all variables
                    # actually went through the symbol map
                    s = results._symbol_map.getSymbol(var, None)
                    if s not in _orig_val_map:
                        _orig_val_map.setdefault(s, (var, var.value))
                        if s in _results_name_map:
                            var.value = _soln.variable[_results_name_map[s]]['Value']
                        else:
                            var.value = 0.0
                _soln.objective[ _symbolMap.getSymbol(obj, labeler)
                                 ].value = value(obj.expr)
            # Finally, put the variables back to their original values
            for var, val in _orig_val_map.itervalues():
                var.value = val
    #
    try:
        # transform the results object into human-readable names.
        # IMPT: the resulting object won't be loadable - it's only for output.
        transformed_results = instance.update_results(results)
    except Exception, e:
        print "Problem updating solver results"
        raise
    #
    if not data.options.show_results:
        if data.options.save_results:
            results_file = data.options.save_results
        elif data.options.results_format == 'yaml':
            results_file = 'results.yml'
        else:
            results_file = 'results.json'
        transformed_results.write(filename=results_file, format=data.options.results_format)
        if not data.options.quiet:
            print "    Number of solutions:", len(transformed_results.solution)
            if len(transformed_results.solution) > 0:
                print "    Solution Information"
                print "      Gap:",transformed_results.solution[0].gap
                print "      Status:",transformed_results.solution[0].status
                if len(transformed_results.solution[0].objective) == 1:
                    key = transformed_results.solution[0].objective.keys()[0]
                    print "      Function Value:",transformed_results.solution[0].objective[key].value
            print "    Solver results file:",results_file
    #
    ep = ExtensionPoint(IPyomoScriptPrintResults)
    if len(ep) == 0:
        try:
            instance.load(results)
        except Exception, e:
            print "Problem loading solver results"
            raise
    if data.options.show_results:
        print ""
        results.write(num=1, format=data.options.results_format)
        print ""
    #
    if data.options.summary:
        print ""
        print "=========================================================="
        print "Solution Summary"
        print "=========================================================="
        if len(results.solution(0).variable) > 0:
            print ""
            display(instance)
            print ""
        else:
            print "No solutions reported by solver."
    #
    for ep in ExtensionPoint(IPyomoScriptPrintResults):
        ep.apply( options=data.options, instance=instance, results=results )
    #
    for ep in ExtensionPoint(IPyomoScriptSaveResults):
        ep.apply( options=data.options, instance=instance, results=results )
    #
    if (pympler_available is True) and (data.options.profile_memory >= 1):
        global memory_data
        objects_after_results_processing = muppy.get_objects()
        memory_data.summary_after_results_processing = summary.summarize(objects_after_results_processing)
        #diff_summary = summary.get_diff( memory_data.summary_after_optimization, memory_data.summary_after_results_processing)
        print "\nObjects created during results processing"
        mem_used = muppy.get_size(objects_after_results_processing)
        if mem_used > data.options.max_memory:
            data.options.max_memory = mem_used
        print "   Total memory used: ",mem_used
        if data.options.profile_memory > 1:
            memory_tracker.print_diff(
                    summary1=memory_data.summary_after_optimization,
                    summary2=memory_data.summary_after_results_processing)


@coopr_api(namespace='pyomo.script')
def apply_postprocessing(data, instance=None, results=None):
    """
    Apply post-processing steps.

    Required:
        instance:   Problem instance.
        results:    Optimization results object.
    """
    #
    if not data.options.quiet:
        sys.stdout.write('[%8.2f] Applying Pyomo postprocessing actions\n' % (time.time()-start_time))
        sys.stdout.flush()
    #
    for file in data.options.postprocess:
        postprocess = pyutilib.misc.import_file(file)
        if "pyomo_postprocess" in dir(postprocess):
            postprocess.pyomo_postprocess(data.options, instance,results)
    for ep in ExtensionPoint(IPyomoScriptPostprocess):
        ep.apply( options=data.options, instance=instance, results=results )
    #
    # Deactivate and delete plugins
    #
    for plugin in data.options._usermodel_plugins:
        plugin.deactivate()
    data.options._usermodel_plugins = []
    #
    if (pympler_available is True) and (data.options.profile_memory >= 1):
        final_objects = muppy.get_objects()
        summary_final = summary.summarize(final_objects)
        final_summary = summary.summarize(final_objects)
        print "\nFinal set of objects"
        mem_used = muppy.get_size(final_objects)
        if mem_used > data.options.max_memory:
            data.options.max_memory = mem_used
        print "   Total memory used: ",mem_used
        if data.options.profile_memory > 1:
            summary.print_(final_summary, limit=50)


@coopr_api(namespace='pyomo.script')
def finalize(data, model=None, instance=None, results=None):
    """
    Perform final actions to finish the execution of the pyomo script.

    This function prints statistics related to the execution of the pyomo script.
    Additionally, this function will drop into the python interpreter if the `interactive` 
    option is `True`.

    Required:
        model:      A pyomo model object.

    Optional:
        instance:   A problem instance derived from the model object.
        results:    Optimization results object.
    """
    #
    if not data.options.quiet:
        sys.stdout.write('[%8.2f] Pyomo Finished\n' % (time.time()-start_time))
        if (pympler_available is True) and (data.options.profile_memory >= 1):
            sys.stdout.write('Maximum Memory Used: %d\n' % data.options.max_memory)
        sys.stdout.flush()
    #
    model=model
    instance=instance
    results=results
    #
    if data.options.interactive:
        if IPython_available:
            ipshell()
        else:
            import code
            shell = code.InteractiveConsole(locals())
            print '\n# Dropping into Python interpreter'
            shell.interact()
            print '\n# Leaving Interpreter, back to Pyomo\n'


@coopr_api(namespace='pyomo.script')
def run_command(command=None, parser=None, args=None, name='unknown', data=None):
    """
    Execute a function that processes command-line arguments and
    then calls a command-line driver.

    This function provides a generic facility for executing a command
    function is rather generic.  This function is segregated from
    the driver to enable profiling of the command-line execution.

    Required:
        command:    The name of a function that will be executed to perform process the command-line
                    options with a parser object.
        parser:     The parser object that is used by the command-line function.

    Optional:
        args:       Command-line arguments that are parsed.  If this value is `None`, then the
                    arguments in `sys.argv` are used to parse the command-line.
        name:       Specifying the name of the command-line (for error messages).
        data:       A container of labeled data.

    Returned:
        retval:     Return values from the command-line execution.
    """
    #
    #
    # Parse command-line options
    #
    #
    try:
        _options = parser.parse_args(args=args)
        # Replace the parser options object with a pyutilib.misc.Options object
        options = pyutilib.misc.Options()
        for key in dir(_options):
            if key[0] != '_':
                val = getattr(_options, key)
                if not isinstance(val, types.MethodType):
                    options[key] = val
    except SystemExit:
        # the parser throws a system exit if "-h" is specified - catch
        # it to exit gracefully.
        return pyutilib.misc.Options(retval=None)
    #
    # Configure the logger
    #
    logging.getLogger('coopr.pyomo').setLevel(logging.ERROR)
    logging.getLogger('coopr').setLevel(logging.ERROR)
    logging.getLogger('pyutilib').setLevel(logging.ERROR)
    #
    if options.warning:
        logging.getLogger('coopr.pyomo').setLevel(logging.WARNING)
        logging.getLogger('coopr').setLevel(logging.WARNING)
        logging.getLogger('pyutilib').setLevel(logging.WARNING)
    if options.info:
        logging.getLogger('coopr.pyomo').setLevel(logging.INFO)
        logging.getLogger('coopr').setLevel(logging.INFO)
        logging.getLogger('pyutilib').setLevel(logging.INFO)
    if options.verbose > 0:
        if options.verbose >= 1:
            logger.setLevel(logging.DEBUG)
        if options.verbose >= 2:
            logging.getLogger('coopr').setLevel(logging.DEBUG)
        if options.verbose >= 3:
            logging.getLogger('pyutilib').setLevel(logging.DEBUG)
    if options.debug:
        logging.getLogger('coopr.pyomo').setLevel(logging.DEBUG)
        logging.getLogger('coopr').setLevel(logging.DEBUG)
        logging.getLogger('pyutilib').setLevel(logging.DEBUG)
    if options.logfile:
        logging.getLogger('coopr.pyomo').handlers = []
        logging.getLogger('coopr').handlers = []
        logging.getLogger('pyutilib').handlers = []
        logging.getLogger('coopr.pyomo').addHandler( logging.FileHandler(options.logfile, 'w'))
        logging.getLogger('coopr').addHandler( logging.FileHandler(options.logfile, 'w'))
        logging.getLogger('pyutilib').addHandler( logging.FileHandler(options.logfile, 'w'))
    #
    # Setup I/O redirect to a file
    #
    logfile = getattr(options, 'output', None)
    if not logfile is None:
        pyutilib.misc.setup_redirect(logfile)
    #
    # Call the main Pyomo runner with profiling
    #
    if options.profile > 0:
        if not pstats_available:
            if not logfile is None:
                pyutilib.misc.reset_redirect()
            msg = "Cannot use the 'profile' option.  The Python 'pstats' "    \
                  'package cannot be imported!'
            raise ValueError, msg
        tfile = TempfileManager.create_tempfile(suffix=".profile")
        tmp = profile.runctx(
          command.__name__ + '(options=options,parser=parser)', command.__globals__, locals(), tfile
        )
        p = pstats.Stats(tfile).strip_dirs()
        p.sort_stats('time', 'cum')
        p = p.print_stats(options.profile)
        p.print_callers(options.profile)
        p.print_callees(options.profile)
        p = p.sort_stats('cum','calls')
        p.print_stats(options.profile)
        p.print_callers(options.profile)
        p.print_callees(options.profile)
        p = p.sort_stats('calls')
        p.print_stats(options.profile)
        p.print_callers(options.profile)
        p.print_callees(options.profile)
        TempfileManager.clear_tempfiles()
        retval = [tmp, None]
    else:
        #
        # Call the main Pyomo runner without profiling
        #
        try:
            retval = command(options=options, parser=parser)
        except SystemExit, err:
            if __debug__:
                if options.debug or options.catch:
                    sys.exit(0)
            print 'Exiting %s: %s' % (name, str(err))
            retval = 1
        except Exception, err:
            # If debugging is enabled, pass the exception up the chain
            # (to pyomo_excepthook)
            if __debug__:
                if options.debug or options.catch:
                    if not logfile is None:
                        pyutilib.misc.reset_redirect()
                    raise

            if len(options.model_file) > 0:
                model = "model " + options.model_file
            else:
                model = "model"

            global filter_excepthook
            if filter_excepthook:
                action = "loading"
            else:
                action = "running"

            msg = "Unexpected exception while %s %s\n" % (action, model)
            #
            # This handles the case where the error is propagated by a KeyError.
            # KeyError likes to pass raw strings that don't handle newlines
            # (they translate "\n" to "\\n"), as well as tacking on single
            # quotes at either end of the error message. This undoes all that.
            #
            errStr = str(err)
            if type(err) == KeyError and errStr != "None":
                errStr = str(err).replace(r"\n","\n")[1:-1]

            logging.getLogger('coopr.pyomo').error(msg+errStr)
            retval = 1

    if not logfile is None:
        pyutilib.misc.reset_redirect()

    if options.disable_gc:
        gc.enable()
    return pyutilib.misc.Options(retval=retval)
