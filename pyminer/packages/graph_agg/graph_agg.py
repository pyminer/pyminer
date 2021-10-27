#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/21 14:07
# @Author  : Jiangchenglong
# @Site    : 
# @File    : graph_agg.py
# @Software: PyCharm
import sys,os
from PySide2 import QtWidgets
from IPython import get_ipython
import pyqtgraph as pg
from . import graph_agg_ui


# 一个简易的UI，地位和pmagg是等同的
class GraphAgg(QtWidgets.QMainWindow, graph_agg_ui.Ui_MainWindow):
    def __init__(self):
        super(GraphAgg, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)
        self.layout = QtWidgets.QVBoxLayout()
        self.widget = pg.GraphicsLayoutWidget()
        self.button = QtWidgets.QPushButton(text='这是GraphAgg的UI界面')
        self.layout.addWidget(self.widget)
        self.layout.addWidget(self.button)
        # self.setLayout(self.layout)
        self.gridLayout.addLayout(self.layout,0,0)

    def show(self):
        super(GraphAgg, self).show()
        ipython = get_ipython()
        if ipython is not None:
            ipython.magic("gui qt5")
            QtWidgets.QApplication(sys.argv).exec_()
            # 这里的写法是有问题的，会阻塞控制台，pmagg里面没有这句，窗口也不闪退，我对比了多次，还没找到原因。
        else:
            QtWidgets.QApplication(sys.argv).exec_()