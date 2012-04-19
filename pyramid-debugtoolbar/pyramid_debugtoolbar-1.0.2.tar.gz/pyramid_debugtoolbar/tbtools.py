# -*- coding: utf-8 -*-
"""
    werkzeug.debug.tbtools
    ~~~~~~~~~~~~~~~~~~~~~~

    This module provides various traceback related utility functions.

    :copyright: (c) 2011 by the Werkzeug Team, see AUTHORS for more details.
    :license: BSD.
"""
import re
import os
import sys
import inspect
import traceback
import codecs
from tokenize import TokenError

from pyramid.decorator import reify
from pyramid.renderers import render

from pyramid_debugtoolbar.compat import text_type
from pyramid_debugtoolbar.compat import string_types
from pyramid_debugtoolbar.compat import text_
from pyramid_debugtoolbar.compat import native_
from pyramid_debugtoolbar.compat import exec_
from pyramid_debugtoolbar.compat import xrange_
from pyramid_debugtoolbar.console import Console
from pyramid_debugtoolbar.utils import escape
from pyramid_debugtoolbar.utils import STATIC_PATH
from pyramid_debugtoolbar.utils import ROOT_ROUTE_NAME
from pyramid_debugtoolbar.utils import EXC_ROUTE_NAME

_coding_re = re.compile(r'coding[:=]\s*([-\w.]+)')
_line_re = re.compile(r'^(.*?)$(?m)')
_funcdef_re = re.compile(r'^(\s*def\s)|(.*(?<!\w)lambda(:|\s))|^(\s*@)')
UTF8_COOKIE = '\xef\xbb\xbf'

system_exceptions = (SystemExit, KeyboardInterrupt)
try:
    system_exceptions += (GeneratorExit,)
except NameError:
    pass

FRAME_HTML = text_('''\
<div class="frame" id="frame-%(id)d">
  <h4>File <cite class="filename">"%(filename)s"</cite>,
      line <em class="line">%(lineno)s</em>,
      in <code class="function">%(function_name)s</code></h4>
  <pre>%(current_line)s</pre>
</div>
''')

SOURCE_TABLE_HTML = text_('<table class=source>%s</table>')

SOURCE_LINE_HTML = text_('''\
<tr class="%(classes)s">
  <td class=lineno>%(lineno)s</td>
  <td>%(code)s</td>
</tr>
''')


def get_current_traceback(ignore_system_exceptions=False,
                          show_hidden_frames=False, skip=0):
    """Get the current exception info as `Traceback` object.  Per default
    calling this method will reraise system exceptions such as generator exit,
    system exit or others.  This behavior can be disabled by passing `False`
    to the function as first parameter.
    """
    info = sys.exc_info()
    return get_traceback(info,
                         ignore_system_exceptions=ignore_system_exceptions,
                         show_hidden_frames=show_hidden_frames, skip=skip)

def get_traceback(info, ignore_system_exceptions=False,
                  show_hidden_frames=False, skip=0):
    exc_type, exc_value, tb = info
    if ignore_system_exceptions and exc_type in system_exceptions:
        raise
    for x in xrange_(skip):
        if tb.tb_next is None:
            break
        tb = tb.tb_next
    tb = Traceback(exc_type, exc_value, tb)
    if not show_hidden_frames:
        tb.filter_hidden_frames()
    return tb


class Line(object):
    """Helper for the source renderer."""
    __slots__ = ('lineno', 'code', 'in_frame', 'current')

    def __init__(self, lineno, code):
        self.lineno = lineno
        self.code = code
        self.in_frame = False
        self.current = False

    def classes(self):
        rv = ['line']
        if self.in_frame:
            rv.append('in-frame')
        if self.current:
            rv.append('current')
        return rv
    classes = property(classes)

    def render(self):
        return SOURCE_LINE_HTML % {
            'classes':      text_(' '.join(self.classes)),
            'lineno':       self.lineno,
            'code':         escape(self.code)
        }


class Traceback(object):
    """Wraps a traceback."""

    def __init__(self, exc_type, exc_value, tb):
        self.exc_type = exc_type
        self.exc_value = exc_value
        if not isinstance(exc_type, str):
            exception_type = exc_type.__name__
            if exc_type.__module__ not in ('__builtin__', 'exceptions'):
                exception_type = exc_type.__module__ + '.' + exception_type
        else:
            exception_type = exc_type
        self.exception_type = exception_type

        # we only add frames to the list that are not hidden.  This follows
        # the the magic variables as defined by paste.exceptions.collector
        self.frames = []
        while tb:
            self.frames.append(Frame(exc_type, exc_value, tb))
            tb = tb.tb_next

    def filter_hidden_frames(self):
        """Remove the frames according to the paste spec."""
        if not self.frames:
            return

        new_frames = []
        hidden = False
        for frame in self.frames:
            hide = frame.hide
            if hide in ('before', 'before_and_this'):
                new_frames = []
                hidden = False
                if hide == 'before_and_this':
                    continue
            elif hide in ('reset', 'reset_and_this'):
                hidden = False
                if hide == 'reset_and_this':
                    continue
            elif hide in ('after', 'after_and_this'):
                hidden = True
                if hide == 'after_and_this':
                    continue
            elif hide or hidden:
                continue
            new_frames.append(frame)

        # if we only have one frame and that frame is from the codeop
        # module, remove it.
        if len(new_frames) == 1 and self.frames[0].module == 'codeop':
            del self.frames[:]

        # if the last frame is missing something went terrible wrong :(
        elif self.frames[-1] in new_frames:
            self.frames[:] = new_frames

    def is_syntax_error(self):
        """Is it a syntax error?"""
        return isinstance(self.exc_value, SyntaxError)
    is_syntax_error = property(is_syntax_error)

    def exception(self):
        """String representation of the exception."""
        buf = traceback.format_exception_only(self.exc_type, self.exc_value)
        return native_(''.join(buf).strip(), 'utf-8', 'replace')
    exception = property(exception)

    def log(self, logfile=None):
        """Log the ASCII traceback into a file object."""
        if logfile is None:
            logfile = sys.stderr
        tb = self.plaintext.encode('utf-8', 'replace').rstrip() + '\n'
        logfile.write(tb)

    def paste(self, lodgeit_url):
        """Create a paste and return the paste id."""
        from xmlrpclib import ServerProxy
        srv = ServerProxy('%sxmlrpc/' % lodgeit_url)
        return srv.pastes.newPaste('pytb', self.plaintext)

    def render_summary(self, include_title=True, request=None):
        """Render the traceback for the interactive console."""
        title = ''
        frames = []
        classes = ['traceback']
        if not self.frames:
            classes.append('noframe-traceback')

        if include_title:
            if self.is_syntax_error:
                title = text_('Syntax Error')
            else:
                title = text_('Traceback <em>(most recent call last)</em>:')

        for frame in self.frames:
            frames.append(
                text_('<li%s>%s') % (
                frame.info and text_(' title="%s"' % escape(frame.info)) or
                    text_(''),
                frame.render()
            ))

        if self.is_syntax_error:
            description_wrapper = text_('<pre class=syntaxerror>%s</pre>')
        else:
            description_wrapper = text_('<blockquote>%s</blockquote>')

        vars = {
            'classes':      text_(' '.join(classes)),
            'title':        title and text_('<h3>%s</h3>' % title) or text_(''),
            'frames':       text_('\n'.join(frames)),
            'description':  description_wrapper % escape(self.exception),
        }
        return render(
            'pyramid_debugtoolbar:templates/exception_summary.dbtmako',
            vars, request=request)

    def render_full(self, request, lodgeit_url=None):
        """Render the Full HTML page with the traceback info."""
        static_path = request.static_url(STATIC_PATH)
        root_path = request.route_url(ROOT_ROUTE_NAME)
        exc = escape(self.exception)
        summary = self.render_summary(include_title=False, request=request)
        qs = {'token':request.exc_history.token, 'tb':str(self.id)}
        url = request.route_url(EXC_ROUTE_NAME, _query=qs)
        evalex = request.exc_history.eval_exc
        vars = {
            'evalex':           evalex and 'true' or 'false',
            'console':          'false',
            'lodgeit_url':      escape(lodgeit_url),
            'title':            exc,
            'exception':        exc,
            'exception_type':   escape(self.exception_type),
            'summary':          summary,
            'plaintext':        self.plaintext,
            'plaintext_cs':     re.sub('-{2,}', '-', self.plaintext),
            'traceback_id':     self.id,
            'static_path':      static_path,
            'token':            request.exc_history.token,
            'root_path':        root_path,
            'url':              url,
        }
        return render('pyramid_debugtoolbar:templates/exception.dbtmako',
                      vars, request=request)

    def generate_plaintext_traceback(self):
        """Like the plaintext attribute but returns a generator"""
        yield text_('Traceback (most recent call last):')
        for frame in self.frames:
            yield text_('  File "%s", line %s, in %s' % (
                frame.filename,
                frame.lineno,
                frame.function_name
            ))
            yield text_('    ' + frame.current_line.strip())
        yield self.exception

    @reify
    def plaintext(self):
        return text_('\n'.join(self.generate_plaintext_traceback()))

    id = property(lambda x: id(x))


class Frame(object):
    """A single frame in a traceback."""

    def __init__(self, exc_type, exc_value, tb):
        self.lineno = tb.tb_lineno
        self.function_name = tb.tb_frame.f_code.co_name
        self.locals = tb.tb_frame.f_locals
        self.globals = tb.tb_frame.f_globals

        fn = inspect.getsourcefile(tb) or inspect.getfile(tb)
        if fn[-4:] in ('.pyo', '.pyc'):
            fn = fn[:-1]
        # if it's a file on the file system resolve the real filename.
        if os.path.isfile(fn):
            fn = os.path.realpath(fn)
        self.filename = fn
        self.module = self.globals.get('__name__')
        self.loader = self.globals.get('__loader__')
        self.code = tb.tb_frame.f_code

        # support for paste's traceback extensions
        self.hide = self.locals.get('__traceback_hide__', False)
        info = self.locals.get('__traceback_info__')
        if info is not None:
            try:
                info = unicode(info)
            except UnicodeError:
                info = str(info).decode('utf-8', 'replace')
        self.info = info

    def render(self):
        """Render a single frame in a traceback."""
        return FRAME_HTML % {
            'id':               self.id,
            'filename':         escape(self.filename),
            'lineno':           self.lineno,
            'function_name':    escape(self.function_name),
            'current_line':     escape(self.current_line.strip())
        }

    def get_annotated_lines(self):
        """Helper function that returns lines with extra information."""
        lines = [Line(idx + 1, x) for idx, x in enumerate(self.sourcelines)]

        # find function definition and mark lines
        if hasattr(self.code, 'co_firstlineno'):
            lineno = self.code.co_firstlineno - 1
            while lineno > 0:
                if _funcdef_re.match(lines[lineno].code):
                    break
                lineno -= 1
            try:
                offset = len(inspect.getblock([x.code + '\n' for x
                                               in lines[lineno:]]))
            except TokenError:
                offset = 0
            for line in lines[lineno:lineno + offset]:
                line.in_frame = True

        # mark current line
        try:
            lines[self.lineno - 1].current = True
        except IndexError:
            pass

        return lines

    def render_source(self):
        """Render the sourcecode."""
        return SOURCE_TABLE_HTML % text_('\n'.join(line.render() for line in
                                              self.get_annotated_lines()))

    def eval(self, code, mode='single'):
        """Evaluate code in the context of the frame."""
        if isinstance(code, string_types):
            if isinstance(code, text_type):
                code = UTF8_COOKIE + code.encode('utf-8')
            code = compile(code, '<interactive>', mode)
        if mode != 'exec':
            return eval(code, self.globals, self.locals)
        exec_(code, self.globals, self.locals)

    @reify
    def sourcelines(self):
        """The sourcecode of the file as list of unicode strings."""
        # get sourcecode from loader or file
        source = None
        if self.loader is not None:
            try:
                if hasattr(self.loader, 'get_source'):
                    source = self.loader.get_source(self.module)
                elif hasattr(self.loader, 'get_source_by_code'):
                    source = self.loader.get_source_by_code(self.code)
            except Exception:
                # we munch the exception so that we don't cause troubles
                # if the loader is broken.
                pass

        if source is None:
            try:
                f = open(self.filename)
            except IOError:
                return []
            try:
                source = f.read()
            finally:
                f.close()

        # already unicode?  return right away
        if isinstance(source, text_type):
            return source.splitlines()

        # yes. it should be ascii, but we don't want to reject too many
        # characters in the debugger if something breaks
        charset = 'utf-8'
        if source.startswith(UTF8_COOKIE):
            source = source[3:]
        else:
            for idx, match in enumerate(_line_re.finditer(source)):
                match = _line_re.search(match.group())
                if match is not None:
                    charset = match.group(1)
                    break
                if idx > 1:
                    break

        # on broken cookies we fall back to utf-8 too
        try:
            codecs.lookup(charset)
        except LookupError:
            charset = 'utf-8'

        return source.decode(charset, 'replace').splitlines()

    @property
    def current_line(self):
        try:
            return self.sourcelines[self.lineno - 1]
        except IndexError:
            return text_('')

    @reify
    def console(self):
        return Console(self.globals, self.locals)

    id = property(lambda x: id(x))
