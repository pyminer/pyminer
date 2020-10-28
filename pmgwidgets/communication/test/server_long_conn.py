"""
基于qthread的服务器
直接基于socket。

"""

import json
from typing import List, Tuple

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject, QThread, QTimer, pyqtSignal
import socket  # 导入 socket 模块
import sys
import logging

from pmgwidgets.communication.test.util import receive, timeit

logger = logging.getLogger(__name__)

g_conn_pool = []


def parse_splicing_packets(packet_bytes: bytes) -> List[bytes]:
    return packet_bytes.split(b'PMEND')


class MessageWork(QObject):
    signal_message_received = pyqtSignal(socket.socket, bytes)
    signal_work_finished = pyqtSignal()
    signal_socket_closed = pyqtSignal(socket.socket)

    def __init__(self, server: 'PMGServer'):
        super(MessageWork, self).__init__()
        self.server = server

    def work(self):
        self.message_handle(client=self.client)
        self.signal_work_finished.emit()

    def handle_packet(self, client: socket.socket, packet: bytes):
        try:
            dic = json.loads(packet)
            func = self.server.dispatcher_dic[dic['method']]
            args = dic['params']
            client.sendall(func(*args).encode('utf-8') + b'PMEND')
        except:
            client.close()
            self.signal_socket_closed.emit(client)
            logger.warning(repr(self.server.long_conn_sockets))
            return b''

    def message_handle(self, client):
        """
        消息处理
        """
        while True:
            logger.info('client waiting!' + repr(client))
            logger.info('conn_pool_length:%d ,list is: %s' % (len(self.server.long_conn_sockets),
                                                              repr(self.server.long_conn_sockets)))
            try:
                bytes = receive(client)
                for packet in parse_splicing_packets(bytes):
                    self.handle_packet(client, packet)
            except:
                import traceback
                traceback.print_exc()
                client.close()
                # 删除连接
                self.signal_socket_closed.emit(client)
                logger.info("客户端%s下线了。" % repr(client))
                break
            if len(bytes) == 0:
                client.close()
                self.signal_socket_closed.emit(client)
                logger.info("客户端%s下线了。" % repr(client))
                break


class LoopWork(QObject):
    def __init__(self, server_obj: 'PMGServer', server_socket: socket.socket):
        super().__init__()
        self.server_socket = server_socket
        self.server_obj = server_obj
        self.threads = []

    def work(self):
        self.accept_client(self.server_socket)

    def accept_client(self, server_socket):
        """
        接收新连接
        """
        while True:
            try:
                client, _ = server_socket.accept()  # 阻塞，等待客户端连接
            except:
                import traceback
                traceback.print_exc()
                break
            # 加入连接池
            conn_message = client.recv(1024)

            if conn_message == b'long_conn':  # 如果请求的是一个长连接，就给每个客户端创建一个独立的线程进行管理
                self.server_obj.long_conn_sockets.append(client)
                thread = QThread()
                worker = MessageWork(self.server_obj)
                worker.signal_socket_closed.connect(self.server_obj.remove_socket)
                worker.client = client

                # worker.server = self.server_obj
                worker.moveToThread(thread)
                thread.started.connect(worker.work)
                thread.start()
                worker.signal_work_finished.connect(thread.quit)
                self.threads.append([thread, worker])  # 保持多连接要求保持引用。
            else:  # 如果请求的不是一个长连接，就直接进行处理，

                client.send(b'conn_established')
                b = receive(client)
                self.handle_packet(client, b)
            # except:
            #     import traceback
            #     traceback.print_exc()
            #     client.close()
            #     break

    def handle_packet(self, client: socket.socket, packet: bytes):
        try:
            dic = json.loads(packet)
            func = self.server_obj.dispatcher_dic[dic['method']]
            args = dic['params']
            vy = func(*args).encode('utf-8') + b'PMEND'
            client.sendall(vy)
        except:
            import traceback
            traceback.print_exc()
            client.close()

            logger.warning(repr(g_conn_pool))
            return b''


class PMGServer(QObject):
    def __init__(self, address=Tuple[str, int], parent=None):
        super().__init__(parent)
        self.dispatcher_dic = {}
        self.long_conn_sockets = []
        self.socket = self.init_socket(address)
        self.server_loop_thread = QThread()
        self.loop_worker = LoopWork(self, self.socket)
        self.loop_worker.moveToThread(self.server_loop_thread)

        self.server_loop_thread.started.connect(self.loop_worker.work)
        self.server_loop_thread.start()

    def init_socket(self, address):
        """
        初始化套接字
        """
        g_socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建 socket 对象

        # g_socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        g_socket_server.bind(address)
        g_socket_server.listen(5)  # 最大等待数（有很多人理解为最大连接数，其实是错误的）
        logger.info("服务端已启动，等待客户端连接...")
        return g_socket_server

    def broadcast_message(self, message_dic: dict = None):
        """
        广播信息
        message:传递信息
        # 'DATA_CHANGED'
        # 'SHUT_DOWN'
        :param clients:
        :return:
        """
        if message_dic is None:
            message_dic = {'name': 'broadcast', 'message': 'Are you alive?'}
        clients = self.long_conn_sockets

        ids = []
        logger.info('broadcast message:'+repr(message_dic))
        for i, client in enumerate(clients):
            try:
                client.sendall(json.dumps(message_dic).encode('utf8') + b'PMEND')
            except:
                import traceback
                traceback.print_exc()
                ids.append(client)
        logger.info('died connections:' + repr(ids))
        for not_used_socket in ids:
            self.remove_socket(not_used_socket)

    def remove_socket(self, socket_to_remove: socket.socket):
        if socket_to_remove in self.long_conn_sockets:
            self.long_conn_sockets.remove(socket_to_remove)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ADDRESS = ('127.0.0.1', 12306)  # 绑定地址
    s = PMGServer(ADDRESS)

    qtimer = QTimer()
    qtimer.start(2000)
    qtimer.timeout.connect(lambda: s.broadcast_message(None))
    sys.exit(app.exec_())
