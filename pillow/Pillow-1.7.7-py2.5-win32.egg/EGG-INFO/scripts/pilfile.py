#!C:\Python25\python.exe
#
# The Python Imaging Library.
# $Id$
#
# a utility to identify image files
#
# this script identifies image files, extracting size and
# pixel mode information for known file formats.  Note that
# you don't need the PIL C extension to use this module.
#
# History:
# 0.0 1995-09-01 fl   Created
# 0.1 1996-05-18 fl   Modified options, added debugging mode
# 0.2 1996-12-29 fl   Added verify mode
# 0.3 1999-06-05 fl   Don't mess up on class exceptions (1.5.2 and later)
# 0.4 2003-09-30 fl   Expand wildcards on Windows; robustness tweaks
#

import site
import getopt, glob, sys

from PIL import Image

if len(sys.argv) == 1:
    print "PIL File 0.4/2003-09-30 -- identify image files"
    print "Usage: pilfile [option] files..."
    print "Options:"
    print "  -f  list supported file formats"
    print "  -i  show associated info and tile data"
    print "  -v  verify file headers"
    print "  -q  quiet, don't warn for unidentified/missing/broken files"
    sys.exit(1)

try:
    opt, args = getopt.getopt(sys.argv[1:], "fqivD")
except getopt.error, v:
    print v
    sys.exit(1)

verbose = quiet = verify = 0

for o, a in opt:
    if o == "-f":
        Image.init()
        id = Image.ID[:]
        id.sort()
        print "Supported formats:"
        for i in id:
            print i,
        sys.exit(1)
    elif o == "-i":
        verbose = 1
    elif o == "-q":
        quiet = 1
    elif o == "-v":
        verify = 1
    elif o == "-D":
        Image.DEBUG = Image.DEBUG + 1

def globfix(files):
    # expand wildcards where necessary
    if sys.platform == "win32":
        out = []
        for file in files:
            if glob.has_magic(file):
                out.extend(glob.glob(file))
            else:
                out.append(file)
        return out
    return files

for file in globfix(args):
    try:
        im = Image.open(file)
        print "%s:" % file, im.format, "%dx%d" % im.size, im.mode,
        if verbose:
            print im.info, im.tile,
        print
        if verify:
            try:
                im.verify()
            except:
                if not quiet:
                    print "failed to verify image",
                    print "(%s:%s)" % (sys.exc_type, sys.exc_value)
    except IOError, v:
        if not quiet:
            print file, "failed:", v
    except:
        import traceback
        if not quiet:
            print file, "failed:", "unexpected error"
            traceback.print_exc(file=sys.stdout)
