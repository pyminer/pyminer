# -*- coding: utf-8 -*-
# @Time    : 2020/9/2 16:59
# @Author  : 别着急慢慢来
# @FileName: axes_control_manager.py.py

"""
负责对生成的ui类绑定事件，添加交互逻辑
"""
from .default_setting import Ui_Form
from PySide2 import QtWidgets, QtGui
from matplotlib.ticker import MultipleLocator
import ast
import os
from PySide2.QtWidgets import QFileDialog, QApplication
import subprocess
import re
import platform
import matplotlib.colors as mcolors
from .linestyles import *
from matplotlib.font_manager import fontManager
import matplotlib
import matplotlib.pyplot as plt
from PySide2.QtCore import QTranslator


class Ui_Form_Manager(Ui_Form):
    def __init__(self, parent):
        self.parent = parent
        if parent.current_language == 'en':
            lang = 'en_axes_control'
        if parent.current_language == 'zh_CN':
            lang = 'zh_CN_axes_control'
        self.ax = parent.current_subplot
        self.canvas = parent.canvas
        self.config = parent.config
        self.dialog = QtWidgets.QDialog()
        self.setupUi(self.dialog)
        self.retranslateUi(self.dialog)
        # 翻译家
        self.trans = QTranslator()
        lang_qm = os.path.join(os.path.dirname(self.parent.config_path), 'langs/{}.qm'.format(lang))
        self.trans.load(lang_qm)
        _app = QApplication.instance()  # 获取app实例
        _app.installTranslator(self.trans)  # 重新翻译主界面
        self.retranslateUi(self.dialog)
        self.init_gui()
        self.pushButton.clicked.connect(self.confirm_slot)
        self.pushButton_2.clicked.connect(self.cancel_slot)
        self.pushButton_3.clicked.connect(self.apply_slot)
        self.dialog.exec_()  # 初始化之后再执行

    def init_gui(self):
        self.get_all_fonts()
        self.set_combox_items()
        self.get_all_settings()

    def apply_slot(self):
        self.set_all_settings()
        self.parent.set_pickers()  # 设置之后，改变配置文件中的变量，更新字体等
        self.parent.read_all_settings()
        self.parent.set_all_fonts()
        self.canvas.draw()
        font=QtGui.QFont()
        font.setFamily(self.config.value('font/gui_font'))
        QtWidgets.QApplication.setFont(font)
        self.parent.set_gui_language()

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
        if os.path.exists(str(self.config.value('font/local_font_path'))):
            self.comboBox.setCurrentText(self.config.value('font/local_font'))
        if os.path.exists(str(self.config.value('font/english_font_path'))):
            self.comboBox_2.setCurrentText(self.config.value('font/english_font'))
        if os.path.exists(str(self.config.value('font/mix_font_path'))):
            self.comboBox_3.setCurrentText(self.config.value('font/mix_font'))
        # draw
        self.comboBox_14.setCurrentText(self.config.value('draw/style'))
        # gui font
        if self.config.value('font/gui_font'):
            self.fontComboBox.setCurrentText(self.config.value('font/gui_font'))
        # gui language
        self.comboBox_gui_language.setCurrentText(self.config.value('language/current_language'))
        self.comboBox_coord.setCurrentText(self.config.value('annotation/coord'))

    def set_all_settings(self):
        # font
        self.config.setValue('font/local_font',self.comboBox.currentText())
        self.config.setValue('font/local_font_path',self.fonts[self.comboBox.currentText()])
        self.config.setValue('font/english_font',self.comboBox_2.currentText())
        self.config.setValue('font/english_font_path',self.fonts[self.comboBox_2.currentText()])
        self.config.setValue('font/mix_font',self.comboBox_3.currentText())
        self.config.setValue('font/mix_font_path',self.fonts[self.comboBox_3.currentText()])
        # draw
        self.config.setValue('draw/style', self.comboBox_14.currentText())
        # gui font
        self.config.setValue('font/gui_font', self.fontComboBox.currentText())
        # gui language
        self.config.setValue('language/current_language', self.comboBox_gui_language.currentText())
        self.config.setValue('annotation/coord', self.comboBox_coord.currentText())

    def set_combox_items(self):
        styles_list = plt.style.available
        if 'default' not in styles_list:
            styles_list.append('default')
        styles_list = sorted(styles_list, key=lambda x: x.lower())
        self.comboBox_14.addItems(styles_list)
        self.comboBox_gui_language.addItems(languages)
