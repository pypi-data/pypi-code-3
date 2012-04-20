# -*- coding: latin-1 -*-
# Copyright (c) 2008-2012 Michael Howitz
# See also LICENSE.txt
# $Id: tests.py 1454 2012-01-05 10:36:41Z icemac $

import icemac.addressbook.testing
import icemac.ab.importer.browser.testing


def test_suite():
    return icemac.addressbook.testing.DocFileSuite(
        "constraints.txt",
        "edgecases.txt",
        "keywords.txt",
        "multientries.txt",
        "wizard.txt",
        "userfields.txt",
        package='icemac.ab.importer.browser.wizard',
        layer=icemac.ab.importer.browser.testing.ImporterLayer,
        )
