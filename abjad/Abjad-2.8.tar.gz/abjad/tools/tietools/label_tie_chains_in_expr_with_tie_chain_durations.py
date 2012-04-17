def label_tie_chains_in_expr_with_tie_chain_durations(expr, markup_direction = 'down'):
    r'''Label tie chains in `expr` with both written tie chain duration
    and prolated tie chain duration::

        abjad> staff = Staff(notetools.make_repeated_notes(4))
        abjad> tuplettools.FixedDurationTuplet(Duration(2, 8), staff[:3])
        FixedDurationTuplet(1/4, [c'8, c'8, c'8])
        abjad> tietools.TieSpanner(staff.leaves[:2])
        TieSpanner(c'8, c'8)
        abjad> tietools.TieSpanner(staff.leaves[2:])
        TieSpanner(c'8, c'8)
        abjad> tietools.label_tie_chains_in_expr_with_tie_chain_durations(staff)
        abjad> f(staff)
        \new Staff {
            \times 2/3 {
                c'8 _ \markup { \column { \small 1/4 \small 1/6 } } ~
                c'8
                c'8 _ \markup { \column { \small 1/4 \small 5/24 } } ~
            }
            c'8
        }

    Return none.
    '''
    from abjad.tools.leaftools._label_leaves_in_expr_with_leaf_durations import _label_leaves_in_expr_with_leaf_durations

    show = ['written', 'prolated']
    return _label_leaves_in_expr_with_leaf_durations(
        expr, markup_direction = markup_direction, show = show, ties = 'together')
