# coding=utf-8
__author__ = '侯展意'

import logging
import sys
import time
from typing import Callable, Tuple

from PySide2.QtGui import QCloseEvent
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QObject, Signal

logger = logging.getLogger(__name__)
from widgets.utilities.uilogics.tasks.minimal_thread import PMGQThreadManager


class PMGOneShotWorker(QObject):
    signal_finished = Signal(object)

    def __init__(self, work_fcn: Callable, args: Tuple = None):
        super(PMGOneShotWorker, self).__init__()
        self.quit = False
        self.args = args
        self.work_fcn: Callable = work_fcn

    def work(self):
        assert callable(self.work_fcn)
        if self.args is not None:
            assert isinstance(self.args, (tuple, list))
            ret = self.work_fcn(*self.args)
        else:
            ret = self.work_fcn()
        self.signal_finished.emit(ret)

    def on_exit(self):
        pass


class PMGOneShotThreadRunner(QObject):

    signal_finished = Signal(object)

    def __init__(self, callback: Callable, args=None):
        """
        Attension: Do not do UI operations in the callback.If callback contains operations for refresh UI, this method might
        cause segmentation fault.

        Args:
            callback: 传入函数对象
            args: 传入函数的参数，默认值为None。应当以元组形式依次传入。如果为None则不对函数传入参数。
        """

        super().__init__()
        self.worker = PMGOneShotWorker(callback, args)
        self.thread_mgr = PMGQThreadManager(worker=self.worker)
        self.worker.signal_finished.connect(self.slot_signal_finished)

    def slot_signal_finished(self, obj):
        """
        When the single shot finished,this slot method will instantly be called.


        Args:
            obj:

        Returns:

        """
        self.signal_finished.emit(obj)
        self.worker.thread().quit()
        self.worker.thread().wait(500)

    def is_running(self):
        return self.worker.thread().isRunning()

if __name__ == '__main__':
    from PySide2.QtWidgets import QTextEdit


    def run(loop_times):
        for i in range(loop_times):
            print(i)
            time.sleep(1)
        return 'finished!!', 'aaaaaa', ['finished', 123]


    class TextEdit(QTextEdit):
        def __init__(self):
            super(TextEdit, self).__init__()
            self.oneshot = PMGOneShotThreadRunner(run, args=(5,))
            self.oneshot.signal_finished.connect(self.on_finished)

        def on_finished(self, obj):
            self.append(repr(obj))

        def closeEvent(self, a0: 'QCloseEvent') -> None:
            super().closeEvent(a0)


    app = QApplication(sys.argv)
    textedit = TextEdit()
    textedit.show()
    sys.exit(app.exec_())
