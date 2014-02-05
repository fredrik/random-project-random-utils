import time
import itertools

import pytest
from mock import Mock, ANY

from utils.testing import OfType

from .better_retry import better_retry as retry


class MyException(Exception):
    pass


@pytest.fixture
def mock_sleep(monkeypatch):
    mock_sleep = Mock()
    monkeypatch.setattr(time, 'sleep', mock_sleep)
    return mock_sleep


def test_no_exception(mock_sleep):
    called = {'count': 0}

    @retry(max_tries=2, exceptions=None)
    def f():
        called['count'] += 1

    f()

    assert not mock_sleep.called
    assert called['count'] == 1


def test_with_exception_no_retries(mock_sleep):
    called = {'count': 0}

    @retry(max_tries=0)
    def f():
        called['count'] += 1
        raise Exception

    with pytest.raises(Exception):
        f()

    assert not mock_sleep.called
    assert called['count'] == 1


def test_with_exception_and_retries(mock_sleep):
    called = {'count': 0}

    @retry(max_tries=3)
    def f():
        called['count'] += 1
        raise Exception

    with pytest.raises(Exception):
        f()

    assert mock_sleep.call_count == 2
    assert called['count'] == 3


def test_sleeping(mock_sleep):
    called = {'count': 0}

    @retry(max_tries=4, start_delay=1, backoff=2)
    def f():
        called['count'] += 1
        raise Exception

    with pytest.raises(Exception):
        f()

    expected_sleeps = [1, 2, 4]
    assert mock_sleep.call_args_list == [((sleep,),) for sleep in expected_sleeps]
    assert called['count'] == 4


def test_hooks(mock_sleep):
    called = {'count': 0}
    hook = Mock()

    @retry(max_tries=4, start_delay=1, backoff=2, hook=hook)
    def f():
        called['count'] += 1
        raise Exception

    with pytest.raises(Exception):
        f()

    expected_sleeps = [1, 2, 4]
    assert mock_sleep.call_args_list == [((sleep,),) for sleep in expected_sleeps]
    assert hook.call_args_list == [((count, OfType(Exception), delay),)
                                   for count, delay
                                   in zip(itertools.count(1), expected_sleeps)]
    assert called['count'] == 4


def test_exceptions(mock_sleep):
    hook = Mock()

    @retry(max_tries=2, hook=hook, exceptions=MyException)
    def f():
        raise MyException

    with pytest.raises(MyException):
        f()

    assert hook.call_args_list[0] == ((1, OfType(MyException), ANY),)
