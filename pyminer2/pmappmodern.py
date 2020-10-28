"""
pmappmodern.py
作者：侯展意
主界面

主界面由一系列PMDockWidget组成，每一个DockWidget可以获取主界面。
1、注册工具栏的方法
主界面的工具栏使用的是okokPMToolBar这个类，继承自QToolBar，结构为1+n。最顶端的选项卡样控件实为QToolBar,可以依靠其按钮的点击来进行工具栏的切换。
切换工具栏时，其他工具栏隐藏，只有按钮对应的工具栏可以显示。详见switch_toolbar方法。
主窗口add_tool_bar()方法，可以将QToolBar或者继承它的控件添加到主窗口。

当需要在已有的工具栏上添加按钮的时候，比方说要获取主页对应的工具栏，那么就使用 MainWindow.toolbars.get('toolbar_home')进行获取就可以了。
获取工具栏后，调用add_tool_button()添加一个按钮，或者调用add_tool_buttons()添加多个竖排的按钮。这两个函数的返回值分别为QPushButton
和List[QPushButton]

如果需要菜单效果，可以自己写一个菜单，然后添加到按钮之上。
2、添加dockwidget的方法
MainWindow.add_widget_on_dock()方法可以用来将任意控件添加到dock,而且下次加载之时布局会被保存。

为了加快软件启动速度，widget可以定义方法setup_ui（也可以没有）。当加载时，首先执行控件的__init__,并且将setup_ui压入任务栈之中，等到主
界面显示出来之后再用定时器调用执行控件的setup_ui方法。对于核心控件可以定义show_directly=True，保证立即执行setup_ui方法。或者干脆不写
setup_ui方法，而是将启动方法放在__init__之中。

当dockwidget点击右上角按钮关闭的时候，它并不会被关闭，而是会被隐藏。

主窗口有一系列的子窗口是必备的(类似于MATLAB的内置窗口)，对启动速度敏感，所以不建议使用插件式安装：
1、插件管理器extension_panel
2、日志窗口log_output_console

4、表格控件table_widget
5、文件管理器file_tree_widget


插件建议继承PMToolBar类，这个类有设置好的样式。
from pyminer.ui.generalwidgets import PMToolBar
"""
import datetime
import getpass
import os
import sys
import time
import webbrowser
from typing import List, Callable
import logging

from PyQt5.QtCore import pyqtSignal, QTimer, Qt, QTranslator, QLocale, QSize
from PyQt5.QtGui import QCloseEvent, QTextCursor, QResizeEvent, QFontDatabase, QMoveEvent, QFont, QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QMenu, QTextEdit, QMessageBox, QToolBar, QSplashScreen, QFileDialog

from pyminer2.features.io import sample
from pyminer2.features import base
from pyminer2.features.io.settings import Settings
from pyminer2.ui.base.widgets.controlpanel import PMPageExt
from pyminer2.ui.pmwidgets import BaseMainWindow
from pmgwidgets import PMGToolBar, ActionWithMessage, PMDockObject
from pmgwidgets.sourcemgr import create_icon
from pyminer2.extensions.extensions_manager.manager import extensions_manager
from pyminer2.extensions.extensions_manager.log import ColorHandler
from pyminer2.pmutil import get_main_window, get_root_dir, get_application
from pyminer2.features.util import utils
from pyminer2.features.io.settings import load_theme

log_folder = os.path.join(get_root_dir(), 'log')
if not os.path.exists(log_folder):
    os.mkdir(log_folder)

logging.Formatter.default_msec_format = '%s.%03d'
logging_file = os.path.join(log_folder, f'log_{datetime.datetime.now().strftime("%Y-%m-%d")}.log')
logging.basicConfig(
    format='[%(asctime)s] %(levelname)-8s %(name)s [%(module)s:%(funcName)s:%(lineno)s] %(message)+8s',
    # filename=logging_file, 
    # filemode='a', 
    level=logging.DEBUG,
    handlers=[logging.FileHandler(logging_file, 'a', encoding='utf8'), ColorHandler()]
)

logger = logging.getLogger('pmapp')
logger.info('Program starts up')


class PMToolBarHome(PMGToolBar):
    """
    菜单工具栏按钮定义
    """

    def __init__(self):
        super().__init__()

        self.add_tool_button(
            'button_new_script','新建脚本',
            create_icon(":/color/source/theme/color/icons/script.svg"))

        self.add_tool_button(
            'button_new',
            '新建',
            create_icon(":/color/source/theme/color/icons/file.svg"))

        self.add_tool_button('button_open', '打开', create_icon(
            ":/color/source/theme/color/icons/open.svg"))

        self.add_buttons(2, ['button_search_for_files', 'button_compare_files'],
                         ['搜索', '比较'],
                         [":/color/source/theme/color/icons/search.svg",
                          ":/color/source/theme/color/icons/compare.svg"])

        self.addSeparator()

        self.add_tool_button(
            'button_import_data', '获取数据',
            create_icon(":/color/source/theme/color/icons/import.svg"))
        self.add_import_data_menus()

        self.add_tool_button(
            'button_import_database', '数据库导入',
            create_icon(":/color/source/theme/color/icons/import_database.svg"))

        self.add_tool_button(
            'button_save_workspace',
            '保存工作区间',
            create_icon(":/color/source/theme/color/icons/save_layout.svg"))

        self.add_buttons(3, ['button_new_variable', 'button_open_variable', 'button_clear_workspace'],
                         ['新建变量', '打开变量', '清除变量'],
                         [":/color/source/theme/color/icons/var.svg",
                          ":/color/source/theme/color/icons/var_open.svg",
                          ":/color/source/theme/color/icons/clear.svg"])

        self.addSeparator()
        self.add_tool_button(
            'button_settings',
            '设置',
            create_icon(':/color/source/theme/color/icons/setting.svg'))
        self.add_tool_button(
            'button_appstore',
            '应用商店',
            create_icon(':/color/source/theme/color/icons/appstore.svg'))
        self.add_tool_button('button_help', '帮助', create_icon(
            ':/color/source/theme/color/icons/help.svg'))
        self.add_tool_button('button_about', '关于', create_icon(
            ':/color/source/theme/color/icons/info.svg'))

        self.view_menu = QMenu()
        self.view_menu.triggered.connect(self.process_visibility_actions)

        buttons = self.add_buttons(2, ['view_config', 'Undefinedbtn123'], ['视图', ''])

        self.view_config_button = buttons[0]

    def process_visibility_actions(self, e: ActionWithMessage):
        """
        处理”视图“菜单点击时触发的事件。
        """
        main_window = get_main_window()
        dws = main_window.dock_widgets
        if e.message in ['load_standard_layout']:
            main_window.load_predefined_layout('standard')
        if e.message in dws.keys():
            dws[e.message].setVisible(e.isChecked())

    def bind_events(self):
        """
        绑定事件。
        """
        self.append_menu('button_new', '数据集',
                         lambda: print('数据集新建未集成'))

        self.get_control_widget('button_search_for_files').clicked.connect(lambda: print('查找文件：未做'))
        self.get_control_widget('button_search_for_files').setEnabled(False)
        self.get_control_widget('button_compare_files').clicked.connect(lambda: print('比较文件：未做'))
        self.get_control_widget('button_compare_files').setEnabled(False)
        # self.get_control_widget('button_import_data').clicked.connect(
        # lambda: get_main_window().main_open_data_chooseFile())
        self.get_control_widget('button_import_database').clicked.connect(
            lambda: get_main_window().import_database_display())
        self.get_control_widget('button_save_workspace').clicked.connect(lambda: print('保存工作区：未做'))
        self.get_control_widget('button_save_workspace').setEnabled(False)
        self.get_control_widget('button_new_variable').clicked.connect(lambda: print('新建变量：未做'))
        self.get_control_widget('button_new_variable').setEnabled(False)
        self.get_control_widget('button_open_variable').clicked.connect(lambda: print('打开变量：未做'))
        self.get_control_widget('button_open_variable').setEnabled(False)
        self.get_control_widget('button_clear_workspace').clicked.connect(lambda: print('清除工作区：未做'))
        self.get_control_widget('button_clear_workspace').setEnabled(False)
        self.get_control_widget('button_settings').clicked.connect(lambda: get_main_window().main_option_display())
        self.get_control_widget('button_appstore').clicked.connect(lambda: get_main_window().main_appstore_dispaly())
        self.get_control_widget('button_help').clicked.connect(lambda: get_main_window().main_help_display())
        self.get_control_widget('button_about').clicked.connect(lambda: get_main_window().main_about_display())

    def add_import_data_menus(self):
        excelImportIcon = create_icon(':/color/source/theme/color/icons/ExcelFile.png')
        self.append_menu('button_import_data', 'Excel导入', lambda: get_main_window().process_file('excel'),
                         excelImportIcon)
        textImportIcon = create_icon(':/color/source/theme/color/icons/txt.svg')
        self.append_menu('button_import_data', 'Text导入', lambda: get_main_window().process_file('text'),
                         textImportIcon)
        sasImportIcon = create_icon(':/color/source/theme/color/icons/sas.ico')
        self.append_menu('button_import_data', 'Sas导入', lambda: get_main_window().process_file('sas'),
                         sasImportIcon)
        spssImportIcon = create_icon(':/color/source/theme/color/icons/spss.svg')
        self.append_menu('button_import_data', 'SPSS导入', lambda: get_main_window().process_file('spss'),
                         spssImportIcon)


class LogOutputConsole(QTextEdit, PMDockObject):
    pass


class MainWindow(BaseMainWindow):
    setupui_tasks: List[Callable] = []
    boot_timer: QTimer = None
    close_signal = pyqtSignal()
    window_geometry_changed_signal = pyqtSignal()

    layouts_ready_signal = pyqtSignal()
    widgets_ready_signal = pyqtSignal()
    events_ready_signal = pyqtSignal()

    settings_changed_signal = pyqtSignal()

    @classmethod
    def __new__(cls, *args):
        if not hasattr(cls, 'instance'):
            instance = super().__new__(cls)
            cls.instance = instance
        return cls.instance

    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_option_form = base.OptionForm()

        import pyminer2.pmutil

        pyminer2.pmutil._main_window = self
        self.resize(1500, 850)
        self.setIconSize(QSize(40, 40))
        settings = Settings()

        root_dir = os.path.dirname(__file__)
        pyminer2.pmutil._root_dir = root_dir

        self.init_toolbar_tab()
        self.add_toolbar('toolbar_home', PMToolBarHome(), text='文件')
        self.setDockNestingEnabled(True)
        self.setWindowTitle('PyMiner')

        self.log_output_console = LogOutputConsole(self)

        self.add_widget_on_dock(
            'log_output_console',
            self.log_output_console,
            text='日志',
            side='right')

        self.extensions_manager = extensions_manager
        self.extensions_manager.load_from_extension_folder(updateSplashMsg)

        self.ext_manager_widget = PMPageExt(self)
        dw = self.add_widget_on_dock(
            'extension_panel',
            self.ext_manager_widget,
            text='插件管理',
            side='left')
        dw.setMaximumWidth(400)

        load_theme(settings['theme'])  # 组件都加载后再设置主题，否则可能有些组件不生效
        self.load_layout()
        self.show()

        self.switch_toolbar('toolbar_home')  # 启动完成时，将工具栏切换到‘主页’
        self.on_main_window_shown()

    def add_toolbar(self, name: str, toolbar: QToolBar,
                    text: str = 'untitled toolbar'):
        """
        添加一个工具栏。
        """
        b = self.top_toolbar_tab.add_button(text)
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

    def moveEvent(self, a0: 'QMoveEvent') -> None:
        self.window_geometry_changed_signal.emit()

    def resizeEvent(self, a0: QResizeEvent) -> None:
        """
        窗口大小调节，或者位置改变的信号。
        """
        self.size_restriction_acquire()
        super().resizeEvent(a0)
        self.delayed_call(500, self.size_restriction_release)
        self.window_geometry_changed_signal.emit()

    def on_settings_changed(self):
        self.settings_changed_signal.emit()

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
        """
        super().on_main_window_shown()
        self.boot_timer = QTimer()
        self.boot_timer.start(50)
        self.boot_timer.timeout.connect(self.on_boot_timer_timeout)
        self.layouts_ready_signal.emit()

    def import_database_display(self):
        """
        显示"从数据库导入"窗口
        """
        self.import_database = sample.ImportDatabase()
        # self.import_database.signal_data_change.connect(self.slot_dataset_reload)
        self.import_database.show()

    def main_appstore_dispaly(self):
        """
        显示"应用商店"窗口
        """
        self.appstore = base.AppstoreForm()
        # self.import_database.signal_data_change.connect(self.slot_dataset_reload)
        self.appstore.show()

    def main_option_display(self):
        """
        显示"选项"窗口
        """
        if self.main_option_form is None:
            self.main_option_form = base.OptionForm()
        # self.import_database.signal_data_change.connect(self.slot_dataset_reload)
        self.main_option_form.show()

    def process_file(self, type: str):
        if type is not None:
            if type == 'excel':
                utils.importutils.doExcelImport(self)
            elif type == 'sas':
                utils.importutils.doSASImport(self)
            elif type == 'spss':
                utils.importutils.doSPSSImport(self)
            elif type == 'text':
                utils.importutils.doTextImport(self)
            else:
                logging.info("type is not supported yet")
        else:
            logging.info('type is null')

    def main_help_display(self):
        """
        打开帮助页面
        """
        try:
            webbrowser.get('chrome').open_new_tab("http://www.py2cn.com")
        except Exception as e:
            webbrowser.open_new_tab("http://www.py2cn.com")

    def main_about_display(self):
        """
        打开关于页面,并将当前操作系统信息写入页面
        """
        self.about_me=base.AboutForm()
        self.about_me.show()

    def on_boot_timer_timeout(self):
        """
        启动时定时器溢出时执行的命令。
        """
        if len(self.setupui_tasks) > 0:
            task = self.setupui_tasks.pop(0)

            t0 = time.time()
            task()
            self.boot_timer.setInterval(int((time.time() - t0) * 1000))
        else:
            self.boot_timer.stop()
            self.widgets_ready_signal.emit()
            self.bind_events()
            self.events_ready_signal.emit()
            # [TODO]print('boot ended!')

    def closeEvent(self, a0: QCloseEvent) -> None:
        """
        主窗体退出时的事件，包括弹框提示等。Mac 上测试点击无法退出,修改为QMessageBox.Warning
        """
        reply = QMessageBox(QMessageBox.Warning, '关闭', '是否关闭！')
        reply.addButton('确定', QMessageBox.ActionRole)
        reply.addButton('取消', QMessageBox.RejectRole)
        if reply.exec_() == QMessageBox.RejectRole:
            a0.ignore()
            return
        else:
            a0.accept()
        """
        reply = QMessageBox.question(
            self,
            '注意',
            '确认退出吗？',
            QMessageBox.Ok | QMessageBox.Cancel,
            QMessageBox.Cancel)
        if reply == QMessageBox.Ok:
            a0.accept()
        else:
            a0.ignore()
            return
        """
        self.delete_temporary_dock_windows()
        self.save_layout()
        Settings.get_instance().save()
        self.close_signal.emit()
        self.extensions_manager.stop()
        for k in self.dock_widgets.keys():
            self.dock_widgets[k].widget().closeEvent(a0)
        super().closeEvent(a0)

    def slot_flush_console(self, level, module, content):
        """
        刷新主窗体执行情况日志
        :return:
        level:文本，warnning error info
        module:业务模块名称，例如 数据获取，数据处理，数据探索，统计，模型，可视化，评估
        """
        create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 日志记录时间
        user = getpass.getuser()
        msg = create_time + ' ' + user + ' ' + \
              level.upper() + ' [' + module + ']' + ':' + content
        if level == "error":
            html = "<a style='font-family:verdana;color:red;font-size:11;'>" + msg + "</a>"
        else:
            html = "<a style='font-family:verdana;color:black;font-size:11;'>" + msg + "</a>"

        console = self.log_output_console  # 由于代码重构，这里出现了不同。
        # [!TODO]应当创建方法，一次性的完成这个工作。
        console.moveCursor(QTextCursor.End)
        console.append(html)


def updateSplashMsg(ext_load_status: dict):
    splash = get_application().splash
    percent = '100%' if ext_load_status.get('ext_count') == 0 \
        else round(ext_load_status.get('loaded') / ext_load_status.get('ext_count') * 100)
    try:
        msg = '正在加载:' + ext_load_status.get('ext_name') + '...' + str(percent) + '%'
        splash.showMessage(msg, Qt.AlignHCenter | Qt.AlignBottom, Qt.black)
    except TypeError:
        return

def load_fonts(app):
    """
    注册字体文件
    """
    app.font_dir = path = os.path.join(os.path.dirname(__file__), 'ui', 'source', 'font')
    for name in os.listdir(path):
        QFontDatabase.addApplicationFont(os.path.join(path, name))
    font_db = QFontDatabase()


def load_translator(app):
    """
    加载翻译文件

    :param app:  QApplication
    :return:
    """
    # 注意需要保留trans变量的引用
    app.trans = QTranslator()
    app.trans.load(os.path.join(os.path.dirname(__file__), 'translations', 'qt_{0}.qm'.format(QLocale.system().name())))
    app.installTranslator(app.trans)


def main():
    from pyminer2 import pmutil
    app = QApplication(sys.argv)
    path_logo = os.path.dirname(os.path.abspath(__file__)) + r'\ui\source\icons\logo.png'
    app.setWindowIcon(QIcon(path_logo))  # 设置应用logo

    path_splash = os.path.dirname(os.path.abspath(__file__)) + r'\ui\source\images\splash.png'
    splash = QSplashScreen(QPixmap(path_splash))
    splash.showMessage("正在加载pyminer... 0%", Qt.AlignHCenter | Qt.AlignBottom, Qt.black)
    splash.show()  # 显示启动界面
    app.splash = splash

    pmutil._application = app
    load_fonts(app)
    load_translator(app)
    app.default_font = 'Deng'
    f = QFont(app.default_font, 10)
    app.setFont(f)
    demo = MainWindow()
    splash.finish(demo)  # 修复故障 I1VYVO 程序启动完成后,关闭启动界面   liugang 20200921
    id(demo)
    sys.exit(app.exec_())
