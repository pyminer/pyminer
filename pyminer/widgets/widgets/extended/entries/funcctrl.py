import ast
import astunparse
from typing import Any, Tuple, List

from PySide2.QtWidgets import QLineEdit, QLabel, QHBoxLayout, QPushButton, QMessageBox

from widgets.widgets.extended.base.baseextendedwidget import BaseExtendedWidget


class CodeVisitor(ast.NodeVisitor):
    def __init__(self):
        super(CodeVisitor, self).__init__()
        self.preserved = {"pi", "e"}
        self.called = set()
        self.func_args = set()
        self._names = set()

    def visit_Name(self, node: ast.Name) -> Any:
        self._names.add(node.id)


    def visit_Call(self, node: ast.Call) -> Any:
        self.generic_visit(node)
        self.called.add(node.func.id)

    def get_result(self) -> Tuple[List[str], List[str]]:
        """

        Returns: 定义的名称，以及调用的ID名称。

        """
        names = self._names.copy()
        names.difference_update(self.preserved)
        names.difference_update(self.called)
        return list(names), list(self.called)


# n = ast.parse("x*cos(v,sin(2*pi*x))")
# print(CodeVisitor().visit(n))
# print(cv := CodeVisitor())
# cv.visit(n)
# print(cv.get_result())
# # # print(ast.get_source_segment("x*cos(v,sin(2*pi*x))",n))
# # print(ast.dump(n))
# # print(astunparse.unparse(n))


class PMGFuncCtrl(BaseExtendedWidget):
    """

    输入：一个有效的函数表达式。
    其中，里面的变量名会自动进行检测。

    """

    def __init__(self, layout_dir: str, title: str, initial_value: str):
        super().__init__(layout_dir)
        self.allowed_chars = set(' ,[](){}:1234567890.+-*/')
        self.on_check_callback = None
        self.prefix = QLabel(text=title)
        self.type = type
        entryLayout = QHBoxLayout()
        self.ctrl = QLineEdit()
        self.central_layout.addWidget(self.prefix)
        self.central_layout.addLayout(entryLayout)
        entryLayout.addWidget(self.ctrl)
        self.set_value(initial_value)

    def get_code(self) -> str:
        text = self.ctrl.text()
        if self.type == 'safe':
            for char in text:
                if char not in self.allowed_chars:
                    return None
        return text

    def set_value(self, obj: Any):
        try:
            self.ctrl.setText(repr(obj))
        except:
            import traceback
            traceback.print_exc()

    def get_value(self) -> object:
        if self.get_code() is not None:
            try:
                return eval(self.ctrl.text())
            except:
                import traceback
                traceback.print_exc()
                return None
        else:
            return None

    def on_eval_test(self):
        """
        点击计算按钮，弹出对话框显示计算结果。
        :return:
        """
        val = self.get_value()
        QMessageBox.information(self, self.tr('Result'), repr(val), QMessageBox.Ok)
