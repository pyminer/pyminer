import sys
import json
import time

from PyQt5.QtCore import pyqtSignal, QTimer
from pmgwidgets.communication.test.server_long_conn import PMGServer
import cloudpickle
import base64
import numpy
import pandas
import logging

logger = logging.getLogger(__name__)


class PMServer(PMGServer):
    extension_lib = None
    signal_data_changed = pyqtSignal(str, object, str)

    def __init__(self, port: int, extension_lib):

        super().__init__(address=('127.0.0.1', port))
        self.extension_lib = extension_lib
        self.dispatcher_dic = {'read_p': self.read_pickle_data,
                               'write_p': self.set_pickle_data,
                               'get_settings': self.get_settings,
                               'set_settings_param': self.set_settings_param,
                               'get_style_sheet': self.get_style_sheet,
                               'get_all_variable_names': self.get_all_data_names,
                               'get_all_public_variable_names':self.get_all_public_data_names,
                               'write_var_dic': self.update_pickle_data_dict,
                               'get_var_dic': self.get_var_dic,
                               'delete_variable': self.delete_variable}
        self.signal_data_changed.connect(self.on_data_changed)
        self.qtimer = QTimer()
        self.qtimer.start(10000)
        self.qtimer.timeout.connect(self.broadcast_message)
        self.extension_lib.Data.add_data_changed_callback(
            lambda data_name, data_value, source: self.broadcast_message({'name': 'broadcast',
                                                                          'message': 'data_changed',
                                                                          'data_name': data_name,
                                                                          'data_source': source}))

    def get_var_dic(self):
        """
        返回全部非内置变量字典
        :return:
        """
        d = self.extension_lib.Data.get_all_variables()
        dic = {
            k: v for k, v in d.items() if not getattr(v, 'type', '') == 'Type'}
        data_b64 = self.pickle_encode_object(dic)
        return json.dumps({'message': 'succeeded', 'var_dic': data_b64})

    def delete_variable(self, var_name, provider: list = 'unknown'):
        """
        删除变量
        :param var_name:变量名
        :return:
        """
        try:
            self.extension_lib.Data.delete_variable(var_name, provider=provider)
        except:
            import traceback
            traceback.print_exc()
        return json.dumps({'message': 'succeeded', 'var_name': var_name, 'data_source': provider})

    def get_all_data_names(self):
        """
        获取所有的变量的名称
        :return:
        """

        var_names = self.extension_lib.Data.get_all_variable_names()
        return json.dumps({'var_names': var_names, 'message': 'succeed'})

    def get_all_public_data_names(self):
        """
        获取所有可访问的变量的名称
        :return:
        """

        var_names = self.extension_lib.Data.get_all_public_variable_names()
        return json.dumps({'var_names': var_names, 'message': 'succeed'})

    def get_style_sheet(self):
        """
        获取程序的样式表
        :return:
        """
        from PyQt5.QtWidgets import QApplication
        return json.dumps({'style_sheet': QApplication.instance().styleSheet(), 'message': 'succeed'})


    def set_settings_param(self, param_name, param_val: object):
        """
        改变设置
        :param param_name: 设置项名称
        :param param_val: 设置项值
        :return:
        """
        if param_name in self.extension_lib.Program.get_settings().keys():

            self.extension_lib.Program.get_settings()[param_name] = param_val
        else:
            raise ValueError('Parameter name \'%s\' not in settings!' % param_name)

    def get_settings(self):
        return json.dumps({'message': 'succeed', 'settings': self.extension_lib.Program.get_settings()})

    @staticmethod
    def pickle_decode_object(data_b64: str) -> object:
        try:
            result = cloudpickle.loads(base64.b64decode(data_b64))
            return result
        except:
            import traceback
            traceback.print_exc()
            return None

    def pickle_encode_object(self, obj) -> str:
        data_seq = cloudpickle.dumps(obj)
        return base64.b64encode(data_seq).decode('ascii')

    def read_data(self, var_name: str) -> bytes:
        return var_name.encode('utf-8')

    def read_pickle_data(self, var_name: str) -> str:
        try:
            data = self.extension_lib.get_var(var_name)
            assert sys.getsizeof(data) / (1024 ** 2) < 150
            data_b64 = self.pickle_encode_object(data)
            assert sys.getsizeof(data_b64) / (1024 ** 2) < 300
            response = json.dumps({var_name: data_b64, 'message': 'success'})
            return response
        except:
            pass
        return '{"message": "variable %s not found!"}' % var_name

    def set_pickle_data(self, var_name: str, data_b64: str, provider: str = 'server'):
        t0 = time.time()
        data = PMServer.pickle_decode_object(data_b64)
        t1 = time.time()
        logger.warning('pickle_decode_time:%f' % (t1 - t0))
        if data is not None:
            self.signal_data_changed.emit(var_name, data, provider)
            return json.dumps({"message": 'success'})
        return '{"message":"failed"}'

    def update_pickle_data_dict(self, data_dict_b64, provider: str = 'server'):
        t0 = time.time()
        data_b64_dic: dict = PMServer.pickle_decode_object(data_dict_b64)
        t1 = time.time()
        logger.warning('pickle_decode_time:%f' % (t1 - t0))
        if data_b64_dic is not None:
            for k in data_b64_dic.keys():
                data = PMServer.pickle_decode_object(data_b64_dic[k])
                self.signal_data_changed.emit(k, data, provider)
            return json.dumps({"message": 'success'})
        return '{"message":"failed"}'

    def on_data_changed(self, data_name, data, provider: str):
        self.extension_lib.set_var(data_name, data, provider)

    def shutdown(self):
        """
        关闭服务器
        :return:
        """
        self.loop_worker.server_socket.close()
        self.server_loop_thread.quit()
        self.server_loop_thread.wait(500)


def run_server(port: int, extension_lib):
    global server
    server = PMServer(port, extension_lib)
    extension_lib.Signal.get_close_signal().connect(server.shutdown)


def run(extension_lib):
    run_server(12306, extension_lib)
