#!/usr/bin/env python
# -*- coding:utf-8 -*-

from .PMDialog import PMDialog
from pyminer.ui.data.data_standard import Ui_Form as DataStandard_Ui_Form

class DataStandardForm(PMDialog, DataStandard_Ui_Form):
    """
    打开数据标准化窗口
    """

    def __init__(self):
        super().__init__()
        self.setupUi(self)

