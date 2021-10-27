"""
本模块用于判断一个数据的类型，并将其封装为合适的Adapter。
"""
from typing import List, Tuple, Dict

from numpy import ndarray
from pandas import DataFrame

from lib.workspace.data_adapter.array import ArrayAdapter
from lib.workspace.data_adapter.base import BaseAdapter
from lib.workspace.data_adapter.data_frame import DataFrameAdapter
from lib.workspace.data_adapter.universal import UniversalAdapter


class Detector:
    """
    类型识别器的作用在于，将任意的类型转换为一个合适的 ``DataAdapter`` 。

    在这里补充一个知识点：在 Python 中，一切变量都是对象。

    >>> class cls: pass
    >>> assert isinstance(cls, type)
    >>> assert isinstance(type, object)
    >>> assert isinstance(type, type)
    >>> assert issubclass(cls, object)
    >>> assert issubclass(cls, type) is False
    >>> assert issubclass(type, object)

    类是 ``type`` 的实例， ``type`` 是 ``object`` 的实例，同时 ``type`` 也是它本身的实例。

    类是 ``object`` 的子类，类不是 ``type`` 的子类， ``type`` 是 ``object`` 的子类。

    这个知识点对于本类的开发是必不可少的，因为本类的主要内容就是基于对象的类进行数据适配器的识别与分配。

    这个类主要包括了以下内容：

    #. 注册数据类型及其相对应的适配器的映射；
    #. 根据已注册的类型实现数据的自动包装；
    #. 定义的数据类型到数据适配器的映射
    """

    def __init__(self):

        # 这个变量用于进行类型与数据适配器的映射。
        # 其中的每一项都是一个列表，采用列表的原因，这保证了数据的有序性。
        # 这里预制了一个类型映射，即将任意类型都映射到 ``UniversalAdapter`` 。
        # 这里并没有预制其他类型映射，因为这些应该在对象初始化时完成。
        # 目前考虑在 ``DataManager`` 里对数据适配器进行初始化，因此内置的类型映射可以在初始化时完成。
        # 内置类型的初始化的定义，是在本类中完成的，这主要是由于内置的数据适配器定义在了本包中，
        # 出于解耦的考虑将他们定义在了 ``init`` 函数中。
        self.__data: List[Tuple[type, type]] = [(object, UniversalAdapter)]

        # 这个变量用于进行类型与数据适配器的快速查询。
        # 由于在程序运行过程中，经常发生变量的改变，因此采用O(1)的字典对映射进行缓存。
        self.__cached_data: Dict[type, type] = {}

    def register(self, detect_type: type, adapter_class: type, replace=False) -> None:
        """注册一个类型，以用于进行类型识别。

        由于PyMiner不可能涵盖所有的数据类型，因此需要插件自行实现其所需要的数据类型。

        Args:
            detect_type:
            adapter_class:
            replace: 如果已注册过该类型，是否覆盖注册。如不覆盖注册，则会报错。

        Raises:
            ValueError: 如果类型

        Notes:
            TODO (panhaoyu) 该方法尚不支持指定类型的插入顺序，后续应当进行调整。
            可选的方案是，支持传入一个 ``before`` 参数，支持一个列表的类型，使得新的类型在这些类型之前。

        """
        assert isinstance(detect_type, type)
        assert issubclass(adapter_class, BaseAdapter)

        # 判断类型是否已存在，如已存在且未指定 ``replace=True`` 则报错。
        if any(detect == detect_type for detect, adapter in self.__data) and not replace:
            raise ValueError('Register failed, data type already registered, user ``replace=True`` to overwrite.')

        # 由于指定了新的类型，类型的映射关系可能出现改变，需要重建映射，故清空已有的映射关系。
        self.__cached_data.clear()

        # 由于暂不支持指定类型的插入位置，先将其插入在第一位。
        self.__data.insert(0, (detect_type, adapter_class))

    def detect(self, data: any) -> BaseAdapter:
        """根据登录的类型自动识别

        Args:
            data: 任何数据

        Returns:
            识别数据得到的数据适配器

        """
        data_type = type(data)
        if data_type in self.__cached_data:
            return self.__cached_data[data_type](data)
        else:
            # 如果没有已缓存的数据适配器，则遍历所有数据，查询当前类型对应的数据适配器。
            available = [adapter_class for detect, adapter_class in self.__data if issubclass(data_type, detect)]
            # 由于 ``UniversalAdapter`` 的存在，这里一定是可以得到至少一个数据适配器的。
            self.__cached_data[data_type] = available[0]
            return available[0](data)

    def init_builtin_adapters(self):
        """建立内置数据类型的映射。

        Notes:
            TODO (panhaoyu) 实现多种数据类型的适配，至少要实现内置的 ``list`` 等数据类型以及 ``Pandas`` 的一系列数据类型的适配。
        """
        self.register(ndarray, ArrayAdapter)
        self.register(DataFrame, DataFrameAdapter)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
