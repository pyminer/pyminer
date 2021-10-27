# coding=utf-8
"""
client端
长连接，短连接，心跳
"""
import json
import threading
import zlib
from typing import List

import time

from .util import timeit, receive
from .baseclient import BaseClient


def parse_splicing_packets(packet_bytes: bytes) -> List[bytes]:
    return packet_bytes.split(b'PMEND')


class GeneralClient(BaseClient):

    def __init__(self, name: str = 'Anonymous GeneralClient'):
        super().__init__(name)
        self.client = self.init_socket(12306)
        self.name = name
        th = threading.Thread(target=self.run_event_loop)
        th.setDaemon(True)
        th.start()

    def shut_down(self):
        self.client.close()

    def on_server_message_received(self, packet: bytes):
        try:
            dic = json.loads(packet)
            msg = dic.get('message')
            if msg == 'data_changed':
                pass
        except:
            import traceback
            traceback.print_exc()
            pass

    @timeit
    def compress(self, byte_str):
        return zlib.compress(byte_str)

    def run_event_loop(self):
        payload = {
            "method": "start_long_connection",
            "name": self.name,
            "params": [],
            "id": 0,
        }
        self.client.sendall(json.dumps(payload).encode('utf-8') + b'PMEND')
        recv = receive(self.client)

        message_dic = json.loads(recv)
        if message_dic.get('message') == 'succeeded':
            while True:
                try:
                    recv = receive(self.client)
                    packets = parse_splicing_packets(recv)
                    for packet in packets:
                        self.on_server_message_received(packet)
                except:
                    import traceback
                    traceback.print_exc()
                    break
        else:
            raise ConnectionError(message_dic.get('content'))


if __name__ == '__main__':
    import numpy as np

    x = np.random.random(10) + np.linspace(1, 10, 10)
    y = np.random.random(10) + np.linspace(1, 10, 10)
    print(x)
    c = GeneralClient()

    print('set_var')
    c.set_var('x', x)
    c.set_var('y', y)
    c.set_var('z', y)
    c.set_var('w', y)
    c.set_var('t', y)
    c.set_var('y', y)
    c.get_var('x')
    print(c.get_all_vars())
    print(c.get_all_var_names())
    while (1):
        time.sleep(1)
