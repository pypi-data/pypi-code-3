import re


_spaces = "(?:\ |\t|\n)*"
# "   from"
_from = "%sfrom" % _spaces
# "   import"
_import = "%simport" % _spaces
_first_imporable = "(?P<firstimporable>\w+)"
_other_imporable = "(?:[.](?P<otherimporable>[\w.]+)?)?"
_import_imporable = "(?:\w+,(?:\ |\t|\n)*)*(?P<importimporable>\w+)"

# "   from   "
_from_begin = "%s%s" % (_from, _spaces)
# "   from   os"
_from_first_imporable = "%s%s" % (_from_begin, _first_imporable)
# "   from   os.path"
_from_other_imporables = "%s%s" % (_from_first_imporable, _other_imporable)
# "   from   os.path import"
_from_import = "%s%s%s" % (_from_other_imporables, _spaces, _import)
# "   from   os.path import join"
_from_complete = "%s%s%s?" % (_from_import, _spaces, _import_imporable)

# "   import"
_import_begin = "%s" % _import
# "   import   os"
_import_complete = "%s%s%s?" % (_import_begin, _spaces, _import_imporable)

from_first_imporable = re.compile(_from_first_imporable + "?$")
from_other_imporables = re.compile(_from_other_imporables + "$")
from_import = re.compile(_from_import + "$")
from_complete = re.compile(_from_complete + "$")

import_begin = re.compile(_import_begin + "$")
import_complete = re.compile(_import_complete + "?$")
