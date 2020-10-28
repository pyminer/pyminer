import pytest

from pyminer_algorithms import *
from pyminer_algorithms.linear_algebra.exceptions import LinearAlgebraError


def test_reshape():
    assert shape(reshape(ones(4, 4, 4), (8, 8))) == (8, 8)

    with pytest.raises(LinearAlgebraError, match=r'cannot reshape array of size 27 into shape \(9,1\)'):
        reshape(ones(3, 3, 3), (9, 1))
