import re


lowercamelcase_regex = re.compile('^([a-z,0-9]+([A-Z,0-9]+[a-z,0-9]*)*)?$')

def is_lowercamelcase_string(expr):
    r'''.. versionadded:: 2.5

    True when `expr` is a string and is lowercamelcase::

        abjad> iotools.is_lowercamelcase_string('fooBar')
        True
    
    False otherwise::

        abjad> iotools.is_lowercamelcase_string('FooBar')
        False

    Return boolean.
    '''

    if not isinstance(expr, str):
        return False

    return bool(lowercamelcase_regex.match(expr))
