"""
专门显示JSON的树状控件。
"""
import os
import time
from typing import Dict, Callable, Any

from PySide2.QtWidgets import QTreeWidget, QTreeWidgetItem, QMenu
from PySide2.QtCore import Signal, Qt, QTimer, QLocale
from widgets.utilities.source.translation import create_translator


class PMGJsonTree(QTreeWidget):
    signal_show_data_value = Signal(str)
    signal_data_saveas = Signal(str)
    signal_data_open = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent=None)
        self.select_data_callbacks = []
        self.filter_all_upper_case = False
        self.filter_all_callables = True
        self.setup_ui()
        self.expanding_stat: Dict[str, bool] = {}

    def setup_ui(self):
        self.translator = create_translator(
            path=os.path.join(os.path.dirname(__file__), 'translations',
                              'qt_{0}.qm'.format(QLocale.system().name())))  # translator
        self.nodes: Dict[str, 'QTreeWidgetItem'] = {}
        self.setColumnCount(2)
        header_item = QTreeWidgetItem()
        header_item.setText(0, self.tr('Name'))
        self.setColumnWidth(0, 200)
        header_item.setText(1, self.tr('Value'))
        header_item.setTextAlignment(0, Qt.AlignCenter)
        header_item.setTextAlignment(1, Qt.AlignCenter)
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

    def memorize_expanding_stat(self):
        for k, node in self.nodes.items():
            self.expanding_stat[k] = node.isExpanded()

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
            return
            # self.show_data(item.text(0))

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
            return

    def autorepr(self, obj: Any, max_length=80) -> str:
        """
        封装了repr方法，数据过长的时候，取较短的。
        """
        if isinstance(obj, str):
            return obj
        else:
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
        elif isinstance(data, str):
            size = 1
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
        self.expanding_stat = {}
        self.memorize_expanding_stat()
        self.clear()
        self.nodes = {}

        for data_name in data_dic:

            data = data_dic[data_name]
            text = str(data_name)
            size = self.get_size(data)
            """
            如果变量不在变量列表中，就新建一个节点，并通过递归方式创建变量的各个属性。
            """
            child = QTreeWidgetItem(self)
            child.item_id = text
            self.nodes[child.item_id] = child
            child.setText(0, text)
            self.try_expand_item(child)
            if isinstance(data, dict):
                self.set_data_view(data, child)

    def get_hier(self, item: QTreeWidgetItem) -> int:
        i = 0
        all_nodes = [self.nodes[k] for k in self.nodes.keys()]
        while (1):
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
            if isinstance(data_dic[k], dict):
                child = QTreeWidgetItem(root)
                child.setText(0, str(k))
                child.item_id = root.item_id + '-' + child.text(0)
                self.nodes[child.item_id] = child
                self.set_data_view(data_dic[k], child)
            else:
                child = QTreeWidgetItem(root)
                child.setText(0, str(k))
                child.item_id = root.item_id + '-' + child.text(0)
                self.nodes[child.item_id] = child

                child.setText(1, self.autorepr(data_dic[k]))
            self.try_expand_item(child)

    def try_expand_item(self, item: QTreeWidgetItem):
        """
        如果状态为展开则展开，否则不展开
        :param item:
        :return:
        """
        expanding_stat = self.expanding_stat.get(item.item_id)
        if expanding_stat is not None:
            item.setExpanded(expanding_stat)
        else:
            item.setExpanded(False)


if __name__ == '__main__':
    from PySide2.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    sa = PMGJsonTree()
    sa.show()
    sa.setup_ui()
    a = 123
    data_dic = {
        'p%d' % i: {'type': str(type(123)),
                    'value': 123,
                    'attributes': {name: str(getattr(a, name)) for name in dir(a)}
                    } for i in range(100)}
    data_dic['aaaaaa'] = 'aaaaa '


    def f():
        data_dic['p10']['value'] = time.time()
        sa.set_data_dic(data_dic)


    sa.set_data_dic(data_dic)
    sa.memorize_expanding_stat()
    timer = QTimer()
    timer.start(1000)
    timer.timeout.connect(f)
    sys.exit(app.exec_())
