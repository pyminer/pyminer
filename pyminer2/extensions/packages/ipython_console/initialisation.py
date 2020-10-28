"""
Modification:
revise __inspect function， return a dict where key:str,value:str
when console receives prints
pickle items sequentially
if catch any error, then pass
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import base64
import cloudpickle as pickle
import types
import json
from matgen import v_, h_, M_
from pyminer_algorithms import *
from pmgwidgets.communication.test.clientgeneral import GeneralClient

__ip = get_ipython()
__builtins = [__k for __k in globals().keys()]
__var_name_list = []
__neglect_post_run = False  # 为True的时候，执行命令不触发回调。防止刷新造成无限反复。

# print('123123123123')
def __on_broadcast_message_received(packet: bytes):
    try:
        dic = json.loads(packet)
        msg = dic.get('message')
        if msg == 'data_changed':
            data_name = dic.get('data_name')
            source = dic.get('data_source')
            # with open(r'c:\users\12957\Desktop\log.txt', 'w') as f:
            #     f.write(repr(source) + '\n')
            if source != 'ipython':

                data = __client.get_var(data_name)
                # with open(r'c:\users\12957\Desktop\log.txt', 'w') as f:
                #     f.write(repr(data) + '\n')
                if data is None:  # 这一步的目的比较简单，只是双保险。如果返回值为None,再来一次就可以基本保证不出错。
                    data = __client.get_var(data_name)
                globals().update({data_name: data})
    except:
        import traceback
        traceback.print_exc()
        pass


def __update_var_set(__data: dict):
    __name_list = list(__data.keys())


def __refresh_vars():
    global __var_name_list
    __data_message = {}
    __data = {
        __k: __v for __k,
                     __v in globals().items() if __k not in __builtins and not __k.startswith('_') and not isinstance(
            __v,
            types.ModuleType)}

    __name_list = list(__data.keys())
    __deleted_data_name = set(__var_name_list) - set(__name_list)
    # __added_data_name = set(__name_list) - set(__var_name_list)
    # __added_data = {}
    __var_name_list = __name_list
    for __deleted_name in __deleted_data_name:
        __client.delete_var(__deleted_name, provider='ipython')
    # for __added_name in __added_data_name:
    #     __added_data[__added_name] = __data[__added_name]
    try:
        # __client.set_var_dic(__added_data, 'ipython')
        __client.set_var_dic(__data, 'ipython')
        __update_globals_from_workspace()
    except:
        import traceback
        traceback.print_exc()


def __inspect():
    __data_message = {}
    __data = {
        __k: __v for __k,
                     __v in globals().items() if __k not in __builtins and not __k.startswith('_') and not isinstance(
            __v,
            types.ModuleType)}
    for __k in __data.keys():
        try:
            __data_message[__k] = base64.b64encode(
                pickle.dumps(__data[__k])).decode('ascii')
        except:
            import traceback
            traceback.print_exc()
    print(base64.b64encode(pickle.dumps(__data_message)).decode('ascii'))


def __inject(data_b64):
    data_b64_dic = pickle.loads(base64.b64decode(data_b64))
    data = {}
    for key in data_b64_dic:
        var = data_b64_dic[key]
        try:
            data[key] = pickle.loads(base64.b64decode(data_b64_dic[key]))
        except BaseException:
            import traceback
            traceback.print_exc()
    globals().update(data)


def __update_globals_from_workspace():
    global __client
    globals().update(__client.get_all_vars())


def __delete_var(__var_name: str):
    """
    删除变量。删除变量时不向工作空间发信息（因为这个变量往往来自工作空间）
    :param __var_name:
    :return:
    """
    global __neglect_post_run, __var_name_list
    if __var_name in globals().keys():
        __unused = globals().pop(__var_name)
        __neglect_post_run = True
        __data = {__k: __v for __k, __v in globals().items()
                  if __k not in __builtins and not __k.startswith('_') and not isinstance(__v, types.ModuleType)}
        __var_name_list = list(__data.keys())


def __post_run_callback():
    global __neglect_post_run
    if __neglect_post_run:
        __neglect_post_run = False
        return
    __refresh_vars()


__client = GeneralClient()

__client.on_server_message_received = __on_broadcast_message_received
# __ip.events.register('post_run_cell', __inspect)
__ip.events.register('post_run_cell', __post_run_callback)
