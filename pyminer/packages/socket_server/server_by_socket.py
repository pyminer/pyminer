import json
import logging
import queue
import sys
import threading
from typing import Dict, Any

from PySide2.QtCore import Signal, QObject, QThread
from PySide2.QtWidgets import QApplication

from lib.comm.base import b64_to_dict, dict_to_b64, DataDesc, get_protocol

logger = logging.getLogger(__name__)
DATA_CHANGED = 1
SETTINGS_CHANGED = 2
INTERFACE_CALLED = 3
from flask import Flask, request

app = Flask(__name__)
message_queue: queue.Queue = queue.Queue()
extension_lib = None


@app.route('/modify_settings')
def modify_settings():
    global message_queue
    try:
        settings = request.args.get('msg')
        settings_dict = b64_to_dict(settings)
        message_queue.put((SETTINGS_CHANGED, settings_dict))
        return 'Succeeded!'
    except:
        import traceback
        traceback.print_exc()
        return "Failed!"


@app.route('/get_python_version_info')
def get_python_version_info():
    info = sys.version_info
    return json.dumps([info.major, info.minor, info.micro])


@app.route('/get_settings')
def get_settings():
    """
    获取设置
    :return:
    """
    global message_queue
    msg = "['Warning this method was deprecated']"
    logger.warning(msg)
    return msg


@app.route('/get_stylesheet')
def get_stylesheet():
    """
    获取QApplication的样式表
    Returns:

    """
    assert QApplication.instance() is not None
    return QApplication.instance().styleSheet()


@app.route('/set_data')
def modify_data_descs():
    """将工作空间中设置为data_desc型变量"""
    global message_queue
    try:
        datadesc_dict = b64_to_dict(request.args.get('msg'))
        for k, v in datadesc_dict.items():
            if not isinstance(v, DataDesc):
                raise TypeError('Data dict value should be instance of DataDesc.'
                                'However you sent key:{k},value:{v}'.format(k=k, v=v))
        message_queue.put((DATA_CHANGED, datadesc_dict))
        return json.dumps({'status': 'succeeded'})
    except TypeError as e:

        return json.dumps({'status': 'failed', 'error': str(e)})


@app.route('/interface_call')
def run_command():
    """运行命令，调用接口函数。"""
    global message_queue
    try:
        settings = request.args.get('msg')
        request_ret = request.args.get('request_ret')
        args_dict = b64_to_dict(settings)
        resp_queue = queue.Queue()
        message_queue.put(
            (INTERFACE_CALLED, args_dict, resp_queue))  # {'interface':'xxxx','method':'xxxx','kwargs':{'...':'...'}}
        if request_ret == 'True':
            response: dict = resp_queue.get(timeout=10)
            return dict_to_b64(response, protocol=get_protocol())
        else:
            return 'Succeeded!'
    except:
        import traceback
        traceback.print_exc()
        return "Failed!"


class QueueWork(QObject):
    signal_queue_recv = Signal(object)

    def __init__(self):
        global message_queue
        super(QueueWork, self).__init__()
        self.on_exit = False

    def work(self):
        global message_queue
        while True:
            if self.on_exit:
                break
            try:
                item = message_queue.get(timeout=0.05)
                self.signal_queue_recv.emit(item)
            except queue.Empty:
                pass
            except Exception as e:
                import traceback
                traceback.print_exc()

    def stop(self):
        self.on_exit = True


class PMGServer(QObject):
    extension_lib = None
    signal_data_set = Signal(dict)
    signal_data_changed = Signal(str, object, str)
    signal_data_deleted = Signal(str, str)
    signal_settings_changed = Signal(dict)

    signal_interface_called = Signal(str, str, dict, queue.Queue)  # 插件名称;接口方法名称;kwargs

    def __init__(self, parent=None):
        super().__init__(parent)
        self.queue_loop_thread = QThread()

        self.queue_worker = QueueWork()  # 队列处理

        self.queue_worker.moveToThread(self.queue_loop_thread)

        self.queue_loop_thread.started.connect(self.queue_worker.work)
        self.queue_loop_thread.start()

        self.queue_worker.signal_queue_recv.connect(self.on_recv)

        self.signal_data_set.connect(self.on_data_set)
        self.signal_settings_changed.connect(self.on_settings_changed)
        self.signal_interface_called.connect(self.on_interface_called)

    def set_extension_lib(self, extension_lib):
        self.extension_lib = extension_lib
        self.extension_lib.Signal.get_close_signal().connect(self.on_close)

    def on_recv(self, msg: object):
        """

        Args:
            msg: 收到的信息

        Returns:

        """
        if msg[0] == DATA_CHANGED:
            self.signal_data_set.emit(msg[1])
        elif msg[0] == SETTINGS_CHANGED:
            self.signal_settings_changed.emit(msg[1])
        elif msg[0] == INTERFACE_CALLED:
            self.signal_interface_called.emit(msg[1]['interface'], msg[1]['method'], msg[1]['kwargs'], msg[2])
        else:
            logger.error("received error:" + repr(object))

    def on_data_set(self, data: Dict[str, Any]):
        """
        当数据设置时的回调
        Args:
            data:

        Returns:

        """
        names = self.extension_lib.Data.get_all_variable_names()
        for name in names:
            if name not in data.keys():
                self.extension_lib.Data.delete_variable(name)
        for k, v in data.items():
            self.extension_lib.Data.set_var(k, v, provider='')

    def on_settings_changed(self, settings: Dict[str, Any]):
        """
        改变设置时的回调
        Args:
            settings:

        Returns:

        """
        for k, v in settings.items():
            self.extension_lib.Program.write_settings_item_to_file("config.ini", k, v)
        self.extension_lib.Signal.get_settings_changed_signal().emit()

    def on_interface_called(self, interface_name: str, method_name: str, kwargs: Dict, res_queue: queue.Queue):
        interface = self.extension_lib.get_interface(interface_name)
        if hasattr(interface, method_name):
            res = getattr(interface, method_name)(**kwargs)
            res_queue.put({'response': res})
        else:
            res_queue.put({'response': 'No Attribute %s' % method_name})

    def on_close(self):
        self.queue_worker.stop()
        self.queue_loop_thread.quit()
        if self.queue_loop_thread.isRunning():
            self.queue_loop_thread.wait(500)


def run_server(port: int = None, ext_lib=None):
    global server, server_thread, extension_lib
    extension_lib = ext_lib
    server = PMGServer()

    def wrapper():
        app.run(port=port)

    server_thread = threading.Thread(target=wrapper)
    server_thread.setDaemon(True)
    server_thread.start()

    return server


def run(extension_lib) -> Flask:
    server = run_server(12306, extension_lib)
    server.set_extension_lib(extension_lib)
    return server


if __name__ == "__main__":
    import cgitb

    cgitb.enable()
    qt_app = QApplication(sys.argv)
    run_server()
    qt_app.exec_()
