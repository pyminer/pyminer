#!/usr/bin/env python
# -*- coding:utf-8 -*-


import numpy as np
import pandas as pd

from PyQt5.QtWidgets import QTableWidgetItem, QInputDialog
from PyQt5.QtCore import Qt

from pyminer.ui.data.data_info import Ui_Form as DataInfo_Ui_Form  # 数据信息
from .PMDialog import PMDialog


class DataInfoForm(PMDialog, DataInfo_Ui_Form):
    """
    打开"数据-数据信息"
    """

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.data_manager = dict()
        self.all_dataset_name = list()

        self.current_dataset_name = ''  # 当前数据集名称
        self.info = pd.DataFrame()

        # 更新数据
        self.pushButton_ok.clicked.connect(self.close)
        self.pushButton_cancel.clicked.connect(self.close)
        # 帮助
        self.pushButton_help.clicked.connect(self.get_help)
        # 修改当前数据集
        self.toolButton_dataset_name.clicked.connect(self.change_dataset_name)
        # 更新当前数据信息
        self.lineEdit_dataset_name.textChanged.connect(self.change_dataset_info)

    def info_init(self):
        # print(self.info) #None
        # print(type(self.info)) #<class 'NoneType'>
        # print(isinstance(self.info,pd.DataFrame)) # py3.7 :False ??
        if self.info is not None:
            input_table_rows = self.info.head(100).shape[0]
            input_table_colunms = self.info.shape[1]
            input_table_header = self.info.columns.values.tolist()
            self.tableWidget.setColumnCount(input_table_colunms)
            self.tableWidget.setRowCount(input_table_rows)
            self.tableWidget.setHorizontalHeaderLabels(input_table_header)

            # 数据预览窗口
            for i in range(input_table_rows):
                input_table_rows_values = self.info.iloc[[i]]
                input_table_rows_values_array = np.array(input_table_rows_values)
                input_table_rows_values_list = input_table_rows_values_array.tolist()[0]
                for j in range(input_table_colunms):
                    input_table_items_list = input_table_rows_values_list[j]

                    input_table_items = str(input_table_items_list)
                    newItem = QTableWidgetItem(input_table_items)
                    newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.tableWidget.setItem(i, j, newItem)

    def change_dataset_name(self):
        # 修改当前数据集名称
        items = self.all_dataset_name
        item, ok = QInputDialog.getItem(self, "修改数据集", "请选择要查看的数据集", items, 0, False)
        if ok and item:
            self.current_dataset_name = item
            self.lineEdit_dataset_name.setText(item)

    def change_dataset_info(self):
        # 修改当前数据集的数据信息
        property_dic = self.data_manager.get_info(self.current_dataset_name)
        self.lineEdit_path.setText(property_dic.get("path"))
        self.lineEdit_row.setText(property_dic.get("row"))
        self.lineEdit_col.setText(property_dic.get('col'))
        self.lineEdit_file_size.setText(property_dic.get("file_size"))
        self.lineEdit_memory_usage.setText(property_dic.get("memory_usage"))
        self.lineEdit_create_time.setText(property_dic.get("create_time"))
        self.lineEdit_update_time.setText(property_dic.get("update_time"))
        self.info = property_dic.get("info")
        self.info_init()
