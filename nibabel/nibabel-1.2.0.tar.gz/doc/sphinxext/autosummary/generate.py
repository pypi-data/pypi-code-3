# -*- coding: utf-8 -*-
"""
    sphinx.ext.autosummary.generate
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Usable as a library or script to generate automatic RST source files for
    items referred to in autosummary:: directives.

    Each generated RST file contains a single auto*:: directive which
    extracts the docstring of the referred item.

    Example Makefile rule::

       generate:
               sphinx-autogen source/*.rst source/generated

    :copyright: Copyright 2007-2010 by the Sphinx team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import os
import re
import sys
import optparse
import inspect
import pydoc

from jinja2 import FileSystemLoader, TemplateNotFound
from jinja2.sandbox import SandboxedEnvironment

from autosummary import import_by_name, get_documenter
from sphinx.util import ensuredir
from sphinx.jinja2glue import BuiltinTemplateLoader

def main(argv=sys.argv):
    usage = """%prog [OPTIONS] SOURCEFILE ..."""
    p = optparse.OptionParser(usage.strip())
    p.add_option("-o", "--output-dir", action="store", type="string",
                 dest="output_dir", default=None,
                 help="Directory to place all output in")
    p.add_option("-s", "--suffix", action="store", type="string",
                 dest="suffix", default="rst",
                 help="Default suffix for files (default: %default)")
    p.add_option("-t", "--templates", action="store", type="string",
                 dest="templates", default=None,
                 help="Custom template directory (default: %default)")
    options, args = p.parse_args(argv[1:])

    if len(args) < 1:
        p.error('no input files given')

    generate_autosummary_docs(args, options.output_dir,
                              "." + options.suffix,
                              template_dir=options.templates)

def _simple_info(msg):
    print msg

def _simple_warn(msg):
    print >> sys.stderr, 'WARNING: ' + msg

# -- Generating output ---------------------------------------------------------

def _is_from_same_file(obj1, obj2):
    try:
        return inspect.getsourcefile(obj1) == inspect.getsourcefile(obj2)
    except TypeError:
        return False

def generate_autosummary_docs(sources, output_dir=None, suffix='.rst',
                              warn=_simple_warn, info=_simple_info,
                              base_path=None, builder=None, template_dir=None):

    showed_sources = list(sorted(sources))
    if len(showed_sources) > 20:
        showed_sources = showed_sources[:10] + ['...'] + showed_sources[-10:]
    info('[autosummary] generating autosummary for: %s' %
         ', '.join(showed_sources))

    if output_dir:
        info('[autosummary] writing to %s' % output_dir)

    if base_path is not None:
        sources = [os.path.join(base_path, filename) for filename in sources]

    # create our own templating environment
    template_dirs = [os.path.join(os.path.dirname(__file__), template_dir)]
    if builder is not None:
        # allow the user to override the templates
        template_loader = BuiltinTemplateLoader()
        template_loader.init(builder, dirs=template_dirs)
    else:
        if template_dir:
            template_dirs.insert(0, template_dir)
        template_loader = FileSystemLoader(template_dirs)
    template_env = SandboxedEnvironment(loader=template_loader)

    # read
    items = find_autosummary_in_files(sources)

    # remove possible duplicates
    items = dict([(item, True) for item in items]).keys()

    # keep track of new files
    new_files = []

    # write
    for name, path, template_name in sorted(items):
        if path is None:
            # The corresponding autosummary:: directive did not have
            # a :toctree: option
            continue

        path = output_dir or os.path.abspath(path)
        ensuredir(path)

        try:
            obj, name = import_by_name(name)
        except ImportError, e:
            warn('[autosummary] failed to import %r: %s' % (name, e))
            continue

        fn = os.path.join(path, name + suffix)

        # skip it if it exists
        if os.path.isfile(fn):
            continue

        new_files.append(fn)

        f = open(fn, 'w')

        try:
            doc = get_documenter(obj)

            if template_name is not None:
                template = template_env.get_template(template_name)
            else:
                try:
                    template = template_env.get_template('autosummary/%s.rst'
                                                         % doc.objtype)
                except TemplateNotFound:
                    template = template_env.get_template('autosummary/base.rst')

            def get_members(obj, typ, include_public=[]):
                items = [
                    # filter by file content !!!!
                    name for name in dir(obj)
                    if get_documenter(getattr(obj, name)).objtype == typ \
                        and _is_from_same_file(getattr(obj, name), obj)
                ]
                public = [x for x in items
                          if x in include_public or not x.startswith('_')]
                return public, items

            ns = {}

            if doc.objtype == 'module':
                ns['members'] = dir(obj)
                ns['functions'], ns['all_functions'] = \
                                   get_members(obj, 'function')
                ns['classes'], ns['all_classes'] = \
                                 get_members(obj, 'class')
                ns['exceptions'], ns['all_exceptions'] = \
                                   get_members(obj, 'exception')
                ns['methods'], ns['all_methods'] = \
                                 get_members(obj, 'method')
            elif doc.objtype == 'class':
                ns['members'] = dir(obj)
                ns['methods'], ns['all_methods'] = \
                                 get_members(obj, 'method', ['__init__'])
                ns['attributes'], ns['all_attributes'] = \
                                 get_members(obj, 'attribute')

            parts = name.split('.')
            if doc.objtype in ('method', 'attribute'):
                mod_name = '.'.join(parts[:-2])
                cls_name = parts[-2]
                obj_name = '.'.join(parts[-2:])
                ns['class'] = cls_name
            else:
                mod_name, obj_name = '.'.join(parts[:-1]), parts[-1]

            ns['fullname'] = name
            ns['module'] = mod_name
            ns['objname'] = obj_name
            ns['name'] = parts[-1]

            ns['objtype'] = doc.objtype
            ns['underline'] = len(name) * '='

            rendered = template.render(**ns)
            f.write(rendered)
        finally:
            f.close()

    # descend recursively to new files
    if new_files:
        generate_autosummary_docs(new_files, output_dir=output_dir,
                                  suffix=suffix, warn=warn, info=info,
                                  base_path=base_path, builder=builder,
                                  template_dir=template_dir)


# -- Finding documented entries in files ---------------------------------------

def find_autosummary_in_files(filenames):
    """
    Find out what items are documented in source/*.rst.
    See `find_autosummary_in_lines`.
    """
    documented = []
    for filename in filenames:
        f = open(filename, 'r')
        lines = f.read().splitlines()
        documented.extend(find_autosummary_in_lines(lines, filename=filename))
        f.close()
    return documented

def find_autosummary_in_docstring(name, module=None, filename=None):
    """
    Find out what items are documented in the given object's docstring.
    See `find_autosummary_in_lines`.
    """
    try:
        obj, real_name = import_by_name(name)
        lines = pydoc.getdoc(obj).splitlines()
        return find_autosummary_in_lines(lines, module=name, filename=filename)
    except AttributeError:
        pass
    except ImportError, e:
        print "Failed to import '%s': %s" % (name, e)
    return []

def find_autosummary_in_lines(lines, module=None, filename=None):
    """
    Find out what items appear in autosummary:: directives in the given lines.

    Returns a list of (name, toctree, template) where *name* is a name
    of an object and *toctree* the :toctree: path of the corresponding
    autosummary directive (relative to the root of the file name), and
    *template* the value of the :template: option. *toctree* and
    *template* ``None`` if the directive does not have the
    corresponding options set.
    """
    autosummary_re = re.compile(r'^\s*\.\.\s+autosummary::\s*')
    automodule_re = re.compile(
        r'^\s*\.\.\s+automodule::\s*([A-Za-z0-9_.]+)\s*$')
    module_re = re.compile(
        r'^\s*\.\.\s+(current)?module::\s*([a-zA-Z0-9_.]+)\s*$')
    autosummary_item_re = re.compile(r'^\s+(~?[_a-zA-Z][a-zA-Z0-9_.]*)\s*.*?')
    toctree_arg_re = re.compile(r'^\s+:toctree:\s*(.*?)\s*$')
    template_arg_re = re.compile(r'^\s+:template:\s*(.*?)\s*$')

    documented = []

    toctree = None
    template = None
    current_module = module
    in_autosummary = False

    for line in lines:
        if in_autosummary:
            m = toctree_arg_re.match(line)
            if m:
                toctree = m.group(1)
                if filename:
                    toctree = os.path.join(os.path.dirname(filename),
                                           toctree)
                continue

            m = template_arg_re.match(line)
            if m:
                template = m.group(1).strip()
                continue

            if line.strip().startswith(':'):
                continue # skip options

            m = autosummary_item_re.match(line)
            if m:
                name = m.group(1).strip()
                if name.startswith('~'):
                    name = name[1:]
                if current_module and \
                       not name.startswith(current_module + '.'):
                    name = "%s.%s" % (current_module, name)
                documented.append((name, toctree, template))
                continue

            if not line.strip():
                continue

            in_autosummary = False

        m = autosummary_re.match(line)
        if m:
            in_autosummary = True
            toctree = None
            template = None
            continue

        m = automodule_re.search(line)
        if m:
            current_module = m.group(1).strip()
            # recurse into the automodule docstring
            documented.extend(find_autosummary_in_docstring(
                current_module, filename=filename))
            continue

        m = module_re.match(line)
        if m:
            current_module = m.group(2)
            continue

    return documented


if __name__ == '__main__':
    main()
