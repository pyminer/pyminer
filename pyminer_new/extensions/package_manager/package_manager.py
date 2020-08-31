import os
import logging
# 导入PyQt5模块
from PyQt5.Qt import *
from qtpy import QtCore, QtWidgets

from pyminer_new.share.threads import *
from pyminer_new.extensions.package_manager import Ui_Form as EnvManager_Ui_Form
from pyminer_new.extensions.package_manager.package_install import Ui_Form as PackageInstall_Ui_Form
from pyminer_new.extensions.package_manager.package_update import Ui_Form as PackageUpdate_Ui_Form
from pyminer_new.extensions.package_manager import Ui_Form as PackageRemove_Ui_Form
from pyminer_new.extensions.package_manager.package_setting import Ui_Form as PackageSetting_Ui_Form
from pyminer_new.ui.source.qss.qss_tools import QssTools



class PackageManagerForm(QWidget, EnvManager_Ui_Form):
    """
    打开"包管理"窗口
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.center()
        self.source_index = "-i https://mirrors.cloud.tencent.com/pypi/simple"  # 设置默认镜像源地址

        self.widget.hide()
        self.package_filter_change()

        ui_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))),'ui')
        qss_path = os.path.join(ui_dir ,"source","qss","patata.qss")
        QssTools.set_qss_to_obj(qss_path, self)

        self.pushButton_install.clicked.connect(self.package_install_display)
        self.pushButton_import.clicked.connect(self.pip_requirements_import)  # 从requirements.txt导入包
        self.pushButton_export.clicked.connect(self.pip_freeze_export)  # 导出当前包到requirements.txt

        self.lineEdit_find.textChanged.connect(self.pip_find)
        self.listWidget.currentRowChanged.connect(self.env_display)
        self.pushButton_new.clicked.connect(self.env_new)
        self.pushButton_delete.clicked.connect(self.env_delete)
        self.pushButton_copy.clicked.connect(self.env_copy)
        self.comboBox.currentIndexChanged.connect(self.package_filter_change)  # 当下拉索引发生改变时发射信号触发绑定的事件

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

    def package_filter_change(self):
        try:
            if self.comboBox.currentText() == "已安装":
                self.package_filter_default()
            elif self.comboBox.currentText() == "可更新":
                # self.package_filter_update()
                self.writing_thread = QtCore.QThread()
                self.package_filter_update.moveToThread(self.writing_thread)


        except:
            pass

    def package_setting_display(self):
        """
        显示"数据信息"窗口
        """
        self.package_setting = PackageSettingForm()
        self.package_setting.show()

    def env_manager_display(self):
        if self.action_env.isChecked():
            self.widget.show()
        else:
            self.widget.hide()

    def env_delete(self):
        button = QMessageBox.Warning(self, "确认删除", "确认删除该虚拟环境吗？",
                                     QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Ok)
        if button == QMessageBox.Ok:
            print("确认")
        elif button == QMessageBox.Cancel:
            print("取消")
        else:
            return

    def env_new(self):
        self.listWidget.addItem("test")

    def env_copy(self):
        pass

    def env_display(self, i):
        self.stackedWidget.setCurrentIndex(i)

    def package_install_display(self):
        """
        显示"数据信息"窗口
        """
        self.package_install = PackageInstallForm()
        self.package_install.show()

    def package_update_display(self):
        """
        显示"数据信息"窗口
        """
        self.package_update = PackageUpdateForm()
        self.package_update.show()

    def package_remove_display(self):
        """
        显示"数据信息"窗口
        """
        self.package_remove = PackageRemoveForm()
        self.package_remove.show()

    def pip_freeze_export(self):
        """
        导出已安装的python包到requirements.txt文件中
        """
        export_path = QFileDialog.getSaveFileName(self, "导出已安装模块为requirements.txt",
                                                  os.path.join(os.path.expanduser('~'), "Desktop"),
                                                  r"文本文件(*.txt)")

        if export_path == "":
            logging.info("\n取消选择")
            return
        # cmd = "python -m pip freeze>" + export_path + "requirements.txt"
        print(export_path)
        # os.system(cmd)

    def pip_requirements_import(self):
        """
        导入requirements.txt文件并进行相关处理
        """
        import_path = QFileDialog.getOpenFileName(self, '导入requirements.txt', '', "文本文件(*.txt)")

        if import_path == "":
            logging.info("\n取消选择")
            return
        cmd = sys.executable + " -m pip install -r" + import_path[0]
        print(import_path)

    def package_filter_default(self):
        """
        pip环境管理页面初始化--默认筛选已安装的pip包
        """
        # result = subprocess.check_output("python -m pip list", encoding="utf-8")
        pipe = subprocess.run(sys.executable + " -m pip list", shell=True, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              encoding="utf-8")
        if pipe.returncode == 0:
            result = pipe.stdout
        else:
            result = pipe.stderr

        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 将表格变为禁止编辑
        self.tableWidget.setColumnCount(6)  # 设置列数
        self.tableWidget.setRowCount(len(result.splitlines()) - 2)  # 设置行数
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)  # 整行选中
        self.tableWidget.setHorizontalHeaderLabels(['包名', '当前版本', ' 最新版本', '类型', '', ''])  # 设置表头
        # self.tableWidget.horizontalHeader().setSectionResizeMode(6, QHeaderView.Stretch)  # 设置第五列宽度自动调整，充满屏幕
        self.tableWidget.horizontalHeader().setStretchLastSection(True)  # 设置最后一列拉伸至最大
        self.tableWidget.sortItems(0, Qt.AscendingOrder)
        self.tableWidget.setColumnHidden(3, False)  # 将第4列隐藏
        self.tableWidget.setColumnHidden(4, False)  # 将第5列隐藏
        self.tableWidget.setColumnWidth(0, 150)  # 设置第1列宽度
        self.tableWidget.setColumnWidth(1, 150)  # 设置第1列宽度
        self.tableWidget.setColumnWidth(2, 150)  # 设置第1列宽度
        self.tableWidget.setColumnWidth(3, 150)  # 设置第5列宽度
        self.tableWidget.setColumnWidth(4, 150)  # 设置第5列宽度
        self.tableWidget.setShowGrid(True)

        font = QFont('微软雅黑', 20)
        font.setBold(True)  # 设置字体加粗
        self.tableWidget.horizontalHeader().setFont(font)  # 设置表头字体
        self.tableWidget.horizontalHeader().setFixedHeight(30)  # 设置表头高度
        stylesheet = "::section{Background-color:rgb(242,242,242);border-radius:5px;border-width: 1px;border-style: " \
                     "outset;border-color: white;font: bold 12px;} "
        self.tableWidget.horizontalHeader().setStyleSheet(stylesheet)

        x = 0  # 当前行数
        for line in result.splitlines():  # 逐行读取pip 清单
            x += 1
            package = line.split()[0]
            version = line.split()[1]

            btn_update = QtWidgets.QPushButton("更新")
            btn_update.setMaximumWidth(40)
            btn_update.setStyleSheet('QPushButton{margin:3px}')
            btn_remove = QtWidgets.QPushButton("卸载")
            btn_remove.setMaximumWidth(40)
            btn_remove.setStyleSheet('QPushButton{margin:3px}')

            btn_update.clicked.connect(self.btn_pip_update)
            btn_remove.clicked.connect(self.btn_pip_remove)

            # 逐行写入pip数据到页面
            if 3 <= x <= len(result.splitlines()):  # 从第3行开始识别
                y = 0  # 列
                while y <= 5:
                    if y == 0:
                        name = QTableWidgetItem(package)
                        name.setTextAlignment(Qt.AlignCenter)
                        self.tableWidget.setItem(x - 3, y, name)
                    elif y == 1:
                        ver = QTableWidgetItem(version)
                        ver.setTextAlignment(Qt.AlignCenter)
                        self.tableWidget.setItem(x - 3, y, ver)
                    elif y == 4:
                        self.tableWidget.setCellWidget(x - 3, y, btn_update)
                    elif y == 5:
                        self.tableWidget.setCellWidget(x - 3, y, btn_remove)

                    y += 1

    def package_filter_update(self):
        """
        pip环境管理页面--筛选可更新的pip包
        """
        print("开始检查更新")
        cmd = sys.executable + " -m pip list -o" + " " + self.source_index
        # result = subprocess.check_output(cmd, encoding="utf-8")
        pipe = subprocess.run(cmd.strip(), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              encoding="utf-8")
        if pipe.returncode == 0:
            result = pipe.stdout
        else:
            result = pipe.stderr

        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 将表格变为禁止编辑
        self.tableWidget.setColumnCount(6)  # 设置列数
        self.tableWidget.setRowCount(len(result.splitlines()) - 2)  # 设置行数
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)  # 整行选中
        self.tableWidget.setHorizontalHeaderLabels(['包名', '当前版本', ' 最新版本', '类型', '', ''])  # 设置表头
        # self.tableWidget.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)  # 设置第五列宽度自动调整，充满屏幕
        self.tableWidget.horizontalHeader().setStretchLastSection(True)  # 设置最后一列拉伸至最大
        self.tableWidget.sortItems(0, Qt.AscendingOrder)
        self.tableWidget.setColumnHidden(3, False)  # 将第4列隐藏
        self.tableWidget.setColumnHidden(4, False)  # 将第5列隐藏
        self.tableWidget.setColumnWidth(0, 150)  # 设置第1列宽度
        self.tableWidget.setColumnWidth(1, 150)  # 设置第1列宽度
        self.tableWidget.setColumnWidth(2, 150)  # 设置第1列宽度
        self.tableWidget.setColumnWidth(3, 150)  # 设置第5列宽度
        self.tableWidget.setColumnWidth(4, 150)  # 设置第5列宽度
        self.tableWidget.setShowGrid(True)

        font = QFont('微软雅黑', 20)
        font.setBold(True)  # 设置字体加粗
        self.tableWidget.horizontalHeader().setFont(font)  # 设置表头字体
        self.tableWidget.horizontalHeader().setFixedHeight(30)  # 设置表头高度
        stylesheet = "::section{Background-color:rgb(242,242,242);border-radius:5px;border-width: 1px;border-style: " \
                     "outset;border-color: white;font: bold 12px;} "
        self.tableWidget.horizontalHeader().setStyleSheet(stylesheet)

        x = 0  # 当前行数
        for line in result.splitlines():  # 逐行读取pip 清单
            x += 1
            package = line.split()[0]
            version = line.split()[1]
            latest = line.split()[2]
            type = line.split()[3]

            btn_update = QtWidgets.QPushButton("更新")
            btn_update.setMaximumWidth(40)
            btn_update.setStyleSheet('QPushButton{margin:3px}')
            btn_remove = QtWidgets.QPushButton("卸载")
            btn_remove.setMaximumWidth(40)
            btn_remove.setStyleSheet('QPushButton{margin:3px}')

            btn_update.clicked.connect(self.btn_pip_update)
            btn_remove.clicked.connect(self.btn_pip_remove)

            # 逐行写入pip数据到页面
            if 3 <= x <= len(result.splitlines()):  # 从第3行开始识别
                y = 0  # 列
                while y <= 5:
                    if y == 0:
                        name = QTableWidgetItem(package)
                        name.setTextAlignment(Qt.AlignCenter)
                        self.tableWidget.setItem(x - 3, y, name)
                    elif y == 1:
                        ver = QTableWidgetItem(version)
                        ver.setTextAlignment(Qt.AlignCenter)
                        self.tableWidget.setItem(x - 3, y, ver)
                    elif y == 2:
                        ver = QTableWidgetItem(latest)
                        ver.setTextAlignment(Qt.AlignCenter)
                        self.tableWidget.setItem(x - 3, y, ver)
                    elif y == 3:
                        ver = QTableWidgetItem(type)
                        ver.setTextAlignment(Qt.AlignCenter)
                        self.tableWidget.setItem(x - 3, y, ver)
                    elif y == 4:
                        self.tableWidget.setCellWidget(x - 3, y, btn_update)
                    elif y == 5:
                        self.tableWidget.setCellWidget(x - 3, y, btn_remove)

                    y += 1

    def btn_pip_remove(self):
        """
        调用pip卸载包
        """
        print("调用pip卸载包")
        row = self.tableWidget.currentRow()
        package = self.tableWidget.item(row, 0).text()
        package_remove_form = PackageRemoveForm()
        package_remove_form.set_package_name(package)
        package_remove_form.exec_()

    def btn_pip_update(self):
        """
        调用pip升级包
        """
        print("调用pip升级包")
        row = self.tableWidget.currentRow()
        package = self.tableWidget.item(row, 0).text()
        package_update_form = PackageUpdateForm()
        package_update_form.set_package_name(package)
        package_update_form.exec_()

    def pip_find(self):
        """
        查找指定包
        """
        text = self.lineEdit_find.text().strip()  # 查找内容
        items = self.tableWidget.findItems(text, Qt.MatchContains)
        rows = self.tableWidget.rowCount()  # 获取表格行数
        i = 0
        # 隐藏所有列
        while i < rows:
            self.tableWidget.setRowHidden(i, True)
            i += 1
        m = 0
        while m < len(items):
            try:
                item = items[m].row()
                self.tableWidget.setRowHidden(item, False)
            except:
                pass
            m += 1

    def pip_update_check(self):
        cmd = sys.executable + " -m pip list -o "


class PackageInstallForm(QWidget, PackageInstall_Ui_Form):
    """
    打开"使用pip安装python包"窗口
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.center()
        self.pip_init()
        self.source_index = "-i https://mirrors.cloud.tencent.com/pypi/simple"

        self.comboBox_source.currentIndexChanged.connect(self.source_change)
        self.comboBox_dir.currentIndexChanged.connect(self.dir_change)
        self.pushButton_ok.clicked.connect(self.package_install)
        self.pushButton_cancel.clicked.connect(self.close)
        self.checkBox_version.stateChanged.connect(self.version_change)

        filter_delay = DelayedExecutionTimer(self.lineEdit_name)
        self.lineEdit_name.textChanged.connect(filter_delay.trigger)
        filter_delay.triggered[str].connect(self.set_package_info)

    def keyPressEvent(self, e):
        """
        按键盘Escape退出当前窗口
        @param e:
        """
        if e.key() == Qt.Key_Escape:
            self.close()

    def center(self):
        """
        设置窗口居中
        """
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)

    def pip_init(self):
        python_path = sys.executable
        package_path = os.path.split(python_path)[0] + r"Lib\site-packages"
        self.lineEdit_dir.setStyleSheet("background-color:rgb(208, 207, 209);")
        self.lineEdit_dir.setReadOnly(True)
        self.lineEdit_dir.setText(package_path)
        self.lineEdit_source.setStyleSheet("background-color:rgb(208, 207, 209);")
        self.lineEdit_source.setReadOnly(True)

    def dir_change(self):
        import sys
        python_path = sys.executable
        if self.comboBox_dir.currentText() == "默认位置":
            self.lineEdit_dir.setReadOnly(True)
            self.lineEdit_dir.setStyleSheet("background-color:rgb(208, 207, 209);")
            package_path = os.path.split(python_path)[0] + r"Lib\site-packages"
            self.lineEdit_dir.setText(package_path)
        elif self.comboBox_dir.currentText() == "用户目录":
            self.lineEdit_dir.setReadOnly(True)
            self.lineEdit_dir.setStyleSheet("background-color:rgb(208, 207, 209);")
            for i in sys.path:
                if i.find("Users") >= 0 and i.find("site-packages") >= 0:
                    self.lineEdit_dir.setText(i)
        elif self.comboBox_dir.currentText() == "自定义":
            self.lineEdit_dir.setReadOnly(False)
            self.lineEdit_dir.setStyleSheet("background-color:rgb(110, 190, 10);")
            self.lineEdit_dir.setText("")
            self.lineEdit_dir.setPlaceholderText("请选择python包安装目录")
        elif self.comboBox_dir.currentText() == "仅下载":
            self.lineEdit_dir.setReadOnly(False)
            self.lineEdit_dir.setStyleSheet("background-color:rgb(110, 190, 10);")
            self.lineEdit_dir.setText("")
            self.lineEdit_dir.setPlaceholderText("请选择下载目录")

    def source_change(self):
        if self.comboBox_source.currentText() == "腾讯(推荐)":
            self.lineEdit_source.setReadOnly(True)
            self.lineEdit_source.setStyleSheet("background-color:rgb(208, 207, 209);")
            self.lineEdit_source.setText("https://mirrors.cloud.tencent.com/pypi/simple")
        elif self.comboBox_source.currentText() == "官方":
            self.lineEdit_source.setReadOnly(True)
            self.lineEdit_source.setStyleSheet("background-color:rgb(208, 207, 209);")
            self.lineEdit_source.setText("https://pypi.org/")
        elif self.comboBox_source.currentText() == "华为":
            self.lineEdit_source.setReadOnly(True)
            self.lineEdit_source.setStyleSheet("background-color:rgb(208, 207, 209);")
            self.lineEdit_source.setText("https://mirrors.huaweicloud.com/repository/pypi/simple")
        elif self.comboBox_source.currentText() == "清华大学":
            self.lineEdit_source.setReadOnly(True)
            self.lineEdit_source.setStyleSheet("background-color:rgb(208, 207, 209);")
            self.lineEdit_source.setText("https://pypi.tuna.tsinghua.edu.cn/simple")
        elif self.comboBox_source.currentText() == "阿里":
            self.lineEdit_source.setReadOnly(True)
            self.lineEdit_source.setStyleSheet("background-color:rgb(208, 207, 209);")
            self.lineEdit_source.setText("https://mirrors.aliyun.com/pypi/simple")
        elif self.comboBox_source.currentText() == "豆瓣":
            self.lineEdit_source.setReadOnly(True)
            self.lineEdit_source.setStyleSheet("background-color:rgb(208, 207, 209);")
            self.lineEdit_source.setText("http://pypi.douban.com/simple")
        elif self.comboBox_source.currentText() == "自定义":
            self.lineEdit_source.setReadOnly(False)
            self.lineEdit_source.setStyleSheet("background-color:rgb(110, 190, 10);")
            self.lineEdit_source.setText("")
            self.lineEdit_source.setPlaceholderText("请输入镜像源地址")

    def version_change(self):
        if self.checkBox_version.checkState() == 2:
            self.comboBox_version.setEnabled(True)
            self.comboBox_version.setEditable(True)
            self.comboBox_version.setItemText(0, "")
            self.comboBox_version.lineEdit().setPlaceholderText("填写需要安装的版本号")
        else:
            self.comboBox_version.setEnabled(False)

    def package_install(self):
        """
        调用系统命令，使用pip安装python包
        """
        if len(self.lineEdit_name.text().strip()) > 0:
            package_name = self.lineEdit_name.text().strip()
        else:
            QMessageBox.warning(self, '注意', '包名为空！', QMessageBox.Yes)

        if self.checkBox_version.isChecked():
            if len(self.comboBox_version.currentText().strip()) > 0:
                version = "==" + self.comboBox_version.currentText().strip()
            else:
                version = ""
        else:
            version = ""

        if self.comboBox_dir.currentText() == "默认位置":
            target = ""
        elif self.comboBox_dir.currentText() == "安装到用户目录":
            target = "--user"
            print("安装到用户目录")
        elif self.comboBox_dir.currentText() == "指定安装位置":
            target = "--target = " + self.lineEdit_dir.text()
        elif self.comboBox_dir.currentText() == "仅下载":
            print("仅下载")

        if self.comboBox_source.currentText() == "腾讯(推荐)":
            self.source_index = "-i https://mirrors.cloud.tencent.com/pypi/simple"
        elif self.comboBox_source.currentText() == "官方":
            self.source_index = ""
        elif self.comboBox_source.currentText() == "华为":
            self.source_index = "-i https://mirrors.huaweicloud.com/repository/pypi/simple"
        elif self.comboBox_source.currentText() == "清华大学":
            self.source_index = "-i https://pypi.tuna.tsinghua.edu.cn/simple"
        elif self.comboBox_source.currentText() == "阿里":
            self.source_index = "-i https://mirrors.aliyun.com/pypi/simple"
        elif self.comboBox_source.currentText() == "豆瓣":
            self.source_index = "-i http://pypi.douban.com/simple"
        elif self.comboBox_source.currentText() == "自定义" and self.lineEdit_source.text() == "":
            self.source_index = "-i http://pypi.douban.com/simple"
            QMessageBox.warning(self, '注意', '镜像源地址为空！', QMessageBox.Yes)

        self.th = threads.ThreadPipInstall(package_name=package_name, target_path=target,
                                           source_index=self.source_index, version=version)
        self.th.finishSignal.connect(self.button_finish)
        self.th.start()

    def button_finish(self, result):
        print("信号接收成功")
        self.textEdit_log.moveCursor(QtGui.QTextCursor.End)  # 鼠标移动到文本末尾
        self.textEdit_log.insertPlainText(result)  # 插入执行结果
        # self.textEdit_log.setText(result)

    def set_package_info(self):
        """
        从pypi获取包的信息
        """
        if len(self.lineEdit_name.text().strip()) > 0:
            self.textEdit_desc.setText("正在加载...")
            package_name = self.lineEdit_name.text()
            cmd = sys.executable + " -m pip search " + package_name
            # result = subprocess.check_output(cmd_info,encoding="utf-8")
            pipe = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                  encoding="utf-8")
            if pipe.returncode == 0:
                result = pipe.stdout
            else:
                result = pipe.stderr
            self.textEdit_desc.setText(result)
        else:
            self.textEdit_desc.setText("")


class PackageUpdateForm(QWidget, PackageUpdate_Ui_Form):
    """
    打开"使用pip更新python包"窗口
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.center()
        self.pip_init()
        self.source_index = "-i https://mirrors.cloud.tencent.com/pypi/simple"

        # self.lineEdit_dir.setHidden(True)  #隐藏安装目录

        self.comboBox_source.currentIndexChanged.connect(self.source_change)
        self.comboBox_dir.currentIndexChanged.connect(self.dir_change)
        self.pushButton_ok.clicked.connect(self.package_update)
        self.pushButton_cancel.clicked.connect(self.close)
        self.checkBox_version.stateChanged.connect(self.version_change)

        filter_delay = DelayedExecutionTimer(self.lineEdit_name)
        self.lineEdit_name.textChanged.connect(filter_delay.trigger)
        filter_delay.triggered[str].connect(self.set_package_info)

    def keyPressEvent(self, e):
        """
        按键盘Escape退出当前窗口
        @param e:
        """
        if e.key() == Qt.Key_Escape:
            self.close()

    def center(self):
        """
        设置窗口居中
        """
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)

    def pip_init(self):
        python_path = sys.executable
        package_path = os.path.split(python_path)[0] + r"Lib\site-packages"
        self.lineEdit_dir.setStyleSheet("background-color:rgb(208, 207, 209);")
        self.lineEdit_dir.setReadOnly(True)
        self.lineEdit_dir.setText(package_path)
        self.lineEdit_source.setStyleSheet("background-color:rgb(208, 207, 209);")
        self.lineEdit_source.setReadOnly(True)

    def dir_change(self):
        import sys
        python_path = sys.executable
        if self.comboBox_dir.currentText() == "默认位置":
            self.lineEdit_dir.setReadOnly(True)
            self.lineEdit_dir.setStyleSheet("background-color:rgb(208, 207, 209);")
            package_path = os.path.split(python_path)[0] + r"Lib\site-packages"
            self.lineEdit_dir.setText(package_path)
        elif self.comboBox_dir.currentText() == "用户目录":
            self.lineEdit_dir.setReadOnly(True)
            self.lineEdit_dir.setStyleSheet("background-color:rgb(208, 207, 209);")
            for i in sys.path:
                if i.find("Users") >= 0 and i.find("site-packages") >= 0:
                    self.lineEdit_dir.setText(i)
        elif self.comboBox_dir.currentText() == "自定义":
            self.lineEdit_dir.setReadOnly(False)
            self.lineEdit_dir.setStyleSheet("background-color:rgb(110, 190, 10);")
            self.lineEdit_dir.setText("")
            self.lineEdit_dir.setPlaceholderText("请选择python包安装目录")
        elif self.comboBox_dir.currentText() == "仅下载":
            self.lineEdit_dir.setReadOnly(False)
            self.lineEdit_dir.setStyleSheet("background-color:rgb(110, 190, 10);")
            self.lineEdit_dir.setText("")
            self.lineEdit_dir.setPlaceholderText("请选择下载目录")

    def source_change(self):
        if self.comboBox_source.currentText() == "腾讯(推荐)":
            self.lineEdit_source.setReadOnly(True)
            self.lineEdit_source.setStyleSheet("background-color:rgb(208, 207, 209);")
            self.lineEdit_source.setText("https://mirrors.cloud.tencent.com/pypi/simple")
        elif self.comboBox_source.currentText() == "官方":
            self.lineEdit_source.setReadOnly(True)
            self.lineEdit_source.setStyleSheet("background-color:rgb(208, 207, 209);")
            self.lineEdit_source.setText("https://pypi.org/")
        elif self.comboBox_source.currentText() == "华为":
            self.lineEdit_source.setReadOnly(True)
            self.lineEdit_source.setStyleSheet("background-color:rgb(208, 207, 209);")
            self.lineEdit_source.setText("https://mirrors.huaweicloud.com/repository/pypi/simple")
        elif self.comboBox_source.currentText() == "清华大学":
            self.lineEdit_source.setReadOnly(True)
            self.lineEdit_source.setStyleSheet("background-color:rgb(208, 207, 209);")
            self.lineEdit_source.setText("https://pypi.tuna.tsinghua.edu.cn/simple")
        elif self.comboBox_source.currentText() == "阿里":
            self.lineEdit_source.setReadOnly(True)
            self.lineEdit_source.setStyleSheet("background-color:rgb(208, 207, 209);")
            self.lineEdit_source.setText("https://mirrors.aliyun.com/pypi/simple")
        elif self.comboBox_source.currentText() == "豆瓣":
            self.lineEdit_source.setReadOnly(True)
            self.lineEdit_source.setStyleSheet("background-color:rgb(208, 207, 209);")
            self.lineEdit_source.setText("http://pypi.douban.com/simple")
        elif self.comboBox_source.currentText() == "自定义":
            self.lineEdit_source.setReadOnly(False)
            self.lineEdit_source.setStyleSheet("background-color:rgb(110, 190, 10);")
            self.lineEdit_source.setText("")
            self.lineEdit_source.setPlaceholderText("请输入镜像源地址")

    def version_change(self):
        if self.checkBox_version.checkState() == 2:
            self.comboBox_version.setEnabled(True)
            self.comboBox_version.setEditable(True)
            self.comboBox_version.setItemText(0, "")
            self.comboBox_version.lineEdit().setPlaceholderText("填写需要安装的版本号")
        else:
            self.comboBox_version.setEnabled(False)

    def package_update(self):
        """
        调用系统命令，使用pip安装python包
        """
        if len(self.lineEdit_name.text().strip()) > 0:
            package_name = self.lineEdit_name.text().strip()
        else:
            QMessageBox.warning(self, '注意', '包名为空！', QMessageBox.Yes)

        if self.checkBox_version.isChecked():
            if len(self.comboBox_version.currentText().strip()) > 0:
                version = "==" + self.comboBox_version.currentText().strip()
            else:
                version = ""
        else:
            version = ""

        if self.comboBox_dir.currentText() == "默认位置":
            target = ""
        elif self.comboBox_dir.currentText() == "安装到用户目录":
            target = "--user"
            print("安装到用户目录")
        elif self.comboBox_dir.currentText() == "指定安装位置":
            target = "--target = " + self.lineEdit_dir.text()
        elif self.comboBox_dir.currentText() == "仅下载":
            print("仅下载")

        if self.comboBox_source.currentText() == "腾讯(推荐)":
            self.source_index = "-i https://mirrors.cloud.tencent.com/pypi/simple"
        elif self.comboBox_source.currentText() == "官方":
            self.source_index = ""
        elif self.comboBox_source.currentText() == "华为":
            self.source_index = "-i https://mirrors.huaweicloud.com/repository/pypi/simple"
        elif self.comboBox_source.currentText() == "清华大学":
            self.source_index = "-i https://pypi.tuna.tsinghua.edu.cn/simple"
        elif self.comboBox_source.currentText() == "阿里":
            self.source_index = "-i https://mirrors.aliyun.com/pypi/simple"
        elif self.comboBox_source.currentText() == "豆瓣":
            self.source_index = "-i http://pypi.douban.com/simple"
        elif self.comboBox_source.currentText() == "自定义" and self.lineEdit_source.text() == "":
            self.source_index = "-i http://pypi.douban.com/simple"
            QMessageBox.warning(self, '注意', '镜像源地址为空！', QMessageBox.Yes)
        cmd = sys.executable + " -m pip install --upgrade " + self.source_index + " " + target + " " + package_name + version
        self.textEdit_log.setPlainText("")  # 清空当前日志
        self.textEdit_log.insertPlainText("正在执行{0}".format(cmd) + '\n')

        # result = subprocess.check_output(cmd.strip(), encoding="utf-8")
        pipe = subprocess.run(cmd.strip(), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              encoding="utf-8")
        if pipe.returncode == 0:
            result = pipe.stdout
        else:
            result = pipe.stderr

        self.textEdit_log.insertPlainText(result)

    def set_cmd(self, str):
        self.textEdit_log.setText("当前命令为：{0}".format(str))
        self.package_update()

    def set_package_name(self, str):
        self.lineEdit_name.setText(str)

    def set_package_info(self):
        if len(self.lineEdit_name.text().strip()) > 0:
            self.textEdit_desc.setText("正在加载...")
            package_name = self.lineEdit_name.text()
            cmd = sys.executable + " -m pip show " + package_name
            # result = subprocess.check_output(cmd_info, encoding="utf-8")
            pipe = subprocess.run(cmd.strip(), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                  encoding="utf-8")
            if pipe.returncode == 0:
                result = pipe.stdout
            else:
                result = pipe.stderr

            self.textEdit_desc.setText(result)
        else:
            self.textEdit_desc.setText("")


class PackageRemoveForm(QWidget, PackageRemove_Ui_Form):
    """
    打开"使用pip卸载python包"窗口
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.center()

        self.toolButton_open.clicked.connect(self.open_package_path)
        self.pushButton_ok.clicked.connect(self.package_remove)

        filter_delay = DelayedExecutionTimer(self.lineEdit_name)
        self.lineEdit_name.textChanged.connect(filter_delay.trigger)
        filter_delay.triggered[str].connect(self.set_package_info)

        # self.pip_init()

        # self.lineEdit_dir.setHidden(True)  #隐藏安装目录

        # self.comboBox_source.currentIndexChanged.connect(self.source_change)
        # self.comboBox_dir.currentIndexChanged.connect(self.dir_change)

        # self.pushButton_cancel.clicked.connect(self.close)
        # self.checkBox_version.stateChanged.connect(self.version_change)

    def keyPressEvent(self, e):
        """
        按键盘Escape退出当前窗口
        @param e:
        """
        if e.key() == Qt.Key_Escape:
            self.close()

    def center(self):
        """
        设置窗口居中
        """
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)

    def open_package_path(self):
        """
        打开python包的安装路径
        """
        import win32api
        path = self.lineEdit_dir.text()
        try:
            win32api.ShellExecute(0, 'open', path, '', '', 1)
        except IOError:
            print("error")

    def pip_init(self):
        python_path = sys.executable
        package_path = os.path.split(python_path)[0] + r"Lib\site-packages"
        self.lineEdit_dir.setStyleSheet("background-color:rgb(208, 207, 209);")
        self.lineEdit_dir.setReadOnly(True)
        self.lineEdit_dir.setText(package_path)
        self.lineEdit_source.setStyleSheet("background-color:rgb(208, 207, 209);")
        self.lineEdit_source.setReadOnly(True)

    def package_remove(self):
        """
        调用系统命令，使用pip卸载python包
        """
        if len(self.lineEdit_name.text().strip()) > 0:
            self.textEdit_desc.setText("正在加载...")
            package_name = self.lineEdit_name.text()
            cmd = sys.executable + " -m pip uninstall " + package_name
            # result = subprocess.check_output(cmd_info, encoding="utf-8")
            pipe = subprocess.run(cmd.strip(), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                  encoding="utf-8")
            if pipe.returncode == 0:
                result = pipe.stdout
            else:
                result = pipe.stderr

            self.textEdit_desc.setText(result)
        else:
            self.textEdit_desc.setText("")

    def set_cmd(self, str):
        self.textEdit_log.setText("当前命令为：{0}".format(str))

    def set_package_name(self, str):
        self.lineEdit_name.setText(str)

    def set_package_info(self):
        if len(self.lineEdit_name.text().strip()) > 0:
            self.textEdit_desc.setText("正在加载...")
            package_name = self.lineEdit_name.text()
            cmd = sys.executable + " -m pip show " + package_name
            # result = subprocess.check_output(cmd_info, encoding="utf-8")
            pipe = subprocess.run(cmd.strip(), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                  encoding="utf-8")
            if pipe.returncode == 0:
                result = pipe.stdout
                for line in result.splitlines():
                    if line.find("Location") >= 0:
                        self.lineEdit_dir.setText(line[10:])
            else:
                result = pipe.stderr

            self.textEdit_desc.setText(result)
        else:
            self.textEdit_desc.setText("")


class PackageSettingForm(QWidget, PackageSetting_Ui_Form):
    """
    打开"使用pip卸载python包"窗口
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.center()

    def keyPressEvent(self, e):
        """
        按键盘Escape退出当前窗口
        @param e:
        """
        if e.key() == Qt.Key_Escape:
            self.close()

    def center(self):
        """
        设置窗口居中
        """
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)


class DelayedExecutionTimer(QObject):  # source: https://wiki.qt.io/Delay_action_to_wait_for_user_interaction
    """
    延迟执行筛选
    """
    triggered = pyqtSignal(str)

    def __init__(self, parent):
        super(DelayedExecutionTimer, self).__init__(parent)
        # The minimum delay is the time the class will wait after being triggered before emitting the triggered() signal
        # (if there is no key press for this time: trigger)
        self.minimumDelay = 500
        self.minimumTimer = QTimer(self)
        self.minimumTimer.timeout.connect(self.timeout)

    def timeout(self):
        self.minimumTimer.stop()
        self.triggered.emit(self.string)

    def trigger(self, string):
        self.string = string
        self.minimumTimer.stop()
        self.minimumTimer.start(self.minimumDelay)


class database_pip_manage(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)

    def db_pip_update_insert(self):
        from PyQt5 import QtSql
        from PyQt5.QtSql import QSqlQuery

        database = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        database.setDatabaseName('patata.db')

        if database.open():
            print("OK")
        else:
            print("连接数据库失败！")

        insert_sql = 'insert into pip_install_info values (?,?,?)'
        query = QSqlQuery()
        query.prepare(insert_sql)
        query.addBindValue(4)
        query.addBindValue('test3')
        query.addBindValue(1)
        if not query.exec_():
            print(query.lastError())
        else:
            print('inserted')



    def button_finish(self, msg):
        print(msg)



# ====================================窗体测试程序============================
if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = PackageManagerForm()
    form.show()
    sys.exit(app.exec_())
