#!/usr/bin/env python
# -*- coding:utf-8 -*-

import webbrowser
from PyQt5.QtWidgets import QDialog, QDesktopWidget
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import Qt

class PMDialog(QDialog):
    '''
    右侧工具栏各ToolButton弹出的对话框父类
    利于避免写重复的方法：比如帮助，窗口居中等
    关闭对话框后单击特效需要消失
    统一写关闭事件，关闭后发送信号
    '''
    unset_effect_signal = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.center()

    def closeEvent(self, e):
        self.unset_effect_signal.emit()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(int((screen.width() - size.width()) / 2), int((screen.height() - size.height()) / 2))


    def keyPressEvent(self, e):
        """
        按键盘Escape退出当前窗口
        @param e:
        """
        if e.key() == Qt.Key_Escape:
            self.close()

    def get_help(self):
        """
        打开帮助页面
        """
        try:
            webbrowser.get('chrome').open_new_tab("http://www.py2cn.com")
        except Exception as e:
            webbrowser.open_new_tab("http://www.py2cn.com")
