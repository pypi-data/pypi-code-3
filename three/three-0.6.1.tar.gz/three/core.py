"""
A new Python wrapper for interacting with the Open311 API.
"""

import os
import re
from collections import defaultdict
from datetime import date
from itertools import ifilter

import requests
from relaxml import xml
import simplejson as json


class Three(object):
    """The main class for interacting with the Open311 API."""

    def __init__(self, endpoint=None, **kwargs):
        keywords = defaultdict(str)
        keywords.update(kwargs)
        if endpoint:
            endpoint = self._configure_endpoint(endpoint)
            keywords['endpoint'] = endpoint
        elif 'OPEN311_CITY_INFO' in os.environ:
            info = json.loads(os.environ['OPEN311_CITY_INFO'])
            endpoint = info['endpoint']
            endpoint = self._configure_endpoint(endpoint)
            keywords.update(info)
            keywords['endpoint'] = endpoint
        self._keywords = keywords
        self.configure()

    def _global_api_key(self):
        """
        If a global Open311 API key is available as an environment variable,
        then it will be used when querying.
        """
        if 'OPEN311_API_KEY' in os.environ:
            api_key = os.environ['OPEN311_API_KEY']
        else:
            api_key = ''
        return api_key

    def configure(self, endpoint=None, **kwargs):
        """Configure a previously initialized instance of the class."""
        if endpoint:
            kwargs['endpoint'] = endpoint
        keywords = self._keywords.copy()
        keywords.update(kwargs)
        if 'endpoint' in kwargs:
            # Then we need to correctly format the endpoint.
            endpoint = kwargs['endpoint']
            keywords['endpoint'] = self._configure_endpoint(endpoint)
        self.api_key = keywords['api_key'] or self._global_api_key()
        self.endpoint = keywords['endpoint']
        self.format = keywords['format'] or 'json'
        self.jurisdiction = keywords['jurisdiction']
        self.proxy = keywords['proxy']

    def _configure_endpoint(self, endpoint):
        """Configure the endpoint with a schema and end slash."""
        if not endpoint.startswith('http'):
            endpoint = 'https://' + endpoint
        if not endpoint.endswith('/'):
            endpoint += '/'
        return endpoint

    def reset(self):
        """Reset the class back to the original keywords and values."""
        self.configure()

    def _create_path(self, *args):
        """Create URL path for endpoint and args."""
        args = ifilter(None, args)
        path = self.endpoint + '/'.join(args) + '.%s' % (self.format)
        return path

    def get(self, *args, **kwargs):
        """Perform a get request."""
        if 'convert' in kwargs:
            conversion = kwargs.pop('convert')
        else:
            conversion = True
        kwargs = self._get_keywords(**kwargs)
        url = self._create_path(*args)
        request = requests.get(url, params=kwargs)
        content = request.content
        self._request = request
        return self.convert(content, conversion)

    def _get_keywords(self, **kwargs):
        """Format GET request parameters and keywords."""
        if self.jurisdiction and 'jurisdiction_id' not in kwargs:
            kwargs['jurisdiction_id'] = self.jurisdiction
        if 'count' in kwargs:
            kwargs['page_size'] = kwargs.pop('count')
        if 'start' in kwargs:
            start, end = kwargs.pop('start'), kwargs.pop('end')
            start, end = self._format_dates(start, end)
            kwargs['start_date'] = start
            kwargs['end_date'] = end
        elif 'between' in kwargs:
            start, end = kwargs.pop('between')
            start, end = self._format_dates(start, end)
            kwargs['start_date'] = start
            kwargs['end_date'] = end
        return kwargs

    def _format_dates(self, start, end):
        """Format start and end dates."""
        start = self._split_date(start)
        end = self._split_date(end)
        return start, end

    def _split_date(self, time):
        """Split apart a date string."""
        month, day, year = [int(t) for t in re.split(r'-|/', time)]
        time = date(year, month, day)
        return time.strftime('%Y-%m-%dT%H:%M:%SZ')

    def convert(self, content, conversion):
        """Convert content to Python data structures."""
        if not conversion:
            data = content
        elif self.format == 'json':
            data = json.loads(content)
        elif self.format == 'xml':
            content = xml(content)
            first = content.keys()[0]
            data = content[first]
        else:
            data = content
        return data

    def discovery(self, url=None):
        """
        Retrieve the standard discovery file that provides routing
        information.

        >>> Three().discovery()
        {'discovery': 'data'}
        """
        if url:
            data = requests.get(url).content
        else:
            data = self.get('discovery')
        return data

    def services(self, code=None, **kwargs):
        """
        Retrieve information about available services. You can also enter a
        specific service code argument.

        >>> Three().services()
        {'all': {'service_code': 'data'}}
        >>> Three().services('033')
        {'033': {'service_code': 'data'}}
        """
        data = self.get('services', code, **kwargs)
        return data

    def requests(self, code=None, **kwargs):
        """
        Retrieve open requests. You can also enter a specific service code
        argument.

        >>> Three('api.city.gov').requests()
        {'all': {'requests': 'data'}}
        >>> Three('api.city.gov').requests('123')
        {'123': {'requests': 'data'}}
        """
        if code:
            kwargs['service_code'] = code
        data = self.get('requests', **kwargs)
        return data

    def request(self, id, **kwargs):
        """
        Retrieve a specific request using its service code ID.

        >>> Three('api.city.gov').request('12345')
        {'request': {'service_code': {'12345': 'data'}}}
        """
        data = self.get('requests', id, **kwargs)
        return data

    def post(self, code='0', **kwargs):
        """
        Post a new Open311 request.

        >>> t = Three('api.city.gov')
        >>> t.post('123', address='123 Any St', name='Zach Williams',
        ...        phone='555-5555', description='My issue description'.)
        {'successful': {'request': 'post'}}
        """
        kwargs['code'] = code
        kwargs = self._post_keywords(**kwargs)
        url = self._create_path('requests')
        self.request = requests.post(url, data=kwargs)
        content = self.request.content
        if self.request.status_code == 200:
            conversion = True
        else:
            conversion = False
        return self.convert(content, conversion)

    def _post_keywords(self, **kwargs):
        """Configure keyword arguments for Open311 POST requests."""
        code = kwargs.pop('code')
        if 'address' in kwargs:
            address = kwargs.pop('address')
            kwargs['address_string'] = address
        if 'name' in kwargs:
            first, last = kwargs.pop('name').split(' ')
            kwargs['first_name'] = first
            kwargs['last_name'] = last
        if 'api_key' not in kwargs:
            kwargs['api_key'] = self.api_key
        if 'service_code' not in kwargs:
            kwargs['service_code'] = code
        return kwargs

    def token(self, id, **kwargs):
        """
        Retrieve a service request ID from a token.

        >>> Three('api.city.gov').token('12345')
        {'service_request_id': {'for': {'token': '12345'}}}
        """
        data = self.get('tokens', id, **kwargs)
        return data
