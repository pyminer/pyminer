import hashlib
import logging
import os
import platform
import subprocess
import sys
from pathlib import Path

import requests
from PySide2.QtCore import Qt, QThread, Signal
from PySide2.QtWidgets import QProgressBar, QVBoxLayout, QLabel, QApplication, QDesktopWidget, QDialog, QHBoxLayout, \
    QPushButton, QTableWidgetItem, QHeaderView, QTableView

import utils
from lib.util.check_update_ui import Ui_Dialog
from lib.util.make_update import should_be_recorded

"""
自动更新逻辑
1. 在程序启动脚本中，先运行本文件，如果检测到上次更新未完成（存在update.log），则执行更新程序。这部分逻辑应在打包程序时添加
2. 在系统启动时，后台开启更新检测，若存在更新，弹出对话框，选择是否更新。如是执行更新程序
3. 手动点击，执行更新程序
"""

# MD5_JSON_URL = "https://gitee.com/py2cn/pyminer/raw/dev/__latest.json"
MD5_JSON_URL = "https://gitee.com/py2cn/pyminer/raw/master/__latest.json"

# REMOTE_URL = 'https://gitee.com/py2cn/pyminer/raw/dev/' # 稳定版
REMOTE_URL = "https://gitee.com/py2cn/pyminer/raw/master/"

logger = logging.getLogger(__name__)


class BaseUpdateThread(QThread):
    def __init__(self, url):
        super().__init__()
        self.url = url
        self.local_files_info = {}
        self.remote_files_info = {}
        self.delete_files_info = []
        self.update_files_info = []
        self.local_pip_list = []
        self.remote_pip_list = []
        self.root = Path(__file__).parent.parent.parent

    def get_pip_list(self):
        platform_ = platform.system()
        requirement = 'requirements.txt'
        if platform_ == "Linux":
            requirement = 'requirements_linux.txt'
        elif platform_ == "Mac":
            requirement = 'requirements_mac.txt'
        path = self.root.joinpath(requirement)
        pip_list = []
        if path.is_file():
            with open(path, 'r', encoding='utf-8') as f:
                pip_list = f.read().splitlines()
        return pip_list

    def get_file_md5(self, path):
        if not os.path.isfile(path):
            return ""
        myhash = hashlib.md5()
        f = open(path, 'rb')
        while True:
            b = f.read(8096)
            b = b.replace(b'\r', b'')  # 这里是因为git会自动转换\r\n，为了保证多平台统一，在计算md5码时去除\r
            if not b:
                break
            myhash.update(b)
        f.close()
        md5 = myhash.hexdigest()
        return md5

    def generate_local_files_info(self):
        """生成目录树信息"""
        for path in self.root.glob('**/*'):
            if should_be_recorded(path):
                re_path = str(path.relative_to(self.root)).replace('\\', '/')
                md5 = self.get_file_md5(path)
                self.local_files_info.update(
                    {
                        re_path: md5
                    }
                )

    def get_remote_json_info(self):
        """获取远程文件信息"""
        try:
            response = requests.get(url=self.url, timeout=5)
        except Exception as e:
            return
        if response.status_code == 200:
            self.remote_files_info = response.json()['files']

    def generate_delete_files_info(self):
        if not self.remote_files_info or not self.local_files_info:
            return
        for key in self.local_files_info.keys():
            if not self.remote_files_info.get(key):
                self.delete_files_info.append(key)

    def generate_update_files_info(self):
        if not self.remote_files_info or not self.local_files_info:
            return
        for key in self.remote_files_info.keys():
            if self.local_files_info.get(key):
                if self.remote_files_info[key] != self.local_files_info[key]:  # md5值不同
                    self.update_files_info.append(key)
            else:
                self.update_files_info.append(key)  # 本地不存在


class UpdateTipThread(BaseUpdateThread):
    """用于程序启动时检测更新"""
    exist_update = Signal(bool)
    update_files_list = Signal(list)
    delete_files_list = Signal(list)

    def __init__(self, url):
        super().__init__(url)

    def run(self):
        self.generate_local_files_info()
        self.local_pip_list = self.get_pip_list()  # 获取当前的pip列表
        self.get_remote_json_info()
        self.generate_delete_files_info()
        self.generate_update_files_info()
        if self.update_files_info or self.delete_files_info:  # 检测到可用更新
            # if self.update_files_info:  # 检测到可用更新
            self.exist_update.emit(True)
            self.update_files_list.emit(self.update_files_info)
            self.delete_files_list.emit(self.delete_files_info)


class UpdateClientThread(BaseUpdateThread):
    """用于执行更新"""
    upgrade_bar = Signal(int)  # 更新进度条
    tip_label = Signal(str)  # 更新进度条
    exit_sign = Signal(bool)

    def __init__(self, url):
        super().__init__(url)

    def run(self):
        log_path = Path(__file__).parent.joinpath('update.log')
        if not log_path.is_file():
            log_path.touch()
        self.tip_label.emit('正在收集本地文件信息')
        self.generate_local_files_info()
        self.local_pip_list = self.get_pip_list()  # 获取当前的pip列表
        self.upgrade_bar.emit(20)
        self.tip_label.emit('正在查找更新')
        self.get_remote_json_info()
        self.upgrade_bar.emit(40)
        self.tip_label.emit('正在查找可删除文件')
        self.generate_delete_files_info()
        self.upgrade_bar.emit(50)
        self.tip_label.emit('正在查找可更新文件')
        self.generate_update_files_info()
        self.upgrade_bar.emit(60)
        self.tip_label.emit('正在执行更新')
        self.perform_update()
        self.upgrade_bar.emit(80)
        self.tip_label.emit('正在删除多余文件')
        self.perform_delete()
        self.remote_pip_list = self.get_pip_list()  # 再次获取pip列表
        self.upgrade_bar.emit(90)
        self.tip_label.emit('正在检查是否需要安装新的第三方库')
        self.perform_pip()
        os.remove(log_path)  # 删除空文件，标志着更新完成
        self.tip_label.emit('更新完成')
        self.exit_sign.emit(True)
        self.upgrade_bar.emit(100)

    def perform_update(self):
        counts = len(self.update_files_info)
        for index, item in enumerate(self.update_files_info):
            try:
                url = REMOTE_URL + item
                self.tip_label.emit('正在下载：%s' % url)
                response = requests.get(url=url, timeout=5)
            except Exception as e:
                return
            if response.status_code == 200:
                local_path = self.root.joinpath(item)
                if not local_path.parent.is_dir():
                    os.makedirs(local_path.parent)
                with open(local_path, 'wb') as f:
                    f.write(response.content)
                self.upgrade_bar.emit(60 + int((index + 1) * 20 / counts))

    def perform_delete(self):
        """执行删除"""
        for item in self.delete_files_info:
            abs_path = self.root.joinpath(item)
            if abs_path.is_file():
                os.remove(abs_path)

    def perform_pip(self):
        for item in self.remote_pip_list:
            if item not in self.local_pip_list:
                self.tip_label.emit('正在安装：%s' % item)
                # 推荐的安装方式
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", item, '-i', 'https://pypi.douban.com/simple'])


class UpdateTipClient(Ui_Dialog):
    def __init__(self, startup: bool):
        self.dialog = QDialog()
        self.setupUi(self.dialog)
        self.url = MD5_JSON_URL
        self.update_files_list = []
        self.delete_files_list = []
        self.root = Path(__file__).parent.parent.parent.parent
        self.is_start_thread(startup)

    def is_start_thread(self, startup: bool):
        """
        根据根目录下是否存在.git目录，判断是否处于开发状态，开发状态不检查更新
        根据设置界面检查更新checkbox是否为True，决定是否启动检查更新
        """
        if self.root.joinpath('.git').is_dir():
            return
        if not (startup and (not utils.get_settings_item_from_file("config.ini", "MAIN/CHECK_UPDATE"))):
            self.thread = UpdateTipThread(url=self.url)
            self.thread.update_files_list.connect(self.set_update_files_list)
            self.thread.delete_files_list.connect(self.set_delete_files_list)
            self.thread.exist_update.connect(self.set_exist_update)
            self.thread.start()

    def init_gui(self):
        self.update_files_num = 0
        self.delete_files_num = 0
        self.button_close.clicked.connect(self.dialog.close)
        self.button_confirm.clicked.connect(self.perform_update)
        self.button_detail.clicked.connect(self.show_table)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(['status', 'file'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table.setEditTriggers(QTableView.NoEditTriggers)
        self.table.setMinimumHeight(300)
        self.table.setVisible(False)
        self.dialog.setFixedHeight(100)
        self.move_center()
        if not QApplication.instance():
            app = QApplication(sys.argv)
        self.dialog.exec_()

    def move_center(self):
        qr = self.dialog.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.dialog.move(qr.topLeft())

    def set_update_files_list(self, files):
        self.update_files_list = files
        row = self.table.rowCount()
        self.table.setRowCount(self.table.rowCount() + len(files))
        for index, item in enumerate(self.update_files_list):
            self.table.setItem(row + index, 1, QTableWidgetItem(item))
            self.table.setItem(row + index, 0, QTableWidgetItem('update'))
        self.set_label()

    def set_delete_files_list(self, files):
        self.delete_files_list = files
        row = self.table.rowCount()
        self.table.setRowCount(row + len(files))
        for index, item in enumerate(self.delete_files_list):
            self.table.setItem(row + index, 1, QTableWidgetItem(item))
            self.table.setItem(row + index, 0, QTableWidgetItem('delete'))
        self.set_label()

    def set_label(self):
        self.label.setText(
            "检测到新版本，此次包含{0}个文件更新，{1}个文件删除。".format(
                len(self.update_files_list), len(self.delete_files_list)))

    def set_exist_update(self, flag):
        """
        存在更新则启动界面
        """
        if flag:
            self.init_gui()

    def perform_update(self):
        self.dialog.close()
        UpgradeClient(url=self.url)

    def show_table(self):
        if self.table.isVisible():
            self.button_detail.setText('+')
            self.table.setVisible(False)
            self.dialog.setFixedHeight(100)
        else:
            self.dialog.setFixedHeight(400)
            self.button_detail.setText('-')
            self.table.setVisible(True)


class UpgradeClient(QDialog):
    def __init__(self, url):
        super().__init__()
        self.setWindowTitle("Pyminer客户端升级助手")
        self.v_layout = QVBoxLayout()
        self.h_layout = QHBoxLayout()
        self.button = QPushButton('退出')
        self.button.setEnabled(False)
        self.button.clicked.connect(lambda: self.close())
        self.upgrade_bar = QProgressBar()
        self.tip_label = QLabel("")
        self.upgrade_bar.setRange(0, 100)
        self.upgrade_bar.setValue(0)
        self.v_layout.addWidget(self.tip_label)
        self.h_layout.addWidget(self.upgrade_bar)
        self.h_layout.addWidget(self.button)
        self.v_layout.addLayout(self.h_layout)
        self.setWindowFlags(Qt.WindowMinimizeButtonHint)
        self.setFixedWidth(500)
        self.setFixedHeight(70)
        self.move_center()
        self.setLayout(self.v_layout)
        self.thread = UpdateClientThread(url=url)
        self.thread.upgrade_bar.connect(self.set_upgrade_bar)
        self.thread.tip_label.connect(self.set_tip_label)
        self.thread.exit_sign.connect(self.set_exit_sign)
        self.thread.start()
        self.exec_()

    def move_center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def set_upgrade_bar(self, i):
        self.upgrade_bar.setValue(i)

    def set_tip_label(self, text):
        self.tip_label.setText(text)

    def set_exit_sign(self, sign):
        self.button.setEnabled(sign)


def perform_update():
    if not QApplication.instance():
        app = QApplication(sys.argv)
    UpgradeClient(url=MD5_JSON_URL)


def check_update_onload():
    """在启动时检查是否需要先执行更新"""
    log_path = Path(__file__).parent.joinpath('update.log')
    if log_path.is_file():
        perform_update()


if __name__ == '__main__':
    check_update_onload()
    perform_update()
