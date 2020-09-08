# -*- coding: utf-8 -*-
# @Time    : 2020/9/2 16:59
# @Author  : 别着急慢慢来
# @FileName: axes_control_manager.py.py

"""
负责对生成的ui类绑定事件，添加交互逻辑
"""
from axes_control import Ui_Form
from PyQt5 import QtWidgets
from matplotlib.ticker import MultipleLocator
import re, ast


class Ui_Form_Manager(Ui_Form):
    def __init__(self, ax, canvas):
        self.ax = ax
        self.canvas = canvas
        self.dialog = QtWidgets.QDialog()
        self.setupUi(self.dialog)
        self.init_gui()
        self.pushButton.clicked.connect(self.confirm_slot)
        self.pushButton_2.clicked.connect(self.cancel_slot)
        self.pushButton_3.clicked.connect(self.apply_slot)
        self.dialog.exec_()  # 初始化之后再执行

    def init_gui(self):
        self.lineEdit.setText(self.ax.get_xlabel())
        self.lineEdit_2.setText(self.ax.get_ylabel())
        try:
            self.lineEdit_3.setText(self.ax.get_zlabel())  # 如果没有z轴，这个输入框变灰
        except Exception as e:
            self.lineEdit_3.setDisabled(True)
        # self.lineEdit_4.setText(self.figure.suptitle()) # suptitle 只能设置无法获取
        self.lineEdit_5.setText(self.ax.get_title())
        self.lineEdit_6.setText(str(tuple([round(i, 2) for i in self.ax.get_xlim()])))
        self.lineEdit_7.setText(str(tuple([round(i, 2) for i in self.ax.get_ylim()])))
        try:
            self.lineEdit_8.setText(str(tuple([round(i, 2) for i in self.ax.get_zlim()])))
        except Exception as e:
            self.lineEdit_8.setDisabled(True)
        # 刻度间隔不好获取，所以就默认留空
        # self.lineEdit_9.setText(self.ax.xaxis.get_major_locator())
        # self.lineEdit_10.setText(self.ax.yaxis.get_major_locator())
        try:
            self.ax.zaxis.get_major_locator()
        except Exception as e:
            self.lineEdit_11.setDisabled(True)
        try:
            self.ax.zaxis.get_minor_locator()
        except Exception as e:
            self.lineEdit_14.setDisabled(True)

    def apply_slot(self):
        self.ax.set_xlabel(self.lineEdit.text())
        self.ax.set_ylabel(self.lineEdit_2.text())
        if self.lineEdit_3.isEnabled():
            self.ax.set_zlabel(self.lineEdit_3.text())
        if self.lineEdit_4.isModified(): self.canvas.figure.suptitle(self.lineEdit_4.text())
        if self.lineEdit_5.isModified(): self.ax.set_title(self.lineEdit_5.text())
        if self.lineEdit_6.isModified():
            value = self._is_right_tuple(self.lineEdit_6.text(), "X坐标轴范围输入有误")
            self.ax.set_xlim(value)
        if self.lineEdit_7.isModified():
            value = self._is_right_tuple(self.lineEdit_7.text(), "Y坐标轴范围输入有误")
            self.ax.set_ylim(value)
        if self.lineEdit_8.isEnabled() and self.lineEdit_8.isModified():
            value = self._is_right_tuple(self.lineEdit_6.text(), "Z坐标轴范围输入有误")
            self.ax.set_zlim(value)
        try:
            if self.lineEdit_9.isModified():
                self.ax.xaxis.set_major_locator(MultipleLocator(ast.literal_eval(self.lineEdit_9.text())))
            if self.lineEdit_10.isModified():
                self.ax.yaxis.set_major_locator(MultipleLocator(ast.literal_eval(self.lineEdit_10.text())))
            if self.lineEdit_11.isModified():
                self.ax.zaxis.set_major_locator(MultipleLocator(ast.literal_eval(self.lineEdit_11.text())))
            if self.lineEdit_12.isModified():
                self.ax.xaxis.set_minor_locator(MultipleLocator(ast.literal_eval(self.lineEdit_12.text())))
            if self.lineEdit_13.isModified():
                self.ax.yaxis.set_minor_locator(MultipleLocator(ast.literal_eval(self.lineEdit_13.text())))
            if self.lineEdit_14.isModified():
                self.ax.zaxis.set_minor_locator(MultipleLocator(ast.literal_eval(self.lineEdit_14.text())))
        except Exception as e:
            QtWidgets.QMessageBox.warning(self.dialog, "错误", "坐标轴刻度输入有误，请确保输入的是数字，且主刻度间隔＞次刻度间隔")
            return
        self.canvas.draw()

    def _is_right_tuple(self, tuple_str, message):
        try:
            value = tuple(ast.literal_eval(tuple_str))
            assert len(value) == 2
            assert str(value[0]).isdigit() and str(value[1]).isdigit()
            return value
        except Exception as e:
            QtWidgets.QMessageBox.warning(self.dialog, "错误", message)
        return

    def _is_digit(self, num_str):
        value = re.compile(r'^[-+]?[0-9]+\.[0-9]+$')
        result = value.match(num_str)
        if result:
            return True
        else:
            return False

    def confirm_slot(self):
        self.apply_slot()
        self.dialog.close()

    def cancel_slot(self):
        self.dialog.close()
