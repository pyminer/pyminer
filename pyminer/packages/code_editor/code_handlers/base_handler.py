from functools import cached_property
from typing import Tuple, Type, List, Optional

from packages.code_editor.utils.base_object import CodeEditorBaseObject


class BaseAnalyzer(CodeEditorBaseObject):
    """
    在每次进行代码分析的时候都创建一遍这个对象。
    这个对象的好处是所有的属性计算都是惰性的，按需计算，降低性能损耗。
    """

    def __init__(self, code: str, cursor: int, selection_range: Optional[Tuple[int, int]] = None):
        self.code: str = code
        self.cursor: int = cursor
        self.selection_range: Tuple[int, int] = selection_range if selection_range is not None else (cursor, cursor)

    @cached_property
    def has_selection(self):
        return self.selection_range[0] != self.selection_range[1]

    @cached_property
    def lines(self) -> List[str]:
        return self.code.split('\n')

    @cached_property
    def lines_with_end(self):
        return [f'{line}\n' for line in self.lines]

    @cached_property
    def current_line_index(self) -> int:
        """行的位置，用于进行索引，从0开始"""
        return self.code[:self.cursor].count('\n')

    @cached_property
    def current_line_number(self) -> int:
        """行号，用于进行显示，从1开始"""
        return self.current_line_index + 1

    @cached_property
    def selected_code(self):
        """获取选中的代码或者当前行的代码"""
        if self.has_selection:
            return self.code[self.selection_range[0]:self.selection_range[1]]
        else:
            return self.lines[self.current_line_index]


class BaseHandler(CodeEditorBaseObject):
    """
    代码的执行、格式化、分析等所有工作都应写在这个类及其子类下。

    这里相当于是界面的后端，所有的对代码的操作都应该放在这里。
    """
    analyzer_class: Type[BaseAnalyzer] = BaseAnalyzer
    analyzer: BaseAnalyzer = None

    def __init__(self, path='Untitled'):
        self.path = path

    def feed(self, code: str, position: int, selection_range: Tuple[int, int]):
        """输入代码，以用于分析等操作

        这个更新的方式为增量更新，仅当参数与上一次的参数不一致时，才创建新的analyzer对象。

        Args:
            code: 代码，应该是plainText
            position: 游标的位置，是一个整数，而不是行列号
            selection_range: 选区的位置，是一对整数，表示起止位置，而不是行列号
        """
        a = self.analyzer
        if a is not None:
            if (code, position, selection_range) == (a.code, a.cursor, a.selection_range):
                return
        self.analyzer = self.analyzer_class(code, position, selection_range)

    def run_code(self, code: str, hint: str = 'run code'):
        """运行一段代码

        Args:
            code: 代码
            hint: 代码的标题
        """
        self._not_implemented_error(self.tr('run code'))

    def run_selected_code(self):
        """运行选中的代码"""
        self._not_implemented_error(self.tr('run selected code'))

    def format_code(self) -> analyzer_class:
        return self.analyzer
