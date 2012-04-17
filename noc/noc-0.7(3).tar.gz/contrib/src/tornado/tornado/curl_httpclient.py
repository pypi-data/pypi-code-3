#!/usr/bin/env python
#
# Copyright 2009 Facebook
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""Blocking and non-blocking HTTP client implementations using pycurl."""

from __future__ import with_statement

import cStringIO
import collections
import logging
import pycurl
import threading
import time

from tornado import httputil
from tornado import ioloop
from tornado import stack_context

from tornado.escape import utf8
from tornado.httpclient import HTTPRequest, HTTPResponse, HTTPError, AsyncHTTPClient, main

class CurlAsyncHTTPClient(AsyncHTTPClient):
    def initialize(self, io_loop=None, max_clients=10,
                   max_simultaneous_connections=None):
        self.io_loop = io_loop
        self._multi = pycurl.CurlMulti()
        self._multi.setopt(pycurl.M_TIMERFUNCTION, self._set_timeout)
        self._multi.setopt(pycurl.M_SOCKETFUNCTION, self._handle_socket)
        self._curls = [_curl_create(max_simultaneous_connections)
                       for i in xrange(max_clients)]
        self._free_list = self._curls[:]
        self._requests = collections.deque()
        self._fds = {}
        self._timeout = None

        try:
            self._socket_action = self._multi.socket_action
        except AttributeError:
            # socket_action is found in pycurl since 7.18.2 (it's been
            # in libcurl longer than that but wasn't accessible to
            # python).
            logging.warning("socket_action method missing from pycurl; "
                            "falling back to socket_all. Upgrading "
                            "libcurl and pycurl will improve performance")
            self._socket_action = \
                lambda fd, action: self._multi.socket_all()

        # libcurl has bugs that sometimes cause it to not report all
        # relevant file descriptors and timeouts to TIMERFUNCTION/
        # SOCKETFUNCTION.  Mitigate the effects of such bugs by
        # forcing a periodic scan of all active requests.
        self._force_timeout_callback = ioloop.PeriodicCallback(
            self._handle_force_timeout, 1000, io_loop=io_loop)
        self._force_timeout_callback.start()

    def close(self):
        self._force_timeout_callback.stop()
        for curl in self._curls:
            curl.close()
        self._multi.close()
        self._closed = True
        super(CurlAsyncHTTPClient, self).close()

    def fetch(self, request, callback, **kwargs):
        if not isinstance(request, HTTPRequest):
            request = HTTPRequest(url=request, **kwargs)
        self._requests.append((request, stack_context.wrap(callback)))
        self._process_queue()
        self._set_timeout(0)

    def _handle_socket(self, event, fd, multi, data):
        """Called by libcurl when it wants to change the file descriptors
        it cares about.
        """
        event_map = {
            pycurl.POLL_NONE: ioloop.IOLoop.NONE,
            pycurl.POLL_IN: ioloop.IOLoop.READ,
            pycurl.POLL_OUT: ioloop.IOLoop.WRITE,
            pycurl.POLL_INOUT: ioloop.IOLoop.READ | ioloop.IOLoop.WRITE
        }
        if event == pycurl.POLL_REMOVE:
            self.io_loop.remove_handler(fd)
            del self._fds[fd]
        else:
            ioloop_event = event_map[event]
            if fd not in self._fds:
                self._fds[fd] = ioloop_event
                self.io_loop.add_handler(fd, self._handle_events,
                                         ioloop_event)
            else:
                self._fds[fd] = ioloop_event
                self.io_loop.update_handler(fd, ioloop_event)

    def _set_timeout(self, msecs):
        """Called by libcurl to schedule a timeout."""
        if self._timeout is not None:
            self.io_loop.remove_timeout(self._timeout)
        self._timeout = self.io_loop.add_timeout(
            time.time() + msecs/1000.0, self._handle_timeout)

    def _handle_events(self, fd, events):
        """Called by IOLoop when there is activity on one of our
        file descriptors.
        """
        action = 0
        if events & ioloop.IOLoop.READ: action |= pycurl.CSELECT_IN
        if events & ioloop.IOLoop.WRITE: action |= pycurl.CSELECT_OUT
        while True:
            try:
                ret, num_handles = self._socket_action(fd, action)
            except pycurl.error, e:
                ret = e.args[0]
            if ret != pycurl.E_CALL_MULTI_PERFORM:
                break
        self._finish_pending_requests()

    def _handle_timeout(self):
        """Called by IOLoop when the requested timeout has passed."""
        with stack_context.NullContext():
            self._timeout = None
            while True:
                try:
                    ret, num_handles = self._socket_action(
                        pycurl.SOCKET_TIMEOUT, 0)
                except pycurl.error, e:
                    ret = e.args[0]
                if ret != pycurl.E_CALL_MULTI_PERFORM:
                    break
            self._finish_pending_requests()

        # In theory, we shouldn't have to do this because curl will
        # call _set_timeout whenever the timeout changes.  However,
        # sometimes after _handle_timeout we will need to reschedule
        # immediately even though nothing has changed from curl's
        # perspective.  This is because when socket_action is
        # called with SOCKET_TIMEOUT, libcurl decides internally which
        # timeouts need to be processed by using a monotonic clock
        # (where available) while tornado uses python's time.time()
        # to decide when timeouts have occurred.  When those clocks
        # disagree on elapsed time (as they will whenever there is an
        # NTP adjustment), tornado might call _handle_timeout before
        # libcurl is ready.  After each timeout, resync the scheduled
        # timeout with libcurl's current state.
        new_timeout = self._multi.timeout()
        if new_timeout != -1:
            self._set_timeout(new_timeout)

    def _handle_force_timeout(self):
        """Called by IOLoop periodically to ask libcurl to process any
        events it may have forgotten about.
        """
        with stack_context.NullContext():
            while True:
                try:
                    ret, num_handles = self._multi.socket_all()
                except pycurl.error, e:
                    ret = e.args[0]
                if ret != pycurl.E_CALL_MULTI_PERFORM:
                    break
            self._finish_pending_requests()

    def _finish_pending_requests(self):
        """Process any requests that were completed by the last
        call to multi.socket_action.
        """
        while True:
            num_q, ok_list, err_list = self._multi.info_read()
            for curl in ok_list:
                self._finish(curl)
            for curl, errnum, errmsg in err_list:
                self._finish(curl, errnum, errmsg)
            if num_q == 0:
                break
        self._process_queue()

    def _process_queue(self):
        with stack_context.NullContext():
            while True:
                started = 0
                while self._free_list and self._requests:
                    started += 1
                    curl = self._free_list.pop()
                    (request, callback) = self._requests.popleft()
                    curl.info = {
                        "headers": httputil.HTTPHeaders(),
                        "buffer": cStringIO.StringIO(),
                        "request": request,
                        "callback": callback,
                        "curl_start_time": time.time(),
                    }
                    # Disable IPv6 to mitigate the effects of this bug
                    # on curl versions <= 7.21.0
                    # http://sourceforge.net/tracker/?func=detail&aid=3017819&group_id=976&atid=100976
                    if pycurl.version_info()[2] <= 0x71500:  # 7.21.0
                        curl.setopt(pycurl.IPRESOLVE, pycurl.IPRESOLVE_V4)
                    _curl_setup_request(curl, request, curl.info["buffer"],
                                        curl.info["headers"])
                    self._multi.add_handle(curl)

                if not started:
                    break

    def _finish(self, curl, curl_error=None, curl_message=None):
        info = curl.info
        curl.info = None
        self._multi.remove_handle(curl)
        self._free_list.append(curl)
        buffer = info["buffer"]
        if curl_error:
            error = CurlError(curl_error, curl_message)
            code = error.code
            effective_url = None
            buffer.close()
            buffer = None
        else:
            error = None
            code = curl.getinfo(pycurl.HTTP_CODE)
            effective_url = curl.getinfo(pycurl.EFFECTIVE_URL)
            buffer.seek(0)
        # the various curl timings are documented at
        # http://curl.haxx.se/libcurl/c/curl_easy_getinfo.html
        time_info = dict(
            queue=info["curl_start_time"] - info["request"].start_time,
            namelookup=curl.getinfo(pycurl.NAMELOOKUP_TIME),
            connect=curl.getinfo(pycurl.CONNECT_TIME),
            pretransfer=curl.getinfo(pycurl.PRETRANSFER_TIME),
            starttransfer=curl.getinfo(pycurl.STARTTRANSFER_TIME),
            total=curl.getinfo(pycurl.TOTAL_TIME),
            redirect=curl.getinfo(pycurl.REDIRECT_TIME),
            )
        try:
            info["callback"](HTTPResponse(
                request=info["request"], code=code, headers=info["headers"],
                buffer=buffer, effective_url=effective_url, error=error,
                request_time=time.time() - info["curl_start_time"],
                time_info=time_info))
        except Exception:
            self.handle_callback_exception(info["callback"])


    def handle_callback_exception(self, callback):
        self.io_loop.handle_callback_exception(callback)


class CurlError(HTTPError):
    def __init__(self, errno, message):
        HTTPError.__init__(self, 599, message)
        self.errno = errno


def _curl_create(max_simultaneous_connections=None):
    curl = pycurl.Curl()
    if logging.getLogger().isEnabledFor(logging.DEBUG):
        curl.setopt(pycurl.VERBOSE, 1)
        curl.setopt(pycurl.DEBUGFUNCTION, _curl_debug)
    curl.setopt(pycurl.MAXCONNECTS, max_simultaneous_connections or 5)
    return curl


def _curl_setup_request(curl, request, buffer, headers):
    curl.setopt(pycurl.URL, utf8(request.url))

    # libcurl's magic "Expect: 100-continue" behavior causes delays
    # with servers that don't support it (which include, among others,
    # Google's OpenID endpoint).  Additionally, this behavior has
    # a bug in conjunction with the curl_multi_socket_action API
    # (https://sourceforge.net/tracker/?func=detail&atid=100976&aid=3039744&group_id=976),
    # which increases the delays.  It's more trouble than it's worth,
    # so just turn off the feature (yes, setting Expect: to an empty
    # value is the official way to disable this)
    if "Expect" not in request.headers:
        request.headers["Expect"] = ""

    # libcurl adds Pragma: no-cache by default; disable that too
    if "Pragma" not in request.headers:
        request.headers["Pragma"] = ""

    # Request headers may be either a regular dict or HTTPHeaders object
    if isinstance(request.headers, httputil.HTTPHeaders):
        curl.setopt(pycurl.HTTPHEADER,
                    [utf8("%s: %s" % i) for i in request.headers.get_all()])
    else:
        curl.setopt(pycurl.HTTPHEADER,
                    [utf8("%s: %s" % i) for i in request.headers.iteritems()])

    if request.header_callback:
        curl.setopt(pycurl.HEADERFUNCTION, request.header_callback)
    else:
        curl.setopt(pycurl.HEADERFUNCTION,
                    lambda line: _curl_header_callback(headers, line))
    if request.streaming_callback:
        curl.setopt(pycurl.WRITEFUNCTION, request.streaming_callback)
    else:
        curl.setopt(pycurl.WRITEFUNCTION, buffer.write)
    curl.setopt(pycurl.FOLLOWLOCATION, request.follow_redirects)
    curl.setopt(pycurl.MAXREDIRS, request.max_redirects)
    curl.setopt(pycurl.CONNECTTIMEOUT_MS, int(1000 * request.connect_timeout))
    curl.setopt(pycurl.TIMEOUT_MS, int(1000 * request.request_timeout))
    if request.user_agent:
        curl.setopt(pycurl.USERAGENT, utf8(request.user_agent))
    else:
        curl.setopt(pycurl.USERAGENT, "Mozilla/5.0 (compatible; pycurl)")
    if request.network_interface:
        curl.setopt(pycurl.INTERFACE, request.network_interface)
    if request.use_gzip:
        curl.setopt(pycurl.ENCODING, "gzip,deflate")
    else:
        curl.setopt(pycurl.ENCODING, "none")
    if request.proxy_host and request.proxy_port:
        curl.setopt(pycurl.PROXY, request.proxy_host)
        curl.setopt(pycurl.PROXYPORT, request.proxy_port)
        if request.proxy_username:
            credentials = '%s:%s' % (request.proxy_username,
                    request.proxy_password)
            curl.setopt(pycurl.PROXYUSERPWD, credentials)
    else:
        curl.setopt(pycurl.PROXY, '')
    if request.validate_cert:
        curl.setopt(pycurl.SSL_VERIFYPEER, 1)
        curl.setopt(pycurl.SSL_VERIFYHOST, 2)
    else:
        curl.setopt(pycurl.SSL_VERIFYPEER, 0)
        curl.setopt(pycurl.SSL_VERIFYHOST, 0)
    if request.ca_certs is not None:
        curl.setopt(pycurl.CAINFO, request.ca_certs)
    else:
        # There is no way to restore pycurl.CAINFO to its default value
        # (Using unsetopt makes it reject all certificates).
        # I don't see any way to read the default value from python so it
        # can be restored later.  We'll have to just leave CAINFO untouched
        # if no ca_certs file was specified, and require that if any
        # request uses a custom ca_certs file, they all must.
        pass

    if request.allow_ipv6 is False:
        # Curl behaves reasonably when DNS resolution gives an ipv6 address
        # that we can't reach, so allow ipv6 unless the user asks to disable.
        # (but see version check in _process_queue above)
        curl.setopt(pycurl.IPRESOLVE, pycurl.IPRESOLVE_V4)

    # Set the request method through curl's irritating interface which makes
    # up names for almost every single method
    curl_options = {
        "GET": pycurl.HTTPGET,
        "POST": pycurl.POST,
        "PUT": pycurl.UPLOAD,
        "HEAD": pycurl.NOBODY,
    }
    custom_methods = set(["DELETE"])
    for o in curl_options.values():
        curl.setopt(o, False)
    if request.method in curl_options:
        curl.unsetopt(pycurl.CUSTOMREQUEST)
        curl.setopt(curl_options[request.method], True)
    elif request.allow_nonstandard_methods or request.method in custom_methods:
        curl.setopt(pycurl.CUSTOMREQUEST, request.method)
    else:
        raise KeyError('unknown method ' + request.method)

    # Handle curl's cryptic options for every individual HTTP method
    if request.method in ("POST", "PUT"):
        request_buffer =  cStringIO.StringIO(utf8(request.body))
        curl.setopt(pycurl.READFUNCTION, request_buffer.read)
        if request.method == "POST":
            def ioctl(cmd):
                if cmd == curl.IOCMD_RESTARTREAD:
                    request_buffer.seek(0)
            curl.setopt(pycurl.IOCTLFUNCTION, ioctl)
            curl.setopt(pycurl.POSTFIELDSIZE, len(request.body))
        else:
            curl.setopt(pycurl.INFILESIZE, len(request.body))

    if request.auth_username is not None:
        userpwd = "%s:%s" % (request.auth_username, request.auth_password or '')
        curl.setopt(pycurl.HTTPAUTH, pycurl.HTTPAUTH_BASIC)
        curl.setopt(pycurl.USERPWD, utf8(userpwd))
        logging.debug("%s %s (username: %r)", request.method, request.url,
                      request.auth_username)
    else:
        curl.unsetopt(pycurl.USERPWD)
        logging.debug("%s %s", request.method, request.url)

    if request.client_key is not None or request.client_cert is not None:
        raise ValueError("Client certificate not supported with curl_httpclient")

    if threading.activeCount() > 1:
        # libcurl/pycurl is not thread-safe by default.  When multiple threads
        # are used, signals should be disabled.  This has the side effect
        # of disabling DNS timeouts in some environments (when libcurl is
        # not linked against ares), so we don't do it when there is only one
        # thread.  Applications that use many short-lived threads may need
        # to set NOSIGNAL manually in a prepare_curl_callback since
        # there may not be any other threads running at the time we call
        # threading.activeCount.
        curl.setopt(pycurl.NOSIGNAL, 1)
    if request.prepare_curl_callback is not None:
        request.prepare_curl_callback(curl)


def _curl_header_callback(headers, header_line):
    # header_line as returned by curl includes the end-of-line characters.
    header_line = header_line.strip()
    if header_line.startswith("HTTP/"):
        headers.clear()
        return
    if not header_line:
        return
    headers.parse_line(header_line)

def _curl_debug(debug_type, debug_msg):
    debug_types = ('I', '<', '>', '<', '>')
    if debug_type == 0:
        logging.debug('%s', debug_msg.strip())
    elif debug_type in (1, 2):
        for line in debug_msg.splitlines():
            logging.debug('%s %s', debug_types[debug_type], line)
    elif debug_type == 4:
        logging.debug('%s %r', debug_types[debug_type], debug_msg)

if __name__ == "__main__":
    AsyncHTTPClient.configure(CurlAsyncHTTPClient)
    main()
