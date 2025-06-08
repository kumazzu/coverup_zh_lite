import pytest
from complex_math import is_prime

@pytest.mark.parametrize("n,expected", [
    (1, False),
    (2, True),
    (3, True),
    (4, False),
    (5, True),
    (6, False),
    (7, True),
    (9, False),
    (25, False),
    (29, True),
    (49, False),
])
def test_is_prime(n, expected):
    assert is_prime(n) == expected
