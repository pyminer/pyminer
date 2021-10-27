import time
import types
from typing import Dict, Union, Any


def get_attributes_dic(name: str, var: Any) -> Dict[str, Union[str, Dict]]:
    v: Dict[str, Union[str, Dict]] = {}
    v['name'] = name
    v['type'] = str(type(var))
    v['value'] = repr(var)
    v['attributes'] = {}
    v['protected_attrs'] = {}
    # print(name,len(dir(var)))
    for attr_name in dir(var):
        if attr_name.startswith('_'):
            v['protected_attrs'][attr_name] = ''  # str(attr)#{'value': str(attr), 'type': str(type(attr))}
        else:
            v['attributes'][attr_name] = ''
    return v


def insight(var_dic: dict):
    from lib.comm import set_var
    # t0 = time.time()
    vars = {}
    callables = {}
    modules = {}
    protecteds = {}
    for name, var in var_dic.items():
        if name.startswith('_'):
            protecteds[name] = {'type': str(var), 'value': str(var)}
        elif isinstance(var, types.ModuleType):
            modules[name] = {'type': str(var), 'value': str(var)}
        elif callable(var):
            callables[name] = {'type': str(var), 'value': str(var)}
        else:
            vars[name] = get_attributes_dic(name, var)
    vars['Callables'] = callables
    vars['Modules'] = modules
    vars['Protected Variables'] = protecteds
    # t1 = time.time()
    # print('time elapsed:',t1-t0 )
    # import cloudpickle
    # with open(r'c:\users\12957\Desktop\dump.pkl', 'wb') as f:
    #     cloudpickle.dump(vars, f)
    set_var('debug_vars', vars, 'debugger')
    # print('step finished!!')


if __name__ == '__main__':
    import pandas as pd

    a = 123
    b = 456
    l = [1, 2, 3, 4, 5]
    insight(globals())
