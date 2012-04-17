from abjad.tools.durationtools import Duration
from abjad.tools.timeintervaltools.TimeIntervalTree import TimeIntervalTree
from abjad.tools.timeintervaltools.all_are_intervals_or_trees_or_empty import all_are_intervals_or_trees_or_empty


def calculate_min_mean_and_max_durations_of_intervals(intervals):
    '''Return a 3-tuple of the minimum, mean and maximum duration of all intervals in `intervals`.
    If `intervals` is empty, return None.
    '''

    assert all_are_intervals_or_trees_or_empty(intervals)
    if isinstance(intervals, TimeIntervalTree):
        tree = intervals
    else:
        tree = TimeIntervalTree(intervals)
    if not tree:
        return None

    durations = [x.duration for x in tree]
    return (min(durations), Duration(sum(durations), len(durations)), max(durations))
