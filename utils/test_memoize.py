import pytest
from uuid import uuid4

from memoize import memoized


@memoized
def do_something(*args, **kwargs):
    return uuid4()


def test_that_memoize_remembers():
    assert do_something() == do_something()


def test_that_memoize_takes_notice_of_args():
    assert do_something() != do_something('foo')
    assert do_something(1) == do_something(1)
    assert do_something(1, 2, 3) == do_something(1, 2, 3)


def test_uncachable_parameters_raises():
    with pytest.raises(TypeError):
        do_something([1, 2, 3])
