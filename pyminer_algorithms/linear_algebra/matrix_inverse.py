import re

import numpy
from numpy import ndarray

from pyminer_algorithms.linear_algebra.exceptions import LinearAlgebraError


def matrix_inverse(arr: ndarray) -> ndarray:
    """
    matrix_inverse(arr)

    对矩阵求逆。
    矩阵应当是二维方阵。

    Parameters
    ----------
    arr: ndarray
        待求逆的方阵

    Returns
    -------
    result: ndarray
        矩阵的逆矩阵。

    Notes
    ---------
    这个函数直接调用的 ``numpy.linalg.inv`` 函数，
    不过做了一些限制，比如仅支持二维矩阵。 [1]_ [2]_

    References
    ---------------
    .. [1] ``inv`` 帮助文档. Numpy. https://numpy.org/doc/stable/reference/generated/numpy.linalg.inv.html
    .. [2] ``inv`` 帮助文档. MATLAB. https://ww2.mathworks.cn/help/matlab/ref/inv.html

    """
    assert isinstance(arr, numpy.ndarray), 'only `numpy.ndarray` supported'
    assert len(arr.shape) == 2, 'only 2d array supported'
    try:
        return numpy.linalg.inv(arr)
    except numpy.linalg.LinAlgError as error:
        if re.match('Singular matrix', error.args[0]):
            raise LinearAlgebraError('inverse of singular matrix is invalid')
        if re.match(r'Last 2 dimensions of the array must be square', error.args[0]):
            raise LinearAlgebraError('inverse of non-square matrix is invalid')
        raise
