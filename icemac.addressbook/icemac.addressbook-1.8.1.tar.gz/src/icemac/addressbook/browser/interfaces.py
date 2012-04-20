# Copyright (c) 2008-2012 Michael Howitz
# See also LICENSE.txt
# $Id: interfaces.py 1453 2012-01-05 10:36:15Z icemac $

from icemac.addressbook.i18n import _
import z3c.form.interfaces
import z3c.formui.interfaces
import z3c.layer.pagelet
import z3c.preference.interfaces
import zope.interface


class IAddressBookLayer(
    z3c.form.interfaces.IFormLayer,
    z3c.layer.pagelet.IPageletBrowserLayer,
    z3c.preference.interfaces.IPreferenceLayer):
    """Address book browser layer with form support."""


class IAddressBookBrowserSkin(
    z3c.formui.interfaces.IDivFormLayer,
    IAddressBookLayer):
    """The address book browser skin using the div-based layout."""


class IPersonCount(zope.interface.Interface):
    "Number of persons for deletion."

    count = zope.schema.Int(title=_(u'number of persons'), required=False)
    notes = zope.schema.TextLine(title=_(u'notes'), required=False)


class IErrorMessage(zope.interface.Interface):
    """Render error message human readable."""

    def __unicode__():
        """Returns the translateable error text."""
