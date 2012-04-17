from abjad import *


def test_stafftools_get_first_staff_in_proper_parentage_of_component_01():

    staff = Staff("c'8 d'8 e'8 f'8")

    assert stafftools.get_first_staff_in_proper_parentage_of_component(staff[0]) is staff
    assert stafftools.get_first_staff_in_proper_parentage_of_component(staff[1]) is staff
    assert stafftools.get_first_staff_in_proper_parentage_of_component(staff[2]) is staff
    assert stafftools.get_first_staff_in_proper_parentage_of_component(staff[3]) is staff

    assert stafftools.get_first_staff_in_proper_parentage_of_component(staff) is None
