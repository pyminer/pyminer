from typing import Tuple

from PySide2.QtGui import QColor
from PySide2.QtWidgets import QLineEdit, QLabel, QHBoxLayout, QPushButton, QColorDialog
from widgets.widgets.extended.base.baseextendedwidget import BaseExtendedWidget


class PMGColorCtrl(BaseExtendedWidget):
    def __init__(self, layout_dir: str, title: str, initial_value: str):
        super().__init__(layout_dir)
        self.on_check_callback = None
        self.prefix = QLabel(text=title)

        entryLayout = QHBoxLayout()

        self.ctrl = QLineEdit()
        self.ctrl.textChanged.connect(self.ontext)

        self.color_button = QPushButton()
        self.color_button.clicked.connect(self.oncolor)
        self.central_layout.addWidget(self.prefix)
        self.central_layout.addLayout(entryLayout)
        entryLayout.addWidget(self.ctrl)
        entryLayout.addWidget(self.color_button)
        self.set_value(initial_value)

    def ontext(self, event):
        if self.get_value() is None:
            self.color_button.setStyleSheet("background-color:#ff0000;")
            self.ctrl.setStyleSheet("background-color:#ff0000;")
        else:
            self.ctrl.setStyleSheet('background-color:#ffffff;')
            self.color_button.setStyleSheet("background-color:%s;" % self.colorTup2Str(self.get_value()))
            self.para_changed()
        self.ctrl.update()
        if callable(self.on_check_callback):
            self.on_check_callback()

    def oncolor(self, event):
        color = QColorDialog.getColor(initial=QColor(*self.get_value()))
        self.set_value(self.colorStr2Tup(color.name()))
        if callable(self.on_check_callback):
            self.on_check_callback()

    def set_value(self, color: Tuple = None):
        if color is None:
            color = (255, 255, 255)
        strcolor = self.colorTup2Str(color)
        self.color_button.setStyleSheet('background-color:%s;' % strcolor)
        self.ctrl.clear()
        self.ctrl.setText(strcolor)

    def get_value(self):
        rgb = self.ctrl.text().strip()
        if len(rgb) != 7 or rgb[0] != '#':
            return None
        try:
            int(rgb[1:], 16)
        except:
            import traceback
            traceback.print_exc()
            return None
        return self.colorStr2Tup(rgb)

    def colorStr2Tup(self, value: str) -> tuple:  # pos或者wh的输入都是tuple
        def convert(c):
            v = ord(c)
            if (48 <= v <= 57):
                return v - 48
            else:
                return v - 87  # 返回a的值。

        value = value.lower()
        c0 = convert(value[1])
        c1 = convert(value[2])
        c2 = convert(value[3])
        c3 = convert(value[4])
        c4 = convert(value[5])
        c5 = convert(value[6])
        a1 = c0 * 16 + c1
        a2 = c2 * 16 + c3
        a3 = c4 * 16 + c5
        return (a1, a2, a3)

    def colorTup2Str(self, value: tuple) -> str:
        if value is None:
            return None
        strcolor = '#'
        for i in value:
            strcolor += hex(int(i))[-2:].replace('x', '0')
        return strcolor
