import pytest
from complex_math import Matrix

@pytest.fixture
def sample_matrix_2x2():
    return Matrix([[1, 2], [3, 4]])

def test_matrix_addition_success(sample_matrix_2x2):
    other = Matrix([[5, 6], [7, 8]])
    result = sample_matrix_2x2 + other
    assert result[0][0] == 6
    assert result[0][1] == 8
    assert result[1][0] == 10
    assert result[1][1] == 12

def test_matrix_addition_dimension_mismatch(sample_matrix_2x2):
    other = Matrix([[1, 2, 3], [4, 5, 6]])
    with pytest.raises(ValueError, match="dimension mismatch for add"):
        sample_matrix_2x2 + other
