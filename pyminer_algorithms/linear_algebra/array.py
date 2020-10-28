import numpy

from pyminer_algorithms.linear_algebra.exceptions import LinearAlgebraError


def array(data, type=None, dtype=None):
    """
    将已有的值转换为一个矩阵。别名 ``matrix`` 。

    Parameters
    -------------
    data: any
        现有的列表
    type: type
        矩阵的类型，可以是一个 ``python`` 类型或者 ``numpy`` 类型，包括 ``int`` 、 ``float`` 等。
        ``type`` 也可以写为 ``dtype`` ，以满足 ``numpy`` 用户的习惯。
        如果不指定 ``type`` ，则 ``PyMiner`` 会自己根据数据判断类型。
        具体支持的类型请参照 `numpy的类型 <https://numpy.org/devdocs/user/basics.types.html>`_ 。
    dtype: type
        ``type`` 的别名，用于 ``numpy`` 兼容

    Returns
    --------
    根据指定的数据、指定的类型生成矩阵。

    Raises
    ---------
    LinearAlgebraError
        如果不能生成矩阵，则返回该错误。
        本函数相对于 ``np.array`` 进行了限制，不接受作为对象而存在的数据类型，
        因此对于非方形的矩阵，将会报此错误。

    Notes
    ---------
    本函数与 ``numpy.array`` 有较大的差别，
    如果需要进行底层的 ``array`` 控制，请采用类似如下方式以访问 ``numpy`` 原生的 ``array`` [1]_ 。

    References
    ---------------

    .. [1] ``array`` 帮助文档. Numpy. https://numpy.org/doc/stable/reference/generated/numpy.array.html

    Examples
    ---------

    >>> from pyminer_algorithms import *

    可以基于列表生成矩阵，包括可以生成一维矩阵、二维矩阵、高维矩阵等。

    >>> array([1, 2, 3])
    array([1, 2, 3])
    >>> array([[1, 2, 3], [4, 5, 6]])
    array([[1, 2, 3],
           [4, 5, 6]])
    >>> array([[1, 2], [3, 4], [5, 6]])
    array([[1, 2],
           [3, 4],
           [5, 6]])
    >>> array([[[1, 2], [3, 4],
    ...         [5, 6], [7, 8]],
    ...        [[9, 10], [11, 12],
    ...         [13, 14], [15, 16]]])
    array([[[ 1,  2],
            [ 3,  4],
            [ 5,  6],
            [ 7,  8]],
    <BLANKLINE>
           [[ 9, 10],
            [11, 12],
            [13, 14],
            [15, 16]]])
    >>> shape(array([[1, 2], [3, 4], [5, 6]]))
    (3, 2)


    基于矩阵生成的矩阵是原矩阵的拷贝。

    >>> arr1 = array([1, 2, 3]); arr1
    array([1, 2, 3])
    >>> arr2 = array(arr1); arr2
    array([1, 2, 3])
    >>> arr1[2] = 4; arr1
    array([1, 2, 4])
    >>> arr2
    array([1, 2, 3])

    ``array`` 函数不仅支持在根据列表生成矩阵时指定数据类型，还支持将已有的矩阵切换数据类型。
    在进行数据类型的切换时，从浮点型向整型时，数据会做向下取整。

    >>> arr1 = array([1, 2, 3], float); arr1
    array([1., 2., 3.])
    >>> arr2 = array(arr1, int); arr2
    array([1, 2, 3])
    >>> arr3 = array([1.1, 2.2, 3.9], int); arr3
    array([1, 2, 3])

    如果传入参数并非方形矩阵，将会报错。这对于 ``np.array`` 是合理的，
    但是为了避免奇怪的异常，暂时不打算支持 ``object`` 数据类型。
    如确有相关需求可以直接使用 ``np.array`` 创建相应的矩阵。

    >>> arr = array([[1, 2], [3]])
    Traceback (most recent call last):
    pyminer_algorithms.linear_algebra.exceptions.LinearAlgebraError: Data is not a matrix.
    >>> import numpy as np
    >>> np.array([[1, 2], [3]])
    array([list([1, 2]), list([3])], dtype=object)

    关于 ``dtype`` 参数和 ``type`` 参数，二者是一致的，
    个人倾向于使用位置参数即可。

    >>> array([1, 2, 3], float)
    array([1., 2., 3.])
    >>> array([1, 2, 3], type=float)
    array([1., 2., 3.])
    >>> array([1, 2, 3], dtype=float)
    array([1., 2., 3.])

    """

    if type is None:
        if dtype is None:
            cleaned_type = None
        else:
            cleaned_type = dtype
    else:
        if dtype is None:
            cleaned_type = type
        else:
            assert False, 'specify both `type` and `dtype` is not allowed'
    result = numpy.array(data, dtype=cleaned_type)
    if result.dtype == object:
        raise LinearAlgebraError('Data is not a matrix.')
    return result


if __name__ == '__main__':
    from doctest import testmod

    testmod()
