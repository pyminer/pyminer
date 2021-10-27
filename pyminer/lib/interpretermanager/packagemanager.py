import subprocess
import sys
from PySide2.QtWidgets import QFrame, QTableWidgetItem, QTableWidget, QMessageBox, QDialog, QDesktopWidget, QHeaderView, \
    QProgressDialog
from PySide2.QtGui import QCloseEvent
from PySide2.QtCore import Signal, Qt, QUrl, QPropertyAnimation, QCoreApplication
from lib.ui.base.pm_marketplace.package_manager_main import Ui_Form as marketplace_Ui_Form
from lib.ui.base.pm_marketplace.install import Ui_Form as marketplace_install_Ui_Form
from lib.ui.base.pm_marketplace.uninstall import Ui_Dialog as marketplace_uninstall_Ui_Dialog

from widgets import PMGOneShotThreadRunner


class MarketPlaceUninstall(QDialog, marketplace_uninstall_Ui_Dialog):
    signal_packages_changed = Signal()

    def __init__(self, parent=None, executable='', package_name=''):
        super(MarketPlaceUninstall, self).__init__(parent=parent)
        if executable == '':
            executable = sys.executable
        self._executable = executable
        self.setupUi(self)

        self.log_console.set_args(['%s' % self._executable, '-m', 'pip', 'uninstall', package_name, '-y'])
        self.log_console.button_to_start.hide()
        self.log_console.button_to_terminate.hide()
        self.log_console.start_process()
        self.button_close.clicked.connect(self.close)

    def closeEvent(self, a0: QCloseEvent) -> None:
        self.signal_packages_changed.emit()


class MarketPlaceInstall(QDialog, marketplace_install_Ui_Form):
    signal_packages_changed = Signal()

    def __init__(self, parent=None, executable=''):
        super(MarketPlaceInstall, self).__init__(parent=parent)
        if executable == '':
            executable = sys.executable
        self._executable = executable
        self.setupUi(self)
        self.center()
        self.groupBox.setVisible(False)  # 隐藏详情窗口。这是因为pip search功能现在已经无法使用。
        self.exec_log.button_to_start.setVisible(False)
        self.exec_log.button_to_terminate.setVisible(False)

        self.exec_log.set_args(['%s' % self._executable, '-m', 'pip', 'download', 'pyqtgraph',
                                '-i', 'https://pypi.tuna.tsinghua.edu.cn/simple'])
        # self.exec_log.start_process()

        self.checkBox_version.clicked.connect(self.checkbox_version_clicked)
        self.pushButton_install.clicked.connect(self.install)
        self.pushButton_close.clicked.connect(self.close)
        _trans = lambda text: QCoreApplication.translate('marketplace_install_Ui_Form', text)

        self.origins = ['https://mirrors.cloud.tencent.com/pypi/simple',
                        'https://pypi.org/simple',
                        'https://pypi.tuna.tsinghua.edu.cn/simple',
                        'https://mirrors.aliyun.com/pypi/simple/',
                        'http://pypi.douban.com/simple/'
                        ]
        self.label_3.hide()
        self.comboBox_dir.hide()
        self.lineEdit_dir.hide()
        self.toolButton.hide()
        self.checkbox_version_clicked(None)
        self.comboBox_source.currentIndexChanged.connect(self.combobox_source_changed)
        self.lineEdit_source.setEnabled(False)

    def checkbox_version_clicked(self, checked):
        if self.checkBox_version.isChecked():
            self.lineEdit_version.setEnabled(True)
        else:
            self.lineEdit_version.setEnabled(False)
            self.lineEdit_version.setText('<Latest>')

    def combobox_source_changed(self, s):
        index = self.comboBox_source.currentIndex()
        if index == len(self.origins):
            self.lineEdit_source.setEnabled(True)
        else:
            self.lineEdit_source.setEnabled(False)
            self.lineEdit_source.setText(self.origins[index])

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def install(self):
        package_name = self.lineEdit_name.text()
        origin_url = self.lineEdit_source.text()
        version = self.lineEdit_version.text()
        version = version if self.checkBox_version.isChecked() else ''

        if package_name.strip() == '':
            QMessageBox.warning(self, self.tr('Warning'),
                                self.tr('Package Name should not be empty!' % self.comboBox_source.currentText()))
            return
        if origin_url == '':
            QMessageBox.warning(self, self.tr('Warning'),
                                self.tr('Origin %s not exist!' % self.comboBox_source.currentText()))
            return
        if version != '':
            package_name = package_name + '==' + version
        self.exec_log.set_args(['%s' % self._executable, '-m', 'pip', 'install', package_name, '-i', origin_url])
        self.exec_log.start_process()

    def closeEvent(self, a0: QCloseEvent) -> None:
        self.signal_packages_changed.emit()


class MarketPlace(QDialog, marketplace_Ui_Form):
    def __init__(self, executable: str = ''):
        super(MarketPlace, self).__init__()
        if executable == '':
            executable = sys.executable
        self._executable = executable
        self.setupUi(self)

        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.center()

        self.pip_list()

        # 绑定事件
        self.toolButton_install.clicked.connect(self.pip_install_display)
        self.toolButton_uninstall.clicked.connect(self.pip_uninstall_display)

    def keyPressEvent(self, e):
        """
        按键盘Escape退出当前窗口
        @param e:
        """
        if e.key() == Qt.Key_Escape:
            self.close()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def pip_list(self):

        def list_pip_packages(executable):
            cmd = executable + ' -m pip list'
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            out, err = p.communicate()
            x = 1
            package_str = list()
            for r in out.splitlines():
                if x > 2:
                    package_str.append(r)
                x = x + 1
            return package_str

        def refresh_table(package_str):
            package_len = len(package_str)
            # 设置表格长度
            self.tableWidget.setRowCount(package_len)

            # 将结果显示在表格中
            for i in range(package_len):
                for j in range(2):
                    items_value = package_str[i].split()[j]
                    item = QTableWidgetItem(str(items_value, encoding="utf-8"))
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.tableWidget.setItem(i, j, item)

        self.process_dlg = QProgressDialog(parent=self, labelText=('Scanning packages..'))
        self.process_dlg.setCancelButton(None)
        self.process_dlg.setWindowFlags(self.process_dlg.windowFlags() | Qt.FramelessWindowHint)
        self.process_dlg.setRange(0, 0)

        self.pip_th = PMGOneShotThreadRunner(list_pip_packages, args=(self._executable,))
        self.pip_th.signal_finished.connect(refresh_table)
        self.pip_th.signal_finished.connect(self.process_dlg.close)
        self.process_dlg.show()

    def pip_install_display(self):
        pm_pack_install = MarketPlaceInstall(self, executable=self._executable)
        pm_pack_install.show()
        pm_pack_install.signal_packages_changed.connect(self.pip_list)

    def pip_uninstall_display(self):
        row = self.tableWidget.currentRow()
        if row >= 0:
            current_package = self.tableWidget.item(row, 0).text()
            ret = QMessageBox.warning(self, self.tr('Warning'),
                                      self.tr('Are you sure to remove package \'%s\'?' % current_package),
                                      QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if ret == QMessageBox.Yes:
                pm_pack_uninstall = MarketPlaceUninstall(self, executable=self._executable,
                                                         package_name=current_package)
                pm_pack_uninstall.show()
                pm_pack_uninstall.signal_packages_changed.connect(self.pip_list)
