import base64
import datetime
import getpass
import json
import logging
import time
import webbrowser
import qdarkstyle
import os, sys
import pandas as pd

# import win32api
# import pywintypes
import shutil

# 导入PyQt5模块
from PyQt5.QtCore import QSize, pyqtSignal, QTimer, QRectF, Qt
from PyQt5.QtWidgets import QApplication, QStyleFactory, QDesktopWidget, QMessageBox, QSplashScreen, QTreeWidgetItem, \
    QListWidgetItem, QWidget, QHBoxLayout, QGridLayout, QLabel, QSpacerItem, QSizePolicy, \
    QGraphicsDropShadowEffect, QListWidget, QGraphicsScene, QAbstractItemView, QTableWidgetItem, QGraphicsObject, \
    QGraphicsItem, QFileDialog, QSystemTrayIcon, QInputDialog, QLineEdit
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QMenu
from PyQt5.QtGui import QIcon, QPixmap, QImage, QColor, QPainter, QPainterPath, QPen, QTextCursor, QBrush, QCursor

# 导入功能组件

from pyminer.share import threads  # 导入多线程处理模块
from pyminer.features.sample import io  # 导入数据相关操作模块
from pyminer.features.visualize import base as plot  # 导入可视化相关操作模块
from pyminer.features.modelling import base as model  # 导入模型相关操作模块
from pyminer.features.extensions.package_manager import package_manager  # 导入插件模块
from pyminer.features.report import pyreport  # 导入输出报告模块

# 导入UI相关模块
from pyminer.share.threads import ThreadJupyter
from pyminer.ui.base.mainForm import Ui_MainWindow
from pyminer.ui.base.newItem import NewItemForm
from pyminer.ui.base.aboutMe import AboutMeForm
from pyminer.ui.base.option import Ui_Form as Option_Ui_Form, OptionForm
from pyminer.ui.source.qss.qss_tools import QssTools

from pyminer.pmutil import get_root_dir, get_application
from pyminer.ui.base.widgets.notificationwidget import NotificationWindow
from pyminer.ui.base.widgets.menu_tool_stat_bars import init_actions
from pyminer.share.datamanager import DataManager
from pyminer.features.statistics.test_basic_stats import StatsBaseForm

from pyminer.features.preprocess.PMDataInfoForm import DataInfoForm
from pyminer.features.preprocess.PMDataFilterForm import DataFilterForm
from pyminer.features.preprocess.PMDataRoleForm import DataRoleForm
from pyminer.features.preprocess.PMDataRowFilterForm import DataRowFilterForm
from pyminer.features.preprocess.PMDataColumnDescForm import DataColumnDescForm
from pyminer.features.preprocess.PMDataDeleteColumnForm import DataDeleteColumnForm
from pyminer.features.preprocess.PMDataDeleteRowForm import DataDeleteRowForm
from pyminer.features.preprocess.PMDataMergeHorizontalForm import DataMergeHorizontalForm
from pyminer.features.preprocess.PMDataMergeVerticalForm import DataMergeVerticalForm
from pyminer.features.preprocess.PMDataColumnEncodeForm import DataColumnEncodeForm
from pyminer.features.preprocess.PMDataColumnNameForm import DataColumnNameForm
from pyminer.features.preprocess.PMDataMissingValueForm import DataMissingValueForm
from pyminer.features.preprocess.PMDataNewColumnForm import DataNewColumnForm
from pyminer.features.preprocess.PMDataPartitionForm import DataPartitionForm
from pyminer.features.preprocess.PMDataReplaceForm import DataReplaceForm
from pyminer.features.preprocess.PMDataSampleForm import DataSampleForm
from pyminer.features.preprocess.PMDataSortForm import DataSortForm
from pyminer.features.preprocess.PMDataStandardForm import DataStandardForm
from pyminer.features.preprocess.PMDataTransposeForm import DataTransposeForm

#导入插件相关组件
from pyminer.features.extensions.extensions_manager.manager import extensions_manager

TextStyle = """
QMessageBox QPushButton[text="OK"] {
    qproperty-text: "确认";
}
QMessageBox QPushButton[text="Open"] {
    qproperty-text: "打开";
}
QMessageBox QPushButton[text="Save"] {
    qproperty-text: "保存";
}
QMessageBox QPushButton[text="Cancel"] {
    qproperty-text: "取消";
}
QMessageBox QPushButton[text="Close"] {
    qproperty-text: "关闭";
}
QMessageBox QPushButton[text="Discard"] {
    qproperty-text: "不保存";
}
QMessageBox QPushButton[text="Don't Save"] {
    qproperty-text: "不保存";
}
QMessageBox QPushButton[text="Apply"] {
    qproperty-text: "应用";
}
QMessageBox QPushButton[text="Reset"] {
    qproperty-text: "重置";
}
QMessageBox QPushButton[text="Restore Defaults"] {
    qproperty-text: "恢复默认";
}
QMessageBox QPushButton[text="Help"] {
    qproperty-text: "帮助";
}
QMessageBox QPushButton[text="Save All"] {
    qproperty-text: "保存全部";
}
QMessageBox QPushButton[text="&Yes"] {
    qproperty-text: "是";
}
QMessageBox QPushButton[text="Yes to &All"] {
    qproperty-text: "全部都是";
}
QMessageBox QPushButton[text="&No"] {
    qproperty-text: "不";
}
QMessageBox QPushButton[text="N&o to All"] {
    qproperty-text: "全部都不";
}
QMessageBox QPushButton[text="Abort"] {
    qproperty-text: "终止";
}
QMessageBox QPushButton[text="Retry"] {
    qproperty-text: "重试";
}
QMessageBox QPushButton[text="Ignore"] {
    qproperty-text: "忽略";
}
QMessageBox::warning QPushButton[text="&No"] {
    qproperty-text: "否";
}
QInputDialog QPushButton[text="OK"] {
    qproperty-text: "确认";
}
QInputDialog QPushButton[text="Cancel"] {
    qproperty-text: "取消";
}
"""


class Application(QApplication):
    def __init__(self, argv):
        QApplication.__init__(self, argv)
        QApplication.setStyle('Fusion')

    def _slot_setStyle(self):
        """
        设置app样式
        """
        self.setStyleSheet('')  # 重置当前app样式
        tmp = self.sender().objectName()[6:]
        print(QStyleFactory.keys())
        if tmp in QStyleFactory.keys():
            self.setStyle(tmp)
        elif tmp == 'Qdarkstyle':
            self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())


class CustomRect(QGraphicsObject):
    def __init__(self):
        super(CustomRect, self).__init__()
        self.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)  # 拖动

    def boundingRect(self):
        return QRectF(0, 0, 200, 50)

    def paint(self, painter, styles, widget=None):
        pen1 = QPen(Qt.SolidLine)
        pen1.setColor(QColor(128, 128, 128))
        painter.setPen(pen1)

        brush1 = QBrush(Qt.SolidPattern)
        brush1.setColor(QColor(212, 227, 242))
        painter.setBrush(brush1)

        painter.setRenderHint(QPainter.Antialiasing)  # 反锯齿
        painter.drawRoundedRect(self.boundingRect(), 10, 10)

    def mousePressEvent(self, evt):
        print('鼠标按下')
        if evt.button() == Qt.LeftButton:
            print("左键被按下")
        elif evt.button() == Qt.RightButton:
            print("左键被按下")
        elif evt.button() == Qt.MidButton:
            print("中间键被按下")

    def paintEvent(self, QPaintEvent):
        pen1 = QPen()
        pen1.setColor(QColor(166, 66, 250))
        painter = QPainter(self)
        painter.setPen(pen1)
        painter.begin(self)
        painter.drawRoundedRect(self.boundingRect(), 10, 10)  # 绘制函数
        painter.end()

class MyMainForm(QMainWindow, Ui_MainWindow):
    """
    主窗体
    """
    @classmethod
    def __new__(cls,*args):
        instance=super().__new__(cls)
        cls.instance=instance
        return instance

    def __init__(self, parent=None):
        super().__init__(parent)
        
        #加载插件
        self.extensions_manager=extensions_manager
        self.extensions_manager.load_setting()
        self.extensions_manager.load()

        self.setupUi(self)
        self.center()
        self.page_data.setup_ui()
        self.console_widget.setup_ui()

        self.page_data.bind_events(self)
        self.page_assess.bind_events(self)
        self.page_model.bind_events(self)
        self.page_plot.bind_events(self)
        self.page_stats.bind_events(self)

        init_actions(self)
        self.toolBar_right.bind_events(self)
        self.toolBar_left.bind_events(self)
        self.menubar.bind_events(self)
        self.menubar.translate()
        self.__file_path_choose = ""

        # 将原有的数据存储工具注释掉。方便之后查阅。
        # self.__all_dataset = dict()  # 定义字典，保存全部数据集的基本信息
        # self.__all_dataset_name = set()  # 定义集合，保存全部数据集名称，确保不会重复
        # 新的工具存储类。
        self.data_manager = DataManager()

        self.__current_dataset_name = ""
        self.__current_dataset = pd.DataFrame()
        self.__current_dataset_dtype = set()  # 定义集合，保存当前数据集中存在的数据类型，确保不会重复
        self.__result_path = ''  # 结果文件保存路径
        self.__setting = dict()  # 设置文件
        

        self.slot_flush_console('info', 'system', 'pyminer已准备就绪')

        # 任务栏图标设置
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setToolTip("pyminer数据分析")
        self.tray_icon.setIcon(QIcon(get_root_dir() + '/ui/source/icons/logo.png'))

        title_action = QAction("pyminer数据分析", self)
        show_action = QAction("显示", self)
        quit_action = QAction("退出", self)
        hide_action = QAction("隐藏", self)
        title_action.triggered.connect(self.main_help_display)
        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(qApp.quit)
        tray_menu = QMenu()
        tray_menu.addAction(title_action)
        tray_menu.addSeparator()
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

        self.action_minitray.triggered.connect(self.minitray_show)

        self.action_info.triggered.connect(self.info_show)
        self.action_success.triggered.connect(self.success_show)
        self.action_warning.triggered.connect(self.warning_show)
        self.action_error.triggered.connect(self.error_show)

        self.action_menu_data_merge_h.triggered.connect(self.data_merge_horizontal_display)
        self.action_menu_data_merge_v.triggered.connect(self.data_merge_vertical_display)

        self.treeView_files.bind_events(self)

        # 流程图
        self.rect = CustomRect()
        self.rect.setPos(50, 50)
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, 300, 300)
        self.scene.addItem(self.rect)
        self.tab_flow.graphicsView.setScene(self.scene)

        # self.btn_data_row_filter.setGraphicsEffect(self.eff) #特效测试。
        # 与page_data有关的全部事件，都移动到了ui.base.widgets.controlpanel的PMPageData类之中。

        # 打开"菜单-文件导入"窗口
        self.action_menu_import_file.triggered.connect(self.data_import_file_display)
        # 打开"菜单-打开"窗口
        self.action_menu_open.triggered.connect(self.main_open_data_chooseFile)

        # 打开"从数据库导入"窗口
        self.action_menu_database.triggered.connect(self.data_import_database_display)
        # 打开"新建"窗口
        self.action_menu_new.triggered.connect(self.main_new_display)
        # 打开"选项"窗口
        self.action_menu_option.triggered.connect(self.main_option_display)

        # 打开"关于"窗口
        self.action_about.triggered.connect(self.main_aboutme_display)
        # 打开"模型WOE"窗口
        self.action_menu_woe_iv.triggered.connect(self.model_woe_display)

        # 打开"数据-行筛选"窗口
        self.action_menu_data_row_filter.triggered.connect(self.data_row_filter_display)
        self.page_data.btn_data_row_filter.clicked.connect(self.data_row_filter_display)

        # "快速退出"
        self.action_menu_quick_exit.triggered.connect(qApp.quit)

        # 隐藏右侧工具栏
        self.action_hide_right.triggered.connect(self.right_widget_hide)

        # 更新主页面的显示数据
        self.action_data.triggered.connect(self.change_stacked_page)
        self.action_stats.triggered.connect(self.change_stacked_page)
        self.action_plot.triggered.connect(self.change_stacked_page)
        self.action_model.triggered.connect(self.change_stacked_page)
        self.action_assess.triggered.connect(self.change_stacked_page)
        self.action_ext.triggered.connect(self.change_stacked_page)

        self.action_menu_data_filter.triggered.connect(self.data_row_filter_display)

        # 排序数据
        self.action_menu_sort.triggered.connect(self.data_sort_display)

        self.action_menu_tree.triggered.connect(self.model_tree_display)  # 打开"模型-决策树"窗口

        self.action_menu_stat_describe.triggered.connect(self.stats_base_display)  # 显示“描述统计”窗口

        # 显示“官方网站”
        self.action_officesite.triggered.connect(self.main_officesite_display)
        # 显示“官方网站-帮助”
        self.action_help.triggered.connect(self.main_help_display)

        # 显示“Python包管理工具”
        self.action_package_manager.triggered.connect(self.package_manager_display)

        # 显示“Jupyter-notebook”
        self.action_jupyter_notebook.triggered.connect(self.jupyter_notebook_display)
        # self.action_ipython.triggered.connect(self.func_test)

        # self.action_menu_result.triggered.connect(self.send_signal)
        # self.action_menu_dataset.triggered.connect(self.accept_signal)
        # self.action_menu_dataset.triggered.connect(self.data_import_file_display)
        # self.accept_signal()

        # 隐藏工具栏、状态栏
        self.action_menu_toolbar.triggered.connect(self.menu_toolbar_hide)
        self.action_menu_statusbar.triggered.connect(self.menu_statusbar_hide)

        # 隐藏工作区间 任务列表
        self.action_menu_workdir.triggered.connect(self.menu_workdir_hide)
        self.action_menu_todolist.triggered.connect(self.menu_todolist_hide)

        # 隐藏工具窗口
        self.action_menu_toolbox.triggered.connect(self.right_widget_hide)

    #  ================================事件处理函数=========================
    def closeEvent(self, event):
        """
        退出时弹出确认消息提示
        """
        reply = QMessageBox.question(self, '注意', '确认退出吗？', QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Cancel)
        # 添加按钮，可用中文
        if reply == QMessageBox.Ok:
            event.accept()
            # os.system(r"taskkill /F /IM pyminer.exe")  # 结束进程
        else:
            event.ignore()

    def keyPressEvent(self, e):
        """
        按键盘Escape退出当前窗口
        """
        if e.key() == Qt.Key_Escape:
            self.close()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def minitray_show(self):
        self.hide()
        self.tray_icon.showMessage(
            "Tray Program",
            "Application was minimized to Tray",
            QSystemTrayIcon.Information,
            2000
        )

    def info_show(self):
        NotificationWindow.info('提示', '这是一条会自动关闭的消息')

    def success_show(self):
        NotificationWindow.success('提示', '这是一条会自动关闭的消息')

    def warning_show(self):
        NotificationWindow.warning('提示', '这是一条会自动关闭的消息')

    def error_show(self):
        NotificationWindow.error('提示',
                                 '<html><head/><body><p><span style=" font-style:italic; color:teal;">这是提示文案这是提示文案这是提示文案这是提示文案这是提示文案这是提示文案这是提示文案这是提示文案</span></p></body></html>')

    def menu_toolbar_hide(self):
        self.toolBar_left.setVisible(False) if self.toolBar_left.isVisible() else self.toolBar_left.setVisible(True)

    def menu_statusbar_hide(self):
        self.statusBar.setVisible(False) if self.statusBar.isVisible() else self.statusBar.setVisible(True)

    def menu_workdir_hide(self):
        if self.widget_left.isHidden():
            self.widget_left.setVisible(True)

        self.treeWidget_storehouse.setVisible(
            False) if self.treeWidget_storehouse.isVisible() else self.treeWidget_storehouse.setVisible(True)

        if self.treeWidget_storehouse.isHidden() and self.treeWidget_history.isHidden():
            self.widget_left.setVisible(False)

    def menu_todolist_hide(self):
        if self.widget_left.isHidden():
            self.widget_left.setVisible(True)

        self.treeWidget_history.setVisible(
            False) if self.treeWidget_history.isVisible() else self.treeWidget_history.setVisible(True)

        if self.treeWidget_storehouse.isHidden() and self.treeWidget_history.isHidden():
            self.widget_left.setVisible(False)

    def right_widget_hide(self):
        self.widget_right.setVisible(False) if self.widget_right.isVisible() else self.widget_right.setVisible(True)

    def test_report(self):
        print("查看测试报告")
        # data = pd.read_csv("c:/demo/uci.csv")
        # data_name = 'class.csv'
        # new = data.describe().T
        # pd.set_option('precision', 2)
        # self.slot_flush_report("info", "描述统计:Age", new, data_name, precision=2)

    #  ================================自定义功能函数=========================

    def openActionHandler(self):
        '''
        文件打开
        Returns:
        '''
        self.fileIndex = self.treeView_files.selectedIndexes()[0]
        #判断打开是否为文件夹
        self.checkDir = self.treeView_files.model.fileInfo(self.fileIndex).isDir()
        if self.checkDir:
            # 判断文件夹是否折叠
            if self.treeView_files.isExpanded(self.fileIndex):
                self.treeView_files.collapse(self.fileIndex)
            else:
                self.treeView_files.expand(self.fileIndex)
        else:
            self.filePath = self.treeView_files.model.filePath(self.fileIndex)
            try:
                win32api.ShellExecute(0, 'open', self.filePath, '', '', 1)
            except pywintypes.error:
                QMessageBox.information(self, '信息', '无法打开此文件，需在外部指定文件打开方式，解决方法暂未找到')


    def importActionHandler(self):
        '''
        文件导入
        Returns:
        '''
        self.fileIndex = self.treeView_files.selectedIndexes()[0]
        # 判断打开是否为文件夹
        self.checkDir = self.treeView_files.model.fileInfo(self.fileIndex).isDir()
        if self.checkDir:
            # 判断文件夹是否折叠
            if self.treeView_files.isExpanded(self.fileIndex):
                self.treeView_files.collapse(self.fileIndex)
            else:
                self.treeView_files.expand(self.fileIndex)
        else:
            self.importFilePath = self.treeView_files.model.filePath(self.fileIndex)
            if self.importFilePath.split('/')[-1].endswith(('xlsx', 'xls', 'xlsm')):
                self.import_excel_form = io.ImportExcelForm()
                self.import_excel_form.file_path_init(self.importFilePath)
                self.import_excel_form.signal_data_change.connect(self.slot_dataset_reload)  # 接收信号
                self.import_excel_form.exec_()
            elif self.importFilePath.split('/')[-1].endswith(('sav', 'zsav')):
                self.import_spss_form = io.ImportSpssForm()
                self.import_spss_form.file_path_init(self.importFilePath)
                self.import_spss_form.signal_data_change.connect(self.slot_dataset_reload)  # 接收信号
                self.import_spss_form.exec_()
            elif self.importFilePath.split('/')[-1].endswith(('sas7bdat')):
                self.import_sas_form = io.ImportSasForm()
                self.import_sas_form.file_path_init(self.importFilePath)
                self.import_sas_form.signal_data_change.connect(self.slot_dataset_reload)  # 接收信号
                self.import_sas_form.exec_()
            elif self.importFilePath.split('/')[-1].endswith(('txt', 'csv', 'tsv')):
                self.import_form = io.ImportForm()
                self.import_form.file_path_init(self.importFilePath)
                self.import_form.signal_data_change.connect(self.slot_dataset_reload)  # 接收信号
                self.import_form.exec_()
            else:
                QMessageBox.warning(self, '信息', '格式不满足', QMessageBox.Yes)


    def renameActionHandler(self):
        '''
        文件重命名
        Returns:
        '''
        self.fileIndex = self.treeView_files.selectedIndexes()[0]
        # 判断打开是否为文件夹
        self.checkDir = self.treeView_files.model.fileInfo(self.fileIndex).isDir()
        if self.checkDir:
            self.oldFloderPath = self.treeView_files.model.filePath(self.fileIndex)
            self.oldFloderPathList = self.oldFloderPath.split('/')
            self.newFloderName, confirmPressed = QInputDialog.getText(self, '文件夹重命名', '新的文件夹名称:', QLineEdit.Normal,
                                                                    self.oldFloderPathList[-1],
                                                                    flags=Qt.WindowCloseButtonHint)
            if confirmPressed and self.newFloderName != '':
                self.oldFloderPathList[-1] = self.newFloderName
                self.newFloderPath = '/'.join(self.oldFloderPathList)
                try:
                    os.rename(self.oldFloderPath, self.newFloderPath)
                except FileExistsError:
                    QMessageBox.warning(self, '警告', '当前路径已有同名文件夹,无法修改!')
            else:
                pass
        else:
            self.oldFilePath = self.treeView_files.model.filePath(self.fileIndex)
            self.oldFilePathList = self.oldFilePath.split('/')
            self.newFileName, confirmPressed = QInputDialog.getText(self, '文件重命名', '新的文件名:', QLineEdit.Normal,
                                                                    self.oldFilePathList[-1],
                                                                    flags=Qt.WindowCloseButtonHint)
            if confirmPressed and self.newFileName != '':
                self.oldFilePathList[-1] = self.newFileName
                self.newFilePath = '/'.join(self.oldFilePathList)
                try:
                    os.rename(self.oldFilePath, self.newFilePath)
                except FileExistsError:
                    QMessageBox.warning(self, '警告', '当前路径已有同名文件,无法修改!')
            else:
                pass


    def deleteActionHandler(self):
        '''
        文件or文件夹删除
        Returns:
        '''
        self.fileIndex = self.treeView_files.selectedIndexes()[0]
        # 判断打开是否为文件夹
        self.checkDir = self.treeView_files.model.fileInfo(self.fileIndex).isDir()
        if self.checkDir:
            self.floderPath = self.treeView_files.model.filePath(self.fileIndex)
            reply = QMessageBox.warning(self, '删除文件夹', '是否删除文件夹:' + self.floderPath.split('/')[-1],
                                        QMessageBox.Yes|QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                shutil.rmtree(self.floderPath)
            else:
                pass
        else:
            self.filePath = self.treeView_files.model.filePath(self.fileIndex)
            reply = QMessageBox.warning(self, '删除文件', '是否删除文件:' + self.filePath.split('/')[-1],
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                os.remove(self.filePath)
            else:
                pass


    def setting_check(self):
        setting_path = get_root_dir() + r'\settings.json'
        logging.info("配置文件加载完成，路径:{}".format(setting_path))
        if os.path.exists(setting_path):
            with open(setting_path, 'r', encoding='utf-8') as f:
                self.__setting = json.load(f)
        else:
            reply = QMessageBox.critical(self,
                                         'pyminer 出现错误',
                                         "在指定位置<br>" + setting_path + "<br>找不到配置文件",
                                         QMessageBox.Yes,
                                         QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                self.close()

    #  ================================自定义槽函数=========================
    def slot_dataset_reload(self, dataset_name, dataset, path, create_time, update_time, remarks, file_size):
        """
        :param dataset_name:数据集名称
        :param dataset: 数据集
        :param path: 数据文件路径
        :param create_time: 创建时间
        :param update_time: 更新时间
        :param remarks: 备注
        :param file_size: 文件大小
        :return: 刷新主窗体中当前显示的数据
        """
        print("开始更新数据")
        all_data = pd.DataFrame(dataset)
        self.alter_current_dataset(dataset_name, all_data, path, create_time, update_time, remarks, file_size)
        # 获取已经导入页面获取的数据集
        data = all_data.head(1000)  # 默认仅在主页加载前1000条数据
        self.tableWidget_dataset.setColumnCount(len(data.columns))
        self.tableWidget_dataset.setRowCount(len(data.index))
        self.tableWidget_dataset.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget_dataset.setHorizontalHeaderLabels(data.columns.values.tolist())

        for i in range(len(data.index)):
            for j in range(len(data.columns)):
                self.tableWidget_dataset.setItem(i, j, QTableWidgetItem(str(data.iat[i, j])))

        for x in range(self.tableWidget_dataset.columnCount()):
            headItem = self.tableWidget_dataset.horizontalHeaderItem(x)  # 获得水平方向表头的Item对象

            headItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        print("更新数据完成")

        # 添加数据集节点
        # 判断是否已经存在同名节点则先删除原节点，再进行添加，否则直接添加节点
        node_dataset = self.get_node_dataset()
        childCount = node_dataset.childCount()
        print("childCount:", childCount)
        if childCount > 0:
            if_exists = 0
            for i in range(childCount):
                txt = node_dataset.child(i).text(0)
                print("txt:", txt)
                if txt == dataset_name:
                    if_exists = 1
            if if_exists == 1:
                print("同名节点已存在，无需添加节点")
            else:
                child_dataset = QTreeWidgetItem(node_dataset)
                child_dataset.setText(0, dataset_name)
                child_dataset.setIcon(0, QIcon(get_root_dir() + '/ui/source/images/sc_viewdatasourcebrowser.png'))
                print("添加节点完成")
        else:
            child_dataset = QTreeWidgetItem(node_dataset)
            child_dataset.setText(0, dataset_name)
            child_dataset.setIcon(0, QIcon(get_root_dir() + '/ui/source/images/sc_viewdatasourcebrowser.png'))
            print("添加节点完成")

    def slot_result_reload(self, result_name, result_path):
        self.__result_path = result_path
        self.inner_browser_display()

        # 添加结果节点
        node_result = self.treeWidget_storehouse.topLevelItem(6)
        child_model = QTreeWidgetItem(node_result)
        child_model.setText(0, result_name)
        child_model.setIcon(0, QIcon(get_root_dir() + '/ui/source/images/lc_optimizetable.png'))
        print("添加节点完成")

    def slot_flush_console(self, level, module, content):
        """
        刷新主窗体执行情况日志
        :return:
        level:文本，warnning error info
        module:业务模块名称，例如 数据获取，数据处理，数据探索，统计，模型，可视化，评估
        """
        create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 日志记录时间
        user = getpass.getuser()
        msg = create_time + ' ' + user + ' ' + level.upper() + ' [' + module + ']' + ':' + content
        if level == "error":
            html = "<a style='font-family:verdana;color:red;font-size:11;'>" + msg + "</a>"
        else:
            html = "<a style='font-family:verdana;color:black;font-size:11;'>" + msg + "</a>"

        console = self.textEdit_console  # 由于代码重构，这里出现了不同。
        # [!TODO]应当创建方法，一次性的完成这个工作。
        console.moveCursor(QTextCursor.End)
        console.append(html)

    def slot_flush_result(self, dataset):
        pass

    def slot_flush_report(self, header_1, header_2, dataset, dataset_name, index=True, precision=-1):
        """
        :param header_1: 主标题，例如 描述性统计量: Age
        :param header_2:副标题，例如 统计量
        :param dataset:数据集
        :param dataset_name:数据集名称
        :param index:数据集是否包含指定索引
        :param precision:显示精度，-1表示自动设置，否则为指定精度
        :return:html
        """
        template = open(get_root_dir() + r"\template\report.html", 'r', encoding='utf-8').read()

        # 根据原始数据是否包含列名，分别处理html
        if index:  # 包含索引
            th = "<th>变量</th>"  # 标题行新增索引名
            for c in dataset.columns:
                col = "<th>" + c + "</th>"
                th = th + col

            td = str()
            for r in range(dataset.shape[0]):  # 行
                grid = str()
                grid_index = "<td>" + str(dataset.index[r]) + "</td>"
                for c in range(dataset.shape[1]):  # 列
                    if precision == -1:
                        grid = grid + "<td>" + str(dataset.iat[r, c]) + "</td>"
                    else:
                        prec = r"{:,." + str(precision) + "f}"
                        grid = grid + "<td>" + prec.format(dataset.iat[r, c]) + "</td>"
                row = "<tr>" + grid_index + grid + "</tr>"
                td = td + row
        else:  # 标题行不指定索引名
            th = str()
            for col in dataset.columns:
                row = "<th>" + col + "</th>"
                th = th + row
            td = str()
            for r in range(dataset.shape[0]):  # 行
                grid = str()
                for c in range(dataset.shape[1]):  # 列
                    if precision == -1:
                        grid = grid + "<td>" + str(dataset.iat[r, c]) + "</td>"
                    else:
                        prec = r"{:,." + str(precision) + "f}"
                        grid = grid + "<td>" + prec.format(dataset.iat[r, c]) + "</td>"
                row = "<tr>" + grid + "</tr>"
                td = td + row

        # 生成新报告内容
        html_report = template.replace("$header_1$", header_1)
        html_report = html_report.replace("$header_2$", header_2)
        html_report = html_report.replace("$dataset_name$", dataset_name)
        html_report = html_report.replace("$th$", th)
        html_report = html_report.replace("$td$", td)
        output_dir = './'
        with open(output_dir + r'\report_' + str(time.time()).split('.')[0] + '.html', 'w', encoding='utf-8') as file:
            file.write(html_report)
        print("报告输出成功")
        print("报告地址：", output_dir + r'\report_' + str(time.time()).split('.')[0] + '.html')

    def on_treeWidget_storehouse_customContextMenuRequested(self, pos):  # 右键快捷菜单
        root_dir = get_root_dir()
        item = self.treeWidget_storehouse.currentItem().text(0)

        self.__treeWidget_storehouse_node_parent = ""
        if item not in ("数据集", "数据处理", "统计", "可视化", "模型", "评估", "结果"):
            self.__treeWidget_storehouse_node_parent = self.treeWidget_storehouse.currentItem().parent().text(0)

        # 数据集右键菜单
        menuList = QMenu(self)  # 创建菜单
        if item == "数据集" or self.__treeWidget_storehouse_node_parent == "数据集":
            menuList.addAction(QAction(QIcon(root_dir + '/ui/source/images/dbqueryedit.png'), '打开', self,
                                       triggered=self.main_open_data))
            menuList.addAction(QAction(QIcon(root_dir + '/ui/source/images/dbqueryedit.png'), '导入数据集', self,
                                       triggered=self.main_open_data_chooseFile))
            menuList.addAction(
                QAction(QIcon(root_dir + '/ui/source/images/formfilternavigator.png'), '筛选', self,
                        triggered=self.main_open_data_chooseFile))
            menuList.addAction(QAction(QIcon(root_dir + '/ui/source/images/lc_sortascending.png'), '排序', self,
                                       triggered=self.main_open_data_chooseFile))

            menuList.addAction(QAction(QIcon(root_dir + '/ui/source/images/lc_renametable.png'), '重命名', self,
                                       triggered=self.stats_base_display))
            menuList.addAction(QAction(QIcon('./ui/source/images/lc_deletepage.png'), '删除', self,
                                       triggered=self.stats_base_display))
        elif item == "数据处理" or self.__treeWidget_storehouse_node_parent == "数据处理":
            menuList.addAction(QAction(QIcon(root_dir + '/ui/source/images/dbviewtables.png'), '新建数据处理', self,
                                       triggered=self.stats_base_display))
            menuList.addAction(QAction(QIcon(root_dir + '/ui/source/images/lc_renametable.png'), '重命名', self,
                                       triggered=self.stats_base_display))
            menuList.addAction(QAction(QIcon(root_dir + '/ui/source/images/lc_deletepage.png'), '删除', self,
                                       triggered=self.stats_base_display))
        elif item == "统计" or self.__treeWidget_storehouse_node_parent == "统计":
            menuList.addAction(QAction(QIcon(root_dir + '/ui/source/images/lc_autosum.png'), '新建描述统计', self,
                                       triggered=self.stats_base_display))
            menuList.addAction(QAction(QIcon(root_dir + '/ui/source/images/lc_renametable.png'), '重命名', self,
                                       triggered=self.stats_base_display))
            menuList.addAction(QAction(QIcon(root_dir + '/ui/source/images/lc_deletepage.png'), '删除', self,
                                       triggered=self.stats_base_display))
        elif item == "可视化" or self.__treeWidget_storehouse_node_parent == "可视化":
            menuList.addAction(QAction(QIcon(root_dir + '/ui/source/images/lc_drawchart.png'), '新建可视化', self,
                                       triggered=self.plot_frame_display))
            menuList.addAction(QAction(QIcon(root_dir + '/ui/source/images/lc_renametable.png'), '重命名', self,
                                       triggered=self.stats_base_display))
            menuList.addAction(QAction(QIcon(root_dir + '/ui/source/images/lc_deletepage.png'), '删除', self,
                                       triggered=self.stats_base_display))
        elif item == "模型" or self.__treeWidget_storehouse_node_parent == "模型":
            menuList.addAction(
                QAction(QIcon(root_dir + '/ui/source/images/lc_switchcontroldesignmode.png'), '新建模型', self,
                        triggered=self.model_frame_display))
            menuList.addAction(QAction(QIcon(root_dir + '/ui/source/images/lc_renametable.png'), '重命名', self,
                                       triggered=self.stats_base_display))
            menuList.addAction(QAction(QIcon(root_dir + '/ui/source/images/lc_deletepage.png'), '删除', self,
                                       triggered=self.stats_base_display))
        elif item == "评估" or self.__treeWidget_storehouse_node_parent == "评估":
            menuList.addAction(QAction(QIcon(root_dir + '/ui/source/images/lc_rotateleft.png'), '新建评估', self,
                                       triggered=self.model_frame_display))
            menuList.addAction(QAction(QIcon(root_dir + '/ui/source/images/lc_renametable.png'), '重命名', self,
                                       triggered=self.stats_base_display))
            menuList.addAction(QAction(QIcon(root_dir + '/ui/source/images/lc_deletepage.png'), '删除', self,
                                       triggered=self.stats_base_display))

        elif item == "结果" or self.__treeWidget_storehouse_node_parent == "结果":
            menuList.addAction(QAction(QIcon(root_dir + '/ui/source/images/lc_optimizetable.png'), '导出结果', self,
                                       triggered=self.model_frame_display))
            menuList.addAction(QAction(QIcon(root_dir + '/ui/source/images/lc_renametable.png'), '重命名', self,
                                       triggered=self.stats_base_display))
            menuList.addAction(QAction(QIcon(root_dir + '/ui/source/images/lc_deletepage.png'), '删除', self,
                                       triggered=self.stats_base_display))

        menuList.exec(QCursor.pos())  # 显示菜单

    def on_treeWidget_customContextMenuRequested(self, pos):  ##右键快捷菜单
        menuList = QMenu(self)

        self.stackedWidget.setCurrentIndex(4)

    def load_data(self, sp):
        for i in range(1, 2):  # 模拟主程序加载过程
            time.sleep(1)  # 加载数据
            sp.showMessage("加载... {0}%".format(i * 30), Qt.AlignHCenter | Qt.AlignBottom, Qt.black)
            qApp.processEvents()  # 允许主进程处理事件

    def main_officesite_display(self):
        """
        打开官方网站页面
        """
        try:
            webbrowser.get('chrome').open_new_tab("http://www.py2cn.com/")
        except Exception as e:
            webbrowser.open_new_tab("http://www.py2cn.com/")

    def main_help_display(self):
        """
        打开帮助页面
        """
        try:
            webbrowser.get('chrome').open_new_tab("http://www.py2cn.com")
        except Exception as e:
            webbrowser.open_new_tab("http://www.py2cn.com")

    def main_dataset_change(self):
        # 重新加载当前数据集到主页面

        try:
            self.main_data_reload()

        except:
            pass

    def main_data_reload(self):
        # 获取已经导入页面获取的数据集
        data = self.__current_dataset.head(1000)  # 默认仅在主页加载前1000条数据
        self.tableWidget_dataset.setColumnCount(len(data.columns))
        self.tableWidget_dataset.setRowCount(len(data.index))
        self.tableWidget_dataset.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget_dataset.setHorizontalHeaderLabels(data.columns.values.tolist())

        for i in range(len(data.index)):
            for j in range(len(data.columns)):
                self.tableWidget_dataset.setItem(i, j, QTableWidgetItem(str(data.iat[i, j])))

        for x in range(self.tableWidget_dataset.columnCount()):
            headItem = self.tableWidget_dataset.horizontalHeaderItem(x)  # 获得水平方向表头的Item对象

            headItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

    def main_result_display(self):
        """
        显示"结果"窗口
        """
        print('test')

    def main_option_display(self):
        """
        显示"选项"窗口
        """
        self.optionForm = OptionForm()
        self.optionForm.show()

    def main_new_display(self):
        """
        显示"新建"窗口
        """
        self.new_item = NewItemForm()
        self.new_item.show()

    def main_aboutme_display(self):
        """
        显示"关于"窗口
        """
        self.aboutme = AboutMeForm()
        self.aboutme.show()

    def main_open_data(self):
        """
                :param dataset_name:数据集名称
                :param dataset: 数据集
                :return: 刷新主窗体中当前显示的数据
                """
        print("开始更新数据")
        node_name = self.treeWidget_storehouse.currentItem().text(0)
        print(node_name)
        all_data = pd.DataFrame(self.__all_dataset.get(node_name))  # 获取当前数据
        self.__current_dataset_name = node_name  # 修改当前数据名称
        # 获取已经导入页面获取的数据集
        data = all_data.head(1000)  # 默认仅在主页加载前1000条数据
        self.tableWidget_dataset.setColumnCount(len(data.columns))
        self.tableWidget_dataset.setRowCount(len(data.index))
        self.tableWidget_dataset.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget_dataset.setHorizontalHeaderLabels(data.columns.values.tolist())

        for i in range(len(data.index)):
            for j in range(len(data.columns)):
                self.tableWidget_dataset.setItem(i, j, QTableWidgetItem(str(data.iat[i, j])))

        for x in range(self.tableWidget_dataset.columnCount()):
            headItem = self.tableWidget_dataset.horizontalHeaderItem(x)  # 获得水平方向表头的Item对象

            headItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        print("更新数据完成")

    def main_open_data_chooseFile(self):

        self.__file_path_choose, filetype = QFileDialog.getOpenFileName(self,
                                                                        '选择文件', '', "All Files (*);;\
                                                                文本文件 (*.txt *.csv *.tsv);;\
                                                                EXCEL文件 (*.xls *.xlsx *.xlsm *.xltx *.xltm);;\
                                                                SPSS文件 (*.sav *.zsav);;\
                                                                SAS文件 (*.sas7bdat)")  # 设置文件扩展名过滤,用双分号间隔

        if self.__file_path_choose == "":
            logging.info("\n取消选择")
            return

        if os.path.split(self.__file_path_choose)[1].endswith(('xlsx', 'xlsm', 'xltx', 'xltm')):
            if len(self.__file_path_choose) > 0:
                self.import_excel_form = io.ImportExcelForm()
                self.import_excel_form.file_path_init(self.__file_path_choose)
                self.import_excel_form.signal_data_change.connect(self.slot_dataset_reload)  # 接收信号
                self.import_excel_form.exec_()
            else:
                logging.info("信号发射失败--导入文件已选择")

        elif os.path.split(self.__file_path_choose)[1].endswith(('sav', 'zsav')):
            if len(self.__file_path_choose) > 0:
                self.import_spss_form = io.ImportSpssForm()
                self.import_spss_form.file_path_init(self.__file_path_choose)
                self.import_spss_form.signal_data_change.connect(self.slot_dataset_reload)  # 接收信号
                self.import_spss_form.exec_()
            else:
                logging.info("信号发射失败")


        elif os.path.split(self.__file_path_choose)[1].endswith(('sas7bdat')):
            if len(self.__file_path_choose) > 0:
                self.import_sas_form = io.ImportSasForm()
                self.import_sas_form.file_path_init(self.__file_path_choose)
                self.import_sas_form.signal_data_change.connect(self.slot_dataset_reload)  # 接收信号
                self.import_sas_form.exec_()
            else:
                logging.info("信号发射失败")

        else:
            if len(self.__file_path_choose) > 0:
                self.import_form = io.ImportForm()
                self.import_form.file_path_init()
                self.import_form.signal_data_change.connect(self.slot_dataset_reload)  # 接收信号
                self.import_form.exec_()
            else:
                logging.info("信号发射失败")

    def change_stacked_page(self):
        """
        显示或隐藏右侧工具栏
        """
        widget = getattr(self, self.sender().objectName().replace('action', 'page'), None)
        print(widget)
        if widget:
            cur_widget = self.stackedWidget.currentWidget()
            if widget == cur_widget:
                self.widget_right.setVisible(not self.widget_right.isVisible())
            else:
                self.widget_right.setVisible(True)
                self.stackedWidget.setCurrentWidget(widget)

    def get_node_dataset(self):
        return self.treeWidget_storehouse.topLevelItem(0)

    def alter_current_dataset(self, dataset_name, dataset, path='',
                              create_time='', update_time='', remarks='',
                              file_size=''):
        # 修改当前正在使用的数据集
        self.__current_dataset = dataset
        self.__current_dataset_name = dataset_name
        self.data_manager.set_data(self.__current_dataset_name,dataset)
        row = str(dataset.shape[0])  # 行数
        col = str(dataset.shape[1])  # 列数
        memory_size = self.__current_dataset.memory_usage().sum()
        # 内存大小
        if memory_size < 1024:
            memory_usage = str(memory_size) + ' bytes'
        elif (memory_size / 1024) < 1024:
            memory_usage = str(round(memory_size / 1024, 2)) + ' KB'
        elif (memory_size / 1024 / 1024) < 1024:
            memory_usage = str(round(memory_size / 1024 / 1024, 2)) + ' M'
        elif (memory_size / 1024 / 1024) >= 1024:
            memory_usage = str(round(memory_size / 1024 / 1024 / 1024, 2)) + ' G'

        # 文件大小
        if file_size.isdigit():
            if int(file_size) < 1024:
                file_usage = str(file_size) + ' bytes'
            elif (int(file_size) / 1024) < 1024:
                file_usage = str(round(int(file_size) / 1024, 2)) + ' KB'
            elif (int(file_size) / 1024 / 1024) < 1024:
                file_usage = str(round(int(file_size) / 1024 / 1024, 2)) + ' M'
            elif (int(file_size) / 1024 / 1024) >= 1024:
                file_usage = str(round(int(file_size) / 1024 / 1024 / 1024, 2)) + ' G'
        else:
            file_usage = file_size

        # 描述信息，包含变量名、数据类型、非空数量
        data_type = []
        data_notna_cnt = []
        for i in dataset.columns:
            data_type.append(str(dataset.loc[:, i].dtype))
            data_notna_cnt.append(dataset.loc[:, i].notna().sum())
        info = pd.DataFrame({"变量名称": list(dataset.columns), "数据类型": data_type, "非空值数量": data_notna_cnt})

        # dataset_new = {dataset_name: dataset,
        #                dataset_name + ".path": path,
        #                dataset_name + ".create_time": create_time,
        #                dataset_name + ".update_time": update_time,
        #                dataset_name + ".row": row,
        #                dataset_name + ".col": col,
        #                dataset_name + ".remarks": remarks,
        #                dataset_name + ".file_size": file_usage,
        #                dataset_name + ".memory_usage": memory_usage,
        #                dataset_name + ".info": info, }

        # 添加当前数据集到数据集列表中
        print("添加当前数据集到数据集列表中")
        # 检查数据集名称是否已存在，如果存在则修改相关信息，否则进行新增
        self.data_manager.set_info(dataset_name, path, create_time=create_time, update_time=update_time, row=row,
                                   col=col, remarks=remarks, file_size=file_usage, memory_usage=memory_usage, info=info)

        self.tabWidget.setCurrentIndex(0)

    def add_dataset_to_workdir(self, dataset_name):
        child_dataset = QTreeWidgetItem()
        child_dataset.setText(0, dataset_name)
        child_dataset.setIcon(0, QIcon(get_root_dir() + '/ui/source/images/sc_viewdatasourcebrowser.png'))
        return child_dataset

    def data_import_file_display(self):
        """
        显示导入文件窗口，当数据改变时，刷新主窗体中当前显示的数据
        """
        self.import_form = io.ImportForm()
        self.import_form.signal_data_change.connect(self.slot_dataset_reload)
        self.import_form.exec_()

    def data_import_file_test(self, csv_path: str):
        '''
        这是一个测试时使用的方法。当调用时，可以直接打开数据。当界面崩溃之后，可以尽可能快速的启动。
        '''
        create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 数据创建时间
        update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 数据更新时间
        path = csv_path
        print("path:", path)
        file_size = str(os.path.getsize(path))
        print("file_size:", file_size)
        remarks = ''
        current_dataset = pd.read_csv(path, engine="python",
                                      encoding='utf8')
        current_dataset_name = 'test_file'
        tmpargs = (current_dataset_name, current_dataset.to_dict(), path,
                   create_time, update_time, remarks, file_size)  # 发射信号
        logging.info("导入数据信号已发射")
        self.slot_dataset_reload(*tmpargs)

    def data_import_database_display(self):
        """
        显示"从数据库导入"窗口
        """
        self.import_database = io.ImportDatabase()
        self.import_database.data_manager = self.data_manager
        self.import_database.signal_data_change.connect(self.slot_dataset_reload)
        self.import_database.show()

    def data_row_filter_display(self):
        """
        显示"数据-行筛选"窗口
        """
        self.data_row_filter_form = DataRowFilterForm()
        self.data_row_filter_form.unset_effect_signal.connect(self.page_data.btn_data_info.unset_btn_clicked_effect)

        self.data_row_filter_form.current_dataset = self.__current_dataset
        self.data_row_filter_form.current_dataset_name = self.__current_dataset_name
        self.data_row_filter_form.data_manager = self.data_manager
        self.data_row_filter_form.current_dataset_columns = self.__current_dataset.columns
        self.data_row_filter_form.comboBox_columns.addItems(list(self.__current_dataset.columns))
        for col in self.__current_dataset.columns:
            self.__current_dataset_dtype.add(str(self.__current_dataset.loc[:, col].dtype))
        self.data_row_filter_form.comboBox_dtype.addItems(list(self.__current_dataset_dtype))
        self.data_row_filter_form.dataset_init()  # 初始化预览数据
        self.data_row_filter_form.signal_data_change.connect(self.slot_dataset_reload)
        self.data_row_filter_form.exec_()

    def data_info_display(self):
        """
        显示"数据信息"窗口
        """
        self.data_info = DataInfoForm()
        self.data_info.unset_effect_signal.connect(self.page_data.btn_data_info.unset_btn_clicked_effect)

        self.data_info.data_manager = self.data_manager
        self.data_info.all_dataset_name = list(self.data_manager.all_data_names)
        self.data_info.current_dataset_name = self.__current_dataset_name
        self.data_info.lineEdit_dataset_name.setText(self.__current_dataset_name)
        property_dic = self.data_manager.get_info(self.__current_dataset_name)
        self.data_info.lineEdit_path.setText(property_dic.get("path"))
        self.data_info.lineEdit_row.setText(property_dic.get("row"))
        self.data_info.lineEdit_col.setText(property_dic.get("col"))
        self.data_info.lineEdit_file_size.setText(property_dic.get("file_size"))
        self.data_info.lineEdit_memory_usage.setText(property_dic.get("memory_usage"))
        self.data_info.lineEdit_create_time.setText(property_dic.get("create_time"))
        self.data_info.lineEdit_update_time.setText(property_dic.get("update_time"))
        self.data_info.info = property_dic.get('info')
        self.data_info.info_init()
        self.data_info.exec_()

    def data_filter_display(self):
        """
        显示"数据筛选"窗口
        """
        self.data_filter = DataFilterForm()
        self.data_filter.unset_effect_signal.connect(self.page_data.btn_data_info.unset_btn_clicked_effect)

        self.data_filter.show()

    def data_role_display(self):
        """
        显示"数据-数据角色"窗口
        """
        self.data_role = DataRoleForm()
        self.data_role.unset_effect_signal.connect(self.page_data.btn_data_info.unset_btn_clicked_effect)

        self.data_role.current_dataset = self.__current_dataset.copy()
        self.data_role.all_dataset = self.__all_dataset
        self.data_role.current_dataset_name = self.__current_dataset_name
        self.data_role.current_dataset_columns = self.__current_dataset.columns
        self.data_role.comboBox_columns.addItems(list(self.__current_dataset.columns))
        self.data_role.signal_data_change.connect(self.slot_dataset_reload)
        self.data_role.dataset_role()  # 初始化预览数据
        self.data_role.exec_()

    def data_merge_vertical_display(self):
        """
        显示"数据-纵向合并"窗口
        """
        self.data_merge_vertical = DataMergeVerticalForm()
        self.data_merge_vertical.unset_effect_signal.connect(self.page_data.btn_data_info.unset_btn_clicked_effect)

        self.data_merge_vertical.listWidget_dataset.addItems(list(self.__all_dataset_name))
        self.data_merge_vertical.all_dataset = self.__all_dataset
        self.data_merge_vertical.all_dataset_name = self.__all_dataset_name
        self.data_merge_vertical.listWidget_start.addItem(self.__current_dataset_name)
        self.data_merge_vertical.current_dataset_name = self.__current_dataset_name
        self.data_merge_vertical.signal_data_change.connect(self.slot_dataset_reload)
        self.data_merge_vertical.exec_()

    def data_merge_horizontal_display(self):
        """
        显示"数据-横向合并"窗口
        """
        self.data_merge_horizontal = DataMergeHorizontalForm()
        self.data_merge_horizontal.unset_effect_signal.connect(self.page_data.btn_data_info.unset_btn_clicked_effect)

        self.data_merge_horizontal.listWidget_dataset.addItems(list(self.__all_dataset_name))
        self.data_merge_horizontal.all_dataset = self.__all_dataset
        self.data_merge_horizontal.all_dataset_name = self.__all_dataset_name
        self.data_merge_horizontal.listWidget_start.addItem(self.__current_dataset_name)
        self.data_merge_horizontal.current_dataset_name = self.__current_dataset_name
        self.data_merge_horizontal.signal_data_change.connect(self.slot_dataset_reload)
        self.data_merge_horizontal.exec_()

    def data_partition_display(self):
        """
        显示"数据-数据分区"窗口
        """
        self.data_partition = DataPartitionForm()
        self.data_partition.unset_effect_signal.connect(self.page_data.btn_data_info.unset_btn_clicked_effect)
        if any(self.__current_dataset):
            self.data_partition.current_dataset = self.__current_dataset
            self.data_partition.current_dataset_name = self.__current_dataset_name
            self.data_partition.lineEdit_dataset_name.setText(self.__current_dataset_name)
            self.data_partition.signal_data_change.connect(self.slot_dataset_reload)

        self.data_partition.exec_()

    def data_new_column_display(self):
        """
        显示"数据-增加列"窗口
        """
        self.data_new_column = DataNewColumnForm()
        self.data_new_column.unset_effect_signal.connect(self.page_data.btn_data_info.unset_btn_clicked_effect)

        self.data_new_column.show()

    def data_missing_value_display(self):
        """
        显示"数据-缺失值"窗口
        """
        self.data_missing_value = DataMissingValueForm()
        self.data_missing_value.unset_effect_signal.connect(self.page_data.btn_data_info.unset_btn_clicked_effect)

        self.data_missing_value.current_dataset = self.__current_dataset
        self.data_missing_value.all_dataset = self.__all_dataset
        self.data_missing_value.current_dataset_name = self.__current_dataset_name
        self.data_missing_value.current_dataset_columns = self.__current_dataset.columns
        self.data_missing_value.listWidget_var.addItems(list(self.__current_dataset.columns))
        self.data_missing_value.listWidget_selected.addItems(list(self.__current_dataset.columns))
        self.data_missing_value.signal_data_change.connect(self.slot_dataset_reload)
        self.data_missing_value.dataset_missing_stat()  # 初始化缺失值统计
        self.data_missing_value.exec_()

    def data_sort_display(self):
        """
        显示"数据-数据排序"窗口
        """
        self.data_sort = DataSortForm()
        self.data_sort.unset_effect_signal.connect(self.page_data.btn_data_info.unset_btn_clicked_effect)

        self.data_sort.show()

    def data_transpose_display(self):
        """
        显示"数据-转置"窗口
        """
        self.data_transpose = DataTransposeForm()
        self.data_transpose.unset_effect_signal.connect(self.page_data.btn_data_info.unset_btn_clicked_effect)

        self.data_transpose.current_dataset = self.__current_dataset
        self.data_transpose.current_dataset_name = self.__current_dataset_name
        self.data_transpose.current_dataset_columns = self.__current_dataset.columns
        self.data_transpose.listWidget_var.addItems(list(self.__current_dataset.columns))
        self.data_transpose.listWidget_selected.addItems(list(self.__current_dataset.columns))
        self.data_transpose.signal_data_change.connect(self.slot_dataset_reload)
        self.data_transpose.exec_()

    def data_standard_display(self):
        """
        显示"数据-标准化"窗口
        """
        self.data_standard = DataStandardForm()
        self.data_standard.unset_effect_signal.connect(self.page_data.btn_data_info.unset_btn_clicked_effect)

        self.data_standard.show()

    def data_column_name_display(self):
        """
        显示"数据-列名处理"窗口
        """
        self.data_column_name = DataColumnNameForm()
        self.data_column_name.unset_effect_signal.connect(self.page_data.btn_data_info.unset_btn_clicked_effect)

        self.data_column_name.current_dataset = self.__current_dataset
        self.data_column_name.dataset_edit = self.__current_dataset
        self.data_column_name.all_dataset = self.__all_dataset
        self.data_column_name.current_dataset_name = self.__current_dataset_name
        self.data_column_name.current_dataset_columns = self.__current_dataset.columns
        self.data_column_name.listWidget_var.addItems(list(self.__current_dataset.columns))
        self.data_column_name.listWidget_selected.addItems(list(self.__current_dataset.columns))
        self.data_column_name.comboBox_columns.addItems(list(self.__current_dataset.columns))
        self.data_column_name.signal_data_change.connect(self.slot_dataset_reload)
        self.data_column_name.signal_flush_console.connect(self.slot_flush_console)
        self.data_column_name.dataset_init()  # 初始化预览数据
        self.data_column_name.exec_()

    def data_column_encode_display(self):
        """
        显示"数据-数据编码"窗口
        """
        self.data_column_encode = DataColumnEncodeForm()
        self.data_column_encode.unset_effect_signal.connect(self.page_data.btn_data_info.unset_btn_clicked_effect)

        self.data_column_encode.show()

    def data_replace_display(self):
        """
        显示"数据-内容替换"窗口
        """
        self.data_replace = DataReplaceForm()
        self.data_replace.unset_effect_signal.connect(self.page_data.btn_data_info.unset_btn_clicked_effect)

        self.data_replace.current_dataset = self.__current_dataset
        self.data_replace.data_manager = self.data_manager
        self.data_replace.current_dataset_name = self.__current_dataset_name
        self.data_replace.current_dataset_columns = self.__current_dataset.columns
        self.data_replace.comboBox_find_columns.addItems(list(self.__current_dataset.columns))
        self.data_replace.comboBox_replace_columns.addItems(list(self.__current_dataset.columns))
        self.data_replace.signal_data_change.connect(self.slot_dataset_reload)
        self.data_replace.signal_flush_console.connect(self.slot_flush_console)

        self.data_replace.show()

    def data_sample_display(self):
        """
        显示"数据-抽样"窗口
        """
        self.data_simple = DataSampleForm()
        self.data_simple.unset_effect_signal.connect(self.page_data.btn_data_info.unset_btn_clicked_effect)

        self.data_simple.current_dataset = self.__current_dataset
        self.data_simple.dataset_edit = self.__current_dataset
        self.data_simple.current_dataset_name = self.__current_dataset_name
        self.data_simple.current_dataset_columns = self.__current_dataset.columns
        self.data_simple.lineEdit_dataset_name.setText(self.__current_dataset_name)
        self.data_simple.listWidget_var.addItems(list(self.__current_dataset.columns))
        self.data_simple.listWidget_selected.addItems(list(self.__current_dataset.columns))
        self.data_simple.signal_data_change.connect(self.slot_dataset_reload)
        self.data_simple.exec_()

    def data_column_desc_display(self):
        """
        显示"数据-列描述"窗口
        """
        self.data_column_desc = DataColumnDescForm()
        self.data_column_desc.unset_effect_signal.connect(self.page_data.btn_data_info.unset_btn_clicked_effect)

        self.data_column_desc.current_dataset = self.__current_dataset
        if any(self.__current_dataset):
            self.data_column_desc.current_dataset_name = self.__current_dataset_name
            self.data_column_desc.all_dataset = self.__all_dataset
            self.data_column_desc.listWidget_var.addItems(self.__current_dataset.columns)
            self.data_column_desc.listWidget_selected.addItem(self.__current_dataset.columns[0])
            self.data_column_desc.listWidget_group.addItem(self.__current_dataset.columns[0])
            self.data_column_desc.signal_data_change.connect(self.slot_dataset_reload)
        self.data_column_desc.exec_()

    def data_delete_row_display(self):
        """
        显示"数据-删除行"窗口
        """
        self.data_delete_row = DataDeleteRowForm()
        self.data_delete_row.unset_effect_signal.connect(self.page_data.btn_data_info.unset_btn_clicked_effect)

        self.data_delete_row.show()

    def data_delete_col_display(self):
        """
        显示"数据-删除列"窗口
        """
        self.data_delete_column = DataDeleteColumnForm()
        self.data_delete_column.unset_effect_signal.connect(self.page_data.btn_data_info.unset_btn_clicked_effect)

        self.data_delete_column.show()

    def model_woe_display(self):
        """
        显示"模型-WOE"窗口
        """
        output_dir = r'./'
        self.model_woe_form = model.ModelWoeForm()
        self.model_woe_form.current_dataset = self.__current_dataset
        self.model_woe_form.all_dataset = self.__all_dataset
        self.model_woe_form.current_dataset_name = self.__current_dataset_name
        self.model_woe_form.current_dataset_columns = self.__current_dataset.columns
        self.model_woe_form.lineEdit_dataset_name.setText(self.__current_dataset_name)
        self.model_woe_form.lineEdit_output_path.setText(output_dir)
        self.model_woe_form.listWidget_var.addItems(list(self.__current_dataset.columns))
        self.model_woe_form.listWidget_var.addItems(list(self.__current_dataset.columns))
        # 自动添加目标变量
        for var in self.__current_dataset.columns:
            if var.lower() in ("y", "target"):
                self.model_woe_form.listWidget_dependent.addItem(var)
            else:
                self.model_woe_form.listWidget_independent.addItem(var)

        # self.model_woe_form.signal_data_change.connect(self.slot_dataset_reload)

        self.model_woe_form.exec_()

    def model_tree_display(self):
        """
        显示"模型-决策树"窗口
        """
        self.model_tree_form = model.ModelTreeForm()
        self.model_tree_form.current_dataset = self.__current_dataset
        self.model_tree_form.current_dataset_columns = self.__current_dataset.columns
        self.model_tree_form.lineEdit_dataset_name.setText(self.__current_dataset_name)
        self.model_tree_form.listWidget_var.addItems(list(self.__current_dataset.columns))
        # 自动添加目标变量
        for var in self.__current_dataset.columns:
            if var.lower() in ("y", "target"):
                self.model_tree_form.listWidget_dependent.addItem(var)
            else:
                self.model_woe_form.listWidget_independent.addItem(var)

        # self.model_tree_form.signal_result.connect(self.slot_result_reload)  # 重新加载输出结果
        self.model_tree_form.exec_()

    def model_frame_display(self):
        """
        显示"模型-框架"窗口
        """
        self.model_frame = model.ModelFrameForm()
        self.model_frame.show()

    def plot_frame_display(self):
        """
        显示"可视化-框架"窗口
        """
        self.plot_frame = plot.PlotForm()
        self.plot_frame.exec_()

    def stats_base_display(self):
        """
        显示"统计-描述统计"窗口
        """
        self.stats_base = StatsBaseForm()
        self.stats_base.show()

    def package_manager_display(self):
        self.package_manager = package_manager.PackageManagerForm()
        self.package_manager.show()

    def jupyter_notebook_display(self):
        """
        使用多线程方式打开jupyter-notebook
        :return:
        """
        try:
            jupyter_path = os.path.dirname(sys.executable) + r"\Scripts\jupyter-notebook.exe"
            self.th = ThreadJupyter(jupyter_path)
            self.th.finishSignal.connect(self.jupyter_log)
            self.th.start()
        except Exception as e:
            print('jupyter_notebook_display:', e)

    def jupyter_log(self, msg):
        self.slot_flush_console("info", "jupyter", msg)