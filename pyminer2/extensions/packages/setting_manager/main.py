import logging

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton

from pyminer2.extensions.extensionlib import BaseExtension, BaseInterface
from .settings import DataManager
from .ui_inputs import inputs

logger = logging.getLogger(__name__)


class SettingDialog(QDialog):
    def __init__(self, setting_objs):
        super().__init__()
        self.vlayout = QVBoxLayout(self)
        self.widgets = []
        for setting_obj in setting_objs:
            widget = inputs[setting_obj['type']](self, setting_obj)
            widget.show()
            self.widgets.append(widget)
            self.vlayout.addWidget(widget)

        self.accept_button = QPushButton(self)
        self.accept_button.setText("确定")
        self.vlayout.addWidget(self.accept_button)
        self.accept_button.clicked.connect(self.accept)

        self.setLayout(self.vlayout)

    def get_settings(self):
        settings = {}
        for widget in self.widgets:
            settings[widget.name] = widget.value
        return settings


class Setting:
    _names = set()
    _dm = DataManager()

    def __init__(self, name):
        if name in self._names:
            raise RuntimeError('The name has already been used')
        self._names.add(name)
        self.name = name

    def set(self, key, value):
        self._dm.set((self.name, key), value)

    def get(self, key):
        return self._dm.get((self.name, key))

    def remove(self, key):
        return self._dm.remove((self.name, key))

    def get_setting_window(self, setting_objs):
        dialog = SettingDialog(setting_objs)
        return dialog

    def config_setting(self, setting_objs):
        dialog = self.get_setting_window(setting_objs)
        dialog.show()
        dialog.exec()
        new_settings = dialog.get_settings()
        for key in new_settings:
            self.set(key, new_settings[key])


class Interface(BaseInterface):
    def __init__(self):
        super().__init__()
        self.setting = Setting


class Extension(BaseExtension):
    def __init__(self):
        super().__init__()
