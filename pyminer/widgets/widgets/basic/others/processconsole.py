"""
作者：侯展意
有关QThread为什么行，为什么不行
我也不知道啊...
"""
import os
import re
import time
import sys
import logging

from PySide2.QtCore import QThread, QObject, Signal, Qt, QUrl
from PySide2.QtGui import QCloseEvent, QKeyEvent, QIcon, QDesktopServices, QColor
from PySide2.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QCheckBox, QTextEdit, QApplication, \
    QMessageBox

logger = logging.getLogger(__name__)

from widgets.utilities.platform.openprocess import PMGProcess


class ProcessMonitorThread(QObject):
    on_err = Signal(str)
    on_out = Signal(str)
    on_finished = Signal()

    def __init__(self):
        super().__init__()
        self.process_terminated = False
        self.args = None

    def stop(self):
        self.process.terminate = True
        self.process_terminated = True

    def run(self):
        try:
            self.process = PMGProcess(self.args)
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
        except:
            import traceback
            traceback.print_exc()


class ProcessConsole(QTextEdit):
    signal_stop_qthread = Signal()
    signal_process_stopped = Signal()
    signal_process_started = Signal()
    signal_hyperlink_clicked = Signal(str)
    signal_goto_file = Signal(str, int)
    insert_mode = ''

    def __init__(self, args: list = None):
        super().__init__()
        self.anchor = None
        self._is_running = False
        self.auto_scroll = True
        self.args = args  #
        self.setContentsMargins(20, 20, 0, 0)
        self.monitor_thread: 'ProcessMonitorThread' = None
        self.out_thread: 'QThread' = None
        self.signal_hyperlink_clicked.connect(self.on_hyperlink_clicked)

    def set_args(self, args: list = None):
        self.args = args

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
            self.clear()
            self.insertHtml('<p style="color:#0063c5;">' + ' '.join(self.args) + '<br/></p>')
            self.insertHtml('<p style="color:#aaaaaa;">' + '' + '</p>')

    def on_stdout(self, text):

        if self.insert_mode == 'error':
            self.insert_mode = 'stdout'

        self.insertHtml(self.insertHtml('<p style="color:#aaaaaa;">' + text + '<br/></p>'))
        if self.auto_scroll:
            self.ensureCursorVisible()

    def on_stderr(self, text):
        self.insert_mode = 'error'
        # result = re.search(r'(/|([a-zA-Z]:((\\)|/))).*:[0-9].*', text)
        result = re.search(r'(/|([a-zA-Z]:((\\)|/))).* line [0-9].*,', text)
        print(result)
        if result is None:
            self.insertHtml('<p style="color:red;">' + text + '<br/></p>')
        else:
            span = result.span()
            self.insertHtml('<p style="color:red;">' + text[:span[0]] + '</p>')
            print(result.group())
            self.insert_hyperlink(text[span[0]: span[1]])
            # self.insertHtml('<p style="color:red;">' + text[result[0]:result[1]] + '</p>')
            self.insertHtml('<p style="color:red;">' + text[span[1]:] + '<br/></p>')
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
        if text != '' and self.monitor_thread is not None:
            try:
                print('sent:', text)
                self.monitor_thread.process.process.stdin.write(text.encode('utf8'))
                self.monitor_thread.process.process.stdin.flush()
            except:
                import traceback
                traceback.print_exc()
        super(ProcessConsole, self).keyPressEvent(e)

    def mousePressEvent(self, e):
        super(ProcessConsole, self).mousePressEvent(e)
        self.anchor = self.anchorAt(e.pos())
        # if self.anchor:
        #     QApplication.setOverrideCursor(Qt.PointingHandCursor)

    def mouseMoveEvent(self, e):
        super(ProcessConsole, self).mouseMoveEvent(e)
        self.anchor = self.anchorAt(e.pos())
        if not self.anchor:
            QApplication.setOverrideCursor(Qt.ArrowCursor)
        else:
            QApplication.setOverrideCursor(Qt.PointingHandCursor)

    def mouseReleaseEvent(self, e):
        super(ProcessConsole, self).mouseReleaseEvent(e)
        if self.anchor:
            # QDesktopServices.openUrl(QUrl(self.anchor))
            # QApplication.setOverrideCursor(Qt.ArrowCursor)
            self.signal_hyperlink_clicked.emit(self.anchor)
            self.anchor = None

    def insert_hyperlink(self, link: str, text=''):
        cursor = self.textCursor()
        fmt = cursor.charFormat()
        fmt.setForeground(QColor('#0063c5'))
        # address = 'http://example.com'
        fmt.setAnchor(True)
        fmt.setAnchorHref(link)
        fmt.setToolTip(link)
        if text == '':
            cursor.insertText(link, fmt)
        else:
            cursor.insertText(text, fmt)

    def on_hyperlink_clicked(self, hyperlink_text: str):
        if re.search(r'(/|([a-zA-Z]:((\\)|/))).* line [0-9].*,', hyperlink_text) is not None:
            try:
                l = hyperlink_text.split('line')
                assert len(l) == 2, l
                for i in [0, 1]:
                    l[i] = l[i].strip(', \"\'')
                file_path, row_str = l
                row = int(row_str)
                if not os.path.exists(file_path):
                    QMessageBox.warning(self, self.tr('Warning'), self.tr('文件%s不存在！' % file_path))
                else:
                    self.signal_goto_file.emit(file_path, row)
                    logger.info('goto file %s, line %d' % (file_path, row))
            except:
                import traceback
                traceback.print_exc()


class PMGProcessConsoleWidget(QWidget):
    signal_goto_file = Signal(str, int)

    def __init__(self, args: list = None):
        super().__init__()
        self.hbox_layout = QHBoxLayout()
        self.tool_widget = QWidget()
        self.tool_widget.setLayout(QVBoxLayout())
        self.process_console = ProcessConsole(args=args)
        self.process_console.signal_goto_file.connect(self.signal_goto_file.emit)
        self.process_console.signal_process_stopped.connect(self.on_terminated)

        self.button_to_start = QPushButton()
        self.button_to_start.setToolTip(self.tr('Start'))
        icon_path = os.path.dirname(__file__)
        self.button_to_start.setIcon(QIcon(os.path.join(icon_path, 'source', 'run.png')))
        self.tool_widget.layout().addWidget(self.button_to_start)
        self.button_to_start.clicked.connect(self.start_process)

        self.button_to_terminate = QPushButton()
        self.button_to_terminate.setToolTip(self.tr('Terminate'))
        self.button_to_terminate.setIcon(QIcon(os.path.join(icon_path, 'source', 'stop.png')))
        self.tool_widget.layout().addWidget(self.button_to_terminate)
        self.button_to_terminate.clicked.connect(self.terminate_process)

        self.button_to_clear = QPushButton()
        self.button_to_clear.setToolTip(self.tr('Clear'))
        self.tool_widget.layout().addWidget(self.button_to_clear)
        self.button_to_clear.setIcon(QIcon(os.path.join(icon_path, 'source', 'clear.png')))
        self.button_to_clear.clicked.connect(lambda: self.process_console.clear())

        self.button_to_clear.setMaximumWidth(20)
        self.button_to_start.setMaximumWidth(20)
        self.button_to_terminate.setMaximumWidth(20)
        self.autoscroll_checker = QCheckBox()
        self.autoscroll_checker.setToolTip('autoscroll')

        self.tool_widget.layout().addWidget(self.autoscroll_checker)
        self.autoscroll_checker.stateChanged.connect(self.set_autoscroll)
        self.autoscroll_checker.setChecked(True)
        self.set_autoscroll()

        self.hbox_layout.addWidget(self.tool_widget)
        vbox = QVBoxLayout()
        self.hbox_layout.addLayout(vbox)
        vbox.addWidget(self.process_console)
        # self.command_input = QLineEdit()
        # vbox.addWidget()
        self.setLayout(self.hbox_layout)

    def set_autoscroll(self):
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
        super(PMGProcessConsoleWidget, self).closeEvent(a0)

    def set_args(self, args: list):
        self.process_console.set_args(args)


if __name__ == '__main__':
    import cgitb
    import sys

    cgitb.enable(format='text')

    app = QApplication(sys.argv)
    w = PMGProcessConsoleWidget(
        [sys.executable, '-u', os.path.join(os.path.dirname(__file__), 'scripts', 'test2_open_app.py')])
    w.show()

    sys.exit(app.exec_())
