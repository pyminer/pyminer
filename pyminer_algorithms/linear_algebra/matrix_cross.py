import numpy


def matrix_cross(a: numpy.ndarray, b: numpy.ndarray) -> numpy.ndarray:
    """
    matrix_cross(a, b)

    返回两个矩阵的叉积。

    两个矩阵必须是相同的大小，且最后一维必须是2或者3。

    如果矩阵的最后一维是2，则计算后该维度消失，即发生降维。
    这种情况下的特殊情况是两个平面向量，也就是形状为 ``(2,)`` 的矩阵，叉积后的结果是一个零维的数。

    如果矩阵的最后一维是3，则计算结果的形状与两个参数的形状相同。
    这种情况下的特殊情况是两个空间向量，
    也就是形状为 ``(3,)`` 的矩阵，叉积后的结果仍为一个空间向量。

    对于两个高维矩阵而言，要求矩阵的最后一个维度为2或3。
    这时的计算实际上是将矩阵理解为众多的空间向量分别进行计算：


    Parameters
    -------------
    a: array
        用于叉积计算的第一个矩阵；
    b: array
        用于叉积计算的第二个矩阵。

    Returns
    -----------
    叉积计算后得到的结果。
    如果两个参数的最后一维是2则返回参数降一维（最后一维度）的矩阵。
    如果两个参数的最后一维是3则返回与原数同形的矩阵。

    Notes
    ------
    本函数与 ``numpy.cross`` 和 ``MATLAB`` 中的 ``cross`` 函数都有较大的区别，请注意。

    ``numpy.cross`` 的功能强于本函数。
    如果您需要全功能的函数，请参考 `numpy.cross的帮助文档`__ 。 [1]_

    .. __: https://numpy.org/doc/stable/reference/generated/numpy.cross.html

    ``MATLAB`` 的功能稍强于本函数，
    支持指定通过哪一维度进行计算，
    而本函数直接指定通过最后一维进行计算。
    这是出于对开发时间的考虑而不得不做出的暂时性的删减。 [2]_

    References
    ------------
    .. [1] ``cross`` 帮助文档. MatPlotLib. https://ww2.mathworks.cn/help/matlab/ref/cross.html
    .. [2] ``cross`` 帮助文档. Numpy. https://numpy.org/doc/stable/reference/generated/numpy.cross.html

    Examples
    -----------
    >>> from pyminer_algorithms import matrix_cross, ones
    >>> import numpy
    >>> a = ones(6, 5, 4, 3).cumsum().reshape((6, 5, 4, 3))
    >>> b = ones(6, 5, 4, 3).cumsum().reshape((6, 5, 4, 3)) * 2
    >>> c = matrix_cross(a, b)
    >>> assert c.shape == (6, 5, 4, 3)
    >>> numpy.testing.assert_equal(c[0, 0, 0, :], matrix_cross(a[0, 0, 0, :], b[0, 0, 0, :]))
    >>> numpy.testing.assert_equal(c[4, 2, 3, :], matrix_cross(a[4, 2, 3, :], b[4, 2, 3, :]))

    在上面的算例中，经过叉积运算后的矩阵与两个参数同形，均为四维矩阵。
    且对于切片 ``[4,2,3,:]`` ，先切片再叉积与先叉积再切片的结果一致。
    """

    assert isinstance(a, numpy.ndarray), f'parameter a should be an array, not "{type(a)}"'
    assert isinstance(b, numpy.ndarray), f'parameter b should be an array, not "{type(b)}"'
    assert a.shape[-1] in (2, 3), f'last dimension of array a should be 2 or 3, not "{a.shape[-1]}"'
    assert b.shape[-1] in (2, 3), f'last dimension of array b should be 2 or 3, not "{b.shape[-1]}"'
    assert a.shape == b.shape, f'two array should have same shape, not "{a.shape}" & "{b.shape}"'
    return numpy.cross(a, b)
