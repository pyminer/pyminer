import os

import cloudpickle
import sympy
import pytest
import pickle
import cloudpickle


# 默认的pickle对于动态类型是无法进行导入导出的，因此采用此测试用例检测cloudpickle是否可以实现此功能。
# 这一部分本想写成multiprocessing的测试用例，奈何cloudpickle似乎不支持保存进程中的对象，故采用run的方式手动测试。

def test_dump_dynamic_type():
    def wrapper():
        class A:
            b = 123

            def __init__(self):
                self.c = 234

        return A

    a = wrapper()()
    with open('a.pkl', mode='wb') as f:
        cloudpickle.dump(a, f)
    with open('a2.pkl', mode='wb') as f:
        with pytest.raises(AttributeError):
            pickle.dump(a, f)
    os.path.exists('a2.pkl') and os.remove('a2.pkl')
    with open('a3.pkl', mode='wb') as f:
        with pytest.raises(cloudpickle.PicklingError):
            cloudpickle.dump(a, f)
    os.path.exists('a3.pkl') and os.remove('a3.pkl')


def test_load_dynamic_type():
    with open('a.pkl', mode='rb') as f:
        a = cloudpickle.load(f)
    assert a.b == 123
    assert a.c == 234
    os.remove('a.pkl')


def test_dump_sympy_function():
    x = sympy.symbols('x')
    f = sympy.Function('F')
    u = f(x)
    with open('b.pkl', mode='wb') as f:
        cloudpickle.dump(u, f)
    with open('b2.pkl', mode='wb') as f:
        with pytest.raises(pickle.PicklingError):  # 很怪，前一次报错ValueError，此处报错PicklingError
            pickle.dump(u, f)
    os.path.exists('b2.pkl') and os.remove('b2.pkl')
    with open('b3.pkl', mode='wb') as f:
        with pytest.raises(pickle.PicklingError):
            cloudpickle.dump(u, f)
    os.path.exists('b3.pkl') and os.remove('b3.pkl')


def test_load_sympy_function():
    with open('b.pkl', mode='rb') as f:
        f = cloudpickle.load(f)
        assert str(f) == 'F(x)'
    os.remove('b.pkl')
