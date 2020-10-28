"""
本模块用于测试基本类型
"""

from pyminer2.data_adapter import UniversalAdapter
import pytest
import collections
import sympy
import pandas
import numpy


def test_normal():
    """
    进行正常使用情况下的功能测试
    """
    ba = UniversalAdapter(123)
    assert ba.shape == (1,)
    assert ba.abstract['shape'] == [1]
    assert UniversalAdapter.load(ba.dump()).data == ba.data
    assert ba.get_matrix() == [['123']]  # 由于是采用repr的方式进行输出，因此会显示为字符串
    assert ba.get_header_name(0) == ['1']
    assert ba.get_header_name(1) == ['1']
    with pytest.raises(AssertionError):
        ba.get_header_name(2)
        ba.get_header_name(-1)


def test_complex_objects():
    """
    复杂对象的导出再导入
    """
    # 测试有序矩阵
    data = collections.OrderedDict()
    data['a'] = 123
    data['b'] = {1, 2, 3, 4, 5}
    assert UniversalAdapter.load(UniversalAdapter(data).dump()).data == data

    # TODO (panhaoyu) sympy公式无法进行传输，暂无解决方案，等reco的接口出来后试一下。
    # 这个问题的原因是，f是一个类，而f(a)的类型是f，但这个f是一个动态类型，pickle找不到，因此报错。
    # a = sympy.symbols('a')
    # f = sympy.Function('f')
    # data = f(a)
    # assert UniversalAdapter.load(UniversalAdapter(data).dump()).data == data

    data = pandas.DataFrame(data=[[1, 'Tom'], [2, 'Jerry'], [3, 'John']], columns=['id', 'name'])
    assert numpy.all(UniversalAdapter.load(UniversalAdapter(data).dump()).data == data)
