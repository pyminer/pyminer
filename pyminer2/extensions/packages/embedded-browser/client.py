#!/usr/bin/python
import socket
import json
import time
import cloudpickle
import base64


def dump_data_from_b64(data: object) -> str:
    try:
        data_dumped_bytes = cloudpickle.dumps(data)
        return base64.b64encode(data_dumped_bytes).decode('ascii')
    except:
        import traceback
        traceback.print_exc()


def load_data_from_b64(data_b64: str) -> object:
    try:
        return cloudpickle.loads(base64.b64decode(data_b64))
    except:
        import traceback
        traceback.print_exc()
        return None


def timeit(func):
    def wrapper(*args, **kwargs):
        t0 = time.time()
        r = func(*args, **kwargs)
        print(time.time() - t0)
        return r

    return wrapper


def request_data(byte_data) -> bytes:
    HOST = '127.0.0.1'
    PORT = 12306
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 定义socket类型，网络通信，TCP
    s.connect((HOST, PORT))  # 要连接的IP与端口

    # cmd=b"Please input cmd:"      #与人交互，输入命令
    s.sendall(byte_data + b'PMEND')  # 把命令发送给对端

    p = b''
    while (1):
        b = s.recv(65536)
        p += b
        if b.endswith(b'PMEND'):
            p = p.strip(b'PMEND')
            break
    data = p  # 把接收的数据定义为变量

    s.close()  # 关闭连接
    return data


@timeit
def get_var(data_name: str):
    payload = {
        "method": "read_p",
        "params": [data_name],
        "jsonrpc": "2.0",
        "id": 0,
    }
    b = request_data(json.dumps(payload).encode('utf-8'))
    response_dic: dict = json.loads(b.decode('utf-8'))
    data_b64 = response_dic.get(data_name)
    if data_b64 is not None:
        s = load_data_from_b64(data_b64)
        return s
    return None


@timeit
def set_var(data_name: str, data: object, provider: str = 'server'):
    dumped_data = dump_data_from_b64(data)
    # print(load_data_from_b64(dumped_data))
    payload = {
        "method": "write_p",
        "params": [data_name, dumped_data, provider],
        "jsonrpc": "2.0",
        "id": 0,
    }
    b = request_data(json.dumps(payload).encode('utf-8'))
    response_dic: dict = json.loads(b.decode('utf-8'))

    return response_dic


if __name__ == '__main__':
    # print('b', get_var_p('b'))
    # print('a', get_var_p('a'))
    # print(dump_data_from_b64(1))
    import numpy as np

    set_var('x', np.zeros((100, 100, 10)))
    set_var('y', 5)
    print('x', get_var('x').shape)
    print('y', get_var('y').shape)
