import unittest
from utils.io.fileutil.search_in_path import word_in_line


class MyTest(unittest.TestCase):

    def test_match_word_and_match_case(self):
        assert word_in_line('Abs', 'Abs 123456', True, True)
        assert not word_in_line('abs', 'Abs 123456', True, True)
        assert not word_in_line('Abs', 'aAbs', True, True)
        assert not word_in_line('Abs', 'Absa', True, True)
        assert not word_in_line('Abs', 'Abs哈哈哈', True, True)
        assert not word_in_line('Abs', '哈哈哈哈Abs', True, True)
        assert word_in_line('Abs', '哈哈哈哈.Abs', True, True)
        assert word_in_line('Abs', '哈哈哈哈?Abs', True, True)
        assert word_in_line('Abs', '哈哈哈哈(Abs', True, True)
        assert word_in_line('Abs', '哈哈哈哈)Abs', True, True)
        assert word_in_line('Abs', '哈哈哈哈[Abs', True, True)
        assert word_in_line('Abs', '哈哈哈哈[Abs]', True, True)

    def test_match_word_only(self):
        assert word_in_line('Abs', 'Abs 123456', True, False)
        assert word_in_line('abs', 'Abs 123456', True, False)
        assert not word_in_line('Abs', 'aAbs', True, False)
        assert not word_in_line('Abs', 'Absa', True, False)
        assert not word_in_line('Abs', 'Abs哈哈哈', True, False)
        assert not word_in_line('Abs', '哈哈哈哈Abs', True, False)
        assert word_in_line('Abs', '哈哈哈哈.Abs', True, False)
        assert word_in_line('Abs', '哈哈哈哈?abs', True, False)
        assert word_in_line('Abs', '哈哈哈哈(Abs', True, False)
        assert word_in_line('Abs', '哈哈哈哈(abs', True, False)
        assert word_in_line('Abs', '哈哈哈哈a)Abs', True, False)
        assert word_in_line('Abs', '哈哈哈哈[Abs', True, False)
        assert word_in_line('Abs', '哈哈哈哈[Abs]', True, False)

    def test_match_case_only(self):
        assert word_in_line('Abs', 'Abs 123456', False, True)
        assert not word_in_line('abs', 'Abs 123456', False, True)
        assert word_in_line('abs', 'abs 123456', False, True)
        assert word_in_line('Abs', 'aAbs', False, True)
        assert word_in_line('Abs', 'Absa', False, True)
        assert word_in_line('Abs', 'Abs哈哈哈', False, True)
        assert word_in_line('Abs', '哈哈哈哈Abs', False, True)
        assert word_in_line('Abs', '哈哈哈哈.Abs', False, True)
        assert not word_in_line('Abs', '哈哈哈哈?abs', False, True)
        assert word_in_line('Abs', '哈哈哈哈(Abs', False, True)
        assert not word_in_line('Abs', '哈哈哈哈(abs', False, True)
        assert word_in_line('Abs', '哈哈哈哈a)Abs', False, True)
        assert word_in_line('Abs', '哈哈哈哈[Abs', False, True)
        assert word_in_line('Abs', '哈哈哈哈[Abs]', False, True)

    def test_match_nothing(self):
        assert word_in_line('Abs', 'Abs 123456', False, False)
        assert word_in_line('abs', 'Abs 123456', False, False)
        assert word_in_line('abs', 'abs 123456', False, False)
        assert word_in_line('Abs', 'aAbs', False, False)
        assert word_in_line('Abs', 'Absa', False, False)
        assert word_in_line('Abs', 'Abs哈哈哈', False, False)
        assert word_in_line('Abs', '哈哈哈哈Abs', False, False)
        assert word_in_line('Abs', '哈哈哈哈.Abs', False, False)
        assert word_in_line('Abs', '哈哈哈哈?abs', False, False)
        assert word_in_line('Abs', '哈哈哈哈(Abs', False, False)
        assert word_in_line('Abs', '哈哈哈哈(abs', False, False)
        assert word_in_line('Abs', '哈哈哈哈a)Abs', False, False)
        assert word_in_line('Abs', '哈哈哈哈[Abs', False, False)
        assert word_in_line('Abs', '哈哈哈哈[Abs]', False, False)
        assert not word_in_line('Abs', 'ab哈s哈a哈哈[Ab]', False, False)


if __name__ == '__main__':
    unittest.main()  # 运行所有的测试用例
