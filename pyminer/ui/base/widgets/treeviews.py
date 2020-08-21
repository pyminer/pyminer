from PyQt5.QtWidgets import QTreeView, QWidget, QTreeWidgetItem, QTreeWidget
from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtGui import QPixmap, QIcon


class PMFilesTreeview(QTreeView):
    def __init__(self):
        super().__init__()
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
