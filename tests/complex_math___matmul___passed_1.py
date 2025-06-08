import pytest
from complex_math import Matrix

@pytest.fixture
def sample_matrix_2x3():
    return Matrix([[1, 2, 3], [4, 5, 6]])

@pytest.fixture
def sample_matrix_3x2():
    return Matrix([[1, 2], [3, 4], [5, 6]])

@pytest.fixture
def sample_matrix_2x2_invalid():
    return Matrix([[1, 2], [3, 4]])

def test_matmul_valid_dimensions(sample_matrix_2x3, sample_matrix_3x2):
    result = sample_matrix_2x3 @ sample_matrix_3x2
    assert isinstance(result, Matrix)
    assert result.m == 2
    assert result.n == 2

def test_matmul_invalid_dimensions(sample_matrix_2x3, sample_matrix_2x2_invalid):
    with pytest.raises(ValueError, match="dimension mismatch for matmul"):
        sample_matrix_2x3 @ sample_matrix_2x2_invalid
