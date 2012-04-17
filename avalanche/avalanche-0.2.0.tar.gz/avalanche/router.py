"""
A request routing system

based on webapp2 with the following differences:
  * supports only class-based handlers as endpoint
  * endpoint is never used by routing system (just stored as route data)
  * removed adpaters and dispatchers configuration
  * removed support for specifing handlers (endpoints) as string
  * many other other internal API and implementation changes

  original webapp2 license:
    :copyright: 2011 by tipfy.org.
    :license: Apache Sotware License, see LICENSE.webapp2 for details.

"""

import re
import urllib
import urlparse
from collections import namedtuple


def to_utf8(value):
    """Encodes a unicode value to UTF-8 if not yet encoded."""
    return value.encode('utf-8') if isinstance(value, unicode) else value


class Route(object):
    """Route for URL paths

        A route template to match against the request path. A template
        can have variables enclosed by ``<>`` that define a name, a
        regular expression or both. Examples:

          =================  ==================================
          Format             Example
          =================  ==================================
          ``<name>``         ``'/blog/<year>/<month>'``
          ``<:regex>``       ``'/blog/<:\d{4}>/<:\d{2}>'``
          ``<name:regex>``   ``'/blog/<year:\d{4}>/<month:\d{2}>'``
          =================  ==================================

        The same template can mix parts with name, regular expression or
        both.

        If the name is set, the value of the matched regular expression
        is passed as keyword argument to the handler. Otherwise it is
        passed as positional argument.

        If only the name is set, it will match anything except a slash.
        So these routes are equivalent::

            Route('/<user_id>/settings', handler=SettingsHandler,
                  name='user-settings')
            Route('/<user_id:[^/]+>/settings', handler=SettingsHandler,
                  name='user-settings')

     """

    # Regex for route definitions.
    _PATH_ARG_RE = re.compile(r"""
      \<               # The exact character "<"
      ([a-zA-Z_]\w*)?  # The optional variable name
      (?:\:([^\>]*))?  # The optional :regex part
      \>               # The exact character ">"
    """, re.VERBOSE)
    _DEFAULT_REGEX = '[^/]+'


    def __init__(self, template, endpoint, name=None):
        """
        :param template:
            template string
        :param endpoint:
            reference to request handler (or whatever)

        :param name:
            (string) route name
        """
        self.template = template
        self.endpoint = endpoint
        self.name = name

        # attributes from template (lazily) calculated (by _parse_template)
        self._regex = None # compiled regex for template
        self._reverse_template = None # used to build urls (uses str.format)
        self._variables = set() # argument names from template


    def __repr__(self):
        name = self.__class__.__name__
        return ('<%s(%r, %r)>' % (name, self.template, self.endpoint))


    def _parse_template(self):
        """parse template and create regex, reverse_template, ...

         * posistional args will are added in the regular expression
           with name __%02d__ % position
        """
        self._reverse_template = ''
        pattern = '' # str pattern for regex (to be compiled)
        last = 0 # keeps track of last position processed from template string
        pos_args_count = 0
        for match in self._PATH_ARG_RE.finditer(self.template):
            # part is a string segment that does not belong to any argument
            part = self.template[last:match.start()]
            name = match.group(1)
            regex = match.group(2) or self._DEFAULT_REGEX
            last = match.end()

            self._reverse_template += part
            if not name: # positional argument
                # hope the there are no more than 99 positional args :)
                name = '__%02d__' % pos_args_count
                self._reverse_template += '{%s}' % pos_args_count
                pos_args_count += 1
            else: # named argument
                self._variables.add(name)
                self._reverse_template += '{%s}' % name

            pattern += '%s(?P<%s>%s)' % (re.escape(part), name, regex)

        # add remaining part of the template string
        part = self.template[last:]
        self._reverse_template += part
        pattern += re.escape(part)

        # save compiled regex
        self._regex = re.compile('^%s$' % pattern)


    def match(self, request):
        """Check if request matches this route

        :param request:
            A request to be checked if matches the template
        :returns:
            A tuple ``(args, kwargs)`` if route matched, or None.
        """
        if self._regex is None:
            self._parse_template()

        match = self._regex.match(urllib.unquote(request.path))
        if match:
            kwargs = match.groupdict()
            if kwargs:
                args = tuple(kwargs.pop(key) for key in sorted(kwargs.keys()) \
                                 if key.startswith('__') and key.endswith('__'))
            else:
                args = ()
            return args, kwargs


    def build(self, *args, **kwargs):
        """build path for this route.

        :param args:
            Tuple of positional arguments to build the URI.
        :param kwargs:
            Dictionary of keyword arguments to build the URI.
        :returns:
            (str) path
        """
        if self._regex is None:
            self._parse_template()

        # get other parts of URI
        scheme = kwargs.pop('_scheme', '') # http://
        netloc = kwargs.pop('_netloc', '') # www.example.com
        fragment = urllib.quote(to_utf8(kwargs.pop('_fragment', ''))) # #anchor

        # extract keywords arguments that belongs to path
        path_kwargs = {}
        for name in self._variables:
            value = kwargs.pop(name, None)
            if value is None:
                raise Exception('Missing argument "%s" to build URI.' % name)
            path_kwargs[name] = value

        _path = self._reverse_template.format(*args, **path_kwargs)
        path = urllib.quote(to_utf8(_path))
        query_list = [(k, to_utf8(v)) for k, v in sorted(kwargs.iteritems())]
        query = urllib.urlencode(query_list)

        return urlparse.urlunsplit((scheme, netloc, path, query, fragment))


# result from Router.match
MatchResult = namedtuple('MatchResult', ('route', 'args', 'kwargs'))

class Router(object):
    """A URI router used to match and build URIs.
    """

    def __init__(self, *routes):
        """Initializes the router.

        :param routes:
            A sequence of (:class:`Route`, :str:name) instances
        """
        self.routes = []
        #: All routes that can be built (must have a name to be build)
        self.by_name = {}

        for route in routes:
            self.add(route)


    def add(self, route):
        """Adds a route to this router.

        :param route:
            A :class:`Route` instance or, for simple routes, a tuple
            ``(regex, handler)``.
        """
        self.routes.append(route)
        if route.name:
            self.by_name[route.name] = route


    def match(self, request):
        """Matches all routes against a value

        :returns:
            MatchResult or None if no route is matched
        """
        for route in self.routes:
            match = route.match(request)
            if match:
                return MatchResult(route, *match)


    def build(self, _name, *args, **kwargs):
        """Returns a URI for a named :class:`Route`.

        :param _name:
            The route name.
        :param args:
            Tuple of positional arguments to build the URI.
            All positional variables defined in the route must be passed.
            Extra arguments are ignored.
        :param kwargs:
            Dictionary of keyword arguments to build the URI.
            All variables values must be passed.
            Extra keywords are appended as a query string.

            A few keywords have special meaning:

            - **_scheme**: URI scheme, e.g., `http` or `https`. If defined,
              an absolute URI is always returned.
            - **_netloc**: Network location, e.g., `www.google.com`. If
              defined, an absolute URI is always returned.
            - **_fragment**: If set, appends a fragment (or "anchor") to the
              generated URI.
        :returns:
            (string) An absolute or relative URI.
        """
        route = self.by_name.get(_name)
        if route is None:
            raise Exception("Route named '%s' is not defined." % _name)

        return route.build(*args, **kwargs)
