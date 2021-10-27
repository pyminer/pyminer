import os
from typing import Dict, TYPE_CHECKING, Callable, Any

from PySide2.QtWidgets import QTreeWidget, QTreeWidgetItem, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QMenu
from PySide2.QtCore import Signal, Qt, QLocale


class PMGAttrTree(QTreeWidget):
    signal_show_data_value = Signal(str)
    signal_data_saveas = Signal(str)
    signal_data_open = Signal(str)
    select_data_callbacks = []
    extension_lib: 'extension_lib' = None

    def __init__(self, parent=None):
        super().__init__(parent=None)

        self.filter_all_upper_case = False
        self.filter_all_callables = True
        self.setup_ui()

    # def is_item_legal(self, name: str, obj: object):
    #     return (not (callable(obj) and self.filter_all_callables)) and \
    #            (not (name.isupper() and self.filter_all_upper_case))

    def setup_ui(self):
        self.nodes: Dict[str, 'QTreeWidgetItem'] = {}
        self.setColumnCount(3)
        header_item = QTreeWidgetItem()
        header_item.setText(0, self.tr('Name'))
        self.setColumnWidth(0, 10 * 10)
        header_item.setText(1, self.tr('Size'))
        self.setColumnWidth(1, 10 * 10)
        header_item.setText(2, self.tr('Value'))
        header_item.setTextAlignment(0, Qt.AlignCenter)
        header_item.setTextAlignment(1, Qt.AlignCenter)
        header_item.setTextAlignment(2, Qt.AlignCenter)
        self.setHeaderItem(header_item)
        self.auto_expand = False

        self.itemClicked.connect(self.on_item_clicked)
        self.itemDoubleClicked.connect(self.on_item_double_clicked)
        self.customContextMenuRequested.connect(self.on_right_clicked)
        self.setContextMenuPolicy(Qt.CustomContextMenu)

        self.context_menu = QMenu()
        show_action = self.context_menu.addAction(self.tr('View'))
        save_action = self.context_menu.addAction(self.tr('Save as '))
        cancel_action = self.context_menu.addAction(self.tr('Undo'))
        redo_action = self.context_menu.addAction(self.tr('Redo'))
        delete_action = self.context_menu.addAction(self.tr('Delete'))
        show_action.triggered.connect(self.on_show_data_by_context_menu)

    def on_item_clicked(self, item: QTreeWidgetItem, col: int) -> None:
        """
        点击条目时的回调函数。会顺次执行self.select_data_callbacks，而self.select_data_callbacks
        是由插件的add_select_data_callback(self, callback: Callable)方式加入的。
        """
        if item.isExpanded():
            self.collapseItem(item)
        else:
            self.expandItem(item)

        if col == 0 and item.text(0) in self.nodes.keys():
            for callback in self.select_data_callbacks:
                callback(item.text(0))

    def add_select_data_callback(self, callback: Callable):
        """
        加入回调函数。
        """

        self.select_data_callbacks.append(callback)

    def on_item_double_clicked(self, item: QTreeWidgetItem, col: int) -> None:
        """
        双击条目的事件，触发数据显示。
        """
        if col == 0 and item.text(0) in self.nodes.keys():
            self.show_data(item.text(0))

    def on_right_clicked(self, pos):
        """
        右键点击某一条目的事件,此时会弹出菜单。
        """
        item = self.currentItem()
        if item is not None and item.text(0) in self.nodes.keys():
            self.context_menu.exec_(self.mapToGlobal(pos))

    def on_show_data_by_context_menu(self, action: 'QAction'):
        """
        右键菜单点击‘显示数据’所触发的事件。
        """
        item = self.currentItem()
        if item is not None and item.text(0) in self.nodes.keys():
            self.show_data(item.text(0))

    def autorepr(self, obj: Any, max_length=80) -> str:
        """
        封装了repr方法，数据过长的时候，取较短的。
        """
        return repr(obj).replace('\n', '').replace('\r', '')[:max_length]

    def get_size(self, data: Any):
        """
        获取数据的尺寸。
        有‘shape’这一属性的，size就等于data.shape
        有‘__len__’这个属性的，返回len(data)
        否则返回1.
        """
        size = 1
        if hasattr(data, 'shape'):
            size = data.shape
        elif hasattr(data, '__len__'):
            try:
                size = len(data)
            except:
                pass
        return size

    def set_data_dic(self, data_dic: Dict[str, object]) -> None:
        """
        显示数据
        :param data_dic:所有数据的字典{变量名：变量对象}
        :return:
        """
        for data_name in data_dic:

            data = data_dic[data_name]
            text = repr(data_name)
            size = self.get_size(data)
            data_str = f'<{size}>\t{self.autorepr(data)}'

            if text in self.nodes.keys():
                """
                如果变量在变量列表中，就刷新这个变量位置显示的文字信息，并通过递归方式创建变量的各个属性。
                """
                data_node = self.nodes[text]
                data_node.setText(0, text)
                data_node.setText(1, repr(size))
                data_node.setText(2, self.autorepr(data))
                data_node.takeChildren()
            else:
                """
                如果变量不在变量列表中，就新建一个节点，并通过递归方式创建变量的各个属性。
                """
                child = QTreeWidgetItem(self)
                self.nodes[text] = child
                child.setText(0, text)
                child.setText(1, str(size))
                child.setText(2, self.autorepr(data))

                if isinstance(data, dict):
                    self.set_data_view(data, child)
                if self.auto_expand:
                    self.expandItem(child)
                else:
                    self.collapseItem(child)

    def get_hier(self, item: QTreeWidgetItem) -> int:
        i = 0
        all_nodes = [self.nodes[k] for k in self.nodes.keys()]
        while (1):
            print(item.parent())
            if item.parent() not in all_nodes:
                i += 1
                item = item.parent()
            else:
                return i

    def set_data_view(self, data_dic: Dict[str, object], root: 'QTreeWidgetItem'):
        """
        递归方式显示json。
        显示的时候要注意层级。
        :param data_dic:
        :param root:
        :return:
        """
        for k in data_dic.keys():
            print(k)
            if type(data_dic[k]) == dict:
                child = QTreeWidgetItem(root)
                child.setText(0, repr(k))
                self.set_data_view(data_dic[k], child)
            elif not isinstance(data_dic[k], str):
                print(k)
                d = {attr_name: str(getattr(data_dic[k], attr_name)) for attr_name in dir(data_dic[k])}

                child = QTreeWidgetItem(root)
                child.setText(0, repr(k))
                self.set_data_view(d, child)
            else:
                child = QTreeWidgetItem(root)
                child.setText(0, repr(k))
                child.setText(1, str(self.get_size(data_dic[k])))
                child.setText(2, data_dic[k])


if __name__ == '__main__':
    from PySide2.QtWidgets import QApplication, QTableWidget
    import sys

    app = QApplication(sys.argv)
    sa = PMGAttrTree()
    sa.show()
    sa.setup_ui()
    data_dic = {'a': {'type': 'statespace',
                      'A': {'type': 'timeseries', 'time': '[1,2,3]', 'mdata': '[3,2,1]'},
                      'B': {'type': 'matrix', 'value': '[[2],[1]]', 'aaaa': {'a': 'aa', 0: {'a': 'a'}}},
                      'C': {'type': 'matrix', 'value': '[[1,2]]', },
                      'D': {'type': 'matrix', 'value': '[[0]]', },
                      'row': ['left', 'x2'], 'column': ['column'], 'u': ['u'], 'sys': 'str'},
                'b': 100,
                55: {123: 456, 'ff': {3333: 555}},
                'sa': sa}
    # sa.set_data_dic(data_dic)
    sa.set_data_view(data_dic, sa)
    sys.exit(app.exec_())
