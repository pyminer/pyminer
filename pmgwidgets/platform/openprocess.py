import queue
import subprocess
import threading
import time
import chardet
from typing import List


class PMGProcess():
    def __init__(self, args: List[str]):
        self.terminate = False
        self.q = queue.Queue()
        self.on_command_received = lambda cmd: print(cmd)
        self.on_error_received = lambda error: print(error)
        self.args = args
        self.process = subprocess.Popen(self.args,
                                        stdin=subprocess.PIPE,
                                        shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.to = threading.Thread(
            target=self.enqueue_stream, args=(
                self.process.stdout, self.q, 1))
        self.te = threading.Thread(
            target=self.enqueue_stream, args=(
                self.process.stderr, self.q, 2))
        self.tp = threading.Thread(target=self.console_loop)
        self.to.setDaemon(True)
        self.te.setDaemon(True)
        self.tp.setDaemon(True)
        self.te.start()
        self.to.start()
        self.tp.start()

    def enqueue_stream(self, stream, queue, type):  # 将stderr或者stdout写入到队列q中。
        for line in iter(stream.readline, b''):
            if self.terminate:
                break
            encoding = chardet.detect(line)['encoding']
            queue.put(str(type) + line.decode(encoding))
        stream.close()

    def console_loop(self):  # 封装后的内容。
        pass


if __name__ == '__main__':
    pmp = PMGProcess(['python', '-u', '-c', 'print(hello world!)'])
    while (1):
        time.sleep(2)
        pass
