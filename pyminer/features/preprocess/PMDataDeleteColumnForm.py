#!/usr/bin/env python
# -*- coding:utf-8 -*-


from .PMDialog import PMDialog

from pyminer.ui.data.data_delete_column import Ui_Form as DataDeleteColumn_Ui_Form

class DataDeleteColumnForm(PMDialog, DataDeleteColumn_Ui_Form):
    """
    打开"数据-删除列"窗口
    """

    def __init__(self):
        super().__init__()
        self.setupUi(self)

