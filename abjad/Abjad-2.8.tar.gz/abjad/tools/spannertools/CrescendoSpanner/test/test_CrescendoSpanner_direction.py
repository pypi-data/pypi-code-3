from abjad import *


def test_CrescendoSpanner_direction_01():

    staff = Staff("c'8 d'8 e'8 f'8 g'2")
    spannertools.CrescendoSpanner(staff[:4], direction='up')

    r'''
    \new Staff {
        c'8 ^ \<
        d'8
        e'8
        f'8 \!
        g'2
    }
    '''

    assert staff.format == "\\new Staff {\n\tc'8 ^ \\<\n\td'8\n\te'8\n\tf'8 \\!\n\tg'2\n}"
