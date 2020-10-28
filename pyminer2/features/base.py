import os
import sys
import webbrowser
from typing import Tuple, List

import qdarkstyle
from PyQt5.Qt import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QFileDialog, QApplication, QDialog
from pmgwidgets import SettingsPanel

from pyminer2.ui.base.option import Ui_Form as Option_Ui_Form
from pyminer2.ui.base.appStore import Ui_Form as appStore_Ui_Form
from pyminer2.ui.base.aboutMe import Ui_Form as About_Ui_Form
from pyminer2.features.io.settings import Settings


class OptionForm(QWidget, Option_Ui_Form):
    """
    打开"选项"窗口
    """
    signal_settings_changed = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)
        from pyminer2.pmutil import get_main_window
        self.setupUi(self)
        self.center()

        # 通过combobox控件选择窗口风格
        self.comboBox_theme.activated[str].connect(self.change_theme)

        self.setting = dict()

        self.listWidget.currentRowChanged.connect(self.option_change)
        self.toolButton_workspace.clicked.connect(self.slot_change_workspace)
        self.lineEdit_workspace.setReadOnly(True)
        self.toolButton_output.clicked.connect(self.slot_change_output)
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_ok.clicked.connect(self.close)

        new_settings = [('line_edit', 'dataserver_address', 'Data Server Address', 'http://localhost:8888'),
                        ('number', 'dataserver_port', 'Data Server Port', 12000, '', (0, 65535)),
                        ('bool', 'save_layout_on_close', 'Save Layout On Close', True),
                        ('choose_box', 'theme', 'Theme', 'Fusion',
                         ['Fusion', 'Qdarkstyle', 'windows', 'windowsvista'])]

        self.add_settings_panel('网络端口设置面板', new_settings)

    def add_settings_panel(self, text: str, settings_content: List):
        settings_widget = SettingsPanel(views=settings_content)
        self.signal_settings_changed.connect(settings_widget.on_settings_changed)
        self.stackedWidget.addWidget(settings_widget)
        self.listWidget.addItem(QListWidgetItem(text))
        return settings_widget

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

    def change_theme(self, style):
        from pyminer2.features.io.settings import load_theme
        load_theme(style)
        self.refresh_settings()

    def slot_change_workspace(self):
        directory = QFileDialog.getExistingDirectory(self, "选择工作区间位置", os.path.expanduser('~'))
        if not directory == '':
            self.lineEdit_workspace.setText(directory)

    def slot_change_output(self):
        directory = QFileDialog.getExistingDirectory(self, "选择输出文件夹位置", os.path.expanduser('~'))
        self.lineEdit_output.setText(directory)

    def load_settings(self):
        """
        在show()之前调用这个方法
        从而每次重新显示的时候都可以刷新数据。
        :return:
        """
        settings = Settings.get_instance()
        if settings.get('theme') is not None:
            for i in range(self.comboBox_theme.count()):
                if self.comboBox_theme.itemText(i) == settings['theme']:
                    self.comboBox_theme.setCurrentIndex(i)
        self.lineEdit_workspace.setText(settings['work_dir'])

    def refresh_settings(self):
        """
        窗口关闭时，调用此方法，刷新主界面设置项。
        :return:
        """
        settings = Settings.get_instance()
        settings['work_dir'] = self.lineEdit_workspace.text()
        settings['theme'] = self.comboBox_theme.currentText()
        from pyminer2.pmutil import get_main_window
        get_main_window().on_settings_changed()
        self.signal_settings_changed.emit()

    def show(self):
        """
        重写此方法，在显示之前重新加载一遍设置。
        :return:
        """
        self.load_settings()
        super(OptionForm, self).show()


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
            webbrowser.get('chrome').open_new_tab("http://www.py2cn.com")
        except Exception as e:
            webbrowser.open_new_tab("http://www.py2cn.com")

class AboutForm(QWidget, About_Ui_Form):
    def __init__(self):
        super(AboutForm, self).__init__()
        self.setupUi(self)
        self.center()

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = AppstoreForm()
    form.show()
    sys.exit(app.exec())
