from typing import Dict, TYPE_CHECKING
import logging

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from PyQt5.QtWidgets import QWidget
    from pyminer2.extensions.extensionlib import extension_lib


class BaseExtension():
    widget_classes: Dict[str, 'QWidget'] = None
    widgets: Dict[str, 'QWidget'] = None
    extension_lib: 'extension_lib' = None
    public_interface: 'BaseInterface' = None
    settings: Dict[str, object] = None

    def get_widget(self, name: str):
        return self.widgets[name]

    def _on_loading(self):
        logger.info(f'{self.info.display_name}即将被加载')
        self.on_loading()

    def on_loading(self):
        pass

    def _on_load(self):
        logger.info(f'{self.info.display_name}已经被加载')
        self.interface._set_extension(self)
        self.on_load()

    def on_load(self):
        pass

    def _on_install(self):
        logger.info(f'{self.info.display_name}被安装')
        self.on_install()

    def on_install(self):
        pass

    def _on_uninstall(self):
        logger.info(f'{self.info.display_name}被卸载')
        self.on_uninstall()

    def on_uninstall(self):
        pass


class BaseInterface():
    def _set_extension(self, extension):
        self.extension = extension
