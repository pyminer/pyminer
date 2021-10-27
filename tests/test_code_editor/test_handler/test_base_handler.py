from packages.code_editor.code_handlers.base_handler import BaseAnalyzer

code = '''
a = 1
b = 2
c = 3
print(a, b, c)
'''


# 2的结尾是位置12，3的前面是位置13


def test_current_line_number():
    analyzer = BaseAnalyzer(code, 12)
    assert analyzer.current_line_index == 2
    analyzer = BaseAnalyzer(code, 13)
    assert analyzer.current_line_index == 3


def test_selection():
    analyzer = BaseAnalyzer(code, 12, (12, 12))
    assert not analyzer.has_selection
    assert analyzer.selected_code == 'b = 2'
    analyzer = BaseAnalyzer(code, 12, (12, 17))
    assert analyzer.has_selection
    assert analyzer.selected_code == '\nc = '
