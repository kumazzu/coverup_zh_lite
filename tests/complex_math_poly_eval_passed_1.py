import pytest
from complex_math import poly_eval

def test_poly_eval_empty_coeffs():
    assert poly_eval([], 5.0) == 0.0

def test_poly_eval_single_coeff():
    assert poly_eval([3.0], 2.0) == 3.0

def test_poly_eval_multiple_coeffs():
    assert poly_eval([2.0, -1.0, 3.0], 4.0) == 31.0
