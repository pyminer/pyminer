import json
import time
import socket
import logging
import warnings
from typing import Dict, Union, List

logger = logging.getLogger(__name__)


def strip_byte_end(bytestream):
    if bytestream.endswith(b'PMEND'):
        return bytestream[: -5]
    else:
        return bytestream


def generate_client_payload() -> Dict[str, Union[str, Dict, List]]:
    """
    生成Client的消息模板
    :return:
    """
    payload = {'timestamp': time.time(),
               'name': 'Anonymous Client',
               'contents': ''
               }
    return payload


def generate_server_payload() -> Dict[str, Union[str, Dict, List]]:
    """
    生成服务器消息模板
    :return:
    """
    payload = {'message': 'succeeded',  # 还有failed
               'timestamp': time.time()
               }
    return payload


def send_dict(sock: socket.socket, dict_to_send: Dict) -> None:
    """
    发送一个字典
    :param sock:
    :param dict_to_send:
    :return:
    """
    content = (json.dumps(dict_to_send) + 'PMEND').encode('utf-8')
    sock.sendall(content)


def receive(socket_obj: socket.socket) -> bytes:
    recv_list = []
    empty_loops = 0
    while (1):
        try:
            b = socket_obj.recv(1024)
            if b == b'':
                empty_loops += 1
                if empty_loops > 1000:
                    raise ValueError('Too much empty values received!All received was:' + repr(recv_list))
            else:
                empty_loops = 0
                recv_list.append(b)
                if len(recv_list) >= 2:
                    if (recv_list[-2] + b).endswith(b'PMEND'):
                        recv_list[-2] = recv_list[-2] + recv_list[-1]
                        recv_list.pop()
                        recv_list[-1] = strip_byte_end(recv_list[-1])
                        break
                else:
                    if b.endswith(b'PMEND'):
                        recv_list[-1] = strip_byte_end(recv_list[-1])
                        break


        except ConnectionAbortedError:
            warnings.warn('Connection terminated.')
            return b''
        except:
            import traceback
            traceback.print_exc()
            return b''

    return b''.join(recv_list)


def timeit(func):
    def wrapper(*args, **kwargs):
        t0 = time.time()
        r = func(*args, **kwargs)
        logger.debug('time_elapsed', time.time() - t0)
        return r

    return wrapper
