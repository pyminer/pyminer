import re
from typing import Iterable

import numpy
from numpy import ndarray

from pyminer_algorithms.linear_algebra.exceptions import LinearAlgebraError


def reshape(arr: ndarray, shape: Iterable[int]):
    """
    reshape(arr, shape)

    改变矩阵的形状。

    Parameters
    ----------
    arr: ndarray
        原始矩阵
    shape: Iterable[int]
        新的矩阵的形状

    Returns
    -------
    result: ndarray
        形状改变后的矩阵。

    Notes
    ---------
    本函数并不是 ``numpy.reshape`` ，而是对其的封装。
    本函数并不支持 ``numpy.reshape`` 的一系列高级操作，
    例如基于内存的顺序等。
    如有需要请直接使用 ``numpy.reshape`` 。

    ``MATLAB`` 的 ``reshape`` 函数支持 ``shape`` 和 ``*shape`` 两种方式。
    由于时间考虑现仅支持 ``shape`` 的参数调用方式。
    如您有时间欢迎补全。 [1]_ [2]_

    References
    -------------
    .. [1] ``reshape`` 帮助文档. Numpy. https://numpy.org/doc/stable/reference/generated/numpy.reshape.html
    .. [2] ``matlab`` 帮助文档. MATLAB. https://ww2.mathworks.cn/help/matlab/ref/reshape.html
    """
    assert isinstance(arr, numpy.ndarray), 'first param should be instance of `numpy.ndarray`'
    assert isinstance(shape, tuple), 'second param should be tuple of int'
    for i in shape:
        assert isinstance(i, int), f'shape items should be int, not "{i}"'
        assert i >= 0, f'shape items should be non-negative integers'
    try:
        return numpy.reshape(arr, shape)
    except ValueError as exception:
        if re.match(r'cannot reshape array of size \d+ into shape', exception.args[0]):
            raise LinearAlgebraError(exception.args[0])
        raise
