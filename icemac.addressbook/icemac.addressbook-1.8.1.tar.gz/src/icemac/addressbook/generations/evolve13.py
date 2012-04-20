# Copyright (c) 2010-2012 Michael Howitz
# See also LICENSE.txt
# $Id: evolve13.py 1453 2012-01-05 10:36:15Z icemac $

import icemac.addressbook.generations.utils
import icemac.addressbook.interfaces
import zope.component


@icemac.addressbook.generations.utils.evolve_addressbooks
def evolve(addressbook):
    "Update sort order of entities: person should be in the second place."
    person = icemac.addressbook.interfaces.IEntity(
        icemac.addressbook.interfaces.IPerson)
    order_storage = zope.component.getUtility(
        icemac.addressbook.interfaces.IOrderStorage)
    person_pos = order_storage.get(
        person.name, icemac.addressbook.interfaces.ENTITIES)
    if person_pos != 1:
        order_storage.up(
            person.name, icemac.addressbook.interfaces.ENTITIES, 5)
