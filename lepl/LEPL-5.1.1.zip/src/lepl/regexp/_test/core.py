
# The contents of this file are subject to the Mozilla Public License
# (MPL) Version 1.1 (the "License"); you may not use this file except
# in compliance with the License. You may obtain a copy of the License
# at http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS IS"
# basis, WITHOUT WARRANTY OF ANY KIND, either express or implied. See
# the License for the specific language governing rights and
# limitations under the License.
#
# The Original Code is LEPL (http://www.acooke.org/lepl)
# The Initial Developer of the Original Code is Andrew Cooke.
# Portions created by the Initial Developer are Copyright (C) 2009-2010
# Andrew Cooke (andrew@acooke.org). All Rights Reserved.
#
# Alternatively, the contents of this file may be used under the terms
# of the LGPL license (the GNU Lesser General Public License,
# http://www.gnu.org/licenses/lgpl.html), in which case the provisions
# of the LGPL License are applicable instead of those above.
#
# If you wish to allow use of your version of this file only under the
# terms of the LGPL License and not to allow others to use your version
# of this file under the MPL, indicate your decision by deleting the
# provisions above and replace them with the notice and other provisions
# required by the LGPL License.  If you do not delete the provisions
# above, a recipient may use your version of this file under either the
# MPL or the LGPL License.

'''
Tests for the lepl.regexp.matchers module.
'''

#from logging import basicConfig, DEBUG
from unittest import TestCase

from lepl import UnicodeAlphabet
from lepl.regexp.core import Compiler
from lepl.support.lib import fmt
from lepl.stream.simple import StringHelper
from lepl.stream.core import DUMMY_HELPER


# pylint: disable-msg=C0103, C0111, C0301
# (dude this is just a test)


class CompilerTest(TestCase):
    
    def test_compiler(self):
        #basicConfig(level=DEBUG)
        self.do_test('a', 'a', 
                     (('label',), 'a', (1, DUMMY_HELPER)), 
                     [('label', 'a', (1, DUMMY_HELPER))])
        self.do_test('ab', 'ab', 
                     (('label',), 'ab', (2, DUMMY_HELPER)), 
                     [('label', 'ab', (2, DUMMY_HELPER))])
        self.do_test('a', 'ab', 
                     (('label',), 'a', (1, DUMMY_HELPER)), 
                     [('label', 'a', (1, DUMMY_HELPER))])
        self.do_test('a*', 'aab', 
                     (('label',), 'aa', (2, DUMMY_HELPER)), 
                     [('label', 'aa', (2, DUMMY_HELPER)), 
                      ('label', 'a', (1, DUMMY_HELPER)), 
                      ('label', '', (0, DUMMY_HELPER))])
        self.do_test('(?:a|b)', 'a', 
                     (('label',), 'a', (1, DUMMY_HELPER)), 
                     [('label', 'a', (1, DUMMY_HELPER))])
        self.do_test('(?:a|b)', 'b', 
                     (('label',), 'b', (1, DUMMY_HELPER)), 
                     [('label', 'b', (1, DUMMY_HELPER))])
        # note how the DFA gives the longest match (only) here 
        self.do_test('(?:a|ab)', 'ab', 
                     (('label',), 'ab', (2, DUMMY_HELPER)), 
                     [('label', 'a', (1, DUMMY_HELPER)), 
                      ('label', 'ab', (2, DUMMY_HELPER))])
        self.do_test('(?:ab|a)', 'ab', 
                     (('label',), 'ab', (2, DUMMY_HELPER)),
                     [('label', 'ab', (2, DUMMY_HELPER)), 
                      ('label', 'a', (1, DUMMY_HELPER))])
        
    def do_test(self, pattern, target, dfa_result, nfa_result):
        alphabet = UnicodeAlphabet.instance()
        compiler = Compiler.single(alphabet, pattern)
        text = str(compiler.expression)
        assert text == fmt('(?P<label>{0!s})', pattern), text
        nfa = compiler.nfa()
        result = list(nfa.match((0, StringHelper(target))))
        assert result == nfa_result, result
        dfa = compiler.dfa()
        result = dfa.match((0, StringHelper(target)))
        assert result == dfa_result, result
