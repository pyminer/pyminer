"""
该模块用于承载数据管理的功能，即工作空间。
"""
from ..data_adapter import BaseAdapter
from typing import Dict, Any, Tuple, List
from collections import OrderedDict


class DataManager(object):
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

    def __getitem__(self, key: str) -> BaseAdapter:
        """
        从工作空间中读取变量
        :param key: 变量名
        :return: 变量值，是Adapter，不是原始值
        """
        current, future = self.container[key]
        current or self.__raise_key_error(key)
        return current[-1]

    def __setitem__(self, key: str, value: BaseAdapter):
        """
        将变量写入工作空间
        :param key: 变量名
        :param value: 变量值，应该是一个Adapter
        :return:
        """
        assert isinstance(value, BaseAdapter)

        # 首先确保工作空间中有该变量的历史记录容器
        if key not in self.container:  # 如果工作空间中没有该变量
            if key not in self.recycle_bin:  # 回收站中也没有，新建该变量的历史记录
                self.container[key] = ([], [])
            else:  # 从回站中恢复
                self.container[key] = self.recycle_bin[key]
                del self.recycle_bin[key]

        # 处理历史记录相关内容
        current, future = self.container[key]
        if future:
            future.clear()
        current.append(value)
        if len(current) > 15:  # 对每个变量的最多保存的历史记录数量
            current.pop(0)

    def __delitem__(self, key: str):
        # TODO (panhaoyu) 这里实际应当进行当前工作空间的变量和回收站中的变量的合并，此处时间原因先采用直接替换的方式
        key in self.container or self.__raise_key_error(key)
        self.recycle_bin[key] = self.container[key]
        del self.container[key]

    def back(self, key: str) -> bool:
        """
        使得变量恢复前一个历史记录点。
        :param key: 变量名
        :return: 变量撤销是否成功
        """
        key in self.container or self.__raise_key_error(key)
        current, future = self.container[key]
        if len(current) < 2:
            return False
        future.insert(0, current.pop())
        return True

    def forward(self, key: str) -> bool:
        """
        使得变量前进一个历史记录点。
        :param key: 变量名
        :return: 变量重做是否成功
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
        :param key: 变量名
        :return:
        """
        key in self.recycle_bin or self.__raise_key_error(key, '回收站')
        self.container['c'] = self.recycle_bin[key]
        del self.recycle_bin[key]

    def __raise_key_error(self, key: str, position='工作空间'):
        raise KeyError(f'{position}未定义变量：{key}')

    def keys(self) -> List[str]:
        return list(self.container.keys())

    def values(self) -> List[BaseAdapter]:
        return [current[-1] for current, future in self.container.values()]

    def items(self) -> List[Tuple[str, BaseAdapter]]:
        return [(key, history[0][-1]) for key, history in self.container.items()]
