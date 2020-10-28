# -*- coding: utf-8 -*-
# @Time    : 2020/9/9 9:40
# @Author  : 别着急慢慢来
# @FileName: linestyle_manager.py.py

from .linestyle_ui import Ui_Dialog
from PyQt5 import QtWidgets, QtGui
from .linestyles import *
import matplotlib.colors as mcolors


class Ui_Dialog_Manager(Ui_Dialog):
    def __init__(self, canvas, line):
        self.canvas = canvas
        self.line = line
        self.dialog = QtWidgets.QDialog()
        self.setupUi(self.dialog)
        self.combox_colors()
        self.comboBox.currentIndexChanged.connect(self.combobox_color_slot)
        self.comboBox_2.currentIndexChanged.connect(
            self.combobox2_linestyle_slot)
        self.comboBox_3.currentIndexChanged.connect(self.combobox3_marker_slot)
        self.comboBox_4.currentIndexChanged.connect(self.combobox4_color_slot)
        self.comboBox_5.currentIndexChanged.connect(self.combobox5_color_slot)
        self.lineEdit.textChanged.connect(self.linewidth_slot)
        self.init_gui()
        self.dialog.exec_()  # 初始化之后再执行

    def init_gui(self):
        color = self.line.get_color()
        if color in self.color_dict.keys():
            self.comboBox.setCurrentText(color)
        markerfacecolor = self.line.get_markerfacecolor()
        if markerfacecolor in self.color_dict.keys():
            self.comboBox_5.setCurrentText(markerfacecolor)
        markeredgecolor = self.line.get_markeredgecolor()
        if markeredgecolor in self.color_dict.keys():
            self.comboBox_4.setCurrentText(markeredgecolor)
        self.lineEdit.setText(str(self.line.get_linewidth()))
        self.lineEdit_2.setText(str(self.line.get_markersize()))
        self.lineEdit_3.setText(str(self.line.get_markeredgewidth()))
        self.comboBox_2.addItems(linestyles)
        self.comboBox_2.setCurrentText(self.line.get_linestyle())
        self.comboBox_3.addItems(markers)
        self.comboBox_3.setCurrentText(self.line.get_marker())

    def combox_colors(self):
        index = 0
        self.color_dict = dict()
        self.color_dict.update(mcolors.BASE_COLORS)
        self.color_dict.update(mcolors.TABLEAU_COLORS)
        self.color_dict.update(mcolors.CSS4_COLORS)
        self.color_dict.update(mcolors.XKCD_COLORS)
        color = QtGui.QColor()
        for color_name in self.color_dict.keys():
            self.comboBox.addItem(color_name)
            self.comboBox_4.addItem(color_name)
            self.comboBox_5.addItem(color_name)
            color.setNamedColor(mcolors.to_hex(color_name))
            self.comboBox.model().item(index).setBackground(color)
            self.comboBox_4.model().item(index).setBackground(color)
            self.comboBox_5.model().item(index).setBackground(color)
            index += 1

    def combobox_color_slot(self):
        color = self.comboBox.model().item(
            self.comboBox.currentIndex()).background().color().getRgb()
        # self.comboBox.setStyleSheet(
        #     "QComboBox{{ background-color: rgb{} }}".format(color))
        self.line.set_color(mcolors.to_hex(rgb_to_hex(*color[:3]),keep_alpha=color[3]))
        self.canvas.draw()
        # self.comboBox.setStyleSheet("QComboBox QAbstractItemView{selection-background-color: lightgreen;}")
        # self.comboBox.setStyleSheet("QComboBox QAbstractItemView::item:hover{background-color: lightgreen;}")

    def combobox4_color_slot(self):
        color = self.comboBox_4.model().item(
            self.comboBox_4.currentIndex()).background().color().getRgb()
        # self.comboBox_4.setStyleSheet(
        #     "QComboBox{{ background-color: rgb{} }}".format(color))
        self.line.set_markeredgecolor(mcolors.to_hex(rgb_to_hex(*color[:3]),keep_alpha=color[3]))
        self.canvas.draw()

    def combobox5_color_slot(self):
        color = self.comboBox_5.model().item(
            self.comboBox_5.currentIndex()).background().color().getRgb()
        # self.comboBox_5.setStyleSheet(
        #     "QComboBox{{ background-color: rgb{} }}".format(color))
        self.line.set_markerfacecolor(mcolors.to_hex(rgb_to_hex(*color[:3]),keep_alpha=color[3]))
        self.canvas.draw()

    def combobox2_linestyle_slot(self):
        self.line.set_linestyle(self.comboBox_2.currentText())
        self.canvas.draw()

    def linewidth_slot(self):
        try:
            self.line.set_linewidth(float(self.lineEdit.text()))
            self.canvas.draw_idle()
        except Exception as e:
            pass

    def combobox3_marker_slot(self):
        self.line.set_marker(self.comboBox_3.currentText())
        self.canvas.draw()
