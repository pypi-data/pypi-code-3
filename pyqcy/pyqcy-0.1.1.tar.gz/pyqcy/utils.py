"""
Utility module.
"""
import functools
import inspect
import collections


def optional_args(decor):
    """Decorator for decorators (sic) that are intended to take
    optional arguments. It supports decorators written both as
    classes or functions, as long as they are "doubly-callable".
    For classes, this means implementing `__call__`, while
    functions must return a function that returns a function
    that accepts a function... which is obvious, of course.
    """
    @functools.wraps(decor)
    def wrapped(*args, **kwargs):
        one_arg = len(args) == 1 and not kwargs
        if one_arg and inspect.isfunction(args[0]):
            decor_instance = decor()
            return decor_instance(args[0])
        else:
            return decor(*args, **kwargs)

    return wrapped


def recursive(func):
    ''' Constructs a function that which recursively applies given callable
    to objects, regardless of whether they are lists (iterables)
    or dictionaries (mapping). It can be thought of as recursive, curried `map`
    for lists, and/or equivalent for dicts.
    '''
    @functools.wraps(func)
    def recursive_func(obj, *args, **kwargs):
        if isinstance(obj, collections.Mapping):
            return dict((k, recursive_func(v, *args, **kwargs))
                        for (k, v) in obj.iteritems())
        if isinstance(obj, (tuple, list)):
            iter_cls = tuple if isinstance(obj, tuple) else list
            return iter_cls([recursive_func(item, *args, **kwargs)
                             for item in obj])
        return func(obj)
    
    return recursive_func