import numpy
from  numpy import ndarray

def matrix_multiply(a: ndarray, b: ndarray) -> ndarray:
    """
    matrix_multiply(a, b)


    计算矩阵的乘积。
    如果 ``a`` 是 ``m×p`` 矩阵， ``b`` 是 ``p×n`` 矩阵，则计算结果 ``c`` 为 ``m×n`` 矩阵。
    其中， ``c`` 的第 ``i`` 行第 ``j`` 列为 ``a`` 的第 ``i`` 行与 ``b`` 的第 ``j`` 列的内积。

    目前仅支持两维数组，后续会支持将高维数组作为多个两维数组进行计算。
    （恳请您能帮忙实现）


    Parameters
    ----------
    a: ndarray
        矩阵乘法运算的第一个矩阵
    b: ndarray
        矩阵乘法运算的第二个矩阵

    Returns
    -------
    result: ndarray
        矩阵乘法的计算结果。

    Notes
    ------
    在 ``matlab`` 中，矩阵乘法可以直接用乘号 ``*`` 来表示。
    在 ``numpy`` 中，对应的函数为 ``numpy.matmul`` ，也就是 ``matrix multiply`` 的简写。
    在 ``numpy`` 中的乘号 ``*`` 表示数乘，或者按位乘，不是线性代数意义上的矩阵的乘法。 [1]_ [2]_

    References
    -----------
    .. [1] MATLAB中的矩阵乘法. MATLAB. https://ww2.mathworks.cn/help/matlab/ref/mtimes.html
    .. [2] ``numpy.matmul`` 帮助文档. Numpy. https://numpy.org/doc/stable/reference/generated/numpy.matmul.html

    """
    assert isinstance(a, numpy.ndarray), f'param a should be `numpy.ndarray` instance, not "{type(a)}"'
    assert isinstance(b, numpy.ndarray), f'param b should be `numpy.ndarray` instance, not "{type(b)}"'
    assert len(a.shape) == 2, f'array a is not matrix, with shape "{a.shape}"'
    assert len(b.shape) == 2, f'array b is not matrix, with shape "{b.shape}"'
    return numpy.matmul(a, b)
