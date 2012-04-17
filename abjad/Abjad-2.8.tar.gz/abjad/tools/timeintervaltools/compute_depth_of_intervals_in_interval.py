from abjad.tools.sequencetools import iterate_sequence_pairwise_strict
from abjad.tools.timeintervaltools.TimeInterval import TimeInterval
from abjad.tools.timeintervaltools.TimeIntervalTree import TimeIntervalTree
from abjad.tools.timeintervaltools.all_are_intervals_or_trees_or_empty import all_are_intervals_or_trees_or_empty
from abjad.tools.timeintervaltools.get_all_unique_bounds_in_intervals import get_all_unique_bounds_in_intervals
from abjad.tools.timeintervaltools.split_intervals_at_rationals import split_intervals_at_rationals


def compute_depth_of_intervals_in_interval(intervals, interval):
    '''Compute a tree whose intervals represent the depth (level of overlap)
    in each boundary pair of `intervals`, cropped within `interval`::

        abjad> from abjad.tools.timeintervaltools import *
        abjad> a = TimeInterval(0, 3)
        abjad> b = TimeInterval(6, 12)
        abjad> c = TimeInterval(9, 15)
        abjad> tree = TimeIntervalTree([a, b, c])
        abjad> d = TimeInterval(-1, 16)
        abjad> compute_depth_of_intervals_in_interval(tree, d)
        TimeIntervalTree([
            TimeInterval(Offset(-1, 1), Offset(0, 1), {'depth': 0}),
            TimeInterval(Offset(0, 1), Offset(3, 1), {'depth': 1}),
            TimeInterval(Offset(3, 1), Offset(6, 1), {'depth': 0}),
            TimeInterval(Offset(6, 1), Offset(9, 1), {'depth': 1}),
            TimeInterval(Offset(9, 1), Offset(12, 1), {'depth': 2}),
            TimeInterval(Offset(12, 1), Offset(15, 1), {'depth': 1}),
            TimeInterval(Offset(15, 1), Offset(16, 1), {'depth': 0})
        ])

    Return interval tree.
    '''

    assert all_are_intervals_or_trees_or_empty(intervals)
    assert isinstance(interval, TimeInterval)
    if isinstance(intervals, TimeIntervalTree):
        tree = intervals
    else:
        tree = TimeIntervalTree(intervals)

    if interval.stop <= tree.start or tree.stop <= interval.start:
        return TimeIntervalTree([TimeInterval(interval.start, interval.stop, {'depth': 0})])
    else:
        bounds = list(get_all_unique_bounds_in_intervals(tree))
        if interval.start < tree.start:
            bounds.insert(0, interval.start)
        elif tree.start < interval.start:
            #bounds = filter(lambda x: interval.start <= x, bounds)
            bounds = [x for x in bounds if interval.start <= x]
            bounds.insert(0, interval.start)
        if tree.stop < interval.stop:
            bounds.append(interval.stop)
        elif interval.stop < tree.stop:
            #bounds = filter(lambda x: x <= interval.stop, bounds)
            bounds = [x for x in bounds if x <= interval.stop]
            bounds.append(interval.stop)
        bounds = sorted(list(set(bounds)))

    intervals = []
#   for i in range(len(bounds) - 1):
    for pair in iterate_sequence_pairwise_strict(bounds):
        target = TimeInterval(pair[0], pair[1], {})
        found = tree.find_intervals_intersecting_or_tangent_to_interval(target)
        if found:
#            target['depth'] = len(filter( \
#                lambda x: (not x.start == target.stop and not x.stop == target.start), found))
            target['depth'] = len([x for x in found \
                if (not x.start == target.stop and not x.stop == target.start)])
        else:
            target['depth'] = 0
        intervals.append(target)

    return TimeIntervalTree(intervals)
