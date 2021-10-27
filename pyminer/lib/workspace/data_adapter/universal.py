import pickle
# from functools import cached_property
from typing import Any, Dict, Tuple

from sliceable_generator import SliceableGenerator

from .base import BaseAdapter


class UniversalAdapter(BaseAdapter):
    """
    该适配器可以传递一切对象。

    TODO (panhaoyu) 不能传递动态类型
    """
    data: Any

    # @cached_property
    def shape(self) -> Tuple[int, ...]:
        """通用类型是没有维度的，这可以适用于一切类型，而对于存在维度的数据类型，应该独立地定义一个适配器。"""
        return ()

    # @cached_property
    def serialized_data(self):
        return pickle.dumps(self.data)

    @classmethod
    def load(cls, data: Dict[str, Any]) -> 'BaseAdapter':
        return cls(pickle.loads(data['data']))

    def get_array(self):
        if self.dimensions > 0:
            return SliceableGenerator(self.data, depth=self.dimensions)
        else:
            return self.data

    def get_array_atleast_2d(self):
        if self.dimensions > 1:
            return self.get_array()
        elif self.dimensions == 1:
            return SliceableGenerator((self.get_array() for _ in range(1)), depth=2)
        else:
            return SliceableGenerator(((self.get_array() for _ in range(1)) for __ in range(1)))

    def get_header_name(self, dimension=0):
        assert dimension in (0, 1), 'Dimension only supports `0` or `1`'
        return SliceableGenerator('0' for _ in range(1))
