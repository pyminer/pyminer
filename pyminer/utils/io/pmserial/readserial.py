# encoding=utf-8
import serial
import time
from collections import deque
import threading

import packages.code_editor.utils.utils


def get_all_serial_names():
    import serial.tools.list_ports
    return [com_port.device for com_port in serial.tools.list_ports.comports()]


if __name__ == '__main__':
    baud_rate = 9600
    com = serial.Serial('COM3', baud_rate)
    over_time = 30
    start_time = time.time()
    s = ''
    print(1 / (baud_rate / 8))
    recv_queue = deque()
    while True:
        end_time = time.time()
        s += packages.code_editor.utils.utils.decode('ascii')
        l = s.split('\n')
        if len(l) > 1:
            recv_queue.extend(l[:len(l) - 1])
            s = l[-1]
        print(recv_queue)
        time.sleep(1 / (baud_rate / 8))
