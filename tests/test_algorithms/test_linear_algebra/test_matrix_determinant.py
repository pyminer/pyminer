from pytest import raises

from pyminer_algorithms import *


def test_matrix_determinant():
    assert matrix_determinant(ones(3, 3)) == 0
    assert abs(matrix_determinant(array([[1, 2], [3, 4]])) - (-2)) < 1E14  # MATLAB 同样存在这个问题

    with raises(AssertionError, match='only `numpy.ndarray`'):
        # noinspection PyTypeChecker
        matrix_determinant([[1, 2], [3, 4]])

    with raises(AssertionError, match='determinant is only valid for 2d array'):
        matrix_determinant(ones(3, 3, 3))

    with raises(AssertionError, match='valid for square matrix'):
        matrix_determinant(ones(3, 4))
