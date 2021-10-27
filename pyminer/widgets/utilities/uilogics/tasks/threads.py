# coding=utf-8
__author__ = '侯展意'

import logging
import sys
import time
from typing import Callable

logger = logging.getLogger(__name__)

from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QObject, QThread, Signal


class PMGThreadWorker(QObject):
    def __init__(self):
        super(PMGThreadWorker, self).__init__()
        self.quit = False
        self.work_loop_fcn = None
        self.on_exit_fcn = None

    def work(self):
        while (1):
            self.work_loop_fcn()
            if self.quit:
                break
        # self.thread().quit()

    def on_exit(self):
        if callable(self.on_exit_fcn):
            self.on_exit_fcn()
        self.quit = True


class PMQThreadObject(QObject):
    signal_server_message_received = Signal(dict)
    signal_data_changed = Signal(str)

    def __init__(self, parent=None, worker: QObject = None):
        super().__init__(parent)
        self.thread = QThread()
        self.worker = worker
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.work)  # self.worker_recv.work)
        self.thread.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()

    def terminate(self):
        logger.info('client quit')
        self.worker.on_exit()

        self.thread.quit()
        self.thread.wait(500)


class PMQThreadManager(QObject):
    signal_server_message_received = Signal(dict)
    signal_data_changed = Signal(str)

    def __init__(self, parent=None, work_fcn: Callable = None, loop_fcn: Callable = None, exit_fcn: Callable = None):
        super().__init__(parent)
        self.thread_recv = QThread()
        self.worker_recv = PMGThreadWorker()

        if work_fcn is not None and loop_fcn is not None:
            raise ValueError('work_fcn and loop_fcn cannot be both not None at the same time!')
        if work_fcn is not None:
            self.worker_recv.work = work_fcn
        else:
            self.worker_recv.work_loop_fcn = loop_fcn
        self.worker_recv.moveToThread(self.thread_recv)
        self.thread_recv.started.connect(self.worker_recv.work)  # self.worker_recv.work)
        self.worker_recv.on_exit_fcn = exit_fcn
        self.thread_recv.start()

    def shut_down(self):
        logger.info('client quit')
        self.worker_recv.on_exit()
        # self.worker_recv.close_socket()
        self.thread_recv.quit()
        self.thread_recv.wait(500)


if __name__ == '__main__':
    from PySide2.QtWidgets import QTextEdit


    def loop():
        print(123)
        time.sleep(0.4)


    def exit():
        print('thread exits!')

    class TextEdit(QTextEdit):
        def __init__(self):
            super(TextEdit, self).__init__()
            self.thread_mgr = PMQThreadManager()

    app = QApplication(sys.argv)
    textedit = QTextEdit()
    textedit.show()
    c = PMQThreadManager(loop_fcn=loop, exit_fcn=exit)
    time.sleep(2)
    c.shut_down()
    sys.exit(app.exec_())
