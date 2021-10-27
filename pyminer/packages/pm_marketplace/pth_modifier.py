import os
import sys
import time
from typing import List
import platform
import socket
import threading


class PMServer():
    def __init__(self,port:int):

        s = socket.socket()  # 创建 socket 对象
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        host = socket.gethostname()  # 获取本地主机名
        s.bind((host, port))  # 绑定端口

        s.listen(5)  # 等待客户端连接
    def run(self):
        # !/usr/bin/python
        # -*- coding: UTF-8 -*-
        # 文件名：server_long_conn.py



        while True:
            c, addr = s.accept()  # 建立客户端连接
            print(            '连接地址：', addr)
            c.send('欢迎访问菜鸟教程！')
            c.close()  # 关闭连接




def run_server(port:int):
    server = PMServer(port)
    server.run()


class PMPathManager():
    _paths: List[str] = []

    def __init__(self):
        pass

    def add_path(self, path: str):
        path = path.strip()
        if platform.system() == 'Windows':
            path = path.lower()
        self._paths.append(path)
        self._paths = list(set(self._paths))

    def get_all_paths(self):
        return self._paths


def remove_pth_file(module_path: str):
    pth_file = find_pth_file()
    if pth_file is None:
        return
    with open(pth_file, 'r+') as f:
        content = f.readlines()

    content = list(map(lambda s: s.strip(), content))
    content.append(module_path)
    print(content)
    content_set = set(content)
    if module_path in content_set:
        content_set.remove(module_path)

    content = list(content_set)
    print(content)
    with open(pth_file, 'w') as f:
        for path in content:
            if path == '' or path == '\n':
                continue
            f.write(path + '\n')


def add_to_pth_file(module_path: str) -> str:
    pth_file = find_pth_file()
    if pth_file is None:
        return
    with open(pth_file, 'r+') as f:
        content = f.readlines()

    content = list(map(lambda s: s.strip(), content))
    content.append(module_path)
    content = list(set(content))
    with open(pth_file, 'w') as f:
        for path in content:
            if path == '' or path == '\n':
                continue
            f.write(path + '\n')


def find_pth_file() -> str:
    """
    返回pyminer的pth文件，专门存储各种模块用。
    """
    import site
    site_packages = site.getsitepackages()
    l = list(filter(lambda s: s.endswith('site-packages'), site_packages))
    if len(l) > 0:
        pm_pth_file = os.path.join(l[0], 'pyminer_modules.pth')
        if not os.path.exists(pm_pth_file):
            with open(pm_pth_file, 'w') as f:
                f.close()

        return pm_pth_file
    return None


if __name__ == '__main__':
    import threading
    th = threading.Thread(target=run_server,args=(12306,))
    th.setDaemon(True)
    th.start()
    while(1):
        time.sleep(1)

