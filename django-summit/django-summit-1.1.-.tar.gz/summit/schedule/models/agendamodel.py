# The Summit Scheduler web application
# Copyright (C) 2008 - 2012 Ubuntu Community, Canonical Ltd
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from django.db import models

from summit.schedule.models.slotmodel import Slot
from summit.schedule.models.roommodel import Room
from summit.schedule.models.meetingmodel import Meeting

__all__ = (
    'Agenda',
)


HELP_TEXT = {
    "auto": ("Whether the meeting was autoscheduled. If this is not "
        "set then the meeting was scheduled by hand."),
}


class Agenda(models.Model):
    slot = models.ForeignKey(Slot)
    room = models.ForeignKey(Room)
    meeting = models.ForeignKey(Meeting)
    auto = models.BooleanField(default=False,
            help_text=HELP_TEXT["auto"])

    class Meta:
        app_label = 'schedule'
        ordering = ('slot', 'room')
        verbose_name = 'agenda item'
        verbose_name_plural = 'agenda items'

        unique_together = ('slot', 'room')

    def __unicode__(self):
        return "%s" % self.meeting
