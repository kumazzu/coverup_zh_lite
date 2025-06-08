import pytest
from complex_math import Matrix

@pytest.fixture
def sample_matrix():
    matrix = Matrix([[1.0, 2.0], [3.0, 4.0]])
    return matrix

def test_matrix_getitem(sample_matrix):
    assert sample_matrix[0] == [1.0, 2.0]
    assert sample_matrix[1] == [3.0, 4.0]
