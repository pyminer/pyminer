import queue
import re
import subprocess
import sys
import threading
import time
import chardet
from typing import List

import packages.code_editor.utils.utils


class PMProcess():
    def __init__(self, args: List[str]):
        self.terminate = False
        self.q = queue.Queue()
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
        self.tp = threading.Thread(target=self.consoleLoop)
        self.to.setDaemon(True)
        self.te.setDaemon(True)
        self.tp.setDaemon(True)
        self.te.start()
        self.to.start()
        self.tp.start()

    def enqueue_stream(self, stream, queue, type):  # 将stderr或者stdout写入到队列q中。
        for line in iter(stream.readline, b''):
            if self.terminate: break
            encoding = chardet.detect(line)['encoding']
            queue.put(str(type) + packages.code_editor.utils.utils.decode(encoding))
        stream.close()

    def consoleLoop(self):  # 封装后的内容。
        # idleLoops = 0
        while True:
            if not self.q.empty():
                line = self.q.get()
                if line[0] == '1':
                    self.on_command_received(line[1:])
                else:
                    self.on_error_received(line[1:])
                sys.stdout.flush()
            else:
                time.sleep(0.01)
                # idleLoops += 1

    def input(self, message: str):
        if not message.endswith('\n'):
            message += '\n'
        self.process.stdin.write(
            message.encode('utf-8'))  # 模拟输入
        self.process.stdin.flush()

    def on_command_received(self, cmd: str):
        # print(cmd)
        cmd = cmd.strip()
        file_paths = re.findall(r'>(.+?)\(', cmd)
        if len(file_paths) > 0:
            path = file_paths[0].strip()
            splitted = cmd.split(path)
            if len(splitted) == 2:
                remaining_words = splitted[1].strip()
                current_row = re.findall(r'\((.+?)\)', remaining_words)
                if len(current_row) >= 1:
                    print(path, int(current_row[0]))
                # if remaining_words.startswith('<'):

            # print('file:', file_result.group())
        # while(1):
        #     if cmd.startswith('(Pdb)'):
        #         cmd = cmd.strip()
        #         cmd = cmd.strip('(Pdb)')
        #     else:
        #         cmd = cmd.strip()
        #         # if cmd.startswith('>'):
        #
        #         break
        print(cmd)


if __name__ == '__main__':
    s = r"""
import os
import pmdebug
__global_keys = set(globals().keys())

b E:\Python\pyminer_bin\PyMiner\bin\pmtoolbox\debug\test2.py:2
alias pi for k in locals().keys(): pmdebug.insight(k,locals()[k]);print(12333333333333,os.path.dirname(r'c:\123123'))
alias tobreak c;;pi a
alias ps pi self

"""
    pmp = PMProcess(['python', '-u', '-m', 'pdb',
                     r'E:\Python\pyminer_bin\PyMiner\bin\pmtoolbox\debug\test.py'])
    pmp.input(s)
    while (1):
        pmp.input('c')
        time.sleep(2)
        pass
