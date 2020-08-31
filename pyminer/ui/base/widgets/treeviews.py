import os

from PyQt5.QtWidgets import QTreeView, QWidget, QTreeWidgetItem, QTreeWidget, QFileSystemModel, QMenu
from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtGui import QPixmap, QIcon, QCursor
from pyminer.pmutil import get_root_dir


class RewriteQFileSystemModel(QFileSystemModel):
    def __init__(self, parent=None):
        super().__init__(parent)

    def headerData(self, p_int, Qt_Orientation, role=None):
        if ((p_int == 0) and (role == Qt.DisplayRole)):
            return u'名称'
        elif ((p_int == 1) and (role == Qt.DisplayRole)):
            return u'大小'
        elif ((p_int == 2) and (role == Qt.DisplayRole)):
            return '类型'
        elif ((p_int == 3) and (role == Qt.DisplayRole)):
            return '修改日期'
        else:
            return super().headerData(p_int, Qt_Orientation, role)


class PMFilesTreeview(QTreeView):
    def __init__(self,parent):
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

        # 文件管理器
        # my_dir = QDir.rootPath()
        my_dir = os.path.dirname('')#get_root_dir())
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
        icon2.addPixmap(QPixmap(":/pyqt/source/images/lc_autosum.png"), QIcon.Normal, QIcon.On)
        item_0.setIcon(0, icon2)
        item_0 = QTreeWidgetItem(self)
        icon3 = QIcon()
        icon3.addPixmap(QPixmap(":/pyqt/source/images/lc_drawchart.png"), QIcon.Normal, QIcon.On)
        item_0.setIcon(0, icon3)
        item_0 = QTreeWidgetItem(self)
        icon4 = QIcon()
        icon4.addPixmap(QPixmap(":/pyqt/source/images/sc_switchcontroldesignmode.png"), QIcon.Normal,
                        QIcon.On)
        item_0.setIcon(0, icon4)
        item_0 = QTreeWidgetItem(self)
        icon5 = QIcon()
        icon5.addPixmap(QPixmap(":/pyqt/source/images/lc_rotateleft.png"), QIcon.Normal, QIcon.On)
        item_0.setIcon(0, icon5)
        item_0 = QTreeWidgetItem(self)
        icon6 = QIcon()
        icon6.addPixmap(QPixmap(":/pyqt/source/images/lc_optimizetable.png"), QIcon.Normal, QIcon.On)
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
