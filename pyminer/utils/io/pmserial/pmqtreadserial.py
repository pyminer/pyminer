# encoding=utf-8
import serial
import serial.tools.list_ports
from collections import deque
import sys
import time
from PySide2.QtWidgets import QApplication, QMainWindow, QTextEdit
from PySide2.QtCore import QObject, QThread, Signal

import packages.code_editor.utils.utils
from widgets import PMQThreadObject, QTextCursor
from utils.io.pmserial.readserial import get_all_serial_names


class PMGSerialWorker(QObject):
    signal_splitter_received = Signal(str)

    def __init__(self, com_name: str, baud_rate: int, splitter='\n', coding: str = 'ascii'):
        super(PMGSerialWorker, self).__init__()
        self.quit = False
        self.queue = False
        self.splitter = splitter
        self.com_name = com_name
        self.baud_rate = baud_rate
        self.coding = coding

    def open_serial(self) -> serial.Serial:
        try:
            com = serial.Serial(self.com_name, self.baud_rate, timeout=1)
            return com
        except serial.SerialException:
            print('串口可能已经关闭！')

    def work(self):
        """
        工作函数.
        如果中间发生断开，就进行重连。
        :return:
        """
        com = self.open_serial()  # serial.Serial(self.com_name, self.baud_rate)
        s = ''
        delay = 0.01
        print(delay)
        recv_queue = deque()
        while (1):
            try:
                if com.inWaiting() == 0:
                    continue
                chars = com.readline(com.inWaiting())
                print(chars)
                try:
                    chars = packages.code_editor.utils.utils.decode(self.coding)
                except UnicodeDecodeError:
                    continue
                if self.splitter != '':
                    s += chars
                    l = s.split(self.splitter)
                    if len(l) > 1:
                        received = l[:len(l) - 1]
                        if self.queue:
                            recv_queue.extend(received)
                        else:
                            for s in recv_queue:
                                self.signal_splitter_received.emit(s)
                else:
                    if self.queue:
                        recv_queue.append(chars)
                    else:
                        self.signal_splitter_received.emit(chars)

            except serial.SerialException:
                print('可能断开连接')
                time.sleep(1)
                if self.com_name in get_all_serial_names():
                    c = self.open_serial()
                    if c is not None:
                        com = c
            time.sleep(delay)
            if self.quit:
                break

    def on_exit(self):
        self.quit = True


class PMSerialMonitor(PMQThreadObject):
    def __init__(self, port_name: str, baud_rate: int = 9600, splitter='\n', coding: str = 'ascii'):
        self.serial_worker = PMGSerialWorker(port_name, baud_rate, splitter, coding)
        super(PMSerialMonitor, self).__init__(parent=None, worker=self.serial_worker)
        self.signal_splitter_received = self.serial_worker.signal_splitter_received


if __name__ == '__main__':
    class W(QMainWindow):

        def closeEvent(self, a0) -> None:
            super().closeEvent(a0)
            m.terminate()


    app = QApplication(sys.argv)
    m = PMSerialMonitor('COM3', 115200, '', 'utf-8')

    w = W()
    text = QTextEdit()
    w.setCentralWidget(text)
    w.show()


    def insert_text(s):
        text.insertPlainText(s)  # 这样做的话可以自动处理换行。
        text.moveCursor(QTextCursor.End)
        text.ensureCursorVisible()


    m.signal_splitter_received.connect(insert_text)
    sys.exit(app.exec_())
