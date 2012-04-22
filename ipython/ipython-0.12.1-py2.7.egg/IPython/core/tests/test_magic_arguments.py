#-----------------------------------------------------------------------------
# Copyright (C) 2010-2011, IPython Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

from nose.tools import assert_equal, assert_true

from IPython.external import argparse
from IPython.core.magic_arguments import (argument, argument_group, kwds,
    magic_arguments, parse_argstring, real_name)
from IPython.testing.decorators import parametric


@magic_arguments()
@argument('-f', '--foo', help="an argument")
def magic_foo1(self, args):
    """ A docstring.
    """
    return parse_argstring(magic_foo1, args)


@magic_arguments()
def magic_foo2(self, args):
    """ A docstring.
    """
    return parse_argstring(magic_foo2, args)


@magic_arguments()
@argument('-f', '--foo', help="an argument")
@argument_group('Group')
@argument('-b', '--bar', help="a grouped argument")
@argument_group('Second Group')
@argument('-z', '--baz', help="another grouped argument")
def magic_foo3(self, args):
    """ A docstring.
    """
    return parse_argstring(magic_foo3, args)


@magic_arguments()
@kwds(argument_default=argparse.SUPPRESS)
@argument('-f', '--foo', help="an argument")
def magic_foo4(self, args):
    """ A docstring.
    """
    return parse_argstring(magic_foo4, args)


@magic_arguments('frobnicate')
@argument('-f', '--foo', help="an argument")
def magic_foo5(self, args):
    """ A docstring.
    """
    return parse_argstring(magic_foo5, args)


@magic_arguments()
@argument('-f', '--foo', help="an argument")
def magic_magic_foo(self, args):
    """ A docstring.
    """
    return parse_argstring(magic_magic_foo, args)


@magic_arguments()
@argument('-f', '--foo', help="an argument")
def foo(self, args):
    """ A docstring.
    """
    return parse_argstring(foo, args)


@parametric
def test_magic_arguments():
    # Ideally, these would be doctests, but I could not get it to work.
    yield assert_equal(magic_foo1.__doc__, '%foo1 [-f FOO]\n\nA docstring.\n\noptional arguments:\n  -f FOO, --foo FOO  an argument\n')
    yield assert_equal(getattr(magic_foo1, 'argcmd_name', None), None)
    yield assert_equal(real_name(magic_foo1), 'foo1')
    yield assert_equal(magic_foo1(None, ''), argparse.Namespace(foo=None))
    yield assert_true(hasattr(magic_foo1, 'has_arguments'))

    yield assert_equal(magic_foo2.__doc__, '%foo2\n\nA docstring.\n')
    yield assert_equal(getattr(magic_foo2, 'argcmd_name', None), None)
    yield assert_equal(real_name(magic_foo2), 'foo2')
    yield assert_equal(magic_foo2(None, ''), argparse.Namespace())
    yield assert_true(hasattr(magic_foo2, 'has_arguments'))

    yield assert_equal(magic_foo3.__doc__, '%foo3 [-f FOO] [-b BAR] [-z BAZ]\n\nA docstring.\n\noptional arguments:\n  -f FOO, --foo FOO  an argument\n\nGroup:\n  -b BAR, --bar BAR  a grouped argument\n\nSecond Group:\n  -z BAZ, --baz BAZ  another grouped argument\n')
    yield assert_equal(getattr(magic_foo3, 'argcmd_name', None), None)
    yield assert_equal(real_name(magic_foo3), 'foo3')
    yield assert_equal(magic_foo3(None, ''),
                       argparse.Namespace(bar=None, baz=None, foo=None))
    yield assert_true(hasattr(magic_foo3, 'has_arguments'))

    yield assert_equal(magic_foo4.__doc__, '%foo4 [-f FOO]\n\nA docstring.\n\noptional arguments:\n  -f FOO, --foo FOO  an argument\n')
    yield assert_equal(getattr(magic_foo4, 'argcmd_name', None), None)
    yield assert_equal(real_name(magic_foo4), 'foo4')
    yield assert_equal(magic_foo4(None, ''), argparse.Namespace())
    yield assert_true(hasattr(magic_foo4, 'has_arguments'))

    yield assert_equal(magic_foo5.__doc__, '%frobnicate [-f FOO]\n\nA docstring.\n\noptional arguments:\n  -f FOO, --foo FOO  an argument\n')
    yield assert_equal(getattr(magic_foo5, 'argcmd_name', None), 'frobnicate')
    yield assert_equal(real_name(magic_foo5), 'frobnicate')
    yield assert_equal(magic_foo5(None, ''), argparse.Namespace(foo=None))
    yield assert_true(hasattr(magic_foo5, 'has_arguments'))

    yield assert_equal(magic_magic_foo.__doc__, '%magic_foo [-f FOO]\n\nA docstring.\n\noptional arguments:\n  -f FOO, --foo FOO  an argument\n')
    yield assert_equal(getattr(magic_magic_foo, 'argcmd_name', None), None)
    yield assert_equal(real_name(magic_magic_foo), 'magic_foo')
    yield assert_equal(magic_magic_foo(None, ''), argparse.Namespace(foo=None))
    yield assert_true(hasattr(magic_magic_foo, 'has_arguments'))

    yield assert_equal(foo.__doc__, '%foo [-f FOO]\n\nA docstring.\n\noptional arguments:\n  -f FOO, --foo FOO  an argument\n')
    yield assert_equal(getattr(foo, 'argcmd_name', None), None)
    yield assert_equal(real_name(foo), 'foo')
    yield assert_equal(foo(None, ''), argparse.Namespace(foo=None))
    yield assert_true(hasattr(foo, 'has_arguments'))
