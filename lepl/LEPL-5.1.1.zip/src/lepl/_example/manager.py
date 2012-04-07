
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

# pylint: disable-msg=W0401,C0111,W0614,W0622,C0301,C0321,C0324,C0103
# (the code style is for documentation, not "real")

'''
Examples from the documentation.
'''

#@PydevCodeAnalysisIgnore


from lepl import *
from lepl._example.support import Example


class ResourceExample(Example):
    
    def test_no_limit(self):
        expr = (Literal('*')[:,...][2] & Eos())
        matcher = expr.get_parse_sequence_all()
#        print(matcher.matcher.tree())
        results = matcher('*' * 4)
        self.examples([(lambda: list(results), 
                        "[['****'], ['***', '*'], ['**', '**'], ['*', '***'], ['****']]")])

    def test_limit(self):
        expr = Literal('*')[:,...][2] & Eos()
        # clear is here because the original test didn't have such a complex config
        expr.config.clear().low_memory(8) # changed from 3 in lepl 5
        matcher = expr.get_parse_sequence_all()
#        print(matcher.matcher.tree())
        results = matcher('*' * 4)
        self.examples([(lambda: list(results), 
                        "[['****'], ['***', '*']]")])
