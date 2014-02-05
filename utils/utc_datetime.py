from datetime import datetime
import pytz


def utc_datetime(*args, **kwargs):
    dt = datetime(*args, **kwargs)
    return pytz.utc.localize(dt)


def today():
    return now().date()


def now():
    return datetime.now().replace(tzinfo=pytz.utc)
