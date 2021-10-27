import unittest
from lib.comm.data_client import get_vars, get_var_names, shm_get_vars, set_vars, \
    shm_set_vars


def transfer(case: unittest.TestCase, protocol: int):
    test_list = [1, 2, 3, 4, 5, 6, 7, 8]
    shm_set_vars({'a': 123, 'b': 3456, 'c': test_list}, protocol=protocol)
    vars = shm_get_vars(['a', 'b', 'c'], protocol=protocol)
    assert vars['a'] == 123
    assert vars['b'] == 3456
    case.assertListEqual(vars['c'],test_list)


class Test(unittest.TestCase):  # 继承unittest.TestCase

    def test_data_transfer(self):
        for protocol in [2, 3, 4, 5]:
            transfer(self, protocol)


if __name__ == '__main__':
    unittest.main()  # 运行所有的测试用例
