import copy
import itertools

from abjad.tools.leaftools import iterate_leaves_forward_in_expr


def replace_leaves_in_expr_with_parallel_voices(expr):
    r'''Replace leaves in `expr` with two parallel voices containing copies of
    leaves in `expr`:

    ::

        abjad> c = p('{ c c c c }')
        abjad> f(c)
        {
            c4
            c4
            c4
            c4
        }

    ::

        abjad> leaftools.replace_leaves_in_expr_with_parallel_voices(c.leaves[1:3])
        ([Note('c4'), Note('c4')], [Note('c4'), Note('c4')])

    ::

        abjad> f(c)
        {
            c4
            <<
                \new Voice {
                    c4
                    c4
                }
                \new Voice {
                    c4
                    c4
                }
            >>
            c4
        }

    If leaves in `expr` have different immediate parents, parallel voices will
    be created in each parent:

    ::

        abjad> c = p(r'{ c8 \times 2/3 { c8 c c } \times 4/5 { c16 c c c c } c8 }')
        abjad> f(c)
        {
            c8
            \times 2/3 {
                c8
                c8
                c8
            }
            \times 4/5 {
                c16
                c16
                c16
                c16
                c16
            }
            c8
        }

    ::

        abjad> leaftools.replace_leaves_in_expr_with_parallel_voices(c.leaves[2:7])
        ([Note('c8'), Note('c8'), Note('c16'), Note('c16'), Note('c16')], [Note('c8'), Note('c8'), Note('c16'), Note('c16'), Note('c16')])

    ::

        abjad> f(c)
        {
            c8
            \times 2/3 {
                c8
                <<
                    \new Voice {
                        c8
                        c8
                    }
                    \new Voice {
                        c8
                        c8
                    }
                >>
            }
            \times 4/5 {
                <<
                    \new Voice {
                        c16
                        c16
                        c16
                    }
                    \new Voice {
                        c16
                        c16
                        c16
                    }
                >>
                c16
                c16
            }
            c8
        }

    Returns a list leaves in upper voice, and a list of leaves in lower voice.
    '''    

    from abjad import Container
    from abjad import Voice

    leaves = [leaf for leaf in iterate_leaves_forward_in_expr(expr)]

    upper_leaves = [ ]
    lower_leaves = [ ]

    for parent, group in itertools.groupby(leaves, lambda x: x._parentage.parent):
        grouped_leaves = list(group)
        start_idx = parent.index(grouped_leaves[0])
        stop_idx = parent.index(grouped_leaves[-1])

        container = Container()
        container.is_parallel = True
        upper_voice = Voice(copy.deepcopy(grouped_leaves))
        lower_voice = Voice(copy.deepcopy(grouped_leaves))
        container.extend([upper_voice, lower_voice])

        upper_leaves.extend(upper_voice[:])
        lower_leaves.extend(lower_voice[:])

        parent[start_idx:stop_idx+1] = [container]
        
    return upper_leaves, lower_leaves
