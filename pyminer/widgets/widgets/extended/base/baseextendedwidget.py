import os
import string
import sys
import time
from typing import List, Dict, Tuple, Union, Callable, Any
from PySide2.QtCore import Signal
from PySide2.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFrame


class BaseExtendedWidget(QFrame):
    """
    基础参数控件的类型。所有的参数控件都在其上派生而来。
    """
    signal_param_changed = Signal(str)
    NORMAL = 0
    WARNING = 1
    ERROR = 2

    def __init__(self, layout_dir='v'):
        super(BaseExtendedWidget, self).__init__()

        self._initial_stylesheet = self.styleSheet()
        # if layout_dir == 'v':
        self.name = ''
        self.central_layout = QVBoxLayout()
        # else:
        #     self.central_layout = QHBoxLayout()
        self.setLayout(self.central_layout)
        self.central_layout.setContentsMargins(0, 0, 0, 0)

        self.on_para_change = None
        self.__app = None  # SciApp。初始化控件的时候指定，并且在调用set_app的时候传入。

    def para_changed(self):
        if (self.on_para_change is not None) and (self.__app is not None):
            self.on_para_change(self.__app)

    def set_app(self, app):
        """
        在sciwx中，需要指定SciApp。但是在PyMiner中目前还没有这种需求。
        :param app:
        :return:
        """
        self.__app = app

    def is_key(self, event, type=''):
        """
        'dir':判断方向键
        'alpha':判断是否为26个字母
        'hex':判断是否为十六进制数字或者字母
        'digit':判断是否为数字0~9
        'valid':包含数字、字母或者退格键。
        """

        type = type.lower()
        if type == '':
            return True
        elif type.startswith('dir'):
            return event.keysym.lower() in ('left', 'right', 'up', 'down')
        elif type.startswith('alpha'):
            return event.keysym in string.ascii_lowercase
        elif type.startswith('hex'):
            return event.keysym in string.hexdigits
        elif type.startswith(('digit')):
            return event.keysym in string.digits

    def set_value(self, value: Any):
        pass

    def get_value(self):
        pass

    def set_params(self, *args, **kwargs):
        pass

    def alert(self, level: str, *args, **kwargs):
        """
        alert
        Args:
            level: str
            'normal'
            'warning'
            'error'

        Returns:

        """
        if level == 'normal':
            self.setStyleSheet(self._initial_stylesheet)
        elif level == 'error':
            self.setStyleSheet('QWidget{background-color:#ff0000;}')
        elif level == 'warning':
            self.setStyleSheet('QWidget{background-color:#ffff00;}')
        else:
            raise ValueError('alert not defined!!')
