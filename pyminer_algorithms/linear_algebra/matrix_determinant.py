import numpy
from numpy import ndarray


def matrix_determinant(arr):
    """
    计算矩阵的行列式。

    Parameters
    ----------
    arr: ndarray
        待计算的矩阵

    Returns
    -------
    deternimant: float
        矩阵的行列式

    Notes
    ------
    本函数参考了 MATLAB 的 ``det`` 函数 [1]_ 以及 ``numpy`` 的 ``linalg.det`` 函数 [2]_ 。

    References
    ---------
    .. [1] ``linalg.det`` 帮助文档. Numpy. https://numpy.org/doc/stable/reference/generated/numpy.linalg.det.html
    .. [2] ``det`` 帮助文档. MATLAB. https://ww2.mathworks.cn/help/matlab/ref/det.html

    """

    assert isinstance(arr, numpy.ndarray), f'only `numpy.ndarray` supported, not "{type(arr)}"'
    assert len(arr.shape) == 2, f'determinant is only valid for 2d array, not "{arr.shape}"'
    assert arr.shape[0] == arr.shape[1], f'determinant is only valid for square matrix, not "{arr.shape}"'
    return numpy.linalg.det(arr)
