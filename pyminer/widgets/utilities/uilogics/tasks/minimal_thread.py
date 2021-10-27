# coding=utf-8
__author__ = '侯展意'

import logging
import sys
import time

from PySide2.QtGui import QCloseEvent, QKeyEvent
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QObject, QThread, Signal, QMutex, QWaitCondition

logger = logging.getLogger(__name__)


class PMGQThreadManager(QObject):
    signal_server_message_received = Signal(dict)
    signal_data_changed = Signal(str)
    signal_finished = Signal()

    def __init__(self, parent=None, worker: QObject = None):
        super().__init__(parent)
        self.thread_recv = QThread()
        self.worker_recv = worker
        self.worker_recv.moveToThread(self.thread_recv)
        self.thread_recv.started.connect(self.worker_recv.work)
        self.thread_recv.start()
        self.thread_recv.finished.connect(self.signal_finished.emit)

    def shut_down(self):
        """
        关闭线程，并且退出。
        :return:
        """
        self.worker_recv.on_exit()
        self.thread_recv.quit()
        self.thread_recv.wait(500)


if __name__ == '__main__':
    from PySide2.QtWidgets import QTextEdit

    i = 0
    j = 0


    def work(p):
        global i, j
        j += 1
        mutex = QMutex()
        print('start')
        while (1):
            mutex.lock()
            # print(self.thread())
            # self.wait_condition.wait(self.mutex)
            # for j in range(3):
            #     print(j)
            i += 1
            p.signal_print.emit(repr(('thread:%d' % p.id, i)))
            # print('thread:%d' % p.id, i, '\n')
            p.thread().msleep(10)

            # mutex.unlock()
            if i>100:
                break
            # while(1):



    class PMGThreadWorker(QObject):
        """
        利用mutex加锁

        """
        signal_print = Signal(str)

        def __init__(self, worker_id: int):
            super(PMGThreadWorker, self).__init__()
            self.quit = False
            self.id = worker_id
            self.mutex = QMutex()
            self.wait_condition = QWaitCondition()

        def work(self):
            i = 0
            while (1):
                self.mutex.lock()
                print(self.thread())
                self.wait_condition.wait(self.mutex)
                for i in range(3):
                    self.signal_print.emit(str(self.id) + ',' + str(i + 1))
                i += 1
                if self.quit:
                    break
                self.mutex.unlock()

        def on_exit(self):
            self.quit = True
            self.wait_condition.wakeAll()

        def wake_all(self):
            self.wait_condition.wakeAll()


    class TextEdit(QTextEdit):
        def __init__(self):
            super(TextEdit, self).__init__()
            self.worker = PMGThreadWorker(1)
            self.thread_mgr = PMGQThreadManager(worker=self.worker)
            self.worker.signal_print.connect(self.append)

            self.worker2 = PMGThreadWorker(2)
            self.thread_mgr2 = PMGQThreadManager(worker=self.worker2)
            self.worker2.signal_print.connect(self.append)

        def keyPressEvent(self, event: 'QKeyEvent') -> None:
            super().keyPressEvent(event)
            self.worker.wake_all()

        def closeEvent(self, a0: 'QCloseEvent') -> None:
            super().closeEvent(a0)
            self.thread_mgr.shut_down()


    app = QApplication(sys.argv)
    textedit = TextEdit()
    textedit.show()
    sys.exit(app.exec_())
