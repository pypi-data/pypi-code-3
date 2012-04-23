import os
import sys
import glob
import json
import tempfile
from io import BytesIO

if sys.version_info[0] < 3:
    import robotparser
else:
    from urllib import robotparser

import mock
from nose.tools import assert_equal, assert_raises
import requests
from .. import (Scraper, HTTPError, HTTPMethodUnavailableError,
                RobotExclusionError, urllib_URLError)
from .. import _user_agent as default_user_agent
from ..cache import FileCache

HTTPBIN = 'http://httpbin.org/'


class FakeResponse(object):
    def __init__(self, url, code, content, encoding='utf-8', headers=None):
        self.url = url
        self.status_code = code
        self.content = content
        self.text = str(content)
        self.encoding = encoding
        self.headers = headers or {}


def request_200(method, url, *args, **kwargs):
    return FakeResponse(url, 200, b'ok')
mock_200 = mock.Mock(wraps=request_200)


def test_constructor():
    # timeout=0 means None
    s = Scraper(timeout=0)
    assert s.timeout is None


def test_get():
    s = Scraper(requests_per_minute=0, follow_robots=False)
    resp = s.urlopen(HTTPBIN + 'get?woo=woo')
    assert_equal(resp.response.code, 200)
    assert_equal(json.loads(resp)['args']['woo'], 'woo')


def test_post():
    s = Scraper(requests_per_minute=0, follow_robots=False)
    resp = s.urlopen(HTTPBIN + 'post', 'POST', b'woo=woo')
    assert_equal(resp.response.code, 200)
    resp_json = json.loads(resp)
    assert_equal(resp_json['form']['woo'], 'woo')
    assert_equal(resp_json['headers']['Content-Type'],
                     'application/x-www-form-urlencoded')


def test_request_throttling():
    s = Scraper(requests_per_minute=30, follow_robots=False,
                accept_cookies=False)
    assert_equal(s.requests_per_minute, 30)

    mock_sleep = mock.Mock()
    mock_200.reset_mock()

    # check that sleep is called
    with mock.patch('time.sleep', mock_sleep):
        with mock.patch.object(s._session, 'request', mock_200):
            s.urlopen('http://dummy/')
            s.urlopen('http://dummy/')
            s.urlopen('http://dummy/')
            assert_equal(mock_sleep.call_count, 2)
            # should have slept for ~2 seconds
            assert 1.8 <= mock_sleep.call_args[0][0] <= 2.2
            assert_equal(mock_200.call_count, 3)

    # unthrottled, should be able to fit in lots of calls
    s.requests_per_minute = 0
    mock_200.reset_mock()
    mock_sleep.reset_mock()

    with mock.patch('time.sleep', mock_sleep):
        with mock.patch.object(s._session, 'request', mock_200):
            s.urlopen('http://dummy/')
            s.urlopen('http://dummy/')
            s.urlopen('http://dummy/')
            assert_equal(mock_sleep.call_count, 0)
            assert_equal(mock_200.call_count, 3)


def test_user_agent():
    s = Scraper(requests_per_minute=0, follow_robots=False)
    resp = s.urlopen(HTTPBIN + 'user-agent')
    ua = json.loads(resp)['user-agent']
    assert_equal(ua, default_user_agent)

    s.user_agent = 'a different agent'
    resp = s.urlopen(HTTPBIN + 'user-agent')
    ua = json.loads(resp)['user-agent']
    assert_equal(ua, 'a different agent')


def test_default_to_http():
    s = Scraper(requests_per_minute=0, follow_robots=False)
    with mock.patch.object(s._session, 'request', mock_200):
        assert_equal('http://dummy/', s.urlopen("dummy/").response.url)


def test_follow_robots():
    s = Scraper(requests_per_minute=0, follow_robots=True)

    with mock.patch.object(s._session, 'request', mock_200):
        # check that a robots.txt is created
        s.urlopen(HTTPBIN)
        assert HTTPBIN + 'robots.txt' in s._robot_parsers

        # set a fake robots.txt for http://dummy
        parser = robotparser.RobotFileParser()
        parser.parse(['User-agent: *', 'Disallow: /private/', 'Allow: /'])
        s._robot_parsers['http://dummy/robots.txt'] = parser

        # anything behind private fails
        assert_raises(RobotExclusionError, s.urlopen,
                      "http://dummy/private/secret.html")
        # but others work
        assert_equal(200, s.urlopen("http://dummy/").response.code)

        # turn off follow_robots, everything works
        s.follow_robots = False
        assert_equal(200,
            s.urlopen("http://dummy/private/secret.html").response.code)


def test_error_context():
    # create error dir
    error_dir = tempfile.mkdtemp()
    s = Scraper(requests_per_minute=0, follow_robots=False,
                error_dir=error_dir)

    with mock.patch.object(s._session, 'request', mock_200):
        # try twice to test file name collision
        try:
            with s.urlopen("http://dummy/"):
                raise Exception('test')
        except:
            pass
        try:
            with s.urlopen("http://dummy/"):
                raise Exception('test')
        except:
            pass

    assert os.path.isfile(os.path.join(error_dir, "http:,,dummy,"))
    assert os.path.isfile(os.path.join(error_dir, "http:,,dummy,-1"))

    # tear down error dir
    for path in glob.iglob(os.path.join(error_dir, "*")):
        os.remove(path)
    os.rmdir(error_dir)


def test_404():
    s = Scraper(requests_per_minute=0, follow_robots=False)
    assert_raises(HTTPError, s.urlopen, HTTPBIN + 'status/404')

    s.raise_errors = False
    resp = s.urlopen(HTTPBIN + 'status/404')
    assert_equal(404, resp.response.code)


def test_500():
    s = Scraper(requests_per_minute=0, follow_robots=False)

    assert_raises(HTTPError, s.urlopen, HTTPBIN + 'status/500')

    s.raise_errors = False
    resp = s.urlopen(HTTPBIN + 'status/500')
    assert_equal(500, resp.response.code)


def test_follow_redirect():
    s = Scraper(requests_per_minute=0, follow_robots=False)

    redirect_url = HTTPBIN + 'redirect/1'
    final_url = HTTPBIN + 'get'

    resp = s.urlopen(redirect_url)
    assert_equal(final_url, resp.response.url)
    assert_equal(redirect_url, resp.response.requested_url)
    assert_equal(200, resp.response.code)

    s.follow_redirects = False
    resp = s.urlopen(redirect_url)
    assert_equal(redirect_url, resp.response.url)
    assert_equal(redirect_url, resp.response.requested_url)
    assert_equal(302, resp.response.code)


def test_caching():
    cache_dir = tempfile.mkdtemp()
    s = Scraper(requests_per_minute=0, follow_robots=False,
                cache_obj=FileCache(cache_dir), cache_write_only=False)

    resp = s.urlopen(HTTPBIN + 'status/200')
    assert not resp.response.fromcache
    resp = s.urlopen(HTTPBIN + 'status/200')
    assert resp.response.fromcache

    for path in glob.iglob(os.path.join(cache_dir, "*")):
        os.remove(path)
    os.rmdir(cache_dir)


def test_urlretrieve():
    s = Scraper(requests_per_minute=0, follow_robots=False)

    with mock.patch.object(s._session, 'request', mock_200):
        fname, resp = s.urlretrieve("http://dummy/")
        with open(fname) as f:
            assert_equal(f.read(), 'ok')
            assert_equal(200, resp.code)
        os.remove(fname)

        (fh, set_fname) = tempfile.mkstemp()
        fname, resp = s.urlretrieve("http://dummy/", set_fname)
        assert_equal(fname, set_fname)
        with open(set_fname) as f:
            assert_equal(f.read(), 'ok')
            assert_equal(200, resp.code)
        os.remove(set_fname)

## TODO: on these retry tests it'd be nice to ensure that it tries
## 3 times for 500 and once for 404


def test_retry():
    s = Scraper(retry_attempts=3, retry_wait_seconds=0.001,
                follow_robots=False, raise_errors=False)

    # On the first call return a 500, then a 200
    mock_request = mock.Mock(side_effect=[
        FakeResponse('http://dummy/', 500, 'failure!'),
        FakeResponse('http://dummy/', 200, 'success!')
    ])

    with mock.patch.object(s._session, 'request', mock_request):
        resp = s.urlopen('http://dummy/')
    assert_equal(mock_request.call_count, 2)

    # 500 always
    mock_request = mock.Mock(return_value=FakeResponse('http://dummy/', 500,
                                                       'failure!'))

    with mock.patch.object(s._session, 'request', mock_request):
        resp = s.urlopen('http://dummy/')
    assert_equal(resp.response.code, 500)
    assert_equal(mock_request.call_count, 4)


def test_retry_404():
    s = Scraper(retry_attempts=3, retry_wait_seconds=0.001,
                follow_robots=False, raise_errors=False)

    # On the first call return a 404, then a 200
    mock_request = mock.Mock(side_effect=[
        FakeResponse('http://dummy/', 404, 'failure!'),
        FakeResponse('http://dummy/', 200, 'success!')
    ])

    with mock.patch.object(s._session, 'request', mock_request):
        resp = s.urlopen('http://dummy/', retry_on_404=True)
    assert_equal(mock_request.call_count, 2)

    # 404 always
    mock_request = mock.Mock(return_value=FakeResponse('http://dummy/', 404,
                                                       'failure!'))

    # retry on 404 true, 4 tries
    with mock.patch.object(s._session, 'request', mock_request):
        resp = s.urlopen('http://dummy/', retry_on_404=True)
    assert_equal(resp.response.code, 404)
    assert_equal(mock_request.call_count, 4)

    # retry on 404 false, just one more try
    with mock.patch.object(s._session, 'request', mock_request):
        resp = s.urlopen('http://dummy/', retry_on_404=False)
    assert_equal(resp.response.code, 404)
    assert_equal(mock_request.call_count, 5)


def test_timeout_retry():
    count = []

    # On the first call raise timeout
    def side_effect(*args, **kwargs):
        if count:
            return FakeResponse('http://dummy/', 200, 'success!')
        count.append(1)
        raise requests.Timeout('timed out :(')

    mock_request = mock.Mock(side_effect=side_effect)

    s = Scraper(retry_attempts=0, retry_wait_seconds=0.001,
                follow_robots=False)

    with mock.patch.object(s._session, 'request', mock_request):
        # first, try without retries
        # try only once, get the error
        assert_raises(requests.Timeout, s.urlopen, "http://dummy/")
        assert_equal(mock_request.call_count, 1)

    # reset and try again with retries
    mock_request.reset_mock()
    count = []
    s = Scraper(retry_attempts=2, retry_wait_seconds=0.001,
                follow_robots=False)
    with mock.patch.object(s._session, 'request', mock_request):
        resp = s.urlopen("http://dummy/")
        # get the result, take two tries
        assert_equal(resp, "success!")
        assert_equal(mock_request.call_count, 2)


def test_disable_compression():
    s = Scraper(disable_compression=True)

    headers = s._make_headers("http://dummy/")
    assert_equal(headers['accept-encoding'], 'text/*')

    # A supplied Accept-Encoding headers overrides the
    # disable_compression option
    s.headers['accept-encoding'] = '*'
    headers = s._make_headers('http://dummy/')
    assert_equal(headers['accept-encoding'], '*')


def test_callable_headers():
    s = Scraper(headers=lambda url: {'url': url})

    headers = s._make_headers('http://google.com')
    assert_equal(headers['url'], 'http://google.com')

    # Make sure it gets called freshly each time
    headers = s._make_headers('http://example.com')
    assert_equal(headers['url'], 'http://example.com')


def test_ftp_uses_urllib2():
    s = Scraper(requests_per_minute=0, follow_robots=False)
    urlopen = mock.Mock(return_value=BytesIO(b"ftp success!"))

    with mock.patch('scrapelib.urllib_urlopen', urlopen):
        r = s.urlopen('ftp://dummy/')
        assert r.response.code == 200
        assert r == "ftp success!"


def test_ftp_retries():
    count = []

    # On the first call raise URLError, then work
    def side_effect(*args, **kwargs):
        if count:
            return BytesIO(b"ftp success!")
        count.append(1)
        raise urllib_URLError('550: ftp failure!')

    mock_urlopen = mock.Mock(side_effect=side_effect)

    # retry on, retry_on_404 on (will retry due to 550 code)
    with mock.patch('scrapelib.urllib_urlopen', mock_urlopen):
        s = Scraper(retry_attempts=2, retry_wait_seconds=0.001,
                    follow_robots=False)
        r = s.urlopen('ftp://dummy/', retry_on_404=True)
        assert r == "ftp success!"
    assert_equal(mock_urlopen.call_count, 2)

    # retry off, retry_on_404 on (shouldn't matter)
    count = []
    mock_urlopen.reset_mock()
    with mock.patch('scrapelib.urllib_urlopen', mock_urlopen):
        s = Scraper(retry_attempts=0, retry_wait_seconds=0.001,
                    follow_robots=False)
        assert_raises(urllib_URLError, s.urlopen, 'ftp://dummy/',
                      retry_on_404=True)
    assert_equal(mock_urlopen.call_count, 1)

    # retry on, retry_on_404 off
    count = []
    mock_urlopen.reset_mock()
    with mock.patch('scrapelib.urllib_urlopen', mock_urlopen):
        s = Scraper(retry_attempts=2, retry_wait_seconds=0.001,
                    follow_robots=False)
        assert_raises(urllib_URLError, s.urlopen, 'ftp://dummy/')
    assert_equal(mock_urlopen.call_count, 1)


def test_ftp_method_restrictions():
    s = Scraper(requests_per_minute=0, follow_robots=False)

    # only http(s) supports non-'GET' requests
    assert_raises(HTTPMethodUnavailableError, s.urlopen, "ftp://dummy/",
                  method='POST')
