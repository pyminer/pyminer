from contextlib import contextmanager
from typing import Dict, Union, Any

from lib.comm.base import DataDesc
from lib.workspace.data_manager import data_manager as next_data_manager
from lib.workspace.signals import workspace_data_created, workspace_data_changed, workspace_data_deleted
from lib.workspace_old.datamanager.exceptions import NotFoundError


class DataManager:
    def __init__(self):
        self.next_data_manager = next_data_manager
        self.provider = 'unknown'
        self.__weakref_protector = []  # 用于避免弱引用的回调函数被销毁

    @contextmanager
    def set_provider(self, provider='unknown'):
        self.provider = provider
        yield
        self.provider = 'unknown'

    def get_all_var(self) -> Dict[str, Any]:
        return {k: v.data for k, v in self.next_data_manager.items()}

    def get_all_public_var(self) -> Dict[str, Union[object, int, float]]:
        return self.get_all_var()

    def get_vars_of_types(self, types):
        return {k: v.data for k, v in self.next_data_manager.items() if isinstance(v, types)}

    def get_var(self, key: str):
        if key not in self.next_data_manager.keys():
            raise NotFoundError(f'{key} not found')
        return self.next_data_manager[key].data

    def get_data_info(self, key: str) -> dict:
        if key not in self.next_data_manager.keys():
            raise NotFoundError(f'{key} not found')
        return self.next_data_manager[key].abstract

    def set_var_dict(self, variables: dict, provider='unknown', info_dict=None):
        with self.set_provider(provider):
            for k, v in variables.items():
                self.next_data_manager.set_raw_data(k, v)

    def set_var(self, key: str, value, provider='unknown', **info):
        assert isinstance(value, DataDesc), 'Variable name:%s value:%s is not instance of DataDesc!' % (key, value)
        with self.set_provider(provider):
            self.next_data_manager.set_raw_data(key, value)

    def delete_data(self, key: str, provider='unknown'):
        with self.set_provider(provider):
            del self.next_data_manager[key]

    def clear(self):
        for key in self.next_data_manager.keys():
            del self.next_data_manager[key]

    def on_modification(self, modification_callback):
        def changed(sender, key: str):
            value = self.next_data_manager[key]
            modification_callback(key, value.data, self.provider)

        self.__weakref_protector.append(changed)

        workspace_data_created.connect(changed)
        workspace_data_changed.connect(changed)

    def on_deletion(self, deletion_callback):
        def deleted(sender, key: str):
            deletion_callback(key, self.provider)

        self.__weakref_protector.append(deleted)
        workspace_data_deleted.connect(deleted)


data_manager = DataManager()
