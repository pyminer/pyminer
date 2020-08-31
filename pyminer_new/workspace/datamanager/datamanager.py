from dataset import DataSet
from varset import VarSet
from metadataset import MetaData, MetaDataSet
from historyset import HistorySet
from recyclebin import RecycleBin
from converter import Converter
from exceptions import ConflictError, NotFoundError


class DataManager():
    
    def __init__(self):
        self.dataset = DataSet()
        self.varset = VarSet()
        self.metadataset = MetaDataSet()
        self.historyset = HistorySet()
        self.recyclebin = RecycleBin()
        self.converter = Converter()
        for typename in self.dataset:
            obj = self.dataset[typename]
            var = self.converter.convert_to_var(obj)
            self.set_var(typename, var, 'builtin')
            self.metadataset.synchronise_data(typename)

    # VarSet related

    def get_all_var(self)->dict:
        return self.varset

    def get_var(self, varname:str):
        if varname not in self.varset:
            raise NotFoundError(f'{varname} not found')
        return self.varset[varname]

    def get_data_info(self, varname:str)->dict:
        if varname not in self.metadataset:
            raise NotFoundError(f'{varname} not found')
        return self.metadataset[varname]

    def set_var(self, varname:str, variable, provider='unknown', **info):
        # it's recommended to give provider
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

    def update_data_info(self, varname:str, **info):
        if varname not in self.metadataset:
            raise NotFoundError(f'{varname} not found')
        self.metadataset.update(varname, **info)

    def delete_data(self, varname:str):
        if varname not in self.varset:
            raise NotFoundError(f'{varname} not found')
        self.recyclebin.discard(varname, self.varset[varname])
        self.varset.pop(varname)
        self.metadataset.delete_data(varname)

    def get_recyclebin(self)->list:
        return [r for r in self.recyclebin]

    def restore(self, index:int):
        varname = self.recyclebin.get_varname(index)
        varname, var_to_restore = self.recyclebin.restore(index, self.varset.get(varname, None))
        self.set_var(varname, var_to_restore)
        self.metadataset.restore_data(varname)

    def cancel(self, varname):
        if varname not in self.historyset:
            raise NotFoundError(f'{varname} has no history')
        variable = self.historyset.stepback(varname, self.varset[varname])
        self.varset.set_var(varname, variable)

    def redo(self, varname):
        if varname not in self.historyset:
            raise NotFoundError(f'{varname} has no history')
        variable = self.historyset.stepforward(varname)
        self.varset.set_var(varname, variable)
        
    # DataSet related

    def read_data(self, varname:str) -> str:
        if varname not in self.metadataset or self.metadataset[varname]['deleted']:
            raise NotFoundError(f'{varname} not found')
        metadata = self.metadataset[varname]
        if metadata['synchronised']==False:
            data = self.converter.convert_to_data(self.varset.get_var(varname))
            self.dataset.synchronise(varname, data)
            self.metadataset.synchronise_data(varname)
        return self.dataset.read(varname)

    def write_data(self, varname:str, data:str, provider='server'):
        self.dataset.write(varname, data)
        obj = self.dataset[varname]
        var = self.converter.convert_to_var(obj)
        self.set_var(varname, var, provider)
        self.metadataset.synchronise_data(varname)

if __name__ == "__main__":
    import numpy as np
    import json

    datamanager = DataManager()

    datamanager.set_var('arr', np.array([[1,2,3],[3,2,1]]))
    print('add arr directly\n', datamanager.varset, '\n')

    mat = {'type': 'matrix', 'value': [[1,2,3],[3,2,1]]}
    datamanager.write_data('mat', json.dumps(mat))
    print('add mat from server\n', datamanager.varset, '\n', datamanager.dataset, '\n')

    print('metadataset\n', datamanager.metadataset, '\n')
    
    datamanager.set_var('mat', np.array([[1,2,4],[4,2,1]]), 'user')
    print('modify mat\n', datamanager.varset, '\n', datamanager.dataset, '\n')

    print('metadataset\n', datamanager.metadataset, '\n')

    datamanager.cancel('mat')
    print('cancel mat\n', datamanager.varset, '\n')

    datamanager.redo('mat')
    print('redo mat\n', datamanager.varset, '\n')

    datamanager.delete_data('arr')
    print('cancel mat\n', datamanager.varset, '\nrecycle bin', datamanager.recyclebin, '\n')

    try:
        var = datamanager.get_var('arr')
    except:
        print('cannot get arr\n')
    else:
        print('get var', var, '\n')

    try:
        var = datamanager.read_data('arr')
    except:
        print('cannot read arr\n')
    else:
        print('read var', var, '\n')

    datamanager.set_var('arr', np.array([[1,2,5],[5,2,1]]))
    datamanager.restore(0)
    print('cancel mat\n', datamanager.varset, '\nrecycle bin', datamanager.recyclebin, '\n')

    print('read arr', datamanager.read_data('arr'))
    print('get mat', datamanager.get_var('mat'))
