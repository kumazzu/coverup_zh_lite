import pytest
from complex_math import Matrix

class TestMatrix:
    def test_repr(self):
        matrix = Matrix([[1, 2], [3, 4]])
        assert repr(matrix) == "Matrix([[1.0, 2.0], [3.0, 4.0]])"
