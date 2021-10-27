"""
处理cloudpickle保存。
pyminer的文件保存格式为.pmd，加载也是.pmd
cloudpickle的协议始终选择默认即可。
"""
from typing import Union, List, Tuple, Iterable, Optional, Any, TYPE_CHECKING

import os
import cloudpickle

if TYPE_CHECKING:
    import pandas as pd
    import numpy as np


def isiterable(obj) -> bool:
    return hasattr(obj, '__iter__')


def save_variable_pmd(var_names: Union[List[str], Tuple[str], str], var_value: Union[object, Iterable[object]],
                      file_path: str, metadata: Union[dict, Iterable[dict]] = None) -> bool:
    """
    输入可迭代对象，将变量存入.pmd文件中。

    如果输入的var_names是一个字符串，那么就将var_values和metadata当成一个变量。
    如果输入的var_names是一个可迭代对象，那么就将var_vaues和metadata当成可迭代对象（必须可迭代！）

    :param var_names: 数据的名称（一个字符串或者字符串列表\元组）
    :param var_value: 数据的值（一个对象或者可迭代对象）
    :param metadata: 元数据（dict）
    :param file_path: 有效路径
    :return:
    """
    from widgets import iter_isinstance
    try:
        if isinstance(var_names, str):
            var_names = [var_names]
            var_value = [var_value]
            if metadata is not None:
                assert isinstance(metadata, dict)
                metadata = [metadata]
            else:
                metadata = [None]
        elif isinstance(var_names, (list, tuple)):
            if metadata is not None:
                assert isiterable(metadata)
                assert iter_isinstance(metadata, dict)
            else:
                metadata = [None] * len(var_names)
            pass
        else:
            raise TypeError('Type of var_names should be a string or iterable. However it is %s' % type(var_names))

        vars = {}
        for name, value, meta in zip(var_names, var_value, metadata):
            try:
                vars[name] = {'value': cloudpickle.dumps(value), 'metadata': {}}  # [TODO:目前无法pickle存储metadata.]
            except:
                import traceback
                traceback.print_exc()
                return
        with open(file_path, 'wb') as f:
            cloudpickle.dump(vars, f)
        return True

    except:
        import traceback
        traceback.print_exc()
    return False


def load_variable_pmd(file_path) -> Tuple[Optional[dict], Optional[dict]]:
    """
    从pmd文件中加载变量,以字典形式返回数据和元数据
    :param file_path:
    :return: data:dict,metadata:dict
    """
    try:
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                pmd_dic: dict = cloudpickle.load(f)
            vars = {}
            metadata = {}
            for k, item in pmd_dic.items():
                vars[k] = cloudpickle.loads(item['value'])
                metadata[k] = item['metadata']
            return vars, metadata
    except:
        import traceback
        traceback.print_exc()
    return None, None


def load_variable_pkl(file_path: str) -> Any:
    """
    加载pickle文件
    :param file_path:
    :return:
    """
    try:
        with open(file_path, 'rb') as f:
            return cloudpickle.load(f)
    except:
        import traceback
        traceback.print_exc()
    return None


def save_variable_pkl(variable, file_path: str, protocol=None) -> bool:
    """
    加载pickle文件
    :param file_path:
    :return:
    """
    try:
        with open(file_path, 'wb') as f:
            cloudpickle.dump(variable, f, protocol=protocol)
        return True
    except:
        import traceback
        traceback.print_exc()
    return False


def save_variable_table(variable: 'pd.DataFrame', file_path: str) -> bool:
    """
    保存表格为dataframe控件。
    :param variable:
    :param file_path:
    :return:
    """
    import pandas as pd
    try:
        if isinstance(variable, pd.DataFrame):
            if file_path.endswith('.csv'):
                variable.to_csv(file_path)
            elif file_path.endswith(('.xls', '.xlsx')):
                variable.to_excel(file_path,engine="openpyxl")
            else:
                raise Exception('invalid path %s,extension name unable to parse' % file_path)
            return True
    except:
        import traceback
        traceback.print_exc()
    return False


def save_variable_matrix(mat_variable: 'np.ndarray', file_path: str) -> bool:
    """
    存储Numpy类型。
    文件格式:.npy,.mat
    :param mat_variable:
    :param file_path:
    :return:
    """
    import numpy as np
    try:
        if file_path.endswith('.npy'):
            np.save(file_path, mat_variable)
        elif file_path.endswith('.mat'):
            from scipy import io
            io.savemat(file_path)
        else:
            raise ValueError('invalid path %s , extension name unable to parse' % file_path)
        return True
    except:
        import traceback
        traceback.print_exc()
    return False


if __name__ == '__main__':
    import time
    import os
    import numpy as np


    class TestIterator:
        def __init__(self, length: int = 3):
            self._length = length

        def __iter__(self):
            self.a = 0
            return self

        def __next__(self):
            x = np.ndarray([1, 2, 3])
            if self.a >= self._length:
                raise StopIteration
            self.a += 1
            return x

        def __len__(self):
            return self._length


    values = TestIterator(5)  # 调节此处值。都不会报错。会按照短的来操作

    root = os.path.dirname(__file__)
    file_path = os.path.join(root, 'testfiles', 'x.pkl')
    save_variable_pmd('a', [1, 2, 3, 4, 5], file_path)
    print(load_variable_pmd(file_path))
    save_variable_pmd(['a', 'b', 'c'], values, file_path)
    print(load_variable_pmd(file_path))
