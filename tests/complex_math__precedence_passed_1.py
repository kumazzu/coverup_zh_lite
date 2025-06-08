import pytest
from complex_math import _precedence

@pytest.mark.parametrize("op, expected", [
    ("+", 1),
    ("-", 1),
    ("*", 2),
    ("/", 2),
])
def test_precedence(op, expected):
    assert _precedence(op) == expected
