import pytest
from complex_math import Matrix

@pytest.fixture
def square_matrix_1x1():
    return Matrix([[5]])

@pytest.fixture
def square_matrix_2x2():
    return Matrix([[1, 2], [3, 4]])

@pytest.fixture
def square_matrix_3x3():
    return Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

@pytest.fixture
def non_square_matrix():
    return Matrix([[1, 2, 3], [4, 5, 6]])

def test_det_1x1(square_matrix_1x1):
    assert square_matrix_1x1.det() == 5

def test_det_2x2(square_matrix_2x2):
    assert square_matrix_2x2.det() == -2

def test_det_3x3(square_matrix_3x3):
    assert square_matrix_3x3.det() == 0

def test_non_square_matrix_det(non_square_matrix):
    with pytest.raises(ValueError, match="determinant requires square matrix"):
        non_square_matrix.det()
