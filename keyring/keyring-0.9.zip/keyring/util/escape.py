"""
escape/unescape routines available for backends which need
alphanumeric usernames, services, or other values
"""

import string
import re
import sys

LEGAL_CHARS = (
    getattr(string, 'letters', None) # Python 2
    or getattr(string, 'ascii_letters') # Python 3
) + string.digits

ESCAPE_FMT = "_%02X"

def _escape_char(c):
    "Single char escape. Return the char, escaped if not already legal"
    if isinstance(c, int):
        c = unichr(c)
    return c if c in LEGAL_CHARS else ESCAPE_FMT % ord(c)

def escape(value):
    """
    Escapes given string so the result consists of alphanumeric chars and
    underscore only.
    """
    return "".join(_escape_char(c) for c in value.encode('utf-8'))

def _unescape_code(regex_match):
    ordinal = int(regex_match.group('code'), 16)
    if sys.version_info >= (3,):
        return bytes([ordinal])
    return chr(ordinal)

def unescape(value):
    """
    Inverse of escape.
    """
    re_esc = re.compile(
        # the pattern must be bytes to operate on bytes
        ESCAPE_FMT.replace('%02X', '(?P<code>[0-9A-F]{2})').encode('ascii')
    )
    return re_esc.sub(_unescape_code, value.encode('ascii')).decode('utf-8')
