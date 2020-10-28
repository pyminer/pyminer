from numpy.testing import assert_equal
from pytest import raises

from pyminer_algorithms import *
from pyminer_algorithms.linear_algebra.exceptions import LinearAlgebraError


def test_matrix_diagonal():
    assert_equal(matrix_diagonal(array([1, 2, 3])), array([
        [1, 0, 0],
        [0, 2, 0],
        [0, 0, 3],
    ]))
    assert_equal(matrix_diagonal(array([1, 2, 3]), 1), array([
        [0, 1, 0, 0],
        [0, 0, 2, 0],
        [0, 0, 0, 3],
        [0, 0, 0, 0],
    ]))

    assert_equal(matrix_diagonal(array([
        [1, 0, 0],
        [0, 2, 0],
        [0, 0, 3],
    ])), array([1, 2, 3]))
    assert_equal(matrix_diagonal(array([
        [0, 1, 0, 0],
        [0, 0, 2, 0],
        [0, 0, 0, 3],
        [0, 0, 0, 0],
    ]), 1), array([1, 2, 3]))

    with raises(AssertionError, match='should be `numpy.ndarray`'):
        # noinspection PyTypeChecker
        matrix_diagonal([1, 2, 3])
    with raises(LinearAlgebraError, match='only 1d array or 2d array supported'):
        matrix_diagonal(ones(3, 3, 3))
