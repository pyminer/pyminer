# -*- coding:utf-8 -*-
# @Time: 2021/4/7 16:43
# @Author: Zhanyi Hou
# @Email: 1295752786@qq.com
# @File: test_ipython_support.py
import os
from typing import TYPE_CHECKING
from PySide2.QtCore import QTimer

os.chdir("../..")

from app2 import main, MainWindow
from features.extensions.extensionlib.extension_lib import extension_lib

if TYPE_CHECKING:
    from pmgui import PMToolBarHome

timer = None


def test_open_notebook(w: MainWindow):
    global timer
    timer = QTimer()
    timer.singleShot(1000, extension_lib.get_interface("jupyter_notebook_support").run)


main(test_open_notebook)
