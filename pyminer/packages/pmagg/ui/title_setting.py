#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/8 16:47
# @Author  : Shark
# @Site    : 
# @File    : title_setting.py
# @Software: PyCharm
from PySide2 import QtWidgets


class Window(QtWidgets.QDialog):
    def __init__(self, canvas):
        super().__init__()
        self.setWindowTitle('Title Setting')
        self.canvas = canvas
        self.current_ax=None
        self.axes=self.canvas.figure.get_axes()
        self.suptitle_lineedit = QtWidgets.QLineEdit()
        self.subtitle_lineedit = QtWidgets.QLineEdit()
        self.sub_combox=QtWidgets.QComboBox()
        self.cancel_button = QtWidgets.QPushButton('取消')
        self.confirm_button = QtWidgets.QPushButton('确认')
        self.layout = QtWidgets.QFormLayout()
        self.generate_items()
        self.layout.addRow('主标题', self.suptitle_lineedit)
        self.layout.addRow('子图', self.sub_combox)
        self.layout.addRow('子标题', self.subtitle_lineedit)
        self.layout.addRow(self.cancel_button, self.confirm_button)
        self.setLayout(self.layout)
        self.confirm_button.clicked.connect(self.confirm_slot)
        self.cancel_button.clicked.connect(self.cancel_slot)
        self.sub_combox.currentIndexChanged.connect(self.sub_combox_slot)
        if self.canvas.figure._suptitle:
            self.suptitle_lineedit.setText(self.canvas.figure._suptitle.get_text())
        self.current_ax = self.axes[self.sub_combox.currentIndex()]
        self.exec_()

    def generate_items(self):
        for item in range(len(self.axes)):
            self.sub_combox.addItem('图'+str(item+1))

    def sub_combox_slot(self):
        self.current_ax=self.axes[self.sub_combox.currentIndex()]
        self.subtitle_lineedit.setText(self.current_ax.get_title())

    def confirm_slot(self):
        self.canvas.figure.suptitle(self.suptitle_lineedit.text())
        self.current_ax.set_title(self.subtitle_lineedit.text())
        self.canvas.draw_idle()

    def cancel_slot(self):
        self.close()