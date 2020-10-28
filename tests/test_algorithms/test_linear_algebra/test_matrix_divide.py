import numpy
import pytest

from pyminer_algorithms import *
from pyminer_algorithms.linear_algebra.exceptions import LinearAlgebraError


def test_matrix_divide():
    a = array([[8, 1, 6],
               [3, 5, 7],
               [4, 9, 2]])
    b = array([[15], [15], [15]])
    numpy.testing.assert_almost_equal(matrix_divide(a, b), ones((3, 1)), decimal=15)

    a = array([[8, 1, 6],
               [3, 5, 7],
               [4, 9, 2]])
    b = array([[15, 5],
               [15, 5],
               [15, 5]])
    c = array([[1, 1 / 3],
               [1, 1 / 3],
               [1, 1 / 3]])
    numpy.testing.assert_almost_equal(matrix_divide(a, b), c, decimal=14)

    with pytest.raises(AssertionError, match='param a should be'):
        # noinspection PyTypeChecker
        matrix_divide([1, 2, 3], [3, 4, 1])

    with pytest.raises(AssertionError, match='param b should be'):
        # noinspection PyTypeChecker
        matrix_divide(ones(3, 3), [3, 4, 1])

    with pytest.raises(AssertionError, match=r'columns\(a\)'):
        matrix_divide(ones(4, 4), ones(5, 4))

    with pytest.raises(LinearAlgebraError, match='should not be singular matrix'):
        matrix_divide(ones(4, 4), ones((4, 4)))
