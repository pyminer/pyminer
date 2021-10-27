import sys
from typing import Any


class DataDesc():
    """
    数据描述类。
    """
    threshold_pandas = 10 * 1024 * 1024  # 阈值限制10MB
    threshold_numpy = 10 * 1024 * 1024  # 阈值限制10MB
    max_len = 1000
    max_pandas_rows = 10000
    max_str_len = 100000

    def __init__(self, data: Any):
        self.cls = data.__class__
        self.type = get_data_type(data)
        self.size = get_size(data)
        repr_value = get_repr(data)
        self.repr_value = repr_value if len(repr_value) < 1000 else repr_value[:1000]
        self.big = is_big_variable(data)

        assert isinstance(self.big, bool), repr(self.big) + '  ' + str(type(self.big)) + '  ' + str(data) + '  ' + str(
            type(data))

    def __repr__(self):
        return 'DataDesc:{type} {repr_value}'.format(type=self.type, repr_value=self.repr_value)


class NoPreviewError(Exception):
    def __init__(self, desciption: str):
        super(NoPreviewError, self).__init__(desciption)


def is_big_variable(var):
    """
    判断是否为大型变量。
    对于较大的变量，需要采用预览模式。
    Args:
        var:

    Returns:

    """
    if isinstance(var, (int, bool, float)):
        return sys.getsizeof(var) > DataDesc.threshold_pandas
    elif isinstance(var, str):
        return len(var) > DataDesc.max_str_len
    elif isinstance(var, dict):
        return len(list(var.keys())) > DataDesc.max_len
    elif isinstance(var, (list, tuple)):
        return len(var) > DataDesc.max_len

    import pandas as pd
    import numpy as np
    if isinstance(var, (pd.DataFrame, pd.Series)):
        if isinstance(var, pd.DataFrame):
            return int(var.memory_usage().sum()) - DataDesc.threshold_pandas > 0
        else:
            return var.memory_usage() - DataDesc.threshold_pandas > 0
    elif isinstance(var, np.ndarray):
        return var.nbytes > DataDesc.threshold_numpy

    else:
        return False


def get_size(data: Any):
    """
    获取数据的尺寸。
    有‘shape’这一属性的，size就等于data.shape
    有‘__len__’这个属性的，返回len(data)
    否则返回1.
    Args:
        data:

    Returns:

    """
    size = 1
    if hasattr(data, 'shape'):
        size = data.shape
    elif hasattr(data, '__len__'):
        try:
            size = len(data)
        except:
            pass
    return size


def get_data_type(data: Any):
    data_type = str(type(data)).replace('class', '').replace(' ', '').replace('\'', '').replace('<',
                                                                                                '').replace('>', '')
    if data_type == 'pandas.core.frame.DataFrame':
        data_type = 'DataFrame'
    elif data_type == 'pandas.core.series.Series':
        data_type = 'Series'
    return data_type


def get_repr(data: Any):
    if isinstance(data, (list, tuple, str)):
        if len(data) > 1000:
            return repr(data[:1000])
    return repr(data)
