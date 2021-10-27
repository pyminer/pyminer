"""
基于qthread的服务器
直接基于socket。

"""

import json
import logging
import socket
import sys
import time
from typing import List, Tuple, Dict, Union

from PySide2.QtCore import QObject, QThread, QTimer
from PySide2.QtWidgets import QApplication

from .util import receive, strip_byte_end

logger = logging.getLogger(__name__)


def parse_splicing_packets(packet_bytes: bytes) -> List[bytes]:
    """
    处理粘包问题的函数
    :param packet_bytes:
    :return:
    """
    return packet_bytes.split(b'PMEND')


def dict_to_byte_msg(dic: Dict) -> bytes:
    b = (json.dumps(dic) + 'PMEND').encode('utf-8')
    return b


def generate_response_template() -> Dict[str, Union[str, int, Dict, List, float]]:
    payload = {'message': 'succeeded', 'content': '', 'timestamp': time.time()}
    return payload


def send_dict(sock: socket.socket, dic: Dict):
    sock.sendall(dict_to_byte_msg(dic))


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
        接收新连接.
        请求长连接的时候就把连接放到连接池中
        请求短链接的时候就直接处理。
        TODO:一眼望去圈复杂度太大，需要重构！
        """
        while True:
            try:
                sock, _ = server_socket.accept()  # 阻塞，等待客户端连接
                # 加入连接池
                conn_message = sock.recv(1024)
                conn_message = strip_byte_end(conn_message)
                try:
                    message_dic = json.loads(conn_message)
                    if message_dic.get('method') == 'start_long_connection':
                        name = message_dic.get('name')
                        if name is not None:
                            self.handle_long_connection(name, sock)
                        else:
                            response = generate_response_template()
                            response['message'] = 'failed'
                            response['content'] = 'socket name is None'
                            send_dict(sock, response)
                            logger.info('name is None, invalid request content!')
                    else:  # 如果请求的不是一个长连接，就直接进行处理，

                        response = generate_response_template()
                        response['message'] = 'succeeded'
                        response['content'] = 'connection established'
                        send_dict(sock, response)
                        b = receive(sock)

                        if len(b) <= 1000:
                            message = str(b)
                        else:
                            message = str(b[:1000])

                        t0 = time.time()
                        self.handle_packet(sock, b)
                        t1 = time.time()
                        logger.info(f"Message handled!\nThe message was:{message}\nTime elapsed {t1 - t0:f} s\n")

                except:
                    import traceback
                    traceback.print_exc()
                    logger.info('failed to decode json:%s' % str(conn_message))
                    response = generate_response_template()
                    response['message'] = 'failed'
                    response['content'] = 'invalid request json:\n%s' % str(conn_message)
                    send_dict(sock, response)
            except:
                import traceback
                traceback.print_exc()
                break

    def handle_long_connection(self, name: str, sock: socket.socket):
        """
        处理长连接请求
        :return:
        """
        if name not in self.server_obj.long_conn_sockets.keys():
            self.server_obj.long_conn_sockets[name] = sock
            response = generate_response_template()
            response['message'] = 'succeeded'
            response['content'] = 'socket connected'
            send_dict(sock, response)
        else:
            logger.info('socket named \'%s\' is already connected!' % name)
            response = generate_response_template()
            response['message'] = 'failed'
            response['content'] = 'socket name \'%s\' already connected' % name
            send_dict(sock, response)

    def handle_packet(self, client: socket.socket, packet: bytes) -> None:
        """
        处理数据包的方法
        :param client: socket.socket,要求为tcp的端口。
        :param packet: bytes
        :return:
        """
        try:
            try:
                dic = json.loads(packet)
                func = self.server_obj.dispatcher_dic[dic['method']]
                args = dic['params']
                vy = func(*args).encode('utf-8') + b'PMEND'
                client.sendall(vy)
            except json.decoder.JSONDecodeError:
                vy = json.dumps({'message': 'failed'}).encode('utf-8') + b'PMEND'
                client.sendall(vy)

        except:
            import traceback
            traceback.print_exc()
            client.close()


def init_socket(address: Tuple[str, int]):
    """
    初始化套接字
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(address)
    server_socket.listen(5)
    logger.info("服务端已启动，等待客户端连接...")
    return server_socket


class PMGServer(QObject):
    def __init__(self, address: Tuple[str, int], parent=None):
        super().__init__(parent)
        self.dispatcher_dic = {}
        self.long_conn_sockets: Dict[str, socket.socket] = {}
        self.socket = init_socket(address)
        self.server_loop_thread = QThread()
        self.loop_worker = LoopWork(self, self.socket)
        self.loop_worker.moveToThread(self.server_loop_thread)

        self.server_loop_thread.started.connect(self.loop_worker.work)
        self.server_loop_thread.start()

    def broadcast_message(self, message_dic: dict = None):
        """
        广播信息
        message:传递信息
        # 'DATA_CHANGED'
        # 'SHUT_DOWN'
        :param message_dic:要发送的信息，应该是一个可以json序列化的字典。
        :return:
        """

        if message_dic is None:
            message_dic = {'name': 'broadcast', 'message': 'Are you alive?'}
        ids = []
        logger.info('broadcast message:' + repr(message_dic))
        for k in self.long_conn_sockets.keys():
            try:
                self.long_conn_sockets[k].sendall(json.dumps(message_dic).encode('utf8') + b'PMEND')
            except ConnectionResetError:
                ids.append(k)
                logger.info('Connection \'%s\' closed!' % k)
            except:
                import traceback
                traceback.print_exc()
                ids.append(k)
        logger.info('died connections:' + repr(ids))
        for not_used_socket_name in ids:
            sock = self.long_conn_sockets.pop(not_used_socket_name)
            sock.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ADDRESS = ('127.0.0.1', 12306)  # 绑定地址
    s = PMGServer(ADDRESS)

    qtimer = QTimer()
    qtimer.start(2000)
    qtimer.timeout.connect(lambda: s.broadcast_message(None))
    sys.exit(app.exec_())
