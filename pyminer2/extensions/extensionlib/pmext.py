import pyminer2.pmutil

from PyQt5.QtWidgets import QAction, QMenu, QWidget, QToolButton, QToolBar, QPushButton
from PyQt5.QtGui import QIcon
from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from pyminer2.pmappmodern import MainWindow
    from pyminer2.ui.base.widgets.consolewidget import ConsoleWidget
    from pyminer2.workspace.datamanager.datamanager import DataManager
    from pyminer2.extensions.packages.code_editor.main import PMCodeEditTabWidget
    from pyminer2.extensions.packages.workspace_inspector.main import PMWorkspaceInspectWidget
    from pyminer2.ui.generalwidgets import PMToolBar


class PluginInterface(object):
    @staticmethod
    def get_root_dir() -> str:
        """
        获取项目的根目录
        """
        return pyminer2.pmutil.get_root_dir()

    # @staticmethod
    # def get_main_window() -> "MainWindow":
    #     """
    #     获取应用主界面
    #     """
    #     return pyminer2.pmutil.get_main_window()

    @staticmethod
    def get_editor() -> 'PMCodeEditTabWidget':
        return pyminer2.pmutil.get_main_window().get_dock_widget('code_editor').widget()

    @staticmethod
    def get_data_manager() -> "DataManager":
        """
        # 获取数据管理类，返回DataManager
        """
        return pyminer2.workspace.datamanager.datamanager.data_manager

    @staticmethod
    def get_toolbar(toolbar_name: str) -> "PMToolBar":
        """
        获取工具栏
        :param toolbar_name:
        :return:
        """
        tb = pyminer2.pmutil.get_main_window().toolbars.get(toolbar_name)
        assert tb is not None
        return tb

    @staticmethod
    def get_toolbar_widget(toolbar_name: str,
                           tool_widget_name: str) -> "QPushButton":
        return PluginInterface.get_toolbar(
            toolbar_name).get_control_widget(tool_widget_name)

    @staticmethod
    def append_to_toolbar(toolbar_name: str, text: str,
                          icon: QIcon, menu: QMenu) -> QToolButton:
        """

        Args:
            text:工具栏显示的文字。一般时候工具栏的文字是不会显示在界面上的，但鼠标悬停时会显示出来。
            icon: 图标
            toolbar_name:工具栏的名称。

        Returns:None

        """
        tool_button = PluginInterface.get_toolbar(
            toolbar_name).add_tool_button(text=text, icon=icon, menu=menu)
        return tool_button  # 返回值为按钮。

    @staticmethod
    def add_tool_bar(name: str, toolbar: QToolBar, text: str):
        pyminer2.pmutil.get_main_window().add_toolbar(
            name=name, toolbar=toolbar, text=text)

    @staticmethod
    def switch_tool_bar(toolbar_name: str):
        """
        切换工具栏
        :param toolbar_name:
        :return:
        """
        pyminer2.pmutil.get_main_window().switch_toolbar(toolbar_name)

    @staticmethod
    def show_tool_bar(toolbar_name: str):
        """
        切换工具栏
        :param toolbar_name:
        :return:
        """
        pyminer2.pmutil.get_main_window().show_toolbar(toolbar_name)

    @staticmethod
    def append_widget_to_toolbar(toolbar_name: str, widget: QWidget):
        PluginInterface.get_toolbar(toolbar_name).addWidget(widget)

    # 插入到菜单栏第action_id之后。调用的是insertAction方法。插入之后其他选项id也会改变。建议从后向前插入。
    @staticmethod
    def append_to_toolbox(tab_id: int, icon_path: str, text: str,
                          command: callable):
        """
        插入到工具箱中按钮。
        Args:
            tab_id:
            icon_path:
            text:
            command:

        Returns:
        """

        return

    @staticmethod
    def append_to_sidebar(text: str,
                          command: Callable, icon_path: str):
        """
        添加到右侧工具栏中。
        Args:
            text:工具栏显示的文字。一般时候工具栏的文字是不会显示在界面上的，但鼠标悬停时会显示出来。
            command: 点击时调用的函数
            icon_path: 图标的文件路径，不得为空。

        Returns:None

        """
        tool_bar = pyminer2.pmutil.get_main_window().toolBar_right
        act = QAction(icon=QIcon(icon_path), text=text,
                      parent=pyminer2.pmutil.get_main_window())
        act.triggered.connect(lambda unused_arg: command())
        tool_bar.addAction(act)

    @staticmethod
    def append_to_context_menu(text: str, command: Callable, icon_path: str):
        """
        添加到鼠标右键菜单当中。
        Args:
            text:
            command:
            icon_path:

        Returns:

        """

        return

    @staticmethod
    def append_to_tray_menu(text: str, command: Callable):
        """
        添加到托盘菜单栏。
        Args:
            text: 菜单的文字内容
            command: 点击菜单触发的函数

        Returns:

        """
        tray_context_menu = pyminer2.pmutil.get_main_window().tray_icon.contextMenu()
        act = QAction(text, pyminer2.pmutil.get_main_window())
        act.triggered.connect(lambda unused_arg: command())
        tray_context_menu.addAction(act)
        return

        # 以上这些方法未来还会定义insert_to_menu等插入到特定位置的方法。

    @staticmethod
    def show_log(level: str, module: str, content: str):
        """
        在日志窗口显示log。
        :param level: 类型，比如‘info’
        :param module: 模块。比如'Jupyter'
        :param content: 内容。自定义的字符串
        :return:
        效果：
        调用——PluginInterface.show_log('info','CodeEditor','新建文件')
        输出——2020-08-29 23:43:10 hzy INFO [CodeEditor]:新建文件
        """
        pyminer2.pmutil.get_main_window().slot_flush_console(level, module, content)

    @staticmethod
    def get_console() -> 'ConsoleWidget':
        """
        获取控制台的实例。
        """
        return pyminer2.pmutil.get_main_window(
        ).dock_widgets['ipython_console'].widget()

    @staticmethod
    def get_workspace_inspector() -> 'PMWorkspaceInspectWidget':
        return pyminer2.pmutil.get_main_window().dock_widgets['workspace_inspector'].widget()

    @staticmethod
    def add_docked_widget(dock_name: str, widget: 'QWidget',
                          text: str, side: str = 'left'):
        return  pyminer2.pmutil.get_main_window().add_widget_on_dock(
            dock_name=dock_name, widget=widget, text=text, side=side)


    @staticmethod
    def show_dialog(dialog_name: str, parent=None, args=tuple()):
        """
        对话框类必须有parent作为输入参数。否则对话框将无法显示。
        另外还可以通过args选项指定除了parent之外的其他输入参数。
        """
        mw = pyminer2.pmutil.get_main_window()
        dialog_class = PluginInterface.get_dialog_class(dialog_name)
        if parent is None:
            parent = mw
        dialog_class(parent, *args).show()

    @staticmethod
    def get_dialog_class(dialog_name: str):
        """
        获取对话框类的方式。
        """
        mw = pyminer2.pmutil.get_main_window()
        dialog_class = mw.dialog_classes.get(dialog_name)
        if dialog_class is None:
            raise Exception(
                'Mainwindow has no dialog_class named \'%s\'' %
                dialog_name)
        else:
            return dialog_class

    @staticmethod
    def get_work_dir() -> str:
        '''
        获取当前工作路径
        '''
        return pyminer2.pmutil.get_main_window().settings['work_dir']

    @staticmethod
    def set_work_dir(work_dir: str) -> None:
        '''
        设置当前工作路径
        '''
        pyminer2.pmutil.get_main_window().settings['work_dir'] = work_dir
        print(work_dir)

    class Signals():
        @staticmethod
        def get_main_window_close_signal():
            return pyminer2.pmutil.get_main_window().close_signal
        # def __init__(self):

