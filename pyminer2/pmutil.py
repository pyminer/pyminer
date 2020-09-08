# 定义了pyminer主界面的一些常用操作
# 将路径和主界面设置为可以全局获取，有助于未来插件式开发更加简便。
# 在主界面启动后，
import os
import sys
from typing import TYPE_CHECKING

from PyQt5.QtWidgets import QApplication

if TYPE_CHECKING:
    import pyminer2.pmappmodern

_application = None
_root_dir = None
_main_window: 'pyminer2.pmappmodern.MainWindow' = None


def get_root_dir() -> str:
    """
    获取根路径。
    Returns:

    """
    # assert _root_dir is not None
    # return _root_dir
    return os.path.dirname(__file__)


def get_application() -> None:
    """
    获取QApplication
    Returns:

    """
    assert _application is not None
    return _application


def get_main_window() -> 'pyminer2.pmappmodern.MainWindow':
    """
    获取主窗口或者主控件。
    Returns:
    """
    return _main_window

def get_work_dir() -> 'str':
    """
    获取主窗口或者主控件。
    Returns:
    """
    return _main_window.settings['work_dir']