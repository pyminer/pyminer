# 使用curve_fit
import re
from typing import Tuple

import numpy as np
from scipy.optimize import curve_fit
from numpy import sin, cos, tan, arcsin, arccos, arctan
from numpy import cosh, tanh, sinh
from numpy import sinc
from numpy import exp, exp2, floor, ceil, power, mod
predefined_functions = {
    'linear': {
        'vars': 'a,b',
        'function': 'a*x+b'
        },
    'sqrt': {
        'vars': 'a,b,c',
        'function': 'a*x**2+b*x+c'
        },
    'cubic': {
        'vars': 'a,b,c,d',
        'function': 'a*x**3+b*x**2+c*x**1+d'
        },
    'customized': {
        'vars': '',
        'function': ''
        }
    }


def check_identifiers(argsStr, funcStr) -> Tuple[bool, str]:
    identifiers_in_def = re.split(r'[;,:\./ \\!&\|\*\+\s\(\)\{\}\[\]0~9]', argsStr)
    func_identifiers = re.split(r'[;,:\./ \\!&\|\*\+\s\(\)\{\}\[\]0~9]', funcStr)
    print(identifiers_in_def)
    print(func_identifiers)
    identifiers_in_def = list(filter(lambda s: (not s == '') and (s.isidentifier()), identifiers_in_def))
    func_identifiers = list(filter(lambda s: (not s == '') and (s.isidentifier()), func_identifiers))

    identifiers_in_func_set = set(func_identifiers)
    identifiers_in_def_set = set(identifiers_in_def)

    for identifier in func_identifiers:
        if (not identifier
            in identifiers_in_def_set) and (globals().get(identifier) is None) and (identifier not in ['x', 'y', 'z']):
            print('Identifier \'%s\' is not defined!' % identifier)
            return False, 'Identifier \'%s\' is not defined!' % identifier

    for identifier in identifiers_in_def:
        if not identifier in identifiers_in_func_set:
            print('Unused Identifier \'%s\'' % identifier)
            return False, 'Unused Identifier \'%s\'' % identifier

    print('checking alright!')
    return True, ''


def fit(x, y, argsStr='a,b,c,d', funcstr='a * x ** 3 + b * x ** 2 + c * x + d'):
    # 非线性最小二乘法拟合

    st = """
def func(x, %s):
    return %s
    """ % (argsStr, funcstr)
    exec(st, globals())
    popt, pcov = curve_fit(func, x, y)
    # 获取popt里面是拟合系数
    xvals = np.linspace(np.min(x), np.max(x), 100)
    yvals = func(xvals, *popt)
    print(yvals)
    # 拟合，将数组作为函数的参数进行传入。
    return popt, pcov, xvals, yvals


def loadVariables():
    return {}
    import novalmber
    path = novalmber.getUserDataPath(debug=False)  # 通过网络直接远程获取。
    a = __file__.split('apps')[0]

    import os
    import pickle
    path = os.path.join(path, 'pluginfiles/scientificshell')
    print(path)
    varDic = {}

    dirList = os.listdir(path)
    print(dirList)
    for file in dirList:
        if file.endswith('.pkl'):
            sl = file.split('.')

            try:
                f = open(os.path.join(path, file), 'rb')
                name = sl[0]
                varDic[name] = pickle.load(f)
                f.close()
            except:
                import traceback
                traceback.print_exc()
    print(varDic)
    return varDic


if __name__ == '__main__':
    check_identifiers('a,b,c,d,e', 'a+b+c/(c**8)')
    check_identifiers('a,b,c', 'a+b+c/(c**8)')
    check_identifiers('a,b,c', 'sin(a)+b+c/(c**8)')
    check_identifiers('a,b,c', 'a+b+c1/(c**8)')
