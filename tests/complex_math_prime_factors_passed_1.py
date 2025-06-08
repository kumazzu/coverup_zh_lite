import pytest
from complex_math import prime_factors

def test_prime_factors_zero():
    with pytest.raises(ValueError, match="0 has infinite prime factors"):
        prime_factors(0)

def test_prime_factors_one():
    assert prime_factors(1) == [1]

def test_prime_factors_negative():
    assert prime_factors(-12) == [2, 2, 3]

def test_prime_factors_prime():
    assert prime_factors(13) == [13]

def test_prime_factors_composite():
    assert prime_factors(24) == [2, 2, 2, 3]

def test_prime_factors_large_composite():
    assert prime_factors(123456) == [2, 2, 2, 2, 2, 2, 3, 643]

def test_prime_factors_square_number():
    assert prime_factors(49) == [7, 7]
