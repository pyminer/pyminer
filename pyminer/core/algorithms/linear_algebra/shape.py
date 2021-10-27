from typing import Tuple

import numpy
from numpy import ndarray


def shape(arr: ndarray):
    """
    shape(arr)

    获取矩阵的形状。

    例如， ``shape(ones(3,4,5))==(3,4,5)`` 。

    本函数仅用于对 ``numpy.ndarray`` 进行操作，
    不操作 ``List[float]`` 等复合结构的类矩阵的列表。

    Parameters
    ----------
    arr: ndarray
        任意形状的矩阵。

    Returns
    -------
    result: Tuple[int]
        以元组方式返回矩阵的形状。

    Notes
    ----------
    对于 ``numpy`` 用户，本函数简单返回 ``numpy.ndarray.shape`` 。

    对于 ``matlab`` 用户，本函数部分等价于 ``size`` 。 [1]_ [2]_

    References
    ----------
    .. [1] ``numpy.ndarray.shape`` 帮助文档. Numpy. https://numpy.org/doc/stable/reference/generated/numpy.ndarray.shape.html
    .. [2] ``size`` 帮助文档. MATLAB. https://ww2.mathworks.cn/help/matlab/ref/size.html
    """
    assert isinstance(arr, numpy.ndarray), 'only `numpy.ndarray` supported'
    return arr.shape
