import os
import threading
from typing import Dict, TYPE_CHECKING, Callable, Any, List

from PySide2.QtWidgets import QTreeWidget, QTreeWidgetItem, QWidget, QVBoxLayout, QMenu, \
    QMessageBox, QFileDialog, QInputDialog, QApplication
from PySide2.QtCore import Signal, Qt, QLocale, QTranslator

from lib.extensions.extensionlib import BaseExtension, BaseInterface

if TYPE_CHECKING:
    from .data_viewer import PMVariableViewerWidget
    from .inspectortable import PMWorkspaceInspectWidget, PMVariableTreeWidget
else:
    from .inspectortable import PMWorkspaceInspectWidget

file_name = os.path.join(os.path.dirname(__file__), 'translations', 'qt_%s.qm' % QLocale.system().name())
app = QApplication.instance()
trans_filetree = QTranslator()
app.trans_filetree = trans_filetree
trans_filetree.load(QLocale.system(), file_name)
app.installTranslator(trans_filetree)


class Extension(BaseExtension):
    interace: 'Interface' = None

    def on_loading(self):
        pass

    def on_load(self):
        self.workspace: 'PMWorkspaceInspectWidget' = self.widgets['PMWorkspaceInspectWidget']
        self.workspace.var_tree.extension_lib = self.extension_lib
        self.workspace.extension_lib = self.extension_lib

        self.data_viewer: 'PMVariableTreeWidget' = None

        self.interface.data_viewer = self.workspace.var_tree
        self.interface.workspace_widget = self.workspace
        self.workspace.bind_show_data(self.on_show_data)

        # self.workspace.connect_to_datamanager(self.extension_lib)
        # 注意：上边被注释掉的一句代码是既不规范也不正确的写法。因为当插件on_load方法调用的时候，
        # 尚未调用setup_ui方法，这就造成了一些相关的变量和控件尚未加载，可能获取不到。
        # 正确的做法如下所示
        self.extension_lib.Signal.get_widgets_ready_signal().connect(self.on_widgets_ready)

    def on_widgets_ready(self):
        self.workspace.set_extension_lib(self.extension_lib)
        self.extension_lib.UI.get_toolbar_widget('toolbar_home', 'button_open_variable').clicked.connect(
            self.workspace.var_tree.on_open_variable)
        # self.extension_lib.UI.get_toolbar_widget('toolbar_home', 'button_save_workspace').clicked.connect(
        #     self.workspace.var_tree.on_save_workspace)
        self.extension_lib.get_interface('file_tree').add_open_file_callback('.pkl',
                                                                             self.workspace.var_tree.open_variable)
        self.extension_lib.get_interface('file_tree').add_open_file_callback('.pmd',
                                                                             self.workspace.var_tree.open_variable)

    def on_show_data(self, dataname: str):
        if self.data_viewer is None:
            app = QApplication.instance()
            self.data_viewer_cls = self.widget_classes['PMVariableViewerWidget']
            self.data_viewer: 'PMVariableViewerWidget' = \
                self.extension_lib.insert_widget(self.data_viewer_cls,
                                                 'new_dock_window',
                                                 {
                                                     "name": "data_view_table",
                                                     "side": "top",
                                                     "text": app.tr("Variable Viewer")})
            self.data_viewer.set_lib(self.extension_lib)
            self.data_viewer.on_dock_widget_deleted = self.on_dock_widget_deleted
        self.data_viewer.show_data(dataname)

    def on_dock_widget_deleted(self):
        self.data_viewer = None


class Interface(BaseInterface):
    # data_viewer: 'PMVariableTreeWidget' = None
    workspace_widget: 'PMWorkspaceInspectWidget' = None

    def add_select_data_callback(self, callback: Callable):
        """
        添加数据被选中时的回调函数。也就是当你单击数据时候的回调函数。
        """
        self.workspace_widget.var_tree.add_select_data_callback(callback)

    def save_workspace(self):
        """
        保存整个工作空间
        Returns:

        """
        self.workspace_widget.var_tree.on_save_workspace()

    def save_current_variable(self):
        """
        TODO:其实导出数据应该用dataio插件来做比较好。
        Args:
            ext:

        Returns:

        """
        self.workspace_widget.var_tree.on_save_variable('Pickle File(*.pkl);;PyMiner Data(*.pmd)')

    def get_selected_variables(self) -> List[str]:
        """
        获取选中的数据名称。
        :return:
        """
        return self.workspace_widget.get_selected_var_names()
