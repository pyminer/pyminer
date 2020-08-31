#!/usr/bin/env python
# -*- coding:utf-8 -*-


from .PMDialog import PMDialog
from pyminer.ui.data.data_column_encode import Ui_Form as DataColumnEncode_Ui_Form


class DataColumnEncodeForm(PMDialog, DataColumnEncode_Ui_Form):
    """
    打开"数据编码"窗口
    """

    def __init__(self):
        super().__init__()
        self.setupUi(self)

