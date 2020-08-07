import os
import sys
import logging
import webbrowser
import time
import numpy as np
import pandas as pd
# 导入PyQt5模块
from PyQt5.QtGui import QCursor, QIcon, QPixmap
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

# 获取项目相关目录添加到path中
rootdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
uidir = rootdir + '\\ui'
# 把目录加入环境变量
sys.path.insert(0, rootdir)
sys.path.insert(0, uidir)

# 导入统计相关操作模块
from ui.stats.stats_base import Ui_Form as StatsBase_Ui_Form

# 定义日志输出格式
logging.basicConfig(format="%(asctime)s %(name)s:%(levelname)s:%(message)s", datefmt="%Y-%m-%d %H:%M:%S",
                    level=logging.INFO)




class StatsBaseForm(QWidget):
    """
    打开"统计--描述统计"窗口
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__ui = StatsBase_Ui_Form()
        self.__ui.setupUi(self)

    def keyPressEvent(self, e):
        """
        按键盘Escape退出当前窗口
        @param e:
        """
        if e.key() == Qt.Key_Escape:
            self.close()

    windowList = []

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)

    def get_data_columns(self):
        # 获取已经导入页面获取的数据集
        try:
            main_form = MyMainForm()
            columns = main_form.get_current_dataset_columns()
            for i in columns:
                self.__ui.listWidget_var.addItem(i)
        except:
            pass


# ====================================窗体测试程序============================
if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = StatsBaseForm()
    form.show()
    sys.exit(app.exec_())
