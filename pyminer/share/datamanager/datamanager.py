import time
import warnings

MAX_STEPS = 15
import copy
from typing import Dict


class Data():
    '''
    这是一个数据对象，可以管理数据的历史。
    支持的对象类型应当是有限的，比如dataframe,ndarray等。
    目前使用的就是这个类。
    '''
    value = None
    info = {}

    def __init__(self, ini_value: object):
        self.info = {}
        self.set_data(ini_value)

    def set_data(self, value: object):
        '''
        添加数据。
        :param value:
        :return:
        '''
        self.value = value
        # self.update_info()

    def get_data(self, copy_val=True) -> object:
        '''
        获取数据的值，采用当前的指针。
        :param copy_val:
            如果为True(默认)，就返回复制后的对象。反之返回引用。当需要修改对象的时候，请保持True。
            特别的，不要使用类似如下的方式。这样会多次复制对象，从而导致不必要的开销：
                for i in range(10):
                    Data.get('a')[i]
                可以使用如下方案：
                for i in range(10):
                    Data.get('a',copy=False)[i]
                但还是推荐使用：
                a = Data.get('a')
                for i in range(10):
                    a[i]
        :return:object
        '''
        return self.value

    def update_info(self):  # 目前逻辑是写死了的。
        name = 'test_file'
        path = '../class.csv'
        create_time = '2017.9.1'  # self.info['create_time']
        update_time = '时间戳：' + str(time.time())
        row = '10'
        col = '10'
        remarks = ''
        file_size = '123'
        memory_usage = '123kb'
        info = ''
        self.set_info(name, path, create_time, update_time, row, col, remarks, file_size, memory_usage, info)

    def set_info(self, dataset_name: str, path: str, create_time: str,
                 update_time: str, row: str, col: str, remarks: str, file_size: str,
                 memory_usage: str, info=''):
        dataset_info = {"name": dataset_name,
                        "path": path,
                        "create_time": create_time,
                        "update_time": update_time,
                        "row": row,
                        "col": col,
                        "remarks": remarks,
                        "file_size": file_size,
                        "memory_usage": memory_usage,
                        "info": info}
        self.info = dataset_info


class Data_With_Undo_Func():
    '''
    这是一个数据对象，可以管理数据的历史。
    支持的对象类型应当是有限的，比如dataframe,ndarray等。
    目前用不上这个类，因为这个比较复杂。
    '''

    def __init__(self, ini_value: object):
        self.value_stack = []
        self.stack_pointer = 0  # 指向起始位置的指针。以下代码注释中简称‘指针’
        self.info = {}
        self.set_data(ini_value)

    def __len__(self):
        return len(self.value_stack)

    def get_latest(self, copy_val=True) -> object:
        if copy_val:
            return copy.copy(self.value_stack[-1])
        return self.value_stack[-1]

    def set_data(self, value: object):
        '''
        添加数据。
        :param value:
        :return:
        '''
        self.value_stack.append(value)
        while len(self.value_stack) > MAX_STEPS:
            self.value_stack.pop(0)
        self.stack_pointer = len(self) - 1
        # self.update_info()

    def get_data(self, copy_val=True) -> object:
        '''
        获取数据的值，采用当前的指针。
        :param copy_val:
            如果为True(默认)，就返回复制后的对象。反之返回引用。当需要修改对象的时候，请保持True。
            特别的，不要使用类似如下的方式。这样会多次复制对象，从而导致不必要的开销：
                for i in range(10):
                    Data.get('a')[i]
                可以使用如下方案：
                for i in range(10):
                    Data.get('a',copy=False)[i]
                但还是推荐使用：
                a = Data.get('a')
                for i in range(10):
                    a[i]
        :return:object
        '''
        index = self.stack_pointer
        if copy_val:
            return copy.copy(self.value_stack[index])
        return self.value_stack[index]

    def get_index(self) -> int:
        return self.stack_pointer

    def set_index(self, index: int):
        if 0 <= index < len(self.value_stack):
            self.stack_pointer = index

    def update_info(self):  # 目前逻辑是写死了的。
        name = 'test_file'
        path = '../class.csv'
        create_time = '2017.9.1'  # self.info['create_time']
        update_time = '时间戳：' + str(time.time())
        row = '10'
        col = '10'
        remarks = ''
        file_size = '123'
        memory_usage = '123kb'
        info = ''
        self.set_info(name, path, create_time, update_time, row, col, remarks, file_size, memory_usage, info)

    def set_info(self, dataset_name: str, path: str, create_time: str,
                 update_time: str, row: str, col: str, remarks: str, file_size: str,
                 memory_usage: str, info=''):

        dataset_info = {"name": dataset_name,
                        "path": path,
                        "create_time": create_time,
                        "update_time": update_time,
                        "row": row,
                        "col": col,
                        "remarks": remarks,
                        "file_size": file_size,
                        "memory_usage": memory_usage,
                        "info": info}
        self.info = dataset_info


class DataManager():
    '''
    以下举例均默认data_manager = DataManager()
    '''

    def __init__(self):
        self.vars: Dict[str, Data] = {}
        self.recycle_bin: Dict[str, Data] = {}
        self.current_data = None
        # self.all_data_sets_info: Dict[str, dict] = {}  # 管理数据集的信息

    @property
    def all_data_names(self) -> set:
        '''
        调用方式：data_manager.all_data_names
        可以代替__all_data_names
        Returns:

        '''
        return {k for k in self.vars.keys()}

    def get_info(self, name: str):
        '''

        Args:
            name: 变量的名称

        Returns:字典。返回变量的全部属性字典。比如get_info('class')['path'],就是返回名为‘class’的数据集中的‘path’属性。

        '''
        return self.vars[name].info

    def set_data(self, name: str, value: object) -> None:
        '''
        设置信息。
        比如说，set_data('a'),就是设置数据集a的值。
        Args:
            name:
            value:

        Returns:

        '''
        if name in self.vars.keys():
            self.vars[name].set_data(value)
        else:
            self.vars[name] = Data(value)

    def get_all_data_dic(self):
        '''
        获取所有数据，是一个名称对元素的字典。但是要注意，返回的值是一个Data对象，而不是变量的字典。
        Returns:

        '''
        return self.vars

    def get_data(self, name: str, copy_val: bool = False) -> object:
        '''
        获取名为name的data。如果copy_val是True，那么就将其设置为True之后再
        Args:
            name:
            copy_val:

        Returns:

        '''
        if name in self.vars.keys():
            return self.vars[name].get_data(copy_val=copy_val)
        else:
            warnings.warn("Variable \'%s\' isn\'t exist." % name)

    def get(self, name: str) -> object:
        '''
        等于get_data。
        Args:
            name:

        Returns:

        '''
        return self.get_data(name)

    def move_data_stack_pointer(self, name: str, step: int = 1):
        '''
        无效方法，暂时无用。等到引入撤销功能之后就用上了。
        Args:
            name:
            step:

        Returns:

        '''
        if name not in self.vars.keys():
            return
        var = self.vars[name]
        pos = var.stack_pointer + step
        if 0 <= pos < len(var):
            var.stack_pointer = pos
        elif pos < 0:
            var.stack_pointer = 0
            print('到达最初数据，不可再撤销！')
        elif pos >= len(var):
            var.stack_pointer = len(var) - 1
            print('到达最新数据，不可再重做！')

    def move_data_stack_pointer_to(self, name: str, pos: int = -1):
        '''
        暂时用不上的方法。
        Args:
            name:
            pos:

        Returns:

        '''
        if name not in self.vars.keys():
            return
        var = self.vars[name]
        if pos < 0:
            pos = len(var.value_stack) - pos

        if 0 <= pos < len(var):
            var.stack_pointer = pos
        elif pos < 0:
            var.stack_pointer = 0
            print('到达最初数据，不可再撤销！')
        elif pos >= len(var):
            var.stack_pointer = len(var) - 1
            print('到达最新数据，不可再重做！')

    def delete_data(self, name: str) -> None:
        '''删除数据，也就是移动到回收站。'''
        if name in self.vars.keys():
            self.recycle_bin[name] = self.vars[name]
            self.vars.pop(name)
        else:
            warnings.warn("Variable \'%s\' isn\'t exist." % name)

    def recover_data(self, name: str) -> None:
        '''从回收站中恢复数据'''
        if name in self.recycle_bin.keys():
            if name in self.vars.keys():
                # 如果恢复数据时，数仓中已有重名变量，将该变量移动至回收站。
                self.vars[name], self.recycle_bin[name] = self.recyble_bin[name], self.vars[name]
                warnings.warn("Variable \'%s\' exists and is moved to recycle bin." % name)
            else:
                self.vars[name] = self.recycle_bin[name]
                self.recycle_bin.pop(name)
        else:
            warnings.warn("Variable \'%s\' doesn\'t exist." % name)

    def set_info(self, dataset_name: str, path: str, create_time: str,
                 update_time: str, row: str, col: str, remarks: str, file_size: str,
                 memory_usage: str, info=''):
        '''设置信息'''

        self.vars[dataset_name].set_info(dataset_name, path=path, create_time=create_time, update_time=update_time,
                                         row=row, col=col, remarks=remarks, file_size=file_size,
                                         memory_usage=memory_usage,
                                         info=info)
