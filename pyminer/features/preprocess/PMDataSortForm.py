#!/usr/bin/env python
# -*- coding:utf-8 -*-

from .PMDialog import PMDialog
from pyminer.ui.data.data_sort import Ui_Form as DataSort_Ui_Form

class DataSortForm(PMDialog, DataSort_Ui_Form):
    """
    打开数据排序窗口
    """

    def __init__(self):
        super().__init__()
        self.setupUi(self)
