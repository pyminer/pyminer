# coding=utf-8
__author__ = '侯展意'

import logging
import sys
import time
from typing import Callable, Tuple, Iterable
# from collections import Iterable
from PySide2.QtGui import QCloseEvent
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QObject, Signal

logger = logging.getLogger(__name__)
from widgets.utilities.uilogics.tasks.minimal_thread import PMGQThreadManager


class PMGEndlessLoopWorker(QObject):
    """
    在循环中工作。
    输入参数：单步工作函数；参数（可迭代对象）。
    """
    signal_step_finished = Signal(object)
    signal_finished = Signal()

    def __init__(self, work_fcn: Callable, args: Iterable = None):
        super(PMGEndlessLoopWorker, self).__init__()
        self.quit = False
        self.args = args if args is not None else []
        self.work_fcn: Callable = work_fcn

    def work(self):
        assert callable(self.work_fcn)

        while (1):
            step_ret = self.work_fcn(*self.args)
            self.signal_step_finished.emit(step_ret)
            if self.quit:
                break
        self.signal_finished.emit()

    def on_exit(self):
        self.quit = True


class PMGLoopWorker(QObject):
    signal_step_finished = Signal(int, object)
    signal_finished = Signal()

    def __init__(self, work_fcn: Callable, iter_args: Iterable = None, loop_times: int = 100,
                 step_args: Iterable = None):
        """
        在循环中工作。
        第一种方法可以传入可迭代对象作为 iter_args 参数，循环次数就是 iter_args 的长度。此种情况下loop_times和step_args无效。
        第二种方法，当iter_args为None的时候，传入循环次数loop_times作为参数，每一步分别的参数由step_args传入。
        输入参数：单步工作函数；参数（可迭代对象）。
        注意：传入的callback函数不得在其中直接刷新UI（比如，调用文本框的setText方法），否则可能出现段错误。段错误会立即导致界面崩溃，且不可使用try...catch...或者cgitb等手段进行处理！
        Args:
            work_fcn:
            iter_args:
            loop_times:
            step_args:

        """
        super(PMGLoopWorker, self).__init__()
        self.quit = False

        self.iter_args = iter_args if iter_args is not None else [([] if step_args is None else step_args) for i in
                                                                  range(loop_times)]
        self.work_fcn: Callable = work_fcn

    def work(self):
        assert callable(self.work_fcn)
        assert self.iter_args is not None
        for i, step_args in enumerate(self.iter_args):
            step_ret = self.work_fcn(*step_args)
            self.signal_step_finished.emit(i, step_ret)
        self.signal_finished.emit()

    def on_exit(self):
        self.quit = True


class PMGLoopThreadRunner(QObject):
    signal_finished = Signal()
    signal_step_finished = Signal(int, object)

    def __init__(self, callback: Callable, iter_args: Iterable = None, loop_times: int = 100,
                 step_args: Iterable = None):
        """
        连续执行有限多次回调函数callback。函数每执行一次，会发出含两个参数（参数依次为“当前步数”和“callback的返回值”）的信号`signal_step_finished`。
        第一种方法可以传入可迭代对象作为`iter_args`参数，循环次数就是 `iter_args` 的长度。此种情况下`loop_times`和`step_args`无效。
        第二种方法，当`iter_args`为`None`的时候，传入循环次数`loop_times`作为参数，此时每步的参数是相同的，均有参数`step_args`传入。

        如果函数有多个返回值，则信号`signal_step_finished`的参数为：<整数，元组>。第二个参数是一个元组，依次包含callback各个返回参数。
        Args:
            callback: 回调函数。函数每执行一次，信号`signal_step_finished`将发出。
            iter_args:循环每一步需要输入的参数
            loop_times:循环次数
            step_args:所有步相同的参数
                注意：传入的callback函数不得在其中直接刷新UI（比如，调用文本框的setText方法），否则可能出现段错误。
            段错误会立即导致界面崩溃，且无法使用try...catch...或者cgitb等手段进行处理！
            
        """
        super().__init__()
        self.worker = PMGLoopWorker(callback, iter_args, loop_times, step_args)
        self.thread_mgr = PMGQThreadManager(worker=self.worker)
        self.worker.signal_step_finished.connect(self.signal_step_finished.emit)
        self.worker.signal_finished.connect(self.signal_finished.emit)


class PMGEndlessLoopThreadRunner(QObject):
    signal_finished = Signal()
    signal_step_finished = Signal(object)

    def __init__(self, callback: Callable, args: Iterable = None):
        """
        连续执行无限多次回调函数callback。函数每执行一次，将发出参数为callback返回值的信号`signal_step_finished`。
        如果函数有多个返回值，则信号`signal_step_finished`的参数为一个元组，依次包含各个返回参数。
        Args:
            callback: 回调函数。函数每执行一次，信号`signal_step_finished`将发出，信号只有一个参数，也就是我们输入的callback的返回值。
            args:
                注意：传入的callback函数不得在其中直接刷新UI（比如，调用文本框的setText方法），否则可能出现段错误。
            段错误会立即导致界面崩溃，且无法使用try...catch...或者cgitb等手段进行处理！
            
        """
        super().__init__()
        self.worker = PMGEndlessLoopWorker(callback, args=args)
        self.thread_mgr = PMGQThreadManager(worker=self.worker)
        self.worker.signal_step_finished.connect(self.signal_step_finished.emit)
        self.worker.signal_finished.connect(self.signal_finished.emit)

    def is_running(self) -> bool:
        return self.worker.thread().isRunning()

    def shut_down(self):
        self.thread_mgr.shut_down()


if __name__ == '__main__':
    from PySide2.QtWidgets import QTextEdit


    def run(i, j):
        time.sleep(0.1)
        return i + j


    class TextEdit(QTextEdit):
        def __init__(self):
            super(TextEdit, self).__init__()
            self.oneshot = PMGLoopThreadRunner(run, iter_args=[(i, i + 1) for i in range(100)])
            self.oneshot.signal_step_finished.connect(self.on_step_finished)
            self.oneshot.signal_finished.connect(self.on_finished)

        def on_step_finished(self, step, result):
            self.append('step:%d,result:%s\n' % (step, repr(result)))

        def on_finished(self):
            self.append('finished!')

        def closeEvent(self, a0: 'QCloseEvent') -> None:
            super().closeEvent(a0)


    app = QApplication(sys.argv)
    textedit = TextEdit()
    textedit.show()
    sys.exit(app.exec_())
