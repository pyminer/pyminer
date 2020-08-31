'''
pmappmodern.py
作者：侯展意
主界面

√任务：写出显示浮动窗口数量的部件（下拉式菜单等），点击之后，可以进行浮动窗口显示或者隐藏。

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
3、控制台console_widget
4、表格控件table_widget
5、文件管理器file_tree_widget
另有以下界面可以用插件，但是此插件几乎是必备的。
1、文本编辑器editor_widget

'''
import datetime
import getpass
import os
import sys
import threading
import time

from PyQt5.QtCore import pyqtSignal, Qt, QTimer, QThread
from PyQt5.QtGui import QIcon, QPixmap, QFont, QCloseEvent, QTextCursor
from PyQt5.QtWidgets import QHBoxLayout, QDockWidget, QMainWindow, QPushButton, QApplication, \
    QWidget, QToolBar, QAction, QVBoxLayout, QMenu, QToolButton, QMessageBox, QStackedWidget, QTabWidget, QTextEdit
from typing import List, Dict, Callable

from pyminer.ui.base.widgets.generalwidgets.containers import PMTabWidget
from pyminer.ui.base.widgets.generalwidgets.containers.pmscrollarea import PMScrollArea
from pyminer.ui.base.widgets.generalwidgets.sourcemgr import create_icon
from pyminer.ui.base.widgets.generalwidgets.buttons import PushButtonPane
from pyminer.ui.base.widgets.generalwidgets.window import PMDockWidget, BaseMainWindow
from pyminer.ui.base.widgets.generalwidgets.toolbars import PMToolBar, ActionWithMessage

from pyminer.ui.base.widgets.treeviews import PMFilesTreeview, PMDatasetsTreeview
from pyminer.ui.base.widgets.consolewidget import ConsoleWidget
from pyminer.ui.base.widgets.controlpanel import PMPageData, PMPageExt
from pyminer.ui.base.widgets.codeeditwidget import PMCodeEditTabWidget
from pyminer.ui.base.widgets.tablewidget import PMTableWidget

from pyminer.features.extensions.extensions_manager.manager import extensions_manager
from pyminer.pmutil import get_main_window, get_root_dir


# 继承QThread
class Runthread(QThread):
    #  通过类成员对象定义信号对象
    _signal = pyqtSignal(str)

    def __init__(self):
        super(Runthread, self).__init__()

    def __del__(self):
        self.wait()

    def run(self):
        # for i in range(100):
        #     time.sleep(0.2)
        self._signal.emit('')  # 注意这里与_signal = pyqtSignal(str)中的类型相同


class PMToolBarHome(PMToolBar):
    def __init__(self):
        super().__init__()

        self.add_tool_button('新建\n脚本', create_icon(":/pyqt/source/images/lc_newdoc.png"))
        self.add_tool_button('新建', create_icon(":/pyqt/source/images/New.png"))
        self.add_tool_button('打开', create_icon(":/pyqt/source/images/lc_open.png"))
        pp = PushButtonPane()
        pp.add_buttons(2, ['查找文件', '文件比较'],
                       [":/pyqt/source/images/lc_searchdialog.png", ":/pyqt/source/images/lc_pickthrough.png"])
        self.addWidget(pp)

        self.addSeparator()

        self.add_tool_button('导入\n数据', create_icon(":/pyqt/source/images/lc_dataimport.png"))
        self.add_tool_button('保存\n工作区', create_icon(":/pyqt/source/images/lc_save.png"))

        pp = PushButtonPane()
        b = pp.add_buttons(3, ['新建变量', '打开变量', '清除工作区'],
                           [":/pyqt/source/images/lc_dbnewform.png", ":/pyqt/source/images/lc_open.png",
                            ":/pyqt/source/images/lc_dbclearquery.png"])
        self.addWidget(pp)
        self.addSeparator()
        self.add_tool_button('设置', create_icon(':/pyqt/source/images/lc_config.png'))
        self.add_tool_button('帮助', create_icon(':/pyqt/source/images/lc_helpindex.png'))

        self.view_menu = QMenu()
        self.view_menu.triggered.connect(self.process_visibility_actions)

        pp = PushButtonPane()
        buttons = pp.add_buttons(2, ['视图', ''])
        self.addWidget(pp)
        buttons[0].setMenu(self.view_menu)
        self.view_config_button = buttons[0]

    def process_visibility_actions(self, e: ActionWithMessage):
        main_window = get_main_window()
        dws = main_window.dock_widgets
        if e.message in dws.keys():
            dws[e.message].setVisible(e.isChecked())





class MainWindow(BaseMainWindow):
    setupui_tasks: List[Callable] = []
    boot_timer: QTimer = None

    @classmethod
    def __new__(cls, *args):
        instance = super().__new__(cls)
        cls.instance = instance
        return instance

    def __init__(self, parent=None):
        super().__init__(parent)

        import pyminer.pmutil
        pyminer.pmutil._main_window = self
        root_dir = os.path.dirname(__file__)
        pyminer.pmutil._root_dir = root_dir

        self.init_toolbar_tab()

        self.add_toolbar('toolbar_home', PMToolBarHome(), text='主页')


        self.setDockNestingEnabled(True)
        self.setWindowTitle('PyMiner')

        self.log_output_console = QTextEdit()


        self.add_widget_on_dock('editor_widget', PMCodeEditTabWidget(), text='编辑器面板', side='right')
        self.add_widget_on_dock('file_tree_widget', PMFilesTreeview(self), text='文件浏览器')

        self.console_widget = ConsoleWidget(self)
        self.add_widget_on_dock('console_widget', self.console_widget, text='控制台', side='right')



        self.add_widget_on_dock('log_output_console', self.log_output_console, text='日志输出', side='right')
        self.tabifyDockWidget(self.dock_widgets['console_widget'], self.dock_widgets['log_output_console'])

        self.add_widget_on_dock('table_panel', PMTableWidget(self), text='数据表格', side='top')
        self.tabifyDockWidget(self.dock_widgets['editor_widget'],self.dock_widgets['table_panel'])



        self.add_widget_on_dock('dataset_treeview_panel', PMDatasetsTreeview(self), text='数据集视图', side='left')

        tab_widget = PMTabWidget()

        self.data_control_page = PMPageData()
        tab_widget.addScrolledAreaTab(self.data_control_page, '数据分析')

        self.add_widget_on_dock('function_panel', tab_widget, text='功能面板', side='left')



        self.extensions_manager = extensions_manager
        self.extensions_manager.load_setting()
        self.extensions_manager.load()

        self.ext_manager_widget =  PMPageExt(self)
        self.add_widget_on_dock('extension_panel', self.ext_manager_widget, text='插件管理器', side='left')


        self.tabifyDockWidget(self.dock_widgets['extension_panel'],self.dock_widgets['function_panel'])

        self.load_layout()# 注掉或者删除配置文件之后，可以按照默认方式加载布局。
        self.switch_toolbar('toolbar_home')
        self.show()
        self.on_boot_finished()

    def action_menu_new(self):
        print('new')

    def action_menu_open(self):
        print('open!')

    def on_boot_finished(self):
        super().on_boot_finished()
        self.boot_timer = QTimer()
        self.boot_timer.start(50)
        self.boot_timer.timeout.connect(self.on_boot_timer_timeout)

    def on_boot_timer_timeout(self):
        if len(self.setupui_tasks) > 0:
            task = self.setupui_tasks.pop(0)
            print('start:', task)
            task()
        else:
            self.boot_timer.stop()
            print('boot ended!')

    def get_toolbar_list(self):
        pass

    def closeEvent(self, a0: QCloseEvent) -> None:
        self.save_layout()
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
        msg = create_time + ' ' + user + ' ' + level.upper() + ' [' + module + ']' + ':' + content
        if level == "error":
            html = "<a style='font-family:verdana;color:red;font-size:11;'>" + msg + "</a>"
        else:
            html = "<a style='font-family:verdana;color:black;font-size:11;'>" + msg + "</a>"


        console = self.log_output_console  # 由于代码重构，这里出现了不同。
        # [!TODO]应当创建方法，一次性的完成这个工作。
        console.moveCursor(QTextCursor.End)
        console.append(html)


def main():
    app = QApplication(sys.argv)
    demo = MainWindow()
    # demo.setMaximumHeight(700)
    id(demo)
    # b=MainWindow()
    # id(b)
    sys.exit(app.exec_())
