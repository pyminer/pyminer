# -*- coding:utf-8 -*-
# @Time: 2021/1/25 18:16
# @Author: Zhanyi Hou
# @Email: 1295752786@qq.com
# @File: pm_client.py
import json
from typing import Any, Dict, Optional, List

from lib.comm.base import get, dict_to_b64, b64_to_dict, DataDesc, get_protocol


class SetDataDescError(Exception):
    pass


def modify_settings(items: Dict[str, Any]):
    """
    修改设置
    :param items:
    :return:
    """
    assert isinstance(items, dict), items
    res = get('modify_settings', dict_to_b64(items, protocol=get_protocol()), 12306, )
    return res

def set_data_desc_dic(data: Dict[str, Any]) -> None:
    for k, v in data.items():
        assert isinstance(v, DataDesc)
    res = get('set_data', dict_to_b64(data, protocol=get_protocol()), 12306)
    res_json = json.loads(res)
    if res_json['status'] == "failed":
        raise SetDataDescError(res_json['error'])


def get_settings() -> Dict[str, Any]:
    res = get('get_settings', '', 12306)
    return json.loads(res)


def get_style_sheet() -> str:
    res = get('get_stylesheet', '', 12306)
    return res.decode('utf-8', errors='replace')


def call_interface(interface: str, method: str, kwargs: dict = None, request_ret=False) -> Optional[Any]:
    """
    通过网络，调用PyMiner内部Extension插件的Interface接口。
    Args:
        interface: 插件的名称
        method: 插件接口的方法名
        kwargs: 插件的接口函数调用的参数，要求需要能被序列化
        request_ret: 是否要求传回结果，默认为False

    Returns:

    """
    kwargs = {} if kwargs is None else kwargs
    res = get('interface_call',
              dict_to_b64({'interface': interface, 'method': method, 'kwargs': kwargs}, protocol=get_protocol()), 12306,
              request_ret=repr(request_ret))
    if request_ret:
        return b64_to_dict(res)['response']
    else:
        return None


def run_command(command: str, hint_text: str = '', hidden: bool = False):
    return call_interface('ipython_console', 'run_command',
                          {'hidden': hidden, 'command': command, 'hint_text': hint_text})


def exec_ipy_command(command: str, rets: List[str]):
    ret = get('exec_command', dict_to_b64({'command': command, 'rets': rets},protocol=get_protocol()),protocol=str(get_protocol()))
    print(ret)
    return b64_to_dict(ret)

def test():
    res = get('test', '', 12306)
    print(res)


if __name__ == "__main__":
    set_data_desc_dic({'a': DataDesc(123)})
    try:
        set_data_desc_dic({'a': 123})
    except BaseException:
        import traceback

        traceback.print_exc()
    print(get_settings())
    print(get_style_sheet())
    print(call_interface('workspace_inspector', 'get_selected_variables', {}))
    print(exec_ipy_command('b=1;c=2;a=b+c', ['a']))
    # print(run_command('a=1+2+5'))
