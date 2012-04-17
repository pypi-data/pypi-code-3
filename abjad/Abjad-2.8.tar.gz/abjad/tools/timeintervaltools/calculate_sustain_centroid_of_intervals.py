from abjad.tools.durationtools import Offset
from abjad.tools.timeintervaltools.TimeIntervalTree import TimeIntervalTree
from abjad.tools.timeintervaltools.all_are_intervals_or_trees_or_empty import all_are_intervals_or_trees_or_empty


def calculate_sustain_centroid_of_intervals(intervals):
    '''Return a weighted mean, such that the centroid of each interval
    in `intervals` are the values, and the weights are their durations.
    '''

    assert all_are_intervals_or_trees_or_empty(intervals)
    if isinstance(intervals, TimeIntervalTree):
        tree = intervals
    else:
        tree = TimeIntervalTree(intervals)
    if not tree:
        return None
    weighted_centroids = sum([(x.center * x.duration) for x in tree])
    sum_of_weights = sum([x.duration for x in tree])
    return Offset(weighted_centroids) / sum_of_weights
