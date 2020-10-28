from pyminer_algorithms import *


def test_shape():
    assert shape(ones(3, 4, 5)) == (3, 4, 5)
