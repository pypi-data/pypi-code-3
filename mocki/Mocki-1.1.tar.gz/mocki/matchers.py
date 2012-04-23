# -*- coding: utf-8 -*-
#
#   Copyright 2011 Olivier Kozak
#
#   This file is part of Mocki.
#
#   Mocki is free software: you can redistribute it and/or modify it under the
#   terms of the GNU Lesser General Public License as published by the Free
#   Software Foundation, either version 3 of the License, or (at your option)
#   any later version.
#
#   Mocki is distributed in the hope that it will be useful, but WITHOUT ANY
#   WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#   FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
#   details.
#
#   You should have received a copy of the GNU Lesser General Public License
#   along with Mocki. If not, see <http://www.gnu.org/licenses/>.
#

"""Several convenient matchers.

"""
def anyCall():
    """Matches any call.

    This is a shortcut to AnyCallMatcher.

    """
    return AnyCallMatcher()

class AnyCallMatcher(object):
    """Matches any call.

    This matcher can be used from 2 different places : verifications and stubs.

    To use this matcher from verifications, first create a mock, then invoke
    some calls from it :
        >>> from mocki import Mock

        >>> mock = Mock('theMock')

        >>> mock('1stCall')
        >>> mock('2ndCall')

    Now, we can ask to verify whether or not any call was invoked from it :
        >>> from mocki.expectations import exactly

        >>> mock.verify(anyCall()).invoked(exactly(2))

    In case of verification failure, an assertion error will be raised with a
    debugging-friendly message indicating the problem :
        >>> mock.verify(anyCall()).invoked(exactly(3))
        Traceback (most recent call last):
        ...
        AssertionError: Found 2 matching calls invoked from theMock up to now :
        > theMock('1stCall')
        > theMock('2ndCall')

    To use this matcher from stubs, first create a mock, then stub it to return
    a given value on any call invocation :
        >>> from mocki.stubs import returnValue

        >>> mock = Mock('theMock')

        >>> mock.on(anyCall()).then(returnValue('value'))

    Now, any call invocation will return this given value :
        >>> mock('1stCall')
        'value'

        >>> mock('2ndCall')
        'value'

    """
    def __call__(self, call):
        return True

    def __repr__(self):
        """This matcher's representation :
            >>> matcher = anyCall()

            >>> repr(matcher)
            'anyCall()'

        """
        return "%s()" % anyCall.__name__

def thatCall(*args, **kwargs):
    """Matches a given call.

    This is a shortcut to ThatCallMatcher.

    """
    return ThatCallMatcher(*args, **kwargs)

class ThatCallMatcher(object):
    """Matches a given call.

    This matcher can be used from 2 different places : verifications and stubs.

    To use this matcher from verifications, first create a mock, then invoke
    some calls from it :
        >>> from mocki import Mock

        >>> mock = Mock('theMock')

        >>> mock()
        >>> mock(1, 2, 3)
        >>> mock(x=7, y=8, z=9)
        >>> mock(1, 2, 3, x=7, y=8, z=9)

    Now, we can ask to verify whether or not some given calls were invoked from
    it, using either values or matchers (i.e. any object having a method named
    'matches' that takes a value, like the ones provided by Hamcrest) :
        >>> from hamcrest import equal_to
        >>> from mocki.expectations import once

        >>> mock.verify(thatCall()).invoked(once())

        >>> mock.verify(thatCall(1, 2, equal_to(3))).invoked(once())

        >>> mock.verify(thatCall(x=7, y=8, z=equal_to(9))).invoked(once())

        >>> mock.verify(thatCall(1, 2, equal_to(3), x=7, y=8, z=equal_to(9))).invoked(once())

    In case of verification failure, an assertion error will be raised with a
    debugging-friendly message indicating the problem :
        >>> mock.verify(thatCall(7, 8, 9, x=1, y=2, z=3)).invoked(once())
        Traceback (most recent call last):
        ...
        AssertionError: Found no matching call invoked from theMock up to now :
          theMock()
          theMock(1, 2, 3)
          theMock(x=7, y=8, z=9)
          theMock(1, 2, 3, x=7, y=8, z=9)

    To use this matcher from stubs, first create a mock, then stub it to return
    given values on given call invocations :
        >>> from mocki.stubs import returnValue

        >>> mock = Mock('theMock')

        >>> mock.on(thatCall('1stCall')).then(returnValue('value'))
        >>> mock.on(thatCall('2ndCall')).then(returnValue('anotherValue'))

    Now, any invocation matching to the 1st call will return 'value', while any
    one matching to the 2nd call will return 'anotherValue' :
        >>> mock('1stCall')
        'value'

        >>> mock('2ndCall')
        'anotherValue'

    """
    def __init__(self, *args, **kwargs):
        self.args, self.kwargs = args, kwargs

    def __call__(self, call):
        from mocki import Call

        class Placeholder(object):
            def __init__(self, matcherOrValue):
                self.matcherOrValue = matcherOrValue

            def __eq__(self, value):
                if hasattr(self.matcherOrValue, 'matches'):
                    return self.matcherOrValue.matches(value)
                else:
                    return self.matcherOrValue == value

        def getMatcherCompatibleArgs():
            return [Placeholder(arg) for arg in self.args]

        def getMatcherCompatibleKwargs():
            return dict([(name, Placeholder(kwarg)) for name, kwarg in self.kwargs.items()])

        return call == Call(*getMatcherCompatibleArgs(), **getMatcherCompatibleKwargs())

    def __repr__(self):
        """This matcher's representation :
            >>> repr(thatCall())
            'thatCall()'

            >>> repr(thatCall(1, 2.0, '300'))
            "thatCall(1, 2.0, '300')"

            >>> repr(thatCall(x=7, y=8.0, z='900'))
            "thatCall(x=7, y=8.0, z='900')"

            >>> repr(thatCall(1, 2.0, '300', x=7, y=8.0, z='900'))
            "thatCall(1, 2.0, '300', x=7, y=8.0, z='900')"

        """
        def getArgsAsCsv():
            return ', '.join(map(repr, self.args))

        def getKwargsAsCsv():
            return ", ".join(map(lambda kwarg: '%s=%r' % kwarg, sorted(self.kwargs.items())))

        if len(self.args) == 0 and len(self.kwargs) == 0:
            return '%s()' % (thatCall.__name__)
        elif len(self.kwargs) == 0:
            return '%s(%s)' % (thatCall.__name__, getArgsAsCsv())
        elif len(self.args) == 0:
            return '%s(%s)' % (thatCall.__name__, getKwargsAsCsv())
        else:
            return '%s(%s, %s)' % (thatCall.__name__, getArgsAsCsv(), getKwargsAsCsv())
