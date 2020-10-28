import numpy
from numpy import ndarray
from pyminer_algorithms.linear_algebra.exceptions import LinearAlgebraError


def matrix_eigenvalue(arr: ndarray):
    """
    matrix_eigenvalue(arr)

    计算矩阵的特征值和特征向量。

    特征值是一个一维矩阵，其长度与传入矩阵的长度相同，
    其中的每一个值都是一个特征值。
    如果某一个特征值存在多个，则矩阵中就存在它的多个拷贝。
    特征值没有顺序。
    如果特征值全为实数，则返回实数矩阵，否则返回复数矩阵。

    特征向量是一个与传入矩阵同形的方阵。
    每一个特征向量都是归一化的特征向量（长度为单位长度）。
    如果特征向量矩阵为 ``v`` ，特征值矩阵为 ``w`` ，
    则向量 ``v[:, i]`` 就是特征值 ``w[i]`` 的特征向量。

    Parameters
    ----------
    arr: ndarray
        待计算的矩阵

    Returns
    -------
    eigenvalue: ndarray
        特征值一维向量。
    eigenvector: ndarray
        特征向量构成的矩阵。

    Raises
    ---------
    AssertionError
        如果传入值不是方阵。

    LinearAlgebraError
        如果特征值计算不收敛。

    Notes
    ----------
    在 ``matlab`` 和 ``numpy`` 中，特征值和特征向量都统一采用一个函数来表示。
    因此本函数也采用类似的方法。

    关于特征值和特征向量的一些复杂计算，
    本人没有能力实现，希望大佬可以帮助实现一下。
    这里仅提供了一个基本的特征值和特征向量的计算。 [1]_ [2]_

    References
    ------------
    .. [1] ``numpy.linalg.eig`` 帮助文档. Numpy. https://numpy.org/doc/stable/reference/generated/numpy.linalg.eig.html
    .. [2] ``eig`` 帮助文档. MATLAB. https://ww2.mathworks.cn/help/matlab/ref/eig.html
    """
    assert len(arr.shape) == 2, f'Eigenvalue is only valid for 2D matrix, not "{arr.shape}"'
    try:
        return numpy.linalg.eig(arr)
    except numpy.linalg.LinAlgError as error:
        raise LinearAlgebraError(error.args[0])
