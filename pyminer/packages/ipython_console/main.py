import os
import sys

import tornado.platform.asyncio as async_io
from PySide2.QtCore import QLocale, QTranslator
from PySide2.QtWidgets import QApplication

from lib.extensions.extensionlib import BaseExtension, BaseInterface
from .ipythonqtconsole import ConsoleWidget

if sys.platform == 'win32':
    try:
        async_io.asyncio.set_event_loop_policy(async_io.asyncio.WindowsSelectorEventLoopPolicy())
    except AttributeError:
        pass
file_name = os.path.join(os.path.dirname(__file__), 'translations', 'qt_{0}.qm'.format(QLocale.system().name()))
app = QApplication.instance()
trans_editor = QTranslator()
trans_editor.load(file_name)
app.installTranslator(trans_editor)


class Extension(BaseExtension):
    public_interface: 'ConsoleInterface'
    console: 'ConsoleWidget'
    _work_dir = ''

    def on_loading(self):
        """在进行加载前，加载翻译文件。"""
        pass

    def on_load(self):
        """插件加载完成后，绑定控制台控件、数据管理器等变量。"""
        self.console: ConsoleWidget = self.widgets['ConsoleWidget']
        self.console.set_extension_lib(self.extension_lib)
        self.console.connect_to_datamanager(self.extension_lib)
        self.interface.widget = self.console
        self.extension_lib.Signal.get_settings_changed_signal().connect(self.on_settings_changed)
        self.extension_lib.Signal.get_events_ready_signal().connect(self.on_settings_changed)
        self._work_dir = self.extension_lib.Program.get_settings_item_from_file("config.ini", "MAIN/PATH_WORKDIR")

    def on_settings_changed(self):
        """
        如果设置项发生改变，重新加载主题文件。
        TODO:倘若ipython发生改变之后，工作路径如何跟着改变？
        """
        theme = self.extension_lib.Program.get_theme()
        self.console.change_ui_theme(theme)
        work_dir =  self.extension_lib.Program.get_work_dir()
        if not os.path.samefile(work_dir, self._work_dir):  # samefile函数：既可判断是否为同一文件，也可判断是否为同一文件夹
            self.command = self.interface.run_command("get_ipython().chdir(\'%s\')" % work_dir.replace('\\', '\\\\'),
                                                      hidden=False)
            self._work_dir = work_dir
        self.console.reset_font()  # 将字体重新设置回来


class ConsoleInterface(BaseInterface):
    """
    定义IPython控制台向外开放的函数接口，包括执行一行命令和运行一个文件。
    """
    widget: 'ConsoleWidget'

    def run_command(self, command: str, hint_text='', hidden=True):
        """执行一行命令。

        Args:
            command: 命令。
            hint_text: 在运行代码前显示的提示。
            hidden: 这个参数看起来像是，隐藏执行结果？
        """
        if self.widget is not None:
            self.widget.execute_command(command, hint_text=hint_text, hidden=hidden)

    def run_file(self, file: str):
        """执行一个文件。

        Args:
            file: 文件路径。
        """
        if self.widget is not None:
            self.widget.execute_file(file, True)
