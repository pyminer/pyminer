import requests
import json
import base64
import pickle
import time
import sys
import numpy as np


class Client:
    def __init__(self):
        pass

    @staticmethod
    def write(dataname: str, data: dict, provider: str = 'server'):
        url = "http://localhost:8783/"
        payload = {
            "method": "write",
            "params": [dataname, data, provider],
            "jsonrpc": "2.0",
            "id": 0,
        }
        response = requests.post(url, json=payload).json()

    @staticmethod
    def read(dataname:str):
        t0=time.time()
        url = "http://localhost:8783/"
        payload = {
            "method": "read",
            "params": [dataname],
            "jsonrpc": "2.0",
            "id": 0,
        }
        response = requests.post(url, json=payload).json()
        t1=time.time()
        print(t1-t0,response)
        return response


if __name__ == "__main__":
    c = Client
    c.read('matrix')

    c.write('mat', {'type': 'matrix', 'value': [[1, 2, 3], [3, 2, 1]]}, 'user')
    c.read('mat')
    # import requests,time

    # r = requests.get('http://localhost:8783/read/arr')
    # print(r.text)

    # r = requests.post('http://localhost:8783/write/', json={'dataname': 'mat', 'data': {'type': 'matrix',
    # 'value': [[1,2,3],[3,2,1]]}, 'provider': 'user'}) print(r.__dict__)
