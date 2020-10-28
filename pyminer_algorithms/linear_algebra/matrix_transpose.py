import numpy
from numpy import ndarray


def matrix_transpose(arr: ndarray) -> ndarray:
    """
    matrix_transpose(arr)

    转置向量或矩阵。

    需要注意的是， ``array`` 必须是一维向量或二维矩阵。
    高维矩阵未定义转置函数。

    转置也可以通过 ``array.T`` 来实现。


    Parameters
    ----------
    arr: ndarray
        待转置的矩阵

    Returns
    -------
    result: ndarray
        对矩阵或向量进行转置后的新矩阵，
        不管输入值是一维矩阵还是二维矩阵，返回值都是二维矩阵。
        关于三维等高维矩阵的支持，后期会添加。

    Notes
    ---------
    在MATLAB里面提到了非共轭转置等内容，看不懂，没有进行相应的实现。

    关于矩阵的大小，MATLAB的矩阵至少是二维的，而 ``numpy`` 支持一维矩阵，因此可能存在歧义。
    在 ``numpy`` 中，转置对于一维数组不产生效果，这实际并不合理。
    本函数遵从 ``matlab`` 的方式，认为一维数组为行向量。

    在 ``numpy.transpose`` 中定义了高维数组的转置方法，
    这一功能目前没有实现，如有需要请自行调用 ``numpy`` 的转置方法。 [1]_ [2]_ [3]_

    References
    ------------
    .. [1] ``transpose`` 帮助文档. MATLAB. https://ww2.mathworks.cn/help/matlab/ref/transpose.html
    .. [2] ``transpose`` 帮助文档. Numpy. https://numpy.org/doc/stable/reference/generated/numpy.transpose.html
    .. [3] ``matrix.transpose`` 帮助文档. Numpy. https://numpy.org/doc/stable/reference/generated/numpy.matrix.transpose.html
    """
    assert len(arr.shape) in (1, 2), '转置操作仅支持一维向量和二维矩阵'
    if len(arr.shape) == 1:
        arr = numpy.atleast_2d(arr)
        return numpy.transpose(arr)
    if len(arr.shape) == 2:
        return numpy.transpose(arr)
