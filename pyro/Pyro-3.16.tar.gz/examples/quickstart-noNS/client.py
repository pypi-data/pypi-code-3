#!/usr/bin/env python

from Pyro.ext import remote_nons

print 'getting remote object "quickstart"...'
test = remote_nons.get_server_object('quickstart','localhost', 9123)

print test.method1("Johnny")
print test.method2(42)

