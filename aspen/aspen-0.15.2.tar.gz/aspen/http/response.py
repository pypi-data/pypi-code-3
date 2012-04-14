import re

try:                # 2
    from Cookie import CookieError, SimpleCookie
except ImportError: # 3
    from http.cookies import CookieError, SimpleCookie

from aspen.http import status_strings
from aspen.http.baseheaders import BaseHeaders as Headers


class CloseWrapper(object):
    """Conform to WSGI's facility for running code *after* a response is sent.
    """

    def __init__(self, request, body):
        self.request = request
        self.body = body

    def __iter__(self):
        return iter(self.body)

    def close(self):
        socket = getattr(self.request, "socket", None)
        if socket is not None:
            pass
            # implement some socket closing logic here
            #self.request.socket.close()


# Define a charset name filter.
# =============================
# "The character set names may be up to 40 characters taken from the
#  printable characters of US-ASCII."
#  (http://www.iana.org/assignments/character-sets)
#
# We're going to be slightly more restrictive. Instead of allowing all
# printable characters, which include whitespace and newlines, we're going to
# only allow punctuation that is actually in use in the current IANA list.

charset_re = re.compile("^[A-Za-z0-9:_()+.-]{1,40}$")


class Response(Exception):
    """Represent an HTTP Response message.
    """

    request = None

    def __init__(self, code=200, body='', headers=None, charset="UTF-8"):
        """Takes an int, a string, a dict, and a basestring.

            - code      an HTTP response code, e.g., 404
            - body      the message body as a string
            - headers   a Headers instance
            - charset   string that will be set in the Content-Type in the future at some point but not now

        Code is first because when you're raising your own Responses, they're
        usually error conditions. Body is second because one more often wants
        to specify a body without headers, than a header without a body.

        """
        if not isinstance(code, int):
            raise TypeError("'code' must be an integer")
        elif not isinstance(body, str) and not hasattr(body, '__iter__'):
            raise TypeError("'body' must be a bytestring or iterable of "
                            "bytestrings")
        elif headers is not None and not isinstance(headers, (dict, list)):
            raise TypeError("'headers' must be a dictionary or a list of " +
                            "2-tuples")
        elif charset_re.match(charset) is None:
            raise TypeError("'charset' must match " + charset_re.pattern)

        Exception.__init__(self)
        self.code = code
        self.body = body
        self.headers = Headers('')
        self.charset = charset
        if headers:
            if isinstance(headers, dict):
                headers = headers.items()
            for k, v in headers:
                self.headers[k] = v
        self.cookie = SimpleCookie()
        try:
            self.cookie.load(self.headers.get('Cookie', ''))
        except CookieError:
            pass

    def __call__(self, environ, start_response):
        wsgi_status = str(self)
        for morsel in self.cookie.values():
            self.headers['Set-Cookie'] = morsel.OutputString()
        wsgi_headers = []
        for k, vals in self.headers.iteritems():
            for v in vals:
                wsgi_headers.append((k, v))
        start_response(wsgi_status, wsgi_headers)
        body = self.body
        if isinstance(body, basestring):
            body = [body]
        return CloseWrapper(self.request, body)

    def __repr__(self):
        return "<Response: %s>" % str(self)

    def __str__(self):
        return "%d %s" % (self.code, self._status())

    def _status(self):
        return status_strings.get(self.code, 'Unknown HTTP status')

    def _to_http(self, version):
        """Given a version string like 1.1, return an HTTP message, a string.
        """
        status_line = "HTTP/%s" % version
        headers = self.headers.raw
        body = self.body
        if self.headers.get('Content-Type', '').startswith('text/'):
            body = body.replace('\n', '\r\n')
            body = body.replace('\r\r', '\r')
        return '\r\n'.join([status_line, headers, '', body])

