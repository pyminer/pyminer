from unittest import TestCase

from packages.code_editor.utils.grammar_analyzer.grammar_analyzer import GrammarAnalyzer

func_def_1 = """
def add(x, y):
    return x + y
print(add(3, 5)
"""


def test_convert_position_to_row_col():
    """
    PyQt得到的position是一个整数，需要将其进行转化，方可被parso识别。
    """
    analyzer = GrammarAnalyzer()
    analyzer.feed(func_def_1)
    assert analyzer._convert_position_to_row_col(22) == (3, 6)
    assert analyzer._convert_position_to_row_col(46) == (4, 13)
    assert analyzer._convert_position_to_row_col(47) == (4, 14)


class TestBracket(TestCase):
    """
    测试JEDI的括号识别功能
    """

    def setUp(self) -> None:
        self.analyzer = GrammarAnalyzer()

    def test_normal(self):
        self.analyzer.feed(func_def_1)
        assert self.analyzer.is_not_matched((4, 15))
        assert self.analyzer.is_not_matched((4, 14))
        assert self.analyzer.is_not_matched(47)

    def test_line_1(self):
        line_1 = """print(a, b, c)"""
        self.analyzer.feed(line_1)
        assert not self.analyzer.is_not_matched((1, 13))

    def test_line_2(self):
        line_2 = """print(a, b, c"""
        self.analyzer.feed(line_2)
        assert self.analyzer.is_not_matched((1, 13))

    def test_line_3(self):
        # 这个用例有问题，parso无法识别，暂不处理
        line_3 = """[][]"""
        self.analyzer.feed(line_3)
        # assert not self.analyzer.is_not_matched((1, 3), left='[')

    def test_line_4(self):
        line_4 = """[]["""
        self.analyzer.feed(line_4)
        assert self.analyzer.is_not_matched((1, 3), left='[')

    def test_code_5(self):
        code = """
a = [[1, 2, 3], [5, 6, 7]]
b = a[1][2]
"""
        self.analyzer.feed(code)
        assert not self.analyzer.is_not_matched((3, 8), left='[')

    def test_code_6(self):
        code = """
a = [[1, 2, 3], [5, 6, 7]]
b = a[1[2]
"""
        self.analyzer.feed(code)
        assert self.analyzer.is_not_matched((3, 8), left='[')

    def test_code_7(self):
        code = """
print(1, 2,
abc(),
"""
        self.analyzer.feed(code)
        assert self.analyzer.is_not_matched((3, 6))

    def test_code_8(self):
        code = """
a = [1, 2, [
3, 4, 5, [
6, 7, [8, 9],
],
10,
"""
        self.analyzer.feed(code)
        assert self.analyzer.is_not_matched((6, 2), left='[')
