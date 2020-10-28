"""
作者：@吴宫幽径
说明：
dialog无需写在json里面，直接调用主界面的控件就可以了。
"""

from PyQt5.QtWidgets import QDialog, QHBoxLayout, QPushButton, QToolButton, QTextEdit, QSizePolicy
from pyminer2.extensions.extensionlib import BaseExtension, BaseInterface


class Extension(BaseExtension):
    def on_load(self):
        self.demo_tool_button = self.widgets['DemoToolButton']
        self.demo_tool_button.main = self


class Interface(BaseInterface):
    pass


class DemoToolButton(QToolButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setText('显示\n插件示例\n的对话框')
        self.clicked.connect(self.show_dialog)

    def show_dialog(self):
        """
        显示一个插件示例所弹出的对话框。
        """
        import subprocess
        import os
        path = os.path.dirname(__file__)
        subprocess.Popen(['python','-u',os.path.join(path,'run_dialog.py')])

