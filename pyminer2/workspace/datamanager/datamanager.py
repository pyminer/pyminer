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
        for typename in self.dataset:
            obj = self.dataset[typename]
            var = self.converter.convert_to_var(obj)
            self.set_var(typename, var, 'builtin')
            self.metadataset.synchronise_data(typename)
        self.add_callbacks()

    # VarSet related

    def get_all_var(self) -> dict:
        return self.varset

    def get_var(self, varname: str):
        if varname not in self.varset:
            raise NotFoundError(f'{varname} not found')
        return self.varset[varname]

    def get_data_info(self, varname: str) -> dict:
        if varname not in self.metadataset:
            raise NotFoundError(f'{varname} not found')
        return self.metadataset[varname]

    def set_var_dict(self, variables:dict, provider='unknown', info_dict:dict={}):
        err_list = []
        for varname in variables:
            info = info_dict.get(varname, {})
            try:
                self.set_var(varname, variables[varname], provider, **info)
            except ConflictError as e:
                err_list.append(e)
                pass
        if err_list:
            raise ConflictError('\n'.join([str(e) for e in err_list]))

    def set_var(self, varname: str, variable, provider='unknown', **info):
        # it's recommended to give provider
        with self.metadataset.lock_data(varname):
            old_var = self.varset.get(varname, None)
            self.varset.set_var(varname, variable)
            if old_var is not None:
                self.historyset.push(varname, old_var)
            if varname in self.metadataset:
                self.metadataset.modify_data(varname, provider)
                self.metadataset.update(varname, **info)
            else:
                meta_data = MetaData(provider, **info)
                self.metadataset.define_data(varname, meta_data)

    def update_data_info(self, varname: str, **info):
        with self.metadataset.lock_data(varname):
            if varname not in self.metadataset:
                raise NotFoundError(f'{varname} not found')
            self.metadataset.update(varname, **info)

    def delete_data(self, varname: str):
        with self.metadataset.lock_data(varname):
            if varname not in self.varset:
                raise NotFoundError(f'{varname} not found')
            self.recyclebin.discard(varname, self.varset[varname])
            self.varset.pop(varname)
            self.metadataset.delete_data(varname)

    def get_recyclebin(self) -> list:
        return [r for r in self.recyclebin]

    def restore(self, index: int):
        varname = self.recyclebin.get_varname(index)
        with self.metadataset.lock_data(varname):
            varname, var_to_restore = self.recyclebin.restore(
                index, self.varset.get(varname, None))
            self.set_var(varname, var_to_restore)
            self.metadataset.restore_data(varname)

    def cancel(self, varname):
        with self.metadataset.lock_data(varname):
            if varname not in self.historyset:
                raise NotFoundError(f'{varname} has no history')
            variable = self.historyset.stepback(varname, self.varset[varname])
            self.varset.set_var(varname, variable)

    def redo(self, varname):
        with self.metadataset.lock_data(varname):
            if varname not in self.historyset:
                raise NotFoundError(f'{varname} has no history')
            variable = self.historyset.stepforward(varname)
            self.varset.set_var(varname, variable)

    # DataSet related

    def read_data(self, varname: str) -> dict:
        with self.metadataset.lock_data(varname):
            if varname not in self.metadataset or self.metadataset[varname]['deleted']:
                raise NotFoundError(f'{varname} not found')
            metadata = self.metadataset[varname]
            if not metadata['synchronised']:
                data = self.converter.convert_to_data(
                    self.varset.get_var(varname))
                self.dataset.synchronise(varname, data)
                self.metadataset.synchronise_data(varname)
            return self.dataset.read(varname)

    def write_data(self, varname: str, data: dict, provider='server'):
        with self.metadataset.lock_data(varname):
            self.dataset.write(varname, data)
            obj = self.dataset[varname]
            var = self.converter.convert_to_var(obj)
            self.set_var(varname, var, provider)
            self.metadataset.synchronise_data(varname)

    def lock_data(self, varname: str):
        return self.metadataset.lock_data(varname)

    def on_modification(self, modification_callback):
        self.modification_callback_actions.append(modification_callback)

    def on_deletion(self, deletion_callback):
        self.deletion_callback_actions.append(deletion_callback)

    def add_callbacks(self):

        def modication_decoration(set_var):
            def wrapper(varname: str, variable):
                set_var(varname, variable)
                for callback in self.modification_callback_actions:
                    callback(varname, variable)

            return wrapper

        self.varset.set_var = modication_decoration(self.varset.set_var)

        def deletion_decoration(delete_data):
            def wrapper(varname: str):
                delete_data(varname)
                for callback in self.deletion_callback_actions:
                    callback(varname)

            return wrapper

        self.delete_data = deletion_decoration(self.delete_data)


data_manager = DataManager()


def main():
    import numpy as np

    datamanager = DataManager()

    def on_modification(varname: str, variable):
        print(f'detect modification: {varname} = {variable}')

    def on_deletion(varname: str):
        print(f'detect deletion: {varname}')

    datamanager.on_modification(on_modification)
    datamanager.on_deletion(on_deletion)

    datamanager.set_var('arr', np.array([[1, 2, 3], [3, 2, 1]]))
    print('add arr directly\n', datamanager.varset, '\n')

    mat = {'type': 'matrix', 'value': [[1, 2, 3], [3, 2, 1]]}
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
