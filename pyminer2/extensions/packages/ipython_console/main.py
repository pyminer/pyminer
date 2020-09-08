from .ipythonqtconsole import ConsoleWidget
from typing import TYPE_CHECKING
from pyminer2.extensions.extensionlib import BaseExtension, BaseInterface

if TYPE_CHECKING:
    pass


class Extension(BaseExtension):
    if TYPE_CHECKING:
        public_interface: 'ConsoleInterface' = None

    def on_load(self):
        self.console = self.widgets['ConsoleWidget']
        self.console.connect_to_datamanager(self.extension_lib)
        self.interface.widget = self.console
        print("Ipython console 被加载!",self.interface.widget,self.interface.hello(),self.console)

    def on_install(self):
        print('被安装')

    def on_uninstall(self):
        print("被卸载")


class ConsoleInterface(BaseInterface):
    def __init__(self):
        widget: 'ConsoleWidget' = None

    def run_command(self, command: str, hint_text=''):
        if self.widget is not None:
            self.widget.execute_command(command, True, hint_text=hint_text)

    def run_file(self, file: str):
        if self.widget is not None:
            self.widget.execute_file(file, True)
