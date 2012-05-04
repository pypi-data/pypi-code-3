# Port of the RightFax Java API
# Author: Ron Smith, ThatAintWorking.com
# Date: 12/7/2011

import time as _time
from datetime import timedelta, tzinfo

STDOFFSET = timedelta(seconds = -_time.timezone)
if _time.daylight:
    DSTOFFSET = timedelta(seconds = -_time.altzone)
else:
    DSTOFFSET = STDOFFSET

DSTDIFF = DSTOFFSET - STDOFFSET

ZERO = timedelta(0)

class LocalTimezone(tzinfo):

    def utcoffset(self, dt):
        if self._isdst(dt):
            return DSTOFFSET
        else:
            return STDOFFSET

    def dst(self, dt):
        if self._isdst(dt):
            return DSTDIFF
        else:
            return ZERO

    def tzname(self, dt):
        return _time.tzname[self._isdst(dt)]

    def _isdst(self, dt):
        tt = (dt.year, dt.month, dt.day,
              dt.hour, dt.minute, dt.second,
              dt.weekday(), 0, 0)
        stamp = _time.mktime(tt)
        tt = _time.localtime(stamp)
        return tt.tm_isdst > 0


def format_datetime_utc(dt):
    if not dt.tzinfo:
        dt = dt.replace(microsecond = 0, tzinfo=LocalTimezone())
    else:
        dt = dt.replace(microsecond = 0)
    return dt.isoformat('T')
