import numpy

from . import _utils
from typing import Tuple
from numpy import ndarray


def ones(shape, *shapes, type=float, dtype=None) -> ndarray:
    """
    ones(*shape, type=float)

    返回一个新的全是 ``1`` 的矩阵，矩阵的维度和大小通过给定的参数进行指定。

    Parameters
    ----------
    shape: Tuple[int]
        矩阵的形状，是整数的数组，整数的个数表示维度，整数的大小表示该维度的大小。
        这个参数可以加括号放在一起，如 ``ones((3,4))`` ，
        也可以不加括号，如 ``ones(3,4)`` ，两种写法等价，不建议加括号。
    type: type
        矩阵的类型，可以是一个 ``python`` 类型或者 ``numpy`` 类型，
        包括 ``int`` 、 ``float`` 等。 ``type`` 也可以写为 ``dtype`` ，以满足 ``numpy`` 用户的习惯。
        具体支持的类型请参照numpy的类型。

    Returns
    -------
    result: ndarray
        按照指定的维度、指定的大小、指定的类型生成的全为`1`的多维矩阵。

    Notes
    -----
    本函数参考了以下文献： [1]_ [2]_ [3]_ [4]_

    References
    -----------
    .. [1] ``numpy`` 的类型. Numpy. https://numpy.org/devdocs/user/basics.types.html
    .. [2] ``ones`` 帮助文档. MATLAB. https://ww2.mathworks.cn/help/matlab/ref/ones.html
    .. [3] ``ones`` 帮助文档. Numpy. https://numpy.org/doc/stable/reference/generated/numpy.ones.html
    .. [4] ``ones`` 帮助文档. R. https://www.rdocumentation.org/packages/matlab/versions/1.0.2/topics/ones
    """
    shape = _utils.preprocess_shape(shape, *shapes)
    type = _utils.preprocess_type(type, dtype)
    return numpy.ones(shape, dtype=type)
