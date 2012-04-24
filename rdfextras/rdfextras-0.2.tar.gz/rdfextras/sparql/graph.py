# -*- coding: utf-8 -*-

from types import FunctionType
from rdflib.graph import ConjunctiveGraph
from rdflib.graph import Graph
from rdflib.term import BNode
from rdflib.term import Literal
from rdflib.term import URIRef
from rdflib.term import Variable
from rdflib.namespace import NamespaceManager
from rdfextras.sparql import _questChar
from rdfextras.sparql import SPARQLError
from rdflib.util import check_object
from rdflib.util import check_subject

__all__ = ['SPARQLGraph', 'GraphPattern', 'BasicGraphPattern']

class SPARQLGraph(object):
    """
    A subclass of Graph with a few extra SPARQL bits.
    """

    SPARQL_DATASET = 0
    NAMED_GRAPH = 1

    __slots__ = ("graphVariable",
                 "DAWG_DATASET_COMPLIANCE",
                 "identifier",
                 "graphKind",
                 "graph")

    def __init__(self, graph, graphVariable = None, dSCompliance = False):

        assert not graphVariable or graphVariable[0] != '?', repr(graphVariable)

        self.graphVariable = graphVariable
        self.DAWG_DATASET_COMPLIANCE = dSCompliance
        self.graphKind = None

        if graph is not None:
            self.graph = graph # TODO
            # self.store = graph.store

            if isinstance(graph, ConjunctiveGraph):
                self.graphKind = self.SPARQL_DATASET
                self.identifier = graph.default_context.identifier

            else:
                self.graphKind = self.NAMED_GRAPH
                self.identifier = graph.identifier

        #super(SPARQLGraph, self).__init__(store, identifier)

    def setupGraph(self, store, graphKind=None):
        gKind = graphKind and graphKind or self.graphKind
        self.graph = gKind(store, self.identifier)

    def __reduce__(self):
        return (SPARQLGraph,
                (None,
                 self.graphVariable,
                 self.DAWG_DATASET_COMPLIANCE),
                self.__getstate__())

    def __getstate__(self):
        return (self.graphVariable,
                self.DAWG_DATASET_COMPLIANCE,
                self.identifier)#,
                # self.graphKind)

    def __setstate__(self, arg):
        # gVar, flag, identifier, gKind = arg
        gVar,flag,identifier = arg
        self.graphVariable = gVar
        self.DAWG_DATASET_COMPLIANCE = flag
        self.identifier = identifier
        # self.graphKind = gKind
        # self.graph = Graph(store, identifier)


    ##########################################################################
    # Clustering methods

    def _clusterForward(self, seed, Cluster):
        """Cluster the triple store: from a seed, transitively get all
        properties and objects in direction of the arcs.

        :param seed: RDFLib Resource

        :param Cluster: a :class:`~rdfextras.sparql.graph.SPARQLGraph`
            instance, that has to be expanded with the new arcs

        """
        try:
            # get all predicate and object pairs for the seed.
            # *If not yet in the new cluster, then go with a recursive round
            # with those*
            for (p,o) in self.graph.predicate_objects(seed):

                if not (seed,p,o) in Cluster.graph:
                    Cluster.add((seed,p,o))
                    self._clusterForward(p, Cluster)
                    self._clusterForward(o, Cluster)

        except:
            pass


    def clusterForward(self, seed, Cluster=None):
        """
        Cluster the triple store: from a seed, transitively get all
        properties and objects in direction of the arcs.

        :param seed: RDFLib Resource

        :param Cluster: another sparqlGraph instance; if None, a new
            one will be created. The subgraph will be added to this graph.

        :return:  The :class:`~rdfextras.sparql.graph.SPARQLGraph` triple store
            containing the cluster

        """
        if Cluster == None:
            Cluster = SPARQLGraph()

        # This will raise an exception if not kosher...
        check_subject(seed) #print "Wrong type for clustering: %s" % seed
        self._clusterForward(seed, Cluster)

        return Cluster


    def _clusterBackward(self, seed, Cluster):
        """Cluster the triple store: from a seed, transitively get all
        properties and objects in backward direction of the arcs.

        :param seed: RDFLib Resource

        :param Cluster: a :class:`~rdfextras.sparql.graph.SPARQLGraph`
            instance, that has to be expanded with the new arcs

        """
        try:
            for (s,p) in self.graph.subject_predicates(seed):

                if not (s,p,seed) in Cluster.graph:
                    Cluster.add((s, p, seed))
                    self._clusterBackward(s, Cluster)
                    self._clusterBackward(p, Cluster)

        except:
            pass

    def clusterBackward(self, seed, Cluster=None):
        """
        Cluster the triple store: from a seed, transitively get all
        properties and objects 'backward', ie, following the link back
        in the graph.

        :param seed: RDFLib Resource

        :param Cluster: another sparqlGraph instance; if None, a new
            one will be created. The subgraph will be added to this graph.

        :return: The :class:`~rdfextras.sparql.graph.SPARQLGraph` triple store
            containing the cluster

        """
        if Cluster == None:
            Cluster = SPARQLGraph()

        # This will raise an exception if not kosher...
        check_object(seed) # print "Wrong type for clustering: %s" % seed
        self._clusterBackward(seed, Cluster)

        return Cluster

    def cluster(self,seed):
        """
        Cluster up and down, by summing up the forward and backward
        clustering

        :param seed: RDFLib Resource

        :return: The :class:`~rdfextras.sparql.graph.SPARQLGraph` triple store
            containing the cluster

        """
        raise "Am I getting here?"
        return self.clusterBackward(seed) + self.clusterForward(seed)


#
#
# $Date: 2005/11/04 14:06:36 $, by $Author: ivan $, $Revision: 1.1 $
#
"""
Graph pattern class used by the SPARQL implementation
"""

def _createResource(v):
    """
    Create an RDFLib Literal instance with the corresponding XML
    Schema datatype set. If the variable is already an RDFLib
    resource, it simply returns the resource; otherwise the
    corresponding Literal.  A SPARQLError Exception is raised if the
    type is not implemented.

    The Literal contains the string representation of the variable (as
    Python does it by default) with the corresponding XML Schema URI
    set.

    :param v: Python variable

    :return: either an RDFLib Literal (if 'v' is not an RDFLib Resource),
        or the same variable if it is already an RDFLib resource (i.e.,
        Literal, BNode, or URIRef)

    :raise SPARQLError: if the type of 'v' is not implemented
    """

    if isinstance(v, Literal) or isinstance(v, BNode) or isinstance(v, URIRef):
        # just do nothing
        return v

    else:
        return Literal(v) # Literal now does the datatype bits


def _isResQuest(r):
    """
    Is 'r' a request string (ie, of the form "?XXX")?

    :rtype:   Boolean
    """

    if r and isinstance(r, basestring) and r[0] == _questChar:
        return True

    return False


class GraphPattern:
    """
    Storage of one Graph Pattern, ie, the pattern tuples and the
    possible (functional) constraints (filters)
    """

    def __init__(self, patterns=[]):
        """
        :param patterns: an initial list of graph pattern tuples
        """

        self.patterns = []
        self.constraints = []
        self.unbounds = []
        self.bnodes = {}

        if type(patterns) == list:
            self.addPatterns(patterns)

        elif type(patterns) == tuple:
            self.addPattern(patterns)

        else:
            raise SPARQLError(
                "illegal argument, pattern must be a tuple or a list of tuples")

    def _generatePattern(self, tupl):
        """
        Append a tuple to the local patterns. Possible type literals
        are converted to real literals on the fly.  Each tuple should
        be contain either 3 elements (for an RDF Triplet pattern) or
        four, where the fourth element is a per-pattern constraint
        (filter). (The general constraint of SPARQL can be optimized
        by assigning a constraint to a specific pattern; because it
        stops the graph expansion, its usage might be much more
        optimal than the the 'global' constraint).

        :param tupl: either a three- or four-element tuple

        """

        if type(tupl) != tuple:
            raise SPARQLError(
                "illegal argument, pattern must be a tuple, got %s" % type(tupl))

        if len(tupl) != 3 and len(tupl) != 4:
            raise SPARQLError(
                "illegal argument, pattern must be a tuple of 3 or 4 element, got %s" % len(tupl))

        if len(tupl) == 3:
            (s,p,o) = tupl
            f = None
        else:
            (s,p,o,f) = tupl

        final = []
        for c in (s,p,o):

            if _isResQuest(c):
                if not c in self.unbounds:
                    self.unbounds.append(c)
                final.append(c)

            elif isinstance(c, BNode):
                # Do nothing - BNode name management is handled by SPARQL parser
                # if not c in self.bnodes:
                #     self.bnodes[c] = BNode()
                final.append(c)

            else:
                final.append(_createResource(c))

        final.append(f)

        return tuple(final)

    def addPattern(self, tupl):
        """
        Append a tuple to the local patterns. Possible type literals
        are converted to real literals on the fly.  Each tuple should
        be contain either 3 elements (for an RDF Triplet pattern) or
        four, where the fourth element is a per-pattern constraint
        (filter). (The general constraint of SPARQL can be optimized
        by assigning a constraint to a specific pattern; because it
        stops the graph expansion, its usage might be much more
        optimal than the the 'global' constraint).

        :param tupl: either a three- or four-element tuple

        """

        self.patterns.append(self._generatePattern(tupl))

    def insertPattern(self, tupl):
        """
        Insert a tuple to to the start of local patterns. Possible
        type literals are converted to real literals on the fly.  Each
        tuple should be contain either 3 elements (for an RDF Triplet
        pattern) or four, where the fourth element is a per-pattern
        constraint (filter). (The general constraint of SPARQL can be
        optimized by assigning a constraint to a specific pattern;
        because it stops the graph expansion, its usage might be much
        more optimal than the the 'global' constraint).

        Semantically, the behaviour induced by a graphPattern does not
        depend on the order of the patterns. However, due to the
        behaviour of the expansion algorithm, users may control the
        speed somewhat by adding patterns that would 'cut' the
        expansion tree soon (ie, patterns that reduce the available
        triplets significantly). API users may be able to do that,
        hence this additional method.

        :param tupl: either a three- or four-element tuple

        """

        self.patterns.insert(0, self._generatePattern(tupl))


    def addPatterns(self, lst):
        """
        Append a list of tuples to the local patterns. Possible type
        literals are converted to real literals on the fly.  Each
        tuple should be contain either three elements (for an RDF
        Triplet pattern) or four, where the fourth element is a
        per-pattern constraint. (The general constraint of SPARQL can
        be optimized by assigning a constraint to a specific pattern;
        because it stops the graph expansion, its usage might be much
        more optimal than the the 'global' constraint).

        :param lst: list consisting of either a three- or four-element tuples

        """

        for l in lst:
            self.addPattern(l)

    def insertPatterns(self, lst):
        """
        Insert a list of tuples to the start of the local
        patterns. Possible type literals are converted to real
        literals on the fly.  Each tuple should be contain either
        three elements (for an RDF Triplet pattern) or four, where the
        fourth element is a per-pattern constraint. (The general
        constraint of SPARQL can be optimized by assigning a
        constraint to a specific pattern; because it stops the graph
        expansion, its usage might be much more optimal than the the
        'global' constraint).

        Semantically, the behaviour induced by a graphPattern does not
        depend on the order of the patterns. However, due to the
        behaviour of the expansion algorithm, users may control the
        speed somewhat by adding patterns that would 'cut' the
        expansion tree soon (ie, patterns that reduce the available
        triplets significantly). API users may be able to do that,
        hence this additional method.

        :param lst: list consisting of either a three- or four-element tuples

        """

        for i in xrange(len(lst) -1, -1, -1):
            self.insertPattern(lst[i])

    def addConstraint(self, func):
        """
        Add a global filter constraint to the graph pattern. 'func'
        must be a method with a single input parameter (a dictionary)
        returning a boolean. This method is I{added} to previously
        added methods, ie, I{all} methods must return True to accept a
        binding.

        :param func: filter function

        """

        if type(func) == FunctionType:
            self.constraints.append(func)
        else:
            raise SPARQLError(
                "illegal argument, constraint must be a function type, got %s" % type(func))

    def addConstraints(self, lst):
        """
        Add a list of global filter constraints to the graph
        pattern. Each function in the list must be a method with a
        single input parameter (a dictionary) returning a
        boolean. These methods are I{added} to previously added
        methods, ie, I{all} methods must return True to accept a
        binding.

        :param lst: list of functions

        """

        for l in lst:
            self.addConstraint(l)

    def construct(self, tripleStore, bindings):
        """
        Add triples to a tripleStore based on a variable bindings of
        the patterns stored locally.  The triples are patterned by the
        current Graph Pattern. The method is used to construct a graph
        after a successful querying.

        :param tripleStore: an (rdflib) Triple Store
        :param bindings: dictionary

        """
        localBnodes = {}

        for c in self.bnodes:
            localBnodes[c] = BNode()

        def bind(st):
            if _isResQuest(st):

                if st in bindings:
                    return bindings[st]

                else:

                    if isinstance(self, GraphPattern):
                        return st
                    else:
                        return None

            elif isinstance(st, BNode):

                for c in self.bnodes:

                    if self.bnodes[c] == st:
                        # this is a BNode that was created as part of building
                        # up the pattern
                        return localBnodes[c]

                # if we got here, the BNode comes from somewhere else...
                return st

            else:
                return st

        for pattern in self.patterns:
            (s,p,o,f) = pattern
            triplet = []
            valid = True

            for res in (s,p,o):
                val = bind(res)

                if val != None:
                    triplet.append(val)
                else:
                    valid = False
                    break

            if valid:
                tripleStore.add(tuple(triplet))

    def __add__(self, other):
        """Adding means concatenating all the patterns and filters arrays"""

        retval = GraphPattern()
        retval += self
        retval += other
        return retval

    def __iadd__(self, other):
        """Adding means concatenating all the patterns and filters arrays"""

        self.patterns += other.patterns
        self.constraints += other.constraints

        for c in other.unbounds:
            if not c in self.unbounds:
                self.unbounds.append(c)

        for c in other.bnodes:
            if not c in self.bnodes:
                self.bnodes[c] = other.bnodes[c]

        return self

    def __str__(self):
        return self.__repr__()

    def isEmpty(self):
        """Is the pattern empty?

        :return:   Boolean
        """
        return len(self.patterns) == 0


class BasicGraphPattern(GraphPattern):
    """
    One justified, problem with the current definition of
    :class:`~rdfextras.sparql.graph.GraphPattern` is that it makes it
    difficult for users to use a literal of the type ``?XXX``, because
    any string beginning with ``?`` will be considered to be an unbound
    variable. The only way of doing this is that the user explicitly
    creates a :class:`rdflib.term.Literal` object and uses that as part
    of the pattern.

    This class is a superclass of :class:`~rdfextras.sparql.graph.GraphPattern`
    which does *not* do this, but requires the usage of a separate variable
    class instance
    """

    def __init__(self, patterns=[], prolog=None):
        """
        :param patterns: an initial list of graph pattern tuples
        """

        GraphPattern.__init__(self, patterns)
        self.prolog = prolog

    def canonicalTerm(self, term):

        if isinstance(term, URIRef):

            if self.prolog is not None:
                namespace_manager = NamespaceManager(Graph())

                for prefix,uri in self.prolog.prefixBindings.items():
                    namespace_manager.bind(prefix, uri, override=False)

                try:
                    prefix,uri,localName = namespace_manager.compute_qname(term)
                except:
                    return term

                if prefix not in self.prolog.prefixBindings:
                    return term
                else:
                    return u':'.join([prefix, localName])

            else:
                return term

        elif isinstance(term, Literal):
            return term.n3()

        elif isinstance(term, BNode):
            return term.n3()

        else:
            assert isinstance(term, Variable)
            return term.n3()

    def __repr__(self):
        # from pprint import pformat
        if self.constraints:
            # return "Filter(.. a filter ..,BGP(%s))"%(','.join([pformat(p[:3]) for p in self.patterns]))
            return "Filter(.. a filter ..,BGP(%s))" % (
                ','.join([','.join([
                        self.canonicalTerm(pat[0]),
                        self.canonicalTerm(pat[1]),
                        self.canonicalTerm(pat[2])]
                        )
                            for pat in self.patterns]))

        else:
            # return "BGP(%s)"%(','.join([repr(p[:3]) for p in self.patterns]))
            return "BGP(%s)" % (
                    ','.join(['('+','.join([
                        self.canonicalTerm(s),
                        self.canonicalTerm(p),
                        self.canonicalTerm(o)]
                        )+')'
                            for s,p,o,f in self.patterns]))
        retval =  "   Patterns:    %s\n" % self.patterns
        retval += "   Constraints: %s\n" % self.constraints
        retval += "   Unbounds:    %s\n" % self.unbounds

        return retval

    def _generatePattern(self, tupl):
        """
        Append a tuple to the local patterns. Possible type literals
        are converted to real literals on the fly.  Each tuple should
        be contain either 3 elements (for an RDF Triplet pattern) or
        four, where the fourth element is a per-pattern constraint
        (filter). (The general constraint of SPARQL can be optimized
        by assigning a constraint to a specific pattern; because it
        stops the graph expansion, its usage might be much more
        optimal than the the 'global' constraint).

        :param tupl: either a three- or four-element tuple

        """
        if type(tupl) != tuple:
            raise SPARQLError(
                "illegal argument, pattern must be a tuple, got %s" % type(tupl))

        if len(tupl) != 3 and len(tupl) != 4:
            raise SPARQLError(
                "illegal argument, pattern must be a tuple of 3 or 4 element, got %s" % len(tupl))

        if len(tupl) == 3:
            (s,p,o) = tupl
            f = None
        else:
            (s,p,o,f) = tupl

        final=[]
        for c in (s,p,o):

            if isinstance(c, Variable):

                if not c in self.unbounds:
                    self.unbounds.append(c)

                final.append(c)

            elif isinstance(c, BNode):
                # Do nothing - BNode name management is handled by SPARQL parser
                final.append(c)

            else:
                final.append(_createResource(c))

        final.append(f)

        return tuple(final)

    def fetchTerminalExpression(self):
        yield self


if __name__ == '__main__':
    from rdfextras.sparql.evaluate import Unbound
    v1 = Variable("a")
    u1 = Unbound("a")
    g = BasicGraphPattern(
        [("a","?b",24), ("?r","?c",12345), (v1,"?c",3333), (u1,"?c",9999)])
    print g

