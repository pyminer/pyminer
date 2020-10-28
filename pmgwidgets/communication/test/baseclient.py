import socket
import cloudpickle
import base64
import sys
import json


def get_style_sheet() -> str:
    return BaseClient().get_style_sheet()


class BaseClient():
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
        payload = {
            "method": "read_p",
            "params": [data_name],
            "jsonrpc": "2.0",
            "id": 0,
        }
        b = self.request_data(json.dumps(payload).encode('utf-8'))
        response_dic: dict = json.loads(b.decode('utf-8'))
        data_b64 = response_dic.get(data_name)

        if data_b64 is not None:
            s = self.load_data_from_b64(data_b64)
            return s
        return None

    def dump_data_from_b64(self, data: object) -> str:
        try:
            data_dumped_bytes = cloudpickle.dumps(data)
            return base64.b64encode(data_dumped_bytes).decode('ascii')
        except:
            pass

    def load_data_from_b64(self, data_b64: str) -> object:
        try:
            return cloudpickle.loads(base64.b64decode(data_b64))
        except:
            import traceback
            traceback.print_exc()
            return None

    def delete_var(self, var_name: list, provider: str):
        payload = {
            "method": "delete_variable",
            "params": [var_name, provider],
            "jsonrpc": "2.0",
            "id": 0,
        }
        # print('set_data', 'set_data')
        payload_byte = json.dumps(payload).encode('utf-8')
        b = self.request_data(payload_byte)
        # print('get_all_data', b)
        response_dic: dict = json.loads(b.decode('utf-8'))
        if response_dic['message'] == 'succeed':
            return response_dic['var_names']
        else:
            return []

    def get_all_public_var_names(self):
        payload = {
            "method": "get_all_public_variable_names",
            "params": [],
            "jsonrpc": "2.0",
            "id": 0,
        }
        payload_byte = json.dumps(payload).encode('utf-8')
        b = self.request_data(payload_byte)
        response_dic: dict = json.loads(b.decode('utf-8'))
        if response_dic['message'] == 'succeed':
            return response_dic['var_names']
        else:
            return []

    def get_all_var_names(self):
        payload = {
            "method": "get_all_variable_names",
            "params": [],
            "jsonrpc": "2.0",
            "id": 0,
        }
        payload_byte = json.dumps(payload).encode('utf-8')
        b = self.request_data(payload_byte)
        response_dic: dict = json.loads(b.decode('utf-8'))
        if response_dic['message'] == 'succeed':
            return response_dic['var_names']
        else:
            return []

    def set_var_dic(self, var_dic: dict, provider: str = 'server'):
        # print(var_dic)
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
        payload = {
            "method": "write_var_dic",
            "params": [dumped_data, provider],
            "jsonrpc": "2.0",
            "id": 0,
        }
        payload_byte = json.dumps(payload).encode('utf-8')
        b = self.request_data(payload_byte)
        response_dic: dict = json.loads(b.decode('utf-8'))
        return response_dic

    def get_all_vars(self):
        payload = {
            "method": "get_var_dic",
            "params": [],
            "jsonrpc": "2.0",
            "id": 0,
        }
        payload_byte = json.dumps(payload).encode('utf-8')
        b = self.request_data(payload_byte)
        response_dic: dict = json.loads(b.decode('utf-8'))
        if response_dic.get('var_dic') != None:
            b = response_dic.get('var_dic')
            return self.load_data_from_b64(b)
        else:
            return response_dic

    def set_var(self, data_name: str, data: object, provider: str = 'server'):
        """
        向数据管理类中写入数据
        :param data_name:
        :param data:
        :param provider:
        :return:
        """
        if sys.getsizeof(data) / (1024 * 1024) > 150:
            raise MemoryError('Data \'%s\' size %f MB is larger than limit ( 150MB ) .' % (
                data_name, sys.getsizeof(data) / 1024 / 1024))
        dumped_data = self.dump_data_from_b64(data)
        message = 'Data size after b64 encode %f MB is too large,it should less than 300MB after base64 encoded.\n ' % (
                sys.getsizeof(dumped_data) / 1024 / 1024)

        assert sys.getsizeof(
            dumped_data) / 1024 / 1024 <= 300, MemoryError(message)
        payload = {
            "method": "write_p",
            "params": [data_name, dumped_data, provider],
            "jsonrpc": "2.0",
            "id": 0,
        }
        payload_byte = json.dumps(payload).encode('utf-8')
        b = self.request_data(payload_byte)
        response_dic: dict = json.loads(b.decode('utf-8'))

        return response_dic

    def get_settings(self) -> dict:
        """
        获取主界面的设置项。
        :return:
        """
        payload = {
            "method": "get_settings",
            "params": [],
            "jsonrpc": "2.0",
            "id": 0,
        }
        b = self.request_data(json.dumps(payload).encode('utf-8'))
        result_dic: dict = json.loads(b.decode('utf-8')).get('settings')
        assert result_dic is not None
        return result_dic

    def get_style_sheet(self) -> str:
        """
        获取主界面的样式表
        :return:
        """
        payload = {
            "method": "get_style_sheet",
            "params": [],
            "jsonrpc": "2.0",
            "id": 0,
        }
        b = self.request_data(json.dumps(payload).encode('utf-8'))
        result = json.loads(b.decode('utf-8')).get('style_sheet')
        assert result is not None
        return result

    def request_data(self, byte_data) -> bytes:
        HOST = '127.0.0.1'
        PORT = 12306
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 定义socket类型，网络通信，TCP
        s.connect((HOST, PORT))  # 要连接的IP与端口
        s.send(b'request_data')
        msg = s.recv(1024)
        s.sendall(byte_data + b'PMEND')  # 把命令发送给对端
        l = []
        while (1):
            b = s.recv(65536)
            l.append(b)
            if b.endswith(b'PMEND'):
                # p = p.strip(b'PMEND')
                l[-1] = l[-1].strip(b'PMEND')
                break
        data = b''.join(l)  # 把接收的数据定义为变量

        s.close()  # 关闭连接
        return data
