import os

from PyQt5.QtCore import Qt, QCoreApplication, QModelIndex, QDir
from PyQt5.QtGui import QPixmap, QIcon, QCursor
from PyQt5.QtWidgets import QTreeView, QTreeWidgetItem, QTreeWidget, QFileSystemModel, QMenu, \
    QVBoxLayout, QWidget, QFileDialog, QPushButton, QHBoxLayout, QDirModel


class RewriteQFileSystemModel(QFileSystemModel):
    def __init__(self, parent=None):
        super().__init__(parent)

    def headerData(self, p_int, Qt_Orientation, role=None):
        if (p_int == 0) and (role == Qt.DisplayRole):
            return u'名称'
        elif (p_int == 1) and (role == Qt.DisplayRole):
            return u'大小'
        # elif (p_int == 2) and (role == Qt.DisplayRole):
        #     return '类型'
        # elif (p_int == 3) and (role == Qt.DisplayRole):
        #     return '修改日期'
        else:
            return super().headerData(p_int, Qt_Orientation, role)

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return 1


class PMFilesTreeview(QTreeView):
    def __init__(self, parent):
        super().__init__(parent)
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

        from pyminer2.extensions.extensionlib.pmext import PluginInterface

        my_dir = PluginInterface.get_work_dir()
        PluginInterface.set_work_dir(my_dir)
        print('当前工作路径：', my_dir)
        self.model = RewriteQFileSystemModel()
        self.model.setRootPath(my_dir)
        # self.setRootIndex(self.model.index(QDir.homePath()))

        self.setModel(self.model)
        self.setRootIndex(self.model.index(my_dir))
        self.setAnimated(False)
        self.setSortingEnabled(True)  # 启用排序
        self.header().setSortIndicatorShown(True)  # 启用标题排序
        self.setContextMenuPolicy(Qt.CustomContextMenu)

        self.init_context_menu()

    def bind_events(self, main_window):
        self.openAction.triggered.connect(main_window.openActionHandler)
        self.importAction.triggered.connect(main_window.importActionHandler)
        self.renameAction.triggered.connect(main_window.renameActionHandler)
        self.deleteAction.triggered.connect(main_window.deleteActionHandler)

        self.customContextMenuRequested.connect(self.show_context_menu)

    def init_context_menu(self):
        self.contextMenu = QMenu(self)
        self.openAction = self.contextMenu.addAction(u'打开')
        self.importAction = self.contextMenu.addAction(u'导入')
        self.renameAction = self.contextMenu.addAction(u'重命名')
        self.deleteAction = self.contextMenu.addAction(u'删除')

    def show_context_menu(self):
        self.contextMenu.popup(QCursor.pos())
        self.contextMenu.show()


class Stack(object):

    def __init__(self):
        # 创建空列表实现栈
        self.__list = []

    def is_empty(self):
        # 判断是否为空
        return self.__list == []

    def push(self,item):
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


class PMFilesTree(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        self.file_tree_view = PMFilesTreeview(self)
        self.file_tree_view.doubleClicked.connect(self.table_change)

        # 定义目录树栈
        self.pre_stack = Stack()
        self.next_stack = Stack()

        hlayout = QHBoxLayout()

        self.pre_dir_button = QPushButton()
        self.pre_dir_button.setToolTip("后退")
        self.pre_dir_button.setFlat(True)
        self.pre_dir_button.setEnabled(False)
        self.pre_dir_button.clicked.connect(self.pre_index_change)
        icon1 = QIcon()
        icon1.addPixmap(QPixmap(":/pyqt/source/images/pre.png"), QIcon.Normal, QIcon.On)
        self.pre_dir_button.setIcon(icon1)

        self.next_dir_button = QPushButton()
        self.next_dir_button.setToolTip("前进")
        self.next_dir_button.clicked.connect(self.next_index_change)
        self.next_dir_button.setFlat(True)
        self.next_dir_button.setEnabled(False)
        icon2 = QIcon()
        icon2.addPixmap(QPixmap(":/pyqt/source/images/next.png"), QIcon.Normal, QIcon.On)
        self.next_dir_button.setIcon(icon2)

        path_choose_button = QPushButton()
        path_choose_button.setToolTip("打开目录")
        icon3 = QIcon()
        icon3.addPixmap(QPixmap(":/pyqt/source/images/openfolder.png"), QIcon.Normal, QIcon.On)
        path_choose_button.setIcon(icon3)
        path_choose_button.clicked.connect(self.on_path_choose_request)

        hlayout.addWidget(self.pre_dir_button)
        hlayout.addWidget(self.next_dir_button)
        hlayout.addWidget(path_choose_button)
        layout.addLayout(hlayout)
        layout.addWidget(self.file_tree_view)

        self.setLayout(layout)

    def table_change(self, index: QModelIndex):

        if self.file_tree_view.model.fileInfo(index).isDir():
            self.file_tree_view.setRootIndex(index)
            self.pre_stack.push(index)
            self.pre_dir_button.setEnabled(True)

            if not self.pre_stack.is_empty():
                self.pre_dir_button.setEnabled(True)
            else:
                self.pre_dir_button.setEnabled(False)
            if not self.next_stack.is_empty():
                self.next_dir_button.setEnabled(True)
            else:
                self.next_dir_button.setEnabled(False)

    def pre_index_change(self):
        if not self.pre_stack.is_empty():
            self.next_dir_button.setEnabled(True)
            path = self.pre_stack.top()
            self.next_stack.push(path)
            self.pre_stack.pop()
            self.file_tree_view.setRootIndex(path)
        else:
            self.pre_dir_button.setEnabled(False)

    def next_index_change(self):
        if self.next_stack.is_empty():
            self.pre_dir_button.setEnabled(False)
            path = self.next_stack.pop()
            self.pre_stack.push(path)
            self.next_stack.pop()
            self.file_tree_view.setRootIndex(path)
        else:
            self.next_dir_button.setEnabled(False)

    def on_path_choose_request(self):
        from pyminer2.extensions.extensionlib.pmext import PluginInterface
        current_work_dir = PluginInterface.get_work_dir()
        path = QFileDialog.getExistingDirectory(self, '选择路径', current_work_dir)
        if path:
            fsmodel = RewriteQFileSystemModel()
            fsmodel.setRootPath(path)
            self.file_tree_view.setModel(fsmodel)
            self.file_tree_view.model = fsmodel
            self.file_tree_view.setRootIndex(
                self.file_tree_view.model.index(path))
            PluginInterface.set_work_dir(path)


class PMDatasetsTreeview(QTreeWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setContextMenuPolicy(Qt.CustomContextMenu)

        item_0 = QTreeWidgetItem(self)
        icon = QIcon()
        icon.addPixmap(QPixmap(":/pyqt/source/images/sc_viewdatasourcebrowser.png"), QIcon.Normal,
                       QIcon.On)
        item_0.setIcon(0, icon)
        item_0 = QTreeWidgetItem(self)
        icon1 = QIcon()
        icon1.addPixmap(QPixmap(":/pyqt/source/images/sc_dataarearefresh.png"), QIcon.Normal,
                        QIcon.On)
        item_0.setIcon(0, icon1)
        item_0 = QTreeWidgetItem(self)
        icon2 = QIcon()
        icon2.addPixmap(
            QPixmap(":/pyqt/source/images/lc_autosum.png"),
            QIcon.Normal,
            QIcon.On)
        item_0.setIcon(0, icon2)
        item_0 = QTreeWidgetItem(self)
        icon3 = QIcon()
        icon3.addPixmap(
            QPixmap(":/pyqt/source/images/lc_drawchart.png"),
            QIcon.Normal,
            QIcon.On)
        item_0.setIcon(0, icon3)
        item_0 = QTreeWidgetItem(self)
        icon4 = QIcon()
        icon4.addPixmap(QPixmap(":/pyqt/source/images/sc_switchcontroldesignmode.png"), QIcon.Normal,
                        QIcon.On)
        item_0.setIcon(0, icon4)
        item_0 = QTreeWidgetItem(self)
        icon5 = QIcon()
        icon5.addPixmap(
            QPixmap(":/pyqt/source/images/lc_rotateleft.png"),
            QIcon.Normal,
            QIcon.On)
        item_0.setIcon(0, icon5)
        item_0 = QTreeWidgetItem(self)
        icon6 = QIcon()
        icon6.addPixmap(
            QPixmap(":/pyqt/source/images/lc_optimizetable.png"),
            QIcon.Normal,
            QIcon.On)
        item_0.setIcon(0, icon6)
        self.translate()

    def translate(self):
        _translate = QCoreApplication.translate
        self.headerItem().setText(0, _translate("MainWindow", "工作区间"))
        __sortingEnabled = self.isSortingEnabled()
        self.setSortingEnabled(False)
        self.topLevelItem(0).setText(0, _translate("MainWindow", "数据集"))
        self.topLevelItem(1).setText(0, _translate("MainWindow", "数据处理"))
        self.topLevelItem(2).setText(0, _translate("MainWindow", "统计"))
        self.topLevelItem(3).setText(0, _translate("MainWindow", "可视化"))
        self.topLevelItem(4).setText(0, _translate("MainWindow", "模型"))
        self.topLevelItem(5).setText(0, _translate("MainWindow", "评估"))
        self.topLevelItem(6).setText(0, _translate("MainWindow", "结果"))
        self.setSortingEnabled(__sortingEnabled)
