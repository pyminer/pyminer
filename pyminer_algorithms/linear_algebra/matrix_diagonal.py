import numpy

from pyminer_algorithms.linear_algebra.exceptions import LinearAlgebraError
from numpy import ndarray


def matrix_diagonal(arr: numpy.ndarray, k: int = 0) -> numpy.ndarray:
    """
    matrix_diagonal(arr, k=0)

    获取矩阵的对角线或根据对角线生成矩阵。

    Parameters
    ----------
    arr: ndarray
        用于生成矩阵的对角线元素，或者用于获取对角线的矩阵。
    k: int
        对角线的位置， ``0`` 为主对角线， ``1`` 为主对角线向上一层， ``-1`` 为主对角线向下一层。

    Returns
    -------
    result: ndarray
        参数二维则返回其对角线上的元素；参数一维则返回根据其生成的二维矩阵。

    Notes
    --------
    本函数参考了 ``numpy`` 的 ``diag`` 的帮助文档 [1]_ 和 MATLAB 的 ``diag`` 帮助文档 [2]_ 。

    References
    -------------
    .. [1] ``diag`` 帮助文档. Numpy. https://numpy.org/doc/stable/reference/generated/numpy.diag.html
    .. [2] ``matlab`` 帮助文档. MATLAB. https://ww2.mathworks.cn/help/matlab/ref/diag.html

    """
    assert isinstance(arr, numpy.ndarray), 'param 1 should be `numpy.ndarray`'
    assert isinstance(k, int), 'param 2 should be `int`'
    try:
        return numpy.diag(arr, k)
    except ValueError as e:
        if e.args[0] == 'Input must be 1- or 2-d.':
            raise LinearAlgebraError('only 1d array or 2d array supported')
        raise
