"""
这个模块是对于 ``np.ndarray`` 进行的封装，也是以此为例探索如何进行数据的封装。
"""

# from functools import cached_property
from typing import Any, Tuple, Dict

import numpy
from sliceable_generator import SliceableGenerator

from .universal import UniversalAdapter


class ArrayAdapter(UniversalAdapter):
    data: numpy.ndarray

    # @cached_property
    def shape(self) -> Tuple[int, ...]:
        """
        获取矩阵的形状。

        矩阵的形状，或者说大小，就是单纯的 ``ndarray.shape`` 。

        Returns:
            矩阵的形状
        """
        return self.data.shape

    # @cached_property
    def serialized_data(self):
        """
        将数据进行序列化。

        对于 ``ndarray`` ， ``numpy`` 原生的 ``ndarray.tolist()`` 已经可以完美地实现这个功能，没必要进行额外的工作。

        Returns:
            序列化后的数据，对于 ``ndarray`` 就直接调用了 ``ndarray.tolist()`` 函数。
        """
        return self.data.tolist()

    @classmethod
    def load(cls, data: Dict[str, Any]) -> 'ArrayAdapter':
        data = numpy.array(data['data'])
        return cls(data)

    def get_header_name(self, dimension=0):
        """
        对于矩阵而言，其行列名就是简单的数字。

        不同于 ``DataFrame`` ， ``array`` 是没有行列名的。
        此处仅作为占位，返回从0开始的数字列表。

        由于 ``python`` 中采用0位置作为数组的第一位，此处采纳相同的用法，采用0作为起点。

        Args:
            dimension: 行列名的维度，这个参数决定了返回值的长度。

        Returns:
            某个维度下的表头的列表。

        """
        dimensions = len(self.data.shape)
        if dimensions == 1 and dimension == 1:  # 一维数组的维度1需要独立定义
            return ('0' for _ in range(1))
        assert 0 <= dimension < dimensions, f'对于此数组，维度应在[0,{dimensions}]范围内'
        assert isinstance(dimension, int), '维度应当是整数'
        return SliceableGenerator(str(i) for i in range(self.shape[dimension]))
