# F                                                                        [100%]
# =================================== FAILURES ===================================
# _____________________________ TestMatrix.test_repr _____________________________
# 
# self = <test_tmp_df973d47.TestMatrix object at 0x7f573232c730>
# 
#     def test_repr(self):
#         matrix = Matrix([[1, 2], [3, 4]])
# >       assert repr(matrix) == "Matrix([[1, 2], [3, 4]])"
# E       AssertionError: assert 'Matrix([[1.0... [3.0, 4.0]])' == 'Matrix([[1, 2], [3, 4]])'
# E         
# E         - Matrix([[1, 2], [3, 4]])
# E         + Matrix([[1.0, 2.0], [3.0, 4.0]])
# E         ?           ++   ++     ++   ++
# 
# test_tmp_df973d47.py:7: AssertionError
# =========================== short test summary info ============================
# FAILED test_tmp_df973d47.py::TestMatrix::test_repr - AssertionError: assert '...

import pytest
from complex_math import Matrix

class TestMatrix:
    def test_repr(self):
        matrix = Matrix([[1, 2], [3, 4]])
        assert repr(matrix) == "Matrix([[1, 2], [3, 4]])"
