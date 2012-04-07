
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

# pylint: disable-msg=W0401,C0111,W0614,W0622,C0301,C0321,C0324,C0103,R0201,R0903
#@PydevCodeAnalysisIgnore
# (the code style is for documentation, not "real")

'''
Examples from the documentation.
'''

from logging import basicConfig, DEBUG

from lepl import *
from lepl._example.support import Example


class NodeErrorTest(Example):
    
    def make_parser(self):

        #basicConfig(level=DEBUG)
        
        class Term(Node): pass
        class Factor(Node): pass
        class Expression(Node): pass
        
        expr    = Delayed()
        number  = Digit()[1:,...]                          > 'number'
        badChar = AnyBut(Space() | Digit() | '(')[1:,...]
        
        with DroppedSpace():
            
            unopen   = number ** make_error("no ( before {out_rest!s}") & ')'
            unclosed = ('(' & expr & Eos()) ** make_error("no ) for {in_rest!s}")
        
            term    = Or(
                         (number | '(' & expr & ')')      > Term,
                         badChar                          ^ 'unexpected text: {results[0]}',
                         unopen,
                         unclosed
                         )
            muldiv  = Any('*/')                           > 'operator'
            factor  = (term & (muldiv & term)[:])         > Factor
            addsub  = Any('+-')                           > 'operator'
            expr   += (factor & (addsub & factor)[:])     > Expression
            line    = (Empty() & expr & Eos())            >> node_throw
        
        return line.get_parse()
    
    def test_errors1(self):
        parser = self.make_parser()
        self.examples([(lambda: parser('1 + 2 * (3 + 4 - 5')[0],
                       """  File "<string>", line 1
    1 + 2 * (3 + 4 - 5
            ^
Error: no ) for '(3 + 4 - 5'
"""),
                       (lambda: parser('1 + 2 * 3 + 4 - 5)')[0],
                        """  File "<string>", line 1
    1 + 2 * 3 + 4 - 5)
                    ^
Error: no ( before ')'
"""),
                       (lambda: parser('1 + 2 * (3 + four - 5)')[0],
                        """  File "<string>", line 1
    1 + 2 * (3 + four - 5)
                 ^
Error: unexpected text: four
"""),
                       (lambda: parser('1 + 2 ** (3 + 4 - 5)')[0],
                        """  File "<string>", line 1
    1 + 2 ** (3 + 4 - 5)
           ^
Error: unexpected text: *
""")])
    
    
class ListErrorTest(Example):
    
    def make_parser(self):

        #basicConfig(level=DEBUG)
        
        class Term(List): pass
        class Factor(List): pass
        class Expression(List): pass
        
        expr    = Delayed()
        number  = Digit()[1:,...]
        badChar = AnyBut(Space() | Digit() | '(')[1:,...]
        
        with DroppedSpace():
            
            unopen   = number ** make_error("no ( before {out_rest!s}") & ')'
            unclosed = ('(' & expr & Eos()) ** make_error("no ) for {in_rest!s}")
        
            term    = Or(
                         (number | '(' & expr & ')')      > Term,
                         badChar                          ^ 'unexpected text: {results[0]}',
                         unopen,
                         unclosed
                         )
            muldiv  = Any('*/')
            factor  = (term & (muldiv & term)[:])         > Factor
            addsub  = Any('+-')
            expr   += (factor & (addsub & factor)[:])     > Expression
            line    = (Empty() & expr & Eos())            >> sexpr_throw
        
        return line.get_parse()
    
    def test_errors2(self):
        parser = self.make_parser()
        self.examples([(lambda: parser('1 + 2 * (3 + 4 - 5')[0],
                       """  File "<string>", line 1
    1 + 2 * (3 + 4 - 5
            ^
Error: no ) for '(3 + 4 - 5'
"""),
                       (lambda: parser('1 + 2 * 3 + 4 - 5)')[0],
                        """  File "<string>", line 1
    1 + 2 * 3 + 4 - 5)
                    ^
Error: no ( before ')'
"""),
                       (lambda: parser('1 + 2 * (3 + four - 5)')[0],
                        """  File "<string>", line 1
    1 + 2 * (3 + four - 5)
                 ^
Error: unexpected text: four
"""),
                       (lambda: parser('1 + 2 ** (3 + 4 - 5)')[0],
                        """  File "<string>", line 1
    1 + 2 ** (3 + 4 - 5)
           ^
Error: unexpected text: *
""")])
    