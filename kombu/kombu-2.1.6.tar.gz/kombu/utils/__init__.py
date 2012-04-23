"""
kombu.utils
===========

Internal utilities.

:copyright: (c) 2009 - 2012 by Ask Solem.
:license: BSD, see LICENSE for more details.

"""
from __future__ import absolute_import

import sys

from contextlib import contextmanager
from time import sleep
from uuid import UUID, uuid4 as _uuid4, _uuid_generate_random

from .encoding import safe_repr as _safe_repr

try:
    import ctypes
except:
    ctypes = None  # noqa

__all__ = ["EqualityDict", "say", "uuid", "kwdict", "maybe_list",
           "fxrange", "fxrangemax", "retry_over_time",
           "emergency_dump_state", "cached_property",
           "reprkwargs", "reprcall", "nested"]


def eqhash(o):
    try:
        return o.__eqhash__()
    except AttributeError:
        return hash(o)


class EqualityDict(dict):

    def __getitem__(self, key):
        h = eqhash(key)
        if h not in self:
            return self.__missing__(key)
        return dict.__getitem__(self, h)

    def __setitem__(self, key, value):
        return dict.__setitem__(self, eqhash(key), value)

    def __delitem__(self, key):
        return dict.__delitem__(self, eqhash(key))


def say(m, *s):
    sys.stderr.write(str(m) % s + "\n")


def uuid4():
    # Workaround for http://bugs.python.org/issue4607
    if ctypes and _uuid_generate_random:  # pragma: no cover
        buffer = ctypes.create_string_buffer(16)
        _uuid_generate_random(buffer)
        return UUID(bytes=buffer.raw)
    return _uuid4()


def uuid():
    """Generate a unique id, having - hopefully - a very small chance of
    collision.

    For now this is provided by :func:`uuid.uuid4`.
    """
    return str(uuid4())
gen_unique_id = uuid


if sys.version_info >= (2, 6, 5):

    def kwdict(kwargs):
        return kwargs
else:
    def kwdict(kwargs):  # pragma: no cover  # noqa
        """Make sure keyword arguments are not in Unicode.

        This should be fixed in newer Python versions,
        see: http://bugs.python.org/issue4978.

        """
        return dict((key.encode("utf-8"), value)
                        for key, value in kwargs.items())


def maybe_list(v):
    if v is None:
        return []
    if hasattr(v, "__iter__"):
        return v
    return [v]


def fxrange(start=1.0, stop=None, step=1.0, repeatlast=False):
    cur = start * 1.0
    while 1:
        if cur <= stop:
            yield cur
            cur += step
        else:
            if not repeatlast:
                break
            yield cur - step


def fxrangemax(start=1.0, stop=None, step=1.0, max=100.0):
    sum_, cur = 0, start * 1.0
    while 1:
        if sum_ >= max:
            break
        yield cur
        if stop:
            cur = min(cur + step, stop)
        else:
            cur += step
        sum_ += cur


def retry_over_time(fun, catch, args=[], kwargs={}, errback=None,
        max_retries=None, interval_start=2, interval_step=2, interval_max=30):
    """Retry the function over and over until max retries is exceeded.

    For each retry we sleep a for a while before we try again, this interval
    is increased for every retry until the max seconds is reached.

    :param fun: The function to try
    :param catch: Exceptions to catch, can be either tuple or a single
        exception class.
    :keyword args: Positional arguments passed on to the function.
    :keyword kwargs: Keyword arguments passed on to the function.
    :keyword errback: Callback for when an exception in ``catch`` is raised.
        The callback must take two arguments: ``exc`` and ``interval``, where
        ``exc`` is the exception instance, and ``interval`` is the time in
        seconds to sleep next..
    :keyword max_retries: Maximum number of retries before we give up.
        If this is not set, we will retry forever.
    :keyword interval_start: How long (in seconds) we start sleeping between
        retries.
    :keyword interval_step: By how much the interval is increased for each
        retry.
    :keyword interval_max: Maximum number of seconds to sleep between retries.

    """
    retries = 0
    interval_range = fxrange(interval_start,
                             interval_max + interval_start,
                             interval_step, repeatlast=True)

    for retries, interval in enumerate(interval_range):  # for infinity
        try:
            return fun(*args, **kwargs)
        except catch, exc:
            if max_retries is not None and retries > max_retries:
                raise
            if errback:
                errback(exc, interval)
            sleep(interval)


def emergency_dump_state(state, open_file=open, dump=None):
    from pprint import pformat
    from tempfile import mktemp

    if dump is None:
        import pickle
        dump = pickle.dump
    persist = mktemp()
    say("EMERGENCY DUMP STATE TO FILE -> %s <-" % persist)
    fh = open_file(persist, "w")
    try:
        try:
            dump(state, fh, protocol=0)
        except Exception, exc:
            say("Cannot pickle state: %r. Fallback to pformat." % (exc, ))
            fh.write(pformat(state))
    finally:
        fh.flush()
        fh.close()
    return persist


class cached_property(object):
    """Property descriptor that caches the return value
    of the get function.

    *Examples*

    .. code-block:: python

        @cached_property
        def connection(self):
            return Connection()

        @connection.setter  # Prepares stored value
        def connection(self, value):
            if value is None:
                raise TypeError("Connection must be a connection")
            return value

        @connection.deleter
        def connection(self, value):
            # Additional action to do at del(self.attr)
            if value is not None:
                print("Connection %r deleted" % (value, ))

    """

    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        self.__get = fget
        self.__set = fset
        self.__del = fdel
        self.__doc__ = doc or fget.__doc__
        self.__name__ = fget.__name__
        self.__module__ = fget.__module__

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        try:
            return obj.__dict__[self.__name__]
        except KeyError:
            value = obj.__dict__[self.__name__] = self.__get(obj)
            return value

    def __set__(self, obj, value):
        if obj is None:
            return self
        if self.__set is not None:
            value = self.__set(obj, value)
        obj.__dict__[self.__name__] = value

    def __delete__(self, obj):
        if obj is None:
            return self
        try:
            value = obj.__dict__.pop(self.__name__)
        except KeyError:
            pass
        else:
            if self.__del is not None:
                self.__del(obj, value)

    def setter(self, fset):
        return self.__class__(self.__get, fset, self.__del)

    def deleter(self, fdel):
        return self.__class__(self.__get, self.__set, fdel)


def reprkwargs(kwargs, sep=', ', fmt="%s=%s"):
    return sep.join(fmt % (k, _safe_repr(v)) for k, v in kwargs.iteritems())


def reprcall(name, args=(), kwargs=(), sep=', '):
    return "%s(%s%s%s)" % (name, sep.join(map(_safe_repr, args or ())),
                           (args and kwargs) and sep or "",
                           reprkwargs(kwargs, sep))


@contextmanager
def nested(*managers):  # pragma: no cover
    """Combine multiple context managers into a single nested
    context manager."""
    exits = []
    vars = []
    exc = (None, None, None)
    try:
        for mgr in managers:
            exit = mgr.__exit__
            enter = mgr.__enter__
            vars.append(enter())
            exits.append(exit)
        yield vars
    except:
        exc = sys.exc_info()
    finally:
        while exits:
            exit = exits.pop()
            try:
                if exit(*exc):
                    exc = (None, None, None)
            except:
                exc = sys.exc_info()
        if exc != (None, None, None):
            # Don't rely on sys.exc_info() still containing
            # the right information. Another exception may
            # have been raised and caught by an exit method
            raise exc[0], exc[1], exc[2]
