# encoding: utf-8
"""
Defines a common implementation of the PyNN API.

Simulator modules are not required to use any of the code herein, provided they
provide the correct interface, but it is suggested that they use as much as is
consistent with good performance (optimisations may require overriding some of
the default definitions given here).

Utility functions and classes:
    is_conductance()
    check_weight()
    check_delay()

Accessing individual neurons:
    IDMixin

Common API implementation/base classes:
  1. Simulation set-up and control:
    setup()
    end()
    run()
    reset()
    get_time_step()
    get_current_time()
    get_min_delay()
    get_max_delay()
    rank()
    num_processes()

  2. Creating, connecting and recording from individual neurons:
    create()
    connect()
    set()
    initialize()
    build_record()

  3. Creating, connecting and recording from populations of neurons:
    Population
    PopulationView
    Assembly
    Projection

:copyright: Copyright 2006-2011 by the PyNN team, see AUTHORS.
:license: CeCILL, see LICENSE for details.

$Id: common.py 994 2011-10-03 13:13:54Z apdavison $
"""

import numpy, os
import logging
from warnings import warn
import operator
import tempfile
from pyNN import random, recording, errors, models, standardmodels, core, space, descriptions
from pyNN.recording import files
from itertools import chain
if not 'simulator' in locals():
    simulator = None  # should be set by simulator-specific modules

DEFAULT_WEIGHT = 0.0
DEFAULT_BUFFER_SIZE = 10000
DEFAULT_MAX_DELAY = 10.0
DEFAULT_TIMESTEP = 0.1
DEFAULT_MIN_DELAY = DEFAULT_TIMESTEP

logger = logging.getLogger("PyNN")

# =============================================================================
#   Utility functions and classes
# =============================================================================


def is_conductance(target_cell):
    """
    Returns True if the target cell uses conductance-based synapses, False if
    it uses current-based synapses, and None if the synapse-basis cannot be
    determined.
    """
    if hasattr(target_cell, 'local') and target_cell.local and hasattr(target_cell, 'celltype'):
        is_conductance = target_cell.celltype.conductance_based
    else:
        is_conductance = None
    return is_conductance


def check_weight(weight, synapse_type, is_conductance):
    if weight is None:
        weight = DEFAULT_WEIGHT
    if core.is_listlike(weight):
        weight = numpy.array(weight)
        nan_filter = (1 - numpy.isnan(weight)).astype(bool)  # weight arrays may contain NaN, which should be ignored
        filtered_weight = weight[nan_filter]
        all_negative = (filtered_weight <= 0).all()
        all_positive = (filtered_weight >= 0).all()
        if not (all_negative or all_positive):
            raise errors.InvalidWeightError("Weights must be either all positive or all negative")
    elif numpy.isreal(weight):
        all_positive = weight >= 0
        all_negative = weight < 0
    else:
        raise errors.InvalidWeightError("Weight must be a number or a list/array of numbers.")
    if is_conductance or synapse_type == 'excitatory':
        if not all_positive:
            raise errors.InvalidWeightError("Weights must be positive for conductance-based and/or excitatory synapses")
    elif is_conductance == False and synapse_type == 'inhibitory':
        if not all_negative:
            raise errors.InvalidWeightError("Weights must be negative for current-based, inhibitory synapses")
    else:  # is_conductance is None. This happens if the cell does not exist on the current node.
        logger.debug("Can't check weight, conductance status unknown.")
    return weight


def check_delay(delay):
    if delay is None:
        delay = get_min_delay()
    # If the delay is too small , we have to throw an error
    if delay < get_min_delay() or delay > get_max_delay():
        raise errors.ConnectionError("delay (%s) is out of range [%s,%s]" % \
                                     (delay, get_min_delay(), get_max_delay()))
    return delay


# =============================================================================
#   Accessing individual neurons
# =============================================================================

class IDMixin(object):
    """
    Instead of storing ids as integers, we store them as ID objects,
    which allows a syntax like:
        p[3,4].tau_m = 20.0
    where p is a Population object.
    """
    # Simulator ID classes should inherit both from the base type of the ID
    # (e.g., int or long) and from IDMixin.

    def __getattr__(self, name):
        try:
            val = self.__getattribute__(name)
        except AttributeError:
            if name == "parent":
                raise Exception("parent is not set")
            try:
                val = self.get_parameters()[name]
            except KeyError:
                raise errors.NonExistentParameterError(name,
                                                       self.celltype.__class__.__name__,
                                                       self.celltype.get_parameter_names())
        return val

    def __setattr__(self, name, value):
        if name == "parent":
            object.__setattr__(self, name, value)
        elif self.celltype.has_parameter(name):
            self.set_parameters(**{name: value})
        else:
            object.__setattr__(self, name, value)

    def set_parameters(self, **parameters):
        """
        Set cell parameters, given as a sequence of parameter=value arguments.
        """
        # if some of the parameters are computed from the values of other
        # parameters, need to get and translate all parameters
        if self.local:
            if self.is_standard_cell:
                computed_parameters = self.celltype.computed_parameters()
                have_computed_parameters = numpy.any([p_name in computed_parameters
                                                      for p_name in parameters])
                if have_computed_parameters:
                    all_parameters = self.get_parameters()
                    all_parameters.update(parameters)
                    parameters = all_parameters
                parameters = self.celltype.translate(parameters)
            self.set_native_parameters(parameters)
        else:
            raise errors.NotLocalError("Cannot set parameters for a cell that does not exist on this node.")

    def get_parameters(self):
        """Return a dict of all cell parameters."""
        if self.local:
            parameters = self.get_native_parameters()
            if self.is_standard_cell:
                parameters = self.celltype.reverse_translate(parameters)
            return parameters
        else:
            raise errors.NotLocalError("Cannot obtain parameters for a cell that does not exist on this node.")

    @property
    def celltype(self):
        return self.parent.celltype

    @property
    def is_standard_cell(self):
        return issubclass(self.celltype.__class__, standardmodels.StandardCellType)

    def _set_position(self, pos):
        """
        Set the cell position in 3D space.

        Cell positions are stored in an array in the parent Population.
        """
        assert isinstance(pos, (tuple, numpy.ndarray))
        assert len(pos) == 3
        self.parent._set_cell_position(self, pos)

    def _get_position(self):
        """
        Return the cell position in 3D space.

        Cell positions are stored in an array in the parent Population, if any,
        or within the ID object otherwise. Positions are generated the first
        time they are requested and then cached.
        """
        return self.parent._get_cell_position(self)

    position = property(_get_position, _set_position)

    @property
    def local(self):
        return self.parent.is_local(self)

    def inject(self, current_source):
        """Inject current from a current source object into the cell."""
        current_source.inject_into([self])

    def get_initial_value(self, variable):
        """Get the initial value of a state variable of the cell."""
        return self.parent._get_cell_initial_value(self, variable)

    def set_initial_value(self, variable, value):
        """Set the initial value of a state variable of the cell."""
        self.parent._set_cell_initial_value(self, variable, value)

    def as_view(self):
        """Return a PopulationView containing just this cell.""" 
        index = self.parent.id_to_index(self) 
        return self.parent[index:index+1] 

# =============================================================================
#   Functions for simulation set-up and control
# =============================================================================


def setup(timestep=DEFAULT_TIMESTEP, min_delay=DEFAULT_MIN_DELAY,
          max_delay=DEFAULT_MAX_DELAY, **extra_params):
    """
    Initialises/reinitialises the simulator. Any existing network structure is
    destroyed.
    
    extra_params contains any keyword arguments that are required by a given
    simulator but not by others.
    """
    invalid_extra_params = ('mindelay', 'maxdelay', 'dt')
    for param in invalid_extra_params:
        if param in extra_params:
            raise Exception("%s is not a valid argument for setup()" % param)
    if min_delay > max_delay:
        raise Exception("min_delay has to be less than or equal to max_delay.")
    if min_delay < timestep:
        raise Exception("min_delay (%g) must be greater than timestep (%g)" % (min_delay, timestep))

def end(compatible_output=True):
    """Do any necessary cleaning up before exiting."""
    raise NotImplementedError

def run(simtime):
    """Run the simulation for simtime ms."""
    raise NotImplementedError

def reset():
    """
    Reset the time to zero, neuron membrane potentials and synaptic weights to
    their initial values, and delete any recorded data. The network structure
    is not changed, nor is the specification of which neurons to record from.
    """
    simulator.reset()

def initialize(cells, variable, value):
    assert isinstance(cells, (BasePopulation, Assembly)), type(cells)
    cells.initialize(variable, value)

def get_current_time():
    """Return the current time in the simulation."""
    return simulator.state.t

def get_time_step():
    """Return the integration time step."""
    return simulator.state.dt

def get_min_delay():
    """Return the minimum allowed synaptic delay."""
    return simulator.state.min_delay

def get_max_delay():
    """Return the maximum allowed synaptic delay."""
    return simulator.state.max_delay

def num_processes():
    """Return the number of MPI processes."""
    return simulator.state.num_processes

def rank():
    """Return the MPI rank of the current node."""
    return simulator.state.mpi_rank

# =============================================================================
#  Low-level API for creating, connecting and recording from individual neurons
# =============================================================================

def build_create(population_class):
    def create(cellclass, cellparams=None, n=1):
        """
        Create n cells all of the same type.

        If n > 1, return a list of cell ids/references.
        If n==1, return just the single id.
        """
        return population_class(n, cellclass, cellparams)  # return the Population or Population.all_cells?
    return create

def build_connect(projection_class, connector_class):
    def connect(source, target, weight=0.0, delay=None, synapse_type=None,
                p=1, rng=None):
        """
        Connect a source of spikes to a synaptic target.

        source and target can both be individual cells or lists of cells, in
        which case all possible connections are made with probability p, using
        either the random number generator supplied, or the default rng
        otherwise. Weights should be in nA or µS.
        """
        if isinstance(source, IDMixin):
            source = source.as_view()
        if isinstance(target, IDMixin):
            target = target.as_view()
        connector = connector_class(p_connect=p, weights=weight, delays=delay)
        return projection_class(source, target, connector, target=synapse_type, rng=rng)
    return connect

def set(cells, param, val=None):
    """
    Set one or more parameters of an individual cell or list of cells.

    param can be a dict, in which case val should not be supplied, or a string
    giving the parameter name, in which case val is the parameter value.
    """
    assert isinstance(cells, (BasePopulation, Assembly))
    cells.set(param, val)

def build_record(variable, simulator):
    def record(source, filename):
        """
        Record spikes to a file. source can be an individual cell, a Population,
        PopulationView or Assembly.
        """
        # would actually like to be able to record to an array and choose later
        # whether to write to a file.
        if not isinstance(source, (BasePopulation, Assembly)):
            source = source.parent
        source._record(variable, to_file=filename)
        # recorder_list is used by end()
        if isinstance(source, BasePopulation):
            simulator.recorder_list.append(source.recorders[variable])  # this is a bit hackish - better to add to Population.__del__?
        if isinstance(source, Assembly):
            for population in source.populations:
                simulator.recorder_list.append(population.recorders[variable])
    if variable == 'v':
        record.__name__ = "record_v"
        record.__doc__ = """
            Record membrane potential to a file. source can be an individual
            cell, a Population, PopulationView or Assembly."""
    elif variable == 'gsyn':
        record.__name__ = "record_gsyn"
        record.__doc__ = """
            Record synaptic conductances to a file. source can be an individual
            cell, a Population, PopulationView or Assembly."""
    return record


# =============================================================================
#   High-level API for creating, connecting and recording from populations of
#   neurons.
# =============================================================================

class BasePopulation(object):
    record_filter = None

    def __getitem__(self, index):
        """
        Return either a single cell (ID object) from the Population, if index
        is an integer, or a subset of the cells (PopulationView object), if
        index is a slice or array.
        
        Note that __getitem__ is called when using [] access, e.g.
            p = Population(...)
            p[2] is equivalent to p.__getitem__(2).
            p[3:6] is equivalent to p.__getitem__(slice(3, 6))
        """
        if isinstance(index, int):
            return self.all_cells[index]
        elif isinstance(index, (slice, list, numpy.ndarray)):
            return PopulationView(self, index)
        elif isinstance(index, tuple):
            return PopulationView(self, list(index))
        else:
            raise TypeError("indices must be integers, slices, lists, arrays or tuples, not %s" % type(index).__name__)

    def __len__(self):
        """Return the total number of cells in the population (all nodes)."""
        return self.size

    @property
    def local_size(self):
        return len(self.local_cells) # would self._mask_local.sum() be faster?

    def __iter__(self):
        """Iterator over cell ids on the local node."""
        return iter(self.local_cells)

    @property
    def conductance_based(self):
        return self.celltype.conductance_based

    def is_local(self, id):
        """
        Determine whether the cell with the given ID exists on the local MPI node.
        """
        assert id.parent is self
        index = self.id_to_index(id)
        return self._mask_local[index]

    def all(self):
        """Iterator over cell ids on all nodes."""
        return iter(self.all_cells)

    def __add__(self, other):
        """
        A Population/PopulationView can be added to another Population,
        PopulationView or Assembly, returning an Assembly.
        """
        assert isinstance(other, BasePopulation)
        return Assembly(self, other)

    def _get_cell_position(self, id):
        index = self.id_to_index(id)
        return self.positions[:, index]

    def _set_cell_position(self, id, pos):
        index = self.id_to_index(id)
        self.positions[:, index] = pos

    def _get_cell_initial_value(self, id, variable):
        assert isinstance(self.initial_values[variable], core.LazyArray)
        index = self.id_to_local_index(id)
        return self.initial_values[variable][index]

    def _set_cell_initial_value(self, id, variable, value):
        assert isinstance(self.initial_values[variable], core.LazyArray)
        index = self.id_to_local_index(id)
        self.initial_values[variable][index] = value

    def nearest(self, position):
        """Return the neuron closest to the specified position."""
        # doesn't always work correctly if a position is equidistant between
        # two neurons, i.e. 0.5 should be rounded up, but it isn't always.
        # also doesn't take account of periodic boundary conditions
        pos = numpy.array([position] * self.positions.shape[1]).transpose()
        dist_arr = (self.positions - pos)**2
        distances = dist_arr.sum(axis=0)
        nearest = distances.argmin()
        return self[nearest]

    def sample(self, n, rng=None):
        """
        Randomly sample n cells from the Population, and return a PopulationView
        object.
        """
        assert isinstance(n, int)
        if not rng:
            rng = random.NumpyRNG()
        indices = rng.permutation(numpy.arange(len(self)))[0:n]
        logger.debug("The %d cells recorded have indices %s" % (n, indices))
        logger.debug("%s.sample(%s)", self.label, n)
        return PopulationView(self, indices)

    def get(self, parameter_name, gather=False):
        """
        Get the values of a parameter for every local cell in the population.
        """
        # if all the cells have the same value for this parameter, should
        # we return just the number, rather than an array?
        
        if hasattr(self, "_get_array"):
            values = self._get_array(parameter_name).tolist()
        else:
            values = [getattr(cell, parameter_name) for cell in self]  # list or array?
        
        if gather == True and num_processes() > 1:
            all_values  = { rank(): values }
            all_indices = { rank(): self.local_cells.tolist()}
            all_values  = recording.gather_dict(all_values)
            all_indices = recording.gather_dict(all_indices)
            if rank() == 0:
                values  = reduce(operator.add, all_values.values())
                indices = reduce(operator.add, all_indices.values())
            idx    = numpy.argsort(indices)
            values = numpy.array(values)[idx]
        return values

    def set(self, param, val=None):
        """
        Set one or more parameters for every cell in the population. param
        can be a dict, in which case val should not be supplied, or a string
        giving the parameter name, in which case val is the parameter value.
        val can be a numeric value, or list of such (e.g. for setting spike
        times).
        e.g. p.set("tau_m",20.0).
             p.set({'tau_m':20,'v_rest':-65})
        """
        #"""
        # -- Proposed change to arguments --
        #Set one or more parameters for every cell in the population.
        #
        #Each value may be a single number or a list/array of numbers of the same
        #size as the population. If the parameter itself takes lists/arrays as
        #values (e.g. spike times), then the value provided may be either a
        #single lists/1D array, a list of lists/1D arrays, or a 2D array.
        #
        #e.g. p.set(tau_m=20.0).
        #     p.set(tau_m=20, v_rest=[-65.0, -65.3, ... , -67.2])
        #"""
        if isinstance(param, str):
            param_dict = {param: val}
        elif isinstance(param, dict):
            param_dict = param
        else:
            raise errors.InvalidParameterValueError
        param_dict = self.celltype.checkParameters(param_dict, with_defaults=False)
        logger.debug("%s.set(%s)", self.label, param_dict)
        if hasattr(self, "_set_array"):
            self._set_array(**param_dict)
        else:
            for cell in self:
                cell.set_parameters(**param_dict)

    def tset(self, parametername, value_array):
        """
        'Topographic' set. Set the value of parametername to the values in
        value_array, which must have the same dimensions as the Population.
        """
        #"""
        # -- Proposed change to arguments --
        #'Topographic' set. Each value in parameters should be a function that
        #accepts arguments x,y,z and returns a single value.
        #"""
        if parametername not in self.celltype.get_parameter_names():
            raise errors.NonExistentParameterError(parametername, self.celltype, self.celltype.get_parameter_names())
        if (self.size,) == value_array.shape:  # the values are numbers or non-array objects
            local_values = value_array[self._mask_local]
            assert local_values.size == self.local_cells.size, "%d != %d" % (local_values.size, self.local_cells.size)
        elif len(value_array.shape) == 2:  # the values are themselves 1D arrays
            if value_array.shape[0] != self.size:
                raise errors.InvalidDimensionsError("Population: %d, value_array first dimension: %s" % (self.size,
                                                                                                         value_array.shape[0]))
            local_values = value_array[self._mask_local]  # not sure this works
        else:
            raise errors.InvalidDimensionsError("Population: %d, value_array: %s" % (self.size,
                                                                                     str(value_array.shape)))
        assert local_values.shape[0] == self.local_cells.size, "%d != %d" % (local_values.size, self.local_cells.size)

        try:
            logger.debug("%s.tset('%s', array(shape=%s, min=%s, max=%s))",
                         self.label, parametername, value_array.shape,
                         value_array.min(), value_array.max())
        except TypeError:  # min() and max() won't work for non-numeric values
            logger.debug("%s.tset('%s', non_numeric_array(shape=%s))",
                         self.label, parametername, value_array.shape)

        # Set the values for each cell
        if hasattr(self, "_set_array"):
            self._set_array(**{parametername: local_values})
        else:
            for cell, val in zip(self, local_values):
                setattr(cell, parametername, val)

    def rset(self, parametername, rand_distr):
        """
        'Random' set. Set the value of parametername to a value taken from
        rand_distr, which should be a RandomDistribution object.
        """
        # Note that we generate enough random numbers for all cells on all nodes
        # but use only those relevant to this node. This ensures that the
        # sequence of random numbers does not depend on the number of nodes,
        # provided that the same rng with the same seed is used on each node.
        logger.debug("%s.rset('%s', %s)", self.label, parametername, rand_distr)
        if isinstance(rand_distr.rng, random.NativeRNG):
            self._native_rset(parametername, rand_distr)
        else:
            rarr = rand_distr.next(n=self.all_cells.size, mask_local=False)
            rarr = numpy.array(rarr)  # isn't rarr already an array?
            assert rarr.size == self.size, "%s != %s" % (rarr.size, self.size)
            self.tset(parametername, rarr)

    def _call(self, methodname, arguments):
        """
        Call the method methodname(arguments) for every cell in the population.
        e.g. p.call("set_background","0.1") if the cell class has a method
        set_background().
        """
        raise NotImplementedError()

    def _tcall(self, methodname, objarr):
        """
        `Topographic' call. Call the method methodname() for every cell in the
        population. The argument to the method depends on the coordinates of
        the cell. objarr is an array with the same dimensions as the
        Population.
        e.g. p.tcall("memb_init", vinitArray) calls
        p.cell[i][j].memb_init(vInitArray[i][j]) for all i,j.
        """
        raise NotImplementedError()

    def randomInit(self, rand_distr):
        """
        Set initial membrane potentials for all the cells in the population to
        random values.
        """
        warn("The randomInit() method is deprecated, and will be removed in a future release. Use initialize('v', rand_distr) instead.")
        self.initialize('v', rand_distr)

    def initialize(self, variable, value):
        """
        Set initial values of state variables, e.g. the membrane potential.

        `value` may either be a numeric value (all neurons set to the same
                value) or a `RandomDistribution` object (each neuron gets a
                different value)
        """
        logger.debug("In Population '%s', initialising %s to %s" % (self.label, variable, value))
        if isinstance(value, random.RandomDistribution):
            initial_value = value.next(n=self.all_cells.size, mask_local=self._mask_local)
            assert len(initial_value) == self.local_size, "%d != %d" % (len(initial_value), self.local_size)
        else:
            initial_value = value
        self.initial_values[variable] = core.LazyArray(initial_value, shape=(self.local_size,))
        if hasattr(self, "_set_initial_value_array"):
            self._set_initial_value_array(variable, initial_value)
        else:
            if isinstance(value, random.RandomDistribution):
                for cell, val in zip(self, initial_value):
                    cell.set_initial_value(variable, val)
            else:
                for cell in self:  # only on local node
                    cell.set_initial_value(variable, initial_value)

    def can_record(self, variable):
        """Determine whether `variable` can be recorded from this population."""
        return (variable in self.celltype.recordable)

    def _add_recorder(self, variable):
        """Create a new Recorder for the supplied variable."""
        assert variable not in self.recorders
        if hasattr(self, "parent"):
            population = self.grandparent
        else:
            population = self
        logger.debug("Adding recorder for %s to %s" % (variable, self.label))
        population.recorders[variable] = population.recorder_class(variable,
                                                                   population=population)

    def _record(self, variable, to_file=True):
        """
        Private method called by record() and record_v().
        """
        if variable is None: # reset the list of things to record
                             # note that if _record(None) is called on a view of a population
                             # recording will be reset for the entire population, not just the view
            for recorder in self.recorders.values():
                recorder.reset()
            self.recorders = {}    
        else:
            if not self.can_record(variable):
                raise errors.RecordingError(variable, self.celltype)        
            logger.debug("%s.record('%s')", self.label, variable)
            if variable not in self.recorders:
                self._add_recorder(variable)
            if self.record_filter is not None:
                self.recorders[variable].record(self.record_filter)
            else:
                self.recorders[variable].record(self.all_cells)
            if isinstance(to_file, basestring):
                self.recorders[variable].file = to_file

    def record(self, to_file=True):
        """
        Record spikes from all cells in the Population.
        """
        self._record('spikes', to_file)

    def record_v(self, to_file=True):
        """
        Record the membrane potential for all cells in the Population.
        """
        self._record('v', to_file)

    def record_gsyn(self, to_file=True):
        """
        Record synaptic conductances for all cells in the Population.
        """
        self._record('gsyn', to_file)

    def printSpikes(self, file, gather=True, compatible_output=True):
        """
        Write spike times to file.

        file should be either a filename or a PyNN File object.

        If compatible_output is True, the format is "spiketime cell_id",
        where cell_id is the index of the cell counting along rows and down
        columns (and the extension of that for 3-D).
        This allows easy plotting of a `raster' plot of spiketimes, with one
        line for each cell.
        The timestep, first id, last id, and number of data points per cell are
        written in a header, indicated by a '#' at the beginning of the line.

        If compatible_output is False, the raw format produced by the simulator
        is used. This may be faster, since it avoids any post-processing of the
        spike files.

        For parallel simulators, if gather is True, all data will be gathered
        to the master node and a single output file created there. Otherwise, a
        file will be written on each node, containing only the cells simulated
        on that node.
        """
        self.recorders['spikes'].write(file, gather, compatible_output, self.record_filter)

    def getSpikes(self, gather=True, compatible_output=True):
        """
        Return a 2-column numpy array containing cell ids and spike times for
        recorded cells.

        Useful for small populations, for example for single neuron Monte-Carlo.
        """
        return self.recorders['spikes'].get(gather, compatible_output, self.record_filter)
        # if we haven't called record(), this will give a KeyError. A more
        # informative error message would be nice.

    def print_v(self, file, gather=True, compatible_output=True):
        """
        Write membrane potential traces to file.

        file should be either a filename or a PyNN File object.

        If compatible_output is True, the format is "v cell_id",
        where cell_id is the index of the cell counting along rows and down
        columns (and the extension of that for 3-D).
        The timestep, first id, last id, and number of data points per cell are
        written in a header, indicated by a '#' at the beginning of the line.

        If compatible_output is False, the raw format produced by the simulator
        is used. This may be faster, since it avoids any post-processing of the
        voltage files.

        For parallel simulators, if gather is True, all data will be gathered
        to the master node and a single output file created there. Otherwise, a
        file will be written on each node, containing only the cells simulated
        on that node.
        """
        self.recorders['v'].write(file, gather, compatible_output, self.record_filter)

    def get_v(self, gather=True, compatible_output=True):
        """
        Return a 2-column numpy array containing cell ids and Vm for
        recorded cells.
        """
        return self.recorders['v'].get(gather, compatible_output, self.record_filter)

    def print_gsyn(self, file, gather=True, compatible_output=True):
        """
        Write synaptic conductance traces to file.

        file should be either a filename or a PyNN File object.

        If compatible_output is True, the format is "t g cell_id",
        where cell_id is the index of the cell counting along rows and down
        columns (and the extension of that for 3-D).
        The timestep, first id, last id, and number of data points per cell are
        written in a header, indicated by a '#' at the beginning of the line.

        If compatible_output is False, the raw format produced by the simulator
        is used. This may be faster, since it avoids any post-processing of the
        voltage files.
        """
        self.recorders['gsyn'].write(file, gather, compatible_output, self.record_filter)

    def get_gsyn(self, gather=True, compatible_output=True):
        """
        Return a 3-column numpy array containing cell ids and synaptic
        conductances for recorded cells.
        """
        return self.recorders['gsyn'].get(gather, compatible_output, self.record_filter)

    def get_spike_counts(self, gather=True):
        """
        Returns the number of spikes for each neuron.
        """
        return self.recorders['spikes'].count(gather, self.record_filter)

    def meanSpikeCount(self, gather=True):
        """
        Returns the mean number of spikes per neuron.
        """
        spike_counts = self.recorders['spikes'].count(gather, self.record_filter)
        total_spikes = sum(spike_counts.values())
        if rank() == 0 or not gather:  # should maybe use allgather, and get the numbers on all nodes
            if len(spike_counts) > 0:
                return float(total_spikes)/len(spike_counts)
            else:
                return 0
        else:
            return numpy.nan
        
    def inject(self, current_source):
        """
        Connect a current source to all cells in the Population.
        """
        if not self.celltype.injectable:
            raise TypeError("Can't inject current into a spike source.")
        current_source.inject_into(self)

    def save_positions(self, file):
        """
        Save positions to file. The output format is id x y z
        """
        # first column should probably be indices, not ids. This would make it
        # simulator independent.
        if isinstance(file, basestring):
            file = files.StandardTextFile(file, mode='w')
        cells  = self.all_cells
        result = numpy.empty((len(cells), 4))
        result[:,0]   = cells
        result[:,1:4] = self.positions.T 
        if rank() == 0:
            file.write(result, {'population' : self.label})
            file.close()


class Population(BasePopulation):
    """
    A group of neurons all of the same type.
    """
    nPop = 0

    def __init__(self, size, cellclass, cellparams=None, structure=None,
                 label=None):
        """
        Create a population of neurons all of the same type.

        size - number of cells in the Population. For backwards-compatibility,
               n may also be a tuple giving the dimensions of a grid,
               e.g. n=(10,10) is equivalent to n=100 with structure=Grid2D()
        cellclass should either be a standardized cell class (a class inheriting
        from common.standardmodels.StandardCellType) or a string giving the
        name of the simulator-specific model that makes up the population.
        cellparams should be a dict which is passed to the neuron model
          constructor
        structure should be a Structure instance.
        label is an optional name for the population.
        """
        if not isinstance(size, int):  # also allow a single integer, for a 1D population
            assert isinstance(size, tuple), "`size` must be an integer or a tuple of ints. You have supplied a %s" % type(size)
            # check the things inside are ints
            for e in size:
                assert isinstance(e, int), "`size` must be an integer or a tuple of ints. Element '%s' is not an int" % str(e)

            assert structure is None, "If you specify `size` as a tuple you may not specify structure."
            if len(size) == 1:
                structure = space.Line()
            elif len(size) == 2:
                nx, ny = size
                structure = space.Grid2D(nx/float(ny))
            elif len(size) == 3:
                nx, ny, nz = size
                structure = space.Grid3D(nx/float(ny), nx/float(nz))
            else:
                raise Exception("A maximum of 3 dimensions is allowed. What do you think this is, string theory?")
            size = reduce(operator.mul, size)
        self.size = size
        self.label = label or 'population%d' % Population.nPop
        self.celltype = cellclass(cellparams)
        self._structure = structure or space.Line()
        self._positions = None
        self._is_sorted = True
        # Build the arrays of cell ids
        # Cells on the local node are represented as ID objects, other cells by integers
        # All are stored in a single numpy array for easy lookup by address
        # The local cells are also stored in a list, for easy iteration
        self._create_cells(cellclass, cellparams, size)
        self.initial_values = {}
        for variable, value in self.celltype.default_initial_values.items():
            self.initialize(variable, value)
        self.recorders = {}
        Population.nPop += 1

    @property
    def local_cells(self):
        return self.all_cells[self._mask_local]

    @property
    def cell(self):
        warn("The `Population.cell` attribute is not an official part of the \
              API, and its use is deprecated. It will be removed in a future \
              release. All uses of `cell` may be replaced by `all_cells`")
        return self.all_cells

    def id_to_index(self, id):
        """
        Given the ID(s) of cell(s) in the Population, return its (their) index
        (order in the Population).
        >>> assert p.id_to_index(p[5]) == 5
        >>> assert p.id_to_index(p.index([1,2,3])) == [1,2,3]
        """
        if not numpy.iterable(id):
            if not self.first_id <= id <= self.last_id:
                raise ValueError("id should be in the range [%d,%d], actually %d" % (self.first_id, self.last_id, id))
            return int(id - self.first_id)  # this assumes ids are consecutive
        else:
            if isinstance(id, PopulationView):
                id = id.all_cells
            id = numpy.array(id)
            if (self.first_id > id.min()) or (self.last_id < id.max()):
                raise ValueError("ids should be in the range [%d,%d], actually [%d, %d]" % (self.first_id, self.last_id, id.min(), id.max()))
            return (id - self.first_id).astype(int)  # this assumes ids are consecutive

    def id_to_local_index(self, id):
        """
        Given the ID(s) of cell(s) in the Population, return its (their) index
        (order in the Population), counting only cells on the local MPI node.
        """
        if num_processes() > 1:
            return self.local_cells.tolist().index(id)          # probably very slow
            #return numpy.nonzero(self.local_cells == id)[0][0] # possibly faster?
            # another idea - get global index, use idx-sum(mask_local[:idx])?
        else:
            return self.id_to_index(id)

    def _get_structure(self):
        return self._structure

    def _set_structure(self, structure):
        assert isinstance(structure, space.BaseStructure)
        if structure != self._structure:
            self._positions = None  # setting a new structure invalidates previously calculated positions
            self._structure = structure
    structure = property(fget=_get_structure, fset=_set_structure)
    # arguably structure should be read-only, i.e. it is not possible to change it after Population creation

    @property
    def position_generator(self):
        def gen(i):
            return self.positions[:,i]
        return gen

    def _get_positions(self):
        """
        Try to return self._positions. If it does not exist, create it and then
        return it.
        """
        if self._positions is None:
            self._positions = self.structure.generate_positions(self.size)
        assert self._positions.shape == (3, self.size)
        return self._positions

    def _set_positions(self, pos_array):
        assert isinstance(pos_array, numpy.ndarray)
        assert pos_array.shape == (3, self.size), "%s != %s" % (pos_array.shape, (3, self.size))
        self._positions = pos_array.copy()  # take a copy in case pos_array is changed later
        self._structure = None  # explicitly setting positions destroys any previous structure

    positions = property(_get_positions, _set_positions,
                         """A 3xN array (where N is the number of neurons in the Population)
                         giving the x,y,z coordinates of all the neurons (soma, in the
                         case of non-point models).""")

    def describe(self, template='population_default.txt', engine='default'):
        """
        Returns a human-readable description of the population.

        The output may be customized by specifying a different template
        togther with an associated template engine (see ``pyNN.descriptions``).

        If template is None, then a dictionary containing the template context
        will be returned.
        """
        context = {
            "label": self.label,
            "celltype": self.celltype.describe(template=None),
            "structure": None,
            "size": self.size,
            "size_local": len(self.local_cells),
            "first_id": self.first_id,
            "last_id": self.last_id,
        }
        if len(self.local_cells) > 0:
            first_id = self.local_cells[0]
            context.update({
                "local_first_id": first_id,
                "cell_parameters": first_id.get_parameters(),
            })
        if self.structure:
            context["structure"] = self.structure.describe(template=None)
        return descriptions.render(engine, template, context)


class PopulationView(BasePopulation):
    """
    A view of a subset of neurons within a Population.
    
    In most ways, Populations and PopulationViews have the same behaviour, i.e.
    they can be recorded, connected with Projections, etc. It should be noted
    that any changes to neurons in a PopulationView will be reflected in the
    parent Population and vice versa.
    
    It is possible to have views of views.
    """

    def __init__(self, parent, selector, label=None):
        """
        Create a view of a subset of neurons within a parent Population or
        PopulationView.
        
        selector - a slice or numpy mask array. The mask array should either be
                   a boolean array of the same size as the parent, or an
                   integer array containing cell indices, i.e. if p.size == 5,
                     PopulationView(p, array([False, False, True, False, True]))
                     PopulationView(p, array([2,4]))
                     PopulationView(p, slice(2,5,2))
                   will all create the same view.
        """
        self.parent = parent
        self.mask = selector # later we can have fancier selectors, for now we just have numpy masks              
        self.label  = label or "view of %s with mask %s" % (parent.label, self.mask)
        # maybe just redefine __getattr__ instead of the following...
        self.celltype     = self.parent.celltype
        # If the mask is a slice, IDs will be consecutives without duplication.
        # If not, then we need to remove duplicated IDs
        if not isinstance(self.mask, slice):
            if isinstance(self.mask, list):
                self.mask = numpy.array(self.mask)
            if self.mask.dtype is numpy.dtype('bool'):
                if len(self.mask) != len(self.parent):
                    raise Exception("Boolean masks should have the size of Parent Population")
                self.mask = numpy.arange(len(self.parent))[self.mask]     
            if len(numpy.unique(self.mask)) != len(self.mask):
                logging.warning("PopulationView can contain only once each ID, duplicated IDs are remove")
                self.mask = numpy.unique(self.mask)
        self.all_cells    = self.parent.all_cells[self.mask]  # do we need to ensure this is ordered?
        idx = numpy.argsort(self.all_cells)
        self._is_sorted =  numpy.all(idx == numpy.arange(len(self.all_cells)))
        self.size         = len(self.all_cells)
        self._mask_local  = self.parent._mask_local[self.mask]
        self.local_cells  = self.all_cells[self._mask_local]
        self.first_id     = numpy.min(self.all_cells) # only works if we assume all_cells is sorted, otherwise could use min()
        self.last_id      = numpy.max(self.all_cells)
        self.recorders    = self.parent.recorders
        self.record_filter= self.all_cells

    @property
    def initial_values(self):
        # this is going to be complex - if we keep initial_values as a dict,
        # need to return a dict-like object that takes account of self.mask
        raise NotImplementedError

    @property
    def structure(self):
        return self.parent.structure
    # should we allow setting structure for a PopulationView? Maybe if the
    # parent has some kind of CompositeStructure?

    @property
    def positions(self):
        return self.parent.positions.T[self.mask].T  # make positions N,3 instead of 3,N to avoid all this transposing?

    def id_to_index(self, id):
        """
        Given the ID(s) of cell(s) in the PopulationView, return its/their
        index/indices (order in the PopulationView).
        >>> assert id_to_index(p.index(5)) == 5
        >>> assert id_to_index(p.index([1,2,3])) == [1,2,3]
        """
        if not numpy.iterable(id):
            if self._is_sorted:
                if id not in self.all_cells:
                    raise IndexError("ID %s not present in the View" %id)
                return numpy.searchsorted(self.all_cells, id)
            else:
                result = numpy.where(self.all_cells == id)[0]
            if len(result) == 0:
                raise IndexError("ID %s not present in the View" %id)
            else:
                return result
        else:
            if self._is_sorted:
                return numpy.searchsorted(self.all_cells, id)
            else:
                result = numpy.array([])
                for item in id:
                    data = numpy.where(self.all_cells == item)[0]
                    if len(data) == 0:
                        raise IndexError("ID %s not present in the View" %item)
                    elif len(data) > 1:
                        raise Exception("ID %s is duplicated in the View" %item)
                    else:
                        result = numpy.append(result, data)
                return result
        
    @property
    def grandparent(self):
        """
        Returns the parent Population at the root of the tree (since the
        immediate parent may itself be a PopulationView).
        
        The name "grandparent" is of course a little misleading, as it could
        be just the parent, or the great, great, great, ..., grandparent.
        """
        if hasattr(self.parent, "parent"):
            return self.parent.grandparent
        else:
            return self.parent
    
    def describe(self, template='populationview_default.txt', engine='default'):
        """
        Returns a human-readable description of the population view.

        The output may be customized by specifying a different template
        togther with an associated template engine (see ``pyNN.descriptions``).

        If template is None, then a dictionary containing the template context
        will be returned.
        """
        context = {"label": self.label,
                   "parent": self.parent.label,
                   "mask": self.mask,
                   "size": self.size}
        return descriptions.render(engine, template, context)


# =============================================================================

class Assembly(object):
    """
    A group of neurons, may be heterogeneous, in contrast to a Population where
    all the neurons are of the same type.
    """
    count = 0

    def __init__(self, *populations, **kwargs):
        """
        Create an Assembly of Populations and/or PopulationViews.
        
        kwargs may contain a keyword argument 'label'.
        """
        if kwargs:
            assert kwargs.keys() == ['label']
        self.populations = []
        for p in populations:
            self._insert(p)
        self.label = kwargs.get('label', 'assembly%d' % Assembly.count)
        assert isinstance(self.label, basestring), "label must be a string or unicode"
        Assembly.count += 1

    def _insert(self, element):
        if not isinstance(element, BasePopulation):
            raise TypeError("argument is a %s, not a Population." % type(element).__name__)
        if isinstance(element, PopulationView):
            if not element.parent in self.populations:
                double = False
                for p in self.populations:
                    data = numpy.concatenate((p.all_cells, element.all_cells))
                    if len(numpy.unique(data))!= len(p.all_cells) + len(element.all_cells):
                        logging.warning('Adding a PopulationView to an Assembly containing elements already present is not posible')
                        double = True #Should we automatically remove duplicated IDs ?
                        break
                if not double:
                    self.populations.append(element)
            else:
                logging.warning('Adding a PopulationView to an Assembly when parent Population is there is not possible')
        elif isinstance(element, BasePopulation):
            if not element in self.populations:
                self.populations.append(element)
            else:
                logging.warning('Adding a Population twice in an Assembly is not possible')

    @property
    def local_cells(self):
        result = self.populations[0].local_cells
        for p in self.populations[1:]:
            result = numpy.concatenate((result, p.local_cells))
        return result

    @property
    def all_cells(self):
        result = self.populations[0].all_cells
        for p in self.populations[1:]:
            result = numpy.concatenate((result, p.all_cells))
        return result

    def all(self):
        """Iterator over cell ids on all nodes."""
        return iter(self.all_cells)    

    @property
    def _is_sorted(self):
        idx = numpy.argsort(self.all_cells)
        return numpy.all(idx == numpy.arange(len(self.all_cells)))
    
    @property
    def _homogeneous_synapses(self):
        syn = is_conductance(self.populations[0].all_cells[0])
        for p in self.populations[1:]:
            if syn != is_conductance(p.all_cells[0]):
                return False
        return True
    
    @property
    def conductance_based(self):
        return all(p.celltype.conductance_based for p in self.populations)
    
    @property
    def _mask_local(self):
        result = self.populations[0]._mask_local
        for p in self.populations[1:]:
            result = numpy.concatenate((result, p._mask_local))
        return result
    
    @property
    def first_id(self):
        return numpy.min(self.all_cells)
        
    @property
    def last_id(self):
        return numpy.max(self.all_cells)
    
    def id_to_index(self, id):
        """
        Given the ID(s) of cell(s) in the Assembly, return its (their) index
        (order in the Assembly).
        >>> assert p.id_to_index(p[5]) == 5
        >>> assert p.id_to_index(p.index([1,2,3])) == [1,2,3]
        """
        all_cells = self.all_cells
        if not numpy.iterable(id):
            if self._is_sorted:
                return numpy.searchsorted(all_cells, id)
            else:
                result = numpy.where(all_cells == id)[0]
            if len(result) == 0:
                raise IndexError("ID %s not present in the View" %id)
            else:
                return result
        else:
            if self._is_sorted:
                return numpy.searchsorted(all_cells, id)
            else:
                result = numpy.array([])
                for item in id:
                    data = numpy.where(all_cells == item)[0]
                    if len(data) == 0:
                        raise IndexError("ID %s not present in the View" %item)
                    elif len(data) > 1:
                        raise Exception("ID %s is duplicated in the View" %item)
                    else:
                        result = numpy.append(result, data)
                return result

    def all(self):
        """Iterator over cell ids on all nodes."""
        return iter(self.all_cells)    
            
    @property
    def positions(self):
        result = self.populations[0].positions
        for p in self.populations[1:]:
            result = numpy.hstack((result, p.positions))
        return result
        
    @property
    def size(self):
        return sum(p.size for p in self.populations)

    def __iter__(self):
        """
        Iterator over cells in all populations within the Assembly, for cells
        on the local MPI node.
        """
        return chain(iter(p) for p in self.populations)

    def __len__(self):
        """Return the total number of cells in the population (all nodes)."""
        return self.size

    def __getitem__(self, index):
        """
        Where index is an integer, return an ID.
        Where index is a slice, list or numpy array, return a new Assembly
          consisting of appropriate populations and (possibly newly created)
          population views.
        """
        count = 0; boundaries = [0]
        for p in self.populations:
            count += p.size
            boundaries.append(count)
        boundaries = numpy.array(boundaries)
        
        if isinstance(index, int): # return an ID
            pindex = boundaries[1:].searchsorted(index, side='right')
            return self.populations[pindex][index-boundaries[pindex]]
        elif isinstance(index, (slice, list, numpy.ndarray)):
            if isinstance(index, slice):
                indices = numpy.arange(self.size)[index]
            else:
                indices = index
            pindices = boundaries[1:].searchsorted(indices, side='right')
            views = (self.populations[i][indices[pindices==i] - boundaries[i]] for i in numpy.unique(pindices))
            return Assembly(*views)
        else:
            raise TypeError("indices must be integers, slices, lists, arrays, not %s" % type(index).__name__)

    def __add__(self, other):
        """
        An Assembly may be added to a Population, PopulationView or Assembly
        with the '+' operator, returning a new Assembly, e.g.:
        
            a2 = a1 + p
        """
        if isinstance(other, BasePopulation):
            return Assembly(*(self.populations + [other]))
        elif isinstance(other, Assembly):
            return Assembly(*(self.populations + other.populations))
        else:
            raise TypeError("can only add a Population or another Assembly to an Assembly")

    def __iadd__(self, other):
        """
        A Population, PopulationView or Assembly may be added to an existing
        Assembly using the '+=' operator, e.g.:
        
            a += p
        """
        if isinstance(other, BasePopulation):
            self._insert(other)
        elif isinstance(other, Assembly):
            for p in other.populations:
                self._insert(p)
        else:
            raise TypeError("can only add a Population or another Assembly to an Assembly")
        return self
    
    def sample(self, n, rng=None):
        """
        Randomly sample n cells from the Assembly, and return a Assembly
        object.
        """
        assert isinstance(n, int)
        if not rng:
            rng = random.NumpyRNG()
        indices = rng.permutation(numpy.arange(len(self)))[0:n]
        logger.debug("The %d cells recorded have indices %s" % (n, indices))
        logger.debug("%s.sample(%s)", self.label, n)
        return self[indices]
    
    def initialize(self, variable, value):
        """
        Set the initial value of one of the state variables of the neurons in
        this assembly.

       `value` may either be a numeric value (all neurons set to the same
        value) or a `!RandomDistribution` object (each neuron gets a
        different value)
        """
        for p in self.populations:
            p.initialize(variable, value)

    def rset(self, parametername, rand_distr):
        """
        'Random' set. Set the value of parametername to a value taken from
        rand_distr, which should be a RandomDistribution object.
        """
        for p in self.populations:
            p.rset(parametername, rand_distr)

    def _record(self, variable, to_file=True):
        # need to think about record_from
        for p in self.populations:
            p._record(variable, to_file)

    def record(self, to_file=True):
        """Record spikes from all cells in the Assembly."""
        self._record('spikes', to_file)

    def record_v(self, to_file=True):
        """Record the membrane potential from all cells in the Assembly."""
        self._record('v', to_file)

    def record_gsyn(self, to_file=True):
        """Record synaptic conductances from all cells in the Assembly."""
        self._record('gsyn', to_file)

    def get_population(self, label):
        """
        Return the Population/PopulationView from within the Assembly that has
        the given label. If no such Population exists, raise KeyError.
        """
        for p in self.populations:
            if label == p.label:
                return p
        raise KeyError("Assembly does not contain a population with the label %s" % label)

    def save_positions(self, file):
        """
        Save positions to file. The output format is id x y z
        """
        # this should be rewritten to use self.positions and recording.files
        if isinstance(file, basestring):
            file = files.StandardTextFile(file, mode='w')
        cells  = self.all_cells
        result = numpy.empty((len(cells), 4))
        result[:,0]   = cells
        result[:,1:4] = self.positions.T 
        if rank() == 0:
            file.write(result, {'assembly' : self.label})
            file.close()

    @property
    def position_generator(self):
        def gen(i):
            return self.positions[:,i]
        return gen

    def _get_recorded_variable(self, variable, gather=True, compatible_output=True, size=1):
        try:
            result = self.populations[0].recorders[variable].get(gather, compatible_output, self.populations[0].record_filter)
        except errors.NothingToWriteError:
            result = numpy.zeros((0, size+2))
        count = self.populations[0].size
        for p in self.populations[1:]:
            try:
                data = p.recorders[variable].get(gather, compatible_output, p.record_filter)
                data[:,0] += count # map index-in-population to index-in-assembly
                result = numpy.vstack((result, data))
            except errors.NothingToWriteError:
                pass
            count += p.size
        return result

    def get_v(self, gather=True, compatible_output=True):
        """
        Return a 2-column numpy array containing cell ids and Vm for
        recorded cells.
        """
        return self._get_recorded_variable('v', gather, compatible_output, size=1)

    def get_gsyn(self, gather=True, compatible_output=True):
        """
        Return a 3-column numpy array containing cell ids and synaptic
        conductances for recorded cells.
        """
        return self._get_recorded_variable('gsyn', gather, compatible_output, size=2)

    def meanSpikeCount(self, gather=True):
        """
        Returns the mean number of spikes per neuron.
        """
        spike_counts = self.get_spike_counts()
        total_spikes = sum(spike_counts.values())
        if rank() == 0 or not gather:  # should maybe use allgather, and get the numbers on all nodes
            return float(total_spikes)/len(spike_counts)
        else:
            return numpy.nan

    def get_spike_counts(self, gather=True):
        """
        Returns the number of spikes for each neuron.
        """
        try:
            spike_counts = self.populations[0].recorders['spikes'].count(gather, self.populations[0].record_filter)      
        except errors.NothingToWriteError:
            spike_counts = {}
        for p in self.populations[1:]:
            try:
                spike_counts.update(p.recorders['spikes'].count(gather, p.record_filter))
            except errors.NothingToWriteError:
                pass
        return spike_counts

    def _print(self, file, variable, format, gather=True, compatible_output=True):
        
        ## First, we write all the individual data for the heterogeneous populations
        ## embedded within the Assembly. To speed things up, we write them in temporary 
        ## folders as Numpy Binary objects
        tempdir   = tempfile.mkdtemp()
        filenames = {} 
        filename  = '%s/%s.%s' %(tempdir, self.populations[0].label, variable)
        p_file    = files.NumpyBinaryFile(filename, mode='w')
        try:
            self.populations[0].recorders[variable].write(p_file, gather, compatible_output, self.populations[0].record_filter)
            filenames[self.populations[0]] = (filename, True)        
        except errors.NothingToWriteError:
            filenames[self.populations[0]] = (filename, False)       
        for p in self.populations[1:]:
            filename = '%s/%s.%s' %(tempdir, p.label, variable)
            p_file = files.NumpyBinaryFile(filename, mode='w')           
            try:
                p.recorders[variable].write(p_file, gather, compatible_output, p.record_filter)
                filenames[p] = (filename, True)
            except errors.NothingToWriteError:
                filenames[p] = (filename, False)
                
        ## Then we need to merge the previsouly written files into a single one, to be consistent
        ## with a Population object. Note that the header should be better considered.          
        metadata = {'variable'    : variable,
                    'size'        : self.size,
                    'label'       : self.label,
                    'populations' : ", ".join(["%s[%d-%d]" %(p.label, p.first_id, p.last_id) for p in self.populations]),
                    'first_id'    : self.first_id,
                    'last_id'     : self.last_id}
        
        metadata['dt'] = simulator.state.dt # note that this has to run on all nodes (at least for NEST)
        data = numpy.zeros(format)
        for pop in filenames.keys():
            if filenames[pop][1] is True:
                name     = filenames[pop][0]
                if gather==False and simulator.state.num_processes > 1:
                    name += '.%d' % simulator.state.mpi_rank            
                p_file   = files.NumpyBinaryFile(name, mode='r') 
                tmp_data = p_file.read()                    
                if compatible_output:
                    tmp_data[:, -1] = self.id_to_index(tmp_data[:,-1] + pop.first_id)
                data = numpy.vstack((data, tmp_data))
            os.remove(name)
        metadata['n'] = data.shape[0]             
        os.rmdir(tempdir)
        
        if isinstance(file, basestring):
            if gather==False and simulator.state.num_processes > 1:
                file += '.%d' % simulator.state.mpi_rank
            file = files.StandardTextFile(file, mode='w')
        
        if simulator.state.mpi_rank == 0 or gather == False:
            file.write(data, metadata)
            file.close()

    def printSpikes(self, file, gather=True, compatible_output=True):
        """
        Write spike times to file.

        file should be either a filename or a PyNN File object.

        If compatible_output is True, the format is "spiketime cell_id",
        where cell_id is the index of the cell counting along rows and down
        columns (and the extension of that for 3-D).
        This allows easy plotting of a `raster' plot of spiketimes, with one
        line for each cell.
        The timestep, first id, last id, and number of data points per cell are
        written in a header, indicated by a '#' at the beginning of the line.

        If compatible_output is False, the raw format produced by the simulator
        is used. This may be faster, since it avoids any post-processing of the
        spike files.

        For parallel simulators, if gather is True, all data will be gathered
        to the master node and a single output file created there. Otherwise, a
        file will be written on each node, containing only the cells simulated
        on that node.
        """
        self._print(file, 'spikes', (0, 2), gather, compatible_output)

    def print_v(self, file, gather=True, compatible_output=True):
        """
        Write membrane potential traces to file.

        file should be either a filename or a PyNN File object.

        If compatible_output is True, the format is "v cell_id",
        where cell_id is the index of the cell counting along rows and down
        columns (and the extension of that for 3-D).
        The timestep, first id, last id, and number of data points per cell are
        written in a header, indicated by a '#' at the beginning of the line.

        If compatible_output is False, the raw format produced by the simulator
        is used. This may be faster, since it avoids any post-processing of the
        voltage files.

        For parallel simulators, if gather is True, all data will be gathered
        to the master node and a single output file created there. Otherwise, a
        file will be written on each node, containing only the cells simulated
        on that node.
        """
        self._print(file, 'v', (0, 2), gather, compatible_output)

    def print_gsyn(self, file, gather=True, compatible_output=True):
        """
        Write synaptic conductance traces to file.

        file should be either a filename or a PyNN File object.

        If compatible_output is True, the format is "t g cell_id",
        where cell_id is the index of the cell counting along rows and down
        columns (and the extension of that for 3-D).
        The timestep, first id, last id, and number of data points per cell are
        written in a header, indicated by a '#' at the beginning of the line.

        If compatible_output is False, the raw format produced by the simulator
        is used. This may be faster, since it avoids any post-processing of the
        voltage files.
        """
        self._print(file, 'gsyn', (0, 3), gather, compatible_output)

    def inject(self, current_source):
        """
        Connect a current source to all cells in the Assembly.
        """
        for p in self.populations:
            current_source.inject_into(p)

    def describe(self, template='assembly_default.txt', engine='default'):
        """
        Returns a human-readable description of the assembly.

        The output may be customized by specifying a different template
        togther with an associated template engine (see ``pyNN.descriptions``).

        If template is None, then a dictionary containing the template context
        will be returned.
        """
        context = {"label": self.label,
                   "populations": [p.describe(template=None) for p in self.populations]}
        return descriptions.render(engine, template, context)

# =============================================================================


class Projection(object):
    """
    A container for all the connections of a given type (same synapse type and
    plasticity mechanisms) between two populations, together with methods to
    set parameters of those connections, including of plasticity mechanisms.
    """

    def __init__(self, presynaptic_neurons, postsynaptic_neurons, method,
                 source=None, target=None, synapse_dynamics=None,
                 label=None, rng=None):
        """
        presynaptic_neurons and postsynaptic_neurons - Population, PopulationView
                                                       or Assembly objects.

        source - string specifying which attribute of the presynaptic cell
                 signals action potentials. This is only needed for
                 multicompartmental cells with branching axons or
                 dendrodendriticsynapses. All standard cells have a single
                 source, and this is the default.

        target - string specifying which synapse on the postsynaptic cell to
                 connect to. For standard cells, this can be 'excitatory' or
                 'inhibitory'. For non-standard cells, it could be 'NMDA', etc.
                 If target is not given, the default values of 'excitatory' is
                 used.

        method - a Connector object, encapsulating the algorithm to use for
                 connecting the neurons.

        synapse_dynamics - a `standardmodels.SynapseDynamics` object specifying
                 which synaptic plasticity mechanisms to use.

        rng - specify an RNG object to be used by the Connector.
        """
        for prefix, pop in zip(("pre", "post"),
                               (presynaptic_neurons, postsynaptic_neurons)):
            if not isinstance(pop, (BasePopulation, Assembly)):
                raise errors.ConnectionError("%ssynaptic_neurons must be a Population, PopulationView or Assembly, not a %s" % (prefix, type(pop)))
        
        if isinstance(postsynaptic_neurons, Assembly):
            if not postsynaptic_neurons._homogeneous_synapses:
                raise Exception('Projection to an Assembly object can be made only with homogeneous synapses types')
            
        self.pre    = presynaptic_neurons  #  } these really
        self.source = source               #  } should be
        self.post   = postsynaptic_neurons #  } read-only
        self.target = target               #  }
        self.label  = label
        if isinstance(rng, random.AbstractRNG):
            self.rng = rng
        elif rng is None:
            self.rng = random.NumpyRNG(seed=151985012)
        else:
            raise Exception("rng must be either None, or a subclass of pyNN.random.AbstractRNG")
        self._method = method
        self.synapse_dynamics = synapse_dynamics
        #self.connection = None # access individual connections. To be defined by child, simulator-specific classes
        self.weights = []
        if label is None:
            if self.pre.label and self.post.label:
                self.label = "%s→%s" % (self.pre.label, self.post.label)
        if self.synapse_dynamics:
            assert isinstance(self.synapse_dynamics, models.BaseSynapseDynamics), \
              "The synapse_dynamics argument, if specified, must be a models.BaseSynapseDynamics object, not a %s" % type(synapse_dynamics)

    def __len__(self):
        """Return the total number of local connections."""
        return len(self.connection_manager)

    def size(self, gather=True):
        """
        Return the total number of connections.
            - only local connections, if gather is False,
            - all connections, if gather is True (default)
        """
        if gather:
            n = len(self)
            return recording.mpi_sum(n)
        else:
            return len(self)

    def __repr__(self):
        return 'Projection("%s")' % self.label

    def __getitem__(self, i):
        """Return the `i`th connection within the Projection."""
        return self.connection_manager[i]

    # --- Methods for setting connection parameters ---------------------------

    def setWeights(self, w):
        """
        w can be a single number, in which case all weights are set to this
        value, or a list/1D array of length equal to the number of connections
        in the projection, or a 2D array with the same dimensions as the
        connectivity matrix (as returned by `getWeights(format='array')`).
        Weights should be in nA for current-based and µS for conductance-based
        synapses.
        """
        # should perhaps add a "distribute" argument, for symmetry with "gather" in getWeights()
        # if post is an Assembly, some components might have cond-synapses, others curr, so need a more sophisticated check here
        w = check_weight(w, self.synapse_type, is_conductance(self.post.local_cells[0]))
        self.connection_manager.set('weight', w)

    def randomizeWeights(self, rand_distr):
        """
        Set weights to random values taken from rand_distr.
        """
        # Arguably, we could merge this with set_weights just by detecting the
        # argument type. It could make for easier-to-read simulation code to
        # give it a separate name, though. Comments?
        self.setWeights(rand_distr.next(len(self)))

    def setDelays(self, d):
        """
        d can be a single number, in which case all delays are set to this
        value, or a list/1D array of length equal to the number of connections
        in the projection, or a 2D array with the same dimensions as the
        connectivity matrix (as returned by `getDelays(format='array')`).
        """
        self.connection_manager.set('delay', d)

    def randomizeDelays(self, rand_distr):
        """
        Set delays to random values taken from rand_distr.
        """
        self.setDelays(rand_distr.next(len(self)))

    def setSynapseDynamics(self, param, value):
        """
        Set parameters of the dynamic synapses for all connections in this
        projection.
        """
        self.connection_manager.set(param, value)

    def randomizeSynapseDynamics(self, param, rand_distr):
        """
        Set parameters of the synapse dynamics to values taken from rand_distr
        """
        self.setSynapseDynamics(param, rand_distr.next(len(self)))

    # --- Methods for writing/reading information to/from file. ---------------

    def getWeights(self, format='list', gather=True):
        """
        Get synaptic weights for all connections in this Projection.

        Possible formats are: a list of length equal to the number of connections
        in the projection, a 2D weight array (with NaN for non-existent
        connections). Note that for the array format, if there is more than
        one connection between two cells, the summed weight will be given.
        """
        if gather:
            logger.error("getWeights() with gather=True not yet implemented")
        return self.connection_manager.get('weight', format)

    def getDelays(self, format='list', gather=True):
        """
        Get synaptic delays for all connections in this Projection.

        Possible formats are: a list of length equal to the number of connections
        in the projection, a 2D delay array (with NaN for non-existent
        connections).
        """
        if gather:
            logger.error("getDelays() with gather=True not yet implemented")
        return self.connection_manager.get('delay', format)

    def getSynapseDynamics(self, parameter_name, format='list', gather=True):
        """
        Get parameters of the dynamic synapses for all connections in this
        Projection.
        """
        if gather:
            logger.error("getstandardmodels.SynapseDynamics() with gather=True not yet implemented")
        return self.connection_manager.get(parameter_name, format)

    def saveConnections(self, file, gather=True, compatible_output=True):
        """
        Save connections to file in a format suitable for reading in with a
        FromFileConnector.
        """
        
        if isinstance(file, basestring):
            file = files.StandardTextFile(file, mode='w')
        
        lines = []
        if not compatible_output:
            for c in self.connections:
                lines.append([c.source, c.target, c.weight, c.delay])
        else:
            for c in self.connections: 
                lines.append([self.pre.id_to_index(c.source), self.post.id_to_index(c.target), c.weight, c.delay])
        
        if gather == True and num_processes() > 1:
            all_lines = { rank(): lines }
            all_lines = recording.gather_dict(all_lines)
            if rank() == 0:
                lines = reduce(operator.add, all_lines.values())
        elif num_processes() > 1:
            file.rename('%s.%d' % (file.name, rank()))
        
        logger.debug("--- Projection[%s].__saveConnections__() ---" % self.label)
        
        if gather == False or rank() == 0:
            file.write(lines, {'pre' : self.pre.label, 'post' : self.post.label})
            file.close()

    def printWeights(self, file, format='list', gather=True):
        """
        Print synaptic weights to file. In the array format, zeros are printed
        for non-existent connections.
        """
        weights = self.getWeights(format=format, gather=gather)
        
        if isinstance(file, basestring):
            file = files.StandardTextFile(file, mode='w')
        
        if format == 'array':
            weights = numpy.where(numpy.isnan(weights), 0.0, weights)
        file.write(weights, {})
        file.close()    

    def printDelays(self, file, format='list', gather=True):
        """
        Print synaptic weights to file. In the array format, zeros are printed
        for non-existent connections.
        """
        delays = self.getDelays(format=format, gather=gather)
        
        if isinstance(file, basestring):
            file = files.StandardTextFile(file, mode='w')
        
        if format == 'array':
            delays = numpy.where(numpy.isnan(delays), 0.0, delays)
        file.write(delays, {})
        file.close()  

    def weightHistogram(self, min=None, max=None, nbins=10):
        """
        Return a histogram of synaptic weights.
        If min and max are not given, the minimum and maximum weights are
        calculated automatically.
        """
        # it is arguable whether functions operating on the set of weights
        # should be put here or in an external module.
        weights = self.getWeights(format='list', gather=True)
        if min is None:
            min = weights.min()
        if max is None:
            max = weights.max()
        bins = numpy.linspace(min, max, nbins+1)
        return numpy.histogram(weights, bins)  # returns n, bins

    def describe(self, template='projection_default.txt', engine='default'):
        """
        Returns a human-readable description of the projection.

        The output may be customized by specifying a different template
        togther with an associated template engine (see ``pyNN.descriptions``).

        If template is None, then a dictionary containing the template context
        will be returned.
        """
        context = {
            "label": self.label,
            "pre": self.pre.describe(template=None),
            "post": self.post.describe(template=None),
            "source": self.source,
            "target": self.target,
            "size_local": len(self),
            "size": self.size(gather=True),
            "connector": self._method.describe(template=None),
            "plasticity": None,
        }
        if self.synapse_dynamics:
            context.update(plasticity=self.synapse_dynamics.describe(template=None))
        return descriptions.render(engine, template, context)


# =============================================================================
