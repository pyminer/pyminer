import time
import requests


def timeit(func):
    def wrapper(*args, **kwargs):
        t0 = time.time()
        r = func(*args, **kwargs)
        print(time.time() - t0)
        return r
    return wrapper


class Client():
    def __init__(self):
        pass

    @timeit
    def write(self, dataname: str, data: dict, provider: str = 'server'):
        url = "http://localhost:8783/"
        payload = {
            "method": "write",
            "params": [dataname, data, provider],
            "jsonrpc": "2.0",
            "id": 0,
        }
        response = requests.post(url, json=payload).json()
        print(response)

    @timeit
    def read(self, dataname: str):
        url = "http://localhost:8783/"
        payload = {
            "method": "read",
            "params": [dataname],
            "jsonrpc": "2.0",
            "id": 0,
        }
        response = requests.post(url, json=payload).json()
        print(response)
        return response


if __name__ == "__main__":
    c = Client()
    c.read('Matrix')
    c.write('mat', {'type': 'Matrix', 'value': [[1, 2, 3], [3, 2, 1]]}, 'user')

    # import requests,time

    # r = requests.get('http://localhost:8783/read/arr')
    # print(r.text)

    # r = requests.post('http://localhost:8783/write/', json={'dataname': 'mat', 'data': {'type': 'matrix',
    # 'value': [[1,2,3],[3,2,1]]}, 'provider': 'user'}) print(r.__dict__)
