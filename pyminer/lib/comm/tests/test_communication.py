import unittest
from lib.comm import set_vars, set_var, get_vars, get_var_names, get_var
from lib.comm import get_style_sheet, get_settings, modify_settings
from lib.comm.base import get_protocol, is_pyminer_service_started, DataDesc


class Test(unittest.TestCase):  # 继承unittest.TestCase

    def test_data_transfer(self):
        if is_pyminer_service_started():
            print(get_protocol())
            test_list = [1, 2, 3, 4, 5, 6, 7, 8]
            set_vars({'a': 123, 'b': 3456, 'c': test_list})
            vars = get_vars(['a', 'b', 'c'])
            assert vars['a'] == 123
            assert vars['b'] == 3456
            self.assertListEqual(vars['c'], test_list)
            set_var('a', 4567)
            assert get_var('a') == 4567
            self.assertListEqual(get_var('c'), test_list)
            vars_in_workspace = get_var_names()
            for var_name in ['a', 'b', 'c']:
                assert var_name in vars_in_workspace
        else:
            print('PyMiner未启动')

    def test_data_desc(self):
        if is_pyminer_service_started():
            set_var('desc_a', DataDesc(123))
            set_var('desc_b', DataDesc([1, 2, 3, 4]))

    def test_configs(self):
        if is_pyminer_service_started():
            assert isinstance(get_settings(), dict)
            assert isinstance(get_style_sheet(), str)
            print(get_settings())
            modify_settings({'theme': 'Fusion'})
            # time.sleep(1)
            modify_settings({'theme': 'QDarkStyle'})
        else:
            print('PyMiner未启动')


if __name__ == '__main__':
    unittest.main()  # 运行所有的测试用例
