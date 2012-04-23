'''
    rauth.oauth
    -----------

    A module providing various OAuth related containers.
'''

import base64
import hmac

from hashlib import sha1
from urlparse import parse_qsl, urlsplit, urlunsplit
from urllib import quote, urlencode


class OAuthObject(object):
    '''A base class for OAuth token objects.'''
    verifier = None

    def __init__(self, key, secret):
        self.key = key
        self.secret = secret


class Consumer(OAuthObject):
    '''The consumer token object.'''
    pass


class Token(OAuthObject):
    '''The access token object.'''
    pass


class SignatureMethod(object):
    '''A base class for signature methods providing a set of common methods.'''
    def _encode_utf8(self, s):
        if isinstance(s, unicode):
            return s.encode('utf-8')
        return unicode(s, 'utf-8').encode('utf-8')

    def _escape(self, s):
        '''Escapes a string, ensuring it is encoded as a UTF-8 octet.

        :param s: A string to be encoded.
        '''
        return quote(self._encode_utf8(s), safe='~')

    def _remove_qs(self, url):
        '''Removes a query string from a URL before signing.

        :param url: The URL to strip.
        '''
        # split 'em up
        scheme, netloc, path, query, fragment = urlsplit(url)

        # the query string can't be sign as per the spec, kill it
        query = ''

        # and return our query-string-less URL!
        return urlunsplit((scheme, netloc, path, query, fragment))

    def _normalize_request_parameters(self, request):
        '''The OAuth 1.0/a specs indicate that parameter and body data must be
        normalized. The specifics of this operation are detailed in the
        respective specs.

        Here we have to ensure that parameter and body data is properly
        handled. This means that the case of params or data being strings is
        taken care of.

        Essentially this is achieved by checking that `request.data` and
        `request.params` are not strings. This being the case we can then
        construct a unified list of tuples from them.

        Otherwise we build a series intermediary lists of tuples depending on
        the type of `request.params` and `request.data`.

        :param request: The request object that will be normalized.
        '''
        if type(request.params) != str and type(request.data) != str:
            # if neither params nor data are a string, i.e. both are dicts

            # we concatenate the respective dicts
            params_and_data = \
                    dict(request.params.items() + request.data.items())

            normalized = []
            for k, v in params_and_data.items():
                normalized += [(k, v)]
        elif type(request.params) == str and type(request.data) == str:
            # if both params and data are strings
            params = parse_qsl(request.params)
            data = parse_qsl(request.data)
            normalized = params + data
        elif type(request.params) == str:
            # parse the string into a list of tuples
            normalized = parse_qsl(request.params)

            # extract any data
            for k, v in request.data.items():
                normalized += [(k, v)]
        elif type(request.data) == str:
            # and we do the same if data
            normalized = parse_qsl(request.data)

            # extract any params
            for k, v in request.params.items():
                normalized += [(k, v)]

        # extract values from our list of tuples
        all_normalized = []
        for t in normalized:
            k, v = t

            # save key/value pairs to the request and our list
            request.params_and_data[k] = v
            all_normalized += [(k, v)]

        # add in the params from data_and_params for signing
        for k, v in request.params_and_data.items():
            if (k, v) in all_normalized:
                continue
            all_normalized += [(k, v)]

        # sort the params as per the OAuth 1.0/a spec
        all_normalized.sort()

        # finally encode the params as a string
        return urlencode(all_normalized)


class HmacSha1Signature(SignatureMethod):
    '''HMAC-SHA1 Signature Method.

    This is a signature method, as per the OAuth 1.0/a and 2.0 specs. As the
    name might suggest, this method signs parameters with HMAC using SHA1.
    '''
    NAME = 'HMAC-SHA1'

    def sign(self, request, consumer, token=None):
        '''Sign request parameters.

        :param request: The request to sign.
        :param consumer: The consumer token object.
        :param token: The access token object.
        '''

        # the necessary parameters we'll sign
        url = self._remove_qs(request.url)
        params_and_data = self._normalize_request_parameters(request)
        parameters = [self._escape(request.method),
                      self._escape(url),
                      self._escape(params_and_data)]

        # set our key
        key = self._escape(consumer.secret) + '&'
        if token is not None:
            key += self._escape(token.secret)

        # build a Signature Base String
        signature_base_string = '&'.join(parameters)

        # hash the string with HMAC-SHA1
        hashed = hmac.new(key, signature_base_string, sha1)

        # add the signature to the request
        request.params_and_data['oauth_signature'] = \
                base64.b64encode(hashed.digest())


class RsaSha1Signature(SignatureMethod):
    '''RSA-SHA1 Signature Method. (Not implemented)'''
    NAME = 'RSA-SHA1'

    def __init__(self):
        raise NotImplementedError


class PlaintextSignature(SignatureMethod):
    '''PLAINTEXT Signature Method. (Not implemented)'''
    NAME = 'PLAINTEXT'

    def __init__(self):
        raise NotImplementedError
