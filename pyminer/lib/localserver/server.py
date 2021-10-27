import threading
from multiprocessing import shared_memory

from flask import Flask
from flask_cors import CORS

server = Flask(__name__, static_folder='static', static_url_path='/static')
CORS(server, supports_credentials=True)  # 解决跨域

server_thread = threading.Thread(target=server.run)  # 这个线程与主界面没有任何交互，直接用系统内建的线程库即可，保证其安全性。
server_thread.setDaemon(True)

"""
创建共享内存sharedMemory，用于存放登录后返回的token和其他信息，token长度为199，索引为0-198，在用户登录后请勿将其覆盖
"""
shared_memo = shared_memory.SharedMemory(name="sharedMemory", create=True, size=4096)

if __name__ == '__main__':
    server_thread.start()
