from pyminer_algorithms.linear_algebra.zeros import zeros
import numpy
import pytest


def test_normal():
    """
    正常运行情况下的功能检测
    :return:
    """
    numpy.testing.assert_equal(zeros(3, 3), numpy.zeros((3, 3)))
    numpy.testing.assert_equal(zeros((3, 3)), numpy.zeros((3, 3)))

    assert zeros(3, 3).dtype == numpy.dtype(float)
    assert zeros(3, 3, type=int).dtype == numpy.dtype(int)
    assert zeros(3, 3, dtype=int).dtype == numpy.dtype(int)
    with pytest.raises(AssertionError):
        zeros(3, 3, type=int, dtype=int)

    assert zeros(3, 3).shape == (3, 3)
    assert zeros(3, 4, 5).shape == (3, 4, 5)
    assert zeros((3, 4, 6)).shape == (3, 4, 6)
