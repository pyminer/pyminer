#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2020/8/24
@author: Irony
@email: 892768447@qq.com
@file: consolewidget
@description: Console Widget
"""
import os
import dill as pickle
import base64

from PyQt5.QtCore import QObject, pyqtSignal, QThread, QWaitCondition, QMutex, QTimer
from PyQt5.QtGui import QTextCursor, QFontMetrics
from PyQt5.QtWidgets import QMessageBox
from qtconsole.manager import QtKernelManager
from qtconsole.rich_jupyter_widget import RichJupyterWidget


class ConsoleInitThread(QObject):
    initialized = pyqtSignal(object, object)

    def __init__(self, *args, **kwargs):
        super(ConsoleInitThread, self).__init__(*args, **kwargs)
        self.mutex = QMutex()
        self.wait_condition = QWaitCondition()

    def run(self):
        self.mutex.lock()
        kernel_manager = QtKernelManager(kernel_name='python3')
        kernel_manager.start_kernel()

        kernel_client = kernel_manager.client()
        kernel_client.start_channels()

        # notify to update ui
        self.initialized.emit(kernel_manager, kernel_client)

        # wait for exit
        self.wait_condition.wait(self.mutex)
        self.mutex.unlock()

        # stop channels and kernel
        kernel_client.stop_channels()
        kernel_manager.shutdown_kernel()

    def stop(self):
        self.wait_condition.wakeAll()


class ConsoleWidget(RichJupyterWidget):

    def __init__(self, *args, **kwargs):
        super(ConsoleWidget, self).__init__(*args, **kwargs)
        self.is_first_execution = True
        self.confirm_restart = False
        self.commands_pool = []
    
    def _handle_kernel_died(self, since_last_heartbit):
        self.is_first_execution = True
        self.restart_kernel(None, True)
        self.initialize_ipython_builtins()
        self.execute_command('')
        return True

    def _handle_execute_input(self, msg):
        super()._handle_execute_result(msg)

    def setup_ui(self):
        self.kernel_manager = None
        self.kernel_client = None
        # initialize by thread
        self.init_thread = QThread(self)
        self.console_object = ConsoleInitThread()
        self.console_object.moveToThread(self.init_thread)
        self.console_object.initialized.connect(self.slot_initialized)
        self.init_thread.finished.connect(self.console_object.deleteLater)
        self.init_thread.finished.connect(self.init_thread.deleteLater)
        self.init_thread.started.connect(self.console_object.run)
        self.init_thread.start()
        cursor: QTextCursor = self._prompt_cursor
        cursor.movePosition(QTextCursor.End)

    def connect_to_datamanager(self, data_manager):
        self.data_manager = data_manager
        self.lib = self.data_manager

    def slot_initialized(self, kernel_manager, kernel_client):
        """
        Args:
            kernel_manager: `qtconsole.manager.QtKernelManager`
            kernel_client: `qtconsole.manager.QtKernelManager.client`

        Returns:
        """
        self.kernel_manager = kernel_manager
        self.kernel_client = kernel_client
        self.initialize_ipython_builtins()

    def initialize_ipython_builtins(self):
        ini_py = os.path.join(self.lib.get_main_program_dir(), 'extensions', 'packages'
                              , 'ipython_console', 'initialisation.py')
        self.execute_file(ini_py, hidden=True)
        for source, hidden, hint_text in self.commands_pool:
            self.execute_command(source, hidden, hint_text)

    def _update_list(self):
        try:
            super(ConsoleWidget, self)._update_list()
        except:
            import traceback
            traceback.print_exc()

    def _handle_complete_reply(self, msg):
        '''
        重写，加上trycatch，直接禁用了没有其他的变化，故不做类型标注。
        :param msg:
        :return:
        '''
        try:
            super()._handle_complete_reply(msg)
        except:
            import traceback
            traceback.print_exc()

    def _banner_default(self):
        """
        自定义控制台开始的文字
        Returns:
        """
        return 'PyMiner\n'

    def closeEvent(self, event):
        if self.init_thread.isRunning():
            self.console_object.stop()
            self.init_thread.quit()
            self.init_thread.wait(500)
        super(ConsoleWidget, self).closeEvent(event)

    def execute_file(self, file: str, hidden: bool = False):
        if not os.path.exists(file) or not file.endswith('.py'):
            raise FileNotFoundError(f'{file} not found or invalid')
        base = os.path.basename(file)
        cmd = os.path.splitext(base)[0]
        with open(file, 'r', encoding='utf-8') as f:
            source = f.read()
        self.execute_command(source, hidden=hidden, hint_text=cmd)

    def execute_command(self, source, hidden: bool = False, hint_text: str = ''):
        '''

        :param source:
        :param hidden:
        :param hint_text: 运行代码前显示的提示
        :return:
        '''
        cursor: QTextCursor = self._prompt_cursor
        cursor.movePosition(QTextCursor.End)
        cursor.insertText('%s\n'%hint_text)
        cursor.movePosition(QTextCursor.End)
        if self.kernel_client is None:
            self.commands_pool.append((source, hidden, hint_text))
        else:
            self._execute(source, hidden)

    def _handle_stream(self, msg):
        cursor: QTextCursor = self._prompt_cursor
        cursor.movePosition(QTextCursor.End)
        msg_lines = msg['content']['text'].strip().split('\n')
        data_b64 = msg_lines[-1]
        try:
            data_b64_dic = pickle.loads(base64.b64decode(data_b64))  # got data
        except:
            pass
        else:
            msg['content']['text'] = '\n'.join(msg_lines[:-1])
            data = {}
            for key in data_b64_dic:
                var = data_b64_dic[key]
                try:
                    data[key] = pickle.loads(base64.b64decode(data_b64_dic[key]))
                except:
                    import traceback
                    traceback.print_exc()
            data = {k: v for k, v in data.items() if k not in self.data or str(self.data[k]) != str(v)}
            try:
                self.data_manager.set_var_dict(data, 'ipython')
            except Exception as e:
                msg['content']['text'] += f'\n{type(e).__name__}: {e}'
        super()._handle_stream(msg)

    def append_stream(self, text):
        """重写的方法。原本before_prompt属性是False。"""
        self._append_plain_text(text, before_prompt=False)

    def _execute(self, source: str, hidden: bool = False):
        if not self.is_source_code_legal(source):
            QMessageBox.warning(self,'警告','命令\n\"%s\"\n为无效命令。'%source)
            return
        if self.is_first_execution:
            self.is_first_execution = False
        else:
            self.data = self.data_manager.get_all_var()  # send data
            data_b64_dic = {}
            for key in self.data:
                var = self.data[key]
                try:
                    data_b64_dic[key] = base64.b64encode(pickle.dumps(var)).decode('ascii')
                except:
                    import traceback
                    traceback.print_exc()
            data_b64 = base64.b64encode(pickle.dumps(data_b64_dic)).decode('ascii')
            source = f'__inject("{data_b64}")\n{source}'
        super()._execute(source, hidden)

    def is_source_code_legal(self, source_code:str)->bool:
        '''
        判断注入到shell的命令是否合法，不合法的话，就避免执行这个函数。
        :param source_code:
        :return:
        '''
        s= source_code.strip()
        s= s.split('(')[0]
        # if s in self.illegal_commands:
        #     return False
        return True




if __name__ == '__main__':
    import sys
    import cgitb

    cgitb.enable(format='text')
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    w = ConsoleWidget()
    w.show()
    w.setup_ui()

    sys.exit(app.exec_())
