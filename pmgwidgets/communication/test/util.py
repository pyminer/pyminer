import time
import socket
from typing import Callable


def receive(socket_obj: socket.socket) -> bytes:
    l = []
    while (1):
        try:
            b = socket_obj.recv(1024)
        except:
            import traceback
            traceback.print_exc()
            return b''
        l.append(b)
        if b.endswith(b'PMEND'):
            l[-1] = l[-1].strip(b'PMEND')
            break
    return b''.join(l)


def timeit(func):
    def wrapper(*args, **kwargs):
        t0 = time.time()
        r = func(*args, **kwargs)
        print('time_elapsed', time.time() - t0)
        return r

    return wrapper
