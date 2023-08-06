import datetime
import decimal
import functools
import json
import uuid


def _is_aware(value):
    '''
        Determine if a given datetime.datetime is aware.

        The concept is defined in Python's docs:
        https://docs.python.org/library/datetime.html#datetime.tzinfo

        Assuming value.tzinfo is either None or a proper datetime.tzinfo,
        value.utcoffset() implements the appropriate logic.

        Originally from django/utils/timezone.py
    '''
    return value.utcoffset() is not None


def _get_duration_components(duration):
    ''' Originally from django/utils/duration.py
    '''
    days = duration.days
    seconds = duration.seconds
    microseconds = duration.microseconds

    minutes = seconds // 60
    seconds = seconds % 60

    hours = minutes // 60
    minutes = minutes % 60

    return days, hours, minutes, seconds, microseconds


def _duration_iso_string(duration):
    ''' Originally from django/utils/duration.py
    '''
    if duration < datetime.timedelta(0):
        sign = '-'
        duration *= -1
    else:
        sign = ''

    days, hours, minutes, seconds, microseconds = _get_duration_components(duration)
    ms = f'.{microseconds:06d}' if microseconds else ''
    return f'{sign}P{days}DT{hours:02d}H{minutes:02d}M{seconds:02d}{ms}S'


class ChattrJSONEncoder(json.JSONEncoder):
    ''' JSONEncoder subclass that knows how to encode date/time, decimal types, and
        UUIDs. Adapted from Django's JSON encoder.

        Originally from: django/core/serializers/json.py

        NOTE: this class/json serialization/deserialization will likely move to another package.
        We want unified serialization/deserialization across the org.
    '''
    def default(self, o):
        # See "Date Time String Format" in the ECMA-262 specification.
        if isinstance(o, datetime.datetime):
            r = o.isoformat()
            if o.microsecond:
                r = r[:23] + r[26:]
            if r.endswith('+00:00'):
                r = r[:-6] + 'Z'
            return r
        elif isinstance(o, datetime.date):
            return o.isoformat()
        elif isinstance(o, datetime.time):
            if _is_aware(o):
                raise ValueError("JSON can't represent timezone-aware times.")
            r = o.isoformat()
            if o.microsecond:
                r = r[:12]
            return r
        elif isinstance(o, datetime.timedelta):
            return _duration_iso_string(o)
        elif isinstance(o, (decimal.Decimal, uuid.UUID)):
            return str(o)
        else:
            return super().default(o)


serialize = functools.partial(json.dumps, cls=ChattrJSONEncoder, default=str)
deserialize = json.loads
