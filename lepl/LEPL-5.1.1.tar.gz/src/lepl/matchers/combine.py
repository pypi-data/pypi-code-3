
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
Matchers that combine sub-matchers (And, Or etc).
'''

# pylint: disable-msg=C0103,W0212
# (consistent interfaces)
# pylint: disable-msg=E1101
# (_args create attributes)
# pylint: disable-msg=R0901, R0904, W0142
# lepl conventions

from abc import ABCMeta
from collections import deque
from operator import __add__

from lepl.matchers.core import Literal
from lepl.matchers.matcher import add_children
from lepl.matchers.support import coerce_, sequence_matcher_factory, \
    trampoline_matcher_factory, to
from lepl.matchers.transform import Transformable
from lepl.support.lib import lmap, fmt, document


# pylint: disable-msg=C0103, W0105
# Python 2.6
#class BaseSearch(metaclass=ABCMeta):
_BaseSearch = ABCMeta('_BaseSearch', (object, ), {})
'''
ABC used to identify matchers.  

Note that graph traversal assumes subclasses are hashable and iterable.
'''

class BaseSearch(_BaseSearch):
    '''
    Common base class (used by smart separators).
    '''


def search_factory(factory):
    '''
    Add the arg processing common to all searching.
    '''
    def new_factory(first, start, stop, rest=None,
                    generator_manager_queue_len=None):
        rest = first if rest is None else rest
        return factory(first, start, stop, rest, generator_manager_queue_len)
    return document(new_factory, factory)


@trampoline_matcher_factory(first=to(Literal), rest=to(Literal))
@search_factory
def DepthFirst(first, start, stop, rest, generator_manager_queue_len):
    '''
    (Post order) Depth first repetition (typically used via `Repeat`).
    '''
    def match(support, stream):
        stack = deque()
        try:
            stack.append((0, [], stream, first._match(stream)))
            stream = None
            while stack:
                (count1, acc1, stream1, generator) = stack[-1]
                extended = False
                if stop == None or count1 < stop:
                    count2 = count1 + 1
                    try:
                        (value, stream2) = yield generator
                        acc2 = acc1 + value
                        stack.append((count2, acc2, stream2, rest._match(stream2)))
                        extended = True
                    except StopIteration:
                        pass
                if not extended:
                    if count1 >= start and (stop == None or count1 <= stop):
                        yield (acc1, stream1)
                    stack.pop()
                while support.generator_manager_queue_len \
                        and len(stack) > support.generator_manager_queue_len:
                    stack.popleft()[3].generator.close()
        finally:
            while stack:
                stack.popleft()[3].generator.close()
            
    return match


@trampoline_matcher_factory(first=to(Literal), rest=to(Literal))
@search_factory
def BreadthFirst(first, start, stop, rest, generator_manager_queue_len):
    '''
    (Level order) Breadth first repetition (typically used via `Repeat`).
    '''
    def match(support, stream):
        queue = deque()
        try:
            queue.append((0, [], stream, first._match(stream)))
            stream = None
            while queue:
                (count1, acc1, stream1, generator) = queue.popleft()
                if count1 >= start and (stop == None or count1 <= stop):
                    yield (acc1, stream1)
                count2 = count1 + 1
                try:
                    while True:
                        (value, stream2) = yield generator
                        acc2 = acc1 + value
                        if stop == None or count2 <= stop:
                            queue.append((count2, acc2, stream2, 
                                          rest._match(stream2)))
                except StopIteration:
                    pass
                while support.generator_manager_queue_len \
                        and len(queue) > support.generator_manager_queue_len:
                    queue.popleft()[3].generator.close()
        finally:
            while queue:
                queue.popleft()[3].generator.close()
            
    return match


@trampoline_matcher_factory(matcher=to(Literal))
def OrderByResultCount(matcher, ascending=True):
    '''
    Modify a matcher to return results in length order.
    '''
    def match(support, stream):
        generator = matcher._match(stream)
        results = []
        try:
            while True:
                # syntax error if this on one line?!
                result = yield generator
                results.append(result)
        except StopIteration:
            pass
        for result in sorted(results,
                             key=lambda x: len(x[0]), reverse=ascending):
            yield result
    return match
            

@sequence_matcher_factory(first=to(Literal), rest=to(Literal))
@search_factory
def DepthNoTrampoline(first, start, stop, rest, generator_manager_queue_len):
    '''
    A more efficient search when all matchers are functions (so no need to
    trampoline).  Depth first (greedy).
    '''
    def matcher(support, stream):
        stack = deque()
        try:
            stack.append((0, [], stream, first._untagged_match(stream)))
            stream = None
            while stack:
                (count1, acc1, stream1, generator) = stack[-1]
                extended = False
                if stop == None or count1 < stop:
                    count2 = count1 + 1
                    try:
                        (value, stream2) = next(generator)
                        acc2 = acc1 + value
                        stack.append((count2, acc2, stream2, 
                                      rest._untagged_match(stream2)))
                        extended = True
                    except StopIteration:
                        pass
                if not extended:
                    if count1 >= start and (stop == None or count1 <= stop):
                        yield (acc1, stream1)
                    stack.pop()
                while support.generator_manager_queue_len \
                        and len(stack) > support.generator_manager_queue_len:
                    stack.popleft()[3].close()
        finally:
            while stack:
                stack.popleft()[3].close()
            
    return matcher
            
            
@sequence_matcher_factory(first=to(Literal), rest=to(Literal))
@search_factory
def BreadthNoTrampoline(first, start, stop, rest, generator_manager_queue_len):
    '''
    A more efficient search when all matchers are functions (so no need to
    trampoline).  Breadth first (non-greedy).
    '''
    def matcher(support, stream):
        queue = deque()
        try:
            queue.append((0, [], stream, first._untagged_match(stream)))
            stream = None
            while queue:
                (count1, acc1, stream1, generator) = queue.popleft()
                if count1 >= start and (stop == None or count1 <= stop):
                    yield (acc1, stream1)
                count2 = count1 + 1
                for (value, stream2) in generator:
                    acc2 = acc1 + value
                    if stop == None or count2 <= stop:
                        queue.append((count2, acc2, stream2, 
                                      rest._untagged_match(stream2)))
                while support.generator_manager_queue_len \
                        and len(queue) > support.generator_manager_queue_len:
                    queue.popleft()[3].close()
        finally:
            while queue:
                queue.popleft()[3].close()
            
    return matcher


add_children(BaseSearch, DepthFirst, BreadthFirst, \
             DepthNoTrampoline, BreadthNoTrampoline)

                
class _BaseCombiner(Transformable):
    '''
    Support for `And` and `Or`.
    '''
    
    def __init__(self, *matchers):
        super(_BaseCombiner, self).__init__()
        self._args(matchers=lmap(coerce_, matchers))
        
    def compose(self, wrapper):
        '''
        Generate a new instance with the composed function from the Transform.
        '''
        copy = type(self)(*self.matchers)
        copy.wrapper = self.wrapper.compose(wrapper)
        return copy
    

@trampoline_matcher_factory(args_=to(Literal))
def And(*matchers):
    '''
    Match one or more matchers in sequence (**&**).
    It can be used indirectly by placing ``&`` between matchers.
    '''
    def match(support, stream_in):
        if matchers:
            stack = deque([([], 
                            matchers[0]._match(stream_in), 
                            matchers[1:])])
            append = stack.append
            pop = stack.pop
            stream_in = None
            try:
                while stack:
                    (result, generator, queued) = pop()
                    try:
                        (value, stream_out) = yield generator
                        append((result, generator, queued))
                        if queued:
                            append((result+value, 
                                    queued[0]._match(stream_out), 
                                    queued[1:]))
                        else:
                            yield (result+value, stream_out)
                    except StopIteration:
                        pass
            finally:
                for (result, generator, queued) in stack:
                    generator.generator.close()
    return match


@sequence_matcher_factory(args_=to(Literal))
def AndNoTrampoline(*matchers):
    '''
    Used as an optimisation when sub-matchers do not require the trampoline.
    '''
    def matcher(support, stream_in):
        if matchers:
            stack = deque([([], matchers[0]._untagged_match(stream_in), matchers[1:])])
            append = stack.append
            pop = stack.pop
            try:
                while stack:
                    (result, generator, queued) = pop()
                    try:
                        (value, stream_out) = next(generator)
                        append((result, generator, queued))
                        if queued:
                            append((result+value, 
                                    queued[0]._untagged_match(stream_out), 
                                    queued[1:]))
                        else:
                            yield (result+value, stream_out)
                    except StopIteration:
                        pass
            finally:
                for (result, generator, queued) in stack:
                    generator.close()
                    
    return matcher
        
        
@trampoline_matcher_factory(args_=to(Literal))
def Or(*matchers):
    '''
    Match one of the given matchers (**|**).
    It can be used indirectly by placing ``|`` between matchers.
    
    Matchers are tried from left to right until one succeeds; backtracking
    will try more from the same matcher and, once that is exhausted,
    continue to the right.  String arguments will be coerced to 
    literal matches.
    '''
    def match(support, stream_in):
        for matcher in matchers:
            generator = matcher._match(stream_in)
            try:
                while True:
                    yield (yield generator)
            except StopIteration:
                pass
    return match


@sequence_matcher_factory(args_=to(Literal))
def OrNoTrampoline(*matchers):
    '''
    Used as an optimisation when sub-matchers do not require the trampoline.
    '''
    def match(support, stream_in):
        for matcher in matchers:
            for result in matcher._untagged_match(stream_in):
                yield result
    return match

       
@trampoline_matcher_factory()
def First(*matchers):
    '''
    Match the first successful matcher only (**%**).
    It can be used indirectly by placing ``%`` between matchers.
    Note that backtracking for the first-selected matcher will still occur.

    Matchers are tried from left to right until one succeeds; backtracking
    will try more from the same matcher (only).  String arguments will be 
    coerced to literal matches.
    '''
    def match(support, stream):
        matched = False
        for matcher in support.matchers:
            generator = matcher._match(stream)
            try:
                while True:
                    yield (yield generator)
                    matched = True
            except StopIteration:
                pass
            if matched:
                break

    return match


@trampoline_matcher_factory(args_=to(Literal))
def Difference(matcher, exclude, count=-1):
    '''
    Match with `matcher`, but exclude any matches that would be made by
    `exclude`.  This is implemented by comparing the remaining stream after 
    matching, so will not be affected by any transform associated with
    `exclude`.  The `count` parameter gives the number of different matches
    from `exclude`.  By default (-1) all matches are used.  A positive
    value restricts that to the number given.
    '''
    def match(support, stream, count=count):
        
        # by default use a set; fall back to a list for unhashable streams
        bad = [None]
        grow_bad = None
        def append_bad(value, bad=bad):
            bad[0].append(value)
        def add_bad(value, bad=bad):
            if bad[0] is None:
                bad[0] = set()
            try:
                bad[0].add(value)
            except TypeError:
                assert not bad[0]
                bad[0] = []
                grow_bad = append_bad
                grow_bad(value)
        grow_bad = add_bad
        
        generator = matcher._match(stream)
        while True:
            (value, stream1) = yield generator
            
            if bad[0] is None: # build bad on demand, once
                bad_generator = exclude._match(stream)
                try:
                    while count:
                        (excluded, stream2) = yield bad_generator
                        support._debug(fmt('Exclude: {0!r}', excluded))
                        grow_bad(stream2)
                        # limit number of matchers, if requested 
                        count -= 1
                except StopIteration:
                    pass # all matches for exclude
                
            if stream1 not in bad[0]:
                yield (value, stream1)
            else:
                support._debug(fmt('Excluding: {0!r}', value))
                
    return match


@trampoline_matcher_factory(args_=to(Literal))
def Limit(match, count=1):
    '''
    Limit the backtracking for a given matcher.  A negative `count` means no
    limit.
    '''
    def matcher(support, stream, count=count):
        generator = match._match(stream)
        try:
            while count:
                yield (yield generator)
                count -= 1
        except StopIteration:
            pass
    return matcher
