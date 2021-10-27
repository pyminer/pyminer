# -*- coding:utf-8 -*-
# @Time: 2021/1/15 19:57
# @Author: Zhanyi Hou
# @Email: 1295752786@qq.com
# @File: findinpath.py
import os
from typing import List, Tuple
from widgets import PMDockObject
from utils import search_in_path
from PySide2.QtWidgets import QDialog, QApplication, QVBoxLayout, QListWidget, QHBoxLayout, QPushButton, QCheckBox, \
    QLineEdit, QListWidgetItem
from PySide2.QtCore import Signal


class FindInPathWidget(QDialog, PMDockObject):
    signal_open_file_line = Signal(str, int)  # 文件绝对路径；文件行号

    def __init__(self, parent=None, path: str = ''):
        super(FindInPathWidget, self).__init__(parent)
        self._path: str = path
        self._result: List[Tuple[int, str, str]] = None
        self.setLayout(QVBoxLayout())
        self.text_to_find_entry = QLineEdit()
        self.layout().addWidget(self.text_to_find_entry)

        result_list = QListWidget()
        self.result_list_widget = result_list
        self.layout().addWidget(result_list)
        h_layout = QHBoxLayout()

        self.layout().addLayout(h_layout)
        self.check_match_case = QCheckBox()
        self.check_match_case.setText(self.tr('Case'))
        self.check_match_whole_word = QCheckBox()
        self.check_match_whole_word.setText(self.tr('Whole Word'))
        self.button_find = QPushButton(self.tr('Find'))

        h_layout.addWidget(self.check_match_whole_word)
        h_layout.addWidget(self.check_match_case)
        h_layout.addWidget(self.button_find)

        self.button_find.clicked.connect(self.slot_find)
        self.result_list_widget.itemDoubleClicked.connect(self.slot_goto_pos)

    def get_widget_text(self) -> str:
        return self.tr('Find In Path')

    def set_path(self, path: str):
        assert os.path.isdir(path)
        self._path = path

    def set_word(self, word: str):
        self.text_to_find_entry.setText(word)

    def slot_find(self):
        self.run_find(self._path)

    def run_find(self, path: str):
        """

        Args:
            path:

        Returns:

        """
        word = self.text_to_find_entry.text()
        result: List[Tuple[int, str, str]] = None
        if word == '':
            result = []
        else:
            result = search_in_path(word, path, self.check_match_case.isChecked(),
                                    self.check_match_whole_word.isChecked())
        print(result)
        self.set_result(result)

    def set_result(self, result: List[Tuple[int, str, str]]):
        """

        Args:
            result:

        Returns:

        """
        self.result_list_widget.clear()
        self._result = result
        for result in self._result:
            item = QListWidgetItem()
            rel_path = os.path.relpath(result[2], self._path)
            item.setText(rel_path + ',' + self.tr('line') + str(result[0]) + '\n' + result[1])
            self.result_list_widget.addItem(item)

    def slot_goto_pos(self, item: QListWidgetItem):
        current_row = self.result_list_widget.currentRow()
        if 0 <= current_row < len(self._result):
            file_name = self._result[current_row][2]
            row = self._result[current_row][0]
            self.signal_open_file_line.emit(file_name, row)


if __name__ == "__main__":
    import cgitb

    cgitb.enable()
    app = QApplication([])
    fip = FindInPathWidget(path=r'C:\Users\12957\Documents\Developing\Python\PyMiner_dev_kit\bin\pmtoolbox\io\fileutil')
    fip.text_to_find_entry.setText('print')
    fip.show()
    app.exec_()
