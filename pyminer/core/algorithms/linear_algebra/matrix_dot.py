import numpy
from numpy import ndarray


def matrix_dot(a: numpy.ndarray, b: numpy.ndarray) -> numpy.ndarray:
    """
    matrix_dot(a, b)

    返回两个矩阵的点积（内积）。
    两个矩阵必须是相同的大小。

    对于向量就是简单的点积。

    对于多维矩阵，将会在最后一个维度上计算点积。
    （由于在numpy中暂时没有找到对应的实现方式，故暂时没有实现，即现在仅支持一维向量）。

    在计算后，矩阵会发生降维，即最后一个维度由于进行了点积算而从一维变成了零维。
    这时的计算实际上是将矩阵理解为众多的空间向量分别进行计算。
    （参考 :mod:`.matrix_cross` 的文档说明，由于目前尚未实现故不进行进一步的说明。）

    Parameters
    ----------
    a: ndarray
        用于点积计算的第一个矩阵。
    b: ndarray
        用于点积计算的第二个矩阵。

    Returns
    -------

    result: ndarray
        点积计算得到的结果。
        返回值是相对于参数降低了一维（最后一个维度）的矩阵。

    Notes
    -------

    这个函数与 ``matlab`` 的 ``dot`` 比较接近，与 ``numpy.dot`` 完全不同。
    ``numpy.dot`` 融合了数乘、点积、矩阵乘法等多个因素，
    根据输入参数的不同，判断采用何种方法，过于复杂，表意不明，故没有采用。
    如果您有高级需求，请直接调用 ``numpy.dot`` 进行操作。 [1]_ [2]_ [3]_

    References
    ------------
    .. [1] ``dot`` 帮助文档. MATLAB. https://ww2.mathworks.cn/help/matlab/ref/dot.html
    .. [2] ``dot`` 帮助文档. Numpy. https://numpy.org/doc/stable/reference/generated/numpy.dot.html
    .. [3] ``dot`` 帮助文档. Octave. https://octave.sourceforge.io/octave/function/dot.html
    """
    assert isinstance(a, numpy.ndarray), f'dot only supply numpy.ndarray object, while a is "{type(a)}"'
    assert isinstance(b, numpy.ndarray), f'dot only supply numpy.ndarray object, while a is "{type(b)}"'
    assert a.shape[-1] in (2, 3), f'last dimension of array a should be 2 or 3, not "{a.shape[-1]}"'
    assert b.shape[-1] in (2, 3), f'last dimension of array b should be 2 or 3, not "{b.shape[-1]}"'
    assert a.shape == b.shape, f'two array should have same shape, not "{a.shape}" & "{b.shape}"'
    assert len(a.shape) == 1, f'currently only support 1 dimension, not {len(a.shape)}'
    return numpy.dot(a, b)
