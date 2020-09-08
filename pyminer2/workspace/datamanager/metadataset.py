import time
import threading
import contextlib
from pyminer2.workspace.datamanager.exceptions import ConflictError, NotFoundError


class WouldBlockError(Exception):
    pass


class MetaData(dict):

    def __init__(self, provider, **info):
        super().__init__()
        self['provider'] = provider
        self['modified_by'] = [provider, ]
        self.update(info)
        self['synchronised'] = False
        self['deleted'] = False
        self['lock'] = threading.RLock()


class MetaDataSet(dict):

    def define_data(self, key: str, info: MetaData):
        if key in self:
            raise ConflictError(f'meta data {key} already exist')
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
            yield
        else:
            lock = self[key]['lock']
            if not lock.acquire(blocking=False):
                raise WouldBlockError(key)
            try:
                yield lock
            finally:
                lock.release()
