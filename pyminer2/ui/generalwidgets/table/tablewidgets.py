# 通用表格控件
# 作者：侯展意
# 带有加载数据集等等的功能，相对来讲比较方便。
# 以PMG作为名字开头的控件，不依赖于主界面，只是会和主界面之间传递信号。

import sys

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QApplication, QTabWidget, QTableWidget, QTableWidgetItem, \
    QAbstractItemView


class PMGTableWidget(QTableWidget):
    data_name: str = ''
    data_shown = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setRowCount(1)
        self.setColumnCount(1)

    def closeEvent(self, a0: 'QCloseEvent') -> None:
        print('close!!')
        super().closeEvent(a0)

    @staticmethod
    def check_data_can_be_displayed_by_table(data: object) -> bool:
        try:
            if not hasattr(data, '__len__'):
                return True

            rows = len(data)
            max_cols = 0
            for i, row_contents in enumerate(data):
                if hasattr(row_contents, '__iter__'):
                    col_span = len(row_contents)
                    a = row_contents[i]  # 尝试index第0项。
                else:
                    col_span = 1
                if col_span > max_cols:
                    max_cols = col_span

            columns = max_cols
            for row, row_content in enumerate(data):
                if hasattr(row_content, '__iter__'):
                    print(row_content, hasattr(row_content, '__iter__'))
                    for col, content in enumerate(row_content):
                        a = data[row][col]
                else:
                    a = data[row]
                return True

        except:
            # import traceback
            # traceback.print_exc()
            return False

    def set_data_2d(self, data_name, data: 'np.ndarray', rows: int = None,
                    columns: int = None):

        self.data_name = data_name
        if not hasattr(data, '__len__'):
            item = QTableWidgetItem(str(data))
            self.setItem(0, 0, item)
            return
        if rows is None or columns is None:
            rows = len(data)
            max_cols = 0
            for row_contents in data:
                if hasattr(row_contents, '__iter__'):
                    col_span = len(row_contents)
                else:
                    col_span = 1
                if col_span > max_cols:
                    max_cols = col_span
            columns = max_cols
        self.setColumnCount(columns)
        self.setRowCount(rows)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        for row, row_content in enumerate(data):
            if hasattr(row_content, '__iter__'):
                print(row_content, hasattr(row_content, '__iter__'))
                for col, content in enumerate(row_content):
                    item = QTableWidgetItem(str(data[row][col]))
                    self.setItem(row, col, item)
            else:
                item = QTableWidgetItem(str(data[row]))
                self.setItem(row, 0, item)


class PMGTableTabWidget(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.currentChanged.connect(lambda: print(self.currentIndex()))  # 4


if __name__ == '__main__':
    import numpy as np

    app = QApplication(sys.argv)
    l = ['hhhhhhhhhhhhhh',
         ['a', 'v'],
         [1, 2, 3, 4],
         [3, 4, 5, 66, 7],
         [123, '333', 'ffffffff']
         ]
    demo = PMGTableWidget()

    demo.set_data_2d('a', l)

    demo.show()
    sys.exit(app.exec_())
