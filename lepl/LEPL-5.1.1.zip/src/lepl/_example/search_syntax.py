
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
http://stackoverflow.com/questions/2364683/what-is-a-good-python-parser-for-a-google-like-search-query
'''

from unittest import TestCase

from lepl import *


class SearchTest(TestCase):
    
    def compile(self):
        
        class Alternatives(Node):
            pass
        
        class Query(Node):
            pass
        
        class Text(Node):
            pass

        qualifier      = Word() + Drop(':')           > 'qualifier'
        word           = ~Lookahead('OR') & Word()
        phrase         = String()
        text           = (phrase | word)
        word_or_phrase = (Optional(qualifier) & text) > Text
        space          = Drop(Space()[1:])
        query          = word_or_phrase[1:, space]    > Query
        separator      = Drop(space & 'OR' & space)
        alternatives   = query[:, separator]          > Alternatives
        return alternatives.get_parse_string()
        
    def test_word(self):
        result = self.compile()('word')
        #print(str(result[0]))
        assert result, result
        
    def test_complex(self):
        result = self.compile()('all of these words "with this phrase" '
                                'OR that OR this site:within.site '
                                'filetype:ps from:lastweek')
        #print(str(result[0]))
        assert result, result
        
        