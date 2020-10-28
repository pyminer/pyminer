# coding=utf-8
__author__ = '药师Aric'

import base64
import json
import zlib
from typing import List
import logging

logger = logging.getLogger(__name__)
import cloudpickle

'''
client端
长连接，短连接，心跳
'''
import socket
import time
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject, QThread, pyqtSignal, QTimer
import sys

from pmgwidgets.communication.test.util import timeit, receive
from pmgwidgets.communication.test.baseclient import BaseClient


def parse_splicing_packets(packet_bytes: bytes) -> List[bytes]:
    return packet_bytes.split(b'PMEND')


class RecvWork(QObject):
    signal_received = pyqtSignal(bytes)

    def __init__(self, socket_client: socket.socket):
        super(RecvWork, self).__init__()
        self.quit = False
        self.socket_client = socket_client

    def work(self):
        client = self.socket_client
        client.sendall(b'long_conn')
        while True:
            try:
                recv = receive(client)
                assert recv != b''
                packets = parse_splicing_packets(recv)
                for p in packets:
                    self.signal_received.emit(p)
            except:
                import traceback
                traceback.print_exc()
                break
            # time.sleep(1)  # 如果想验证长时间没发数据，SOCKET连接会不会断开，则可以设置时间长一点
        self.thread().quit()

    def close_socket(self):
        self.socket_client.close()


class PMClient(QObject, BaseClient):
    signal_server_message_received = pyqtSignal(dict)
    signal_data_changed = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.client = self.init_socket(12306)
        self.thread_recv = QThread()
        self.worker_recv = RecvWork(self.client)
        self.signal_received = self.worker_recv.signal_received
        self.worker_recv.signal_received.connect(self.on_server_message_received)

        self.worker_recv.moveToThread(self.thread_recv)
        self.thread_recv.started.connect(self.worker_recv.work)
        self.thread_recv.start()

    def shut_down(self):
        logger.info('client quit')
        self.worker_recv.close_socket()
        self.thread_recv.quit()
        self.thread_recv.wait(500)

    def on_server_message_received(self, packet: bytes):
        try:
            dic = json.loads(packet)
            logger.info(dic)
            msg = dic.get('message')
            if msg == 'data_changed':
                data_name = dic.get('data_name')
                if data_name is not None:
                    self.signal_data_changed.emit(data_name)
            self.signal_server_message_received.emit(dic)
        except:
            import traceback
            traceback.print_exc()
            pass

    def send_bytes(self, packet: bytes):
        self.client.sendall(packet)

    @timeit
    def compress(self, byte_str):
        return zlib.compress(byte_str)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    import numpy as np

    x = np.random.random(10) + np.linspace(1, 10, 10)
    y = np.random.random(10) + np.linspace(1, 10, 10)
    print(x)
    c = PMClient()
    print('set_var')
    c.set_var('x', x)
    c.set_var('y', y)
    c.get_var('x')
    print(c.get_all_var_names())
    timer = QTimer()
    timer.start(10000)
    timer.timeout.connect(lambda: c.get_var('x'))
    c.shut_down()
    sys.exit(app.exec_())
