#!/usr/bin/env python
# -*- coding:utf-8 -*-

from .PMDialog import PMDialog
from pyminer.ui.data.data_new_column import Ui_Form as DataNewColumn_Ui_Form

class DataNewColumnForm(PMDialog, DataNewColumn_Ui_Form):
    """
    新增列窗口
    """

    def __init__(self):
        super().__init__()
        self.setupUi(self)
