import pytest
from complex_math import Matrix

def test_matrix_init_valid():
    data = [[1, 2], [3, 4]]
    matrix = Matrix(data)
    assert matrix.m == 2
    assert matrix.n == 2
    assert matrix._data == [[1.0, 2.0], [3.0, 4.0]]

def test_matrix_init_empty_data():
    with pytest.raises(ValueError, match="All rows must be same non-zero length"):
        Matrix([])

def test_matrix_init_uneven_rows():
    with pytest.raises(ValueError, match="All rows must be same non-zero length"):
        Matrix([[1, 2], [3]])

def test_matrix_init_non_numeric_conversion():
    data = [["1", "2"], ["3", "4"]]
    matrix = Matrix(data)
    assert matrix._data == [[1.0, 2.0], [3.0, 4.0]]
