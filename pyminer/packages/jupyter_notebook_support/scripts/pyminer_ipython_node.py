"""
此文件在IPython启动之时，输入到IPython的变量空间中。
它的作用是预先定义一些函数和魔术方法，定义与工作空间通信的方法。
之后重构可以考虑直接重写IPython.core.interactiveshell.InteractiveShell的各个方法，这样比在这里装配要好一些。
"""
import logging
import types

import os
import typing
from IPython.core.magic import register_line_cell_magic

__logger = logging.getLogger()
__logger.info("Env variable-- IPYTHON_AS_PYMINER_NODE： %s" % os.environ.get('IPYTHON_AS_PYMINER_NODE'))
if (os.environ.get('IPYTHON_AS_PYMINER_NODE') is not None) and (int(os.environ.get('IPYTHON_AS_PYMINER_NODE')) >= 1):
    PORT = int(os.environ.get('IPYTHON_AS_PYMINER_NODE'))
    __ip = get_ipython()
    __ip.builtin_constants = {'tau', 'In', 'Out', 'PI', 'inf', 'nan', 'E'}
    try:
        from lib.comm.base import DataDesc
        from lib.comm import set_var
        # import ipyparams
    except:
        pass


    def generate_console_id() -> str:
        """
        通过当前的文件名和
        :return:
        """
        # importlib.reload(ipyparams)
        # current_notebook = ipyparams.notebook_name
        # if current_notebook == '':
        #     current_notebook = 'Console'
        return 'IPy_{port}'.format(port=PORT)


    if typing.TYPE_CHECKING:
        from IPython.core.interactiveshell import InteractiveShell
        from IPython.core.getipython import get_ipython

    __ip: 'InteractiveShell' = get_ipython()
    __ip.builtin_vars = [__k for __k in globals().keys()]  # 内置保留变量，不可删除或者清空。
    __ip.builtin_values = {__k: __v for __k, __v in globals().items() if not __k.startswith('__')}

    __ip.var_name_list = []

    __ip.neglect_post_run = False


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
                callable(__v) or __k.startswith('_') or isinstance(__v,
                                                                   types.ModuleType) or __k in __ip.builtin_constants)}


    def __delete_var(__var_name: str):
        """
        删除变量。删除变量时不向前端发信息
        :param __var_name:
        :return:
        """
        __ip = get_ipython()
        __unused = globals().pop(__var_name)


    def __is_transfer_allowed(__key: str) -> bool:
        import types
        __ip = get_ipython()
        return __key not in __ip.builtin_vars and not __key.startswith('_') and not isinstance(globals().get(__key),
                                                                                               types.ModuleType)


    def __update_workspace():

        __var_dic = {}
        __ip = get_ipython()
        for __k in __ip.filter_vars(globals()):
            __var = globals()[__k]
            __var_dic[__k] = DataDesc(__var)
        set_var(generate_console_id(), __var_dic)
        __logger.debug("update workspace:%s" % __var_dic)


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


    def __cell_exec_func(raw_cell, store_history=False, silent=False, shell_futures=True):
        """
        相当于重写IPython的执行代码的函数！
        Args:
            raw_cell:
            store_history:
            silent:
            shell_futures:

        Returns:

        """
        __logger.info("running cell!")
        __ip = get_ipython()
        s = get_ipython().original_run_cell_func(raw_cell, store_history=store_history, silent=silent,
                                                 shell_futures=shell_futures)
        __ip.var_name_list = list(__ip.filter_vars(globals()).keys())
        __ip.update_workspace()
        return s


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


    # def __load_vars():
    __ip = get_ipython()

    __ip.original_run_cell_func = __ip.run_cell
    __ip.run_cell = __cell_exec_func
    __ip.filter_vars = __filter_vars
    __ip.update_workspace = __update_workspace
    os.environ['IPYTHON_AS_PYMINER_NODE'] = str(-1)
