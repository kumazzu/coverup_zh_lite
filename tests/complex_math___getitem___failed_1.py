# E                                                                        [100%]
# ==================================== ERRORS ====================================
# ____________________ ERROR at setup of test_matrix_getitem _____________________
# 
#     @pytest.fixture
#     def sample_matrix():
# >       matrix = Matrix()
# E       TypeError: Matrix.__init__() missing 1 required positional argument: 'data'
# 
# test_tmp_f01ebda8.py:6: TypeError
# =========================== short test summary info ============================
# ERROR test_tmp_f01ebda8.py::test_matrix_getitem - TypeError: Matrix.__init__(...

import pytest
from complex_math import Matrix

@pytest.fixture
def sample_matrix():
    matrix = Matrix()
    matrix._data = [[1.0, 2.0], [3.0, 4.0]]
    return matrix

def test_matrix_getitem(sample_matrix):
    assert sample_matrix[0] == [1.0, 2.0]
    assert sample_matrix[1] == [3.0, 4.0]
