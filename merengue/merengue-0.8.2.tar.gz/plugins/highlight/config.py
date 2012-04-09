# Copyright (c) 2010 by Yaco Sistemas
#
# This file is part of Merengue.
#
# Merengue is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Merengue is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Merengue.  If not, see <http://www.gnu.org/licenses/>.

from merengue.pluggable import Plugin

from plugins.highlight.admin import HighlightAdmin
from plugins.highlight.blocks import HighlightBlock
from plugins.highlight.models import Highlight


class PluginConfig(Plugin):
    name = 'Highlight'
    description = 'Highlight content on home page'
    version = '0.0.1a'

    def get_blocks(self):
        return [HighlightBlock]

    def models(self):
        return [
            (Highlight, HighlightAdmin),
        ]
