from typing import List, Any, Dict, Tuple, Union

from .base_structure import BaseAdapter, SELECTOR_TYPE
from functools import cached_property
import pickle


class UniversalAdapter(BaseAdapter):
    """
    该适配器可以传递一切对象。
    # TODO (panhaoyu) 不能传递动态类型
    """
    data: Any

    @cached_property
    def shape(self) -> Tuple[int]:
        return 1,

    @cached_property
    def serialized_data(self):
        return pickle.dumps(self.data)

    @classmethod
    def load(cls, data: Dict[str, Any]) -> 'BaseAdapter':
        return cls(pickle.loads(data['data']))

    def get_matrix(self, *selector: SELECTOR_TYPE) -> List[List[Any]]:
        return [[repr(self.data)]]

    def get_header_name(self, dimension=0) -> List[str]:
        assert dimension in (0, 1), '维度只能是0和1'
        return ['1']
