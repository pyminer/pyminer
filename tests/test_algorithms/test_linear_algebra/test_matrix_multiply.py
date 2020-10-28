import pytest
from numpy.testing import assert_equal

from pyminer_algorithms import *


def test_matrix_multiply():
    # 正常使用
    assert_equal(matrix_multiply(ones(3, 4), ones(4, 3)), ones(3, 3) * 4)

    # 传入非二维数组
    with pytest.raises(AssertionError, match='param a .*?, not'):
        # noinspection PyTypeChecker
        matrix_multiply(2, array([1, 2, 3]))
    with pytest.raises(AssertionError, match='param b .*?, not'):
        # noinspection PyTypeChecker
        matrix_multiply(array([1, 2, 3]), 2)
    with pytest.raises(AssertionError, match=r'array a is not matrix, with shape "\(3, 3, 3\)"'):
        matrix_multiply(ones(3, 3, 3), ones(3, 3))
    with pytest.raises(AssertionError, match=r'array b is not matrix, with shape "\(3, 3, 3\)"'):
        matrix_multiply(ones(3, 3), ones(3, 3, 3))
