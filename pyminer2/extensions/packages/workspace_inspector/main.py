import os
from typing import Dict, TYPE_CHECKING, Callable

from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QMenu
from PyQt5.QtCore import pyqtSignal, Qt, QLocale
from pmgwidgets import PMDockObject

from pyminer2.extensions.extensionlib import BaseExtension, BaseInterface

if TYPE_CHECKING:
    from .data_viewer import PMVariableViewerWidget


class Extension(BaseExtension):
    interace: 'Interface' = None

    def on_loading(self):
        translation_file = os.path.join(os.path.dirname(__file__), 'translations',
                                        'qt_{0}.qm'.format(QLocale.system().name()))
        self.extension_lib.UI.add_translation_file(translation_file)
        self.extension_lib.Program.add_translation('zh_CN',
                                                   {'Workspace': '工作空间', 'Collapse All': '全部折叠', 'Expand All': '全部展开'})

    def on_load(self):
        self.workspace: 'PMWorkspaceInspectWidget' = self.widgets['PMWorkspaceInspectWidget']
        self.workspace.var_tree.extension_lib = self.extension_lib
        self.workspace.extension_lib = self.extension_lib

        self.data_viewer: 'PMVariableViewerWidget' = None

        self.interface.data_viewer = self.workspace.var_tree
        self.workspace.bind_show_data(self.on_show_data)

        # self.workspace.connect_to_datamanager(self.extension_lib)
        # 注意：上边被注释掉的一句代码是既不规范也不正确的写法。因为当插件on_load方法调用的时候，
        # 尚未调用setup_ui方法，这就造成了一些相关的变量和控件尚未加载，可能获取不到。
        # 正确的做法如下所示
        self.extension_lib.Signal.get_widgets_ready_signal().connect(
            lambda: self.workspace.connect_to_datamanager(self.extension_lib))

    def on_show_data(self, dataname: str):
        if self.data_viewer is None:
            self.data_viewer_cls = self.widget_classes['PMVariableViewerWidget']
            self.data_viewer: 'PMVariableViewerWidget' = \
                self.extension_lib.insert_widget(self.data_viewer_cls,
                                                 'new_dock_window', {
                                                     "name": "data_view_table",
                                                     "side": "top",
                                                     "text": "变量管理器"})
            self.data_viewer.set_lib(self.extension_lib)
            self.data_viewer.on_dock_widget_deleted = self.on_dock_widget_deleted
        self.data_viewer.show_data(dataname)

    def on_dock_widget_deleted(self):
        self.data_viewer = None


class Interface(BaseInterface):

    def add_select_data_callback(self, callback: Callable):
        """
        添加数据被选中时的回调函数。也就是当你单击数据时候的回调函数。
        """

        self.data_viewer.add_select_data_callback(callback)


class PMVariableTreeWidget(QTreeWidget):
    signal_show_data_value = pyqtSignal(str)
    signal_data_saveas = pyqtSignal(str)
    signal_data_open = pyqtSignal(str)
    select_data_callbacks = []
    extension_lib: 'extension_lib' = None

    def __init__(self, parent=None):
        super().__init__(parent=None)

        self.filter_all_upper_case = False
        self.filter_all_callables = True

    def is_item_legal(self, name: str, obj: object):
        return (not (callable(obj) and self.filter_all_callables)) and \
               (not (name.isupper() and self.filter_all_upper_case))

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
        # save_action = self.context_menu.addAction(self.tr('Save as '))
        # cancel_action = self.context_menu.addAction(self.tr('Undo'))
        # redo_action = self.context_menu.addAction(self.tr('Redo'))
        delete_action = self.context_menu.addAction(self.tr('Delete'))
        show_action.triggered.connect(self.on_show_data_by_context_menu)
        delete_action.triggered.connect(self.on_delete_data_by_context_menu)

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

    def on_delete_data_by_context_menu(self):
        item = self.currentItem()
        if item is not None and item.text(0) in self.nodes.keys():
            self.delete_data(item.text(0))

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

    def autorepr(self, obj: object, max_length=80) -> str:
        """
        封装了repr方法，数据过长的时候，取较短的。
        """
        return repr(obj).replace('\n', '').replace('\r', '')[:max_length]

    def get_size(self, data: object):
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

    def delete_data(self, data_name: str) -> None:
        self.extension_lib.Data.delete_variable(data_name)

    def clear_all_nodes(self):
        self.nodes = {}
        self.clear()

    def set_data(self, data_dic: Dict[str, object]) -> None:
        """
        显示数据
        :param data_dic:所有数据的字典{变量名：变量对象}
        :return:
        """
        for data_name in data_dic:
            data = data_dic[data_name]
            if not self.is_item_legal(data_name, data):
                continue
            size = self.get_size(data)
            data_str = f'<{size}>\t{self.autorepr(data)}'

            if data_name in self.nodes.keys():
                """
                如果变量在变量列表中，就刷新这个变量位置显示的文字信息，并通过递归方式创建变量的各个属性。
                """
                data_node = self.nodes[data_name]
                data_node.setText(0, data_name)
                data_node.setText(1, repr(size))
                data_node.setText(2, self.autorepr(data))
                data_node.takeChildren()

                # if isinstance(data, dict):
                #     self.set_data_view(data, self.nodes[data_name])
            else:
                """
                如果变量不在变量列表中，就新建一个节点，并通过递归方式创建变量的各个属性。
                """
                child = QTreeWidgetItem(self)
                self.nodes[data_name] = child
                child.setText(0, data_name)
                child.setText(1, str(size))
                child.setText(2, self.autorepr(data))

                # if isinstance(data, dict):
                #     self.set_data_view(data, child)
                if self.auto_expand:
                    self.expandItem(child)
                else:
                    self.collapseItem(child)

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
            if type(data_dic[k]) == dict:

                child = QTreeWidgetItem(root)
                # self.indexOfTopLevelItem(child)
                child.setText(0, repr(k))
                if self.get_hier(child) <= 1:
                    self.set_data_view(data_dic[k], child)
                # print(self.get_hier(child))
            else:
                child = QTreeWidgetItem(root)
                child.setText(0, repr(k))
                child.setText(1, str(self.get_size(data_dic[k])))
                child.setText(2, self.autorepr(data_dic[k]))


class PMWorkspaceInspectWidget(QWidget, PMDockObject):
    """
    用于承载 PMVariableTreeWidget以及相关的按钮。

    """

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        self.var_tree = PMVariableTreeWidget(parent)
        self.collapse_all()
        layout.addWidget(self.var_tree)
        self.setLayout(layout)

    def setup_ui(self):
        self.var_tree.setup_ui()
        parent = self.parent()
        layout = self.layout()
        control_layout = QHBoxLayout()
        button_expand = QPushButton(self.tr('Expand All'))
        button_collapse = QPushButton(self.tr('Collapse All'))
        control_layout.addWidget(button_expand)
        control_layout.addWidget(button_collapse)
        layout.addLayout(control_layout)
        button_collapse.clicked.connect(self.collapse_all)
        button_expand.clicked.connect(self.expand_all)

        self.signal_show_data_value = self.var_tree.signal_show_data_value
        self.signal_data_saveas = self.var_tree.signal_data_saveas
        self.signal_data_open = self.var_tree.signal_data_open

    def expand_all(self):
        """
        展开所有节点
        """
        self.var_tree.auto_expand = True
        self.var_tree.expandAll()

    def collapse_all(self):
        """
        折叠所有节点
        """
        self.var_tree.auto_expand = False
        self.var_tree.collapseAll()

    def connect_to_datamanager(self, extension_lib):
        """
        与数据管理相连接。
        同时，在这个函数中定义了闭包子函数on_modification和on_deletion，
        也就是在数据变更或者删除时候调用的方法。
        """
        self.extension_lib = extension_lib
        self.data = self.extension_lib.get_all_var()
        data = {
            k: v for k,
                     v in self.data.items() if not getattr(
                v,
                'type',
                '') == 'Type'}
        self.var_tree.set_data(data)

        def on_modification(varname: str, variable, data_source: str):
            self.data[varname] = variable
            self.var_tree.set_data({varname: variable})
            # need to detect whether it is modified or created

        def on_deletion(varname: str, provider: str):
            self.extension_lib = extension_lib
            self.data = self.extension_lib.get_all_var()
            data = {
                k: v for k,
                         v in self.data.items() if not getattr(v, 'type', '') == 'Type'}

            self.var_tree.clear_all_nodes()
            self.var_tree.set_data(data)
            if provider != 'ipython':
                self.extension_lib.get_interface('ipython_console').run_command('__delete_var(\'%s\')' % varname,
                                                                                hint_text='delete variable %s' % varname,
                                                                                hidden=False)

        self.extension_lib.on_modification(on_modification)
        self.extension_lib.on_deletion(on_deletion)

    def bind_show_data(self, on_show_data):
        """
        绑定变量树视图在show_data事件触发时的回调。
        """
        self.var_tree.show_data = on_show_data


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication, QTableWidget
    import sys

    app = QApplication(sys.argv)
    sa = PMWorkspaceInspectWidget()
    sa.show()
    sa.setup_ui()
    data_dic = {'a': {'type': 'statespace',
                      'A': {'type': 'timeseries', 'time': '[1,2,3]', 'mdata': '[3,2,1]'},
                      'B': {'type': 'matrix', 'value': '[[2],[1]]', 'aaaa': {'a': 'aa', 0: {'a': 'a'}}},
                      'C': {'type': 'matrix', 'value': '[[1,2]]', },
                      'D': {'type': 'matrix', 'value': '[[0]]', },
                      'row': ['left', 'x2'], 'column': ['column'], 'u': ['u'], 'sys': 'str'},
                'b': 100}
    sa.var_tree.set_data(data_dic)
    sys.exit(app.exec())
