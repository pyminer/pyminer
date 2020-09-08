'''
修改：
原先，主窗口中的各个可停靠窗口，在点击右上角关闭按钮的时候会隐藏，可以在视图菜单中打开。
但是当控件中有on_closed_action属性，且值为‘delete’的时候，控件就会被回收。
为了实现控件的管理，控件需要继承PMDockObject，并且需要用多继承的方式。

from pyminer2.ui.generalwidgets import PMDockObject
这个PMDockObject中定义了一些方法，作为补充。

class PMDockObject(object):
    on_closed_action = 'hide'  # 或者'delete'。
    signal_raise_into_view = pyqtSignal()

    def raise_widget_to_visible(self, widget: 'QWidget'):
        pass

    def on_dock_widget_deleted(self):
        pass
其中。signal_raise_into_view时一个信号，调用signal_raise_into_view.emit()时
它的上层控件会收到这个信号，从而显示到上层。当标签页数目较多的时候，格外需要这种交互。

'''
from typing import Dict, TYPE_CHECKING

from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QMenu
from PyQt5.QtCore import pyqtSignal, Qt
from .dataclient import Client
from pyminer2.extensions.extensionlib import BaseExtension

if TYPE_CHECKING:
    from .data_viewer import PMVariableViewerWidget


class Extension(BaseExtension):
    def on_load(self):
        self.workspace: 'PMWorkspaceInspectWidget' = self.widgets['PMWorkspaceInspectWidget']
        self.workspace.connect_to_datamanager(self.extension_lib)
        self.workspace.bind_show_data(self.on_show_data)
        self.data_viewer: 'PMVariableViewerWidget' = None
        print("插件%s被加载!" % "工作空间管理器")

    def on_show_data(self, dataname: str):
        if self.data_viewer is None:
            self.data_viewer_cls = self.widget_classes['PMVariableViewerWidget']
            self.data_viewer: 'PMVariableViewerWidget' = \
                self.extension_lib.insert_widget(self.data_viewer_cls,
                                                 'new_dock_window', {
                                                     "name": "data_view_table",
                                                     "side": "n",
                                                     "text": "变量视图"})
            self.data_viewer.set_lib(self.extension_lib)
            self.data_viewer.on_dock_widget_deleted = self.on_dock_widget_deleted
        self.data_viewer.show_data(dataname)

    def on_install(self):
        print('被安装')

    def on_uninstall(self):
        print("被卸载")

    def on_dock_widget_deleted(self):
        self.data_viewer = None


class Interface:
    def hello(self):
        print("Hello")


class PMJsonViewWidget(QTreeWidget):
    signal_show_data_value = pyqtSignal(str)
    signal_data_saveas = pyqtSignal(str)
    signal_data_open = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent=None)
        self.setColumnCount(3)
        item = QTreeWidgetItem()
        item.setText(0, '名称')
        self.setColumnWidth(0, 10 * 10)
        item.setText(1, '大小')
        self.setColumnWidth(1, 5 * 10)
        item.setText(2, '值')
        item.setTextAlignment(0, Qt.AlignCenter)
        item.setTextAlignment(1, Qt.AlignCenter)
        self.setHeaderItem(item)
        self.auto_expand = False

        self.nodes: Dict[str, 'QTreeWidgetItem'] = {}

        self.itemClicked.connect(self.on_item_clicked)
        self.itemDoubleClicked.connect(self.on_item_double_clicked)
        self.customContextMenuRequested.connect(self.on_right_clicked)
        self.setContextMenuPolicy(Qt.CustomContextMenu)

        self.context_menu = QMenu()
        show_action = self.context_menu.addAction('查看')
        save_action = self.context_menu.addAction('保存')
        cancel_action = self.context_menu.addAction('撤销')
        redo_action = self.context_menu.addAction('重做')
        delete_action = self.context_menu.addAction('删除')
        show_action.triggered.connect(self.on_show_data_by_context_menu)

    def on_item_clicked(self, item: QTreeWidgetItem, col: int) -> None:
        if item.isExpanded():
            self.collapseItem(item)
        else:
            self.expandItem(item)

    def on_item_double_clicked(self, item: QTreeWidgetItem, col: int) -> None:
        if col == 0 and item.text(0) in self.nodes.keys():
            self.show_data(item.text(0))

    def on_right_clicked(self, pos):
        item = self.currentItem()
        if item is not None and item.text(0) in self.nodes.keys():
            self.context_menu.exec_(self.mapToGlobal(pos))

    def on_show_data_by_context_menu(self, action: 'QAction'):
        item = self.currentItem()
        if item is not None and item.text(0) in self.nodes.keys():
            self.show_data(item.text(0))

    def autorepr(self, obj: object, max_length=80) -> str:
        """
        封装了repr方法，数据过长的时候，取较短的。
        """
        return repr(obj).replace('\n', '').replace('\r', '')[:max_length]

    def get_size(self, data: object):
        size = 1
        if hasattr(data, 'shape'):
            size = data.shape
        elif hasattr(data, '__len__'):
            size = len(data)
        return size

    def set_data(self, data_dic, root):
        '''
        根据数据生成metadata,并且显示数据
        metadata的生成算法需要继续看。
        :param data_dic:
        :param root:
        :return:
        '''
        for data_name in data_dic:
            data = data_dic[data_name]
            size = self.get_size(data)
            data_str = f'<{size}>\t{self.autorepr(data)}'

            if data_name in self.nodes.keys():
                '''
                如果变量在变量列表中，就刷新这个变量位置显示的文字信息，并通过递归方式创建变量的各个属性。
                '''
                data_node = self.nodes[data_name]
                data_node.setText(0, data_name)
                data_node.setText(1, repr(size))
                data_node.setText(2, self.autorepr(data))
                data_node.takeChildren()

                if isinstance(data, dict):
                    self.set_data_view(data, self.nodes[data_name])
            else:
                '''
                如果变量不在变量列表中，就新建一个节点，并通过递归方式创建变量的各个属性。
                '''
                child = QTreeWidgetItem(self)
                self.nodes[data_name] = child
                child.setText(0, data_name)
                child.setText(1, str(size))
                child.setText(2, self.autorepr(data))

                if isinstance(data, dict):
                    self.set_data_view(data, child)
                if self.auto_expand:
                    self.expandItem(child)
                else:
                    self.collapseItem(child)

    def set_data_view(self, data_dic: Dict[str, object], root):
        '''
        递归方式显示json。
        :param data_dic:
        :param root:
        :return:
        '''
        for k in data_dic.keys():
            if type(data_dic[k]) == dict:

                child = QTreeWidgetItem(root)
                child.setText(0, repr(k))
                self.set_data_view(data_dic[k], child)
            else:
                child = QTreeWidgetItem(root)
                child.setText(0, repr(k))
                child.setText(1, str(self.get_size(data_dic[k])))
                child.setText(2, self.autorepr(data_dic[k]))


class PMWorkspaceInspectWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        self.var_tree = PMJsonViewWidget(parent)
        self.collapse_all()
        layout.addWidget(self.var_tree)
        control_layout = QHBoxLayout()
        button_expand = QPushButton('全部展开')
        button_collapse = QPushButton('全部折叠')
        control_layout.addWidget(button_expand)
        control_layout.addWidget(button_collapse)
        layout.addLayout(control_layout)
        button_collapse.clicked.connect(self.collapse_all)
        button_expand.clicked.connect(self.expand_all)
        self.setLayout(layout)

        self.data_client = Client()

        self.signal_show_data_value = self.var_tree.signal_show_data_value
        self.signal_data_saveas = self.var_tree.signal_data_saveas
        self.signal_data_open = self.var_tree.signal_data_open

    def expand_all(self):
        self.var_tree.auto_expand = True
        self.var_tree.expandAll()

    def collapse_all(self):
        self.var_tree.auto_expand = False
        self.var_tree.collapseAll()

    def connect_to_datamanager(self, datamanager):
        self.datamanager = datamanager
        self.data = self.datamanager.get_all_var()
        data = {k: v for k, v in self.data.items() if not getattr(v, 'type', '') == 'Type'}
        self.var_tree.set_data(data, self.var_tree)

        def on_modification(varname: str, variable):
            self.data[varname] = variable
            self.var_tree.set_data({varname: variable}, self.var_tree)
            # need to detect whether it is modified or created

        def on_deletion(varname: str):
            self.data.pop(varname)
            # self.var_tree.set_data_view(self.data, self.var_tree.root)
            raise NotImplementedError()

        self.datamanager.on_modification(on_modification)
        self.datamanager.on_deletion(on_deletion)

    def bind_show_data(self, on_show_data):
        self.var_tree.show_data = on_show_data


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication, QTableWidget
    import sys

    app = QApplication(sys.argv)
    sa = PMWorkspaceInspectWidget()
    sa.show()
    data_dic = {'a': {'type': 'statespace',
                      'A': {'type': 'timeseries', 'time': '[1,2,3]', 'mdata': '[3,2,1]'},
                      'B': {'type': 'matrix', 'value': '[[2],[1]]', },
                      'C': {'type': 'matrix', 'value': '[[1,2]]', },
                      'D': {'type': 'matrix', 'value': '[[0]]', },
                      'row': ['left', 'x2'], 'column': ['column'], 'u': ['u'], 'sys': 'str'}}
    sa.show_data_view(data_dic, sa)
    sys.exit(app.exec())
