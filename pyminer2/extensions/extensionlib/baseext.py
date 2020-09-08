from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from PyQt5.QtWidgets import QWidget
    from pyminer2.extensions.extensionlib import extension_lib


class BaseExtension():
    widget_classes: Dict[str, 'QWidget'] = None
    widgets: Dict[str, 'QWidget'] = None
    extension_lib: 'extension_lib' = None
    public_interface:'BaseInterface' = None

    def get_widget(self, name: str):
        return self.widgets[name]


class BaseInterface():
    def hello(self):
        print("Hello")
