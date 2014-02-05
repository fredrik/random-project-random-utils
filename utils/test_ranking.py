import pytest
from .ranking import rankify


@pytest.mark.parametrize(('values', 'expected_ranks'), [
    # List of values (sorted desc) to pass to rankify
    # Checks that the ranks returned are as ranks
    ([], []),
    ([1], [1]),
    ([5, 4, 3, 2, 1], [1, 2, 3, 4, 5]),
    ([5, 5, 3, 3, 1], [1, 1, 3, 3, 5]),
    ([5, 5, 5, 5, 5, 5, 5, 5, 5], [1, 1, 1, 1, 1, 1, 1, 1, 1]),
])
def test_rankify(values, expected_ranks):
    dict_values = [{'attr': value} for value in values]
    rankify_ranks = [rank for _, rank in rankify(dict_values, 'attr')]
    assert rankify_ranks == expected_ranks
