#!/usr/bin/env python
#
#    Copyright (C) 2009 Google Inc.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.


# This module is used for version 2 of the Google Data APIs.


__author__ = 'j.s@google.com (Jeff Scudder)'


import unittest
import atom.auth
import atom.http_core


class BasicAuthTest(unittest.TestCase):
 
  def test_modify_request(self):
    http_request = atom.http_core.HttpRequest()
    credentials = atom.auth.BasicAuth('Aladdin', 'open sesame')
    self.assert_(credentials.basic_cookie == 'QWxhZGRpbjpvcGVuIHNlc2FtZQ==')
    credentials.modify_request(http_request)
    self.assert_(http_request.headers[
        'Authorization'] == 'Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ==')


def suite():
  return unittest.TestSuite((unittest.makeSuite(BasicAuthTest,'test'),))


if __name__ == '__main__':
  unittest.main()
