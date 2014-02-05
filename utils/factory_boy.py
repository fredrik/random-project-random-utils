# -*- coding: utf-8 -*-

from functools import partial

from django.utils import timezone

from factory import Sequence, LazyAttributeSequence


# Personally I prefer my counters to be integers rather than strings..
Sequence = partial(Sequence, type=int)
LazyAttributeSequence = partial(LazyAttributeSequence, type=int)


def basic_sequence(prefix=None):
    """Simple sequence generator that returns names of form `Prefix #`.
    If no name specified, uses the target class name as the prefix.
    """
    def f(o, n):
        # If no name specified, use the name of the target class
        _prefix = prefix or o._LazyStub__target_class._associated_class.__name__
        # Also add some unicrud for good measure
        return u'{0} лüϻƃéｒ {1}'.format(_prefix, n)

    return LazyAttributeSequence(f)


def short_basic_sequence(prefix=None, max_length=11):
    def f(o, n):
        # If no name specified, use the name of the target class
        _prefix = prefix or o._LazyStub__target_class._associated_class.__name__
        _short_prefix = _prefix[:6]
        return u'{0}😎{1}'.format(_short_prefix, n)[:max_length]

    return LazyAttributeSequence(f)


def datetime_sequence(delta,
                      start=timezone.now(),
                      offset=0):
    """Sequence returning datetimes incremented by the given delta.
    Can also take an offset which is added to the counter.

    """
    return Sequence(lambda n: start + ((n + offset) * delta))
