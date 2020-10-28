import sys

from .ipythonqtconsole import ConsoleWidget
from typing import TYPE_CHECKING
from pyminer2.extensions.extensionlib import BaseExtension, BaseInterface

import tornado.platform.asyncio as async_io

if sys.platform == 'win32':
    async_io.asyncio.set_event_loop_policy(
        async_io.asyncio.WindowsSelectorEventLoopPolicy())
if TYPE_CHECKING:
    from .ipythonqtconsole import ConsoleWidget


class Extension(BaseExtension):
    if TYPE_CHECKING:
        public_interface: 'ConsoleInterface' = None

    def on_loading(self):
        self.extension_lib.Program.add_translation('zh_CN', {'Console': '控制台'})

    def on_load(self):
        self.console:'ConsoleWidget' = self.widgets['ConsoleWidget']
        self.console.connect_to_datamanager(self.extension_lib)
        self.extension_lib.Signal.get_settings_changed_signal().connect(self.on_settings_changed)
        self.interface.widget = self.console

    def on_settings_changed(self):
        settings = self.extension_lib.Program.get_settings()
        self.console.change_ui_theme(settings['theme'])


class ConsoleInterface(BaseInterface):
    def __init__(self):
        widget: 'ConsoleWidget' = None

    def run_command(self, command: str, hint_text='', hidden=True):
        if self.widget is not None:
            self.widget.execute_command(command, hint_text=hint_text, hidden=hidden)

    def run_file(self, file: str):
        if self.widget is not None:
            self.widget.execute_file(file, True)
