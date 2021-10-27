import base64
import json
import logging
import os
import sys
import time
import webbrowser
from multiprocessing import shared_memory
from typing import List

import qdarkstyle
from PySide2.QtCore import QPoint, QRectF
from PySide2.QtGui import QMouseEvent, QPainter, QLinearGradient, QCursor
from PySide2.QtGui import QCloseEvent
from PySide2.QtCore import Signal, Qt, QUrl, QPropertyAnimation
from PySide2.QtGui import QCloseEvent
from PySide2.QtGui import QMouseEvent
from PySide2.QtWebEngineWidgets import *
from PySide2.QtWidgets import QListWidgetItem, QWizard, QMessageBox
from PySide2.QtWidgets import QWidget, QDesktopWidget, QFileDialog, QApplication, QDialog

import utils
from lib.extensions.extensionlib.extension_lib import extension_lib
from lib.ui.ui_aboutme import Ui_Form as About_Ui_Form
from lib.ui.ui_appstore import Ui_Form as appStore_Ui_Form
from lib.ui.ui_first_form import Ui_Form as first_Ui_Form
from lib.ui.ui_login import Ui_Form as login_Ui_Form
from lib.ui.ui_logined import Ui_Form as logined_Ui_Form
from lib.ui.ui_option import Ui_Form as Option_Ui_Form
from lib.ui.ui_project_wizard import Ui_Wizard as Project_Ui_Form
from widgets import PMGPanel
from utils import get_main_window, http_client

logger = logging.getLogger(__name__)


class OptionForm(QDialog, Option_Ui_Form):
    """
    打开"选项"窗口
    """
    signal_settings_changed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.center()
        self.page_format.setEnabled(False)
        self.page_appearance.setEnabled(False)

        self.setup_ui()

        # 通过combobox控件选择窗口风格
        self.comboBox_theme.activated[str].connect(self.slot_theme_changed)

        self.setting = dict()

        self.listWidget.currentRowChanged.connect(self.option_change)
        self.toolButton_workspace.clicked.connect(self.slot_change_workspace)
        self.toolButton_output.clicked.connect(self.slot_change_output)
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_ok.clicked.connect(self.close)
        self.pushButton_help.clicked.connect(self.get_help)

    def setup_ui(self):
        self.comboBox_9.setEnabled(False)
        self.comboBox_8.setEnabled(False)
        # self.checkbox_show_startpage.setEnabled(False)
        # self.checkBox_minitray.setEnabled(False)

    def add_settings_panel(self, text: str, settings_content: List):
        settings_widget = PMGPanel(views=settings_content)
        self.signal_settings_changed.connect(settings_widget.emit_settings_changed_signal)
        self.stackedWidget.addWidget(settings_widget)
        self.listWidget.addItem(QListWidgetItem(text))
        return settings_widget

    def add_page(self, text, page: QWidget):
        self.stackedWidget.addWidget(page)
        self.listWidget.addItem(QListWidgetItem(text))
        return page

    def closeEvent(self, a0: 'QCloseEvent') -> None:
        super(OptionForm, self).closeEvent(a0)
        self.refresh_settings()

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

    def option_change(self, i):
        self.stackedWidget.setCurrentIndex(i)

    def slot_theme_changed(self, style):
        """
        在主题颜色改变时触发的回调
        :param style:
        :return:
        """
        from features.io.settings import load_theme
        load_theme(style)
        utils.write_settings_item_to_file("config.ini", "MAIN/THEME", self.comboBox_theme.currentText())
        get_main_window().settings_changed_signal.emit()

    def slot_change_workspace(self):
        """
        改变工作路径时的回调
        Returns:

        """
        work_dir = utils.get_settings_item_from_file("config.ini", "MAIN/THEME", self.comboBox_theme.currentText())
        directory = QFileDialog.getExistingDirectory(self, "选择工作路径位置", directory=work_dir)
        if not directory == '':
            self.lineEdit_worksapce.setText(directory)

    def slot_change_output(self):
        directory = QFileDialog.getExistingDirectory(self, "选择输出文件夹位置", os.path.expanduser('~'))
        self.lineEdit_output.setText(directory)

    def load_settings(self):
        """
        在show()之前调用这个方法
        从而每次重新显示的时候都可以刷新数据。
        :return:
        """
        settings = utils.get_settings_from_file("config.ini")
        logger.debug("PATH/WORKDIR", settings.value('MAIN/PATH_WORKDIR'))
        if settings.value('MAIN/THEME') is not None:
            for i in range(self.comboBox_theme.count()):
                if self.comboBox_theme.itemText(i) == settings.value('MAIN/THEME'):
                    self.comboBox_theme.setCurrentIndex(i)
        self.lineEdit_worksapce.setText(settings.value("MAIN/PATH_WORKDIR"))
        self.lineEdit_output.setText(settings.value("MAIN/PATH_OUTPUT"))

        check_update = utils.get_settings_item_from_file("config.ini", "MAIN/CHECK_UPDATE")
        show_start_page = utils.get_settings_item_from_file("config.ini", "MAIN/SHOW_START_PAGE")
        self.check_box_check_upd_on_startup.setChecked(check_update)
        self.checkbox_show_startpage.setChecked(show_start_page)

    def refresh_settings(self):
        """
        窗口关闭时，调用此方法，刷新主界面设置项。
        :return:
        """
        utils.write_settings_item_to_file("config.ini", "MAIN/THEME", self.comboBox_theme.currentText())
        utils.write_settings_item_to_file("config.ini", "MAIN/PATH_WORKDIR", self.lineEdit_worksapce.text())
        utils.write_settings_item_to_file("config.ini", "MAIN/PATH_OUTPUT", self.lineEdit_output.text())
        utils.write_settings_item_to_file("config.ini", "MAIN/CHECK_UPDATE",
                                          self.check_box_check_upd_on_startup.isChecked())
        utils.write_settings_item_to_file("config.ini", "MAIN/SHOW_START_PAGE",
                                          self.checkbox_show_startpage.isChecked())

        get_main_window().on_settings_changed()
        self.signal_settings_changed.emit()

    def show(self):
        """
        重写此方法，在显示之前重新加载一遍设置。
        :return:
        """
        self.load_settings()
        super(OptionForm, self).show()

    def exec_(self):
        """
        继承exec_方法。
        :return:
        """
        self.load_settings()
        super(OptionForm, self).exec_()

    def get_help(self):
        webbrowser.open('https://gitee.com/py2cn/pyminer/wikis/%E9%85%8D%E7%BD%AEPyMiner?sort_id=3263840')


class AppstoreForm(QWidget, appStore_Ui_Form):
    def __init__(self):
        super(AppstoreForm, self).__init__()
        self.setupUi(self)
        self.center()

        self.browser = QWebEngineView()
        # 加载外部的web界面
        self.browser.load(QUrl('https://chrome.zzzmh.cn/index#ext'))
        self.horizontalLayout_2.addWidget(self.browser)

        self.toolButton_help.clicked.connect(self.main_help_display)

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

    def main_help_display(self):
        """
        打开帮助页面
        """
        try:
            webbrowser.get('chrome').open_new_tab("http://www.pyminer.com")
        except Exception as e:
            webbrowser.open_new_tab("http://www.pyminer.com")


class AboutForm(QWidget, About_Ui_Form):
    """
    关于 弹出框

    """

    def __init__(self):
        super(AboutForm, self).__init__()
        self.setupUi(self)
        self.center()
        AUTHOR = utils.get_settings_item_from_file("config.ini", "INFO/AUTHOR", "default")
        MAIL = utils.get_settings_item_from_file("config.ini", "INFO/MAIL", "default")
        self.textedit_about.setMarkdown("""# PyMiner
PyMiner 是一款基于Python的开源、跨平台数据分析环境。它以方便Python初学者为己任，在Python的知识理论和工作实践之间搭建桥梁，竭诚为初学者服务。
- PyMiner开箱即用，大大减少配置解释器环境的繁琐性。不仅提供了编程运行的功能，还能够以交互式的形式进行常见的数据分析操作，减少代码编写和文档查阅的时间。
- PyMiner通过加载各种插件实现不同的需求，开发者可以通过编写插件，将PyMiner扩展的更强大、更趁手，甚至创建一番自己的商用程序。
- PyMiner提供面向新手的快速入门教程，教程正由开发团队编写中。
- 我们诚挚希望与Python培训或教育机构/个人合作，让我们的产品帮助到更多学习Python的人。

作者：{AUTHOR}    

邮箱：{MAIL}
""".format(AUTHOR=AUTHOR, MAIL=MAIL))

        self.main_about_display()

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

    def main_about_display(self):
        """
        打开关于页面
        """
        import platform
        python_info = 'Python版本: ' + platform.python_version() + ' ' + platform.python_compiler()
        system_info = '系统信息: ' + platform.platform() + ' ' + platform.architecture()[0]
        cpu_info = 'CPU信息: ' + platform.processor()
        self.feedback.setPlainText(python_info + '\n' + system_info + '\n' + cpu_info)
        self.label_version_show.setText(utils.get_settings_item_from_file("config.ini", "INFO/VERSION", "default"))


class ProjectWizardForm(QWizard, Project_Ui_Form):
    """
    新建项目引导窗口
    """

    def __init__(self, parent=None):
        super(ProjectWizardForm, self).__init__(parent=None)
        self.setupUi(self)
        self.center()
        self.default_setting()
        self.init()

    def init(self):
        # 初始化项目路径
        project_name = self.projectNameLineEdit.text()
        workspace_dir = os.path.join(os.path.expanduser('~'), 'PyMiner_workspace', project_name)
        file_dir = os.path.join(os.path.expanduser('~'), 'PyMiner_workspace', project_name, 'main.py')
        self.projectDirectoryEditLine.setText(workspace_dir)
        self.absoluteDirectoryEditLine.setText(file_dir)

        # 浏览按钮触发事件
        self.toolButton.clicked.connect(self.getProjectDirectory)
        # 向导界面finish按钮按下后触发的事件
        self.button(QWizard.FinishButton).clicked.connect(self.finishWizard)
        # 项目名称框text发生改变时触发的事件
        self.projectNameLineEdit.textChanged.connect(self.projectNameLineEditTextChange)
        # 选择不同项目类型时下方展示不同的类型描述
        self.file_list.itemClicked.connect(self.fileListItemClicked)

    def getProjectDirectory(self):
        """
        浏览按钮触发的事件，选择文件夹
        :return:
        """
        absolute_directory = self.absoluteDirectoryEditLine.text()
        project_directory = self.projectDirectoryEditLine.text()
        directory_name = QFileDialog.getExistingDirectory(None, "请选择文件夹路径", "./").replace("/", "\\")
        self.projectDirectoryEditLine.setText(directory_name)
        project_name = self.projectNameLineEdit.text()
        if len(project_name) != 0:
            if len(directory_name) != 0:
                self.absoluteDirectoryEditLine.setText(directory_name + "\\" + project_name + '\\main.py')
                self.projectDirectoryEditLine.setText(directory_name + "\\" + project_name)
            else:
                self.absoluteDirectoryEditLine.setText(absolute_directory)
                self.projectDirectoryEditLine.setText(project_directory)
        else:
            if len(directory_name) != 0:
                self.absoluteDirectoryEditLine.setText(directory_name + "\\" + project_name + '\\main.py')
                self.projectDirectoryEditLine.setText(directory_name + "\\" + project_name)
            else:
                self.absoluteDirectoryEditLine.setText(absolute_directory)
                self.projectDirectoryEditLine.setText(project_directory)
        project_directory = self.projectDirectoryEditLine.text()
        if project_directory != "" and os.path.exists(project_directory):
            # 警告：该项目已存在，完成向导后原来的项目将会被覆盖！！！
            self.warningLabel.adjustSize()
            self.warningLabel.setText("Warning: The project already exists, the original \nproject will be overwritten "
                                      "after completing the \nwizard! ! !")
        else:
            self.warningLabel.setText("")

    def finishWizard(self):
        """
        完成项目创建向导后做的动作，文件夹不存在时创建路径并创建空的main.py文件，文件存在时只创建main.py，然后在主窗口中打开
        :return:
        """
        import os
        import pathlib
        file_path = self.absoluteDirectoryEditLine.text()
        project_path = self.projectDirectoryEditLine.text()
        current_project_type = self.file_list.currentRow()
        if os.path.exists(project_path):
            if current_project_type != 3:  # Python-Template-PySide2
                pathlib.Path(file_path).touch()  # 创建空文件
            else:
                from shutil import rmtree
                rmtree(project_path)
        else:
            if current_project_type != 3:  # Python-Template-PySide2
                os.mkdir(project_path)
                pathlib.Path(file_path).touch()
        from shutil import copyfile
        if current_project_type == 0:  # Python-Empty  # 创建空项目
            template_dir = "features/project/template/Empty-Template.py"
            if os.path.exists(template_dir):
                copyfile(template_dir, file_path)
            else:  # 若模板文件不存在，默认新建空main.py
                with open(file_path, "w") as f:
                    f.write("# --coding:utf-8--\n")
                    f.write("")
        elif current_project_type == 1:  # Python-Template-Basic  # 创建base template项目
            template_dir = "features/project/template/Basic-Template.py"
            if os.path.exists(template_dir):
                copyfile(template_dir, file_path)
            else:  # 若模板文件不存在，默认将以下内容写入main.py
                with open(file_path, "w") as f:
                    f.write("# --coding:utf-8--\n")
                    f.write("if __name__ == '__main__':\n")
                    f.write("    # Create your codes here")
                    f.write("    pass")
        elif current_project_type == 2:  # Python-Template-Plot  # 创建plot template项目
            template_dir = "features/project/template/Plot-Template.py"
            if os.path.exists(template_dir):
                copyfile(template_dir, file_path)
            else:  # 若模板文件不存在，默认将以下内容写入main.py
                with open(file_path, "w") as f:
                    f.write("# --coding:utf-8--\n")
                    f.write("\n")
                    f.write("import matplotlib.pyplot as plt\n")
                    f.write("import numpy as np\n")
                    f.write("\n")
                    f.write("\n")
                    f.write("def demoTemplate():\n")
                    f.write("    x = np.linspace(0, 5, 200)\n")
                    f.write("    y1 = x + 1\n")
                    f.write("    y2 = x - 1\n")
                    f.write("    plt.figure()\n")
                    f.write("    ax = plt.axes()\n")
                    f.write("    ax.spines['top'].set_visible(False)\n")
                    f.write("    ax.spines['right'].set_visible(False)\n")
                    f.write("    plt.grid(axis='both', linestyle='-.', c='b')\n")
                    f.write("    plt.plot(x, y1, 'c--')\n")
                    f.write("    plt.plot(x, y2, 'r-.')\n")
                    f.write("    plt.text(1, 0.5, 'text')\n")
                    f.write("    plt.legend(['y1', 'y2'])\n")
                    f.write("    plt.xlabel('xlabel')\n")
                    f.write("    plt.ylabel('ylabel')\n")
                    f.write("    plt.title('title')\n")
                    f.write("    plt.show()\n")
                    f.write("\n")
                    f.write("\n")
                    f.write("if __name__ == '__main__':\n")
                    f.write("    demoTemplate()\n")
        elif current_project_type == 3:  # Python-Template-PySide2  # 创建pyqt template项目
            template_dir = "features/project/template/PySide2Template"
            if os.path.exists(template_dir):
                from shutil import copytree
                copytree(template_dir, project_path)
            else:  # 若模板文件不存在，默认将以下内容写入main.py
                QMessageBox.warning(self, "警告", "模板路径不存在，请确保模板在程序根目录下的features/project/template/PySide2Template",
                                    QMessageBox.Ok)
        extension_lib.Program.set_work_dir(project_path)  # 在文件树区域打开新建项目，将当前工作路径切换为新建的项目

    def projectNameLineEditTextChange(self):
        """
        项目名称发生改变时同步改变绝对路径
        Returns
        -------

        """
        project_name = self.projectNameLineEdit.text()
        absolute_directory = self.absoluteDirectoryEditLine.text()
        # 将文件路径按照\分割成列表，然后把右边2个元素也就是main.py与项目名称pop()移出列表，最后再拼接成完整的路径
        absolute_directory_list = absolute_directory.split("\\")
        absolute_directory_list.pop()  # 移除最右边的元素"main.py"
        absolute_directory_list.pop()  # 移除右边的项目名称元素
        if absolute_directory != "":
            # 将新项目名称和main.py与浏览按钮选择的路径进行拼接组合成新的绝对路径和项目路径
            self.projectDirectoryEditLine.setText("\\".join(absolute_directory_list) + "\\" + project_name)
            self.absoluteDirectoryEditLine.setText("\\".join(absolute_directory_list) + "\\" + project_name
                                                   + "\\main.py")
        project_dir = self.projectDirectoryEditLine.text()
        if os.path.exists(project_dir):
            # 警告：该项目已存在，完成向导后原来的项目将会被覆盖！！！
            self.warningLabel.setText("Warning: The project already exists, the original \nproject will be overwritten "
                                      "after completing the \nwizard! ! !")
        else:
            self.warningLabel.setText("")

    def fileListItemClicked(self):
        current_project_type = self.file_list.currentRow()
        if current_project_type == 0:  # Python-Empty
            self.plainTextEdit.setPlainText("Create a Python Project containing an Empty main.py.")
        elif current_project_type == 1:  # Python-Template-Basic
            self.plainTextEdit.setPlainText("Create a Python Project containing a Base Template main.py.")
        elif current_project_type == 2:  # Python-Template-Plot
            self.plainTextEdit.setPlainText("Create a Python Project containing a Plot Template main.py.")
        elif current_project_type == 3:  # Python-Template-PySide2
            self.plainTextEdit.setPlainText("Create a Python Project containing a PySide2 Template main.py.")

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

    def default_setting(self):
        item = self.file_list.item(1)
        item.setSelected(True)


class FirstForm(QDialog, first_Ui_Form):
    """
    快速操作窗口
    """

    def __init__(self, parent=None):
        super(FirstForm, self).__init__(parent)
        self.setupUi(self)
        self.center()
        self.setWindowOpacity(0.95)
        self.setWindowTitle(self.tr('Quick Start'))
        # self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Popup)  # 无边框、弹出式
        self.animation = None
        # self.setStyleSheet("border-radius:10px;border:none;")
        # self.setAttribute(Qt.WA_TranslucentBackground)

        # 绑定事件
        self.btn_open_python.clicked.connect(self.open_script)
        self.btn_manual.clicked.connect(self.open_manual)
        self.btn_website.clicked.connect(self.open_website)
        self.btn_source.clicked.connect(self.open_source)
        self.btn_member.clicked.connect(self.open_member)
        self.btn_donate.clicked.connect(self.open_donate)

        self.btn_open_csv.clicked.connect(self.open_csv)
        self.btn_open_excel.clicked.connect(self.open_excel)
        self.btn_open_matlab.clicked.connect(self.open_matlab)
        self.btn_open_folder.clicked.connect(self.open_folder)

    def closeEvent(self, event):
        if self.animation is None:
            self.animation = QPropertyAnimation(self, b'windowOpacity', self.parent())
            # self.animation.setPropertyName(b'windowOpacity')
            self.animation.setDuration(200)
            self.animation.setStartValue(self.windowOpacity())
            self.animation.setEndValue(0)
            self.animation.finished.connect(self.close)
            self.animation.start()
            event.ignore()

    def mouseMoveEvent(self, e: QMouseEvent):  # 重写移动事件
        self._endPos = e.pos() - self._startPos
        self.move(self.pos() + self._endPos)
        super(FirstForm, self).mouseMoveEvent(e)

    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._isTracking = True
            self._startPos = QPoint(e.x(), e.y())
        super(FirstForm, self).mousePressEvent(e)

    def mouseReleaseEvent(self, e: QMouseEvent):
        super(FirstForm, self).mouseReleaseEvent(e)
        if e.button() == Qt.LeftButton:
            self._isTracking = False
            self._startPos = None
            self._endPos = None

    def keyPressEvent(self, e):
        """
        按键盘Escape退出当前窗口
        @param e:
        """
        super(FirstForm, self).keyPressEvent(e)
        if e.key() == Qt.Key_Escape:
            self.close()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def open_script(self):
        user_home = os.path.expanduser('~')
        file_name, filetype = QFileDialog.getOpenFileName(self, "选取文件", user_home, "Python Files (*.py);;All Files (*)")
        self.hide()
        extension_lib.get_interface('code_editor').open_script(file_name)
        self.close()

    def open_manual(self):
        """
        打开快速入门
        :return:
        """
        utils.open_url("https://gitee.com/py2cn/pyminer/wikis/%E5%85%A5%E9%97%A8%E6%95%99%E7%A8%8B?sort_id=3137860")

    def open_website(self):
        """
        打开快速入门
        :return:
        """
        utils.open_url("http://www.pyminer.com")

    def open_source(self):
        """
        打开快速入门
        :return:
        """
        utils.open_url("https://gitee.com/py2cn/pyminer")

    def open_member(self):
        """
        打开 ‘加入我们’ 页面
        :return:
        """
        utils.open_url("https://gitee.com/py2cn/pyminer/wikis/%E8%81%94%E7%B3%BB%E6%88%91%E4%BB%AC?sort_id=2761039")

    def open_donate(self):
        """
        打开 ‘捐赠’ 页面
        :return:
        """
        utils.open_url("https://gitee.com/py2cn/pyminer/wikis/%E6%8D%90%E8%B5%A0?sort_id=2925146")

    def open_csv(self):
        """
        调用主程序打开csv到工作区间
        :return:
        """
        self.hide()
        extension_lib.get_interface('dataio').show_import_file_dialog('csv', '')
        self.close()

    def open_excel(self):
        """
        调用主程序打开excel到工作区间
        :return:
        """
        self.hide()
        extension_lib.get_interface('dataio').show_import_file_dialog('excel', '')
        self.close()

    def open_matlab(self):
        """
        调用主程序打开matlab到工作区间
        :return:
        """
        self.hide()
        extension_lib.get_interface('dataio').show_import_file_dialog('matlab', '')
        # get_main_window().process_file('matlab')
        self.close()

    def open_folder(self):
        user_home = os.path.expanduser('~')
        project_path = QFileDialog.getExistingDirectory(self, "选取文件夹", user_home)
        self.hide()
        extension_lib.Program.set_work_dir(project_path)
        self.close()


class LoginForm(QDialog, login_Ui_Form):
    """
    登录窗口
    """

    def __init__(self, parent=None):
        super(LoginForm, self).__init__(parent)
        self.setupUi(self)
        self.init()

    def init(self):
        self.loginButton.clicked.connect(self.login)
        self.forgetPwdButton.clicked.connect(self.forgetPwd)
        self.usernameLineEdit.textChanged.connect(self.usernameErrorChange)

    def login(self):
        username = self.usernameLineEdit.text()
        password = self.passwordLineEdit.text()
        flag = False
        if username == "":
            self.usernameError.setText("用户名不能为空")
            flag = True
        if password == "":
            self.passwordError.setText("密码不能为空")
            flag = True
        if not flag:
            data = {
                "usr": username,
                "password": base64.b64encode(password.encode())
            }
            url = http_client.API + http_client.LOGIN_URL
            resp = http_client.client(url, "post", data)
            resp_info = json.loads(resp.text)
            if resp.status_code == 200:
                if resp_info["code"] == 10000:
                    token = resp_info["token"]
                    token_len = len(token)
                    username_len = len(username.encode("utf-8"))
                    """
                    将登录后django返回的token令牌保存在共享内存token中，共享内存token在启动pyminer主程序时附带启动了本地flask服务然后
                    创建共享内存token，详情见lib/localserver/server.py
                    """
                    shared_memo = shared_memory.SharedMemory(name="sharedMemory")  # 通过name找到共享内存token
                    buff = shared_memo.buf
                    # token长度随着用户名长度的增加而增加，用户名最长为21个汉字加一个字符
                    # buff[:3]存放token长度，目前最长的用户名21汉字加一字符生成的token长度为343
                    # buff[3:5]存放用户名长度，用户名字段最长为64字节，最多21个汉字（字符集utf8）
                    # buff[5:token_len+5]位存放token
                    # buff[token_len+5:实际用户名长度（用utf8转换为bytes后的长度）]存放用户名
                    buff[:3] = str(token_len).encode("utf-8")  # 存放token长度
                    buff[3:5] = str(username_len).encode("utf-8")  # 将用户名长度存放共享内存
                    buff[5:token_len+5] = token.encode("utf-8")  # 将token存放进共享内存中，工作空间重启后也能获取到
                    buff[token_len+5:token_len+5+username_len] = username.encode("utf-8")  # 存放用户名
                    self.usernameError.setText("登录成功")
                    time.sleep(0.5)
                    self.close()
            else:
                self.usernameError.setText(resp_info["msg"][0])

    def forgetPwd(self):
        utils.open_url("http://pyminer.com/forgetpassword")

    def usernameErrorChange(self):
        self.usernameError.setText("")
        self.passwordError.setText("")
        username = self.usernameLineEdit.text()
        if len(username.encode("utf-8")) > 64:
            self.usernameError.setText("最多只能输入21个汉字")
            self.loginButton.setEnabled(False)
            self.loginButton.setCursor(QCursor(Qt.ForbiddenCursor))
        else:
            self.usernameError.setText("")
            self.loginButton.setEnabled(True)
            self.loginButton.setCursor(QCursor(Qt.PointingHandCursor))


class LoginedForm(QDialog, logined_Ui_Form):

    def __init__(self, parent=None):
        super(LoginedForm, self).__init__(parent)
        self.setupUi(self)
        self.init()
        shared_memo = shared_memory.SharedMemory(name="sharedMemory")  # 通过name找到共享内存token
        buff = shared_memo.buf
        token_len = int(bytes(buff[:3]).decode())
        username_len = int(bytes(buff[3:5]).decode())
        username = bytes(buff[token_len+5:token_len+5+username_len]).decode("utf-8")
        self.usernameLabel.setText(username)

    def init(self):
        self.loginOutButton.clicked.connect(self.logout)

    def logout(self):
        shared_memo = shared_memory.SharedMemory(name="sharedMemory")  # 通过name找到共享内存token
        buff = shared_memo.buf
        for i in range(0, len(buff)):
            buff[i:i + 1] = "\x00".encode()
        time.sleep(0.5)
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # form = FirstForm()
    form = LoginedForm()
    form.show()
    sys.exit(app.exec_())
