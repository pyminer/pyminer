import numpy
import pytest

from pyminer_algorithms import *


def test_transpose():
    # 测试一维矩阵
    a = numpy.ones((3,))
    assert matrix_transpose(a).shape == (3, 1)

    # 测试二维矩阵
    a = numpy.ones((3, 4))
    assert matrix_transpose(a).shape == (4, 3)

    # 测试三维矩阵
    a = numpy.ones((3, 4, 5))
    with pytest.raises(AssertionError):
        matrix_transpose(a)
