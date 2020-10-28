from typing import Dict, Union

from pyminer2.workspace.datamanager.converter import Converter
from pyminer2.workspace.datamanager.dataset import DataSet
from pyminer2.workspace.datamanager.exceptions import NotFoundError, ConflictError
from pyminer2.workspace.datamanager.historyset import HistorySet
from pyminer2.workspace.datamanager.metadataset import MetaData, MetaDataSet
from pyminer2.workspace.datamanager.recyclebin import RecycleBin
from pyminer2.workspace.datamanager.varset import VarSet


class DataManager:
    def __init__(self):
        self.dataset = DataSet()
        self.varset = VarSet()
        self.metadataset = MetaDataSet()
        self.historyset = HistorySet()
        self.recyclebin = RecycleBin()
        self.converter = Converter(self)
        self.modification_callback_actions = []
        self.deletion_callback_actions = []
        self.add_callbacks()
        for typename in self.dataset:
            obj = self.dataset[typename]
            var = self.converter.convert_to_var(obj)
            self.set_var(typename, var, 'builtin')
            self.metadataset.synchronise_data(typename)

    # VarSet related

    def get_all_var(self) -> VarSet:
        return self.varset

    def get_all_public_var(self) -> Dict[str, Union[object, int, float]]:
        data = {
            k: v for k,
                     v in self.varset.items() if not getattr(
                v,
                'type',
                '') == 'Type'}
        return data

    def get_vars_of_types(self, types):
        data = {
            k: v for k, v in self.varset.items() if isinstance(v, types)
        }
        return data

    def get_var(self, key: str):
        if key not in self.varset:
            raise NotFoundError(f'{key} not found')
        return self.varset[key]

    def get_data_info(self, key: str) -> dict:
        if key not in self.metadataset:
            raise NotFoundError(f'{key} not found')
        return self.metadataset[key]

    def set_var_dict(self, variables: dict, provider='unknown', info_dict=None):
        # TODO (panhaoyu) 检查这里的逻辑是否正确
        # 是否需要在最后收集错误，然后再返回？程序报错后，是中止程序，还是允许程序继续运行？
        if info_dict is None:
            info_dict = {}
        err_list = []
        for key in variables:
            info = info_dict.get(key, {})
            try:
                self.set_var(key, variables[key], provider, **info)
            except ConflictError as e:
                err_list.append(e)
        if err_list:
            raise ConflictError('\n'.join([str(e) for e in err_list]))

    def set_var(self, key: str, value, provider='unknown', **info):
        """
        设置数据
        数据会产生一个回调，回调中的data_souurce信息就是这里的provider。
        比如ipython产生的provider，就是‘ipython’。这样可以防止数据收到自己造成的更新之后造成无限反复。
        :param key:
        :param value:
        :param provider:
        :param info:
        :return:
        """
        # it's recommended to give provider
        with self.metadataset.lock_data(key):
            old_var = self.varset.get(key, None)
            self.varset.set_var(key, value, provider)
            if old_var is not None:
                self.historyset.push(key, old_var)
            if key in self.metadataset:
                self.metadataset.modify_data(key, provider)
                self.metadataset.update(key, **info)
            else:
                meta_data = MetaData(provider, **info)
                self.metadataset.define_data(key, meta_data)

    def update_data_info(self, key: str, **info):
        with self.metadataset.lock_data(key):
            if key not in self.metadataset:
                raise NotFoundError(f'{key} not found')
            self.metadataset.update(key, **info)

    def delete_data(self, key: str, provider='unknown'):
        with self.metadataset.lock_data(key):
            if key not in self.varset:
                raise NotFoundError(f'{key} not found')
            self.recyclebin.discard(key, self.varset[key])
            self.varset.pop(key)
            self.metadataset.delete_data(key)

    def clear(self):
        for key in self.metadataset:
            self.delete_data(key)

    def get_recyclebin(self) -> list:
        return [r for r in self.recyclebin]

    def restore(self, index: int):
        key = self.recyclebin.get_varname(index)
        with self.metadataset.lock_data(key):
            key, var_to_restore = self.recyclebin.restore(
                index, self.varset.get(key, None))
            self.set_var(key, var_to_restore)
            self.metadataset.restore_data(key)

    def cancel(self, key):
        with self.metadataset.lock_data(key):
            if key not in self.historyset:
                raise NotFoundError(f'{key} has no history')
            variable = self.historyset.stepback(key, self.varset[key])
            self.varset.set_var(key, variable)

    def redo(self, key):
        with self.metadataset.lock_data(key):
            if key not in self.historyset:
                raise NotFoundError(f'{key} has no history')
            variable = self.historyset.stepforward(key)
            self.varset.set_var(key, variable)

    # DataSet related

    def read_data(self, key: str) -> dict:
        with self.metadataset.lock_data(key):
            if key not in self.metadataset or self.metadataset[key]['deleted']:
                raise NotFoundError(f'{key} not found')
            metadata = self.metadataset[key]
            if not metadata['synchronised']:
                data = self.converter.convert_to_data(
                    self.varset.get_var(key))
                self.dataset.synchronise(key, data)
                self.metadataset.synchronise_data(key)
            return self.dataset.read(key)

    def write_data(self, key: str, data: dict, provider='server'):
        with self.metadataset.lock_data(key):
            self.dataset.write(key, data)
            obj = self.dataset[key]
            var = self.converter.convert_to_var(obj)
            self.set_var(key, var, provider)
            self.metadataset.synchronise_data(key)

    def lock_data(self, key: str):
        self.metadataset.lock_data(key)

    def on_modification(self, modification_callback):
        self.modification_callback_actions.append(modification_callback)

    def on_deletion(self, deletion_callback):
        self.deletion_callback_actions.append(deletion_callback)

    def add_callbacks(self):
        """
        通过对varset添加装饰器以实现对变量的修改和删除的回调控制
        :return:
        """

        # TODO (panhaoyu) 如果需要回调函数，应该将回调函数作为参数写成register，可能会稍微优雅一点

        # TODO (panhaoyu) 回调函数的添加方式非常不优雅，可以考虑优化
        def modification_decorator(set_var):
            def wrapper(varname: str, variable, provider: str = 'unknown'):
                set_var(varname, variable)
                for callback in self.modification_callback_actions:
                    callback(varname, variable, provider)

            return wrapper

        self.varset.set_var = modification_decorator(self.varset.set_var)

        def deletion_decoration(delete_data):
            def wrapper(key: str, provider: str):
                delete_data(key)
                for callback in self.deletion_callback_actions:
                    callback(key, provider)

            return wrapper

        self.delete_data = deletion_decoration(self.delete_data)


data_manager = DataManager()


def main():
    # 前半段为datamanager的测试，已重写为测试用例
    import numpy as np

    datamanager = DataManager()

    def on_modification(varname: str, variable, data_source: str):
        print(f'detect modification: {varname} = {variable}')

    def on_deletion(varname: str):
        print(f'detect deletion: {varname}')

    datamanager.on_modification(on_modification)
    datamanager.on_deletion(on_deletion)

    datamanager.set_var('arr', np.array([[1, 2, 3], [3, 2, 1]]))
    print('add arr directly\n', datamanager.varset, '\n')

    mat = {'type': 'Matrix', 'value': [[1, 2, 3], [3, 2, 1]]}
    datamanager.write_data('mat', mat)
    print(
        'add mat from server\n',
        datamanager.varset,
        '\n',
        datamanager.dataset,
        '\n')

    print('metadataset\n', datamanager.metadataset, '\n')

    datamanager.set_var('mat', np.array([[1, 2, 4], [4, 2, 1]]), 'user')
    print('modify mat\n', datamanager.varset, '\n', datamanager.dataset, '\n')

    print('metadataset\n', datamanager.metadataset, '\n')

    datamanager.cancel('mat')
    print('cancel mat\n', datamanager.varset, '\n')

    datamanager.redo('mat')
    print('redo mat\n', datamanager.varset, '\n')

    datamanager.delete_data('arr')
    print(
        'cancel mat\n',
        datamanager.varset,
        '\nrecycle bin',
        datamanager.recyclebin,
        '\n')
    # noinspection PyBroadException
    try:
        var = datamanager.get_var('arr')
    except BaseException:
        print('cannot get arr\n')
    else:
        print('get var', var, '\n')
    # noinspection PyBroadException
    try:
        var = datamanager.read_data('arr')
    except BaseException:
        print('cannot read arr\n')
    else:
        print('read var', var, '\n')

    datamanager.set_var('arr', np.array([[1, 2, 5], [5, 2, 1]]))
    datamanager.restore(0)
    print(
        'cancel mat\n',
        datamanager.varset,
        '\nrecycle bin',
        datamanager.recyclebin,
        '\n')

    print('read arr', datamanager.read_data('arr'))
    print('get mat', datamanager.get_var('mat'))

    # TODO (panhaoyu) 以下是dataserver部分的测试，本次提交没有进行更新
    from pyminer2.workspace.dataserver.dataserver import DataServer

    def test(datamanager=datamanager):
        import requests
        import time
        time.sleep(5)

        r = requests.get('http://localhost:8783/read/arr')
        print(r.text)

        r = requests.post(
            'http://localhost:8783/write/',
            json={
                'dataname': 'mat',
                'data': mat,
                'provider': 'user'})
        print(datamanager.varset, datamanager.dataset)
        print(r.__dict__)

    dataserver = DataServer(datamanager, test)
    dataserver.start()


if __name__ == "__main__":
    main()
