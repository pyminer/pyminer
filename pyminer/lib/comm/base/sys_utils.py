# -*- coding:utf-8 -*-
# @Time: 2021/1/26 10:52
# @Author: Zhanyi Hou
# @Email: 1295752786@qq.com
# @File: sys_utils.py
import json
import pickle
import logging
import socket
import sys
from typing import List

from lib.comm.base.network import get

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

_pickle_protocol = -1
_shm_allowed = None


def is_pyminer_service_started() -> bool:
    """
    判断PyMiner服务是否已经启动
    :return:
    """
    try:
        get('get_python_version_info', '', 12306, _timeout=0.5)
        return True
    except socket.timeout:
        return False


def get_highest_pickle_protocol(version_info: List[int]) -> int:
    server_protocol = 0
    try:

        if version_info[0] < 3:
            raise SystemError('Python Major version %d should be 3.' % version_info[0])
        if version_info[1] < 4:
            server_protocol = 3
        elif 4 <= version_info[1] <= 7:
            server_protocol = 4
        else:
            server_protocol = 5
    except SystemError as e:
        import traceback
        traceback.print_exc()
        server_protocol = 0

    client_protocol = pickle.HIGHEST_PROTOCOL
    return min(client_protocol, server_protocol)


def update_transfer_globals():
    global _shm_allowed, _pickle_protocol
    try:
        res = get('get_python_version_info', '', 12306, _timeout=1)
        version_list = json.loads(res)
    except ConnectionRefusedError:
        version_list = [sys.version_info.major, sys.version_info.minor, sys.version_info.micro]
        logger.warning(
            'Connection refused, the server protocol is set as current interpreter\'s highest protocol: %d.' % pickle.HIGHEST_PROTOCOL)

    except socket.timeout:
        server_protocol = pickle.HIGHEST_PROTOCOL
        logger.warning(
            'Connection time out, the server protocol is set as current interpreter\'s highest protocol: %d.' % pickle.HIGHEST_PROTOCOL)
        version_list = [sys.version_info.major, sys.version_info.minor, sys.version_info.micro]

    _pickle_protocol = get_highest_pickle_protocol(version_list)
    if version_list[0] >= 3 and version_list[1] >= 8:
        _shm_allowed = True
    else:
        _shm_allowed = False


def get_protocol() -> int:
    global _pickle_protocol

    if _pickle_protocol >= 0:
        return _pickle_protocol
    else:
        update_transfer_globals()
        return _pickle_protocol


def shm_allowed() -> bool:
    global _shm_allowed
    if _shm_allowed is None:
        update_transfer_globals()
    return _shm_allowed


if __name__ == "__main__":
    print(get_protocol())
    print(shm_allowed())
