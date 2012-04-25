'''
Utility classes for creating dynamic html documents
'''

__license__ = '''
This file is part of pyy.

pyy is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as
published by the Free Software Foundation, either version 3 of
the License, or (at your option) any later version.

pyy is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General
Public License along with pyy.  If not, see
<http://www.gnu.org/licenses/>.
'''

from pyy_tag import pyy_tag


def include(f):
  '''
  includes the contents of a file on disk.
  takes a filename
  '''
  fl = file(f, 'rb')
  data = fl.read()
  fl.close()
  return data


def system(cmd, data='', mode='t'):
  '''
  pipes the output of a program
  '''
  import os
  fin, fout = os.popen4(cmd, mode)
  fin.write(data)
  fin.close()
  return fout.read()


def escape(data, quote=True): # stoled from std lib cgi
  '''
  escapes special characters into their html entities
  Replace special characters "&", "<" and ">" to HTML-safe sequences.
  If the optional flag quote is true, the quotation mark character (")
  is also translated.
  '''
  data = data.replace("&", "&amp;") # Must be done first!
  data = data.replace("<", "&lt;")
  data = data.replace(">", "&gt;")
  if quote:
    data = data.replace('"', "&quot;")
  return data

_unescape = {'quot' :34,
             'amp'  :38,
             'lt'   :60,
             'gt'   :62,
             'nbsp' :32,
             # more here
             # http://www.w3.org/TR/html4/sgml/entities.html
             'yuml' :255
             }


def unescape(data):
  '''
  unescapes html entities. the opposite of escape.
  '''
  import re
  cc = re.compile('&(?:(?:#(\d+))|([^;]+));')

  result = []
  m = cc.search(data)
  while m:
    result.append(data[0:m.start()])
    d = m.group(1)
    if d:
      d = int(d)
      result.append(d > 255 and unichr(d) or chr(d))
    else:
      d = _unescape.get(m.group(2), ord('?'))
      result.append(d > 255 and unichr(d) or chr(d))

    data = data[m.end():]
    m = cc.search(data)

  result.append(data)
  return ''.join(result)


class lazy(pyy_tag):
  '''
  delays function execution until rendered
  '''
  def __init__(self, func, *args, **kwargs):
    pyy_tag.__init__(self)

    self.func   = func
    self.args   = args
    self.kwargs = kwargs

  def render(self, indent=1, inline=False):
    return self.func(*self.args, **self.kwargs)

class text(pyy_tag):
  '''
  Just a string. useful for inside context managers
  '''
  def __init__(self, text):
    pyy_tag.__init__(self)
    self.text = text

  def render(self, indent, inline):
    return self.text
