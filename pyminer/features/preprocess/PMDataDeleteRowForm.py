#!/usr/bin/env python
# -*- coding:utf-8 -*-


from .PMDialog import PMDialog
from pyminer.ui.data.data_delete_row import Ui_Form as DataDeleteRow_Ui_Form  # 数据删除行


class DataDeleteRowForm(PMDialog, DataDeleteRow_Ui_Form):
    """
    打开"数据-删除行"窗口
    """

    def __init__(self):
        super().__init__()
        self.setupUi(self)
