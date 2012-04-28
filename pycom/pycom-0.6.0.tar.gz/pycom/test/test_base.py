#   PyCOM - Distributed Component Model for Python
#   Copyright (c) 2011-2012, Dmitry "Divius" Tantsur
#
#   Redistribution and use in source and binary forms, with or without
#   modification, are permitted provided that the following conditions are
#   met:
#
#   * Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#   * Redistributions in binary form must reproduce the above
#     copyright notice, this list of conditions and the following disclaimer
#     in the documentation and/or other materials provided with the
#     distribution.
#
#   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#   "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#   LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#   A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#   OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#   SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#   LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#   DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#   THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#   (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#   OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""Tests for pycom.base."""

import os
import tempfile

import pycom
from pycom import base

from zerojson.testing import unittest


class BaseTest(object):

    def setUp(self):
        self.oldConf = base.configuration.copy()
        base.configuration.clear()

    def tearDown(self):
        base.configuration.clear()
        base.configuration.update(self.oldConf)


class ConfigurationTest(BaseTest, unittest.TestCase):

    def testConfigureDict(self):
        # Very-very smart test follows:
        self.assertIsInstance(pycom.configuration, dict)


class ConfigureTest(BaseTest, unittest.TestCase):

    def testValues(self):
        pycom.configure(nameserver="localhost")
        self.assertDictEqual(pycom.configuration, {"nameserver": "localhost"})
        pycom.configure(nameserver="localhost2", service="/test/Test")
        self.assertDictEqual(pycom.configuration,
            {"nameserver": "localhost2", "service": "/test/Test"})

    def testFile(self):
        with tempfile.NamedTemporaryFile() as f:
            f.write(b"""{
                "nameserver" : "localhost3",
                "service"    : "/test/Test2"
            }""")
            f.flush()

            pycom.configure(f.name)

        self.assertDictEqual(pycom.configuration,
            {"nameserver": "localhost3", "service": "/test/Test2"})
