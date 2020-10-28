import os
from typing import Dict, Callable, List
from PyQt5.QtCore import Qt, QModelIndex
from PyQt5.QtGui import QPixmap, QIcon, QCloseEvent
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QFileDialog, QPushButton, QHBoxLayout, QLineEdit
from pmgwidgets import PMGFilesTreeview, PMDockObject


class Stack(object):

    def __init__(self):
        # 创建空列表实现栈
        self.__list = []

    def is_empty(self):
        # 判断是否为空
        return self.__list == []

    def push(self, item):
        # 压栈，添加元素
        self.__list.append(item)

    def pop(self):
        # 弹栈，弹出最后压入栈的元素
        if self.is_empty():
            return
        else:
            return self.__list.pop()

    def top(self):
        # 取最后压入栈的元素
        if self.is_empty():
            return
        else:
            return self.__list[-1]

    def __len__(self):
        return len(self.__list)

    def __str__(self):
        return str(self.__list)


class PMFilesTree(QWidget, PMDockObject):
    extension_lib = None
    open_methods_dic: Dict[str, List[Callable]] = {}
    settings: Dict[str, List[Callable]] = {}

    def __init__(self, parent=None):
        global extension_lib
        super().__init__(parent)

        extension_lib = self.extension_lib

    def setup_ui(self):

        my_dir = self.extension_lib.Program.get_work_dir()

        layout = QVBoxLayout()
        self.file_tree_view = PMGFilesTreeview(my_dir, self)
        self.file_tree_view.extension_lib = self.extension_lib

        self.file_tree_view.doubleClicked.connect(self.file_item_double_clicked)
        self.file_tree_view.open_signal[str].connect(self.open_file)  # 文件树右键菜单打开功能绑定  20200921  liugang

        # 定义目录树栈
        self.pre_stack = self.file_tree_view.model.index(my_dir)
        self.root_index = self.file_tree_view.model.index(my_dir)
        hlayout = QHBoxLayout()

        self.pre_dir_button = QPushButton()
        self.pre_dir_button.setFixedWidth(20)
        self.pre_dir_button.setToolTip(self.tr("Back"))
        self.pre_dir_button.setFlat(True)
        self.pre_dir_button.setStyleSheet("border: none;")
        self.pre_dir_button.setEnabled(False)
        self.pre_dir_button.clicked.connect(self.pre_index_change)
        icon1 = QIcon()
        icon1.addPixmap(
            QPixmap(":/color/source/theme/color/icons/undo.svg"),
            QIcon.Normal,
            QIcon.On)

        self.pre_dir_button.setIcon(icon1)

        path_choose_button = QPushButton()
        path_choose_button.setFixedWidth(20)
        path_choose_button.setToolTip(self.tr("Open Path"))
        path_choose_button.setStyleSheet("border: none;")
        icon3 = QIcon()
        icon3.addPixmap(
            QPixmap(":/color/source/theme/color/icons/open_folder.svg"),
            QIcon.Normal,
            QIcon.On)
        path_choose_button.setIcon(icon3)
        path_choose_button.clicked.connect(self.on_path_choose_request)

        self.addressEntry = QLineEdit()
        self.addressEntry.setStyleSheet("border-style: outset; border:1px solid rgba(0, 0, 0, 0.5);border-radius:5px;")
        self.addressEntry.setText(my_dir)
        self.addressEntry.home(False)
        self.addressEntry.setAlignment(Qt.AlignLeft)
        self.addressEntry.returnPressed.connect(self.returnPressed)
        # qspacer = QSpacerItem(20, 20, QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        #
        # # hlayout.addItem(qspacer)
        self.filter_file_btn = QPushButton()
        self.filter_file_btn.setText('.')
        self.filter_file_btn.clicked.connect(self.file_tree_view.show_ext_filter_selection_dialog)

        hlayout.addWidget(self.addressEntry)
        hlayout.addWidget(path_choose_button)
        hlayout.addWidget(self.pre_dir_button)
        # hlayout.addWidget(self.next_dir_button)
        layout.addLayout(hlayout)
        layout.addWidget(self.file_tree_view)

        self.setLayout(layout)

        self.read_settings()
        if len(self.settings.items()) == 0:
            self.settings = {'ext_names': self.file_tree_view.exts_to_filter}

    def table_change(self, index):
        self.file_tree_view.setRootIndex(index)
        self.pre_stack = index
        self.addressEntry.clear()
        self.addressEntry.setText(self.file_tree_view.model.filePath(index))
        self.addressEntry.home(False)
        self.pre_dir_button.setEnabled(True)

    def returnPressed(self):
        index = self.file_tree_view.model.index(self.addressEntry.text())
        if index.isValid():
            self.file_tree_view.setRootIndex(index)

    def open_file(self, path: str):
        import os
        ext: str = os.path.splitext(path)[1]
        open_methods_for_this_ext = self.open_methods_dic.get(ext)
        if open_methods_for_this_ext is not None:
            for method in open_methods_for_this_ext:
                method(path)
        else:
            os.startfile(path)

    def file_item_double_clicked(self, index: QModelIndex):
        file_info = self.file_tree_view.model.fileInfo(index)
        if self.file_tree_view.model.fileInfo(index).isDir():
            self.table_change(index)
        else:
            self.open_file(file_info.absoluteFilePath())

    def pre_index_change(self):
        if self.pre_stack != self.root_index:
            index = self.pre_stack.parent()
            self.file_tree_view.setRootIndex(index)
            self.addressEntry.clear()
            self.addressEntry.setText(self.file_tree_view.model.filePath(index))
            self.addressEntry.home(False)
            self.pre_stack = self.pre_stack.parent()
            if self.pre_stack == self.root_index:
                self.pre_dir_button.setEnabled(False)
        else:
            self.pre_dir_button.setEnabled(False)

    def on_path_choose_request(self):
        """
        选择路径时触发的函数
        :return:
        """
        current_work_dir = self.extension_lib.Program.get_work_dir()
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
        if os.path.isdir(path):
            self.addressEntry.clear()
            self.addressEntry.setText(path)
            self.addressEntry.home(False)
            fsmodel = self.file_tree_view.model
            fsmodel.setRootPath(path)
            self.file_tree_view.setRootIndex(
                self.file_tree_view.model.index(path))
            self.extension_lib.Program.set_work_dir(path)

    def read_settings(self):
        """
        加载设置
        ext_names:代表扩展名类型。

        :return:
        """
        import json
        path = os.path.dirname(__file__)
        with open(os.path.join(path, 'settings.json'), 'r') as f:
            self.settings = json.load(f)
            self.file_tree_view.exts_to_filter = self.settings['ext_names']
            self.file_tree_view.update_ext_filter()

    def save_settings(self):
        """
        保存设置。
        :return:
        """
        import json
        path = os.path.dirname(__file__)
        with open(os.path.join(path, 'settings.json'), 'w') as f:
            json.dump(self.settings, f, indent=4)

    def closeEvent(self, a0: 'QCloseEvent') -> None:
        self.save_settings()
        super(PMFilesTree, self).closeEvent(a0)
