#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/11 14:05
# @Author  : Shark
# @Site    : 
# @File    : arrow_setting.py.py
# @Software: PyCharm
from PySide2 import QtWidgets, QtGui,QtCore
import matplotlib.colors as mcolors
from .linestyles import *

class Window(QtWidgets.QDialog):
    def __init__(self,event, canvas):
        super().__init__()
        self.setWindowTitle('Arrow Setting')
        self.event_arrow = event
        self.canvas = canvas
        self.arrow = event.artist
        self.cancel_button = QtWidgets.QPushButton('取消')
        self.confirm_button = QtWidgets.QPushButton('确认')
        self.layout = QtWidgets.QFormLayout()
        self.arrow_width_spinbox=QtWidgets.QDoubleSpinBox()
        self.arrow_width_spinbox.setRange(0,100)
        self.arrow_style_combox=QtWidgets.QComboBox()
        self.connection_style_combox=QtWidgets.QComboBox()
        self.color_combox=QtWidgets.QComboBox()
        self.arrow_style_combox.addItems(arrowstyles)
        self.connection_style_combox.addItems(connection_styles)
        self.arrow_style_combox.setCurrentText(self.arrow.arrowprops['arrowstyle'])
        self.connection_style_combox.setCurrentText(self.arrow.connectionstyle)
        self.arrow_width_spinbox.setValue(self.arrow.arrow_patch.get_linewidth())
        self.layout.addRow('线宽', self.arrow_width_spinbox)
        self.layout.addRow('箭头样式', self.arrow_style_combox)
        self.layout.addRow('线条颜色', self.color_combox)
        self.layout.addRow('线条样式', self.connection_style_combox)
        self.layout.addRow(self.cancel_button, self.confirm_button)
        self.setLayout(self.layout)
        self.confirm_button.clicked.connect(self.confirm_slot)
        self.cancel_button.clicked.connect(self.cancel_slot)
        self.generate_items()
        color = self.arrow.arrow_patch.get_facecolor()
        if color == (0, 0, 0, 0):
            self.color_combox.setCurrentText('None')
        else:
            for item in self.color_dict:
                if mcolors.to_hex(item) == mcolors.to_hex(color):
                    self.color_combox.setCurrentText(item)
        self.exec_()

    def generate_items(self):
        index = 0
        self.color_dict = dict()
        self.color_dict.update(mcolors.BASE_COLORS)
        self.color_dict.update(mcolors.TABLEAU_COLORS)
        self.color_dict.update(mcolors.CSS4_COLORS)
        self.color_dict.update(mcolors.XKCD_COLORS)
        color = QtGui.QColor()
        for color_name in self.color_dict.keys():
            self.color_combox.addItem(color_name)
            color.setNamedColor(mcolors.to_hex(color_name))
            self.color_combox.model().item(index).setBackground(color)
            index += 1

    def confirm_slot(self):
        self.arrow.arrow_patch.set_arrowstyle(self.arrow_style_combox.currentText())
        self.arrow.arrow_patch.set_linewidth(self.arrow_width_spinbox.value())
        self.arrow.arrow_patch.set_color(self.color_combox.currentText())
        self.arrow.arrow_patch.set_connectionstyle(self.connection_style_combox.currentText())
        self.arrow.connectionstyle=self.connection_style_combox.currentText()
        self.canvas.draw_idle()

    def cancel_slot(self):
        self.close()