"""
规则编辑面板
"""
import sys
from typing import List, Union, Tuple, Dict, TYPE_CHECKING, Callable, Optional

from PySide2.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QHBoxLayout, QPushButton, QTableWidgetItem, QHeaderView
if TYPE_CHECKING:
    import pandas as pd
    from widgets import PANEL_VIEW_CLASS
if __name__ == '__main__':
    from widgets.widgets.extended.base import BaseExtendedWidget
else:
    from ..base import BaseExtendedWidget



def parse_simplified_expression(identifier, title, data) -> Optional[List[Union[int, str, float, bool]]]:
    """
    解析简化版的json数据！
    :param identifier:
    :param data:
    :param params:
    :return:
    """

    if isinstance(data, bool):
        return ['check_ctrl', identifier, title, data]

    elif isinstance(data, (int, float)):

        return ['numberspin_ctrl', identifier, title, data]

    elif isinstance(data, str):
        return ['line_ctrl', identifier, title, data]

    else:
        raise ValueError('cannot parse' + repr(data))


class PMGRuleCtrl(BaseExtendedWidget):
    """
    rules:
    {'name':'regex',
    'text':'匹配正则表达式',
    'init':False
    }
    """

    def __init__(self, layout_dir='v', title='', rules: List[Dict[str, Union[bool, int, float, str]]] = None):
        super().__init__(layout_dir)
        self.table_h_headers = []
        self.table_keys = []
        self.initial_values = []
        for rule in rules:
            self.table_h_headers.append(rule['text'])
            self.table_keys.append(rule['name'])
            self.initial_values.append(rule['init'])
        self.regulations_table = QTableWidget(0, len(self.table_h_headers))
        self.regulations_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.regulations_table.setHorizontalHeaderLabels(self.table_h_headers)

        self.layout().addWidget(self.regulations_table)
        self.set_layout = QHBoxLayout()
        self.layout().addLayout(self.set_layout)
        self.button_add = QPushButton('Add')
        self.button_remove = QPushButton('Remove')
        self.set_layout.addWidget(self.button_add)
        self.set_layout.addWidget(self.button_remove)
        self.button_add.clicked.connect(self.add_regulation)
        self.button_remove.clicked.connect(self.remove_regulation)

    def load_regulations(self, regulations: List[Dict[str, Union[int, str, float, bool]]]):
        row_count = len(regulations)
        self.regulations_table.setRowCount(row_count)
        for i, regulation in enumerate(regulations):
            l = [regulation[k] for k in self.table_keys]
            for j, obj in enumerate(l):
                item = QTableWidgetItem()
                item.setData(0, obj)
                self.regulations_table.setItem(i, j, item)

    def add_regulation(self):
        rc = self.regulations_table.rowCount()
        self.regulations_table.setRowCount(rc + 1)
        for i, obj in enumerate(self.initial_values):
            item = QTableWidgetItem()
            item.setData(0, obj)
            self.regulations_table.setItem(rc, i, item)

    def remove_regulation(self):
        self.regulations_table.removeRow(self.regulations_table.currentRow())

    def get_value(self) -> List[Dict]:
        l = []
        for i in range(self.regulations_table.rowCount()):
            dic = {}
            for j in range(self.regulations_table.columnCount()):
                item = self.regulations_table.item(i, j)
                dic[self.table_keys[j]] = item.data(0)
            l.append(dic)
        return l

    def set_value(self, value):
        self.load_regulations(value)


if __name__ == '__main__':
    from PySide2.QtWidgets import QApplication

    app = QApplication([])
    rc = PMGRuleCtrl(rules=[
        {'name': 'property1', 'text': '属性1', 'init': '字符串属性'},
        {'name': 'property2', 'text': '属性2', 'init': True},
        {'name': 'property3', 'text': '属性3', 'init': False},
        {'name': 'property4', 'text': '属性4', 'init': 0},
    ])
    rc.show()
    rc.set_value([
        {'property1': 'aaa', 'property2': False, 'property3': True, 'property4': 1},
        {'property1': 'whatif', 'property2': False, 'property3': False, 'property4': 12}
    ])
    print(rc.get_value())
    app.exec_()
