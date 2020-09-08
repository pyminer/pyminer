"""
pmappmodern.py
作者：侯展意
主界面

任务：将主界面中所有功能都迁移到目前的界面中去。

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
from typing import List, Callable, TYPE_CHECKING

from PyQt5.QtCore import pyqtSignal, QTimer, QThread
from PyQt5.QtGui import QCloseEvent, QTextCursor, QResizeEvent, QFontDatabase, QMoveEvent, QMouseEvent
from PyQt5.QtWidgets import QApplication, \
    QMenu, QTextEdit, QSizePolicy, QAction, QToolButton, QMessageBox

from pyminer2.extensions.extensions_manager.manager import extensions_manager
from pyminer2.pmutil import get_main_window
from pyminer2.ui.base.widgets.consolewidget import ConsoleWidget
from pyminer2.ui.base.widgets.controlpanel import PMPageData, PMPageExt
from pyminer2.ui.base.widgets.tablewidget import PMTableWidget
from pyminer2.ui.base.widgets.treeviews import PMDatasetsTreeview, PMFilesTree
from pyminer2.ui.generalwidgets import BaseMainWindow
from pyminer2.ui.generalwidgets import PMTabWidget
from pyminer2.ui.generalwidgets import PMToolBar, ActionWithMessage
from pyminer2.ui.generalwidgets.basicwidgets import PMPushButtonPane
from pyminer2.ui.generalwidgets.sourcemgr import create_icon
from pyminer2.workspace.datamanager.datamanager import data_manager
from pyminer2.workspace.dataserver.dataserver import DataServer

if TYPE_CHECKING:
    from pyminer2.extensions.packages.code_editor.editor import PMCodeEditTabWidget


# 继承QThread
class Runthread(QThread):
    #  通过类成员对象定义信号对象
    _signal = pyqtSignal(str)

    def __init__(self):
        super(Runthread, self).__init__()

    def __del__(self):
        self.wait()

    def run(self):
        self._signal.emit('')  # 注意这里与_signal = pyqtSignal(str)中的类型相同


class PMToolBarHome(PMToolBar):
    '''
    'button_new_script':'新建\n脚本'
    'button_new':'新建'
    'button_open':'打开'
    'button_import_data':'导入\n数据',
    'button_save_workspace':'保存\n工作区',
    'button_new_variable':'新建变量'
    'button_open_variable':'打开变量'
    'button_clear_workspace':'清除工作区'
    'button_search_for_files':'查找文件'
    'button_compare_files':'文件比较'
    'button_settings':'设置'
    'button_help': '帮助'
    'view_config':'视图'
    '''

    def __init__(self):
        super().__init__()

        self.add_tool_button(
            'button_new_script',
            '新建\n脚本',
            create_icon(":/pyqt/source/images/lc_newdoc.png"))

        self.add_tool_button(
            'button_new',
            '新建',
            create_icon(":/pyqt/source/images/New.png"))

        self.add_tool_button('button_open', '打开', create_icon(
            ":/pyqt/source/images/lc_open.png"))

        self.add_buttons(2, ['button_search_for_files', 'button_compare_files'], ['查找文件', '文件比较'],
                         [":/pyqt/source/images/lc_searchdialog.png", ":/pyqt/source/images/lc_pickthrough.png"])

        self.addSeparator()

        self.add_tool_button(
            'button_import_data',
            '导入\n数据',
            create_icon(":/pyqt/source/images/lc_dataimport.png"))
        self.add_tool_button(
            'button_save_workspace',
            '保存\n工作区',
            create_icon(":/pyqt/source/images/lc_save.png"))

        self.add_buttons(3, ['button_new_variable', 'button_open_variable', 'button_clear_workspace'],
                         ['新建变量', '打开变量', '清除工作区'],
                         [":/pyqt/source/images/lc_dbnewform.png", ":/pyqt/source/images/lc_open.png",
                          ":/pyqt/source/images/lc_dbclearquery.png"])

        self.addSeparator()
        self.add_tool_button(
            'button_settings',
            '设置',
            create_icon(':/pyqt/source/images/lc_config.png'))
        self.add_tool_button('button_help', '帮助', create_icon(
            ':/pyqt/source/images/lc_helpindex.png'))

        self.view_menu = QMenu()
        self.view_menu.triggered.connect(self.process_visibility_actions)

        buttons = self.add_buttons(2, ['view_config', 'Undefinedbtn123'], ['视图', ''])

        self.view_config_button = buttons[0]

    def process_visibility_actions(self, e: ActionWithMessage):
        main_window = get_main_window()
        dws = main_window.dock_widgets
        if e.message in ['load_standard_layout']:
            main_window.load_predefined_layout('standard')
        if e.message in dws.keys():
            dws[e.message].setVisible(e.isChecked())

    def bind_events(self):
        self.get_control_widget('button_new_script').clicked.connect(self.new_script)
        self.add_menu_to('button_new', ['数据集', '脚本'], [lambda: print('数据集新建未集成'), self.new_script])
        self.add_menu_to('button_open', ['脚本'], [self.open_script])
        self.get_control_widget('button_search_for_files').clicked.connect(lambda: print('查找文件：未做'))
        self.get_control_widget('button_compare_files').clicked.connect(lambda: print('比较文件：未做'))
        self.get_control_widget('button_import_data').clicked.connect(lambda: print('导入数据：未做'))
        self.get_control_widget('button_save_workspace').clicked.connect(lambda: print('保存工作区：未做'))
        self.get_control_widget('button_new_variable').clicked.connect(lambda: print('新建变量：未做'))
        self.get_control_widget('button_open_variable').clicked.connect(lambda: print('打开变量：未做'))
        self.get_control_widget('button_clear_workspace').clicked.connect(lambda: print('清除工作区：未做'))
        self.get_control_widget('button_settings').clicked.connect(lambda: print('设置：未做'))
        self.get_control_widget('button_help').clicked.connect(lambda: print('帮助：未做'))

    def open_script(self):
        editor: 'PMCodeEditTabWidget' = get_main_window().get_dock_widget('code_editor').widget()
        editor.open_file()

    def new_script(self):
        editor: 'PMCodeEditTabWidget' = get_main_window().get_dock_widget('code_editor').widget()
        editor.create_new_editor_tab()


class MainWindow(BaseMainWindow):
    setupui_tasks: List[Callable] = []
    boot_timer: QTimer = None
    close_signal = pyqtSignal()
    resize_signal = pyqtSignal()

    layouts_ready_signal = pyqtSignal()
    widgets_ready_signal = pyqtSignal()
    events_ready_signal = pyqtSignal()

    @classmethod
    def __new__(cls, *args):
        if not hasattr(cls, 'instance'):
            instance = super().__new__(cls)
            cls.instance = instance
        return cls.instance

    def __init__(self, parent=None):
        super().__init__(parent)
        self.load_settings()

        import pyminer2.pmutil
        pyminer2.pmutil._main_window = self
        root_dir = os.path.dirname(__file__)
        pyminer2.pmutil._root_dir = root_dir

        self.init_toolbar_tab()

        self.add_toolbar('toolbar_home', PMToolBarHome(), text='主页')

        self.setDockNestingEnabled(True)
        self.setWindowTitle('PyMiner')

        self.log_output_console = QTextEdit()

        ft = PMFilesTree(self)
        ft.size = (0.2, None)
        ft.get_size_hint = lambda: self.width() * 0.2
        self.add_widget_on_dock(
            'file_tree_widget',
            ft,
            text='文件浏览器')

        self.add_widget_on_dock(
            'log_output_console',
            self.log_output_console,
            text='日志输出',
            side='right')

        self.add_widget_on_dock(
            'table_panel',
            PMTableWidget(self),
            text='数据表格',
            side='top')

        self.add_widget_on_dock(
            'dataset_treeview_panel',
            PMDatasetsTreeview(self),
            text='数据集视图',
            side='left')

        tab_widget = PMTabWidget()

        self.data_control_page = PMPageData()
        tab_widget.addScrolledAreaTab(self.data_control_page, '数据分析')

        self.add_widget_on_dock(
            'function_panel',
            tab_widget,
            text='功能面板',
            side='left')

        self.extensions_manager = extensions_manager
        self.extensions_manager.load()
        self.tabifyDockWidget(
            self.dock_widgets['ipython_console'],
            self.dock_widgets['log_output_console'])

        self.ext_manager_widget = PMPageExt(self)
        dw = self.add_widget_on_dock(
            'extension_panel',
            self.ext_manager_widget,
            text='插件管理器',
            side='left')
        dw.setMaximumWidth(400)

        self.tabifyDockWidget(
            self.dock_widgets['extension_panel'],
            self.dock_widgets['function_panel'])

        # self.showMaximized()

        self.load_layout()  # 注掉或者删除配置文件之后，可以按照默认方式加载布局。

        self.show()

        self.switch_toolbar('toolbar_home')  # 启动完成时，将工具栏切换到‘主页’
        self.on_boot_finished()

        self.get_dock_widget('code_editor').setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding)

    def get_editor(self) -> 'PMCodeEditTabWidget':
        return self.get_dock_widget('code_editor').widget()

    def moveEvent(self, a0: 'QMoveEvent') -> None:
        self.resize_signal.emit()

    def resizeEvent(self, a0: QResizeEvent) -> None:

        self.size_restriction_acquire()

        super().resizeEvent(a0)
        self.delayed_call(500, self.size_restriction_release)
        self.resize_signal.emit()

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
        :return:
        """
        dw = self.get_dock_widget('file_tree_widget')
        if hasattr(dw.widget(),'get_size_hint'):
            dw.setMaximumWidth(int(dw.widget().get_size_hint()))
            dw.setMinimumWidth(int(dw.widget().get_size_hint()))
        dw2 = self.get_dock_widget('code_editor')
        dw2.setMinimumWidth(500)
        dw = self.get_dock_widget('function_panel')
        dw.setMaximumWidth(350)

        dw = self.get_dock_widget('workspace_inspector')
        dw.setMaximumWidth(300)
        dw.setMinimumWidth(280)

    def size_restriction_release(self):
        for w_name in self.dock_widgets.keys():
            self.dock_widgets[w_name].setMaximumWidth(100000)
            self.dock_widgets[w_name].setMaximumHeight(100000)
            self.dock_widgets[w_name].setMinimumHeight(0)
            self.dock_widgets[w_name].setMinimumWidth(0)

    def action_menu_new(self):
        print('new')

    def action_menu_open(self):
        print('open!')

    def on_boot_finished(self):
        import time
        print(time.time())
        super().on_boot_finished()
        self.boot_timer = QTimer()
        self.boot_timer.start(50)
        self.boot_timer.timeout.connect(self.on_boot_timer_timeout)
        self.layouts_ready_signal.emit()

    def on_boot_timer_timeout(self):
        if len(self.setupui_tasks) > 0:
            task = self.setupui_tasks.pop(0)

            t0 = time.time()
            task()
            print(
                'time elapsed %f for task %s!' %
                (time.time() - t0, repr(task)))
            # self.boot_timer.setInterval(int((time.time() - t0) * 1000))
        else:
            self.boot_timer.stop()
            self.widgets_ready_signal.emit()
            self.bind_events()
            self.events_ready_signal.emit()
            print('boot ended!')

    def get_toolbar_list(self):
        pass

    def closeEvent(self, a0: QCloseEvent) -> None:
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
        self.save_layout()
        self.save_settings()
        from pyminer2.extensions import PluginInterface
        self.close_signal.emit()
        PluginInterface.get_console().closeEvent(a0)
        PluginInterface.get_editor().closeEvent(a0)
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


def load_fonts():
    """
    注册字体文件
    """
    path = 'pyminer2/ui/source/font'
    for name in os.listdir(path):
        QFontDatabase.addApplicationFont(os.path.join(path, name))
    font_db = QFontDatabase()


def main():
    data_server = DataServer(data_manager, 'localhost', 8783)
    data_server.start()
    app = QApplication(sys.argv)
    load_fonts()
    demo = MainWindow()
    id(demo)
    sys.exit(app.exec_())
