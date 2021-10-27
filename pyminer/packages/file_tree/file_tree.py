import os
import platform
from typing import Dict, Callable, List

from PySide2.QtCore import Qt, QModelIndex
from PySide2.QtGui import QPixmap, QIcon, QCloseEvent
from PySide2.QtWidgets import QVBoxLayout, QWidget, QFileDialog, QPushButton, QHBoxLayout, QLineEdit, QToolButton, \
    QApplication, QMessageBox

from widgets import PMGFilesTreeview, PMDockObject, in_unit_test, UndoManager


class PMFilesTree(QWidget, PMDockObject):
    extension_lib = None
    open_methods_dic: Dict[str, List[Callable]] = {}
    settings: Dict[str, List[Callable]] = {}

    def __init__(self, parent=None):
        global extension_lib
        super().__init__(parent)

        extension_lib = self.extension_lib
        self.undo_manager = UndoManager(stack_size=10)

    def get_widget_text(self) -> str:
        return self.tr('Files Tree')

    def setup_ui(self):
        if in_unit_test():
            my_dir = ''
        else:
            my_dir = self.extension_lib.Program.get_work_dir()

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.file_tree_view = PMGFilesTreeview(my_dir, self)
        self.file_tree_view.sortByColumn(0, Qt.AscendingOrder)

        self.file_tree_view.open_signal[str].connect(self.open_file)  # 文件树右键菜单打开功能绑定  20200921  liugang
        self.file_tree_view.open_folder_signal[str].connect(self.change_current_path)
        self.file_tree_view.signal_ext_filter_changed.connect(self.slot_ext_filter_changed)
        hlayout = QHBoxLayout()
        layout.addLayout(hlayout)
        self.setLayout(layout)

        self.pre_dir_button = QToolButton()
        self.pre_dir_button.setFixedWidth(20)
        self.pre_dir_button.setToolTip(self.tr("Back"))
        self.pre_dir_button.setEnabled(False)
        self.pre_dir_button.clicked.connect(self.goto_pre_dir)

        self.parent_dir_button = QToolButton()
        self.parent_dir_button.setFixedWidth(20)
        self.parent_dir_button.setToolTip(self.tr("Parent Path"))
        self.parent_dir_button.clicked.connect(self.goto_parent_dir)

        icon_back = QIcon()
        icon_back.addPixmap(
            QPixmap(":/resources/icons/undo.svg"),
            QIcon.Normal,
            QIcon.On)

        icon_up = QIcon()
        icon_up.addPixmap(
            QPixmap(os.path.join(os.path.dirname(__file__), 'src', 'up.svg')),
            QIcon.Normal,
            QIcon.On)

        self.pre_dir_button.setIcon(icon_back)
        self.parent_dir_button.setIcon(icon_up)

        path_choose_button = QToolButton()
        path_choose_button.setFixedWidth(20)
        path_choose_button.setToolTip(self.tr("Open Path"))
        # path_choose_button.setStyleSheet("border: none;")
        icon_choose_path = QIcon()
        icon_choose_path.addPixmap(
            QPixmap(":/resources/icons/open_folder.svg"),
            QIcon.Normal,
            QIcon.On)
        path_choose_button.setIcon(icon_choose_path)
        path_choose_button.clicked.connect(self.on_path_choose_request)

        self.addressEntry = QLineEdit()
        self.addressEntry.setStyleSheet("border-style: outset; border:1px solid rgba(0, 0, 0, 0.5);border-radius:5px;")
        self.addressEntry.setText(my_dir)
        self.addressEntry.home(False)
        self.addressEntry.setAlignment(Qt.AlignLeft)

        self.addressEntry.returnPressed.connect(self.returnPressed)

        self.filter_file_btn = QPushButton()
        self.filter_file_btn.setText('.')
        self.filter_file_btn.clicked.connect(self.file_tree_view.show_ext_filter_selection_dialog)
        self.pre_dir_button.setEnabled(True)

        hlayout.addWidget(self.addressEntry)
        hlayout.addWidget(path_choose_button)

        hlayout.addWidget(self.pre_dir_button)
        hlayout.addWidget(self.parent_dir_button)
        # hlayout.addWidget(self.next_dir_button)
        layout.addWidget(self.file_tree_view)
        self.read_settings()

    def goto_parent_dir(self):
        """
        前往父路径
        :return:
        """
        path = self.file_tree_view.get_root_path()
        parent_path = os.path.dirname(path)
        self.change_current_path(parent_path)

    def returnPressed(self):
        if os.path.isdir(self.addressEntry.text()):
            self.change_current_path(self.addressEntry.text())
        else:
            QMessageBox.warning(self, self.tr('Warning'),
                                self.tr('\'%s\' is not a directory.\n') % self.addressEntry.text())

    def open_file(self, path: str):
        import os
        ext: str = os.path.splitext(path)[1]
        open_methods_for_this_ext = self.open_methods_dic.get(ext)
        if open_methods_for_this_ext is not None:
            for method in open_methods_for_this_ext:
                method(path)
        else:
            if platform.system().lower() == 'windows':
                os.startfile(path)
            elif platform.system().lower() == 'linux':
                os.popen('xdg-open %s' % path)
            else:
                raise NotImplementedError

    def file_item_double_clicked(self, index: QModelIndex):
        file_info = self.file_tree_view.model.fileInfo(index)
        if self.file_tree_view.model.fileInfo(index).isDir():
            path: str = self.file_tree_view.model.filePath(index)
            self.change_current_path(path)
        else:
            self.open_file(file_info.absoluteFilePath())

    def goto_pre_dir(self):
        """
        前往之前的路径
        :return:
        """
        path = self.undo_manager.undo()
        index = self.file_tree_view.model.index(path)
        if index is not None:
            self.file_tree_view.setRootIndex(index)
            self.addressEntry.clear()
            self.addressEntry.setText(self.file_tree_view.model.filePath(index))
            self.addressEntry.home(False)
        else:
            self.pre_dir_button.setEnabled(False)

    def on_path_choose_request(self):
        """
        选择路径时触发的函数
        :return:
        """
        if not in_unit_test():
            current_work_dir = self.extension_lib.Program.get_work_dir()
        else:
            current_work_dir = ''
        path = QFileDialog.getExistingDirectory(self, '...', current_work_dir)
        if path:
            self.change_current_path(path)

    def get_split_portion_hint(self):
        """
        获取切分比例的提示。
        :return:
        """
        return (0.2, None)

    def change_current_path(self, path: str):
        """
        切换当前路径
        :param path: 绝对路径
        :return:
        """
        last_path = self.file_tree_view.get_root_path()
        if os.path.isdir(path) and os.path.normcase(path) != os.path.normcase(last_path):

            self.undo_manager.push(last_path)
            self.addressEntry.clear()
            self.addressEntry.setText(path)
            self.addressEntry.home(False)
            self.file_tree_view.model.setRootPath(path)
            self.file_tree_view.setRootIndex(self.file_tree_view.model.index(path))
            self.file_tree_view.setCurrentIndex(self.file_tree_view.model.index(path))
            self.pre_dir_button.setEnabled(True)
            if path.endswith(':/') or path == '':  # 根目录下，不可撤销
                self.parent_dir_button.setEnabled(False)
            else:
                self.parent_dir_button.setEnabled(True)
            self.addressEntry.setToolTip(self.file_tree_view.get_root_path())
            if not in_unit_test():
                self.extension_lib.Program.set_work_dir(path)

    def read_settings(self):
        """
        加载设置,更新字典。
        ext_names:代表扩展名类型。

        :return:
        """
        import json
        if in_unit_test():
            path = 'c:/users/hzy/.pyminer/packages/file_tree'
        else:
            path = self.extension_lib.Program.get_plugin_data_path('file_tree')
        with open(os.path.join(os.path.dirname(__file__), 'settings.json'), 'r') as f:
            self.settings = json.load(f)
        if os.path.exists(os.path.join(path, 'settings.json')):
            with open(os.path.join(path, 'settings.json'), 'r') as f:
                custom_settings = json.load(f)

                exts_to_filter: Dict[str, Dict] = self.settings['ext_names']
                for k in exts_to_filter.keys():
                    if k in self.settings['ext_names'] and k in custom_settings['ext_names']:
                        exts_to_filter[k].update(custom_settings['ext_names'][k])
                self.settings['ext_names'] = exts_to_filter
                for k in custom_settings.keys():
                    if k != 'ext_names':
                        self.settings[k] = custom_settings[k]

                self.file_tree_view.filter_exts = self.settings['filter_exts']
                self.file_tree_view.exts_to_filter = self.settings['ext_names']

        print(self.settings)
        self.file_tree_view.update_ext_filter()

    def save_settings(self):
        """
        保存设置。
        :return:
        """
        import json
        if not in_unit_test():
            path = self.extension_lib.Program.get_plugin_data_path('file_tree')
        else:
            path = 'c:/users/hzy/.pyminer/packages/file_tree'
        with open(os.path.join(path, 'settings.json'), 'w') as f:
            json.dump(self.settings, f, indent=4)

    def slot_ext_filter_changed(self, ext_names: dict):
        self.settings['ext_names'] = ext_names
        self.settings['filter_exts'] = self.file_tree_view.filter_exts
        print(self.settings)

    def closeEvent(self, a0: 'QCloseEvent') -> None:
        self.save_settings()
        super(PMFilesTree, self).closeEvent(a0)


if __name__ == '__main__':
    import sys
    import cgitb

    cgitb.enable(format='text')
    app = QApplication(sys.argv)

    w = PMFilesTree()
    w.show()
    w.setup_ui()
    w.change_current_path('c:/users/12957/desktop')

    sys.exit(app.exec_())
