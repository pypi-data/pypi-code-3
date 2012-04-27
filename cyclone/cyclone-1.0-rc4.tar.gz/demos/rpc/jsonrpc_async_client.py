#!/usr/bin/env python
# coding: utf-8
#
# Copyright 2010 Alexandre Fiori
# based on the original Tornado by Facebook
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

import cyclone.httpclient
from twisted.internet import defer, reactor


@defer.inlineCallbacks
def main():
    cli = cyclone.httpclient.JsonRPC("http://localhost:8888/jsonrpc")
    print "echo:", (yield cli.echo("foo bar"))
    print "sort:", (yield cli.sort(["foo", "bar"]))
    print "count:", (yield cli.count(["foo", "bar"]))
    print "geoip_lookup:", (yield cli.geoip_lookup("google.com"))
    reactor.stop()

if __name__ == "__main__":
    main()
    reactor.run()
