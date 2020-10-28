from functools import cached_property
from typing import List, Any, Tuple, Dict, Union

import numpy

from .base_structure import BaseAdapter, SELECTOR_TYPE


class ArrayAdapter(BaseAdapter):
    data: numpy.ndarray

    def __init__(self, data: numpy.ndarray):
        super(ArrayAdapter, self).__init__(data)

    @cached_property
    def shape(self) -> Tuple[int]:
        return self.data.shape

    @cached_property
    def serialized_data(self):
        return self.data.tolist()

    @classmethod
    def load(cls, data: Dict[str, Any]) -> 'BaseAdapter':
        data = numpy.array(data['data'])
        return cls(data)

    def get_matrix(self, *selector: SELECTOR_TYPE) -> List[List[Any]]:
        dimensions = len(self.data.shape)
        if dimensions == 1:
            # noinspection PyTypeChecker
            return [self.data.tolist()]
        elif dimensions == 2:
            # noinspection PyTypeChecker
            return self.data.tolist()
        else:
            assert len(selector) == dimensions, '多维数组的切片参数的数量必须与数组维度一致'
            parsed_selector = []
            range_selector_count = 0
            for index, slice_args in enumerate(selector):
                if isinstance(slice_args, int):  # 该维度直接指定某一个值
                    parsed_selector.append(slice_args)
                elif isinstance(slice_args, tuple) and len(slice_args) == 3:  # 该维度指定一个范围
                    range_selector_count += 1
                    start, stop, step = slice_args
                    start = 0 if start is None else start
                    stop = self.data.shape[index] if stop is None else stop
                    step = 1 if step is None else step
                    assert isinstance(start, int), f'第{index}个维度的start参数错误：需要None或有效自然数'
                    assert isinstance(stop, int), f'第{index}个维度的stop参数错误：需要None或有效自然数'
                    assert isinstance(step, int), f'第{index}个维度的step参数错误：需要None或有效自然数'
                    parsed_selector.append(slice(start, stop, step))
                else:
                    raise ValueError(f'第{index}个维度的参数错误：需要整数或三个元素的元组')
            assert range_selector_count == 2, '为显示为矩阵，范围参数必须有且只有两个'
            return self.data[tuple(parsed_selector)].tolist()

    def get_header_name(self, dimension=0) -> List[str]:
        dimensions = len(self.data.shape)
        if dimensions == 1 and dimension == 1:  # 一维数组的维度1需要独立定义
            return ['0']
        assert 0 <= dimension < dimensions, f'对于此数组，维度应在[0,{dimensions}]范围内'
        assert isinstance(dimension, int), '维度应当是整数'
        return [str(i) for i in range(self.shape[dimension])]
