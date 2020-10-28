import numpy
import pytest

from pyminer_algorithms import *


def test_cross():
    """
    这个用例用于测试numpy本身的cross的功能。
    """
    # 对于三个元素的向量，就是标准的叉积，叉积后为垂直于两个向量方向的新向量
    a = array([1, 2, -2])
    b = array([1, 1, -4])
    numpy.testing.assert_equal(matrix_cross(a, b), array([-6, 2, -1]))
    assert numpy.dot(numpy.cross(a, b), a) == 0  # 检测垂直
    assert numpy.dot(numpy.cross(a, b), b) == 0

    # 对于两个元素的向量
    a = array([1, 2])
    b = array([2, 3])
    assert matrix_cross(a, b).shape == ()  # 原本是一维的两个向量，变成了零维，维度降低了
    assert matrix_cross(a, b) == -1

    # 对于四个元素的向量，应该报错
    a = array([1, 2, 3, 4])
    b = array([5, 6, 7, 8])
    with pytest.raises(AssertionError, match='last dimension of array a should be 2 or 3, not "4"'):
        matrix_cross(a, b)

    # 只要最后一位是3就可以计算
    a = ones(6, 5, 4, 3)
    b = ones(6, 5, 4, 3)
    assert matrix_cross(a, b).shape == (6, 5, 4, 3)
    assert (matrix_cross(a, b) == 0).all()

    # 检测如何按照最后一个轴进行计算
    a = ones(6, 5, 4, 3).cumsum().reshape((6, 5, 4, 3))
    b = ones(6, 5, 4, 3).cumsum().reshape((6, 5, 4, 3)) * 2
    c = matrix_cross(a, b)
    assert c.shape == (6, 5, 4, 3)
    numpy.testing.assert_equal(c[0, 0, 0, :], matrix_cross(a[0, 0, 0, :], b[0, 0, 0, :]))
    numpy.testing.assert_equal(c[4, 2, 3, :], matrix_cross(a[4, 2, 3, :], b[4, 2, 3, :]))

    # 检测如何按照最后一个轴进行计算
    a = ones(6, 5, 4, 2).cumsum().reshape((6, 5, 4, 2))
    b = ones(6, 5, 4, 2).cumsum().reshape((6, 5, 4, 2)) * 2
    c = matrix_cross(a, b)
    assert c.shape == (6, 5, 4)  # 发生降维
    numpy.testing.assert_equal(c[0, 0, 0], matrix_cross(a[0, 0, 0, :], b[0, 0, 0, :]))
    numpy.testing.assert_equal(c[4, 2, 3], matrix_cross(a[4, 2, 3, :], b[4, 2, 3, :]))

    # 两个矩阵应当是同样的大小
    a = ones(6, 5, 4, 3).cumsum().reshape((6, 5, 4, 3))
    b = ones(6, 5, 3, 3).cumsum().reshape((6, 5, 3, 3))
    with pytest.raises(AssertionError, match='two array should have same shape'):
        matrix_cross(a, b)

    # 非标准array（也就是List[float]）虽然理论上可以计算，但本函数不承认该变量是一个合法的参数
    with pytest.raises(AssertionError, match='parameter a should be an array, not'):
        # noinspection PyTypeChecker
        matrix_cross((1, 2, 3), (3, 2, 1))
