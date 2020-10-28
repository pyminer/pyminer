from pyminer_algorithms import *


def test_dot():
    # 目前仅支持一维向量
    a = ones(3)
    b = ones(3)
    assert matrix_dot(a, b) == 3
    assert matrix_dot(a, b).shape == ()
