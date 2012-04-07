
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
Display information when matchers that are bound to variables are called.

This is possible thanks to a neat trick suggested by Carl Banks on c.l.p 
'''

from __future__ import generators, print_function
from contextlib import contextmanager
from sys import stderr, _getframe

from lepl.stream.core import s_debug, s_line, s_kargs
from lepl.matchers.support import trampoline_matcher_factory
from lepl.support.lib import fmt, str


@trampoline_matcher_factory()
def NamedResult(name, matcher, out=stderr):
    
    def fmt_stream(stream):
        try:
            (line, _) = s_line(stream, False)
            text = str(line)
            if len(text) > 20:
                text = text[:17] + '...'
            return repr(text)
        except StopIteration:
            return '<EOS>'
    
    def record_success(count, stream_in, result):
        (value, stream_out) = result
        count_desc = fmt(' ({0})', count) if count > 1 else ''
        # Python bug #4618
        print(fmt('{0}{1} = {2}\n    {3} -> {4}', 
                     name, count_desc, value, 
                     fmt_stream(stream_in), fmt_stream(stream_out)), 
              file=out, end=str('\n'))
        
    def record_failure(count, stream_in):
        # Python bug #4618
        print(fmt('! {0} (after {1} matches)\n    {2}', name, count, 
                     fmt_stream(stream_in)),
              file=out, end=str('\n'))
    
    def match(support, stream):
        count = 0
        generator = matcher._match(stream)
        try:
            while True:
                value = yield generator
                count += 1
                record_success(count, stream, value)
                yield value
        except StopIteration:
            record_failure(count, stream)

    return match


def _adjust(text, width, pad=False, left=False):
    if len(text) > width:
        text = text[:width-3] + '...'
    if pad and len(text) < width:
        space = ' ' * (width - len(text))
        if left:
            text = space + text
        else:
            text = text + space
    return text


def name(name, show_failures=True, width=80, out=stderr):
    
    left = 3 * width // 5 - 1
    right = 2 * width // 5 - 1
    
    def namer(stream_in, matcher):
        try:
            (result, stream_out) = matcher()
        except StopIteration:
            if show_failures:
                stream = \
                    _adjust(fmt('stream = {rest}', **s_kargs(stream_in)), 
                            right) 
                str_name = _adjust(name, left // 4, True, True)
                match = _adjust(fmt(' {0} failed', str_name), left, True)
                # Python bug #4618
                print(match + ' ' + stream, file=out, end=str('\n'))
            raise StopIteration
        else:
            try:
                try:
                    rest = fmt('{rest}', **s_kargs(stream_out))
                except StopIteration:
                    rest = '<EOS>'
                stream = _adjust(fmt('stream = {0}', rest), right) 
                str_name = _adjust(name, left // 4, True, True)
                match = _adjust(fmt(' {0} = {1}', str_name, result), left, True)
                # Python bug #4618
                print(match + ' ' + stream, file=out, end=str('\n'))
                return (result, stream_out)
            except Exception as e:
                print('Error in trace', file=out, end=str('\n'))
                print(repr(e), file=out, end=str('\n'))
                return (result, stream_out)
                
    return namer


@contextmanager
def TraceVariables(on=True, show_failures=True, width=80, out=stderr):
    '''
    Add this as a context (`with TraceVariables():`) and you will see 
    debug logging indicating how variables are bound during matching.
    '''
    if on:
        before = _getframe(2).f_locals.copy()
    yield None
    if on:
        after = _getframe(2).f_locals
        for key in after:
            value = after[key]
            if key not in before or value != before[key]:
                try:
                    try:
                        value.wrapper.append(name(key, show_failures, width, out))
                    except AttributeError:
                        value.trace_variables = name(key, show_failures, width, out)
                except: # what exception?
                    print('Unfortunately the following matchers cannot '
                          'be tracked:', end=str('\n'))
                    print(fmt('  {0} = {1}', key, value), end=str('\n'))
                    


