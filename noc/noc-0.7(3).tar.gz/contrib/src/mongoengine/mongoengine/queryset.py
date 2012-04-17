from connection import _get_db

import pprint
import pymongo
import pymongo.code
import pymongo.dbref
import pymongo.objectid
import re
import copy
import itertools
import operator

__all__ = ['queryset_manager', 'Q', 'InvalidQueryError',
           'DO_NOTHING', 'NULLIFY', 'CASCADE', 'DENY']


# The maximum number of items to display in a QuerySet.__repr__
REPR_OUTPUT_SIZE = 20

# Delete rules
DO_NOTHING = 0
NULLIFY = 1
CASCADE = 2
DENY = 3


class DoesNotExist(Exception):
    pass


class MultipleObjectsReturned(Exception):
    pass


class InvalidQueryError(Exception):
    pass


class OperationError(Exception):
    pass


RE_TYPE = type(re.compile(''))


class QNodeVisitor(object):
    """Base visitor class for visiting Q-object nodes in a query tree.
    """

    def visit_combination(self, combination):
        """Called by QCombination objects.
        """
        return combination

    def visit_query(self, query):
        """Called by (New)Q objects.
        """
        return query


class SimplificationVisitor(QNodeVisitor):
    """Simplifies query trees by combinging unnecessary 'and' connection nodes
    into a single Q-object.
    """

    def visit_combination(self, combination):
        if combination.operation == combination.AND:
            # The simplification only applies to 'simple' queries
            if all(isinstance(node, Q) for node in combination.children):
                queries = [node.query for node in combination.children]
                return Q(**self._query_conjunction(queries))
        return combination

    def _query_conjunction(self, queries):
        """Merges query dicts - effectively &ing them together.
        """
        query_ops = set()
        combined_query = {}
        for query in queries:
            ops = set(query.keys())
            # Make sure that the same operation isn't applied more than once
            # to a single field
            intersection = ops.intersection(query_ops)
            if intersection:
                msg = 'Duplicate query conditions: '
                raise InvalidQueryError(msg + ', '.join(intersection))

            query_ops.update(ops)
            combined_query.update(copy.deepcopy(query))
        return combined_query


class QueryTreeTransformerVisitor(QNodeVisitor):
    """Transforms the query tree in to a form that may be used with MongoDB.
    """

    def visit_combination(self, combination):
        if combination.operation == combination.AND:
            # MongoDB doesn't allow us to have too many $or operations in our
            # queries, so the aim is to move the ORs up the tree to one
            # 'master' $or. Firstly, we must find all the necessary parts (part
            # of an AND combination or just standard Q object), and store them
            # separately from the OR parts.
            or_groups = []
            and_parts = []
            for node in combination.children:
                if isinstance(node, QCombination):
                    if node.operation == node.OR:
                        # Any of the children in an $or component may cause
                        # the query to succeed
                        or_groups.append(node.children)
                    elif node.operation == node.AND:
                        and_parts.append(node)
                elif isinstance(node, Q):
                    and_parts.append(node)

            # Now we combine the parts into a usable query. AND together all of
            # the necessary parts. Then for each $or part, create a new query
            # that ANDs the necessary part with the $or part.
            clauses = []
            for or_group in itertools.product(*or_groups):
                q_object = reduce(lambda a, b: a & b, and_parts, Q())
                q_object = reduce(lambda a, b: a & b, or_group, q_object)
                clauses.append(q_object)
            # Finally, $or the generated clauses in to one query. Each of the
            # clauses is sufficient for the query to succeed.
            return reduce(lambda a, b: a | b, clauses, Q())

        if combination.operation == combination.OR:
            children = []
            # Crush any nested ORs in to this combination as MongoDB doesn't
            # support nested $or operations
            for node in combination.children:
                if (isinstance(node, QCombination) and
                    node.operation == combination.OR):
                    children += node.children
                else:
                    children.append(node)
            combination.children = children

        return combination


class QueryCompilerVisitor(QNodeVisitor):
    """Compiles the nodes in a query tree to a PyMongo-compatible query
    dictionary.
    """

    def __init__(self, document):
        self.document = document

    def visit_combination(self, combination):
        if combination.operation == combination.OR:
            return {'$or': combination.children}
        elif combination.operation == combination.AND:
            return self._mongo_query_conjunction(combination.children)
        return combination

    def visit_query(self, query):
        return QuerySet._transform_query(self.document, **query.query)

    def _mongo_query_conjunction(self, queries):
        """Merges Mongo query dicts - effectively &ing them together.
        """
        combined_query = {}
        for query in queries:
            for field, ops in query.items():
                if field not in combined_query:
                    combined_query[field] = ops
                else:
                    # The field is already present in the query the only way
                    # we can merge is if both the existing value and the new
                    # value are operation dicts, reject anything else
                    if (not isinstance(combined_query[field], dict) or
                        not isinstance(ops, dict)):
                        message = 'Conflicting values for ' + field
                        raise InvalidQueryError(message)

                    current_ops = set(combined_query[field].keys())
                    new_ops = set(ops.keys())
                    # Make sure that the same operation isn't applied more than
                    # once to a single field
                    intersection = current_ops.intersection(new_ops)
                    if intersection:
                        msg = 'Duplicate query conditions: '
                        raise InvalidQueryError(msg + ', '.join(intersection))

                    # Right! We've got two non-overlapping dicts of operations!
                    combined_query[field].update(copy.deepcopy(ops))
        return combined_query


class QNode(object):
    """Base class for nodes in query trees.
    """

    AND = 0
    OR = 1

    def to_query(self, document):
        query = self.accept(SimplificationVisitor())
        query = query.accept(QueryTreeTransformerVisitor())
        query = query.accept(QueryCompilerVisitor(document))
        return query

    def accept(self, visitor):
        raise NotImplementedError

    def _combine(self, other, operation):
        """Combine this node with another node into a QCombination object.
        """
        if other.empty:
            return self

        if self.empty:
            return other

        return QCombination(operation, [self, other])

    @property
    def empty(self):
        return False

    def __or__(self, other):
        return self._combine(other, self.OR)

    def __and__(self, other):
        return self._combine(other, self.AND)


class QCombination(QNode):
    """Represents the combination of several conditions by a given logical
    operator.
    """

    def __init__(self, operation, children):
        self.operation = operation
        self.children = []
        for node in children:
            # If the child is a combination of the same type, we can merge its
            # children directly into this combinations children
            if isinstance(node, QCombination) and node.operation == operation:
                self.children += node.children
            else:
                self.children.append(node)

    def accept(self, visitor):
        for i in range(len(self.children)):
            if isinstance(self.children[i], QNode):
                self.children[i] = self.children[i].accept(visitor)

        return visitor.visit_combination(self)

    @property
    def empty(self):
        return not bool(self.children)


class Q(QNode):
    """A simple query object, used in a query tree to build up more complex
    query structures.
    """

    def __init__(self, **query):
        self.query = query

    def accept(self, visitor):
        return visitor.visit_query(self)

    @property
    def empty(self):
        return not bool(self.query)


class QueryFieldList(object):
    """Object that handles combinations of .only() and .exclude() calls"""
    ONLY = True
    EXCLUDE = False

    def __init__(self, fields=[], value=ONLY, always_include=[]):
        self.value = value
        self.fields = set(fields)
        self.always_include = set(always_include)

    def as_dict(self):
        return dict((field, self.value) for field in self.fields)

    def __add__(self, f):
        if not self.fields:
            self.fields = f.fields
            self.value = f.value
        elif self.value is self.ONLY and f.value is self.ONLY:
            self.fields = self.fields.intersection(f.fields)
        elif self.value is self.EXCLUDE and f.value is self.EXCLUDE:
            self.fields = self.fields.union(f.fields)
        elif self.value is self.ONLY and f.value is self.EXCLUDE:
            self.fields -= f.fields
        elif self.value is self.EXCLUDE and f.value is self.ONLY:
            self.value = self.ONLY
            self.fields = f.fields - self.fields

        if self.always_include:
            if self.value is self.ONLY and self.fields:
                self.fields = self.fields.union(self.always_include)
            else:
                self.fields -= self.always_include
        return self

    def reset(self):
        self.fields = set([])
        self.value = self.ONLY

    def __nonzero__(self):
        return bool(self.fields)


class QuerySet(object):
    """A set of results returned from a query. Wraps a MongoDB cursor,
    providing :class:`~mongoengine.Document` objects as the results.
    """

    __already_indexed = set()

    def __init__(self, document, collection):
        self._document = document
        self._collection_obj = collection
        self._mongo_query = None
        self._query_obj = Q()
        self._initial_query = {}
        self._where_clause = None
        self._loaded_fields = QueryFieldList()
        self._ordering = []
        self._snapshot = False
        self._timeout = True
        self._class_check = True
        self._slave_okay = False

        # If inheritance is allowed, only return instances and instances of
        # subclasses of the class being used
        if document._meta.get('allow_inheritance'):
            self._initial_query = {'_types': self._document._class_name}
            self._loaded_fields = QueryFieldList(always_include=['_cls'])
        self._cursor_obj = None
        self._limit = None
        self._skip = None
        self._hint = -1  # Using -1 as None is a valid value for hint

    def clone(self):
        """Creates a copy of the current :class:`~mongoengine.queryset.QuerySet`

        .. versionadded:: 0.5
        """
        c = self.__class__(self._document, self._collection_obj)

        copy_props = ('_initial_query', '_query_obj', '_where_clause',
                    '_loaded_fields', '_ordering', '_snapshot',
                    '_timeout', '_limit', '_skip', '_slave_okay', '_hint')

        for prop in copy_props:
            val = getattr(self, prop)
            setattr(c, prop, copy.deepcopy(val))

        return c

    @property
    def _query(self):
        if self._mongo_query is None:
            self._mongo_query = self._query_obj.to_query(self._document)
            if self._class_check:
                self._mongo_query.update(self._initial_query)
        return self._mongo_query

    def ensure_index(self, key_or_list, drop_dups=False, background=False,
        **kwargs):
        """Ensure that the given indexes are in place.

        :param key_or_list: a single index key or a list of index keys (to
            construct a multi-field index); keys may be prefixed with a **+**
            or a **-** to determine the index ordering
        """
        index_spec = QuerySet._build_index_spec(self._document, key_or_list)
        self._collection.ensure_index(
            index_spec['fields'],
            drop_dups=drop_dups,
            background=background,
            sparse=index_spec.get('sparse', False),
            unique=index_spec.get('unique', False))
        return self

    @classmethod
    def _build_index_spec(cls, doc_cls, spec):
        """Build a PyMongo index spec from a MongoEngine index spec.
        """
        if isinstance(spec, basestring):
            spec = {'fields': [spec]}
        if isinstance(spec, (list, tuple)):
            spec = {'fields': spec}

        index_list = []
        use_types = doc_cls._meta.get('allow_inheritance', True)
        for key in spec['fields']:
            # Get direction from + or -
            direction = pymongo.ASCENDING
            if key.startswith("-"):
                direction = pymongo.DESCENDING
            if key.startswith(("+", "-")):
                    key = key[1:]

            # Use real field name, do it manually because we need field
            # objects for the next part (list field checking)
            parts = key.split('.')
            fields = QuerySet._lookup_field(doc_cls, parts)
            parts = [field.db_field for field in fields]
            key = '.'.join(parts)
            index_list.append((key, direction))

            # Check if a list field is being used, don't use _types if it is
            if use_types and not all(f._index_with_types for f in fields):
                use_types = False

        # If _types is being used, prepend it to every specified index
        index_types = doc_cls._meta.get('index_types', True)
        allow_inheritance = doc_cls._meta.get('allow_inheritance')
        if spec.get('types', index_types) and allow_inheritance and use_types:
            index_list.insert(0, ('_types', 1))

        spec['fields'] = index_list

        if spec.get('sparse', False) and len(spec['fields']) > 1:
            raise ValueError(
                'Sparse indexes can only have one field in them. '
                'See https://jira.mongodb.org/browse/SERVER-2193')

        return spec

    @classmethod
    def _reset_already_indexed(cls):
        """Helper to reset already indexed, can be useful for testing purposes"""
        cls.__already_indexed = set()

    def __call__(self, q_obj=None, class_check=True, slave_okay=False, **query):
        """Filter the selected documents by calling the
        :class:`~mongoengine.queryset.QuerySet` with a query.

        :param q_obj: a :class:`~mongoengine.queryset.Q` object to be used in
            the query; the :class:`~mongoengine.queryset.QuerySet` is filtered
            multiple times with different :class:`~mongoengine.queryset.Q`
            objects, only the last one will be used
        :param class_check: If set to False bypass class name check when
            querying collection
        :param slave_okay: if True, allows this query to be run against a
            replica secondary.
        :param query: Django-style query keyword arguments
        """
        query = Q(**query)
        if q_obj:
            query &= q_obj
        self._query_obj &= query
        self._mongo_query = None
        self._cursor_obj = None
        self._class_check = class_check
        return self

    def filter(self, *q_objs, **query):
        """An alias of :meth:`~mongoengine.queryset.QuerySet.__call__`
        """
        return self.__call__(*q_objs, **query)

    def all(self):
        """Returns all documents."""
        return self.__call__()

    @property
    def _collection(self):
        """Property that returns the collection object. This allows us to
        perform operations only if the collection is accessed.
        """
        if self._document not in QuerySet.__already_indexed:
            QuerySet.__already_indexed.add(self._document)

            background = self._document._meta.get('index_background', False)
            drop_dups = self._document._meta.get('index_drop_dups', False)
            index_opts = self._document._meta.get('index_options', {})
            index_types = self._document._meta.get('index_types', True)

            # determine if an index which we are creating includes
            # _type as its first field; if so, we can avoid creating
            # an extra index on _type, as mongodb will use the existing
            # index to service queries against _type
            types_indexed = False
            def includes_types(fields):
                first_field = None
                if len(fields):
                    if isinstance(fields[0], basestring):
                        first_field = fields[0]
                    elif isinstance(fields[0], (list, tuple)) and len(fields[0]):
                        first_field = fields[0][0]
                return first_field == '_types'

            # Ensure indexes created by uniqueness constraints
            for index in self._document._meta['unique_indexes']:
                types_indexed = types_indexed or includes_types(index)
                self._collection.ensure_index(index, unique=True,
                    background=background, drop_dups=drop_dups, **index_opts)

            # Ensure document-defined indexes are created
            if self._document._meta['indexes']:
                for spec in self._document._meta['indexes']:
                    types_indexed = types_indexed or includes_types(spec['fields'])
                    opts = index_opts.copy()
                    opts['unique'] = spec.get('unique', False)
                    opts['sparse'] = spec.get('sparse', False)
                    self._collection.ensure_index(spec['fields'],
                        background=background, **opts)

            # If _types is being used (for polymorphism), it needs an index,
            # only if another index doesn't begin with _types
            if index_types and '_types' in self._query and not types_indexed:
                self._collection.ensure_index('_types',
                    background=background, **index_opts)

            # Add geo indicies
            for field in self._document._geo_indices():
                index_spec = [(field.db_field, pymongo.GEO2D)]
                self._collection.ensure_index(index_spec,
                    background=background, **index_opts)

        return self._collection_obj

    @property
    def _cursor_args(self):
        cursor_args = {
            'snapshot': self._snapshot,
            'timeout': self._timeout,
            'slave_okay': self._slave_okay
        }
        if self._loaded_fields:
            cursor_args['fields'] = self._loaded_fields.as_dict()
        return cursor_args

    @property
    def _cursor(self):
        if self._cursor_obj is None:

            self._cursor_obj = self._collection.find(self._query,
                                                     **self._cursor_args)
            # Apply where clauses to cursor
            if self._where_clause:
                self._cursor_obj.where(self._where_clause)

            # apply default ordering
            if self._ordering:
                self._cursor_obj.sort(self._ordering)
            elif self._document._meta['ordering']:
                self.order_by(*self._document._meta['ordering'])

            if self._limit is not None:
                self._cursor_obj.limit(self._limit)

            if self._skip is not None:
                self._cursor_obj.skip(self._skip)

            if self._hint != -1:
                self._cursor_obj.hint(self._hint)

        return self._cursor_obj

    @classmethod
    def _lookup_field(cls, document, parts):
        """Lookup a field based on its attribute and return a list containing
        the field's parents and the field.
        """
        if not isinstance(parts, (list, tuple)):
            parts = [parts]
        fields = []
        field = None

        for field_name in parts:
            # Handle ListField indexing:
            if field_name.isdigit():
                try:
                    new_field = field.field
                except AttributeError, err:
                    raise InvalidQueryError(
                        "Can't use index on unsubscriptable field (%s)" % err)
                fields.append(field_name)
                continue
            if field is None:
                # Look up first field from the document
                if field_name == 'pk':
                    # Deal with "primary key" alias
                    field_name = document._meta['id_field']
                field = document._fields[field_name]
            else:
                # Look up subfield on the previous field
                new_field = field.lookup_member(field_name)
                from base import ComplexBaseField
                if not new_field and isinstance(field, ComplexBaseField):
                    fields.append(field_name)
                    continue
                elif not new_field:
                    raise InvalidQueryError('Cannot resolve field "%s"'
                                                % field_name)
                field = new_field  # update field to the new field type
            fields.append(field)

        return fields

    @classmethod
    def _translate_field_name(cls, doc_cls, field, sep='.'):
        """Translate a field attribute name to a database field name.
        """
        parts = field.split(sep)
        parts = [f.db_field for f in QuerySet._lookup_field(doc_cls, parts)]
        return '.'.join(parts)

    @classmethod
    def _transform_query(cls, _doc_cls=None, _field_operation=False, **query):
        """Transform a query from Django-style format to Mongo format.
        """
        operators = ['ne', 'gt', 'gte', 'lt', 'lte', 'in', 'nin', 'mod',
                     'all', 'size', 'exists', 'not']
        geo_operators = ['within_distance', 'within_spherical_distance', 'within_box', 'within_polygon', 'near', 'near_sphere']
        match_operators = ['contains', 'icontains', 'startswith',
                           'istartswith', 'endswith', 'iendswith',
                           'exact', 'iexact']

        mongo_query = {}
        for key, value in query.items():
            if key == "__raw__":
                mongo_query.update(value)
                continue

            parts = key.split('__')
            indices = [(i, p) for i, p in enumerate(parts) if p.isdigit()]
            parts = [part for part in parts if not part.isdigit()]
            # Check for an operator and transform to mongo-style if there is
            op = None
            if parts[-1] in operators + match_operators + geo_operators:
                op = parts.pop()

            negate = False
            if parts[-1] == 'not':
                parts.pop()
                negate = True

            if _doc_cls:
                # Switch field names to proper names [set in Field(name='foo')]
                fields = QuerySet._lookup_field(_doc_cls, parts)
                parts = []

                cleaned_fields = []
                append_field = True
                for field in fields:
                    if isinstance(field, str):
                        parts.append(field)
                        append_field = False
                    else:
                        parts.append(field.db_field)
                    if append_field:
                        cleaned_fields.append(field)

                # Convert value to proper value
                field = cleaned_fields[-1]

                singular_ops = [None, 'ne', 'gt', 'gte', 'lt', 'lte', 'not']
                singular_ops += match_operators
                if op in singular_ops:
                    if isinstance(field, basestring):
                        if op in match_operators and isinstance(value, basestring):
                            from mongoengine import StringField
                            value = StringField().prepare_query_value(op, value)
                        else:
                            value = field
                    else:
                        value = field.prepare_query_value(op, value)
                elif op in ('in', 'nin', 'all', 'near'):
                    # 'in', 'nin' and 'all' require a list of values
                    value = [field.prepare_query_value(op, v) for v in value]

            # if op and op not in match_operators:
            if op:
                if op in geo_operators:
                    if op == "within_distance":
                        value = {'$within': {'$center': value}}
                    elif op == "within_spherical_distance":
                        value = {'$within': {'$centerSphere': value}}
                    elif op == "within_polygon":
                        value = {'$within': {'$polygon': value}}
                    elif op == "near":
                        value = {'$near': value}
                    elif op == "near_sphere":
                        value = {'$nearSphere': value}
                    elif op == 'within_box':
                        value = {'$within': {'$box': value}}
                    else:
                        raise NotImplementedError("Geo method '%s' has not "
                                                  "been implemented" % op)
                elif op not in match_operators:
                    value = {'$' + op: value}

            if negate:
                value = {'$not': value}

            for i, part in indices:
                parts.insert(i, part)
            key = '.'.join(parts)
            if op is None or key not in mongo_query:
                mongo_query[key] = value
            elif key in mongo_query and isinstance(mongo_query[key], dict):
                mongo_query[key].update(value)

        return mongo_query

    def get(self, *q_objs, **query):
        """Retrieve the the matching object raising
        :class:`~mongoengine.queryset.MultipleObjectsReturned` or
        `DocumentName.MultipleObjectsReturned` exception if multiple results and
        :class:`~mongoengine.queryset.DoesNotExist` or `DocumentName.DoesNotExist`
        if no results are found.

        .. versionadded:: 0.3
        """
        self.__call__(*q_objs, **query)
        count = self.count()
        if count == 1:
            return self[0]
        elif count > 1:
            message = u'%d items returned, instead of 1' % count
            raise self._document.MultipleObjectsReturned(message)
        else:
            raise self._document.DoesNotExist("%s matching query does not exist."
                                              % self._document._class_name)

    def get_or_create(self, write_options=None, *q_objs, **query):
        """Retrieve unique object or create, if it doesn't exist. Returns a tuple of
        ``(object, created)``, where ``object`` is the retrieved or created object
        and ``created`` is a boolean specifying whether a new object was created. Raises
        :class:`~mongoengine.queryset.MultipleObjectsReturned` or
        `DocumentName.MultipleObjectsReturned` if multiple results are found.
        A new document will be created if the document doesn't exists; a
        dictionary of default values for the new document may be provided as a
        keyword argument called :attr:`defaults`.

        :param write_options: optional extra keyword arguments used if we
            have to create a new document.
            Passes any write_options onto :meth:`~mongoengine.Document.save`

        .. versionadded:: 0.3
        """
        defaults = query.get('defaults', {})
        if 'defaults' in query:
            del query['defaults']

        self.__call__(*q_objs, **query)
        count = self.count()
        if count == 0:
            query.update(defaults)
            doc = self._document(**query)
            doc.save(write_options=write_options)
            return doc, True
        elif count == 1:
            return self.first(), False
        else:
            message = u'%d items returned, instead of 1' % count
            raise self._document.MultipleObjectsReturned(message)

    def create(self, **kwargs):
        """Create new object. Returns the saved object instance.

        .. versionadded:: 0.4
        """
        doc = self._document(**kwargs)
        doc.save()
        return doc

    def first(self):
        """Retrieve the first object matching the query.
        """
        try:
            result = self[0]
        except IndexError:
            result = None
        return result

    def insert(self, doc_or_docs, load_bulk=True):
        """bulk insert documents

        :param docs_or_doc: a document or list of documents to be inserted
        :param load_bulk (optional): If True returns the list of document instances

        By default returns document instances, set ``load_bulk`` to False to
        return just ``ObjectIds``

        .. versionadded:: 0.5
        """
        from document import Document

        docs = doc_or_docs
        return_one = False
        if isinstance(docs, Document) or issubclass(docs.__class__, Document):
            return_one = True
            docs = [docs]

        raw = []
        for doc in docs:
            if not isinstance(doc, self._document):
                msg = "Some documents inserted aren't instances of %s" % str(self._document)
                raise OperationError(msg)
            if doc.pk:
                msg = "Some documents have ObjectIds use doc.update() instead"
                raise OperationError(msg)
            raw.append(doc.to_mongo())

        ids = self._collection.insert(raw)

        if not load_bulk:
            return return_one and ids[0] or ids

        documents = self.in_bulk(ids)
        results = []
        for obj_id in ids:
            results.append(documents.get(obj_id))
        return return_one and results[0] or results

    def with_id(self, object_id):
        """Retrieve the object matching the id provided.

        :param object_id: the value for the id of the document to look up
        """
        return self._document.objects(pk=object_id).first()

    def in_bulk(self, object_ids):
        """Retrieve a set of documents by their ids.

        :param object_ids: a list or tuple of ``ObjectId``\ s
        :rtype: dict of ObjectIds as keys and collection-specific
                Document subclasses as values.

        .. versionadded:: 0.3
        """
        doc_map = {}

        docs = self._collection.find({'_id': {'$in': object_ids}},
                                     **self._cursor_args)
        for doc in docs:
            doc_map[doc['_id']] = self._document._from_son(doc)

        return doc_map

    def next(self):
        """Wrap the result in a :class:`~mongoengine.Document` object.
        """
        try:
            if self._limit == 0:
                raise StopIteration
            return self._document._from_son(self._cursor.next())
        except StopIteration, e:
            self.rewind()
            raise e

    def rewind(self):
        """Rewind the cursor to its unevaluated state.

        .. versionadded:: 0.3
        """
        self._cursor.rewind()

    def count(self):
        """Count the selected elements in the query.
        """
        if self._limit == 0:
            return 0
        return self._cursor.count(with_limit_and_skip=True)

    def __len__(self):
        return self.count()

    def map_reduce(self, map_f, reduce_f, output, finalize_f=None, limit=None,
                   scope=None):
        """Perform a map/reduce query using the current query spec
        and ordering. While ``map_reduce`` respects ``QuerySet`` chaining,
        it must be the last call made, as it does not return a maleable
        ``QuerySet``.

        See the :meth:`~mongoengine.tests.QuerySetTest.test_map_reduce`
        and :meth:`~mongoengine.tests.QuerySetTest.test_map_advanced`
        tests in ``tests.queryset.QuerySetTest`` for usage examples.

        :param map_f: map function, as :class:`~pymongo.code.Code` or string
        :param reduce_f: reduce function, as
                         :class:`~pymongo.code.Code` or string
        :param output: output collection name, if set to 'inline' will try to
                       use :class:`~pymongo.collection.Collection.inline_map_reduce`
        :param finalize_f: finalize function, an optional function that
                           performs any post-reduction processing.
        :param scope: values to insert into map/reduce global scope. Optional.
        :param limit: number of objects from current query to provide
                      to map/reduce method

        Returns an iterator yielding
        :class:`~mongoengine.document.MapReduceDocument`.

        .. note::

            Map/Reduce changed in server version **>= 1.7.4**. The PyMongo
            :meth:`~pymongo.collection.Collection.map_reduce` helper requires
            PyMongo version **>= 1.11**.

        .. versionchanged:: 0.5
           - removed ``keep_temp`` keyword argument, which was only relevant
             for MongoDB server versions older than 1.7.4

        .. versionadded:: 0.3
        """
        from document import MapReduceDocument

        if not hasattr(self._collection, "map_reduce"):
            raise NotImplementedError("Requires MongoDB >= 1.7.1")

        map_f_scope = {}
        if isinstance(map_f, pymongo.code.Code):
            map_f_scope = map_f.scope
            map_f = unicode(map_f)
        map_f = pymongo.code.Code(self._sub_js_fields(map_f), map_f_scope)

        reduce_f_scope = {}
        if isinstance(reduce_f, pymongo.code.Code):
            reduce_f_scope = reduce_f.scope
            reduce_f = unicode(reduce_f)
        reduce_f_code = self._sub_js_fields(reduce_f)
        reduce_f = pymongo.code.Code(reduce_f_code, reduce_f_scope)

        mr_args = {'query': self._query}

        if finalize_f:
            finalize_f_scope = {}
            if isinstance(finalize_f, pymongo.code.Code):
                finalize_f_scope = finalize_f.scope
                finalize_f = unicode(finalize_f)
            finalize_f_code = self._sub_js_fields(finalize_f)
            finalize_f = pymongo.code.Code(finalize_f_code, finalize_f_scope)
            mr_args['finalize'] = finalize_f

        if scope:
            mr_args['scope'] = scope

        if limit:
            mr_args['limit'] = limit

        if output == 'inline' and not self._ordering:
            map_reduce_function = 'inline_map_reduce'
        else:
            map_reduce_function = 'map_reduce'
            mr_args['out'] = output

        results = getattr(self._collection, map_reduce_function)(map_f, reduce_f, **mr_args)

        if map_reduce_function == 'map_reduce':
            results = results.find()

        if self._ordering:
            results = results.sort(self._ordering)

        for doc in results:
            yield MapReduceDocument(self._document, self._collection,
                                    doc['_id'], doc['value'])

    def limit(self, n):
        """Limit the number of returned documents to `n`. This may also be
        achieved using array-slicing syntax (e.g. ``User.objects[:5]``).

        :param n: the maximum number of objects to return
        """
        if n == 0:
            self._cursor.limit(1)
        else:
            self._cursor.limit(n)
        self._limit = n

        # Return self to allow chaining
        return self

    def skip(self, n):
        """Skip `n` documents before returning the results. This may also be
        achieved using array-slicing syntax (e.g. ``User.objects[5:]``).

        :param n: the number of objects to skip before returning results
        """
        self._cursor.skip(n)
        self._skip = n
        return self

    def hint(self, index=None):
        """Added 'hint' support, telling Mongo the proper index to use for the
        query.

        Judicious use of hints can greatly improve query performance. When doing
        a query on multiple fields (at least one of which is indexed) pass the
        indexed field as a hint to the query.

        Hinting will not do anything if the corresponding index does not exist.
        The last hint applied to this cursor takes precedence over all others.

        .. versionadded:: 0.5
        """
        self._cursor.hint(index)
        self._hint = index
        return self

    def __getitem__(self, key):
        """Support skip and limit using getitem and slicing syntax.
        """
        # Slice provided
        if isinstance(key, slice):
            try:
                self._cursor_obj = self._cursor[key]
                self._skip, self._limit = key.start, key.stop
            except IndexError, err:
                # PyMongo raises an error if key.start == key.stop, catch it,
                # bin it, kill it.
                start = key.start or 0
                if start >= 0 and key.stop >= 0 and key.step is None:
                    if start == key.stop:
                        self.limit(0)
                        self._skip, self._limit = key.start, key.stop - start
                        return self
                raise err
            # Allow further QuerySet modifications to be performed
            return self
        # Integer index provided
        elif isinstance(key, int):
            return self._document._from_son(self._cursor[key])
        raise AttributeError

    def distinct(self, field):
        """Return a list of distinct values for a given field.

        :param field: the field to select distinct values from

        .. versionadded:: 0.4
        """
        return self._cursor.distinct(field)

    def only(self, *fields):
        """Load only a subset of this document's fields. ::

            post = BlogPost.objects(...).only("title", "author.name")

        :param fields: fields to include

        .. versionadded:: 0.3
        .. versionchanged:: 0.5 - Added subfield support
        """
        fields = dict([(f, QueryFieldList.ONLY) for f in fields])
        return self.fields(**fields)

    def exclude(self, *fields):
        """Opposite to .only(), exclude some document's fields. ::

            post = BlogPost.objects(...).exclude("comments")

        :param fields: fields to exclude

        .. versionadded:: 0.5
        """
        fields = dict([(f, QueryFieldList.EXCLUDE) for f in fields])
        return self.fields(**fields)

    def fields(self, **kwargs):
        """Manipulate how you load this document's fields.  Used by `.only()`
        and `.exclude()` to manipulate which fields to retrieve.  Fields also
        allows for a greater level of control for example:

        Retrieving a Subrange of Array Elements:

        You can use the $slice operator to retrieve a subrange of elements in
        an array ::

            post = BlogPost.objects(...).fields(slice__comments=5) // first 5 comments

        :param kwargs: A dictionary identifying what to include

        .. versionadded:: 0.5
        """

        # Check for an operator and transform to mongo-style if there is
        operators = ["slice"]
        cleaned_fields = []
        for key, value in kwargs.items():
            parts = key.split('__')
            op = None
            if parts[0] in operators:
                op = parts.pop(0)
                value = {'$' + op: value}
            key = '.'.join(parts)
            cleaned_fields.append((key, value))

        fields = sorted(cleaned_fields, key=operator.itemgetter(1))
        for value, group in itertools.groupby(fields, lambda x: x[1]):
            fields = [field for field, value in group]
            fields = self._fields_to_dbfields(fields)
            self._loaded_fields += QueryFieldList(fields, value=value)
        return self

    def all_fields(self):
        """Include all fields. Reset all previously calls of .only() and .exclude(). ::

            post = BlogPost.objects(...).exclude("comments").only("title").all_fields()

        .. versionadded:: 0.5
        """
        self._loaded_fields = QueryFieldList(always_include=self._loaded_fields.always_include)
        return self

    def _fields_to_dbfields(self, fields):
        """Translate fields paths to its db equivalents"""
        ret = []
        for field in fields:
            field = ".".join(f.db_field for f in QuerySet._lookup_field(self._document, field.split('.')))
            ret.append(field)
        return ret

    def order_by(self, *keys):
        """Order the :class:`~mongoengine.queryset.QuerySet` by the keys. The
        order may be specified by prepending each of the keys by a + or a -.
        Ascending order is assumed.

        :param keys: fields to order the query results by; keys may be
            prefixed with **+** or **-** to determine the ordering direction
        """
        key_list = []
        for key in keys:
            if not key: continue
            direction = pymongo.ASCENDING
            if key[0] == '-':
                direction = pymongo.DESCENDING
            if key[0] in ('-', '+'):
                key = key[1:]
            key = key.replace('__', '.')
            try:
                key = QuerySet._translate_field_name(self._document, key)
            except:
                pass
            key_list.append((key, direction))

        self._ordering = key_list
        self._cursor.sort(key_list)
        return self

    def explain(self, format=False):
        """Return an explain plan record for the
        :class:`~mongoengine.queryset.QuerySet`\ 's cursor.

        :param format: format the plan before returning it
        """

        plan = self._cursor.explain()
        if format:
            plan = pprint.pformat(plan)
        return plan

    def snapshot(self, enabled):
        """Enable or disable snapshot mode when querying.

        :param enabled: whether or not snapshot mode is enabled

        ..versionchanged:: 0.5 - made chainable
        """
        self._snapshot = enabled
        return self

    def timeout(self, enabled):
        """Enable or disable the default mongod timeout when querying.

        :param enabled: whether or not the timeout is used

        ..versionchanged:: 0.5 - made chainable
        """
        self._timeout = enabled
        return self

    def slave_okay(self, enabled):
        """Enable or disable the slave_okay when querying.

        :param enabled: whether or not the slave_okay is enabled
        """
        self._slave_okay = enabled
        return self

    def delete(self, safe=False):
        """Delete the documents matched by the query.

        :param safe: check if the operation succeeded before returning
        """
        doc = self._document

        # Check for DENY rules before actually deleting/nullifying any other
        # references
        for rule_entry in doc._meta['delete_rules']:
            document_cls, field_name = rule_entry
            rule = doc._meta['delete_rules'][rule_entry]
            if rule == DENY and document_cls.objects(**{field_name + '__in': self}).count() > 0:
                msg = u'Could not delete document (at least %s.%s refers to it)' % \
                        (document_cls.__name__, field_name)
                raise OperationError(msg)

        for rule_entry in doc._meta['delete_rules']:
            document_cls, field_name = rule_entry
            rule = doc._meta['delete_rules'][rule_entry]
            if rule == CASCADE:
                document_cls.objects(**{field_name + '__in': self}).delete(safe=safe)
            elif rule == NULLIFY:
                document_cls.objects(**{field_name + '__in': self}).update(
                        safe_update=safe,
                        **{'unset__%s' % field_name: 1})

        self._collection.remove(self._query, safe=safe)

    @classmethod
    def _transform_update(cls, _doc_cls=None, **update):
        """Transform an update spec from Django-style format to Mongo format.
        """
        operators = ['set', 'unset', 'inc', 'dec', 'pop', 'push', 'push_all',
                     'pull', 'pull_all', 'add_to_set']

        mongo_update = {}
        for key, value in update.items():
            parts = key.split('__')
            # Check for an operator and transform to mongo-style if there is
            op = None
            if parts[0] in operators:
                op = parts.pop(0)
                # Convert Pythonic names to Mongo equivalents
                if op in ('push_all', 'pull_all'):
                    op = op.replace('_all', 'All')
                elif op == 'dec':
                    # Support decrement by flipping a positive value's sign
                    # and using 'inc'
                    op = 'inc'
                    if value > 0:
                        value = -value
                elif op == 'add_to_set':
                    op = op.replace('_to_set', 'ToSet')

            if _doc_cls:
                # Switch field names to proper names [set in Field(name='foo')]
                fields = QuerySet._lookup_field(_doc_cls, parts)
                parts = []

                cleaned_fields = []
                append_field = True
                for field in fields:
                    if isinstance(field, str):
                        # Convert the S operator to $
                        if field == 'S':
                            field = '$'
                        parts.append(field)
                        append_field = False
                    else:
                        parts.append(field.db_field)
                    if append_field:
                        cleaned_fields.append(field)

                # Convert value to proper value
                field = cleaned_fields[-1]

                if op in (None, 'set', 'push', 'pull', 'addToSet'):
                    value = field.prepare_query_value(op, value)
                elif op in ('pushAll', 'pullAll'):
                    value = [field.prepare_query_value(op, v) for v in value]

            key = '.'.join(parts)

            if op:
                value = {key: value}
                key = '$' + op

            if op is None or key not in mongo_update:
                mongo_update[key] = value
            elif key in mongo_update and isinstance(mongo_update[key], dict):
                mongo_update[key].update(value)

        return mongo_update

    def update(self, safe_update=True, upsert=False, multi=True, write_options=None, **update):
        """Perform an atomic update on the fields matched by the query. When
        ``safe_update`` is used, the number of affected documents is returned.

        :param safe_update: check if the operation succeeded before returning
        :param upsert: Any existing document with that "_id" is overwritten.
        :param write_options: extra keyword arguments for :meth:`~pymongo.collection.Collection.update`

        .. versionadded:: 0.2
        """
        if not update:
            raise OperationError("No update parameters, would remove data")

        if not write_options:
            write_options = {}

        update = QuerySet._transform_update(self._document, **update)
        try:
            ret = self._collection.update(self._query, update, multi=multi,
                                          upsert=upsert, safe=safe_update,
                                          **write_options)
            if ret is not None and 'n' in ret:
                return ret['n']
        except pymongo.errors.OperationFailure, err:
            if unicode(err) == u'multi not coded yet':
                message = u'update() method requires MongoDB 1.1.3+'
                raise OperationError(message)
            raise OperationError(u'Update failed (%s)' % unicode(err))

    def update_one(self, safe_update=True, upsert=False, write_options=None, **update):
        """Perform an atomic update on first field matched by the query. When
        ``safe_update`` is used, the number of affected documents is returned.

        :param safe_update: check if the operation succeeded before returning
        :param upsert: Any existing document with that "_id" is overwritten.
        :param write_options: extra keyword arguments for :meth:`~pymongo.collection.Collection.update`
        :param update: Django-style update keyword arguments

        .. versionadded:: 0.2
        """
        if not update:
            raise OperationError("No update parameters, would remove data")

        if not write_options:
            write_options = {}
        update = QuerySet._transform_update(self._document, **update)
        try:
            # Explicitly provide 'multi=False' to newer versions of PyMongo
            # as the default may change to 'True'
            ret = self._collection.update(self._query, update, multi=False,
                                          upsert=upsert, safe=safe_update,
                                           **write_options)

            if ret is not None and 'n' in ret:
                return ret['n']
        except pymongo.errors.OperationFailure, e:
            raise OperationError(u'Update failed [%s]' % unicode(e))

    def __iter__(self):
        return self

    def _sub_js_fields(self, code):
        """When fields are specified with [~fieldname] syntax, where
        *fieldname* is the Python name of a field, *fieldname* will be
        substituted for the MongoDB name of the field (specified using the
        :attr:`name` keyword argument in a field's constructor).
        """
        def field_sub(match):
            # Extract just the field name, and look up the field objects
            field_name = match.group(1).split('.')
            fields = QuerySet._lookup_field(self._document, field_name)
            # Substitute the correct name for the field into the javascript
            return u'["%s"]' % fields[-1].db_field

        def field_path_sub(match):
            # Extract just the field name, and look up the field objects
            field_name = match.group(1).split('.')
            fields = QuerySet._lookup_field(self._document, field_name)
            # Substitute the correct name for the field into the javascript
            return ".".join([f.db_field for f in fields])

        code = re.sub(u'\[\s*~([A-z_][A-z_0-9.]+?)\s*\]', field_sub, code)
        code = re.sub(u'\{\{\s*~([A-z_][A-z_0-9.]+?)\s*\}\}', field_path_sub, code)
        return code

    def exec_js(self, code, *fields, **options):
        """Execute a Javascript function on the server. A list of fields may be
        provided, which will be translated to their correct names and supplied
        as the arguments to the function. A few extra variables are added to
        the function's scope: ``collection``, which is the name of the
        collection in use; ``query``, which is an object representing the
        current query; and ``options``, which is an object containing any
        options specified as keyword arguments.

        As fields in MongoEngine may use different names in the database (set
        using the :attr:`db_field` keyword argument to a :class:`Field`
        constructor), a mechanism exists for replacing MongoEngine field names
        with the database field names in Javascript code. When accessing a
        field, use square-bracket notation, and prefix the MongoEngine field
        name with a tilde (~).

        :param code: a string of Javascript code to execute
        :param fields: fields that you will be using in your function, which
            will be passed in to your function as arguments
        :param options: options that you want available to the function
            (accessed in Javascript through the ``options`` object)
        """
        code = self._sub_js_fields(code)

        fields = [QuerySet._translate_field_name(self._document, f)
                  for f in fields]
        collection = self._document._get_collection_name()

        scope = {
            'collection': collection,
            'options': options or {},
        }

        query = self._query
        if self._where_clause:
            query['$where'] = self._where_clause

        scope['query'] = query
        code = pymongo.code.Code(code, scope=scope)

        db = _get_db()
        return db.eval(code, *fields)

    def where(self, where_clause):
        """Filter ``QuerySet`` results with a ``$where`` clause (a Javascript
        expression). Performs automatic field name substitution like
        :meth:`mongoengine.queryset.Queryset.exec_js`.

        .. note:: When using this mode of query, the database will call your
                  function, or evaluate your predicate clause, for each object
                  in the collection.

        .. versionadded:: 0.5
        """
        where_clause = self._sub_js_fields(where_clause)
        self._where_clause = where_clause
        return self

    def sum(self, field):
        """Sum over the values of the specified field.

        :param field: the field to sum over; use dot-notation to refer to
            embedded document fields

        .. versionchanged:: 0.5 - updated to map_reduce as db.eval doesnt work
            with sharding.
        """
        map_func = pymongo.code.Code("""
            function() {
                emit(1, this[field] || 0);
            }
        """, scope={'field': field})

        reduce_func = pymongo.code.Code("""
            function(key, values) {
                var sum = 0;
                for (var i in values) {
                    sum += values[i];
                }
                return sum;
            }
        """)

        for result in self.map_reduce(map_func, reduce_func, output='inline'):
            return result.value
        else:
            return 0

    def average(self, field):
        """Average over the values of the specified field.

        :param field: the field to average over; use dot-notation to refer to
            embedded document fields

        .. versionchanged:: 0.5 - updated to map_reduce as db.eval doesnt work
            with sharding.
        """
        map_func = pymongo.code.Code("""
            function() {
                if (this.hasOwnProperty(field))
                    emit(1, {t: this[field] || 0, c: 1});
            }
        """, scope={'field': field})

        reduce_func = pymongo.code.Code("""
            function(key, values) {
                var out = {t: 0, c: 0};
                for (var i in values) {
                    var value = values[i];
                    out.t += value.t;
                    out.c += value.c;
                }
                return out;
            }
        """)

        finalize_func = pymongo.code.Code("""
            function(key, value) {
                return value.t / value.c;
            }
        """)

        for result in self.map_reduce(map_func, reduce_func, finalize_f=finalize_func, output='inline'):
            return result.value
        else:
            return 0

    def item_frequencies(self, field, normalize=False, map_reduce=True):
        """Returns a dictionary of all items present in a field across
        the whole queried set of documents, and their corresponding frequency.
        This is useful for generating tag clouds, or searching documents.

        .. note::

            Can only do direct simple mappings and cannot map across
            :class:`~mongoengine.ReferenceField` or
            :class:`~mongoengine.GenericReferenceField` for more complex
            counting a manual map reduce call would is required.

        If the field is a :class:`~mongoengine.ListField`, the items within
        each list will be counted individually.

        :param field: the field to use
        :param normalize: normalize the results so they add to 1.0
        :param map_reduce: Use map_reduce over exec_js

        .. versionchanged:: 0.5 defaults to map_reduce and can handle embedded
                            document lookups
        """
        if map_reduce:
            return self._item_frequencies_map_reduce(field, normalize=normalize)
        return self._item_frequencies_exec_js(field, normalize=normalize)

    def _item_frequencies_map_reduce(self, field, normalize=False):
        map_func = """
            function() {
                path = '{{~%(field)s}}'.split('.');
                field = this;
                for (p in path) { field = field[path[p]]; }
                if (field && field.constructor == Array) {
                    field.forEach(function(item) {
                        emit(item, 1);
                    });
                } else {
                    emit(field, 1);
                }
            }
        """ % dict(field=field)
        reduce_func = """
            function(key, values) {
                var total = 0;
                var valuesSize = values.length;
                for (var i=0; i < valuesSize; i++) {
                    total += parseInt(values[i], 10);
                }
                return total;
            }
        """
        values = self.map_reduce(map_func, reduce_func, 'inline')
        frequencies = {}
        for f in values:
            key = f.key
            if isinstance(key, float):
                if int(key) == key:
                    key = int(key)
                key = str(key)
            frequencies[key] = f.value

        if normalize:
            count = sum(frequencies.values())
            frequencies = dict([(k, v / count) for k, v in frequencies.items()])

        return frequencies

    def _item_frequencies_exec_js(self, field, normalize=False):
        """Uses exec_js to execute"""
        freq_func = """
            function(path) {
                path = path.split('.');

                if (options.normalize) {
                    var total = 0.0;
                    db[collection].find(query).forEach(function(doc) {
                        field = doc;
                        for (p in path) { field = field[path[p]]; }
                        if (field && field.constructor == Array) {
                            total += field.length;
                        } else {
                            total++;
                        }
                    });
                }

                var frequencies = {};
                var inc = 1.0;
                if (options.normalize) {
                    inc /= total;
                }
                db[collection].find(query).forEach(function(doc) {
                    field = doc;
                    for (p in path) { field = field[path[p]]; }
                    if (field && field.constructor == Array) {
                        field.forEach(function(item) {
                            frequencies[item] = inc + (isNaN(frequencies[item]) ? 0: frequencies[item]);
                        });
                    } else {
                        var item = field;
                        frequencies[item] = inc + (isNaN(frequencies[item]) ? 0: frequencies[item]);
                    }
                });
                return frequencies;
            }
        """
        data = self.exec_js(freq_func, field, normalize=normalize)
        if 'undefined' in data:
            data[None] = data['undefined']
            del(data['undefined'])
        return data

    def __repr__(self):
        limit = REPR_OUTPUT_SIZE + 1
        if self._limit is not None and self._limit < limit:
            limit = self._limit
        try:
            data = list(self[self._skip:limit])
        except pymongo.errors.InvalidOperation:
            return ".. queryset mid-iteration .."
        if len(data) > REPR_OUTPUT_SIZE:
            data[-1] = "...(remaining elements truncated)..."
        return repr(data)

    def select_related(self, max_depth=1):
        """Handles dereferencing of :class:`~pymongo.dbref.DBRef` objects to
        a maximum depth in order to cut down the number queries to mongodb.

        .. versionadded:: 0.5
        """
        from dereference import dereference
        return dereference(self, max_depth=max_depth)


class QuerySetManager(object):

    get_queryset = None

    def __init__(self, queryset_func=None):
        if queryset_func:
            self.get_queryset = queryset_func
        self._collections = {}

    def __get__(self, instance, owner):
        """Descriptor for instantiating a new QuerySet object when
        Document.objects is accessed.
        """
        if instance is not None:
            # Document class being used rather than a document object
            return self

        # owner is the document that contains the QuerySetManager
        queryset_class = owner._meta['queryset_class'] or QuerySet
        queryset = queryset_class(owner, owner._get_collection())
        if self.get_queryset:
            if self.get_queryset.func_code.co_argcount == 1:
                queryset = self.get_queryset(queryset)
            else:
                queryset = self.get_queryset(owner, queryset)
        return queryset


def queryset_manager(func):
    """Decorator that allows you to define custom QuerySet managers on
    :class:`~mongoengine.Document` classes. The manager must be a function that
    accepts a :class:`~mongoengine.Document` class as its first argument, and a
    :class:`~mongoengine.queryset.QuerySet` as its second argument. The method
    function should return a :class:`~mongoengine.queryset.QuerySet`, probably
    the same one that was passed in, but modified in some way.
    """
    if func.func_code.co_argcount == 1:
        import warnings
        msg = 'Methods decorated with queryset_manager should take 2 arguments'
        warnings.warn(msg, DeprecationWarning)
    return QuerySetManager(func)
