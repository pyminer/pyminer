from typing import List

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QMenu

from pyminer.ui.base.widgets.generalwidgets.sourcemgr import create_icon


class PushButtonPane(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

    def add_buttons(self, button_num: int = 2, text: list = None, icon_path: list = None,
                    menu: list = None) -> List[QPushButton]:
        if text is None:
            text = [''] * button_num
        if icon_path == None:
            icon_path = [None] * button_num
        if menu == None:
            menu = [None] * button_num
        if len(text) != button_num or len(icon_path) != button_num or len(menu) != button_num:
            raise Exception('text,icon和menu参数都必须为长为2的可迭代对象。')
        if button_num == 2:
            height = 30
            font_size = 12
        else:
            height = 25
            font_size = 12
        btn_list = []
        for i in range(button_num):
            b = self.add_button(text=text[i], icon=create_icon(icon_path[i]), menu=menu[i], height=height,
                                font_size=font_size)
            btn_list.append(b)
        return btn_list

    def add_button(self, text: str = '', icon: QIcon = None, menu: QMenu = None, height: int = 30,
                   font_size: int = 14) -> QPushButton:
        b = QPushButton()
        b.setText(text)
        if icon is not None:
            b.setIcon(icon)
        if menu is not None:
            b.setMenu(menu)
        b.setStyleSheet(
            'QPushButton{border:0px;font-size:%dpx;padding:2px 2px;width:80px;height:%dpx;text-align:left;}' % (
                font_size, height) + \
            'QPushButton:hover{background-color:#ededed;}')
        self.layout.addWidget(b)
        return b