"""
该模块用于承载数据管理的功能，即工作空间。

``DataManager`` 类，其实例就是工作空间，提供了包括添加变量、删除变量、历史记录回溯、历史记录访问量等内容。

该模块在设计时考虑了历史记录功能，不过该功能是否有必要，还有待商榷。

该模块的操作对象为 ``DataAdapter``。
将数据外面包上一层可以确保其元数据的识别等便利性。
关于 ``DataAdapter`` 的详细内容请参见相关文档。

"""
from collections import OrderedDict
from typing import Dict, Tuple, List, Any

from lib.workspace.data_adapter import BaseAdapter
from lib.workspace.data_adapter import Detector
from .signals import workspace_data_created, workspace_data_deleted, workspace_data_changed


class DataManager(object):
    """
    数据管理类。

    应当注意的时，数据管理的对象，是 ``DataAdapter`` 而不是原生的数据。

    如果需要写入一个原生数据，可以采用 ``set_raw_data`` 方法。

    值得一提的是，最初的设想，通过 ``__setitem__`` 写入原生数据，然后通过 ``__getitem__`` 读出数据适配器。
    但是这样相当于与字典的功能发生了较大的差异，一个 python 用户的习惯应该是写入什么就取出什么，这不符合 python 用户的习惯。
    因此，采用了一个独立的方法 ``set_raw_data`` 用于写入原生数据并自动进行识别。
    """

    def __init__(self):
        # TODO 将历史记录的上限和回收站的上限作为对象初始化的参数进行传值

        # Container数据结构中管理器的主要内容。
        # 其键为变量名，值为两个列表构成的元组，共同用来表示历史记录。
        # 变量的历史记录和大多数程序一致，都是采用单线式的历史记录管理策略，如下所示：
        #     当前记录：[1,2,3,4,5,6,7],[]
        #     撤销一次：[1,2,3,4,5,6],[7]
        #     撤销一次：[1,2,3,4,5],[6,7]
        #     重做一次：[1,2,3,4,5,6],[7]
        #     写入一次：[1,2,3,4,5,6,8],[] # 写入时删除重做列表
        self.container: Dict[str, Tuple[List[BaseAdapter], List[BaseAdapter]]] = dict()

        # RecycleBin用于存储用户明确删除的变量，其基本工作流程的伪代码如下所示：
        #     当前空间：container={a,b,c},       recycle_bin={}
        #     删除a:   container={b,c},         recycle_bin={a}
        #     删除b:   container={c},           recycle_bin={a,b}
        #     恢复a:   container={a,c},         recycle_bin={b}
        self.recycle_bin = OrderedDict()

        # 数据适配器自动识别类
        self.detector = Detector()
        self.detector.init_builtin_adapters()

    def __getitem__(self, key: str) -> BaseAdapter:
        """
        从工作空间读取变量。

        Args:
            key: 变量名

        Returns:
            BaseAdapter: 变量值的Adapter，不是原始值

        """
        current, future = self.container[key]
        current or self.__raise_key_error(key)
        return current[-1]

    def __setitem__(self, key: str, value: BaseAdapter):
        """
        将变量写入工作空间

        Args:
            key: 变量名
            value: 变量值，应该是 ``BaseAdapter`` 的子类。
        """
        created = False  # 用于记录本次操作是新建了一个变量还是修改了一个变量
        assert isinstance(value, BaseAdapter)

        # 首先确保工作空间中有该变量的历史记录容器
        if key not in self.container:  # 如果工作空间中没有该变量
            created = True
            if key not in self.recycle_bin:  # 回收站中也没有，新建该变量的历史记录
                self.container[key] = ([], [])
            else:  # 从回站中恢复
                self.container[key] = self.recycle_bin[key]
                del self.recycle_bin[key]

        # 处理历史记录相关内容
        current, future = self.container[key]
        if future:
            future.clear()
        if not current:
            created = True
        current.append(value)
        if len(current) > 15:  # 对每个变量的最多保存的历史记录数量
            current.pop(0)
        if created:
            workspace_data_created.send(self, key=key)
        else:
            workspace_data_changed.send(self, key=key)

    def __delitem__(self, key: str):
        """
        在工作空间中删去一个变量。

        Args:
            key: 需要删去的变量名。
        """
        # TODO (panhaoyu) 这里实际应当进行当前工作空间的变量和回收站中的变量的合并，此处时间原因先采用直接替换的方式
        key in self.container or self.__raise_key_error(key)
        self.recycle_bin[key] = self.container[key]
        del self.container[key]
        workspace_data_deleted.send(self, key=key)

    def __contains__(self, item: str):
        """检查工作空间中是否已存在某个变量"""
        return item in self.container

    def __iter__(self):
        yield from self.container

    def set_raw_data(self, key: str, value: Any):
        """将一个原生变量写入数据管理器。

        Args:
            key: 变量名。
            value: 原生变量。
        """
        self[key] = self.detector.detect(value)

    def back(self, key: str) -> bool:
        """
        将变量撤回到前一个历史记录点。

        Args:
            key: 变量名

        Returns:
            bool: 变量是否撤销成功

        """
        key in self.container or self.__raise_key_error(key)
        current, future = self.container[key]
        if len(current) < 2:
            return False
        future.insert(0, current.pop())
        return True

    def forward(self, key: str) -> bool:
        """
        重做变量，即使得变量前进一个历史记录点。

        Args:
            key: 变量名

        Returns:
            变量是否重做成功
        """
        key in self.container or self.__raise_key_error(key)
        current, future = self.container[key]
        if not future:
            return False
        current.append(future.pop(0))
        if len(current) > 15:
            current.pop(0)
        return True

    def restore_from_recycle_bin(self, key: str):
        """
        从回收站中恢复一个变量。

        这将覆盖工作空间中的同名变量！需要弹窗警告！
        这个方法的名字很长，就是为了防止与“从历史记录中前移一位”功能相混淆。

        Args:
            key: 变量名
        """
        key in self.recycle_bin or self.__raise_key_error(key, '回收站')
        self.container[key] = self.recycle_bin[key]
        workspace_data_created.send(key=key)
        del self.recycle_bin[key]

    def __raise_key_error(self, key: str, position='工作空间'):
        raise KeyError(f'{position}未定义变量：{key}')

    def keys(self) -> List[str]:
        """
        将工作空间内的名字作为一个列表返回。

        每次都返回一个新列表。

        Returns:
            变量名的列表。
        """
        return list(self.container.keys())

    def values(self) -> List[BaseAdapter]:
        """
        将工作空间内的值作为一个列表返回。

        每次都返回一个新列表。
        Returns:
            变量值的列表。
        """
        return [current[-1] for current, future in self.container.values()]

    def items(self) -> List[Tuple[str, BaseAdapter]]:
        """
        将工作空间的键值对作为一个列表返回。

        每次都返回一个新列表。

        Returns:
            工作空间的数据的键值对
        """
        return [(key, history[0][-1]) for key, history in self.container.items()]


# 请不要直接使用此变量！
# 目前已知的用法仅有两处，一个是在 workspace_old ，一个是在 extension_lib 。
data_manager = DataManager()
