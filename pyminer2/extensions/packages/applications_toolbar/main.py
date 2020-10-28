from typing import TYPE_CHECKING, Callable, Dict
from PyQt5.QtCore import pyqtSignal, QLocale

from pyminer2.extensions.extensionlib import BaseExtension, BaseInterface

_ = lambda s: s
if TYPE_CHECKING:
    pass
    from pyminer2.extensions.extensionlib import extension_lib

from .applications_toolbar import PMDrawingsToolBar
from .process_monitor import PMProcessConsoleTabWidget
import os


class Extension(BaseExtension):
    if TYPE_CHECKING:
        interface: 'ApplicationsInterface' = None
        widget: 'PMDrawingsToolBar' = None
        extension_lib: 'extension_lib' = None

    def on_loading(self):
        self.extension_lib.Program.add_translation('zh_CN', {'Apps': '应用',
                                                             'Control System': '控制系统','Process Console':'进程控制台'})
        self.extension_lib.UI.add_translation_file(
            os.path.join(os.path.dirname(__file__), 'translations', 'qt_{0}.qm'.format(QLocale.system().name())))

    def on_load(self):
        drawings_toolbar: 'PMDrawingsToolBar' = self.widgets['PMDrawingsToolBar']
        drawings_toolbar.extension_lib = self.extension_lib
        self.interface.extension_lib = self.extension_lib
        self.drawings_toolbar = drawings_toolbar

        self.interface.drawing_item_double_clicked_signal = drawings_toolbar.drawing_item_double_clicked_signal

        self.interface.drawing_item_double_clicked_signal.connect(self.interface.on_clicked)
        self.interface.drawings_toolbar = drawings_toolbar
        self.interface.console_tab_widget = self.widgets['PMProcessConsoleTabWidget']

        # self.extension_lib.on_modification(drawings_toolbar.on_data_modified)
        self.extension_lib.Signal.get_widgets_ready_signal().connect(self.bind_events)

    def bind_events(self):
        pass
        # self.interface.add_app('statistics', 'aaa', ':/pyqt/source/images/lc_searchdialog.png',
        #                        lambda: print('1231231231'))
        # self.drawings_toolbar.buttons_toolbox.set_group_text('controlsys', self.extension_lib.UI._('Control System'))


class ApplicationsInterface(BaseInterface):
    drawing_item_double_clicked_signal: 'pyqtSignal' = None
    drawings_toolbar: 'PMDrawingsToolBar' = None
    console_tab_widget: 'PMProcessConsoleTabWidget' = None

    def on_clicked(self, name: str):
        print('interface', name)


    def add_app(self, group: str, text: str, icon_path: str, callback: Callable, hint: str = ''):
        """
        添加一个绘图按钮。name表示按钮的名称,text表示按钮的文字，icon_path表示按钮的图标路径，callback表示按钮的回调函数
        hint表示的就是按钮鼠标悬浮时候的提示文字。
        例如：
        extension_lib.get_interface('drawings_toolbar').add_graph_button('aaaaaa','hahahaahahah',
                                                                         ':/pyqt/source/images/lc_searchdialog.png',lambda :print('123123123'))
        """
        self.drawings_toolbar.add_toolbox_widget(group, text, icon_path, action=callback, hint=hint, refresh=True)

    def add_process_action(self, group: str, text: str, icon_path: str, process_args: list, hint: str = ''):
        """
        添加一个绘图按钮。name表示按钮的名称,text表示按钮的文字，icon_path表示按钮的图标路径，callback表示按钮的回调函数
        hint表示的就是按钮鼠标悬浮时候的提示文字。
        例如：
        extension_lib.get_interface('drawings_toolbar').add_graph_button('aaaaaa','hahahaahahah',
                                                                         ':/pyqt/source/images/lc_searchdialog.png',lambda :print('123123123'))
        """
        def callback():
            self.console_tab_widget.create_process(text,process_args)
            self.extension_lib.UI.raise_dock_into_view('process_console_tab')

        self.drawings_toolbar.add_toolbox_widget(group, text, icon_path, action=callback, hint=hint, refresh=True)
