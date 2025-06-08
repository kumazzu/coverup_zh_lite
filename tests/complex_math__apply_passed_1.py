import pytest
from complex_math import _apply


@pytest.mark.parametrize(
    "op, a, b, expected",
    [
        ("+", 1.0, 2.0, 3.0),
        ("-", 5.0, 3.0, 2.0),
        ("*", 2.0, 3.0, 6.0),
        ("/", 6.0, 2.0, 3.0),
    ],
)
def test_apply_valid_operations(op, a, b, expected):
    assert _apply(op, b, a) == expected


def test_apply_division_by_zero():
    with pytest.raises(ZeroDivisionError, match="division by zero"):
        _apply("/", 0.0, 1.0)


def test_apply_invalid_operation():
    with pytest.raises(ValueError):
        _apply("^", 1.0, 2.0)
