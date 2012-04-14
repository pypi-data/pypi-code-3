# IDLEX EXTENSION
##    """
##    Copyright(C) 2011 The Board of Trustees of the University of Illinois.
##    All rights reserved.
##
##    Developed by:   Roger D. Serwy
##                    University of Illinois
##
##    Permission is hereby granted, free of charge, to any person obtaining
##    a copy of this software and associated documentation files (the
##    "Software"), to deal with the Software without restriction, including
##    without limitation the rights to use, copy, modify, merge, publish,
##    distribute, sublicense, and/or sell copies of the Software, and to
##    permit persons to whom the Software is furnished to do so, subject to
##    the following conditions:
##
##    + Redistributions of source code must retain the above copyright
##      notice, this list of conditions and the following disclaimers.
##    + Redistributions in binary form must reproduce the above copyright
##      notice, this list of conditions and the following disclaimers in the
##      documentation and/or other materials provided with the distribution.
##    + Neither the names of Roger D. Serwy, the University of Illinois, nor
##      the names of its contributors may be used to endorse or promote
##      products derived from this Software without specific prior written
##      permission.
##
##    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
##    OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
##    MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
##    IN NO EVENT SHALL THE CONTRIBUTORS OR COPYRIGHT HOLDERS BE LIABLE FOR
##    ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
##    CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH
##    THE SOFTWARE OR THE USE OR OTHER DEALINGS WITH THE SOFTWARE.
##
##
##
##    Run Selection Extension - run parts of source code in IDLE
##
##    About:
##
##    This code executes the currently highlighted text
##    from the editor in the shell window, or a single line.
##
##    How to Use:
##
##        Run Selection or Line:
##
##        * To run a single statement (including indented code)
##          move cursor to the line and press F9.
##
##        * To run a selection of statements, select the statements
##          to run and press F9
##
##
##        Run Region
##
##        A Run Region behaves like a selection, but it is tagged
##        with a blue background. A group of commands can be tagged
##        as a Run Region and executed using Ctrl+F9.
##
##        Tag/Join Run Region
##          - Tags a line or selection of code as a Run Region
##          - Can join separate Run Regions
##
##        Untag/Split Run Region
##          - Untags a line or selection of code
##          - Can split a Run Region into two separate Run Regions
##
##    """
config_extension_def = """

[RunSelection]
enable=1
enable_shell=0
enable_editor=1
[RunSelection_cfgBindings]
run-region=<F9>
"""

TAG_REGIONS = False  # allow for selections to be tagged (EXPERIMENTAL)
TAG_REGIONS = True

if TAG_REGIONS:
    config_extension_def += """
run-tagged=<Control-F9>
region-tagged-join=<Control-j>
region-tagged-split=<Control-k>
"""

RUNREGION_BACKGROUND = '#BBE0FF'    # background color for a runregion

import sys

if sys.version < '3':
    from Tkinter import *
    import tkMessageBox
else:
    from tkinter import *
    import tkinter.messagebox as tkMessageBox
    xrange = range
    

from idlelib.EditorWindow import classifyws
from idlelib.configHandler import idleConf

import ast
import re

jn = lambda x,y: '%i.%i' % (x,y)              # join integers to text coordinates
sp = lambda x: list(map(int, x.split('.')))   # convert tkinter Text coordinate to a line and column tuple

def index(text, marker='insert', lineoffset=0):
    """ helper function to split a marker location of a text object """
    line, col = sp(text.index(marker))
    return (line + lineoffset, col)


#---------------------
# AST helper functions
#---------------------

def find_sel_range(y, sline, eline=None, first=None, last=None):
    """ Returns the first and last nodes in AST for given line range. """
    if not (hasattr(y, 'body') or hasattr(y, 'orelse')):
        return first, last

    if eline is None:
        eline = sline

    def helper(M, first=None, last=None):
        for n, stmt in enumerate(M):
            if sline <= stmt.lineno:
                if stmt.lineno <= eline:
                    last = (M, n)  # last found statement in range
                    if first is None:
                        first = (M, n) # first found statement in range
            first, last = find_sel_range(stmt, sline, eline, first, last)
        return first, last

    if hasattr(y, 'body'):
        M = y.body
        first, last = helper(M, first, last)
    if hasattr(y, 'orelse'):
        M = y.orelse
        first, last = helper(M, first, last)

    return first, last

def get_module_endline(y):
    if not hasattr(y, 'body'):
        return y.lineno
    lastnode = y.body[-1]
    if hasattr(lastnode, 'orelse'):
        if lastnode.orelse:
            lastnode = lastnode.orelse[-1]
    v = get_module_endline(lastnode)
    if v is None:
        return lastnode.lineno
    else:
        return v

#---------------
# The extension
#----------------

class RunSelection(object):

    _menu = [None,
             ('Run Selection or Line', '<<run-region>>')]

    if TAG_REGIONS:
        _menu.extend([
                ('Run Tagged Region', '<<run-tagged>>'),
                ('Tag/Join Region', '<<region-tagged-join>>'),
                ('Untag/Split Region', '<<region-tagged-split>>')])
    menudefs = [
        ('run', _menu),
       ]

    def __init__(self, editwin):
        self.editwin = editwin
        text = self.text = editwin.text

        text.tag_configure('RUNREGION', **{'background':RUNREGION_BACKGROUND,
                                           #'borderwidth':2,
                                           #'relief':GROOVE,
                                           })
        text.tag_raise('sel')
        text.tag_raise('ERROR')

        specs = [('Run Selection or Line', '<<run-region>>')]
        for m in specs:
            if m not in editwin.rmenu_specs:
                editwin.rmenu_specs.append(m)


    #---------------------------------
    # Event Handlers
    #---------------------------------

    def run_region_event(self, event=None):
        # <<run-region>> was triggered

        sel = self.get_sel_range()
        if sel:
            # Run the selected code.
            code_region = self.send_code(*sel)
        else:
            # Run the code on current line
            lineno, col = sp(self.text.index('insert'))
            code_region = self.send_code(lineno, lineno)

        self.text.tag_remove('sel', '1.0', END)
        if code_region:
            self.shrink_region(*code_region, tag='sel')


    def run_tagged_event(self, event=None):
        # <<run-tagged>> was triggered
        lineno, col = sp(self.text.index('insert'))
        r = self.get_tagged_region(lineno)
        if r:
            # Run the code contained in the tagged run region.
            self.untag_entire_region(r[0])
            self.tag_run_region(*r)
            self.adjust_cursor(*r)
            code_region = self.send_code(*r)
            if code_region:
                self.shrink_region(*code_region, tag='RUNREGION')

    def region_tagged_join_event(self, event=None):
        sel = self.get_sel_range()
        if sel:
            self.tag_run_region(*sel)
            self.clear_sel()
        else:
            lineno, col = sp(self.text.index('insert'))
            self.tag_run_region(lineno, lineno)
        return "break"

    def region_tagged_split_event(self, event=None):
        sel = self.get_sel_range()
        if sel:
            self.untag_run_region(*sel)
            self.clear_sel()
        else:
            lineno, col = sp(self.text.index('insert'))
            self.untag_run_region(lineno, lineno)
        return "break"


    #--------------------------
    # Tag/Untag Run Region Code
    #--------------------------

    def _tag_region(self, first, last, tag):
        self.text.tag_add(tag, '%i.0' % (first),
                          '%i.0' % (last+1))

    def _untag_region(self, first, last, tag):
        self.text.tag_remove(tag, '%i.0' % (first),
                          '%i.0' % (last+1))

    def get_tagged_region(self, line):
        """ Return the Region at line number.

            None             If no region
            (first, last)    Line numbers

        """
        if line < 0:
            return None

        text = self.text
        loc = '%i.0+1c' % line
        p = text.tag_prevrange("RUNREGION", loc)
        if p:
            if text.compare(p[0], '<=', loc) and \
               text.compare(p[1], '>=', loc):
                first, col = sp(p[0])
                last, col = sp(p[1])
                return first, last-1
        return None


    def tag_run_region(self, first, last):
        """ Tag a given span of lines as a Run Region """
        if first > last:
            first, last = last, first

        tree = self.get_tree()
        active = self.get_active_statements(first, last, tree=tree)

        if active:
            # Active statements are in the given range.
            # Tag this range.
            mod, firstline, lastline, offset = active
            self._tag_region(firstline, lastline, 'RUNREGION')

        # Check if joining regions. This may happen
        #  if the user expanded an existing region
        #  but the expansion contains no active code.
        firstregion = self.get_tagged_region(first)
        lastregion = self.get_tagged_region(last)

        if firstregion:
            if lastregion:
                # join the separated run regions
                r1 = self.get_active_statements(*firstregion, tree=tree)
                r2 = self.get_active_statements(*lastregion, tree=tree)
                # make sure both regions at same indentation
                if r1 and r2:
                    if r1[3] == r2[3]:  # make sure offsets are same
                        firstline = firstregion[0]
                        lastline = lastregion[0]
                        self._tag_region(firstline, lastline, 'RUNREGION')
                    else:
                        #print('wrong offsets for join')
                        msg = 'Could not join regions due to indentation mismatch.'
                        self.show_error('Join region error', msg)
                        pass
            else:
                # expand downward
                self.tag_run_region(firstregion[0], last)

    def untag_run_region(self, first, last):
        """ Untags a run region over the given range of lines. """
        if first > last:
            first, last = last, first

        tag = 'RUNREGION'

        r1 = self.get_tagged_region(first)
        r2 = self.get_tagged_region(last)
                
        self._untag_region(first, last, tag)  # untag the given range

        T = self.get_tree()

        # shrink the surrounding run regions if they exist
        firstregion = self.get_tagged_region(first-1)
        lastregion = self.get_tagged_region(last+2)

        def retag(region):
            if region is None:
                return
            F, L = region
            self._untag_region(F, L, tag)
            active = self.get_active_statements(F, L, tree=T)
            if active:
                mod, F, L, offset = active
                self._tag_region(F, L, tag)

        retag(firstregion)
        retag(lastregion)

        # If RUNREGION tag still exists within [first, last]
        # then restore prior tags
        t1 = self.text.tag_names('%i.0' % first)
        t2 = self.text.tag_names('%i.0-1c' % last)

        restore = False
        if first != last:
            if tag in t1 or tag in t2:
                #print('could not untag')
                restore = True
        else:
            if tag in t1:
                #print('could not untag2')
                restore = True
        if restore:
            msg = 'Could not untag because line %i is tagged.' % firstregion[0]
            self._untag_region(first, last, tag)
            retag(r1)
            retag(r2)
            self.show_error('Split region error', msg)

    def untag_entire_region(self, line):
        """ Untags an entire region containing the given line. """
        r = self.get_tagged_region(line)
        if r:
            self.untag_run_region(*r)


    def shrink_region(self, first, last, tag):
        text = self.text
        if first == last:
            endsel = '%i.0 lineend' % first
        else:
            endsel = '%i.0' % (last + 1)
        text.tag_add(tag, '%i.0' % first, endsel)


    #---------------------
    # Editor-handling code
    #---------------------

    def adjust_cursor(self, start, end):
        """ Move the cursor in case run region shrinks """
        text = self.text
        if text.compare('insert', '>', '%i.0' % end):
            text.mark_set('insert', '%i.0' % end + ' lineend')
        elif text.compare('insert', '<', '%i.0' % start):
            text.mark_set('insert','%i.0' % start)

    def get_sel_range(self):
        """ Return the first and last line containing the selection """
        text = self.text
        sel_first = text.index('sel.first')
        if sel_first:
            firstline, firstcol = sp(sel_first)
            lastline, lastcol = sp(text.index('sel.last'))
            if lastcol == 0:
                lastline -= 1
            return firstline, lastline
        else:
            return None

    def clear_sel(self):
        self.text.tag_remove('sel', '1.0', 'end')

    def focus_editor(self, ev=None):
        self.editwin.text.focus_set()
        self.editwin.top.lift()


    def show_error(self, title, msg):
        tkMessageBox.showerror(title=title,
                               message=msg,
                               parent = self.text)
        pass

    #-------------
    # Code-parsing
    #-------------

    def send_code(self, first, last):
        """ Sends the code contained in the selection """
        text = self.text
        active = self.get_active_statements(first, last)
        if active is not None:
            mod, firstline, lastline, offset = active
            code = compile(mod, '<string>', 'exec')
            # return the code that can be executed
            if firstline != lastline:
                msg = '# Run Region [%i-%i]' % (firstline, lastline)
            else:
                msg = '# Run Region [line %i]' % firstline

            src = text.get('%i.0' % firstline,
                           '%i.0' % (lastline + 1))

            if offset:   # dedent indented code
                src = re.sub(r"(?<![^\n]) {%i,%i}" % (offset, offset), "", src)

            shell = self.editwin.flist.open_shell()
            src_c = shell.interp.compile(src, '<string>', 'exec')
            self.shell_run(src_c, message=msg)
            #self.shell_run(code, message=msg)
            return  firstline, lastline
        else:
            return None


    def get_tree(self):
        src = self.text.get('1.0', END)
        try:
            tree = ast.parse(src)
            return tree
        except Exception as e:
            self.handle_error(e)
            return None

    def get_active_statements(self, first, last, tree=None):
        """ Parse the AST to get the code in the selection range """

        if tree is None:
            tree = self.get_tree()

        sline = first
        eline = last
        F, L = find_sel_range(tree, sline, eline)

        if F is not None:
            fbody, findex = F
            body = []
            lastn = None
            for n in range(findex, len(fbody)):
                if fbody[n].lineno <= eline:
                    body.append(fbody[n])
                    lastn = n
            mod = ast.Module()
            mod.body = body

            lineno = body[0].lineno
            offset = body[0].col_offset
            lastline = get_module_endline(mod)

            return mod, lineno, lastline, offset
        else:
            return None

    #--------------------
    # Shell-handling code
    #--------------------

    def shell_run(self, code, message=None):
        """ Returns True is code is actually executed. """
        shell = self.editwin.flist.open_shell()
        self.focus_editor()
        try:
            if shell.interp.tkconsole.executing:
                return False # shell is busy
        except:
            return False # shell is not in a valid state

        if message:
            console = shell.interp.tkconsole
            console.text.insert('insert', '%s\n' % message)
            endpos = 'insert +%ic' % (len(message)+1)
            console.text.mark_set('iomark', endpos)

        try:
            shell.interp.runcode(code)
        except AttributeError as e:
            pass

        self.focus_editor()
        return True

    def handle_error(self, e, depth=0):  # Same as SubCode.py
        """ Highlight the error and display it on the shell prompt """
        text = self.editwin.text
        try:
            msg, lineno, offset = e.msg, e.lineno, e.offset
            message = '\n    There is an error (%s) at line %i, column %i.\n' % \
              (msg, lineno, offset)
            self._highlight_error(lineno, offset, depth)
        except Exception as err:
            msg = e
            lineno = 0
            offset = 0
            message = '\n    There is an error: %s' % e

        # send error feedback to shell
        shell = self.editwin.flist.open_shell()
        shell.interp.tkconsole.stderr.write(message)
        shell.showprompt()
        self.focus_editor()

    def _highlight_error(self, lineno, offset, depth): # Same as SubCode.py
        text = self.text
        if offset is None:
            offset = 0
        offset += depth  # for dedented code

        pos = '0.0 + %i lines + %i chars' % (lineno - 1, offset - 1)
        pos = '%i.%i' % (lineno, offset-1)
        text.tag_add("ERROR", pos)

        if text.get(pos) != '\n':
            pos += '+1c'

        text.mark_set("insert", pos)
        text.see(pos)
