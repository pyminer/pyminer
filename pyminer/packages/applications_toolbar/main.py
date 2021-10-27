import sys
from typing import TYPE_CHECKING, Callable, Dict, List

from PySide2.QtWidgets import QApplication
from PySide2.QtCore import Signal, QLocale, QTranslator

from lib.extensions.extensionlib import BaseExtension, BaseInterface

if TYPE_CHECKING:
    pass
    from lib.extensions.extensionlib import extension_lib

from .applications_toolbar import PMApplicationsToolBar
from .process_monitor import PMProcessConsoleTabWidget
from .manage_apps import APPManager, ToolAppDesc
import os

file_name = os.path.join(os.path.dirname(__file__), 'translations', 'qt_{0}.qm'.format(QLocale.system().name()))
app = QApplication.instance()
trans = QTranslator()
trans.load(file_name)
app.installTranslator(trans)


class Extension(BaseExtension):
    if TYPE_CHECKING:
        interface: 'ApplicationsInterface' = None
        widget: 'PMApplicationsToolBar' = None
        extension_lib: 'extension_lib' = None

    def on_loading(self):
        pass
        # self.trans = self.extension_lib.UI.add_translation_file(
        #     os.path.join(os.path.dirname(__file__), 'translations', 'qt_{0}.qm'.format(QLocale.system().name())))

    def on_load(self):
        applications_toolbar: 'PMApplicationsToolBar' = self.widgets['PMApplicationsToolBar']
        applications_toolbar.extension_lib = self.extension_lib
        self.interface.extension_lib = self.extension_lib
        self.applications_toolbar = applications_toolbar

        self.interface.app_item_double_clicked_signal = applications_toolbar.app_item_double_clicked_signal

        self.interface.app_item_double_clicked_signal.connect(self.interface.on_clicked)
        self.interface.toolbar = applications_toolbar
        self.interface.console_tab_widget: 'PMProcessConsoleTabWidget' = self.widgets['PMProcessConsoleTabWidget']
        self.interface.console_tab_widget.set_extension_lib(self.extension_lib)
        self.console_tab_widget = self.widgets['PMProcessConsoleTabWidget']
        self.extension_lib.Signal.get_widgets_ready_signal().connect(self.bind_events)
        self.applications_toolbar.console_tab_widget = self.console_tab_widget

    def bind_events(self):
        self.extension_lib.get_interface('file_tree').add_open_file_callback('.ui', lambda
            name: self.applications_toolbar.open_in_designer(name))
        self.extension_lib.get_interface('file_tree').add_open_file_callback('.ts', lambda
            name: self.applications_toolbar.open_in_linguist(name))


class ApplicationsInterface(BaseInterface):
    app_item_double_clicked_signal: 'Signal' = None
    toolbar: 'PMApplicationsToolBar' = None
    console_tab_widget: 'PMProcessConsoleTabWidget' = None

    def on_clicked(self, name: str):
        print('interface', name)

    def add_app(self, group: str, text: str, icon_path: str, callback: Callable, hint: str = ''):
        """
        添加一个绘图按钮。name表示按钮的名称,text表示按钮的文字，icon_path表示按钮的图标路径，callback表示按钮的回调函数
        hint表示的就是按钮鼠标悬浮时候的提示文字。
        例如：
        extension_lib.get_interface('applications_toolbar').add_app('aaaaaa','hahahaahahah',
                                                                         ':/pyqt/source/images/lc_searchdialog.png',lambda :print('123123123'))
        """
        self.toolbar.add_toolbox_widget(group, text, icon_path, action=callback, hint=hint, refresh=True)

    def add_process_action(self, group: str, text: str, icon_path: str, process_args: list, hint: str = ''):
        """
        添加一个绘图按钮。name表示按钮的名称,text表示按钮的文字，icon_path表示按钮的图标路径，callback表示按钮的回调函数
        hint表示的就是按钮鼠标悬浮时候的提示文字。
        例如：
        extension_lib.get_interface('applications_toolbar').app_toolbar_interface.add_process_action('应用测试', '拟合工具',
                                                 os.path.join(path, 'src', 'cftool.png'),
                                                 ['python', '-u', os.path.join(path, 'start_cftool.py')])
        """

        def callback():
            self.console_tab_widget.create_process(text, process_args)
            self.extension_lib.UI.raise_dock_into_view('process_console_tab')
        # self.toolbar.show_apps_button_bar.add_button(text, icon_path, btn_action=callback)

    def create_process(self, text: str, process_args: List[str]):
        print(text, process_args)
        self.console_tab_widget.create_process(text, process_args)
        self.extension_lib.UI.raise_dock_into_view('process_console_tab')

    def create_python_file_process(self, file_name, interpreter_path='', args: List[str] = None):
        if args is None:
            args = []
        if interpreter_path == '':
            interpreter_path = sys.executable
        command_list = [interpreter_path, file_name, '-u'] + args
        self.create_process(os.path.basename(file_name), process_args=command_list)

    def create_instant_boot_python_file_process(self, file_name, interpreter_path=''):
        self.console_tab_widget.create_instant_boot_process(file_name, interpreter_path)
        self.extension_lib.UI.raise_dock_into_view('process_console_tab')
