# ..F                                                                      [100%]
# =================================== FAILURES ===================================
# _______________________ test_lcm_zero_raises_value_error _______________________
# 
#     def test_lcm_zero_raises_value_error():
#         with pytest.raises(ValueError, match="lcm() arguments must be non-zero"):
# >           lcm(0, 5)
# 
# test_tmp_86f01edf.py:18: 
# _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
# 
# a = 0, b = 5
# 
#     def lcm(a: int, b: int) -> int:
#         """最小公倍数；0 会抛 ValueError。"""
#         if a == 0 or b == 0:
# >           raise ValueError("lcm() arguments must be non-zero")
# E           ValueError: lcm() arguments must be non-zero
# 
# complex_math.py:24: ValueError
# 
# During handling of the above exception, another exception occurred:
# 
#     def test_lcm_zero_raises_value_error():
# >       with pytest.raises(ValueError, match="lcm() arguments must be non-zero"):
# E       AssertionError: Regex pattern did not match.
# E        Regex: 'lcm() arguments must be non-zero'
# E        Input: 'lcm() arguments must be non-zero'
# E        Did you mean to `re.escape()` the regex?
# 
# test_tmp_86f01edf.py:17: AssertionError
# =========================== short test summary info ============================
# FAILED test_tmp_86f01edf.py::test_lcm_zero_raises_value_error - AssertionErro...

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
    with pytest.raises(ValueError, match="lcm() arguments must be non-zero"):
        lcm(0, 5)
    with pytest.raises(ValueError, match="lcm() arguments must be non-zero"):
        lcm(3, 0)
    with pytest.raises(ValueError, match="lcm() arguments must be non-zero"):
        lcm(0, 0)
