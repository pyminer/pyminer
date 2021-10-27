import numpy

from pyminer_algorithms.linear_algebra.exceptions import LinearAlgebraError
from numpy import ndarray


def matrix_divide(a: numpy.ndarray, b: numpy.ndarray) -> numpy.ndarray:
    """
    matrix_divide(a, b)

    矩阵的除法。

    在 ``pyminer-algorithms`` 中我们采用线性代数对除法的通常理解，即：

    .. math::
        Ax=B，x=A^{-1}B

    这在 ``MATLAB`` 当中也可以被称为左除，即对 ``inverse(A)`` 这一项在 ``B`` 的左侧。

    目前仅支持两维数组，后续会支持将高维数组作为多个两维数组进行计算。
    （恳请您能帮忙实现）

    Parameters
    ----------
    a: ndarray
        :math:`Ax=B` 中的 :math:`A` 。
    b: ndarray
        :math:`Ax=B` 中的 :math:`B` 。

    Returns
    -------
    result: ndarray
        矩阵除法的运算结果，:math:`Ax=B` 中的 :math:`x` 。

    Notes
    ---------

    ``matlab`` 中定义了四种除法：
    矩阵的按位左除 ``.\\`` 、矩阵的按位右除 ``./`` 、矩阵的左除 ``\\`` 、矩阵的右除 ``/`` 。
    其中按位指的是对矩阵的每一个格子进行分别的计算，
    而非线性代数意义上的矩阵的除法。 [1]_ [2]_

    在 ``PyMiner`` 中，直接对矩阵进行 ``*`` 和 ``/`` 操作表示对矩阵进行按位乘法和按位除法。
    矩阵的乘除法需要使用 ``matrix_multiply`` 和 ``matrix_divide`` 进行计算。
    这主是要由于矩阵的乘法和除法并非一个通用的内容，
    对于多维数组这两个功能实际上是无用的，
    因此 ``pyminer-algorithms`` 不将其做为重要函数，故加了 ``matrix`` 前缀。

    在 ``numpy`` 中是采用 ``numpy.solve`` 作为除法运算的，
    这个函数表义不是太清晰，
    个人认为不如 ``matrix_divide`` 清晰，故斗胆使用此命名，
    如有建议或意见请提出。 [3]_ [4]_


    References
    ------------
    .. [1] ``mrdivide`` 帮助文档. MATLAB. https://ww2.mathworks.cn/help/fixedpoint/ref/embedded.fi.mrdivide.html
    .. [2] ``mldivide`` 帮助文档. MATLAB. https://ww2.mathworks.cn/help/matlab/ref/mldivide.html
    .. [3] ``numpy.solve`` 帮助文档. Numpy. https://numpy.org/doc/stable/reference/generated/numpy.linalg.solve.html
    .. [4] ``scipy.solve`` 帮助文档. Numpy. https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.solve.html

    Examples
    ----------
    矩阵自己除自己，显然应该得到单位矩阵：

    >>> from pyminer_algorithms import *
    >>> arr1 = array([
    ...     [1, 2, 3],
    ...     [4, 5, 6],
    ...     [7, 8, 5],
    ... ])
    >>> arr2 = arr1
    >>> matrix_divide(arr1, arr2)
    array([[1., 0., 0.],
           [0., 1., 0.],
           [0., 0., 1.]])

    在MATLAB中，定义了矩阵的左除与矩阵的右除。
    对于 :math:`AB=C` ，右除为 :math:`A=CB^{-1}` ，左除为 :math:`B=A^{-1}C` 。

    矩阵的左除，即已知 :math:`A` 和 :math:`C` 求 :math:`B` ，可以简单地调用 ``matrix_divide`` 函数：

    .. math::
        AB = C

        B = A^{-1} C

    >>> from pyminer_algorithms import *
    >>> a = array([
    ...     [1, 1, 0],
    ...     [0, 1, 0],
    ...     [0, 0, 1]])
    >>> b = array([
    ...     [1, 1, 1],
    ...     [0, 1, 0],
    ...     [0, 0, 1],
    ... ])
    >>> c = matrix_multiply(a, b)
    >>> c
    array([[1, 2, 1],
           [0, 1, 0],
           [0, 0, 1]])
    >>> matrix_divide(a, c)
    array([[1., 1., 1.],
           [0., 1., 0.],
           [0., 0., 1.]])

    矩阵的右除，即已知 :math:`B` 和 :math:`C` 求:math:`A` ，可以采用如下替代实现：

    .. math::
        AB=C

        B^T A^T = C^T

        A^T = (B^T)^{-1} \\ C^T

        A = ((B^T)^{-1} \\ C^T)^T

    >>> matrix_divide(b.T, c.T).T
    array([[1., 1., 0.],
           [0., 1., 0.],
           [0., 0., 1.]])

    """

    assert isinstance(a, numpy.ndarray), 'param a should be `numpy.ndarray`'
    assert isinstance(b, numpy.ndarray), 'param b should be `numpy.ndarray`'
    assert len(a.shape) == len(b.shape) == 2, 'only two dimensional array supported'
    assert a.shape[0] == b.shape[0], 'columns(a) should be equal to columns(b)'
    try:
        return numpy.linalg.solve(a, b)
    except numpy.linalg.LinAlgError as exception:
        info = exception.args[0]
        if info == 'Singular matrix':
            raise LinearAlgebraError('matrix a should not be singular matrix')
        raise


if __name__ == '__main__':
    import doctest

    doctest.testmod()
