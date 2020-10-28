from numpy.testing import assert_equal

from pyminer_algorithms import *


def test_linear_space():
    assert linear_space(1, 100, 100).shape == (100,)
    assert_equal(linear_space(1, 100, 100)[:5], array([1, 2, 3, 4, 5]))
    assert_equal(linear_space(array([1, 1]), array([3, 5]), 5), array([
        [1, 1],
        [1.5, 2],
        [2, 3],
        [2.5, 4],
        [3, 5],
    ]))
