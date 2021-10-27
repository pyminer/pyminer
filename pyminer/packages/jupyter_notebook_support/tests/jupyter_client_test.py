# -*- coding:utf-8 -*-
# @Time: 2021/1/25 9:38
# @Author: Zhanyi Hou
# @Email: 1295752786@qq.com
# @File: jupyter_client_test.py

kernel = {
  "shell_port": 59046,
  "iopub_port": 59047,
  "stdin_port": 59048,
  "control_port": 59049,
  "hb_port": 59050,
  "ip": "127.0.0.1",
  "key": "4032a091-06eff0767941288d2e59b4ae",
  "transport": "tcp",
  "signature_scheme": "hmac-sha256",
  "kernel_name": ""
}

from jupyter_client import BlockingKernelClient
c = BlockingKernelClient(connection_file='test.json')
c.load_connection_file()
c.start_channels()
print(c.execute('a=123445677'))