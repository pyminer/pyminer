# from functools import cached_property
from typing import Any, Tuple, Dict, Union

from sliceable_generator import SliceableGenerator

SELECTOR_TYPE = Union[Tuple[Union[int, None], Union[int, None], Union[int, None]], int]


class BaseAdapter(object):
    """
    数据适配器的基类。

    数据适配器的意义在于，将逻辑与界面进行分离。
    工作空间中的每一个数据都将是一个数据适配器的实例。
    这就确保了所有的数据接口统一，可以方便地用于在界面中进行显示，
    而不必要在界面中加入逻辑进行判断。

    在这个类中采用了缓存属性的方案，使得一些计算耗时比较长的内容可以仅在需要的时候才进行计算。

    所有在 ``pyminer`` 中进行跨线程、跨进程、跨插件的数据交换功能都应当采用这个类的子类的实例进行传输。

    目前（2020/11/22）这个适配器仍是一个愿景，各个插件依旧各自为战，后面需要进行整合。

    请不要直接继承此类，请继承 ``UniversalAdapter`` 类，以获得更通用的功能，以及新实现的通用方法。

    """
    data: Any  # 请各个子适配器都定义这个data的类型，以便于IDE进行类型提示

    def __init__(self, data: Any):
        self.data = data

    # @cached_property
    def shape(self) -> Tuple[int, ...]:
        """数据的形状，与 ``numpy`` 保持一致。

        Returns:
            #. 对于没有维度的数据，比如整型、字符串，其尺寸就是一个空元组。
            #. 对于一个长度为 ``n`` 的一维列表，其尺寸就是 (n,)


        """
        raise NotImplementedError

    # @cached_property
    def dimensions(self):
        """数据的维度，事实上就是 ``shape`` 的长度的简单计算。"""
        return len(self.shape)

    # @cached_property
    def abstract(self) -> Dict[str, Any]:
        """
        摘要，用于实现元数据的快速传输
        """
        return {
            'shape': list(self.shape)
        }

    # @cached_property
    def serialized_data(self):
        """
        实现实际存储的数据的序列化。

        数据转变为字符串是通过 ``json.dumps`` 实现的，
        这个接口只需要保证返回值是 ``json.dumps`` 可以解析的内容即可，
        这个接口的具体实现不需要调用 ``json.dumps`` 。

        这个接口仅处理数据本身，不包括数据的信息等元数据。
        关于元数据的处理将在 ``dump`` 接口中进行描述。

        以下是一些序列化的示例：
        * 对于Numpy的矩阵可以序列化为[[1,2,3],[4,5,6]]。
        * 对于Pandas的表格可以序列化为[[1,2,3],['Tom','Jack','Jenny']]。
        * 对于Pandas等具有行列名的数据结构，其行列名定义在Abstract中，而非serialized_data中。

        Returns:
            嵌套的 ``dict`` ， ``list`` ，以及具体的 ``str`` ， ``int`` ， ``float`` 等数据。
            这应该是可以被 ``json.dumps`` 处理的类型。
        """
        raise NotImplementedError

    def dump(self) -> Dict[str, Any]:
        """
        将数据进行序列化。

        dump/load用于进行数据的交互，即打造类似于pickle的功能，不过可以序列化后通过http进行传输。

        目前考虑可能要在Server端添加type信息，因此可能需要保留关键字type。

        这个接口将处理包括具体的数据本身，以及元数据在内的所有数据。
        这个接口相当于实现了 ``pickle`` 的部分功能，可以确保整个 ``Adapter`` 在处理前后保持一致。

        TODO (panhaoyu) 如果后期采用高速传输方案，将修改这个接口，将value字段设置为内存地址的标识符。

        Returns:
            所有数据的序列化。
        """
        result = self.abstract.copy()  # 这里是浅复制，因为本函数仅修改第一层对象，因此没必要采用深复制
        result['data'] = self.serialized_data
        result['type'] = self.__class__.__name__  # 这个用于在反序列化时查找值
        return result

    @classmethod
    def load(cls, data: Dict[str, Any]) -> 'BaseAdapter':
        """
        将数据进行反序列化。

        dump/load用于进行数据的交互，即打造类似于pickle的功能，不过可以序列化后通过http进行传输。

        这个接口用于解析由 ``dump`` 函数存储的数据。

        Args:
            data: 由 ``dump`` 进行导出的数据。

        Returns:
            一个基于 ``dump`` 的导出数据读取得到的新的 ``Adapter`` 的实例。

        """
        raise NotImplementedError

    def get_array(self) -> Union[SliceableGenerator[Any], Any]:
        # TODO (panhaoyu) 这个类型事实上应该采用递归类型进行表示，不过我暂时不会用，就采用 ``Any`` 进行临时的表示了。
        """将数据整合为一个多维数组。

        这个方法主要用于切片等需要对数据进行操作的场景。

        这个数组采用了 ``SliceableGenerator`` ，以获得懒加载功能以及多维切片功能，相对于 ``list`` 性能较高，
        不过相对于 ``numpy.ndarray`` 的直接索引，还是慢了不少，特殊数据类型还是需要进行优化。

        Returns:
            由多层生成器构成的多维数组。
            这个数组的维度以及各维度的大小应当于 ``shape`` 保持一致。

        Notes:
            这个方法并不包含对数据的切片操作，而是返回了一个可以用于切片的生成器。

            这个方法并不一定会返回一个数组！
            如果需要保证可以拿到数组，可以使用 ``get_array_atleast_2d`` 。
        """
        raise NotImplementedError

    def get_array_atleast_2d(self) -> SliceableGenerator[Any]:
        """在工作空间的数据查看等场合，需要保证数据类型至少是一个二维数组，以用于表格显式。

        Returns:
            一个至少是二维的数组。

        Notes:
            ``get_array`` 和 ``get_array_atleast_2d`` 都是有应用场景的。
            ``get_array`` 是用于用户进行切片操作。
            ``get_array_atleast_2d`` 是用于进行表格显示的。

        """
        raise NotImplementedError

    def get_header_name(self, dimension=0) -> SliceableGenerator[str]:
        """
        获取数据在某个维度上的名称列表。

        即使是一维数组，也要同时定义dimension=0和dimension=1。

        Args:
            dimension: 需要查看的维度。

        Returns:
            该维度上所有表头的名称。

        """
        raise NotImplementedError


if __name__ == '__main__':
    from doctest import testmod

    testmod()
