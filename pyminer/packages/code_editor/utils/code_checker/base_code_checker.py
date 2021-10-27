import logging
import re
from contextlib import redirect_stdout
from io import StringIO
from queue import Queue
from typing import List, Tuple

from PySide2.QtCore import QObject, Signal, QThread, QTemporaryFile, SignalInstance
from flake8.main.application import Application

from ..base_object import CodeEditorBaseObject

logger = logging.getLogger(__name__)


class CodeCheckWorker(CodeEditorBaseObject, QObject):
    """代码检查"""
    checked: SignalInstance = Signal(object, list)

    def __init__(self, *args, **kwargs):
        super(CodeCheckWorker, self).__init__(*args, **kwargs)
        self._queue = Queue()
        self._running = True
        self.background_checking = True

    def add(self, widget: 'QsciScintilla', code: str):
        """添加需要检测的对象

        Args:
            widget: 目标编辑器
            code: 目标编辑器代码
        """
        self._queue.put_nowait((widget, code))
        while self._queue.qsize() > 3:
            self._queue.get(False, 0)

    def stop(self):
        """通知线程需要退出，等待线程自行退出"""
        self._running = False

    def run(self):
        """代码检测工作函数"""
        while 1:
            if not self._running:
                logger.info('code checker quit')
                break
            if not self.background_checking:
                QThread.msleep(500)
                continue
            if self._queue.qsize() == 0:
                QThread.msleep(500)
                continue
            try:
                widget, code = self._queue.get(False, 0.5)
                # 创建临时文件
                file = QTemporaryFile(self)
                file.setAutoRemove(True)
                if file.open():
                    with open(file.fileName(), 'wb') as fp:
                        fp.write(code.encode())
                    file.close()
                    # 使用flake8检测代码
                    with StringIO() as out, redirect_stdout(out):
                        app = Application()
                        app.initialize(['flake8', '--exit-zero', '--config', self.settings.assets_dir / '.flake8'])
                        app.run_checks([file.fileName()])
                        app.report()
                        results = out.getvalue().split('\n')
                    new_results: List[Tuple[int, int, str, str]] = []
                    for ret in results:
                        if re.search(r'\d+:\d+:[EFW]\d+:.*?', ret):
                            split_list = ret.split(':')
                            line_no = int(split_list[0])
                            column = int(split_list[1])
                            error_code = split_list[2]
                            error_type = split_list[3]
                            new_results.append((line_no, column, error_code, error_type))
                    # results = [ret for ret in results if re.search(r'\d+:\d+:[EFW]\d+:.*?', ret)]

                    self.checked.emit(widget, new_results)  # 如果为空，也应该这样做。将空列表传入可以清空所有的标记。
                file.deleteLater()
                del file
            except Exception as e:
                logger.warning(str(e))
