import os
import sys
import logging
import webbrowser
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FC

# 导入PyQt5模块
from PyQt5.QtGui import QCursor, QIcon, QPixmap
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

# 导入功能组件
from data_miner.ui.plot.draw import Ui_Form as Plot_Ui_Form  # 数据可视化

# 定义日志输出格式
logging.basicConfig(format="%(asctime)s %(name)s:%(levelname)s:%(message)s", datefmt="%Y-%m-%d %H:%M:%S",
                    level=logging.INFO)

class PlotForm(QDialog,Plot_Ui_Form):
    """
    打开"数据可视化-画图"窗口
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.center()

        self.current_dataset=pd.DataFrame()
        self.dataset_all=dict()
        self.current_dataset_columns=list()

        # 解决无法显示中文
        plt.rcParams['font.sans-serif'] = ['SimHei']
        # 解决无法显示负号
        plt.rcParams['axes.unicode_minus'] = False



    def keyPressEvent(self, e):
        """
        按键盘Escape退出当前窗口
        @param e:
        """
        if e.key() == Qt.Key_Escape:
            self.close()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(int((screen.width() - size.width()) / 2),int((screen.height() - size.height()) / 2))

    #  ================================自定义槽函数=========================
    def get_help(self):
        """
        打开帮助页面
        """
        try:
            webbrowser.get('chrome').open_new_tab("http://www.py2cn.com")
        except Exception as e:
            webbrowser.open_new_tab("http://www.py2cn.com")






# ====================================窗体测试程序============================
if __name__ == '__main__':
    app = QApplication(sys.argv)
    #app.setStyle('Fusion')
    form = PlotForm()
    form.show()
    sys.exit(app.exec_())
