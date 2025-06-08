import pytest
from complex_math import gcd

@pytest.mark.parametrize("a, b, expected", [
    (0, 5, 5),
    (5, 0, 5),
    (-10, 6, 2),
    (10, -6, 2),
    (17, 5, 1),
    (24, 18, 6),
])
def test_gcd(a, b, expected):
    assert gcd(a, b) == expected
