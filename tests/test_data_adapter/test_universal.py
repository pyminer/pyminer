"""
本模块用于测试基本类型
"""

import collections
from unittest import TestCase

import numpy
import pandas

from features.workspace.data_adapter import UniversalAdapter


class TestUniversal(TestCase):
    def test_normal(self):
        """正常使用情况下的测试。"""
        ba = UniversalAdapter(123)
        self.assertEqual(ba.shape, ())
        self.assertDictEqual(ba.abstract, {
            'shape': [],
        })
        self.assertEqual(UniversalAdapter.load(ba.dump()).data, ba.data)
        self.assertEqual(ba.get_array(), 123)
        self.assertListEqual(list(ba.get_header_name(0)), ['0'])
        self.assertListEqual(list(ba.get_header_name(1)), ['0'])
        with self.assertRaises(AssertionError):
            ba.get_header_name(2)
        with self.assertRaises(AssertionError):
            ba.get_header_name(-1)

    def test_complex_objects(self):
        data = collections.OrderedDict()
        data['a'] = 123
        data['b'] = {1, 2, 3, 4, 5}
        self.assertEqual(UniversalAdapter.load(UniversalAdapter(data).dump()).data, data)

        # TODO (panhaoyu) sympy公式暂时无法进行传输，采用共享内存等方案可以解决，后期补全。
        # 这个问题的原因是，f是一个类，而f(a)的类型是f，但这个f是一个动态类型，pickle找不到，因此报错。
        # a = sympy.symbols('a')
        # f = sympy.Function('f')
        # data = f(a)
        # assert UniversalAdapter.load(UniversalAdapter(data).dump()).data == data

        data = pandas.DataFrame(data=[[1, 'Tom'], [2, 'Jerry'], [3, 'John']], columns=['id', 'name'])
        numpy.testing.assert_array_equal(UniversalAdapter.load(UniversalAdapter(data).dump()).data, data)
