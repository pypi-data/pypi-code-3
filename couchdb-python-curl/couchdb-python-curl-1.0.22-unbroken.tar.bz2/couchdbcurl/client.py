# -*- coding: utf-8 -*-
#
# Copyright (C) 2007-2009 Christopher Lenz
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.

"""Python client API for CouchDB.

>>> server = Server('http://localhost:5984/')
>>> db = server.create('python-tests')
>>> doc_id = db.create({'type': 'Person', 'name': 'John Doe'})
>>> doc = db[doc_id]
>>> doc['type']
'Person'
>>> doc['name']
'John Doe'
>>> del db[doc.id]
>>> doc.id in db
False

>>> del server['python-tests']
"""

#import httplib2
import pycurl
import mimetypes
from urllib import quote, urlencode
from types import FunctionType
from inspect import getsource
from textwrap import dedent
import re
import socket
import sys
import hashlib
import random
from urlparse import urlparse

from cStringIO import StringIO
#from couchdbcurl import json
import json

__all__ = ['PreconditionFailed', 'ResourceNotFound', 'ResourceConflict',
           'ServerError', 'Server', 'Database', 'Document', 'ViewResults',
           'Row']
__docformat__ = 'restructuredtext en'


DEFAULT_BASE_URI = 'http://localhost:5984/'


class PreconditionFailed(Exception):
    """Exception raised when a 412 HTTP error is received in response to a
    request.
    """


class ResourceNotFound(Exception):
    """Exception raised when a 404 HTTP error is received in response to a
    request.
    """


class ResourceConflict(Exception):
    """Exception raised when a 409 HTTP error is received in response to a
    request.
    """


class ServerError(Exception):
    """Exception raised when an unexpected HTTP error is received in response
    to a request.
    """


class Server(object):
    """Representation of a CouchDB server.

    >>> server = Server('http://localhost:5984/')

    This class behaves like a dictionary of databases. For example, to get a
    list of database names on the server, you can simply iterate over the
    server object.

    New databases can be created using the `create` method:

    >>> db = server.create('python-tests')
    >>> db
    <Database 'python-tests'>

    You can access existing databases using item access, specifying the database
    name as the key:

    >>> db = server['python-tests']
    >>> db.name
    'python-tests'

    Databases can be deleted using a ``del`` statement:

    >>> del server['python-tests']
    """

    def __init__(self, uri=DEFAULT_BASE_URI, cache=None, timeout=None):
        """Initialize the server object.

        :param uri: the URI of the server (for example
                    ``http://localhost:5984/``)
        :param cache: either a cache directory path (as a string) or an object
                      compatible with the ``httplib2.FileCache`` interface. If
                      `None` (the default), no caching is performed.
        :param timeout: socket timeout in number of seconds, or `None` for no
                        timeout
        """
        #http = httplib2.Http(cache=cache, timeout=timeout)
        #http.force_exception_to_status_code = False
        #curl = pycurl.Curl()
        self.resource = Resource(uri)

    def __contains__(self, name):
        """Return whether the server contains a database with the specified
        name.

        :param name: the database name
        :return: `True` if a database with the name exists, `False` otherwise
        """
        try:
            self.resource.head(validate_dbname(name))
            return True
        except ResourceNotFound:
            return False

    def __iter__(self):
        """Iterate over the names of all databases."""
        #resp, data = self.resource.get('_all_dbs')
        data = self.resource.get('_all_dbs')
        return iter(data)

    def __len__(self):
        """Return the number of databases."""
        #resp, data = self.resource.get('_all_dbs')
        data = self.resource.get('_all_dbs')
        return len(data)

    def __nonzero__(self):
        """Return whether the server is available."""
        try:
            self.resource.head()
            return True
        except:
            return False

    def __repr__(self):
        return '<%s %r>' % (type(self).__name__, self.resource.uri)

    def __delitem__(self, name):
        """Remove the database with the specified name.

        :param name: the name of the database
        :raise ResourceNotFound: if no database with that name exists
        """
        self.resource.delete(validate_dbname(name))

    def __getitem__(self, name):
        """Return a `Database` object representing the database with the
        specified name.

        :param name: the name of the database
        :return: a `Database` object representing the database
        :rtype: `Database`
        :raise ResourceNotFound: if no database with that name exists
        """
        db = Database(uri(self.resource.uri, name), validate_dbname(name))
        #db.resource.head() # actually make a request to the database
        return db

    @property
    def config(self):
        """The configuration of the CouchDB server.

        The configuration is represented as a nested dictionary of sections and
        options from the configuration files of the server, or the default
        values for options that are not explicitly configured.

        :type: `dict`
        """
        data = self.resource.get('_config')
        return data

    @property
    def version(self):
        """The version string of the CouchDB server.

        Note that this results in a request being made, and can also be used
        to check for the availability of the server.

        :type: `unicode`"""
        data = self.resource.get()
        return data['version']

    def stats(self):
        """Database statistics."""
        data = self.resource.get('_stats')
        return data

    def tasks(self):
        """A list of tasks currently active on the server."""
        data = self.resource.get('_active_tasks')
        return data

    def create(self, name):
        """Create a new database with the given name.

        :param name: the name of the database
        :return: a `Database` object representing the created database
        :rtype: `Database`
        :raise PreconditionFailed: if a database with that name already exists
        """
        self.resource.put(validate_dbname(name))
        return self[name]

    def delete(self, name):
        """Delete the database with the specified name.

        :param name: the name of the database
        :raise ResourceNotFound: if a database with that name does not exist
        :since: 0.6
        """
        del self[name]

    def replicate(self, source, target, **options):
        """Replicate changes from the source database to the target database.

        :param source: URL of the source database
        :param target: URL of the target database
        :param options: optional replication args, e.g. continuous=True
        """
        data = {'source': source, 'target': target}
        data.update(options)
        data = self.resource.post('_replicate', data, headers={'Content-Type': 'application/json'})
        return data


class Database(object):
    """Representation of a database on a CouchDB server.

    >>> server = Server('http://localhost:5984/')
    >>> db = server.create('python-tests')

    New documents can be added to the database using the `create()` method:

    >>> doc_id = db.create({'type': 'Person', 'name': 'John Doe'})

    This class provides a dictionary-like interface to databases: documents are
    retrieved by their ID using item access

    >>> doc = db[doc_id]
    >>> doc                 #doctest: +ELLIPSIS
    <Document '...'@... {...}>

    Documents are represented as instances of the `Row` class, which is
    basically just a normal dictionary with the additional attributes ``id`` and
    ``rev``:

    >>> doc.id, doc.rev     #doctest: +ELLIPSIS
    ('...', ...)
    >>> doc['type']
    'Person'
    >>> doc['name']
    'John Doe'

    To update an existing document, you use item access, too:

    >>> doc['name'] = 'Mary Jane'
    >>> db[doc.id] = doc

    The `create()` method creates a document with a random ID generated by
    CouchDB (which is not recommended). If you want to explicitly specify the
    ID, you'd use item access just as with updating:

    >>> db['JohnDoe'] = {'type': 'person', 'name': 'John Doe'}

    >>> 'JohnDoe' in db
    True
    >>> len(db)
    2

    >>> del server['python-tests']
    """

    def __init__(self, uri, name=None):
        self.resource = Resource(uri)
        self._name = name

    def __repr__(self):
        return '<%s %r>' % (type(self).__name__, self.name)

    def __contains__(self, id):
        """Return whether the database contains a document with the specified
        ID.

        :param id: the document ID
        :return: `True` if a document with the ID exists, `False` otherwise
        """
        try:
            self.resource.head(id)
            return True
        except ResourceNotFound:
            return False

    def __iter__(self):
        """Return the IDs of all documents in the database."""
        return iter([item.id for item in self.view('_all_docs')])

    def __len__(self):
        """Return the number of documents in the database."""
        data = self.resource.get()
        return data['doc_count']

    def __nonzero__(self):
        """Return whether the database is available."""
        try:
            self.resource.head()
            return True
        except:
            return False

    def __delitem__(self, id):
        """Remove the document with the specified ID from the database.

        :param id: the document ID

        This method id broken. Use Document.delete() instead
        """
        if not id:
            raise ResourceNotFound("Document can't be empty, dude")
        data = self.resource.head(id)
        self.resource.delete(id, rev=data['etag'].strip('"'))

    def __getitem__(self, id):
        """Return the document with the specified ID.

        :param id: the document ID
        :return: a `Row` object representing the requested document
        :rtype: `Document`
        """

        if not id:
            raise ResourceNotFound("Document can't be empty, dude")
        
        #data = self.resource.get(id)
        #print 'getitem, id', id
        #print 'aaaaaaa', data, type(data)
        #d = Document(data)
        return Document(self.resource.get(id), _db = self)
        #return Document(data, _db  = self)

    def __setitem__(self, id, content):
        """Create or update a document with the specified ID.

        :param id: the document ID
        :param content: the document content; either a plain dictionary for
                        new documents, or a `Row` object for existing
                        documents
        """
        if not id:
            raise ResourceNotFound("Document can't be empty, dude")
        if '_db' in content:
            del(content['_db'])
        data = self.resource.put(id, content=content)
        content.update({'_id': data['id'], '_rev': data['rev'], '_db': self})

    @property
    def name(self):
        """The name of the database.

        Note that this may require a request to the server unless the name has
        already been cached by the `info()` method.

        :type: basestring
        """
        if self._name is None:
            self.info()
        return self._name

    def create(self, data):
        """Create a new document in the database with a random ID that is
        generated by the server.

        Note that it is generally better to avoid the `create()` method and
        instead generate document IDs on the client side. This is due to the
        fact that the underlying HTTP ``POST`` method is not idempotent, and
        an automatic retry due to a problem somewhere on the networking stack
        may cause multiple documents being created in the database.

        To avoid such problems you can generate a UUID on the client side.
        Python (since version 2.5) comes with a ``uuid`` module that can be
        used for this::

            from uuid import uuid4
            doc_id = uuid4().hex
            db[doc_id] = {'type': 'person', 'name': 'John Doe'}

        :param data: the data to store in the document
        :return: the ID of the created document
        :rtype: `unicode`
        """
        data = self.resource.post(content=data, headers={'Content-Type': 'application/json'})
        return data['id']

    def compact(self):
        """Compact the database.

        This will try to prune all revisions from the database.

        :return: a boolean to indicate whether the compaction was initiated
                 successfully
        :rtype: `bool`
        """
        data = self.resource.post('_compact', headers={'Content-Type': 'application/json'})
        return data['ok']

    def compact_view(self, name):
        """Compact view.
        Name must be provided without leading `_design/'
        :return: a boolean to indicate whether the compaction was initiated
                 successfully
        :rtype: `bool`
        """

        assert not name.startswith('_design/')
        
        resource = Resource('/'.join([self.resource.uri, '_compact']))
        return resource.post(name, headers={'Content-Type': 'application/json'})['ok']

    def copy(self, src, dest):
        """Copy the given document to create a new document.

        :param src: the ID of the document to copy, or a dictionary or
                    `Document` object representing the source document.
        :param dest: either the destination document ID as string, or a
                     dictionary or `Document` instance of the document that
                     should be overwritten.
        :return: the new revision of the destination document
        :rtype: `str`
        :since: 0.6
        """
        if not isinstance(src, basestring):
            if not isinstance(src, dict):
                if hasattr(src, 'items'):
                    src = src.items()
                else:
                    raise TypeError('expected dict or string, got %s' %
                                    type(src))
            src = src['_id']

        if not isinstance(dest, basestring):
            if not isinstance(dest, dict):
                if hasattr(dest, 'items'):
                    dest = dest.items()
                else:
                    raise TypeError('expected dict or string, got %s' %
                                    type(dest))
            if '_rev' in dest:
                dest = '%s?%s' % (unicode_quote(dest['_id']),
                                  unicode_urlencode({'rev': dest['_rev']}))
            else:
                dest = unicode_quote(dest['_id'])

        data = self.resource._request('COPY', src,
                                      headers={'Destination': dest})
        return data['rev']

    def delete(self, doc):
        """Delete the given document from the database.

        Use this method in preference over ``__del__`` to ensure you're
        deleting the revision that you had previously retrieved. In the case
        the document has been updated since it was retrieved, this method will
        raise a `ResourceConflict` exception.

        >>> server = Server('http://localhost:5984/')
        >>> db = server.create('python-tests')

        >>> doc = dict(type='Person', name='John Doe')
        >>> db['johndoe'] = doc
        >>> doc2 = db['johndoe']
        >>> doc2['age'] = 42
        >>> db['johndoe'] = doc2
        >>> db.delete(doc)
        Traceback (most recent call last):
          ...
        ResourceConflict: ('conflict', 'Document update conflict.')

        >>> del server['python-tests']

        :param doc: a dictionary or `Document` object holding the document data
        :raise ResourceConflict: if the document was updated in the database
        :since: 0.4.1
        """
        self.resource.delete(doc['_id'], rev=doc['_rev'])

    def get(self, id, default=None, **options):
        """Return the document with the specified ID.

        :param id: the document ID
        :param default: the default value to return when the document is not
                        found
        :return: a `Row` object representing the requested document, or `None`
                 if no document with the ID was found
        :rtype: `Document`
        """
        if id == None:
            raise ResourceNotFound('Document with Null id is impossible, dude')
        
        try:
            data = self.resource.get(id, **options)
        except ResourceNotFound:
            return default
        else:
            return Document(data, _db = self)

    def revisions(self, id, **options):
        """Return all available revisions of the given document.

        :param id: the document ID
        :return: an iterator over Document objects, each a different revision,
                 in reverse chronological order, if any were found
        """
        try:
            data = self.resource.get(id, revs=True)
        except ResourceNotFound:
            return

        startrev = data['_revisions']['start']
        for index, rev in enumerate(data['_revisions']['ids']):
            options['rev'] = '%d-%s' % (startrev - index, rev)
            revision = self.get(id, **options)
            if revision is None:
                return
            yield revision

    def info(self):
        """Return information about the database as a dictionary.

        The returned dictionary exactly corresponds to the JSON response to
        a ``GET`` request on the database URI.

        :return: a dictionary of database properties
        :rtype: ``dict``
        :since: 0.4
        """
        data = self.resource.get()
        self._name = data['db_name']
        return data

    def delete_attachment(self, doc, filename):
        """Delete the specified attachment.

        Note that the provided `doc` is required to have a ``_rev`` field.
        Thus, if the `doc` is based on a view row, the view row would need to
        include the ``_rev`` field.

        :param doc: the dictionary or `Document` object representing the
                    document that the attachment belongs to
        :param filename: the name of the attachment file
        :since: 0.4.1
        """
        data = self.resource(doc['_id']).delete(filename, rev=doc['_rev'])
        doc['_rev'] = data['rev']

    def get_attachment(self, id_or_doc, filename, default=None):
        """Return an attachment from the specified doc id and filename.

        :param id_or_doc: either a document ID or a dictionary or `Document`
                          object representing the document that the attachment
                          belongs to
        :param filename: the name of the attachment file
        :param default: default value to return when the document or attachment
                        is not found
        :return: the content of the attachment as a string, or the value of the
                 `default` argument if the attachment is not found
        :since: 0.4.1
        """
        if isinstance(id_or_doc, basestring):
            id = id_or_doc
        else:
            id = id_or_doc['_id']
        try:
            data = self.resource(id).get(filename)
            return data
        except ResourceNotFound:
            return default

    def put_attachment(self, doc, content, filename=None, content_type=None):
        """Create or replace an attachment.

        Note that the provided `doc` is required to have a ``_rev`` field. Thus,
        if the `doc` is based on a view row, the view row would need to include
        the ``_rev`` field.

        :param doc: the dictionary or `Document` object representing the
                    document that the attachment should be added to
        :param content: the content to upload, either a file-like object or
                        a string
        :param filename: the name of the attachment file; if omitted, this
                         function tries to get the filename from the file-like
                         object passed as the `content` argument value
        :param content_type: content type of the attachment; if omitted, the
                             MIME type is guessed based on the file name
                             extension
        :since: 0.4.1
        """
        if hasattr(content, 'read'):
            content = content.read()
        if filename is None:
            if hasattr(content, 'name'):
                filename = content.name
            else:
                raise ValueError('no filename specified for attachment')
        if content_type is None:
            content_type = ';'.join(filter(None, mimetypes.guess_type(filename)))

        data = self.resource(doc['_id']).put(filename, content=content,
                                                   headers={
            'Content-Type': str(content_type)
        }, rev=doc['_rev'])
        doc['_rev'] = data['rev']

    def query(self, map_fun, reduce_fun=None, language='javascript',
              wrapper=None, **options):
        """Execute an ad-hoc query (a "temp view") against the database.

        >>> server = Server('http://localhost:5984/')
        >>> db = server.create('python-tests')
        >>> db['johndoe'] = dict(type='Person', name='John Doe')
        >>> db['maryjane'] = dict(type='Person', name='Mary Jane')
        >>> db['gotham'] = dict(type='City', name='Gotham City')
        >>> map_fun = '''function(doc) {
        ...     if (doc.type == 'Person')
        ...         emit(doc.name, null);
        ... }'''
        >>> for row in db.query(map_fun):
        ...     print row.key
        John Doe
        Mary Jane

        >>> for row in db.query(map_fun, descending=True):
        ...     print row.key
        Mary Jane
        John Doe

        >>> for row in db.query(map_fun, key='John Doe'):
        ...     print row.key
        John Doe

        >>> del server['python-tests']

        :param map_fun: the code of the map function
        :param reduce_fun: the code of the reduce function (optional)
        :param language: the language of the functions, to determine which view
                         server to use
        :param wrapper: an optional callable that should be used to wrap the
                        result rows
        :param options: optional query string parameters
        :return: the view reults
        :rtype: `ViewResults`
        """
        return TemporaryView(uri(self.resource.uri, '_temp_view'), map_fun,
                             reduce_fun, language=language, wrapper=wrapper)(**options)

    def update(self, documents, **options):
        """Perform a bulk update or insertion of the given documents using a
        single HTTP request.

        >>> server = Server('http://localhost:5984/')
        >>> db = server.create('python-tests')
        >>> for doc in db.update([
        ...     Document(type='Person', name='John Doe'),
        ...     Document(type='Person', name='Mary Jane'),
        ...     Document(type='City', name='Gotham City')
        ... ]):
        ...     print repr(doc) #doctest: +ELLIPSIS
        (True, '...', '...')
        (True, '...', '...')
        (True, '...', '...')

        >>> del server['python-tests']

        The return value of this method is a list containing a tuple for every
        element in the `documents` sequence. Each tuple is of the form
        ``(success, docid, rev_or_exc)``, where ``success`` is a boolean
        indicating whether the update succeeded, ``docid`` is the ID of the
        document, and ``rev_or_exc`` is either the new document revision, or
        an exception instance (e.g. `ResourceConflict`) if the update failed.

        If an object in the documents list is not a dictionary, this method
        looks for an ``items()`` method that can be used to convert the object
        to a dictionary. Effectively this means you can also use this method
        with `schema.Document` objects.

        :param documents: a sequence of dictionaries or `Document` objects, or
                          objects providing a ``items()`` method that can be
                          used to convert them to a dictionary
        :return: an iterable over the resulting documents
        :rtype: ``list``

        :since: version 0.2
        """
        docs = []
        for doc in documents:
            if isinstance(doc, dict):
                if '_db' in doc:
                    del(doc['_db'])
                docs.append(doc)
            elif hasattr(doc, 'items'):
                docs.append(dict(doc.items()))
            else:
                raise TypeError('expected dict, got %s' % type(doc))

        content = options
        content.update(docs=docs)
        data = self.resource.post('_bulk_docs', content=content, headers={
            'Content-Type': 'application/json'
        })

        results = []
        for idx, result in enumerate(data):
            if 'error' in result:
                if result['error'] == 'conflict':
                    exc_type = ResourceConflict
                else:
                    # XXX: Any other error types mappable to exceptions here?
                    exc_type = ServerError
                results.append((False, result['id'],
                                exc_type(result['reason'])))
            else:
                doc = documents[idx]
                if isinstance(doc, dict): # XXX: Is this a good idea??
                    doc.update({'_id': result['id'], '_rev': result['rev']})
                results.append((True, result['id'], result['rev']))

        return results

    def view(self, name, wrapper=None, **options):
        """Execute a predefined view.

        >>> server = Server('http://localhost:5984/')
        >>> db = server.create('python-tests')
        >>> db['gotham'] = dict(type='City', name='Gotham City')

        >>> for row in db.view('_all_docs'):
        ...     print row.id
        gotham

        >>> del server['python-tests']

        :param name: the name of the view; for custom views, use the format
                     ``design_docid/viewname``, that is, the document ID of the
                     design document and the name of the view, separated by a
                     slash
        :param wrapper: an optional callable that should be used to wrap the
                        result rows
        :param options: optional query string parameters
        :return: the view results
        :rtype: `ViewResults`
        """
        if not name.startswith('_'):
            design, name = name.split('/', 1)
            name = '/'.join(['_design', design, '_view', name])
        return PermanentView(uri(self.resource.uri, *name.split('/')), name,
                             wrapper=wrapper)(**options)

    
    def view_cleanup(self):
        """Cleanup database views (emits POST /db/_view_cleanup request)"""
        return self.resource.post('_view_cleanup', headers={'Content-Type': 'application/json'})


    def design_info(self, name):
        assert name.startswith('_design/')
        resource = Resource('/'.join([self.resource.uri, name, '_info']))
        return resource.get()
    
class Document(dict):
    """Representation of a document in the database.

    This is basically just a dictionary with some helper functions and properties (see below).
    You may work with this object in dict-style or attribute-style
    
    >>> from couchdbcurl.client import Document
    >>> doc = Document()
    >>> doc['some_field'] = 'this is value'
    >>> doc.other_field = 'another value'
    >>> dict(doc)
    {'other_field': 'another value', 'some_field': 'this is value'}
    >>> doc.some_field
    'this is value'
    >>> doc['other_field']
    'another value'

    You may check wether Document is new or existing simply by testing it id property. So, you may use constructions like::
    
      if doc.id:
          doc.save()
      else:
          doc.create('some_id_prefix')
    
    """

    def __init__(self, *args, **kwargs):
        if '_db' in kwargs:
            self._db = kwargs['_db']
            del(kwargs['_db'])
        dict.__init__(self, *args, **kwargs)
    
    def __repr__(self):
        return '<%s %s@%s %r>' % (type(self).__name__, self.get('_id', '-'), self.get('_rev', '-'),
                                  dict([(k,v) for k,v in self.items()
                                        if k not in ('_id', '_rev')]))
    
    ## def __nonzero__(self):
    ##     return '_id' in self and bool(self.id)
        
    @property
    def id(self):
        """The document ID.

        :type: basestring or None for new documents
        """
        return self.get('_id')

    @property
    def rev(self):
        """The document revision.

        :type: basestring
        """
        return self.get('_rev')

    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            raise AttributeError(u'Field %s is undefined in this document' % name)

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        del(self[name])

    def save(self, db = None):
        """Save document. Document will be saved to database ``db`` or ``document._db``"""
        
        db = db or getattr(self, '_db', None)
        if db:
            db[self.id] = self
        else:
            raise Exception('Can\'t save document - target database is undefined')
        
    def delete(self, db = None):
        """Delete document"""
        db = db or getattr(self, '_db', None)
        if db:
            db.delete(self)
        else:
            raise Exception('Can\'t delete document - target database is undefined')

    def create(self, id, suffix_length = 12, max_retry = 100, db = None, force_random_suffix=False):
        """Conflict-safe document creator.
        Document id will be '<id>' or '<id><random suffix>' if '<id>' already exists.
        
        id - id prefix.
        suffix_length - suffix length
        max_retry - upper retry limit
        db - database to create document in
        """
        id_string = '%s%s'
        db = db or getattr(self, '_db', None)
        if db:
            rand = ''
            if force_random_suffix:
                rand = '_' + hashlib.sha1(str(random.random())).hexdigest()[:suffix_length]
                
            doc_id = id_string % (id, rand)
            
            while True:
                
                try:
                    db[doc_id] = self
                    break
                except ResourceConflict:
                    pass

                max_retry -= 1
                if max_retry < 0:
                    raise Exception("Retry-limit reached during document generation")
                
                rand = hashlib.sha1(str(random.random())).hexdigest()[:suffix_length]
                doc_id = id_string % (id, '_%s' % rand)
            
        else:
            raise Exception('Can\'t create document - target database is undefined')
        

    def get_attachment(self, name):
        """Shortcut to Database.get_attachment()"""
        return self._db.get_attachment(self, name)
        
    def put_attachment(self, file_object, name, content_type = None):
        """Shortcut to Database.put_attachment()"""
        return self._db.put_attachment(self, file_object, name, content_type)
        
    def delete_attachment(self, name):
        """Shortcut to Database.delete_attachment()"""
        self._db.delete_attachment(self, name)
    
    def reload(self, db = None):
        """Checks documents revision and reloads if necessary"""
        db = db or getattr(self, '_db', None)
        rev = db.resource.head(self.id)['etag']
        
        if rev != self.rev:
            doc = db[self.id]
            for key in self.keys():
                del(self[key])
            self.update(doc)
            return True
        else:
            return False
        
class View(object):
    """Abstract representation of a view or query."""

    def __init__(self, uri, wrapper=None):
        self.resource = Resource(uri)
        self.wrapper = wrapper

    def __call__(self, **options):
        return ViewResults(self, options)

    def __iter__(self):
        return self()

    def _encode_options(self, options):
        retval = {}
        for name, value in options.items():
            if name in ('key', 'startkey', 'endkey') \
                    or not isinstance(value, basestring):
                value = json.dumps(value)
            retval[name] = value
        return retval

    def _exec(self, options):
        raise NotImplementedError


class PermanentView(View):
    """Representation of a permanent view on the server."""

    def __init__(self, uri, name, wrapper=None):
        View.__init__(self, uri, wrapper=wrapper)
        self.name = name

    def __repr__(self):
        return '<%s %r>' % (type(self).__name__, self.name)

    def _exec(self, options):
        if 'keys' in options:
            options = options.copy()
            keys = {'keys': options.pop('keys')}
            data = self.resource.post(content=keys, headers={
                'Content-Type': 'application/json'
            },
            **self._encode_options(options))
        else:
            data = self.resource.get(**self._encode_options(options))
        return data


class TemporaryView(View):
    """Representation of a temporary view."""

    def __init__(self, uri, map_fun, reduce_fun=None,
                 language='javascript', wrapper=None):
        View.__init__(self, uri, wrapper=wrapper)
        if isinstance(map_fun, FunctionType):
            map_fun = getsource(map_fun).rstrip('\n\r')
        self.map_fun = dedent(map_fun.lstrip('\n\r'))
        if isinstance(reduce_fun, FunctionType):
            reduce_fun = getsource(reduce_fun).rstrip('\n\r')
        if reduce_fun:
            reduce_fun = dedent(reduce_fun.lstrip('\n\r'))
        self.reduce_fun = reduce_fun
        self.language = language

    def __repr__(self):
        return '<%s %r %r>' % (type(self).__name__, self.map_fun,
                               self.reduce_fun)

    def _exec(self, options):
        body = {'map': self.map_fun, 'language': self.language}
        if self.reduce_fun:
            body['reduce'] = self.reduce_fun
        if 'keys' in options:
            options = options.copy()
            body['keys'] = options.pop('keys')
        content = json.dumps(body).encode('utf-8')
        data = self.resource.post(content=content, headers={
            'Content-Type': 'application/json'
        }, **self._encode_options(options))
        return data


class ViewResults(object):
    """Representation of a parameterized view (either permanent or temporary)
    and the results it produces.

    This class allows the specification of ``key``, ``startkey``, and
    ``endkey`` options using Python slice notation.

    >>> server = Server('http://localhost:5984/')
    >>> db = server.create('python-tests')
    >>> db['johndoe'] = dict(type='Person', name='John Doe')
    >>> db['maryjane'] = dict(type='Person', name='Mary Jane')
    >>> db['gotham'] = dict(type='City', name='Gotham City')
    >>> map_fun = '''function(doc) {
    ...     emit([doc.type, doc.name], doc.name);
    ... }'''
    >>> results = db.query(map_fun)

    At this point, the view has not actually been accessed yet. It is accessed
    as soon as it is iterated over, its length is requested, or one of its
    `rows`, `total_rows`, or `offset` properties are accessed:

    >>> len(results)
    3

    You can use slices to apply ``startkey`` and/or ``endkey`` options to the
    view:

    >>> people = results[['Person']:['Person','ZZZZ']]
    >>> for person in people:
    ...     print person.value
    John Doe
    Mary Jane
    >>> people.total_rows, people.offset
    (3, 1)

    Use plain indexed notation (without a slice) to apply the ``key`` option.
    Note that as CouchDB makes no claim that keys are unique in a view, this
    can still return multiple rows:

    >>> list(results[['City', 'Gotham City']])
    [<Row id='gotham', key=['City', 'Gotham City'], value='Gotham City'>]

    >>> del server['python-tests']
    """

    def __init__(self, view, options):
        self.view = view
        self.options = options
        self._rows = self._total_rows = self._offset = None

    def __repr__(self):
        return '<%s %r %r>' % (type(self).__name__, self.view, self.options)

    def __getitem__(self, key):
        options = self.options.copy()
        if type(key) is slice:
            if key.start is not None:
                options['startkey'] = key.start
            if key.stop is not None:
                options['endkey'] = key.stop
            return ViewResults(self.view, options)
        else:
            options['key'] = key
            return ViewResults(self.view, options)

    def __iter__(self):
        wrapper = self.view.wrapper
        for row in self.rows:
            if wrapper is not None:
                yield wrapper(row)
            else:
                yield row

    def __len__(self):
        return len(self.rows)

    def _fetch(self):
        data = self.view._exec(self.options)
        self._rows = [Row(row) for row in data['rows'] if not row.get('error')]
        self._total_rows = data.get('total_rows')
        self._offset = data.get('offset', 0)

    @property
    def rows(self):
        """The list of rows returned by the view.

        :type: `list`
        """
        if self._rows is None:
            self._fetch()
        return self._rows

    @property
    def total_rows(self):
        """The total number of rows in this view.

        This value is `None` for reduce views.

        :type: `int` or ``NoneType`` for reduce views
        """
        if self._rows is None:
            self._fetch()
        return self._total_rows

    @property
    def offset(self):
        """The offset of the results from the first row in the view.

        This value is 0 for reduce views.

        :type: `int`
        """
        if self._rows is None:
            self._fetch()
        return self._offset


class Row(dict):
    """Representation of a row as returned by database views."""

    def __repr__(self):
        if self.id is None:
            return '<%s key=%r, value=%r>' % (type(self).__name__, self.key,
                                              self.value)
        return '<%s id=%r, key=%r, value=%r>' % (type(self).__name__, self.id,
                                                 self.key, self.value)

    @property
    def id(self):
        """The associated Document ID if it exists. Returns `None` when it
        doesn't (reduce results).
        """
        return self.get('id')

    @property
    def key(self):
        """The associated key."""
        return self['key']

    @property
    def value(self):
        """The associated value."""
        return self['value']

    @property
    def doc(self):
        """The associated document for the row. This is only present when the
        view was accessed with ``include_docs=True`` as a query parameter,
        otherwise this property will be `None`.
        """
        doc = self.get('doc')
        if doc:
            return Document(doc)


# Internals


class Resource(object):

    def __init__(self, uri):
        #self.curl = pycurl.Curl()
        self.uri = uri

    def __del__(self):
        #self.curl.close()
        pass

    # temporary commented out. Is there anyone uses it?
    def __call__(self, path):
        return type(self)(uri(self.uri, path))

    def delete(self, path=None, headers=None, **params):
        return self._request('DELETE', path, headers=headers, **params)

    def get(self, path=None, headers=None, **params):
        return self._request('GET', path, headers=headers, **params)

    def head(self, path=None, headers=None, **params):
        return self._request('HEAD', path, headers=headers, **params)

    def post(self, path=None, content=None, headers=None, **params):
        return self._request('POST', path, content=content, headers=headers,
                             **params)

    def put(self, path=None, content=None, headers=None, **params):
        return self._request('PUT', path, content=content, headers=headers,
                             **params)

    def _request(self, method, path=None, content=None, headers=None,
                 **params):
        def _make_request(curl, path, params, body, retry = 1):
            
            stringbuf = StringIO()
            
            if method in ("PUT", "POST"):
                if method == "POST":
                    curl.setopt(pycurl.POST, 1)
                else:
                    curl.setopt(pycurl.CUSTOMREQUEST, method)
                if body:
                    curl.setopt(pycurl.POSTFIELDS, body)
            elif method in ("DELETE", "HEAD"):
                curl.setopt(pycurl.CUSTOMREQUEST, method)
                if method == 'HEAD':
                    curl.setopt(pycurl.NOBODY, True)
                    curl.setopt(pycurl.HEADER, True)
            
            try:
                curl.setopt(pycurl.URL, uri(self.uri, path, **params).encode('utf-8'))
                params = urlparse(self.uri)
                if params.username and params.password:
                    curl.setopt(pycurl.USERPWD, "%s:%s" % (params.username, params.password))
                curl.setopt(pycurl.WRITEFUNCTION, stringbuf.write)
                curl.setopt(pycurl.FOLLOWLOCATION, 1)
                curl.setopt(pycurl.MAXREDIRS, 5)
                #curl.setopt(pycurl.FORBID_REUSE, 0)
                curl.perform()
                stringbuf.seek(0)
                return stringbuf.read()
            except socket.error, e:
                if retry > 0 and e.args[0] == 54: # reset by peer
                    return _make_request(retry - 1)
                raise
        

        from couchdbcurl import __version__
        curl = pycurl.Curl()
        
        ## if method in ("PUT", "POST"):
        ##     if method == "POST":
        ##         self.curl.setopt(pycurl.POST, 1)
        ##     else:
        ##         curl.setopt(pycurl.CUSTOMREQUEST, method)
        ##         curl.setopt(pycurl.POSTFIELDS, body)
        ## elif method in ("DELETE", "HEAD"):
        ##     curl.setopt(pycurl.CUSTOMREQUEST, method)
        ##     if method == 'HEAD':
        ##         curl.setopt(pycurl.NOBODY, True)
        
        headers = headers or {}
        headers.setdefault('Accept', 'application/json')
        headers["User-Agent"] = "couchdb-python-curl %s" % __version__
  
       
        #curl.setopt(pycurl.HTTPHEADER, headers)
        #headers.setdefault('User-Agent', 'couchdb-python %s' % __version__)
        #curl.setopt(pycurl.HTTPHEADER, [])
        body = None
        if content is not None:
            if not isinstance(content, basestring):
                body = json.dumps(content).encode('utf-8')
                #headers.setdefault('Content-Type', 'application/json')
                #curl.setopt(pycurl.HTTPHEADER, ["Content-Type: application/json"])
            else:
                body = content
            headers.setdefault('Content-Length', str(len(body)))
            #curl.setopt(pycurl.HTTPHEADER, ["Content-Length: %s" % str(len(body))])

        curl.setopt(pycurl.HTTPHEADER, ['%s: %s' % (key, headers[key]) for key in headers])
        data = _make_request(curl, path, params, body)
        status_code = curl.getinfo(pycurl.HTTP_CODE)
        #status_code = int(resp.status)

        
        #if data and resp.get('content-type') == 'application/json':
        if data and curl.getinfo(pycurl.CONTENT_TYPE) == 'application/json':
            try:
                data = json.loads(data)
            except ValueError:
                pass

        if method == 'HEAD':
            data = dict([(key.lower(), value) for key, value in [i.split(': ', 1) for i in data.splitlines()[1:] if i]])
            if 'etag' in data:
                data['etag'] = json.loads(data['etag'])
        
        
        if status_code >= 400:
            if type(data) is dict:
                error = (data.get('error'), data.get('reason'))
            else:
                error = data
            if status_code == 404:
                raise ResourceNotFound(error)
            elif status_code == 409:
                raise ResourceConflict(error)
            elif status_code == 412:
                raise PreconditionFailed(error)
            else:
                raise ServerError((status_code, error))

        #return resp, data
        curl.close()
        
        return data


def uri(base, *path, **query):
    """Assemble a uri based on a base, any number of path segments, and query
    string parameters.

    >>> uri('http://example.org', '_all_dbs')
    'http://example.org/_all_dbs'

    A trailing slash on the uri base is handled gracefully:

    >>> uri('http://example.org/', '_all_dbs')
    'http://example.org/_all_dbs'

    And multiple positional arguments become path parts:

    >>> uri('http://example.org/', 'foo', 'bar')
    'http://example.org/foo/bar'

    All slashes within a path part are escaped:

    >>> uri('http://example.org/', 'foo/bar')
    'http://example.org/foo%2Fbar'
    >>> uri('http://example.org/', 'foo', '/bar/')
    'http://example.org/foo/%2Fbar%2F'
    """
    if base and base.endswith('/'):
        base = base[:-1]
    retval = [base]

    # build the path
    path = '/'.join([''] + [unicode_quote(s) for s in path if s is not None])
    if path:
        retval.append(path)

    # build the query string
    params = []
    for name, value in query.items():
        if type(value) in (list, tuple):
            params.extend([(name, i) for i in value if i is not None])
        elif value is not None:
            if value is True:
                value = 'true'
            elif value is False:
                value = 'false'
            params.append((name, value))
    if params:
        retval.extend(['?', unicode_urlencode(params)])

    return ''.join(retval)


def unicode_quote(string, safe=''):
    if isinstance(string, unicode):
        string = string.encode('utf-8')
    return quote(string, safe)


def unicode_urlencode(data):
    if isinstance(data, dict):
        data = data.items()
    params = []
    for name, value in data:
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        params.append((name, value))
    return urlencode(params)


VALID_DB_NAME = re.compile(r'^[_a-z][a-z0-9_$()+-/]*$')
def validate_dbname(name):
    if not VALID_DB_NAME.match(name):
        raise ValueError('Invalid database name')
    return name
