# coding=utf-8
__author__ = '药师Aric'

import json
import threading
import zlib
from typing import List

'''
client端
长连接，短连接，心跳
'''
import socket
import time
import sys

from pmgwidgets.communication.test.util import timeit, receive
from pmgwidgets.communication.test.baseclient import BaseClient


def parse_splicing_packets(packet_bytes: bytes) -> List[bytes]:
    return packet_bytes.split(b'PMEND')


class GeneralClient(BaseClient):

    def __init__(self):
        self.client = self.init_socket(12306)
        th = threading.Thread(target=self.run_event_loop)
        th.setDaemon(True)
        th.start()

    def shut_down(self):
        print('quit')
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
        self.client.sendall(b'long_conn')
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
