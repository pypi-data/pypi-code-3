from abjad.tools.timeintervaltools.TimeIntervalTree import TimeIntervalTree
from abjad.tools.timeintervaltools.all_are_intervals_or_trees_or_empty import all_are_intervals_or_trees_or_empty
from abjad.tools.timeintervaltools.calculate_depth_density_of_intervals import calculate_depth_density_of_intervals
from abjad.tools.timeintervaltools.compute_depth_of_intervals import compute_depth_of_intervals


def calculate_min_mean_and_max_depth_of_intervals(intervals):
    '''Return a 3-tuple of the minimum, mean and maximum depth of `intervals`.
    If `intervals` is empty, return None.  "Mean" in this case is a weighted mean,
    where the durations of the intervals in depth tree of `intervals` are the weights
    '''

    assert all_are_intervals_or_trees_or_empty(intervals)
    if isinstance(intervals, TimeIntervalTree):
        tree = intervals
    else:
        tree = TimeIntervalTree(intervals)
    if not tree:
        return None

    depth_tree = compute_depth_of_intervals(tree)
    depths = [x['depth'] for x in depth_tree]
    mean = calculate_depth_density_of_intervals(tree)
    return min(depths), mean, max(depths)
