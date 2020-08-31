#!/usr/bin/env python
# -*- coding:utf-8 -*-




from pyminer.ui.data.data_filter import Ui_Form as DataFilter_Ui_Form  # 数据筛选
from .PMDialog import PMDialog

class DataFilterForm(PMDialog, DataFilter_Ui_Form):
    """
    打开"数据-筛选"窗口
    """
    def __init__(self):
        super().__init__()
        self.setupUi(self)

