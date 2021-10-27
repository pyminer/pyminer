import contextlib
import threading
import time

from pyminer2.workspace_old.datamanager.exceptions import ConflictError, NotFoundError
from .exceptions import WouldBlockError


class MetaData(dict):
    # TODO (panhaoyu) 这里建议采用object加属性的方式进行操作，现在这种方式不支持代码提示
    def __init__(self, provider, **info):
        super().__init__()
        self['provider'] = provider
        self['modified_by'] = [provider, ]
        self.update(info)
        self['synchronised'] = False
        self['deleted'] = False
        self['lock'] = threading.RLock()


class MetaDataSet(dict):
    # TODO (panhaoyu) 既然所有的方法名都带有“data“，那么这个“data“可能就是冗余的。

    # 这两个函数仅仅用于添加代码提示
    def __getitem__(self, item: str) -> MetaData:
        return super(MetaDataSet, self).__getitem__(item)

    def __setitem__(self, key: str, value: MetaData):
        super(MetaDataSet, self).__setitem__(key, value)

    def define_data(self, key: str, info: MetaData):
        if key in self and not self[key]['deleted']:
            raise ConflictError(f'meta data {key} already exist')

        # TODO (panhaoyu) 数据类型的定义是否应统一放在MataData里面
        info['creation_time'] = time.time()
        info['modification_time'] = [info['creation_time'], ]
        self[key] = info

    def modify_data(self, key: str, modified_by: str):
        if key not in self:
            raise NotFoundError(f'no such data {key}')
        info = self[key]
        info['modification_time'].append(time.time())
        info['modified_by'].append(modified_by)
        info['synchronised'] = False
        info['deleted'] = False

    def delete_data(self, key: str):
        if key not in self or self[key]['deleted']:
            raise NotFoundError(f'no such data {key}')
        self[key]['deleted'] = True

    def restore_data(self, key: str):
        if key not in self:
            raise NotFoundError(f'no such data {key}')
        self[key]['deleted'] = False

    def synchronise_data(self, key: str):
        if key not in self or self[key]['deleted']:
            raise NotFoundError(f'no such data {key}')
        self[key]['synchronised'] = True

    def update(self, key: str, **info):
        if key not in self or self[key]['deleted']:
            raise NotFoundError(f'no such data {key}')
        self[key].update(info)

    @contextlib.contextmanager
    def lock_data(self, key: str):
        if key not in self or self[key]['deleted']:
            # TODO (panhaoyu) 对于不存在的变量，需要明确报错，而不是继续运行
            yield
        else:
            lock = self[key]['lock']
            if not lock.acquire(blocking=False):
                raise WouldBlockError(key)
            try:
                yield lock
            finally:
                lock.release()
