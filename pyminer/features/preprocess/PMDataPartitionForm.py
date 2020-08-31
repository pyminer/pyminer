#!/usr/bin/env python
# -*- coding:utf-8 -*-


import pandas as pd
from PyQt5.QtCore import pyqtSignal

from .PMDialog import PMDialog
from pyminer.ui.data.data_partition import Ui_Form as DataPartition_Ui_Form

class DataPartitionForm(PMDialog, DataPartition_Ui_Form):
    """
    打开"数据-数据分区"窗口
    """
    signal_data_change = pyqtSignal(str, dict, str, str, str, str, str)  # 自定义信号，用于修改数据

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Todo:待实现
        # self.current_dataset = pd.DataFrame()
        # self.current_dataset_name = ''
        #
        #
        # self.widget_part_2.hide()
        # self.widget_part_3.hide()
        # self.widget_part_4.hide()
        # self.widget_part_other.setVisible(False)


