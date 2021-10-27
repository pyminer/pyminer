"""
这个模块是对于 ``np.ndarray`` 进行的封装，也是以此为例探索如何进行数据的封装。
"""

# from functools import cached_property
from typing import Any, Tuple, Dict

from pandas import DataFrame
from sliceable_generator import SliceableGenerator

from . import ArrayAdapter


class DataFrameAdapter(ArrayAdapter):
    data: DataFrame

    # @cached_property
    def shape(self) -> Tuple[int, int]:
        """获取表格的形状，必为一个二维数组"""
        return self.data.shape

    # @cached_property
    def serialized_data(self):
        return self.data.to_dict()

    @classmethod
    def load(cls, data: Dict[str, Any]) -> 'DataFrameAdapter':
        return cls(DataFrame.from_dict(data['data']))

    def get_array(self):
        return SliceableGenerator(self.data.values, depth=2)

    def get_array_atleast_2d(self):
        return self.get_array()

    def get_header_name(self, dimension=0):
        assert dimension in (0, 1)
        if dimension == 0:
            return SliceableGenerator(str(i) for i in self.data.index.to_list())
        else:
            return SliceableGenerator(str(i) for i in self.data.columns.to_list())
