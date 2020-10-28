from numpy import sqrt
from numpy.testing import assert_equal

from pyminer_algorithms import *


def test_matrix_eigenvalue():
    # 由于本人线性代数能力有限，此处仅进行了基本的测试
    a = matrix_diagonal(array([1, 2, 3]))
    w, h = matrix_eigenvalue(a)
    assert_equal(w, array([1, 2, 3]))
    assert_equal(h, array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]))

    a = array([
        [1, 2],
        [2, 4],
    ])
    w, h = matrix_eigenvalue(a)
    assert_equal(w, array([0, 5]))
    assert_equal(h, array([
        [-2, -1],
        [1, -2],
    ]) / sqrt(5))
    assert (matrix_multiply(a, reshape(h[:, 1], (2, 1))), w[1] * h[:, 1])
    assert (matrix_multiply(a, reshape(h[:, 0], (2, 1))), w[0] * h[:, 0])
