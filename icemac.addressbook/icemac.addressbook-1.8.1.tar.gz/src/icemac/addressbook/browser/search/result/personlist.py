# -*- coding: utf-8 -*-
# Copyright (c) 2008-2012 Michael Howitz
# See also LICENSE.txt
# $Id: personlist.py 1453 2012-01-05 10:36:15Z icemac $

import icemac.addressbook.browser.personlist
import icemac.addressbook.browser.search.result.base


class PersonTable(
    icemac.addressbook.browser.personlist.BasePersonList,
    icemac.addressbook.browser.search.result.base.BasePersonTable):
    """Result table displaying columns defined in user preferences."""

    values = (
        icemac.addressbook.browser.search.result.base.BasePersonTable.values)


class ExportForm(
    icemac.addressbook.browser.search.result.base.BaseSearchResultForm):
    "Export form showing a table of found results."

    table_class = PersonTable
