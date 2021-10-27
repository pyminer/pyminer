#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/25 20:01
# @Author  : Jiangchenglong
# @Site    : 
# @File    : color_table.py
# @Software: PyCharm
from PySide2 import QtWidgets, QtGui
import matplotlib.colors as mcolors


class Window(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Colors')
        self.layout = QtWidgets.QFormLayout()
        self.scroll = QtWidgets.QScrollArea()
        self.generate_items()
        self.widget=QtWidgets.QWidget()
        self.widget.setLayout(self.layout)
        self.scroll.setWidget(self.widget)
        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.addWidget(self.scroll)
        self.scroll.horizontalScrollBar().setVisible(False)
        self.setLayout(self.vbox)
        # self.resize(300,500)
        self.exec_()

    def get_color_name(self):
        for i in range(self.layout.rowCount()):
            if self.layout.itemAt(i, self.layout.FieldRole).widget()==self.sender():
                label=self.layout.itemAt(i, self.layout.LabelRole).widget().text()
                QtWidgets.QApplication.clipboard().setText(label)
                return

    def generate_items(self):
        index = 0
        self.color_dict = dict()
        self.color_dict.update(mcolors.BASE_COLORS)
        self.color_dict.update(mcolors.TABLEAU_COLORS)
        self.color_dict.update(mcolors.CSS4_COLORS)
        self.color_dict.update(mcolors.XKCD_COLORS)
        for item in self.color_dict.keys():
            self.color_dict[item]=mcolors.to_hex(item)
        self.color_dict=dict(sorted(self.color_dict.items(),key=lambda x:x[1],reverse=True))
        color = QtGui.QColor()
        for color_name in self.color_dict.keys():
            label=QtWidgets.QLabel(color_name)
            button=QtWidgets.QPushButton('copy')
            self.layout.addRow(label,button)
            color.setNamedColor(self.color_dict[color_name])
            label.setStyleSheet('background-color:rgb{}'.format(tuple(i*255 for i in mcolors.to_rgb(color_name))))
            label.setFixedWidth(100)
            button.setFixedWidth(40)
            button.clicked.connect(self.get_color_name)
            index += 1