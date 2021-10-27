# -*- coding:utf-8 -*-
# @Time: 2021/1/26 10:29
# @Author: Zhanyi Hou
# @Email: 1295752786@qq.com
# @File: base.py
import logging
import socket

logger = logging.getLogger(__name__)
# 由于这个文件里的内容会在ipython中进行调用，因此使用WARNING级别以降低在ipython里面的输出
logger.setLevel(logging.WARNING)


def get(method: str, msg: str, port=52346, _timeout: int = None, **kwargs) -> bytes:
    s = socket.socket()
    if _timeout is not None:
        s.settimeout(_timeout)
    try:
        s.connect(('localhost', port))
    except socket.timeout as e:
        s.close()
        logger.debug('Connection timeout')
        raise e
    if _timeout is not None:
        s.settimeout(None)
    req_args = ''
    for k, v in kwargs.items():
        assert isinstance(v, str), v
        req_args += '&%s=%s' % (k, v)
    s.sendall(('''GET %s?msg=%s%s HTTP/1.1\r\n\r\n''' % (method, msg, req_args)).encode('ascii'))
    bytes_list = []
    buf = s.recv(1024)
    while len(buf):
        buf = s.recv(1024)
        bytes_list.append(buf)
    logger.info('got message,length:%d' % len(bytes_list))
    s.close()
    return b''.join(bytes_list).split(b'\r\n\r\n', maxsplit=1)[1]
