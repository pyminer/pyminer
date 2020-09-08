#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2020/8/24
@author: Irony
@email: 892768447@qq.com
@file: consolewidget
@description: Console Widget
"""
from PyQt5.QtCore import QObject, pyqtSignal, QThread, QWaitCondition, QMutex
from PyQt5.QtGui import QTextCursor
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
        kernel_manager = QtKernelManager(kernel_name="""python3""")
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

    def slot_initialized(self, kernel_manager, kernel_client):
        """
        Args:
            kernel_manager: `qtconsole.manager.QtKernelManager`
            kernel_client: `qtconsole.manager.QtKernelManager.client`

        Returns:
        """
        self.kernel_manager = kernel_manager
        self.kernel_client = kernel_client

    def _banner_default(self):
        """
        自定义控制台开始的文字
        Returns:
        """
        return """PyMiner\n"""

    def closeEvent(self, event):
        if self.init_thread.isRunning():
            self.console_object.stop()
            self.init_thread.quit()
            self.init_thread.wait(500)
        super(ConsoleWidget, self).closeEvent(event)

    def execute_command(self, source, hidden: bool = False,
                        hint_text: str = ''):
        """

        :param source:
        :param hidden:
        :param hint_text: 运行代码前显示的提示
        :return:
        """
        cursor: QTextCursor = self._prompt_cursor
        cursor.movePosition(QTextCursor.End)
        cursor.insertText("""running\n""")
        cursor.movePosition(QTextCursor.End)
        self._execute(source, hidden)

    def _handle_stream(self, msg):
        cursor: QTextCursor = self._prompt_cursor
        cursor.movePosition(QTextCursor.End)

        super()._handle_stream(msg)
        pass

    def append_stream(self, text):
        """重写的方法。原本before_prompt属性是False。"""
        self._append_plain_text(text, before_prompt=False)


if __name__ == """__main__""":
    import sys
    import cgitb

    cgitb.enable(format="""text""")
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    w = ConsoleWidget()
    w.show()
    w.setup_ui()

    sys.exit(app.exec_())
