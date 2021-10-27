# -*- coding:utf-8 -*-
# @Time: 2021/1/28 16:57
# @Author: Zhanyi Hou
# @Email: 1295752786@qq.com
# @File: find_free_port.py

import socket
from contextlib import closing

def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]

print(find_free_port())