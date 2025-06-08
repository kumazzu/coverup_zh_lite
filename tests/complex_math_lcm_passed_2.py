import pytest
from complex_math import lcm
from math import gcd


def test_lcm_positive_numbers():
    assert lcm(4, 6) == 12
    assert lcm(5, 7) == 35


def test_lcm_negative_numbers():
    assert lcm(-4, 6) == 12
    assert lcm(5, -7) == 35


def test_lcm_zero_raises_value_error():
    with pytest.raises(ValueError):
        lcm(0, 5)
    with pytest.raises(ValueError):
        lcm(3, 0)
    with pytest.raises(ValueError):
        lcm(0, 0)
