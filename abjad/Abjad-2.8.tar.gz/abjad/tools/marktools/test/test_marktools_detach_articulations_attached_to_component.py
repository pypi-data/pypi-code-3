from abjad import *


def test_marktools_detach_articulations_attached_to_component_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    slur = spannertools.SlurSpanner(staff.leaves)
    marktools.Articulation('^')(staff[0])
    marktools.Articulation('.')(staff[0])
    articulations = marktools.get_articulations_attached_to_component(staff[0])
    assert len(articulations) == 2

    marktools.detach_articulations_attached_to_component(staff[0])
    articulations = marktools.get_articulations_attached_to_component(staff[0])
    assert len(articulations) == 0
