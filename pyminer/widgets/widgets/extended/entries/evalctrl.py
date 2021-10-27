from typing import Any

from PySide2.QtWidgets import QLineEdit, QLabel, QHBoxLayout, QPushButton, QMessageBox
from widgets.widgets.extended.base.baseextendedwidget import BaseExtendedWidget


class PMGEvalCtrl(BaseExtendedWidget):
    """
    type:
    safe--can only input ',[](){}:1234567890.'
    """

    def __init__(self, layout_dir: str, title: str, initial_value: str, type='normal'):
        super().__init__(layout_dir)
        self.allowed_chars = set(' ,[](){}:1234567890.+-*/')
        self.on_check_callback = None
        self.prefix = QLabel(text=title)
        self.type = type
        entryLayout = QHBoxLayout()

        self.ctrl = QLineEdit()

        self.color_button = QPushButton()
        self.color_button.clicked.connect(self.on_eval_test)

        self.central_layout.addWidget(self.prefix)
        self.central_layout.addLayout(entryLayout)
        entryLayout.addWidget(self.ctrl)
        entryLayout.addWidget(self.color_button)
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
