'''
Modification:
revise __inspect function， return a dict where key:str,value:str
when console receives prints
pickle items sequentially
if catch any error, then pass
'''

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import base64
import dill as pickle
import types
from matgen import v_, h_, M_

__ip = get_ipython()
__builtins = [__k for __k in globals().keys()]

def __inspect():
    __data_message = {}
    __data = {__k: __v for __k, __v in globals().items() if __k not in __builtins and not __k.startswith('_') and not isinstance(__v, types.ModuleType)}
    for __k in __data.keys():
        try:
            __data_message[__k]=base64.b64encode(pickle.dumps(__data[__k])).decode('ascii')
        except:
            pass
    print(base64.b64encode(pickle.dumps(__data_message)).decode('ascii'))

def __inject(data_b64):
    data_b64_dic = pickle.loads(base64.b64decode(data_b64))
    data = {}
    for key in data_b64_dic:
            var = data_b64_dic[key]
            try:
                data[key] = pickle.loads(base64.b64decode(data_b64_dic[key]))
            except:
                import traceback
                traceback.print_exc()
    globals().update(data)

__ip.events.register('post_run_cell', __inspect)
