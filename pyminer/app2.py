"""
作者：PyMiner开发组
启动方式：在app2的根目录下，运行：python app2.py。其中python和app2.py应当使用绝对路径。
命令行的调出：在Windows系统，启动后会自动隐藏命令行窗口。若要保持命令行窗口的显示，请使用-d选项：
         python.exe app2.py -d
"""

import cgitb
import ctypes
import datetime
import getpass
import logging
import os
import platform
import sys
import time
import traceback
from multiprocessing import shared_memory
sys.path.append(os.path.dirname(__file__))

import utils
sys.path.append(utils.get_resources_dir())



os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = utils.get_pysideplugins_directory()
os.environ['QT_API'] = 'pyside2'
os.environ['PYQTGRAPH_QT_LIB'] = 'PySide2'
os.environ['FORCE_QT_API'] = "1"

from typing import List, Callable, Tuple, ClassVar, Optional
from PySide2.QtCore import Signal, QTimer, Qt, QCoreApplication
from PySide2.QtGui import QCloseEvent, QCursor, QTextCursor, QResizeEvent, QMoveEvent, QFont, QIcon, QPixmap
from PySide2.QtWidgets import QApplication, QMessageBox, QSplashScreen, QStatusBar, QDialog, QVBoxLayout, QProgressBar
import widgets

widgets.in_unit_test = lambda: False
from widgets import PMGToolBar

from lib.extensions.extensions_manager.manager import extensions_manager
from lib.main_window import base
from lib.io.settings import load_theme
from lib.interpretermanager.interpretermanager import InterpreterManagerWidget

from lib.feedback import FeedbackClient
from lib.ui.widgets.controlpanel import PMPageExt
from lib.ui.pmwidgets import BaseMainWindow
from lib.pluginsmanager.pluginsmanager import MarketplaceForm
from load_modules import load_translator, load_fonts
from lib.ui.ui_main_window import PMToolBarHome

t0 = time.time()
from lib.localserver import server

# TODO:实例化server需要消耗

logging.info('Program starts up')

if "-debug" in sys.argv:
    for l in sys.argv:
        if l == '-debug' or l == '-d':
            print('debug')
            logging.basicConfig(level=logging.DEBUG)


def updateSplashMsg(ext_load_status: dict):
    splash = utils.get_application().splash
    percent = '100%' if ext_load_status.get('ext_count') == 0 \
        else round(ext_load_status.get('loaded') / ext_load_status.get('ext_count') * 100)
    try:
        msg = 'Loading:' + ext_load_status.get('ext_name') + '...' + str(percent) + '%'
        splash.showMessage(msg, Qt.AlignHCenter | Qt.AlignBottom, Qt.white)
    except TypeError:
        return


def try_hide_terminal():
    if '-debug' not in sys.argv and '-d' not in sys.argv :
        if platform.system().lower() == 'windows':
            whnd = ctypes.windll.kernel32.GetConsoleWindow()
            if whnd != 0:
                ctypes.windll.user32.ShowWindow(whnd, 0)
                ctypes.windll.kernel32.CloseHandle(whnd)


class MainWindow(BaseMainWindow):
    setupui_tasks: List[Callable] = []
    boot_timer: QTimer = None
    close_signal = Signal()
    window_geometry_changed_signal = Signal()

    layouts_ready_signal = Signal()
    widgets_ready_signal = Signal()
    events_ready_signal = Signal()

    settings_changed_signal = Signal()

    @classmethod
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            instance = super().__new__(cls, *args, **kwargs)
            cls.instance = instance
        return cls.instance

    def __init__(self, parent=None, extensions: Optional[List[str]] = None):
        """主程序

        Args:
            parent: 父窗口，由于是主程序，始终是None
            extensions: 如果指定，则仅加载指定的插件，否则加载全部插件
        """
        super().__init__(parent)
        # self.setWindowFlags(Qt.FramelessWindowHint)  # 无边框
        self.extension_names = extensions  # 需要加载的插件名称
        # settings = Settings()
        t00 = time.time()
        self.main_option_form = base.OptionForm()
        self.project_wizard: base.ProjectWizardForm = None
        self.settings_changed_signal.connect(self.on_settings_changed)
        self.main_option_form.add_page(self.tr('Interpreter'), InterpreterManagerWidget())

        utils._main_window = self



        # 设置主窗体标题
        self.setWindowTitle('PyMiner ' + utils.get_settings_item_from_file("config.ini", "INFO/VERSION", "default"))

        # 设置状态栏
        self.statusBar = QStatusBar()
        version = utils.get_python_version()
        self.statusBar.showMessage(version, 0)
        self.setStatusBar(self.statusBar)

        self.init_toolbar_tab()
        tb_home = PMToolBarHome()
        self.add_toolbar('toolbar_home', tb_home, text=tb_home.get_toolbar_text())
        self.setDockNestingEnabled(True)



        # 加载插件
        self.extensions_manager = extensions_manager
        if self.extension_names is None:
            self.extensions_manager.load_from_extension_folder(updateSplashMsg)
        else:
            for name in self.extension_names:
                self.extensions_manager.load(name)

        self.ext_manager_widget = PMPageExt(self)
        dw = self.add_widget_on_dock(
            'extension_panel',
            self.ext_manager_widget,
            text=self.tr('Plugs'),
            side='left')
        dw.setMaximumWidth(400)

        # 设置主题 ，组件都加载后再设置主题，否则可能有些组件不生效
        settings = utils.get_settings_from_file("config.ini")
        load_theme(settings.value("MAIN/THEME"))

        self.show()
        self.load_layout()
        self.switch_toolbar('toolbar_home')  # 启动完成时，将工具栏切换到‘主页’

        self.on_main_window_shown()
        self.start_localserver()  # 只要在插件加载完成之后启动就行，目前放在最后


        t01 = time.time()
        logging.debug('Time Elapsed for loading main window contents: %f' % (t01 - t00))

    def closeEvent(self, a0: QCloseEvent) -> None:
        """
        主窗体退出时的事件，包括弹框提示等。Mac 上测试点击无法退出,修改为QMessageBox.Warning
        """
        reply = QMessageBox(QMessageBox.Warning, self.tr('Close'), self.tr('Are you sure close?'))
        reply.addButton(self.tr('OK'), QMessageBox.ActionRole)
        reply.addButton(self.tr('Cancel'), QMessageBox.RejectRole)
        if reply.exec_() == QMessageBox.RejectRole:
            a0.ignore()
            return
        else:
            a0.accept()
        self.delete_temporary_dock_windows()
        self.save_layout()  # TODO:PySide2上存储布局有问题。
        self.close_signal.emit()
        self.extensions_manager.stop()
        for k in self.dock_widgets.keys():
            self.dock_widgets[k].widget().closeEvent(a0)
        super().closeEvent(a0)

    def mousePressEvent(self, event):
        if event.button()==Qt.LeftButton:
            self.m_flag=True
            self.m_Position=event.globalPos()-self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos()-self.m_Position)
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag=False
        self.setCursor(QCursor(Qt.ArrowCursor))

    def mouseDoubleClickEvent(self, event):
        self.window_maximum()
        event.accept()  # 接受事件，禁止传到父控件


    def moveEvent(self, a0: 'QMoveEvent') -> None:
        self.window_geometry_changed_signal.emit()

    def start_localserver(self):
        """启动本地flask服务器localserver"""
        server.server_thread.start()

    def clear_workspace(self):
        from lib.extensions.extensionlib.extension_lib import extension_lib
        extension_lib.get_interface('ipython_console').run_command('Clearing_Variables_ =\'Clear All\'',
                                                                   hint_text=self.tr('Start Clear...'), hidden=False)
        extension_lib.get_interface('ipython_console').run_command('get_ipython().clear_all()',
                                                                   hint_text=self.tr('Clear all variables'),
                                                                   hidden=False)

    def add_toolbar(self, name: str, toolbar: PMGToolBar,
                    text: str = 'untitled toolbar'):
        """
        添加一个工具栏。
        """
        if toolbar.insert_after() == '':
            b = self.top_toolbar_tab.add_button(name, text)
        else:
            b = self.top_toolbar_tab.insert_button(name, text, toolbar.insert_after())
        toolbar.tab_button = b
        b.clicked.connect(lambda: self.on_toolbar_switch_button_clicked(name))

        if hasattr(self, 'toolbar_path'):
            self.insertToolBar(self.toolbar_path, toolbar)
            self.insertToolBarBreak(self.toolbar_path)
        else:
            self.addToolBarBreak(Qt.TopToolBarArea)
            self.addToolBar(toolbar)
        toolbar.setObjectName(name)
        self.toolbars[name] = toolbar
        toolbar.setMovable(False)
        toolbar.setFloatable(False)

        if self._current_toolbar_name != '':
            self.refresh_toolbar_appearance()

    def resizeEvent(self, a0: QResizeEvent) -> None:
        """
        窗口大小调节，或者位置改变的信号。
        Window size adjustment, or a signal of a change in position.
        """
        self.size_restriction_acquire()
        super().resizeEvent(a0)
        self.delayed_call(500, self.size_restriction_release)
        self.window_geometry_changed_signal.emit()

    def on_settings_changed(self):
        """
        当设置项发生改变时，加载这些设置项。
        Returns:

        """
        load_theme(utils.get_settings_from_file("config.ini").value("MAIN/THEME"))

    def delayed_call(self, time_ms: int, callback: Callable) -> None:
        """
        封装了QTimer.SingleShot
        :param time_ms:
        :param callback:
        :return:
        """
        timer = QTimer()
        timer.singleShot(time_ms, callback)

    def size_restriction_acquire(self) -> None:
        """
        设置插件尺寸的最大值。
        控件需要指定get_split_portion_hint才可以。
        :return:
        """
        for k in self.dock_widgets.keys():
            dw = self.dock_widgets[k]
            horizontal_portion_hint = dw.widget().get_split_portion_hint()[0]
            if horizontal_portion_hint is not None:
                dw.setMaximumWidth(int(self.width() * horizontal_portion_hint))
                dw.setMinimumWidth(int(self.width() * horizontal_portion_hint))

    def size_restriction_release(self):
        for w_name in self.dock_widgets.keys():
            self.dock_widgets[w_name].setMaximumWidth(100000)
            self.dock_widgets[w_name].setMaximumHeight(100000)
            self.dock_widgets[w_name].setMinimumHeight(0)
            self.dock_widgets[w_name].setMinimumWidth(0)

    def on_main_window_shown(self):
        """
        在界面显示后触发的事件。
        Returns: None
        """
        t0 = time.time()
        super().on_main_window_shown()

        self.layouts_ready_signal.emit()
        for task in self.setupui_tasks:
            task()
        self.widgets_ready_signal.emit()
        t1 = time.time()
        logging.info('Layout ready time elapsed:%f' % (t1 - t0))
        self.set_dock_titlebar_visible(utils.get_settings_item_from_file("config.ini", "MAIN/DOCK_TITLEBAR_VISIBLE"))
        self.bind_events()
        self.events_ready_signal.emit()
        t2 = time.time()
        logging.info('Events ready, time elapsed:%f' % (t2 - t1))

    def first_form_display(self):
        """
        显示"快速操作"窗口
        Displays the "Quick Action" window
        """
        self.main_first_form = base.FirstForm(parent=self)
        self.main_first_form.show()

    def login_form_display(self):
        """
        显示"登录"窗口
        Displays the "Login In" window
        """
        shared_memo = shared_memory.SharedMemory(name="sharedMemory")  # 通过name找到共享内存token
        buff = shared_memo.buf
        token = bytes(buff[:199]).decode().replace("\x00", "")
        if token != "":
            self.main_login_form = base.LoginedForm(parent=self)
            self.main_login_form.exec_()
        else:
            self.main_login_form = base.LoginForm(parent=self)
            self.main_login_form.show()

    def main_appstore_dispaly(self):
        """
        显示"应用商店"窗口
        Displays the "App Store" window
        """
        self.appstore = MarketplaceForm()
        self.appstore.show()

    def main_option_display(self):
        """
        显示"选项"窗口
        """
        if self.main_option_form is None:
            self.main_option_form = base.OptionForm()
        self.main_option_form.exec_()

    def main_help_display(self):
        """
        打开帮助页面
        """
        utils.open_url("https://gitee.com/py2cn/pyminer/wikis")

    def main_check_update_display(self):
        """
        打开'检查更新'页面
        """
        dlg = QDialog()
        dlg.setLayout(QVBoxLayout())
        proc = QProgressBar()
        dlg.layout().addWidget(proc)
        dlg.setWindowTitle("请稍等，正在进行更新检查")
        dlg.setFixedWidth(500)
        proc.setRange(0, 0)  # 设置进度条忙

        def close(b):
            if b:
                dlg.close()
            else:
                dlg.close()
                QMessageBox.information(self, "更新提示", "已经是最新版，无需更新！")



        dlg.exec_()

    def main_install_update(self):
        closed = self.close()
        if closed:
            from widgets import run_python_file_in_terminal
            path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'update', 'update.py')
            run_python_file_in_terminal(path + ' -i')

    def main_feedback_display(self):
        """
        打开'反馈'页面
        """
        FeedbackClient()
        # reply = QMessageBox.information(self, self.tr('Feedback'), self.tr(
        #     'You can give feedback through issue on suggestions or problems encountered in use'),
        #                                 QMessageBox.Yes | QMessageBox.No,
        #                                 QMessageBox.Yes)
        # if reply == QMessageBox.Yes:
        #     utils.open_url("https://gitee.com/py2cn/pyminer/issues")

    def main_homesite_display(self):
        """
        打开官方网站页面
        """
        utils.open_url("http://www.pyminer.com")

    def main_markdown_display(self):
        pass
        # TODO 添加markdown编辑器代码

    def main_new_script_display(self):
        from lib.extensions.extensionlib.extension_lib import extension_lib
        extension_lib.get_interface('code_editor').open_script('')

    def main_community_display(self):
        """
        打开帮助页面
        """
        utils.open_url("https://www.kuxai.com/")

    def main_project_wizard_display(self):
        """
        打开新建项目向导
        """
        self.wizard = project_wizard = base.ProjectWizardForm(parent=self)
        project_wizard.exec_()

    def main_about_display(self):
        """
        打开关于页面,并将当前操作系统信息写入页面
        """
        self.about_me = base.AboutForm()
        self.about_me.show()

    def slot_flush_console(self, level: str, module, content):
        """刷新主窗体执行情况日志

        Args:
            level: 报错级别，包括 ``info`` , ``warnning`` , ``error`` 。
            module: 业务模块名称，例如 数据获取，数据处理，数据探索，统计，模型，可视化，评估
            content: 具体显示的内容
        """
        create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 日志记录时间
        user = getpass.getuser()
        msg = create_time + ' ' + user + ' ' + level.upper() + ' [' + module + ']' + ':' + content
        if level == "error":
            html = "<a style='font-family:verdana;color:red;font-size:11;'>" + msg + "</a>"
        else:
            html = "<a style='font-family:verdana;color:black;font-size:11;'>" + msg + "</a>"

        console = self.log_output_console  # 由于代码重构，这里出现了不同。
        console.moveCursor(QTextCursor.End)
        console.append(html)


def main(
        test_function: Callable[[MainWindow], None] = None,
        extensions: Optional[List[str]] = None,
        show_welcome=True,
):
    """启动主程序

    Args:
        test_function: 测试函数
        extensions: 需要加载的插件名
        show_welcome: 是否显示欢迎屏
    """
    global t0


    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)  # 设置应用支持高分屏
    app = QApplication.instance() if QApplication.instance() is not None else QApplication(sys.argv)
    app.setWindowIcon(QIcon(':/resources/logo/logo.png'))  # 设置应用logo

    # 设置启动画面
    splash_image = QPixmap(':/resources/images/splash_v2.png')
    splash_image = splash_image.scaled(700, 400)
    splash = QSplashScreen(splash_image)
    splash.show()  # 显示启动界面
    try_hide_terminal()  # 试图隐藏终端
    app.splash = splash

    utils._application = app

    # 设置字体
    load_fonts(app)
    app.default_font = 'Deng'
    f = QFont(app.default_font, 10)
    app.setFont(f)

    # 设置翻译
    load_translator(app)

    # 启动主程序
    window = MainWindow(extensions=extensions)

    t1 = time.time()

    # 启动画面结束
    splash.finish(window)

    if test_function is None:
        # 展示快速启动窗口。只有在设置为True的情况下才显示起始页。
        if show_welcome:
            if utils.get_settings_item_from_file("config.ini", "MAIN/SHOW_START_PAGE"):
                window.first_form_display()
    else:
        test_function(window)
    logging.info('boot time elapsed:%f s' % (t1 - t0))
    logging.info('boot finished at time:' + time.strftime('%H:%M:%S', time.localtime()) + '+%f s' % (
            time.time() - int(time.time())))
    res = app.exec_()
    logging.debug("Shutting down, result %d", res)
    logging.shutdown()

    sys.exit(res)


if __name__ == '__main__':
    logging.info('preload_module_time %f' % (time.time() - t0))
    main()
