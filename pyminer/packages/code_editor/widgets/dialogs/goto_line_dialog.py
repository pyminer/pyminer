from typing import Callable

from PySide2.QtWidgets import QDialog, QMessageBox

from ..ui.gotoline import Ui_DialogGoto


class PMGotoLineDialog(QDialog, Ui_DialogGoto):
    tr: Callable[[str], str]

    def __init__(self, parent=None):
        super(PMGotoLineDialog, self).__init__(parent)
        self.current_line = -1
        self.max_row_count = 0
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.run_goto)
        self.buttonBox.rejected.connect(self.reject)

    def set_max_row_count(self, length: int):
        """
        设置最大可跳转的行数
        :param length:
        :return:
        """
        self.max_row_count = length

    def set_current_line(self, line: int):
        """
        line：从0开始
        :param line:
        :return:
        """
        self.current_line = line
        self.lineEdit.setText(str(line + 1))

    def run_goto(self):
        """
        跳转到行
        :return:
        """
        text = self.lineEdit.text()
        if not text.isdecimal():
            QMessageBox.warning(self, self.tr('Input Value Error'), self.tr('Cannot convert \'%s\' to integer.') % text)
            return
        line = int(text)
        if not 0 <= line < self.max_row_count:
            QMessageBox.warning(self, self.tr('Input Value Error'),
                                self.tr('Line Number {line} out of range!').format(line=line))
            return
        self.accept()

    def get_line(self) -> int:
        return int(self.lineEdit.text())
