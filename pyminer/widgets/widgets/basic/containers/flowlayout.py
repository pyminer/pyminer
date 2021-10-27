from PySide2.QtWidgets import QGridLayout, QWidget, QSizePolicy


class PMFlowLayoutWithGrid(QGridLayout):
    """
    流式布局，继承自QGridLayout，以Grid的方式添加widget。
    主要作用是在保证兼容代码的基础上，做到流式布局。
    """

    def __init__(self, parent=None, column_width=100):
        super().__init__(parent)

        self.column_width = column_width
        self.widgets_list = []

    def addWidget(self, w: QWidget, row: int, column: int,
                  rowSpan: int, columnSpan: int) -> None:
        """
        添加控件的方法。多了一个列表将所有的控件存储起来。当然，不允许重复添加。
        :param w:
        :param row:
        :param column:
        :param rowSpan:
        :param columnSpan:
        :return:
        """
        if w not in self.widgets_list:
            self.widgets_list.append(w)
        super().addWidget(w, row, column, rowSpan, columnSpan)

    def on_resize(self):
        """
        在界面放大缩小的时候，会将按钮重新排布。按照表格上从上到下、从左到右的顺序，就像下面这样：
        注意这个方法无法自动调用，只能依靠它的父控件。
        1 2 3 4
        5 6 7 8
        9
        :return:
        """
        geometry = self.geometry()
        cols = int(geometry.width() / self.column_width)

        if cols == self.columnCount():
            return
        row = 0
        col = 0
        for i in range(len(self.widgets_list)):
            w = self.widgets_list[i]
            self.removeWidget(w)
            self.addWidget(w, row, col, 1, 1)
            col += 1
            if col == cols:
                row += 1
                col = 0


class PMFlowLayout(QGridLayout):
    def __init__(self, parent=None, initial_columns=3, column_width=100):
        super().__init__(parent)

        self.column_width = column_width
        self.widgets_list = []
        self.occupy_widget = QWidget()
        self.occupy_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

    def add_widget(self, w: QWidget) -> None:
        """
        添加控件的方法。多了一个列表将所有的控件存储起来。当然，不允许重复添加。
        :param w:
        :param row:
        :param column:
        :param rowSpan:
        :param columnSpan:
        :return:
        """

        if w not in self.widgets_list:
            self.widgets_list.append(w)
        items = len(self.widgets_list)
        geometry = self.geometry()
        cols = int(geometry.width() / self.column_width)
        if cols == 0:
            cols = 3
        current_row = int(items / cols)
        current_col = int(items % cols)
        super().addWidget(w, current_row, current_col, 1, 1)

    def on_resize(self):
        """
        在界面放大缩小的时候，会将按钮重新排布。按照表格上从上到下、从左到右的顺序，就像下面这样：
        注意这个方法无法自动调用，只能依靠它的父控件。
        1 2 3 4
        5 6 7 8
        9
        :return:
        """
        geometry = self.geometry()
        cols = int(geometry.width() / self.column_width)

        if cols == self.columnCount():
            return
        row = 0
        col = 0
        for i in range(len(self.widgets_list)):
            w = self.widgets_list[i]
            self.removeWidget(w)
            self.addWidget(w, row, col, 1, 1)
            col += 1
            if col == cols:
                row += 1
                col = 0
        self.removeWidget(self.occupy_widget)
        self.addWidget(self.occupy_widget, row, col, 1, 1)
