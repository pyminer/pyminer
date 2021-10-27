# coding=utf-8
__author__ = '侯展意'

import json
import logging
import socket
import sys
import warnings
import zlib
from typing import List

from PySide2.QtCore import QObject, QThread, Signal, QTimer
from PySide2.QtWidgets import QApplication

from .baseclient import BaseClient
from .util import timeit, receive

logger = logging.getLogger(__name__)


def parse_splicing_packets(packet_bytes: bytes) -> List[bytes]:
    return packet_bytes.split(b'PMEND')


class RecvWork(QObject):
    signal_received = Signal(bytes)

    def __init__(self, sock: socket.socket, name: str):
        super(RecvWork, self).__init__()
        self.quit = False
        self.socket = sock
        self.name = name

    def work(self):
        payload = {
            "method": "start_long_connection",
            "name": self.name,
            "id": 0,
        }
        self.socket.sendall(json.dumps(payload).encode('utf-8') + b'PMEND')
        while True:
            try:
                recv = receive(self.socket)
                assert recv != b''
                packets = parse_splicing_packets(recv)
                for p in packets:
                    self.signal_received.emit(p)
            except AssertionError:
                self.socket.close()
                warnings.warn('Connection \'%s\' Closed!' % self.name)
                break
            except:
                import traceback
                traceback.print_exc()
                break
        self.thread().quit()

    def close_socket(self):
        self.socket.close()


class PMClient(QObject, BaseClient):
    signal_server_message_received = Signal(dict)
    signal_data_changed = Signal(str)

    def __init__(self, parent=None, name='Anonymous QtClient'):
        super().__init__(parent)
        self.name = name
        self.client = self.init_socket(12306)
        self.thread_recv = QThread()
        self.worker_recv = RecvWork(self.client, self.name)
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
