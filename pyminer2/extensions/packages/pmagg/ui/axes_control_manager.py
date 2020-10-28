# -*- coding: utf-8 -*-
# @Time    : 2020/9/2 16:59
# @Author  : 别着急慢慢来
# @FileName: axes_control_manager.py.py

"""
负责对生成的ui类绑定事件，添加交互逻辑
"""
from .axes_control import Ui_Form
from PyQt5 import QtWidgets, QtGui
from matplotlib.ticker import MultipleLocator
import ast
import configparser
import os
from PyQt5.QtWidgets import QFileDialog, QApplication
import subprocess
import re
import platform
import matplotlib.colors as mcolors
from .linestyles import *
from matplotlib.font_manager import fontManager
import matplotlib
import matplotlib.pyplot as plt
from PyQt5.QtCore import QTranslator


class Ui_Form_Manager(Ui_Form):
    def __init__(self, ax, canvas, config: configparser.ConfigParser, config_path: str, lang: str):
        self.ax = ax
        self.canvas = canvas
        self.config = config
        self.config_path = config_path
        self.dialog = QtWidgets.QDialog()
        self.setupUi(self.dialog)
        self.retranslateUi(self.dialog)
        # 翻译家
        self.trans = QTranslator()
        lang_qm = os.path.join(os.path.dirname(self.config_path), 'langs/{}.qm'.format(lang))
        self.trans.load(lang_qm)
        _app = QApplication.instance()  # 获取app实例
        _app.installTranslator(self.trans)  # 重新翻译主界面
        self.retranslateUi(self.dialog)
        self.init_gui()
        self.pushButton.clicked.connect(self.confirm_slot)
        self.pushButton_2.clicked.connect(self.cancel_slot)
        self.pushButton_3.clicked.connect(self.apply_slot)
        self.pushButton_4.clicked.connect(self.get_all_fonts)
        self.dialog.exec_()  # 初始化之后再执行

    def init_gui(self):
        self.get_all_fonts()
        self.set_combox_items()
        self.get_all_settings()
        self.lineEdit.setText(self.ax.get_xlabel())
        self.lineEdit_2.setText(self.ax.get_ylabel())
        try:
            self.lineEdit_3.setText(self.ax.get_zlabel())  # 如果没有z轴，这个输入框变灰
        except Exception as e:
            self.lineEdit_3.setDisabled(True)
        if self.canvas.figure._suptitle:
            self.lineEdit_4.setText(self.canvas.figure._suptitle.get_text())
        self.lineEdit_5.setText(self.ax.get_title())
        self.lineEdit_6.setText(
            str(tuple([round(i, 2) for i in self.ax.get_xlim()])))
        self.lineEdit_7.setText(
            str(tuple([round(i, 2) for i in self.ax.get_ylim()])))
        try:
            self.lineEdit_8.setText(
                str(tuple([round(i, 2) for i in self.ax.get_zlim()])))
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
        if self.lineEdit_4.isModified():
            self.canvas.figure.suptitle(self.lineEdit_4.text())
        if self.lineEdit_5.isModified():
            self.ax.set_title(self.lineEdit_5.text())
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
                self.ax.xaxis.set_major_locator(MultipleLocator(
                    ast.literal_eval(self.lineEdit_9.text())))
            if self.lineEdit_10.isModified():
                self.ax.yaxis.set_major_locator(MultipleLocator(
                    ast.literal_eval(self.lineEdit_10.text())))
            if self.lineEdit_11.isModified():
                self.ax.zaxis.set_major_locator(MultipleLocator(
                    ast.literal_eval(self.lineEdit_11.text())))
            if self.lineEdit_12.isModified():
                self.ax.xaxis.set_minor_locator(MultipleLocator(
                    ast.literal_eval(self.lineEdit_12.text())))
            if self.lineEdit_13.isModified():
                self.ax.yaxis.set_minor_locator(MultipleLocator(
                    ast.literal_eval(self.lineEdit_13.text())))
            if self.lineEdit_14.isModified():
                self.ax.zaxis.set_minor_locator(MultipleLocator(
                    ast.literal_eval(self.lineEdit_14.text())))
        except Exception as e:
            QtWidgets.QMessageBox.warning(
                self.dialog, "错误", "坐标轴刻度输入有误，请确保输入的是数字，且主刻度间隔＞次刻度间隔")
            return
        self.set_all_settings()
        with open(self.config_path, "w+", encoding='utf-8') as f:
            self.config.write(f)

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

    def get_all_fonts(self):
        self.fonts = dict()
        for font in fontManager.ttflist:
            self.fonts.update({font.name: font.fname})
        self.comboBox.addItems(sorted(self.fonts.keys(), key=lambda x: x.lower()))
        self.comboBox_2.addItems(sorted(self.fonts.keys(), key=lambda x: x.lower()))
        self.comboBox_3.addItems(sorted(self.fonts.keys(), key=lambda x: x.lower()))

    def get_all_settings(self):
        # font
        if os.path.exists(self.config['font']['local_font_path']):
            self.comboBox.setCurrentText(self.config['font']['local_font'])
        if os.path.exists(self.config['font']['english_font_path']):
            self.comboBox_2.setCurrentText(self.config['font']['english_font'])
        if os.path.exists(self.config['font']['mix_font_path']):
            self.comboBox_3.setCurrentText(self.config['font']['mix_font'])
        # annotation
        self.lineEdit_16.setText(self.config['annotation']['axis_style'])
        self.comboBox_8.setCurrentText(self.config['annotation']['bg_color'])
        self.comboBox_12.setCurrentText(self.config['annotation']['border_color'])
        self.lineEdit_17.setText(self.config['annotation']['border'])
        self.lineEdit_19.setText(self.config['annotation']['offset'])
        self.lineEdit_20.setText(self.config['annotation']['arrow_width'])
        self.comboBox_9.setCurrentText(self.config['annotation']['arrow_color'])
        self.comboBox_10.setCurrentText(self.config['annotation']['arrow_shape'])
        self.lineEdit_21.setText(self.config['annotation']['text_size'])
        self.comboBox_11.setCurrentText(self.config['annotation']['text_color'])
        self.checkBox_2.setChecked(eval(self.config['annotation']['show_point']))
        self.checkBox_4.setChecked(eval(self.config['annotation']['show_text']))
        self.checkBox_5.setChecked(eval(self.config['annotation']['show_arrow']))
        # grid
        self.comboBox_4.setCurrentText(self.config['grid']['axis'])
        self.comboBox_5.setCurrentText(self.config['grid']['color'])
        self.comboBox_6.setCurrentText(self.config['grid']['which'])
        self.comboBox_7.setCurrentText(self.config['grid']['linestyle'])
        self.lineEdit_15.setText(self.config['grid']['linewidth'])
        # draw
        self.comboBox_13.setCurrentText(self.config['draw']['tab'])
        self.lineEdit_18.setText(self.config['draw']['width'])
        self.lineEdit_22.setText(self.config['draw']['height'])
        self.lineEdit_23.setText(self.config['draw']['dpi'])
        self.comboBox_14.setCurrentText(self.config['draw']['style'])

    def set_all_settings(self):
        # font
        self.config.set('font', 'local_font', self.comboBox.currentText())
        self.config.set('font', 'local_font_path', self.fonts[self.comboBox.currentText()])
        self.config.set('font', 'english_font', self.comboBox_2.currentText())
        self.config.set('font', 'english_font_path', self.fonts[self.comboBox_2.currentText()])
        self.config.set('font', 'mix_font', self.comboBox_3.currentText())
        self.config.set('font', 'mix_font_path', self.fonts[self.comboBox_3.currentText()])
        # annotation
        self.config['annotation']['axis_style'] = self.lineEdit_16.text()
        self.config['annotation']['bg_color'] = self.comboBox_8.currentText()
        self.config['annotation']['border_color'] = self.comboBox_12.currentText()
        self.config['annotation']['border'] = self.lineEdit_17.text()
        self.config['annotation']['offset'] = self.lineEdit_19.text()
        self.config['annotation']['arrow_width'] = self.lineEdit_20.text()
        self.config['annotation']['arrow_color'] = self.comboBox_9.currentText()
        self.config['annotation']['arrow_shape'] = self.comboBox_10.currentText()
        self.config['annotation']['text_size'] = self.lineEdit_21.text()
        self.config['annotation']['text_color'] = self.comboBox_11.currentText()
        self.config['annotation']['show_point'] = str(self.checkBox_2.isChecked())
        self.config['annotation']['show_text'] = str(self.checkBox_4.isChecked())
        self.config['annotation']['show_arrow'] = str(self.checkBox_5.isChecked())
        # grid
        self.config['grid']['axis'] = self.comboBox_4.currentText()
        self.config['grid']['color'] = self.comboBox_5.currentText()
        self.config['grid']['which'] = self.comboBox_6.currentText()
        self.config['grid']['linestyle'] = self.comboBox_7.currentText()
        self.config['grid']['linewidth'] = self.lineEdit_15.text()
        # draw
        self.config['draw']['tab'] = self.comboBox_13.currentText()
        self.config['draw']['width'] = self.lineEdit_18.text()
        self.config['draw']['height'] = self.lineEdit_22.text()
        self.config['draw']['dpi'] = self.lineEdit_23.text()
        self.config['draw']['style'] = self.comboBox_14.currentText()

    def set_combox_items(self):
        index = 0
        self.color_dict = dict()
        self.color_dict.update(mcolors.BASE_COLORS)
        self.color_dict.update(mcolors.TABLEAU_COLORS)
        self.color_dict.update(mcolors.CSS4_COLORS)
        self.color_dict.update(mcolors.XKCD_COLORS)
        color = QtGui.QColor()
        for color_name in self.color_dict.keys():
            self.comboBox_5.addItem(color_name)
            self.comboBox_8.addItem(color_name)
            self.comboBox_9.addItem(color_name)
            self.comboBox_11.addItem(color_name)
            self.comboBox_12.addItem(color_name)
            color.setNamedColor(mcolors.to_hex(color_name))
            self.comboBox_5.model().item(index).setBackground(color)
            self.comboBox_8.model().item(index).setBackground(color)
            self.comboBox_9.model().item(index).setBackground(color)
            self.comboBox_11.model().item(index).setBackground(color)
            self.comboBox_12.model().item(index).setBackground(color)
            index += 1
        self.comboBox_4.addItems(grid_axis)
        self.comboBox_6.addItems(grid_which)
        self.comboBox_7.addItems(linestyles)
        self.comboBox_10.addItems(arrowstyles)
        self.comboBox_13.addItems(draw_tabs)
        styles_list = plt.style.available
        styles_list.append('None')
        styles_list = sorted(styles_list, key=lambda x: x.lower())
        self.comboBox_14.addItems(styles_list)
