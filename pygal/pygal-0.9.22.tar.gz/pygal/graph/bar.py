# -*- coding: utf-8 -*-
# This file is part of pygal
#
# A python svg graph plotting library
# Copyright © 2012 Kozea
#
# This library is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# This library is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with pygal. If not, see <http://www.gnu.org/licenses/>.
"""
Bar chart

"""

from __future__ import division
from pygal.graph.graph import Graph
from pygal.util import swap, ident, compute_scale, decorate


class Bar(Graph):
    """Bar graph"""

    def __init__(self, *args, **kwargs):
        self._x_ranges = None
        super(Bar, self).__init__(*args, **kwargs)

    def bar(self, serie_node, serie, values, stack_vals=None):
        """Draw a bar graph for a serie"""
        # value here is a list of tuple range of tuple coord

        def view(rng):
            """Project range"""
            t, T = rng
            fun = swap if self.horizontal else ident
            return self.view(fun(t)), self.view(fun(T))

        bars = self.svg.node(serie_node['plot'], class_="bars")
        view_values = map(view, values)
        for i, ((x, y), (X, Y)) in enumerate(view_values):
            if None in (x, y):
                continue

            #          +-------+
            #          |       |
            #          |       |
            #          |       +-------+
            #          |       |       |
            #          |       |       |
            #          |       |       |
            #          +-------+-------+
            #        (x,y)   (X,Y)
            #
            # x and y are left range coords and X, Y right ones
            metadata = serie.metadata[i]
            val = self._format(values[i][1][1])
            if self.horizontal:
                x, y, X, Y = Y, X, y, x
            width = X - x
            padding = .1 * width
            inner_width = width - 2 * padding
            if self.horizontal:
                height = self.view.x(self.zero) - y
            else:
                height = self.view.y(self.zero) - y
            if stack_vals == None:
                bar_width = inner_width / len(self.series)
                bar_padding = .1 * bar_width
                bar_inner_width = bar_width - 2 * bar_padding
                offset = serie.index * bar_width + bar_padding
                shift = 0
            else:
                offset = 0
                bar_inner_width = inner_width
                shift = stack_vals[i][int(height < 0)]
                stack_vals[i][int(height < 0)] += height
            x = x + padding + offset

            if height < 0:
                y = y + height
                height = -height
            y -= shift

            bar = decorate(
                self.svg,
                self.svg.node(bars, class_='bar'),
                metadata)
            self.svg.transposable_node(
                bar, 'rect',
                x=x,
                y=y,
                rx=self.rounded_bars * 1,
                ry=self.rounded_bars * 1,
                width=bar_inner_width,
                height=height,
                class_='rect reactive tooltip-trigger')

            x += bar_inner_width / 2
            y += height / 2

            if self.horizontal:
                x, y = y, x

            self._tooltip_data(bar, val, x, y, classes="centered")
            self._static_value(serie_node, val, x, y)

        return stack_vals

    def _compute(self):
        self._box.ymin = min(min(self._values), self.zero)
        self._box.ymax = max(max(self._values), self.zero)
        x_step = len(self.series[0].values)
        x_pos = [x / x_step for x in range(x_step + 1)
        ] if x_step > 1 else [0, 1]  # Center if only one value
        y_pos = compute_scale(
            self._box.ymin, self._box.ymax, self.logarithmic
        ) if not self.y_labels else map(float, self.y_labels)

        self._x_ranges = zip(x_pos, x_pos[1:])
        self._x_labels = self.x_labels and zip(self.x_labels, [
            sum(x_range) / 2 for x_range in self._x_ranges])
        self._y_labels = zip(map(self._format, y_pos), y_pos)

    def _plot(self):
        for serie in self.series:
            serie_node = self._serie(serie.index)
            self.bar(serie_node, serie, [
                tuple((self._x_ranges[i][j], v) for j in range(2))
                for i, v in enumerate(serie.values)])
