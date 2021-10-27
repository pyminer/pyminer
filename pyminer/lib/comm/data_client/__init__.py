
import logging
import typing
from typing import Dict, Any, List

from lib.comm.base import get, dict_to_b64, b64_to_dict, pickle_to_dict, dict_to_pickle, get_protocol, shm_allowed, \
    DataDesc

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

_pickle_protocol = -1


def http_set_vars(vars: typing.Dict[str, typing.Any]):
    protocol = get_protocol()
    msg = get('/set_data',
              dict_to_b64(vars, protocol),
              protocol=str(protocol))
    return msg


def http_get_vars(var_names: typing.List[str], preview: bool) -> typing.Dict[str, typing.Any]:
    protocol = get_protocol()
    var_b64 = get('/get_data',
                  dict_to_b64({'var_names': var_names, 'preview': preview}, protocol=protocol),
                  protocol=str(protocol))
    msg = b64_to_dict(var_b64)
    return msg


def shm_get_vars(var_names: List[str]) -> Dict[str, Any]:
    """
    通过共享内存获取多个变量，以字典的形式返回。
    Args:
        var_names:

    Returns:

    """
    protocol = get_protocol()
    shm_name = get('/start_share_variables',
                   dict_to_b64({'var_names': var_names}, protocol),
                   protocol=str(protocol))
    logger.info('get shared variables %s from shmname%s' % (var_names, shm_name))
    from multiprocessing import shared_memory
    shm_b = shared_memory.SharedMemory(shm_name.decode(encoding='utf8'))
    buf_bytes = shm_b.buf.tobytes()
    shm_vars_dict = pickle_to_dict(buf_bytes)
    shm_b.close()  # Close each SharedMemory instance
    response = get('/end_share_variables',
                   shm_name.decode(encoding='utf8'),
                   protocol=str(protocol))
    return shm_vars_dict


def shm_set_vars(var_dic: Dict[str, Any]) -> None:
    """
    通过共享内存，设置多个变量的值。
    Args:
        var_dic:

    Returns:

    """
    from multiprocessing import shared_memory
    protocol = get_protocol()
    dmp = dict_to_pickle(var_dic, protocol)
    shm_a = shared_memory.SharedMemory(create=True, size=len(dmp))
    buffer = shm_a.buf
    buffer[:] = dmp
    response = get('/set_variables_shared',
                   shm_a.name,
                   protocol=str(protocol))
    shm_a.close()
    shm_a.unlink()


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
        return get_vars([var_name], preview).get(var_name)
    except ConnectionRefusedError:
        raise ConnectionRefusedError('Cannot connect to workspace. Please confirm that PyMiner has been started!')


def get_vars(var_names: List, preview: bool = False) -> Dict[str, Any]:
    """
    获取多个数据
    Args:
        var_names: 变量名称列表
        preview: 是否进行预览

    Returns:

    """
    try:
        if shm_allowed() and not preview:
            try:
                return shm_get_vars(var_names)
            except Exception as e:
                logger.error("共享内存传输失效，退回到http传输。")
                import traceback
                traceback.print_exc()
                return http_get_vars(var_names, False)
        else:
            return http_get_vars(var_names, preview=preview)
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

        在允许使用共享内存的情况下，会尽量使用共享内存。如果共享内存无法成功，那么就降级到http传输方式。
        http传输方式在传输较小的数据时，反而会比共享内存快一点。

    Examples
    ---------

    >>> set_var('x',[1,2,3,4,5])
    >>> get_var('x')
    [1,2,3,4,5]
    >>> get_var('y') # 如果y在工作空间不存在
    ValueError: variable 'y' not found!

    """

    try:
        set_vars({var_name: var})
    except ConnectionRefusedError:
        raise ConnectionRefusedError('Cannot connect to workspace. Please confirm that PyMiner has been started!')


def del_vars(var_names: str):
    """
    删除变量
    Args:
        var_names:

    Returns:

    """

    try:
        protocol = get_protocol()
        var_b64 = get('/delete_variables',
                      dict_to_b64({'var_names': var_names}, protocol),
                      protocol=str(protocol))
    except:
        import traceback
        traceback.print_exc()


def del_var(var_name: str):
    """
    删除变量var_name
    Args:
        var_name:

    Returns:

    """
    del_vars([var_name])


def set_vars(var_dic: Dict[str, Any]):
    """
    设置多个变量
    Args:
        var_dic:

    Returns:

    """
    try:
        if not shm_allowed():
            http_set_vars(var_dic)
        else:
            try:
                shm_set_vars(var_dic)
            except Exception as e:
                import traceback
                traceback.print_exc()
                http_set_vars(var_dic)
    except:
        import traceback
        traceback.print_exc()


def get_var_names(filter: str = '') -> typing.List[str]:
    """
    从工作空间按照指定类型获取所有的变量名。

    Parameters
    -------------
    filter: str
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
    assert filter in ['dataframe', 'array', 'numeric', '']  # type_filter不能乱！
    protocol = get_protocol()
    msg = get('/get_var_names',
              dict_to_b64({'type_filter': filter}, protocol),
              protocol=str(protocol))
    var_names = b64_to_dict(msg).get('var_names')
    return var_names


def get_data_descs() -> typing.Dict[str, DataDesc]:
    protocol = get_protocol()
    msg = get('/get_data_descs', "", protocol=str(protocol))
    var_names = b64_to_dict(msg).get('data_descs')
    return var_names


if __name__ == '__main__':
    set_var('a', 1233)
    get_var('a')
    print(get_var_names())
    print(get_data_descs())

# if __name__ == '__main__':
#     import numpy as np
#
#     # rdm = np.random.rand(1000, 1000, 100)
#     t0 = time.time()
#     # res = get('/get_data')
#     st = shm_set_vars({'a': 123, 'b': 456, 'c': 0}, protocol=3)
#     st = shm_set_vars({'l': 123, 'm': 456, 'n': [2, 3, 4, 5, 6]}, protocol=4)
#     st = shm_set_vars({'h': [1, 2, 3, 4, 5]}, protocol=5)
#     # st = get_vars(['a', 'b'])
#     # get_shared_data()
#     # get_shared_variables(['a','b'])
#     t1 = time.time()
#     print(t1 - t0)
