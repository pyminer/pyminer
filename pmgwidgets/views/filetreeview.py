import os
from typing import List

from PyQt5.QtCore import Qt, QModelIndex, pyqtSignal, QLocale, QTranslator
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QTreeView, QFileSystemModel, QMenu, QApplication, QMessageBox, QInputDialog, \
    QLineEdit, QDialog, QVBoxLayout, QDialogButtonBox
from pmgwidgets.views.treecheckwidget import PMTreeCheckWidget


class PMFileSystemModel(QFileSystemModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        # self.setFilter(QDir.Dirs | QDir.AllDirs)

    def headerData(self, p_int, qt_orientation, role=None):
        if (p_int == 0) and (role == Qt.DisplayRole):
            return self.tr('Name')
        elif (p_int == 1) and (role == Qt.DisplayRole):
            return self.tr('Size')
        elif (p_int == 2) and (role == Qt.DisplayRole):
            return self.tr('Type')
        elif (p_int == 3) and (role == Qt.DisplayRole):
            return self.tr('Last Modified')
        else:
            return super().headerData(p_int, qt_orientation, role)

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return 1


class PMGFilesTreeview(QTreeView):
    """
        文件树
    """
    open_signal = pyqtSignal(str)
    new_file_signal = pyqtSignal(str)
    new_folder_signal = pyqtSignal(str)
    delete_file_signal = pyqtSignal(str)
    rename_file_signal = pyqtSignal(str, str)

    def __init__(self, initial_dir: str = '', parent=None):
        super().__init__(parent)
        self.initial_dir = initial_dir
        self.setup_ui()
        self.bind_events()

        self.filter_exts = True
        self.exts_to_filter = {
            'Program Scripts': {'.pyx': True, '.py': True, '.c': True, '.pyi': True, '.dll': True,
                                '.h': True, '.cpp': True, '.ipynb': True},
            'Documents': {'.txt': True, '.md': True, '.doc': True, '.docx': True, '.ppt': True, '.pptx': True},
            'Data Files': {'.csv': True, '.xls': True, '.xlsx': True, '.tab': True, '.dat': True, '.tsv': True,
                           '.sav': True, '.zsav': True, '.sas7bdat': True}}

    def setup_ui(self):
        """
        界面初始化
        :return:
        """
        path = os.path.join(os.path.dirname(__file__), 'translations', 'qt_{0}.qm'.format(QLocale.system().name()))
        inner_app = QApplication.instance()
        translator = QTranslator()
        translator.load(path)
        inner_app.installTranslator(translator)
        self.translator = translator

        self.setTabKeyNavigation(True)
        self.setDragEnabled(True)
        self.setDragDropOverwriteMode(True)
        self.setAlternatingRowColors(False)
        self.setUniformRowHeights(True)
        self.setSortingEnabled(True)
        self.setAnimated(True)
        self.setAllColumnsShowFocus(False)
        self.setWordWrap(False)
        self.setHeaderHidden(False)
        self.setObjectName("treeView_files")
        self.header().setSortIndicatorShown(True)

        self.model = PMFileSystemModel()
        self.model.setRootPath(self.initial_dir)

        self.setModel(self.model)
        self.setRootIndex(self.model.index(self.initial_dir))
        self.setAnimated(False)
        self.setSortingEnabled(True)  # 启用排序
        self.header().setSortIndicatorShown(True)  # 启用标题排序
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        self.init_context_menu()

    def bind_events(self):
        """
        回调、事件与信号初始化
        :return:
        """
        self.openAction.triggered.connect(self.on_open)
        self.importAction.triggered.connect(self.on_import)
        self.renameAction.triggered.connect(self.on_rename)
        self.deleteAction.triggered.connect(self.on_delete)

        self.copyAction.triggered.connect(self.on_copy)
        self.pasteAction.triggered.connect(self.on_paste)
        self.filterAction.triggered.connect(self.show_ext_filter_selection_dialog)

        self.new_file_action.triggered.connect(self.on_new_file)
        self.new_folder_action.triggered.connect(self.on_new_folder)

        self.customContextMenuRequested.connect(self.show_context_menu)

    def init_context_menu(self):
        """
        初始化右键菜单
        :return:
        """
        self.contextMenu = QMenu(self)
        self.openAction = self.contextMenu.addAction(self.tr('Open'))

        self.importAction = self.contextMenu.addAction(self.tr('Import'))
        self.importAction.setEnabled(False)

        self.new_file_or_folder_menu = QMenu(self.tr('New..'))
        self.contextMenu.addMenu(self.new_file_or_folder_menu)
        self.new_file_action = self.new_file_or_folder_menu.addAction(self.tr('File'))
        self.new_folder_action = self.new_file_or_folder_menu.addAction(self.tr('Folder'))
        self.new_file_or_folder_menu.addSeparator()

        self.copyAction = self.contextMenu.addAction(self.tr("Copy"))
        self.pasteAction = self.contextMenu.addAction(self.tr("Paste"))
        self.pasteAction.setEnabled(False)

        self.renameAction = self.contextMenu.addAction(self.tr('Rename'))
        self.deleteAction = self.contextMenu.addAction(self.tr('Delete'))
        self.filterAction = self.contextMenu.addAction(self.tr('Filter'))

    def show_context_menu(self):
        """
        显示上下文右键菜单
        :return:
        """
        self.contextMenu.popup(QCursor.pos())
        self.contextMenu.show()

    def get_current_file_path(self):
        """
        获取当前文件的路径
        :return:
        """
        index = self.currentIndex()
        file_info = self.model.fileInfo(index)
        return file_info.absoluteFilePath()

    def set_item_focus(self, file_path: str):
        """
        set item focus in TreeView
        :param file_path: File or Dir
        :return:
        """
        self.setCurrentIndex(self.model.index(file_path))

    def on_new_folder(self):
        """
        新建文件夹时出发的回调
        :return:
        """
        path = self.get_current_file_path()
        name, stat = QInputDialog.getText(self, self.tr('Please Input file name'), '', QLineEdit.Normal, '')
        if name.find('.') != -1:
            QMessageBox.critical(self, self.tr('Error'),
                                 self.tr('Folder name %s is illeagal!' % name))
            return
        if stat:
            if os.path.isdir(path):
                new_folder_path = os.path.join(path, name)
            else:
                new_folder_path = os.path.join(os.path.dirname(path), name)

            if os.path.exists(new_folder_path):
                self.set_item_focus(new_folder_path)  # 设置focus liugang 200923
                QMessageBox.critical(self, self.tr('Error'),
                                     self.tr('Folder %s already exists!' % name))
                return
            else:
                os.mkdir(new_folder_path)
                self.new_folder_signal[str].emit(new_folder_path)
                self.set_item_focus(new_folder_path)  # 设置focus liugang 200923

    def on_new_file(self):
        """
        新建文件时触发的回调
        :return:
        """
        path = self.get_current_file_path()
        name, stat = QInputDialog.getText(self, self.tr('Please Input file name'), '', QLineEdit.Normal, '')
        if stat:
            if os.path.isdir(path):
                new_file_path = os.path.join(path, name)
            else:
                new_file_path = os.path.join(os.path.dirname(path), name)

            if os.path.exists(new_file_path):
                self.set_item_focus(new_file_path)  # 设置focus  liugang 200923
                QMessageBox.critical(self, self.tr('Error'),
                                     self.tr('File %s already exists!' % name))
                return
            with open(new_file_path, 'wb') as f:
                f.close()
                self.new_file_signal[str].emit(new_file_path)

            self.set_item_focus(new_file_path)
            self.on_open()  # 创建文件后打开  liugang 200923

    def on_open(self):
        """
        点击‘open’时候触发的回调，相当于双击。
        :return:
        """
        path = self.get_current_file_path()
        self.open_signal[str].emit(path)

    def on_import(self):
        """

        :return:
        """
        pass

    def on_rename(self):
        """
        点击’重命名‘时候的回调。
        :return:
        """
        from pmgwidgets.platform import rename_file
        path = self.get_current_file_path()
        basename = os.path.basename(path)
        dir_name = os.path.dirname(path)
        name, stat = QInputDialog.getText(self, self.tr('Please Input file name'), '', QLineEdit.Normal, basename)
        if stat:
            new_absolute_path = os.path.join(dir_name, name)
            rename_result = rename_file(path, new_absolute_path)
            if not rename_result:
                QMessageBox.critical(self, self.tr('Error'),
                                     self.tr('Unable to Rename this file.'))
            else:
                self.rename_file_signal[str, str].emit(path, new_absolute_path)

    def on_delete(self):
        """
        点击’删除‘时的回调
        :return:
        """
        from pmgwidgets.platform import move_to_trash
        path = self.get_current_file_path()

        moved_successful = move_to_trash(path)
        if not moved_successful:
            QMessageBox.critical(self, self.tr('Error'),
                                 self.tr('Unable to Move this file to recycle bin.'))
        else:
            self.delete_file_signal[str].emit(path)

    def on_copy(self):
        """
        copy file or dir , save path in pasteAction data.
        :return:
        """
        path = self.get_current_file_path()
        self.pasteAction.setEnabled(True)
        self.pasteAction.setData(path)

    def on_paste(self):
        """
        Paste file or dir in pasteAction data
        :return:
        """
        from pmgwidgets.platform import copy_paste
        path = self.get_current_file_path()
        target_dir_name = path if os.path.isdir(path) else os.path.dirname(path)
        source_path = self.pasteAction.data()
        # File
        if os.path.isfile(source_path):
            source_file_name = os.path.basename(source_path)
            # if exist ,rename to copy_xxx
            if os.path.isfile(os.path.join(target_dir_name, source_file_name)):
                target_file_name = "copy_{0}".format(source_file_name)
            else:
                target_file_name = source_file_name
            target_path = os.path.join(target_dir_name, target_file_name)
        # Directory
        else:
            last_dir_name = os.path.split(source_path)[-1]
            # if exist , rename dir copy_xxxx
            if os.path.isdir(os.path.join(target_dir_name, last_dir_name)):
                target_name = "copy_{0}".format(last_dir_name)
            else:
                target_name = last_dir_name
            target_path = os.path.join(target_dir_name, target_name)

        copy_succ = copy_paste(source_path, target_path)
        if not copy_succ:
            QMessageBox.critical(self, self.tr('Error'),
                                 self.tr('Copy File or Directory Error.'))
        else:
            self.set_item_focus(target_path)

    def show_ext_filter_selection_dialog(self):

        self.dlg = QDialog(self)
        self.dlg.setWindowTitle(self.tr('Extension Name To Show'))
        self.dlg.setLayout(QVBoxLayout())
        check_widget = PMTreeCheckWidget(data=self.exts_to_filter)
        self.dlg.check_widget = check_widget
        self.dlg.layout().addWidget(check_widget)
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        buttonBox.accepted.connect(self.on_ext_filter_changed)
        buttonBox.rejected.connect(self.dlg.deleteLater)
        # 清除选择功能不完善目前禁用
        # button_clear = buttonBox.addButton(self.tr('Clear Filter'), QDialogButtonBox.ApplyRole)
        # button_clear.clicked.connect(self.clear_ext_filter)
        self.dlg.layout().addWidget(buttonBox)
        self.dlg.exec_()

    def on_ext_filter_changed(self):
        """
        当扩展名过滤失效的时候。
        :return:
        """
        self.exts_to_filter = self.dlg.check_widget.get_data()
        self.update_ext_filter()
        self.dlg.deleteLater()

    def clear_ext_filter(self):
        self.set_ext_filter(None)
        self.dlg.deleteLater()

    def update_ext_filter(self):
        """
        刷新扩展名过滤。
        :return:
        """
        l = []
        for key in self.exts_to_filter.keys():
            for name in self.exts_to_filter[key].keys():
                if self.exts_to_filter[key][name]:
                    l.append('*' + name)
        self.set_ext_filter(l)

    def set_ext_filter(self, ext_names: List[str]):
        """
        文件名过滤
        例如要过滤出.py和.pyx文件，就是ext_names=['*.py','*.pyx']
        discard功能不太完善，目前先禁用。
        :param ext_names:
        :return:
        """
        if ext_names is not None:
            self.model.setNameFilterDisables(False)
            self.model.setNameFilters(ext_names)
        else:
            self.model.setNameFilterDisables(True)


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


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    tree = PMGFilesTreeview('c:/users/', None)
    tree.show()
    sys.exit(app.exec_())
