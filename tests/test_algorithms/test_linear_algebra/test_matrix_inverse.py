import pytest
from numpy.testing import assert_almost_equal

from pyminer_algorithms import *
from pyminer_algorithms.linear_algebra.exceptions import LinearAlgebraError


def test_matrix_inverse():
    assert_almost_equal(matrix_inverse(array([[1, 2], [3, 4]])),
                        array([[-2, 1], [1.5, -0.5]]), decimal=15)

    with pytest.raises(LinearAlgebraError, match='inverse of singular'):
        assert matrix_inverse(zeros(3, 3))

    with pytest.raises(LinearAlgebraError, match='inverse of non-square matrix'):
        assert matrix_inverse(zeros(4, 3))
