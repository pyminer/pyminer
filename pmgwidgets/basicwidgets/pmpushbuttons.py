"""
pmpushbuttons是一个按钮组，专门负责向工具栏中插入按钮。
其中PMPushButtonPane是按钮的载体，可以插入竖向排布的两个到三个按钮。
作者：Zhanyi Hou
"""
from typing import List

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QMenu, QLabel

from pmgwidgets.sourcemgr import create_icon


class PMPushButtonPane(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

    def add_height_occu_buttons(self):
        button_num = 3
        btn_list = []
        for i in range(button_num):
            btn = QLabel()
            btn.setText(' ')
            btn.setProperty('qssp', 'occu')
            btn_list.append(btn)
            btn.setObjectName('space_occupation_button')
            self.layout.addWidget(btn)
        return btn_list

    def add_buttons(self, button_num: int = 2, text: list = None, icon_path: list = None,
                    menu: list = None) -> List[QPushButton]:
        if text is None:
            text = [''] * button_num
        if icon_path is None:
            icon_path = [None] * button_num
        if menu is None:
            menu = [None] * button_num
        if len(text) != button_num or len(
                icon_path) != button_num or len(menu) != button_num:
            raise Exception('text,icon和menu参数都必须为长为2的可迭代对象。')
        qssproperty = "minibutton3"
        if button_num == 2:
            qssproperty = "minibutton2"

        btn_list = []
        for i in range(button_num):
            btn = self.add_button(text=text[i], icon=create_icon(icon_path[i]), menu=menu[i], qssproperty=qssproperty)
            btn_list.append(btn)
        return btn_list

    def add_button(self, text: str = '', icon: QIcon = None, menu: QMenu = None, qssproperty = "minibutton3") \
            -> QPushButton:
        pbtn = QPushButton()
        pbtn.setText(text)
        if icon is not None:
            pbtn.setIcon(icon)
        if menu is not None:
            pbtn.setMenu(menu)
        pbtn.setProperty("qssp", qssproperty)
        self.layout.addWidget(pbtn)
        return pbtn
