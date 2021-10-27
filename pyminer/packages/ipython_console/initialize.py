"""
此文件在IPython启动之时，输入到IPython的变量空间中。
它的作用是预先定义一些函数和魔术方法，定义与工作空间通信的方法。
之后重构可以考虑直接重写IPython.core.interactiveshell.InteractiveShell的各个方法，这样比在这里装配要好一些。
"""

import types
import typing

from lib.comm import modify_settings, set_data_desc_dic
from lib.comm.base import dict_to_b64, b64_to_dict, dict_to_pickle, pickle_to_dict, DataDesc, is_big_variable, \
    NoPreviewError

try:
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    import scipy.integrate
    import scipy.stats
    from core import *

    __packages = [np, plt, pd, scipy.integrate, scipy.stats]
except Exception as e:
    import traceback

    traceback.print_exc()

if typing.TYPE_CHECKING:
    from IPython.core.interactiveshell import InteractiveShell
    from IPython.core.getipython import get_ipython

from IPython.core.magic import register_line_cell_magic

__ip: 'InteractiveShell' = get_ipython()

__ip.builtin_vars = [__k for __k in globals().keys()]  # 内置保留变量，不可删除或者清空。
__ip.builtin_values = {__k: __v for __k, __v in globals().items() if not __k.startswith('__')}
__ip.builtin_constants = {'tau', 'In', 'Out', 'PI', 'inf', 'nan', 'E'}
__ip.var_name_list = []

__ip.neglect_post_run = False


def __init_server():
    """
    初始化本地ipython数据服务器。
    Returns:

    """
    from flask import Flask
    from flask import request
    import threading
    import logging
    import typing

    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    server = Flask('ipython_data_server')
    __ip = get_ipython()
    __ip.shms = {}
    log.debug("started server!")

    def get_preview(var: typing.Any):
        if is_big_variable(var):
            if isinstance(var, (int, float, complex)):
                return var
            if isinstance(var, (list, tuple)):
                return var[:DataDesc.max_len]
            elif isinstance(var, str):
                if len(var) > DataDesc.max_str_len:
                    return var[:DataDesc.max_str_len]
                else:
                    return var

            try:
                if isinstance(var, pd.DataFrame):
                    if var.shape[0] > DataDesc.max_pandas_rows:
                        return var.iloc[:DataDesc.max_pandas_rows, :]
                    else:
                        return var

                if isinstance(var, np.ndarray):
                    if is_big_variable(var):
                        return NoPreviewError(
                            'Big numpy.ndarray with shape: %s, dtype:%s, memory usage: %s MB, cannot be viewed.'
                            % (repr(var.shape), repr(var.dtype), repr(var.nbytes / 1024 / 1024)))
                    else:
                        return var

            except Exception as e:
                return e


            else:
                return NoPreviewError('Big Variable typed %s cannot be viewed.' % (type(var)))  # 无法产生预览视图。
        else:
            return repr(var)

    def write_log(arg):
        if os.path.exists(r'c:\users\hzy\Desktop\log.txt'):
            log_file = open(r'c:\users\hzy\Desktop\log.txt', 'a')
            log_file.write(repr(arg) + '\n')
            log_file.close()

    @server.route('/')
    def index():
        user_agent = request.headers.get('User_Agent')
        return 'user_agent is %s' % user_agent

    @server.route('/get_data')
    def get_var_by_http():
        """
        请求参数：name(变量空间中有的变量);type(pickle/json)
        Returns:

        """
        protocol = int(request.args.get('protocol'))
        assert 1 < protocol <= 5
        msg = request.args.get('msg')
        req_dict = b64_to_dict(msg)
        var_names = req_dict.get('var_names')
        preview = req_dict.get('preview')
        if preview:
            vars = {k: get_preview(globals().get(k)) for k in var_names}
        else:
            vars = {k: globals().get(k) for k in var_names}
        return dict_to_b64(vars, protocol)

    @server.route('/get_data_descs')
    def get_data_descs():
        """
        请求参数：name(变量空间中有的变量);type(pickle/json)
        Returns:

        """
        protocol = int(request.args.get('protocol'))
        assert 1 < protocol <= 5

        return dict_to_b64({"data_descs": get_ipython().get_data_descs()}, protocol)

    @server.route('/set_data')
    def set_var_by_http():
        """
        protocol可以自动检测。
        相关文档中如是说：
        Protocol version 2 was introduced in Python 2.3.

        Protocol version 3 was added in Python 3.0.

        Protocol version 4 was added in Python 3.4.

        Protocol version 5 was added in Python 3.8.

        Python 3.8 on default was pickle protocol 5.

        vars:
        input:msg#pickle stream
        input:params#(json)
        {   "protocol":4,
            "vars":{"a":123,"b":"aaaaaaa"}
        }
        Returns:

        """
        protocol = int(request.args.get('protocol'))
        msg = request.args.get('msg')
        vars = b64_to_dict(msg)
        get_ipython().push(vars)
        __ip.update_workspace()
        return 'set succeeded!'

    @server.route('/get_var_names')
    def get_var_names():
        """
        type_filter.
        'dataframe' for pandas.DataFrame
        'array' for numpy.ndarray
        'numeric' for bool, int and float
        Returns:

        """
        protocol = int(request.args.get('protocol'))
        msg = request.args.get('msg')
        args = b64_to_dict(msg)
        type_filter = args.get('type_filter')
        vars_dic = __ip.filter_vars(globals())
        if type_filter == '':
            msg = dict_to_b64({'var_names': list(__ip.filter_vars(globals()).keys())},
                              protocol=protocol)
        elif type_filter == 'dataframe':
            msg = dict_to_b64(
                {'var_names': list({k: v for k, v in vars_dic.items() if isinstance(v, pd.DataFrame)}.keys())},
                protocol=protocol)
        elif type_filter == 'array':
            msg = dict_to_b64(
                {'var_names': list({k: v for k, v in vars_dic.items() if isinstance(v, np.ndarray)}.keys())},
                protocol=protocol)
        elif type_filter == 'numeric':
            msg = dict_to_b64(
                {'var_names': list({k: v for k, v in vars_dic.items() if isinstance(v, (bool, int, float))}.keys())},
                protocol=protocol)
        elif msg == 'str':
            msg = dict_to_b64(
                {'var_names': list({k: v for k, v in vars_dic.items() if isinstance(v, str)}.keys())},
                protocol=protocol)
        else:
            msg = dict_to_b64(
                {'var_names': list(__ip.filter_vars(globals()).keys())},
                protocol=protocol)
        return msg

    @server.route('/get_variables_preview')
    def get_vars_preview():
        protocol = int(request.args.get('protocol'))
        msg = request.args.get('msg')
        var_names = b64_to_dict(msg, protocol).get('var_names')
        vars = {k: get_preview(globals().get(k)) for k in var_names}
        return dict_to_b64(vars, protocol)

    def start():
        server.run(host='127.0.0.1', port=52346, debug=False, threaded=True)

    @server.route('/start_share_variables')
    def start_share_variables():
        from multiprocessing import shared_memory
        global __lock
        protocol = int(request.args.get('protocol'))

        __lock = threading.Lock()
        msg = request.args.get('msg')
        var_names = b64_to_dict(msg).get('var_names')
        vars = {k: globals().get(k) for k in var_names}
        dmp = dict_to_pickle(vars, protocol=protocol)
        __lock.acquire()
        __shm_a = shared_memory.SharedMemory(create=True, size=len(dmp))
        buffer = __shm_a.buf
        buffer[:] = dmp
        write_log([b64_to_dict(msg), var_names, __shm_a.name])
        __ip.shms[__shm_a.name] = __shm_a
        return __shm_a.name

    @server.route('/end_share_variables')
    def stop_share_variables():
        global __lock
        shm_name = request.args.get('msg')
        __shm_a = __ip.shms.get(shm_name)
        if __shm_a is not None:
            __shm_a.close()
            __shm_a.unlink()
            __ip.shms.pop(shm_name)
            __lock.release()
            return 'succeeded!%s closed!' % __shm_a.name
        else:
            return 'Failed.shm %s not exist.' % shm_name

    @server.route('/set_variables_shared')
    def set_variables_shared():
        from multiprocessing import shared_memory
        shm_name = request.args.get('msg')
        shm_b = shared_memory.SharedMemory(shm_name)
        b = shm_b.buf.tobytes()
        shm_b.close()
        var_dic = pickle_to_dict(b)
        globals().update(var_dic)
        __ip.update_workspace()
        return 'succeeded!shared variable!'

    @server.route('/delete_variables')
    def delete_variables():
        msg = request.args.get('msg')
        var_names = b64_to_dict(msg).get('var_names')
        for __name in var_names:
            __ip.delete_var(__name)
        __ip.update_workspace()
        return 'succeeded!'

    @server.route('/exec_command')
    def exec_command():
        msg = request.args.get('msg')  # {'command':'xxxxxx','rets':['a','b',...]}
        protocol = int(request.args.get('protocol'))
        try:
            msg = b64_to_dict(msg)
            exec(msg['command'])
            vars = locals()
            print({ret: vars.get(ret) for ret in msg['rets']})
            return dict_to_b64({ret: vars.get(ret) for ret in msg['rets']}, protocol=protocol)
        except Exception as e:
            import traceback
            return dict_to_b64({'message': traceback.format_exc()}, protocol=protocol)

    th = threading.Thread(target=start)
    th.setDaemon(True)
    th.start()

    __ip.server_thread = th
    __ip.server = server


def __filter_vars(__data: dict) -> dict:
    """
    过滤掉可调用的变量，以防用户使用
    from numpy import *
    这一类操作，造成工作空间不堪重负。
    :param __data:
    :return:
    """
    __ip = get_ipython()
    return {__k: __v for __k, __v in __data.items() if not (
            __k.startswith('_') or isinstance(__v, types.ModuleType) or __k in __ip.builtin_constants
            or __k in __ip.builtin_values.keys())}


def __delete_var(__var_name: str):
    """
    删除变量。删除变量时不向工作空间发信息（因为这个变量往往来自工作空间）
    :param __var_name:
    :return:
    """
    __ip = get_ipython()
    __unused = globals().pop(__var_name)


def __is_transfer_allowed(__key: str) -> bool:
    import types
    __ip = get_ipython()
    return not __key.startswith('_') and not isinstance(globals().get(__key), types.ModuleType)


def __update_workspace():
    __var_dic = {}
    __ip = get_ipython()
    for __k in __ip.filter_vars(globals()):
        __var = globals()[__k]
        __var_dic[__k] = DataDesc(__var)
    set_data_desc_dic(__var_dic)


@register_line_cell_magic
def lcmagic(line, cell=None):
    """
    这是IPython魔术方法的一个例子，可以通过这个来找到例子。
    :param line:
    :param cell:
    :return:
    """
    if cell is None:
        print("Called as line magic")
        return line
    else:
        print("Called as cell magic")
        return line, cell


def __clear_all():
    """
    清除全部变量
    Returns:

    """
    __ip = get_ipython()
    for __var_name in __ip.var_name_list:
        globals().pop(__var_name)

    # __ip.neglect_post_run = True


__ip.original_run_cell_func = __ip.run_cell


def __cell_exec_func(raw_cell, store_history=False, silent=False, shell_futures=True):
    """
    相当于重写IPython的执行代码的函数！
    在执行的外边包了一层抽象语法树解释。
    Args:
        raw_cell:
        store_history:
        silent:
        shell_futures:

    Returns:

    """
    __ip = get_ipython()
    __cwd = os.getcwd()

    __ret = get_ipython().original_run_cell_func(raw_cell, store_history=store_history, silent=silent,
                                                 shell_futures=shell_futures)
    __ip.var_name_list = list(__ip.filter_vars(globals()).keys())
    __ip.update_workspace()
    if __cwd != os.getcwd():
        modify_settings({'MAIN/PATH_WORKDIR': os.getcwd()})
    return __ret


def __chdir(path: str):
    os.chdir(path)
    print('The work path has been switched to: %s' % path)


def __reset(new_session=True):
    __ip = get_ipython()
    __ip.original_reset_func(new_session)

    globals().update(__ip.builtin_values)


def __save_vars(var_names: list, path: str, save_type: str):
    __ip = get_ipython()
    from utils.io.fileutil.variableutils import save_variable_pmd
    if len(var_names) == 0:
        var_names = list(__ip.filter_vars(globals()).keys())

    if save_type == 'pmd':
        values = [globals().get(_name) for _name in var_names]
        save_variable_pmd(var_names, values, path)
    if save_type == 'csv':
        pass
    print('保存成功！')


def __load_vars():
    __ip = get_ipython()


def __get_data_descs():
    __var_dic = {}
    __ip = get_ipython()
    for __k in __ip.filter_vars(globals()):
        __var = globals()[__k]
        __var_dic[__k] = DataDesc(__var)
    return __var_dic


__init_server()

__ip.builtin_values = {__k: __v for __k, __v in globals().items() if not __k.startswith('__')}

__ip.filter_vars = __filter_vars
__ip.delete_var = __delete_var
__ip.clear_all = __clear_all
__ip.run_cell = __cell_exec_func
__ip.save_vars = __save_vars
__ip.original_reset_func = __ip.reset
__ip.reset = __reset
__ip.update_workspace = __update_workspace
__ip.chdir = __chdir
__ip.get_data_descs = __get_data_descs
