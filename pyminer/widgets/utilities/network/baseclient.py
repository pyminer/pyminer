import base64
import json
import socket
import sys
import time
from typing import List, Union, Dict, Any

import cloudpickle

from widgets.utilities.network.util import generate_client_payload, strip_byte_end


def get_style_sheet() -> str:
    return BaseClient().get_style_sheet()


class BaseClient(object):
    def __init__(self, name='Anonymous BaseClient'):
        self.name = name

    def init_socket(self, port: int = 12306):
        host = 'localhost'
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)  # 在客户端开启心跳维护
        client.connect((host, port))
        return client

    def get_var(self, data_name: str):
        """
        从工作空间获取数据
        :param data_name:
        :return:
        """
        payload = self.generate_request_template()
        payload['method'] = 'read_p'
        payload['params'] = [data_name]

        response_dic = self.send_dict_and_get_request_dict(payload)
        if response_dic.get('message') == 'succeeded':
            data_b64 = response_dic.get(data_name)
            s = self.load_data_from_b64(data_b64)
            return s
        else:
            raise ValueError(response_dic.get('message'))

    def dump_data_from_b64(self, data: Any) -> str:
        try:
            data_dumped_bytes = cloudpickle.dumps(data)
            return base64.b64encode(data_dumped_bytes).decode('ascii')
        except:
            return ''

    def load_data_from_b64(self, data_b64: str) -> object:
        try:
            return cloudpickle.loads(base64.b64decode(data_b64))
        except:
            import traceback
            traceback.print_exc()
            return None

    def delete_var(self, var_name: Union[str, List[str]], provider: str):
        payload = self.generate_request_template()
        payload['method'] = 'delete_variable'
        payload['params'] = [var_name, provider]
        response_dic = self.send_dict_and_get_request_dict(payload)
        if response_dic['message'] == 'succeeded':
            return response_dic['var_name']
        else:
            return []

    def get_all_public_var_names(self):
        """
        获取所有的可由外部获取的变量
        :return:
        """

        payload = self.generate_request_template()
        payload['method'] = 'get_all_public_variable_names'
        payload['params'] = []
        response_dic = self.send_dict_and_get_request_dict(payload)
        if response_dic['message'] == 'succeeded':
            return response_dic['var_names']
        else:
            return []

    def get_all_var_names(self):
        """
        获取所有的变量名称
        :return:
        """
        payload = self.generate_request_template()
        payload['method'] = 'get_all_variable_names'
        payload['params'] = []
        response_dic = self.send_dict_and_get_request_dict(payload)
        if response_dic['message'] == 'succeeded':
            return response_dic['var_names']
        else:
            return []

    def set_var_dic(self, var_dic: dict, provider: str = 'server'):
        """
        设置种类
        :param var_dic:
        :param provider:
        :return:
        """
        t0 = time.time()
        dic = {}
        for k in var_dic.keys():
            try:
                b64 = self.dump_data_from_b64(var_dic[k])
                dic[k] = b64
            except:
                import traceback
                traceback.print_exc()
                pass
        dumped_data = self.dump_data_from_b64(dic)
        payload = self.generate_request_template()
        payload['method'] = 'write_var_dic'
        payload['params'] = [dumped_data, provider]
        t2 = time.time()
        response_dic = self.send_dict_and_get_request_dict(payload)
        t1 = time.time()
        # print('set variable dict time elapsed %f s, with transfering consumed %f s.' % (t1 - t0, t1 - t2))
        return response_dic

    def get_all_vars(self):
        # print('set variable dict time elapsed %f' % (t1 - t0))
        payload = self.generate_request_template()
        payload['method'] = 'get_var_dic'
        payload['params'] = []
        response_dic = self.send_dict_and_get_request_dict(payload)
        if response_dic.get('var_dic') is not None:
            b = response_dic.get('var_dic')
            return self.load_data_from_b64(b)
        else:
            return response_dic

    def get_vars(self, var_names: str):
        payload = self.generate_request_template()
        payload['method'] = 'get_vars'
        payload['params'] = [var_names]
        response_dic = self.send_dict_and_get_request_dict(payload)
        if response_dic.get('var_dic') is not None:
            b = response_dic.get('var_dic')
            return self.load_data_from_b64(b)
        else:
            return response_dic
        return

    def get_all_var_names_of_type(self, type: str):
        """
        获取一定类型的数据。
        :param type:
        :return:
        """
        assert type in ['string', 'array', 'table', 'numeric']
        payload = self.generate_request_template()
        payload['method'] = 'get_all_var_names_of_type'
        payload['params'] = [type]
        response_dic = self.send_dict_and_get_request_dict(payload)
        if response_dic.get('message') == 'succeeded':
            b = response_dic.get('var_names')
            return self.load_data_from_b64(b)
        else:
            return []

    def set_var(self, data_name: str, data: Any, provider: str = 'server'):
        """
        向数据管理类中写入数据
        Args:
            data_name:
            data:
            provider:

        Returns:

        """
        if sys.getsizeof(data) / (1024 * 1024) > 150:
            raise MemoryError('Data \'%s\' size %f MB is larger than limit ( 150MB ) .' % (
                data_name, sys.getsizeof(data) / 1024 / 1024))
        dumped_data = self.dump_data_from_b64(data)
        message = 'Data size after b64 encode %f MB is too large,it should less than 300MB after base64 encoded.\n ' % (
                sys.getsizeof(dumped_data) / 1024 / 1024)

        assert sys.getsizeof(
            dumped_data) / 1024 / 1024 <= 300, MemoryError(message)

        payload = self.generate_request_template()
        payload['method'] = 'write_p'
        payload['params'] = [data_name, dumped_data, provider]
        response_dic = self.send_dict_and_get_request_dict(payload)
        return response_dic

    def get_settings(self) -> dict:
        """
        获取主界面的设置项。
        :return:
        """
        payload = self.generate_request_template()
        payload['method'] = 'get_settings'
        payload['params'] = []
        result_dic = self.send_dict_and_get_request_dict(payload)
        assert result_dic is not None
        return result_dic

    def set_settings_param(self, param_name: str, param_val: Any):
        payload = self.generate_request_template()
        payload['method'] = 'set_settings_param'
        payload['params'] = [param_name, param_val]
        result_dic = self.send_dict_and_get_request_dict(payload)
        assert result_dic is not None
        return result_dic

    def get_style_sheet(self) -> str:
        """
        获取主界面的样式表
        :return:
        """
        payload = self.generate_request_template()
        payload['method'] = 'get_style_sheet'
        payload['params'] = []
        result = self.send_dict_and_get_request_dict(payload).get('style_sheet')
        assert result is not None
        return result

    def request_data(self, byte_data) -> bytes:
        HOST = '127.0.0.1'
        PORT = 12306
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 定义socket类型，网络通信，TCP
        s.settimeout(5)
        s.connect((HOST, PORT))  # 要连接的IP与端口
        payload = self.generate_request_template()
        payload['method'] = 'request_data'
        s.send(json.dumps(payload).encode('utf-8'))
        msg = s.recv(1024)
        s.sendall(byte_data + b'PMEND')  # 把命令发送给对端
        recv_list = []
        while (1):
            b = s.recv(65536)
            recv_list.append(b)
            if b.endswith(b'PMEND'):
                recv_list[-1] = strip_byte_end(recv_list[-1])
                break
        data = b''.join(recv_list)  # 把接收的数据定义为变量

        s.close()  # 关闭连接
        return data

    def generate_request_template(self) -> Dict[str, Union[List, str]]:
        template = generate_client_payload()
        template['name'] = self.name
        return template

    def send_dict_and_get_request_dict(self, dict_to_send: Dict) -> Dict[str, Union[Dict, List, str, float, int]]:
        try:
            dict_byte = json.dumps(dict_to_send).encode('utf-8')
            data_byte = self.request_data(dict_byte)
            return json.loads(data_byte)
        except TypeError:
            import traceback
            traceback.print_exc()
            raise TypeError(
                'Cannot dump this object \'%s\' due to its type cannot be json serialized.' % repr(dict_to_send))
        except json.decoder.JSONDecodeError:
            import traceback
            traceback.print_exc()
            raise ValueError('Cannot decode this json: \'%s\'' % str(data_byte))
        except ConnectionRefusedError:
            raise ConnectionRefusedError('Connection Refused!')
        except:
            import traceback
            traceback.print_exc()


if __name__ == '__main__':
    import numpy as np

    dic = {
        'a': np.ndarray([200, 200]),
        'b': np.ndarray([200, 200]),
        'c': np.ndarray([200, 200]),
    }
    t0 = time.time()
    bc = BaseClient()
    a = bc.set_var_dic(dic)
    # s = bc.get_all_var_names_of_type('table')
    t1 = time.time()
    print(t1 - t0)
