import os
import time
from typing import Dict, TYPE_CHECKING, Callable, Any, List

from PySide2.QtWidgets import QAction
from PySide2.QtWidgets import QWidget, QVBoxLayout, QMenu, \
    QMessageBox, QFileDialog, QInputDialog, QApplication, QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView
from PySide2.QtCore import Signal, Qt, QLocale, QModelIndex

from widgets import PMDockObject, in_unit_test, create_translator
from utils import load_variable_pmd, load_variable_pkl, save_variable_pkl, save_variable_pmd, save_variable_table, \
    save_variable_matrix
from lib.comm.base import DataDesc
from lib.comm import get_var, set_var, del_var, set_vars

if TYPE_CHECKING:
    pass


class PMVariableTreeWidget(QTableWidget):
    signal_show_data_value = Signal(str)
    signal_data_saveas = Signal(str)
    signal_data_open = Signal(str)
    select_data_callbacks = []
    extension_lib: 'extension_lib' = None

    def __init__(self, parent=None):
        super().__init__(parent=None)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self._show_data = lambda data_name: print('show data \'%s\'' % data_name)
        self.filter_all_upper_case = False
        self.filter_all_callables = True
        self.row_mapping: Dict[str, int] = {}

    def is_item_legal(self, name: str, obj: Any):
        return (not (callable(obj) and self.filter_all_callables)) and \
               (not (name.isupper() and self.filter_all_upper_case))

    def setup_ui(self):
        self.headers = [self.tr('Name'), self.tr('Type'), self.tr('Size'), self.tr('Value')]

        self.setColumnCount(len(self.headers))
        self.setHorizontalHeaderLabels(self.headers)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.itemClicked.connect(self.on_item_clicked)
        self.itemDoubleClicked.connect(self.on_item_double_clicked)
        self.customContextMenuRequested.connect(self.on_right_clicked)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)

    def init_save_menu(self, parent_menu: QMenu, var_desc: DataDesc) -> QMenu:
        import pandas as pd
        import numpy as np
        save_menu = QMenu(parent=parent_menu, title=self.tr('Save..'))
        parent_menu.addMenu(save_menu)
        save_to_pmd_action = save_menu.addAction(self.tr('PyMiner Data(.pmd)'))
        save_to_pmd_action.triggered.connect(lambda: self.on_save_variable(self.tr('PyMiner Data(*.pmd)')))
        save_to_pkl_action = save_menu.addAction(self.tr('Pickle(.pkl)'))
        save_to_pkl_action.triggered.connect(self.on_save_variable)
        if issubclass(var_desc.cls, pd.DataFrame):
            save_to_excel_action = save_menu.addAction(self.tr('Excel Table(.xls/.xlsx)'))
            save_to_excel_action.triggered.connect(
                lambda: self.on_save_to_table(self.tr("Excel (*.xls *.xlsx)")))
            save_to_csv_action = save_menu.addAction(self.tr('Text File (.csv)'))
            save_to_csv_action.triggered.connect(
                lambda: self.on_save_to_table(self.tr("CSV File(*.csv)")))
        if issubclass(var_desc.cls, np.ndarray):
            save_to_npy_action = save_menu.addAction(self.tr('Numpy Matrix'))
            save_to_npy_action.triggered.connect(self.on_save_to_npy)
        # action_save_as_table = save_menu.addAction('aaaaaa')

    def create_context_menu(self) -> QMenu:
        """
        创建右键菜单。由于右键菜单用的不会太多，所以动态生成应当也是可以接受的。
        :return:
        """
        var_desc = self.get_current_var_desc()

        context_menu = QMenu()
        show_action: QAction = context_menu.addAction(self.tr('View'))

        # save_action = self.context_menu.addAction(self.tr('Save as '))
        # cancel_action = self.context_menu.addAction(self.tr('Undo'))
        # redo_action = self.context_menu.addAction(self.tr('Redo'))
        delete_action = context_menu.addAction(self.tr('Delete'))
        open_action = context_menu.addAction(self.tr('Open Variable'))

        save_to_workdir = context_menu.addAction(self.tr('Quick Save to Workdir'))

        if var_desc is not None:
            self.init_save_menu(context_menu, var_desc)

        save_workspace_action = context_menu.addAction(self.tr('Save Workspace'))
        show_action.triggered.connect(self.on_show_data_by_context_menu)
        delete_action.triggered.connect(self.on_delete_data_by_context_menu)
        save_to_workdir.triggered.connect(self.on_save_to_workdir)
        open_action.triggered.connect(self.on_open_variable)

        save_workspace_action.triggered.connect(self.on_save_workspace)
        return context_menu

    def on_save_to_npy(self):
        file_path, filetype = QFileDialog.getSaveFileName(self,
                                                          self.tr('Choose File'), self._get_work_dir(),
                                                          "Numpy Matrix(*.npy)")  # 设置文件扩展名过滤,用双分号间隔
        save_variable_matrix(self.get_current_var(), file_path)

    def on_save_to_table(self, ext_type: str):
        file_path, filetype = QFileDialog.getSaveFileName(self,
                                                          self.tr('Choose File'), self._get_work_dir(),
                                                          self.tr(ext_type))
        save_variable_table(self.get_current_var(), file_path)

    def on_item_clicked(self, item: QTableWidgetItem) -> None:
        """
        点击条目时的回调函数。会顺次执行self.select_data_callbacks，而self.select_data_callbacks
        是由插件的add_select_data_callback(self, callback: Callable)方式加入的。
        """
        name = self.get_current_var_name()
        if name.isidentifier():
            for callback in self.select_data_callbacks:
                callback(name)

    def on_item_double_clicked(self, item: QTableWidgetItem) -> None:
        """
        双击条目的事件，触发数据显示。
        """
        name = self.get_current_var_name()
        if name.isidentifier():
            self.show_data(name)

    def on_right_clicked(self, pos):
        """
        右键点击某一条目的槽,此时会弹出菜单。
        Args:
            pos: 右键点击某个条目时候菜单弹出的位置。

        Returns:

        """
        context_menu = self.create_context_menu()
        context_menu.exec_(self.mapToGlobal(pos))

    def on_delete_data_by_context_menu(self):
        name = self.get_current_var_name()
        if name.isidentifier():
            self.delete_data(name)

    def get_current_var_desc(self) -> DataDesc:
        return self.extension_lib.Data.get_data_desc(self.get_current_var_name())

    def get_current_var_name(self) -> str:
        """

        获取当前选中变量的名称
        Returns:

        """
        row = self.currentItem().row()
        item = self.item(row, 0)
        if item is not None:
            return item.text()
        return ''

    def _get_work_dir(self) -> str:
        if not in_unit_test():
            work_dir = self.extension_lib.Program.get_work_dir()
        else:
            work_dir = os.path.join(os.path.expanduser('~'), "Desktop")
        return work_dir

    def get_current_var(self) -> Any:
        """
        获取当前选中的变量。如果没有就返回None
        Returns:

        """
        var_name = self.get_current_var_name()
        if var_name == '':
            return None
        else:
            if not in_unit_test():
                var = get_var(var_name)
            else:
                global data_dic
                var = data_dic.get(var_name)
            return var

    def on_save_to_workdir(self):
        """
        保存到当前工作路径的回调
        Returns:

        """
        var_name = self.get_current_var_name()
        if var_name != '':
            work_dir = self._get_work_dir()
            import cloudpickle
            file_dir = os.path.join(work_dir, var_name + '.pkl')
            try:
                with open(file_dir, 'wb') as f:
                    cloudpickle.dump(self.get_current_var(), f)

            except:
                import traceback
                traceback.print_exc()

    def on_open_variable(self):
        file_path, filetype = QFileDialog.getOpenFileName(self,
                                                          self.tr('Choose File'), self._get_work_dir(),
                                                          "Data File(*.pkl *.pmd)")  # 设置文件扩展名过滤,用双分号间隔
        self.open_variable(file_path)

    def open_variable(self, file_path: str):
        """
        打开路径下的变量
        Args:
            file_path:

        Returns:

        """
        if os.path.exists(file_path) and file_path != '':
            try:
                if file_path.endswith('.pmd'):
                    variables, metadatas = load_variable_pmd(file_path)
                    if variables is not None:
                        if not in_unit_test():

                            set_vars(variables)
                            # TODO:(侯展意)目前还无法将metadata读入。这个或许需要问一下。
                        else:
                            print(variables, metadatas)
                        return
                    else:
                        error_message = self.tr('Variable %s is corrupted.' % file_path)
                elif file_path.endswith('.pkl'):
                    base_name, ext = os.path.splitext(os.path.basename(file_path))
                    while 1:
                        var_name, ok = QInputDialog.getText(self, self.tr('Variable Name'),
                                                            self.tr('Please Input Variable Name:'), text=base_name)
                        if not ok:
                            return
                        if var_name.isidentifier():
                            break
                    variable = load_variable_pkl(file_path)
                    if variable is not None:
                        if not in_unit_test():
                            set_var(var_name, variable)
                        else:
                            print(var_name, variable)
                        return
                    else:
                        error_message = self.tr('Variable %s is corrupted.' % file_path)
                else:
                    error_message = self.tr('Cannot Load this type of file:%s' % file_path)

            except Exception as e:
                import traceback
                traceback.print_exc()
                error_message = str(e)
            QMessageBox.warning(self, self.tr('Error Occurs In Loading'), error_message)

    def on_save_variable(self, ext_type: str):
        """
        保存变量时触发的函数
        Args:
            ext_type:

        Returns:

        """
        work_dir = self._get_work_dir()
        if not in_unit_test():

            var_name = self.get_current_var_name()
            value = self.get_current_var()
            metadata = self.extension_lib.Data.get_metadata(var_name)
        else:
            var_name = 'abc'
            value = 123
            metadata = {'time': time.time()}
        export_path, ext = QFileDialog.getSaveFileName(self, self.tr("Choose File Name To Save"),
                                                       os.path.join(work_dir, var_name),
                                                       ext_type)  # ;;Numpy数组文件(*.npy)")
        if export_path != '':
            if export_path.endswith('.pkl'):
                save_variable_pkl(value, export_path)
            elif export_path.endswith('.pmd'):
                print(export_path)
                save_variable_pmd(var_name, value, export_path, metadata)
            else:
                raise ValueError(self.tr('File %s cannot be saved as its'
                                         ' extension name is not supported') % export_path)

    def on_save_workspace(self):
        """
        保存整个工作空间时触发的函数.
        注入一条命令到IPython里面，从而进行保存。
        Returns:

        """

        work_dir = self._get_work_dir()
        export_path, ext = QFileDialog.getSaveFileName(self, self.tr("Choose File Name To Save"), work_dir,
                                                       r"PyMiner Data File(*.pmd)")  # ;;Numpy数组文件(*.npy)")
        if export_path != '':
            cmd = 'get_ipython().save_vars([],\'%s\',\'pmd\')' % os.path.normcase(export_path)
            cmd = cmd.replace('\\', '\\\\')
            self.extension_lib.get_interface('ipython_console'). \
                run_command(cmd, hint_text='保存工作空间', hidden=False)
            # save_variable_pmd(var_name_list, var_value_list, export_path, var_metadata_list)

    def add_select_data_callback(self, callback: Callable):
        """
        加入回调函数。
        Returns:
        """

        self.select_data_callbacks.append(callback)

    def on_show_data_by_context_menu(self, action: 'QAction'):
        """
        右键菜单点击‘显示数据’所触发的事件。
        Args:
            action:
        Returns:
        """
        name = self.get_current_var_name()
        if name.isidentifier():
            self.show_data(name)

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
        Args:
            data:

        Returns:

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
        """
        删除数据的回调
        :param data_name:
        :return:
        """
        if not in_unit_test():
            del_var(data_name)
        else:
            print('in unit test.delete data:%s' % data_name)

    def clear_all_nodes(self):
        self.nodes = {}
        self.clear()

    def set_data(self, data_dic: Dict[str, Any]) -> None:
        """
        显示数据
        :param data_dic:所有数据的字典{变量名：变量对象}
        :return:
        """
        for data_name in data_dic:
            data = data_dic[data_name]
            if not isinstance(data, DataDesc):
                if not self.is_item_legal(data_name, data):
                    continue
                data_size = self.get_size(data)

                # 数据类型处理
                data_type = str(type(data)).replace('class', '').replace(' ', '').replace('\'', '').replace('<',
                                                                                                            '').replace(
                    '>',
                    '')
                if data_type == 'pandas.core.frame.DataFrame':
                    data_type = 'DataFrame'
                elif data_type == 'pandas.core.series.Series':
                    data_type = 'Series'

                data_str = self.autorepr(data)
            else:
                data_type = data.type
                data_size = data.size
                data_str = data.repr_value
            row = self.get_variable_row(data_name)
            if row != -1:
                self.setItem(row, 0, QTableWidgetItem(data_name))
                self.setItem(row, 1, QTableWidgetItem(data_type))
                self.setItem(row, 2, QTableWidgetItem(repr(data_size)))
                self.setItem(row, 3, QTableWidgetItem(data_str))
            else:
                new_row = self.rowCount()
                self.insertRow(new_row)
                self.setItem(new_row, 0, QTableWidgetItem(data_name))
                self.setItem(new_row, 1, QTableWidgetItem(data_type))
                self.setItem(new_row, 2, QTableWidgetItem(repr(data_size)))
                self.setItem(new_row, 3, QTableWidgetItem(data_str))

    def get_variable_row(self, var_name: str):
        for row in range(self.rowCount()):
            text = self.item(row, 0).text()
            if text == var_name:
                return row
        return -1

    def variable_exists(self, var_name: str):
        return self.get_variable_row(var_name) != -1

    def get_hier(self, item: QTableWidgetItem) -> int:
        i = 0
        all_nodes = [self.nodes[k] for k in self.nodes.keys()]
        while (1):
            if item.parent() not in all_nodes:
                i += 1
                item = item.parent()
            else:
                return i

    def show_data(self, data_name):
        import pandas as pd
        data_desc = self.get_current_var_desc()
        if data_desc.big:
            if issubclass(data_desc.cls, (str, list, tuple, pd.DataFrame)):
                ret = QMessageBox.warning(self, "警告", "数据过大，仅支持显示预览,是否确定继续？", QMessageBox.Ok | QMessageBox.Cancel,
                                          QMessageBox.Ok)
                if ret == QMessageBox.Ok:
                    return self._show_data(data_name)
                else:
                    return
            else:
                QMessageBox.warning(self, "警告", "数据过大,暂不支持此类型的查看")
            return
        else:
            return self._show_data(data_name)

    def slot_delete_var(self, name):
        """

        Args:
            data_name:

        Returns:

        """
        row = self.get_variable_row(name)
        assert row != -1
        data_name = self.item(row, 0).text()
        assert data_name == name
        self.removeRow(row)
        
    def keyPressEvent(self, event):
        """
        监控键盘事件
        Args:
            data_name:

        Returns:

        """
        key = event.key()
        ##Delete删除数据
        if (key == Qt.Key_Delete)and(self.get_current_var_name() != ""):
            self.delete_data(self.get_current_var_name())  

class PMWorkspaceInspectWidget(QWidget, PMDockObject):
    """
    用于承载 PMVariableTreeWidget以及相关的按钮。

    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.translator = create_translator(
            path=os.path.join(os.path.dirname(__file__), 'translations',
                              'qt_{0}.qm'.format(QLocale.system().name())))
        # print(self.tr('Variable Viewer'))
        layout = QVBoxLayout()
        self.var_tree = PMVariableTreeWidget(parent)
        layout.addWidget(self.var_tree)
        self.setLayout(layout)

    def get_widget_text(self) -> str:
        return self.tr('Workspace')

    def setup_ui(self):
        self.var_tree.setup_ui()
        layout = self.layout()
        layout.setContentsMargins(0, 0, 0, 0)

        self.signal_show_data_value = self.var_tree.signal_show_data_value
        self.signal_data_saveas = self.var_tree.signal_data_saveas
        self.signal_data_open = self.var_tree.signal_data_open

    def set_extension_lib(self, extension_lib):
        """
        与数据管理相连接。
        同时，在这个函数中定义了闭包子函数on_modification和on_deletion，
        也就是在数据变更或者删除时候调用的方法。
        """
        self.extension_lib = extension_lib
        self.data = self.extension_lib.Data.get_all_variables()
        self.var_tree.set_data(self.extension_lib.Data.get_all_public_variables())

        def on_changed(varname: str, variable, data_source: str):
            self.data[varname] = variable
            self.var_tree.set_data({varname: variable})
            # need to detect whether it is modified or created

        def on_deletion(varname: str, provider: str):
            self.extension_lib = extension_lib
            self.data = self.extension_lib.Data.get_all_variables()
            self.var_tree.slot_delete_var(varname)
            # self.var_tree.clear_all_nodes()
            # self.var_tree.set_data(self.extension_lib.Data.get_all_public_variables())

            # if provider != 'ipython':
            #     self.extension_lib.get_interface('ipython_console').run_command(
            #         '__delete_var(\'%s\')' % varname,
            #         hint_text=self.tr('delete variable %s') % varname,
            #         hidden=False)

        self.extension_lib.Data.add_data_changed_callback(on_changed)
        self.extension_lib.Data.add_data_deleted_callback(on_deletion)

    def bind_show_data(self, on_show_data):
        """
        绑定变量树视图在show_data事件触发时的回调。
        """
        self.var_tree._show_data = on_show_data

    def get_selected_var_names(self) -> List[str]:
        """
        获取当前选中的变量名称
        :return:
        """
        index: QModelIndex = None
        selected_rows = set()
        for index in self.var_tree.selectedIndexes():
            selected_rows.add(index.row())
        print([self.var_tree.item(row, 0).text() for row in selected_rows])
        return [self.var_tree.item(row, 0).text() for row in selected_rows]


if __name__ == '__main__':
    import sys
    import pandas as pd
    import numpy as np

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
                'b': 100,
                'c': np.array([1, 2, 3, 4, 5]),
                'd': pd.DataFrame([[1, 2, 3], [4, 5, 6]])}
    sa.var_tree.set_data(data_dic)
    sa.var_tree.add_select_data_callback(lambda name: sa.get_selected_var_names())
    sys.exit(app.exec_())
