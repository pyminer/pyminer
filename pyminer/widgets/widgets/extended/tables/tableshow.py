from typing import List, Union

from PySide2.QtCore import Qt
from PySide2.QtGui import QBrush, QColor
from PySide2.QtWidgets import QHBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView
from ..base import BaseExtendedWidget
from widgets.utilities import color_str2tup


class PMGTableShow(BaseExtendedWidget):
    default_bg = QTableWidgetItem().background()
    default_fg = QTableWidgetItem().foreground()

    def __init__(self, layout_dir: str, title: List[str],
                 initial_value: List[List[Union[int, float, str]]],
                 size_restricted=False, header_adaption_h=False, header_adaption_v=False,
                 background_color: List[List[Union[str]]] = None,
                 foreground_color: List[List[Union[str]]] = None):
        super().__init__(layout_dir=layout_dir)

        self.maximum_rows = 100
        self.size_restricted = size_restricted
        self.header_adaption_h = header_adaption_h
        self.header_adaption_v = header_adaption_v
        self.background_color = background_color if background_color is not None else ''
        self.foreground_color = foreground_color if foreground_color is not None else ''
        self.char_width = 15
        self.on_check_callback = None
        self.title_list = title
        entryLayout = QHBoxLayout()
        entryLayout.setContentsMargins(0, 0, 0, 0)

        self.ctrl = QTableWidget()
        self.ctrl.verticalHeader().setVisible(False)
        self.set_params(size_restricted, header_adaption_h, header_adaption_v)
        self.ctrl.setColumnCount(len(title))

        self.ctrl.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        for i, text in enumerate(title):
            self.ctrl.setColumnWidth(i, len(text) * self.char_width + 10)
            self.ctrl.setHorizontalHeaderItem(i, QTableWidgetItem(text))

        self.central_layout.addLayout(entryLayout)
        entryLayout.addWidget(self.ctrl)

        if initial_value is not None:
            for sublist in initial_value:
                assert len(sublist) == len(title), \
                    'title is not as long as sublist,%s,%s' % (repr(title), sublist)
                self.ctrl.setRowCount(len(initial_value))
                self.set_value(initial_value)

    def set_params(self, size_restricted=False, header_adaption_h=False, header_adaption_v=False):
        self.size_restricted = size_restricted
        self.header_adaption_h = header_adaption_h
        self.header_adaption_v = header_adaption_v
        if header_adaption_h:
            self.ctrl.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        if header_adaption_v:
            self.ctrl.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def check_data(self, value: List[List[Union[int, float, str]]]):
        for sublist in value:
            assert len(sublist) == len(self.title_list),\
                '%s,%s' % (repr(sublist), repr(self.title_list))

    def set_value(self, value: List[List[Union[int, float, str]]]):
        self.check_data(value)
        self.ctrl.setRowCount(len(value))
        cols = len(value[0])
        if isinstance(self.foreground_color, str):
            fg = [[self.foreground_color for i in range(cols)] for j in range(len(value))]

        else:
            fg = self.foreground_color
        if isinstance(self.background_color, str):
            bg = [[self.background_color for i in range(cols)] for j in range(len(value))]
        else:
            bg = self.background_color
        for row, row_list in enumerate(value):
            for col, content in enumerate(row_list):
                if len(str(content)) * self.char_width > self.ctrl.columnWidth(col):
                    self.ctrl.setColumnWidth(col, len(str(content)) * self.char_width + 10)
                table_item = QTableWidgetItem(str(content))
                table_item.setTextAlignment(Qt.AlignCenter)
                # 字体颜色（红色）
                if fg[row][col] == '':
                    table_item.setForeground(self.default_fg)
                else:
                    table_item.setForeground(QBrush(QColor(*color_str2tup(fg[row][col]))))

                # 背景颜色（红色）
                if bg[row][col] == '':
                    table_item.setBackground(self.default_bg)
                else:
                    table_item.setBackground(QBrush(QColor(*color_str2tup(bg[row][col]))))
                self.ctrl.setItem(row, col, table_item)

        if self.size_restricted:
            if self.header_adaption_h:
                self.ctrl.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                scrollbar_area_width = 0
            else:
                self.ctrl.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
                scrollbar_area_width = 10
            self.ctrl.setMaximumHeight((self.ctrl.rowCount() + 1) * 30 + scrollbar_area_width)
            self.setMaximumHeight((self.ctrl.rowCount() + 1) * 30 + scrollbar_area_width)

    def alert(self, alert_level: int):
        self.ctrl.alert(alert_level)

    def add_row(self, row: List):
        assert len(row) == self.ctrl.columnCount()
        rc = self.ctrl.rowCount()
        self.ctrl.setRowCount(rc + 1)
        for i, val in enumerate(row):
            self.ctrl.setItem(rc, i, QTableWidgetItem(str(val)))
        if self.ctrl.rowCount() > self.maximum_rows:
            self.ctrl.removeRow(0)
