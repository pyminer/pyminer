"""
作者：侯展意
有关QThread为什么行，为什么不行
我也不知道啊...
"""
import os
import platform
import re
import time
import sys
import logging
from PySide2.QtCore import QThread, QObject, Signal, QTimer, Qt
from PySide2.QtGui import QCloseEvent
from PySide2.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QTextBrowser, QCheckBox, QTextEdit
from typing import TYPE_CHECKING, List
from widgets import PMGJsonTree

logger = logging.getLogger(__name__)
if TYPE_CHECKING:
    from lib.openprocess import PMProcess
    from packages.code_editor.widgets.tab_widget import PMCodeEditTabWidget
else:
    from lib.openprocess import PMProcess


class DebugProcess(PMProcess):
    """
    TODO:Ugly structure and it must be refactored soon!!!!!!!!!
    """

    def enqueue_stream(self, stream, queue, type):
        self.enqueue_stream_err(stream, queue, type)


class ProcessMonitorThread(QObject):
    on_err = Signal(str)
    on_out = Signal(str)
    signal_process_started = Signal()
    on_finished = Signal()

    def __init__(self):
        super().__init__()
        self.process_terminated = False
        self.args = None
        self.process: 'DebugProcess' = None

    def stop(self):
        self.process.terminate = True
        self.process_terminated = True

    def run(self):
        self.process = DebugProcess(self.args)
        self.signal_process_started.emit()
        self.q = self.process.q
        idleLoops = 0
        while True:
            if self.process_terminated == True:
                return
            if not self.q.empty():
                line = self.q.get()
                if line[0] == '1':
                    self.on_out.emit(line[1:])
                else:
                    self.on_err.emit(line[1:])
                sys.stdout.flush()
            else:
                time.sleep(0.01)
                if idleLoops >= 5:
                    idleLoops = 0
                    if self.process.process.poll() is None:
                        pass
                    else:
                        self.on_finished.emit()
                        return
                    continue
                idleLoops += 1


class ProcessConsole(QTextEdit):
    signal_stop_qthread = Signal()
    signal_process_stopped = Signal()
    signal_process_started = Signal()
    signal_goto_file = Signal(str, int)

    def __init__(self, args: list = None):
        super().__init__()
        self._is_running = False
        self.auto_scroll = True
        self.args = args  #
        self.setContentsMargins(20, 20, 0, 0)
        self.monitor_thread: 'ProcessMonitorThread' = None
        self.out_thread: 'QThread' = None

    def is_running(self):
        if self.monitor_thread is not None:
            if self.monitor_thread.process.process.poll() is None:
                return True
        return False

    def start_process(self):
        if not self.is_running():
            self.out_thread = QThread(self)
            self.monitor_thread = ProcessMonitorThread()
            self.monitor_thread.args = self.args
            self.monitor_thread.moveToThread(self.out_thread)

            self.out_thread.started.connect(self.monitor_thread.run)
            self.out_thread.start()

            self.monitor_thread.on_out.connect(self.on_stdout)
            self.monitor_thread.on_err.connect(self.on_stderr)

            self.signal_stop_qthread.connect(self.monitor_thread.stop)

            self.out_thread.finished.connect(self.out_thread.deleteLater)
            self.out_thread.finished.connect(self.monitor_thread.deleteLater)

            self.monitor_thread.on_finished.connect(self.terminate_process)
            self.monitor_thread.signal_process_started.connect(lambda: self.signal_process_started.emit())

    def on_stdout(self, text):
        cmd = text.strip()
        file_paths = re.findall(r'>(.+?)\(', cmd)
        if len(file_paths) > 0:
            path = file_paths[0].strip()
            splitted = cmd.split(path)
            if len(splitted) == 2:
                if os.path.exists(path):
                    remaining_words = splitted[1].strip()
                    current_row = re.findall(r'\((.+?)\)', remaining_words)
                    if len(current_row) >= 1:
                        # self.insertHtml('<p style="color:blue;">' + path + ';' + current_row[0] + '<br/></p>')
                        print(file_paths[0], current_row, remaining_words)
                        self.signal_goto_file.emit(path, int(current_row[0]))
        self.insertHtml('<p>' + text + '<br/></p>')
        if self.auto_scroll:
            self.ensureCursorVisible()

    def on_stderr(self, text):
        self.insertHtml('<p style="color:red;">' + text + '<br/></p>')
        if self.auto_scroll:
            self.ensureCursorVisible()

    def terminate_process(self):
        if self.monitor_thread is not None:
            self.monitor_thread.process_terminated = True
            self.monitor_thread.process.process.terminate()
            if self.out_thread.isRunning():
                self.signal_stop_qthread.emit()
                self.out_thread.quit()
                self.out_thread.wait(500)
        self.monitor_thread = None
        self.out_thread = None
        self.signal_process_stopped.emit()

    def keyPressEvent(self, e: 'QKeyEvent'):
        if e.key() == Qt.Key_Backspace or e.key() == Qt.Key_Delete:
            return
        print(e.key(), e.text())
        if e.key() == Qt.Key_Return:
            text = '\n'
        else:
            text = e.text()
        print(text,e.text())
        if text != '' and self.monitor_thread is not None:
            try:
                print('sent:', text)
                self.monitor_thread.process.process.stdin.write(text.encode('utf8'))
                self.monitor_thread.process.process.stdin.flush()
            except:
                import traceback
                traceback.print_exc()
        super(ProcessConsole, self).keyPressEvent(e)


class PMGDebugConsoleWidget(QWidget):
    def __init__(self, args: list = None, editor_tab_widget: 'PMCodeEditTabWidget' = None):
        super().__init__()
        self.extension_lib = None

        self.editor_tab_widget: 'PMCodeEditTabWidget' = editor_tab_widget
        self.hbox_layout = QHBoxLayout()
        self.tool_widget = QWidget()
        self.input_queue: List[str] = []
        self.tool_widget.setLayout(QVBoxLayout())
        self.process_console = ProcessConsole(args=args)
        self.process_console.signal_process_stopped.connect(self.on_terminated)

        self.button_to_start = QPushButton('start')
        self.tool_widget.layout().addWidget(self.button_to_start)
        self.button_to_start.clicked.connect(self.start_process)

        self.button_to_terminate = QPushButton('termi')
        self.tool_widget.layout().addWidget(self.button_to_terminate)
        self.button_to_terminate.clicked.connect(self.terminate_process)

        self.button_to_clear = QPushButton('step')
        self.tool_widget.layout().addWidget(self.button_to_clear)
        self.button_to_clear.clicked.connect(lambda: self.input('s'))

        self.button_to_clear = QPushButton('continue')
        self.tool_widget.layout().addWidget(self.button_to_clear)
        self.button_to_clear.clicked.connect(lambda: self.input('tobreak'))

        self.button_to_clear = QPushButton('clear')
        self.tool_widget.layout().addWidget(self.button_to_clear)
        self.button_to_clear.clicked.connect(lambda: self.process_console.clear())

        self.autoscroll_checker = QCheckBox()
        self.autoscroll_checker.setToolTip('autoscroll')
        self.tool_widget.layout().addWidget(self.autoscroll_checker)
        self.autoscroll_checker.stateChanged.connect(self.set_autoscroll)
        self.autoscroll_checker.setChecked(True)
        self.set_autoscroll()

        self.hbox_layout.addWidget(self.tool_widget)

        self.hbox_layout.addWidget(self.process_console)
        self.var_viewer = PMGJsonTree()
        self.hbox_layout.addWidget(self.var_viewer)
        self.setLayout(self.hbox_layout)
        self.process_console.signal_process_started.connect(self.clear_input_queue)

    def set_extension_lib(self, extension_lib):
        self.extension_lib = extension_lib
        self.extension_lib.Data.add_data_changed_callback(self.on_data_changed)

    def on_data_changed(self, data_name: str, var: object, provider: str):
        if data_name == 'debug_vars':
            self.var_viewer.set_data_dic(var)

    def input(self, message):
        """
        输入命令。
        若在windows的终端运行则需要用gbk编码；若在pycharm中运行，则无需gbk编码。
        因此注意，下面多了个判断过程！
        :param message:
        :return:
        """
        line_ending = '\n'
        # if platform.system().lower() == 'windows':
        #     line_ending = '\r\n'
        if not message.endswith(line_ending):
            message += line_ending
        th = self.process_console.monitor_thread
        if th is not None:
            if th.process is not None:
                process = th.process.process
                encoded = b''
                if platform.system().lower() == 'windows' and sys.stdout.isatty():  # 如果在windows的终端运行
                    encoded = message.encode('gbk')
                else:
                    encoded = message.encode('utf-8')
                process.stdin.write(encoded)  # 模拟输入
                process.stdin.flush()
                return

        self.input_queue.append(message)

    def clear_input_queue(self):
        """
        进程启动之后，调用这个队列处理器，逐条运行未能运行的命令。
        :return:
        """
        for m in self.input_queue:
            self.input(m)

    def set_autoscroll(self):
        print(self.autoscroll_checker.isChecked())
        self.process_console.auto_scroll = self.autoscroll_checker.isChecked()

    def on_terminated(self):
        self.button_to_start.setEnabled(True)
        self.button_to_terminate.setEnabled(False)

    def on_started(self):
        self.button_to_start.setEnabled(False)
        self.button_to_terminate.setEnabled(True)

    def start_process(self):
        bp_input = self.editor_tab_widget.get_all_breakpoints('python')
        bp_input = bp_input.strip()
        self.input(bp_input)
        self.process_console.start_process()
        self.on_started()
        s = r"""
!import sys;sys.path.append(r'%s')
alias pi !import pmtoolbox,os;pmtoolbox.debug.pmdebug.insight(locals());
alias tobreak c;;pi
alias ps pi self
""" % r'E:\Python\pyminer_bin\PyMiner\bin'
        self.input(s)

    def terminate_process(self):
        for index in range(self.editor_tab_widget.count()):
            self.editor_tab_widget.widget(index).remove_debug_indicator()
        self.process_console.terminate_process()
        self.on_terminated()

    def is_process_running(self) -> bool:
        return self.process_console.is_running()

    def close(self) -> bool:
        self.terminate_process()
        self.extension_lib.Data.remove_data_changed_callback(self.on_data_changed)
        return super().close()

    def closeEvent(self, a0: QCloseEvent) -> None:
        self.terminate_process()
        super(PMGDebugConsoleWidget, self).closeEvent(a0)

# if __name__ == '__main__':
#     import cgitb
#
#     cgitb.enable(format='text')
#     from PyQt5.QtWidgets import QApplication
#
#     app = QApplication(sys.argv)
#
#     w = PMGDebugConsoleWidget(['python', '-u', '-m', 'pdb',
#                                r'E:\Python\pyminer_bin\PyMiner\bin\pmtoolbox\debug\test.py'])
#     w.show()
#     w.start_process()
#     sys.exit(app.exec_())
