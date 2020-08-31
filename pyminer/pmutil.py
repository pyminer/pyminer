# 定义了pyminer主界面的一些常用操作
# 将路径和主界面设置为可以全局获取，有助于未来插件式开发更加简便。
# 在主界面启动后，
import os
import sys
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import pyminer.pmappmodern

_application = None
_root_dir = None
_main_window:'pyminer.pmappmodern.MainWindow' = None


def get_root_dir() -> str:
    '''
    获取根路径。
    Returns:

    '''
    assert _root_dir is not None
    return _root_dir


def get_application() -> QApplication:
    '''
    获取QApplication
    Returns:

    '''
    assert _application is not None
    return _application


def get_main_window() -> 'pyminer.pmappmodern.MainWindow':
    '''
    获取主窗口或者主控件。
    Returns:
    '''
    return _main_window


def test_widget_run(widget_type):
    '''
    控件测试函数
    Args:
        widget_type:控件类（直接输入）

    Returns:None

    '''

    _root_dir = os.path.dirname(os.path.abspath(__file__))

    app = QApplication(sys.argv)
    _application = app
    myWidget = widget_type()
    _main_window = myWidget
    myWidget.show()
    sys.exit(app.exec_())
