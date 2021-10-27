"""
本模块用于进行数据适配器的类型自动识别功能的测试，
包括类型的注册与查询等操作。
"""

from unittest import TestCase

from numpy import ndarray, array
from pandas import DataFrame

from features.workspace.data_adapter import Detector
from features.workspace.data_adapter import UniversalAdapter, ArrayAdapter
from features.workspace.data_adapter.data_frame import DataFrameAdapter


class TestDetector(TestCase):
    def setUp(self) -> None:
        self.detector = Detector()

    def test_recognize_data(self):
        adapter = self.detector.detect('test string')
        self.assertEqual(adapter.data, 'test string')
        # 这里采用 ``type(adapter)`` 而不是 ``isinstance`` 是由于我们希望精确地测试是否获取到了我们需要的类。
        self.assertEqual(type(adapter), UniversalAdapter)

    def test_register_new_adapter(self):
        adapter = self.detector.detect(array([1, 2, 3]))
        self.assertEqual(type(adapter), UniversalAdapter)
        self.detector.register(ndarray, ArrayAdapter)
        adapter = self.detector.detect(array([1, 2, 3]))
        self.assertEqual(type(adapter), ArrayAdapter)
        adapter = self.detector.detect([1, 2, 3])
        self.assertEqual(type(adapter), UniversalAdapter)

    def test_init_function(self):
        self.assertEqual(type(self.detector.detect(array([1, 2, 3]))), UniversalAdapter)
        self.detector.init_builtin_adapters()
        self.assertEqual(type(self.detector.detect(array([1, 2, 3]))), ArrayAdapter)

    def test_replace_adapter(self):
        self.detector.init_builtin_adapters()
        with self.assertRaisesRegex(ValueError, 'replace=True'):
            self.detector.register(ndarray, ArrayAdapter)


class TestBuiltinDataTypes(TestCase):
    def setUp(self) -> None:
        self.detector = Detector()
        self.detector.init_builtin_adapters()

    def test_universal(self):
        class A(object):
            def __repr__(self):
                return 'This is A'

        adapter = self.detector.detect(A())
        self.assertEqual(str(adapter.get_array()), 'This is A')
        self.assertIsInstance(adapter, UniversalAdapter)

    def test_data_frame(self):
        df = DataFrame(((i for i in range(10)) for j in range(10)))
        adapter = self.detector.detect(df)
        self.assertIsInstance(adapter, DataFrameAdapter)

    def test_nd_array(self):
        ar = array(range(100))
        adapter = self.detector.detect(ar)
        self.assertIsInstance(adapter, ArrayAdapter)
