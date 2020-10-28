"""
作者：侯展意
有关QThread为什么行，为什么不行
我也不知道啊...
"""
import time
import sys
from PyQt5.QtCore import QThread, QObject, pyqtSignal
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QTextBrowser, QCheckBox
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pyminer2.features.util.openprocess import PMProcess
else:
    from pyminer2.features.util.openprocess import PMProcess


class ProcessMonitorThread(QObject):
    on_err = pyqtSignal(str)
    on_out = pyqtSignal(str)
    on_finished = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.process_terminated = False
        self.args = None

    def stop(self):
        self.process.terminate = True
        self.process_terminated = True

    def run(self):
        self.process = PMProcess(self.args)
        self.q = self.process.q
        idleLoops = 0
        while True:
            if self.process_terminated == True:
                return
            if not self.q.empty():
                line = self.q.get()
                # print(line)
                if line[0] == '1':
                    self.on_out.emit(line[1:])
                else:
                    self.on_err.emit(line[1:])
                sys.stdout.flush()
            else:
                time.sleep(0.01)
                if idleLoops >= 5:
                    idleLoops = 0
                    # print(self.process.process.poll())
                    if self.process.process.poll() is None:
                        try:
                            self.process.process.stdin.write(
                                'messsage\n'.encode('ascii'))  # 模拟输入
                            self.process.process.stdin.flush()
                        except:
                            import traceback
                            traceback.print_exc()
                            self.on_finished.emit()
                            return
                    else:
                        self.on_finished.emit()
                        return
                    continue
                idleLoops += 1


class ProcessConsole(QTextBrowser):
    signal_stop_qthread = pyqtSignal()
    signal_process_stopped = pyqtSignal()
    signal_process_started = pyqtSignal()

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
            self.out_thread.finished.connect(lambda: print('exit!!'))
            self.out_thread.finished.connect(self.monitor_thread.deleteLater)

            self.monitor_thread.on_finished.connect(self.terminate_process)

    def on_stdout(self, text):
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


class PMGProcessConsoleWidget(QWidget):
    def __init__(self, args: list = None):
        super().__init__()
        self.hbox_layout = QHBoxLayout()
        self.tool_widget = QWidget()
        self.tool_widget.setLayout(QVBoxLayout())
        self.process_console = ProcessConsole(args=args)
        self.process_console.signal_process_stopped.connect(self.on_terminated)

        self.button_to_start = QPushButton('start')
        self.tool_widget.layout().addWidget(self.button_to_start)
        self.button_to_start.clicked.connect(self.start_process)

        self.button_to_terminate = QPushButton('termi')
        self.tool_widget.layout().addWidget(self.button_to_terminate)
        self.button_to_terminate.clicked.connect(self.terminate_process)

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
        self.setLayout(self.hbox_layout)

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
        self.process_console.start_process()
        self.on_started()

    def terminate_process(self):
        self.process_console.terminate_process()
        self.on_terminated()

    def is_process_running(self) -> bool:
        return self.process_console.is_running()

    def closeEvent(self, a0: QCloseEvent) -> None:
        self.terminate_process()
        # if self.process_console.out_thread.isRunning():
        #     self.process_console.monitor_thread.stop()
        #     self.process_console.out_thread.quit()
        #     self.process_console.out_thread.wait(500)

        # self.process_console.monitor_thread.stop()
        # self.process_console.monitor_thread.deleteLater()
        # self.process_console.out_thread.deleteLater()
        super(PMGProcessConsoleWidget, self).closeEvent(a0)


if __name__ == '__main__':
    import cgitb

    cgitb.enable(format='text')
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    w = PMGProcessConsoleWidget(['python', '-u', 'test_open_app.py'])
    w.show()

    sys.exit(app.exec_())
