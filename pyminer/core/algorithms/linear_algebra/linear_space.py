from typing import Union

import numpy


def linear_space(start: Union[float, numpy.ndarray], end: Union[float, numpy.ndarray], step: int):
    """
    在 ``start`` 和 ``stop`` 之间（包括两端点）生成 ``count`` 个点位。

    Parameters
    -----------
    start: float or array
        起点处的位置，可以是一个标量或矩阵
    end: float or array
        终点处的位置，可以是一个标量或矩阵
    step: int
        点位数量，包括起点和终点

    Returns
    ------------
    比 ``start`` 和 ``stop`` 高一维的矩阵

    Notes
    ------
    本函数参照了 MATLAB 的 linspace 函数 [1]_ 和 numpy 的 ``linspace`` 函数 [2]_ 。

    References
    ------------
    .. [1] ``linspace`` 帮助文档. Numpy. https://numpy.org/doc/stable/reference/generated/numpy.linspace.html
    .. [2] ``linspace`` 帮助文档. MATLAB. https://ww2.mathworks.cn/help/matlab/ref/linspace.html

    """
    assert isinstance(start, (int, float, numpy.ndarray)), 'param 1 should be integer or array'
    assert isinstance(end, (int, float, numpy.ndarray)), 'param 2 should be integer or array'
    assert isinstance(step, int), 'step should be integer'
    try:
        return numpy.linspace(start, end, step)
    except:
        raise
