from typing import Any, Tuple, List, Dict, Union
from functools import cached_property

SELECTOR_TYPE = Union[Tuple[Union[int, None], Union[int, None], Union[int, None]], int]


class BaseAdapter(object):
    """
    数据适配器的基类。
    定义了多个缓存属性，仅在需要时才进行计算。
    """
    data: Any  # 请各个子适配器都定义这个data的类型，以便于IDE进行类型提示

    def __init__(self, data: Any):
        self.data = data

    @cached_property
    def shape(self) -> Tuple[int]:
        raise NotImplementedError

    @cached_property
    def abstract(self) -> Dict[str, Any]:
        """
        摘要，用于实现元数据的快速传输
        :return:
        """
        return {
            'shape': list(self.shape)
        }

    @cached_property
    def serialized_data(self):
        """
        实现实际存储的数据的序列化。
        对于Numpy的矩阵可以序列化为[[1,2,3],[4,5,6]]。
        对于Pandas的表格可以序列化为[[1,2,3],['Tom','Jack','Jenny']]。
        对于Pandas等具有行列名的数据结构，其行列名定义在Abstract中，而非serialized_data中。
        :return:
        """
        raise NotImplementedError

    def dump(self) -> Dict[str, Any]:
        """
        将所有数据都进行序列化。
        dump/load用于进行数据的交互，即打造类似于pickle的功能，不过可以序列化后通过http进行传输。
        目前考虑可能要在Server端添加type信息，因此可能需要保留关键字type。
        TODO (panhaoyu) 如果后期采用高速传输方案，将修改这个接口，将value字段设置为内存地址的标识符。
        :return:
        """
        result = self.abstract.copy()  # 这里是浅复制，因为本函数仅修改第一层对象，因此没必要采用深复制
        result['data'] = self.serialized_data
        result['type'] = self.__class__.__name__  # 这个用于在反序列化时查找值
        return result

    @classmethod
    def load(cls, data: Dict[str, Any]) -> 'BaseAdapter':
        """
        从可以序列化的数据中恢复数据。
        :param data: 包含所有的数据的信息，是一个大字典。
        :return: 实例化的对象
        """
        raise NotImplementedError

    def get_matrix(self, *selector: SELECTOR_TYPE) -> List[List[Any]]:
        """
        将任意数据整合成两维数据以进行显示。
        TODO (panhaoyu) 这个接口是否如此定义还需要讨论。
        目前我对于多维数组的显示的构想是，可以通过指定数据的某些维度而单独显示这个维度。
        对于一维数组和二维数组，row_index和col_index不起作用。
        对于高维数组，需要明确指出需要索引哪两个维度才能获取到数据。
        一个示例的用法是，对于6维数组，shape为(4,5,6,7,8,9)，可以使用如下方法：
            adapter.get_matrix(0,3,4,(2,6,1),(3,12,2),5,2)
        这表示对该数组进行如下操作：
            array[0,3,4,2:6:1,3:12:2,5,2]
        这对于array而言是很平常的，不过对于张量等并没有定义这些过滤过能的数据结构是比较有用的。（虽然张量八成也要采用numpy实现）
        :param selector: 分别指定各个维度的索引范围，三个值分别是start,stop,step，如果只指定了一个整数则为在该维度选定一行
        :return:
        """
        raise NotImplementedError

    def get_header_name(self, dimension=0) -> List[str]:
        """
        获取数据在某个维度上的名称列表。
        即使是一维数组，也要同时定义dimension=0和dimension=1。
        TODO (panhaoyu) 这个接口是否如此定义还需要讨论。
        :param dimension: 需要查看的维度
        :return: 该维度上所有表头的名称
        """
        raise NotImplementedError
