# -*- coding: utf-8 -*-
from typing import List
import lib.comm
from lib.comm.base import shm_allowed


def get_var(var_name: str, preview=False) -> object:
    """
    从工作空间获取一个变量。

    Parameters
    -------------
    var_name: str
        变量名
    preview :bool
        是否返回预览格式。使用预览格式的时候，通常数据传输量不会太大。因此可以使用较为简单的方式进行预览。
        当其为False的时候，数据传输使用共享内存，传输全部。
        为True的时候，数据传输使用网络，对于较大的数据只传输预览。
        如果预览时数据过大，则会传回错误。
    Returns
    --------
    工作空间中该变量的值。

    Raises
    ---------
    ConnectionRefusedError
        无法连接工作空间，可能是因为PyMiner未启动。
        如果发生，可能会出现如下错误：
        `ConnectionRefusedError: Cannot connect to workspace. Please confirm that PyMiner has been started!`
    ValueError
        工作空间中不存在此变量。
    Examples
    ---------
    见set_var函数

    """

    try:
        if preview or (not shm_allowed()):
            if preview:
                var = lib.comm.get_vars([var_name], preview=True).get(var_name)
            else:
                var = lib.comm.get_vars([var_name], preview=False).get(var_name)
            return var
        else:
            return lib.comm.shm_get_vars([var_name]).get(var_name)
    except ConnectionRefusedError:
        raise ConnectionRefusedError('Cannot connect to workspace. Please confirm that PyMiner has been started!')


def get_vars(var_names: List) -> object:
    try:
        if not shm_allowed():
            return lib.comm.get_vars(var_names, preview=False)
        else:
            return lib.comm.shm_get_vars(var_names)
    except ConnectionRefusedError:
        raise ConnectionRefusedError('Cannot connect to workspace. Please confirm that PyMiner has been started!')


def set_var(var_name: str, var: object, provider: str = 'external') -> None:
    """
    对工作空间加入一个变量，或者修改工作空间已有变量。

    Parameters
    -------------
    var_name: str
    变量名
    var:object
    变量值
    provider:str='external'
    提供者标签。
    一般默认即可。如有需要可以改成其他值

    Returns
    --------
    None

    Raises
    ---------
    ConnectionRefusedError
        无法连接工作空间，可能是因为PyMiner未启动。
        如果发生，可能会出现如下错误：
        `ConnectionRefusedError: Cannot connect to workspace. Please confirm that PyMiner has been started!`

    Notes
    ---------
        如果在Ipython中运行，则无需使用这个函数来修改工作空间的变量。这是因为所有在Ipython中产生和修改的变量，都会被自动传送到工作空间，无需
        人为添加代码。
        当然，在IPython中调用了这个函数也不会出现错误，只是会降低效率。

    Examples
    ---------

    >>> from core.algorithms import *
    >>> set_var('x',[1,2,3,4,5])
    >>> get_var('x')
    [1,2,3,4,5]
    >>> get_var('y') # 如果y在工作空间不存在
    ValueError: variable 'y' not found!

    """

    try:
        try:
            get_ipython().neglect_post_run = True  # 检测是否在Ipython中，如果是，就将这个标志位置为True防止重复更改。
        except NameError:
            pass
        if not shm_allowed():
            lib.comm.set_vars({var_name: var})
        else:
            lib.comm.shm_set_vars({var_name: var})
    except ConnectionRefusedError:
        raise ConnectionRefusedError('Cannot connect to workspace. Please confirm that PyMiner has been started!')


def get_var_names(type_filter: str = '') -> List[str]:
    """
    从工作空间按照指定类型获取所有的变量名。

    Parameters
    -------------
    type_filter: str
        变量类型的字符表示
        目前支持四种：string,table,array和numeric。使用table可以过滤出所有的二维array\pd.DataFrame
        默认值为‘’也就是空字符串，此时将返回所有的变量名。


    Returns
    --------
    工作空间中该变量的值。

    Raises
    ---------
    ConnectionRefusedError
        无法连接工作空间，可能是因为PyMiner未启动。
        如果发生，可能会出现如下错误：
        `ConnectionRefusedError: Cannot connect to workspace. Please confirm that PyMiner has been started!`
    TypeError:
        输入参数类型不对
    Examples
    ---------
    见set_var函数

    """
    assert type_filter in ['dataframe', 'array', 'numeric', '']  # type_filter不能乱！
    try:
        return lib.comm.get_var_names(type_filter)
    except ConnectionRefusedError:
        raise ConnectionRefusedError('Cannot connect to workspace. Please confirm that PyMiner has been started!')


def del_var(var_name: str):
    try:
        lib.comm.delete_variables([var_name])
    except:
        import traceback
        traceback.print_exc()


def set_vars(var_dic: dict, provider=''):
    try:
        if not shm_allowed():
            lib.comm.set_vars(var_dic)
        else:
            lib.comm.shm_set_vars(var_dic)
    except:
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    set_var('a', 1233)
    get_var('a')
    print(get_var_names())
