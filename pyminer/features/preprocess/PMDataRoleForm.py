#!/usr/bin/env python
# -*- coding:utf-8 -*-

import numpy as np
import pandas as pd
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem
from pandas.core.dtypes.common import is_float_dtype, is_numeric_dtype, is_string_dtype

from .PMDialog import PMDialog
from pyminer.ui.data.data_role import Ui_Form as DataRole_Ui_Form  # 数据角色

class DataRoleForm(PMDialog, DataRole_Ui_Form):
    """
    数据角色
    """
    signal_data_change = pyqtSignal(str, dict, str, str, str, str, str)  # 自定义信号，用于修改数据

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.center()

        self.current_dataset = pd.DataFrame()  # 当前数据集
        self.current_dataset_name = ""
        self.all_dataset = dict()
        self.filter_dataset = pd.DataFrame()  # 预览筛选后内容
        self.role_dataset = pd.DataFrame()  # 预览筛选后内容

        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_ok.clicked.connect(self.close)
        self.pushButton_help.clicked.connect(self.get_help)
        self.pushButton_export.clicked.connect(self.dataset_export)
        self.pushButton_find.clicked.connect(self.change_find)
        self.lineEdit_col_find.textChanged.connect(self.change_find)
        self.comboBox_columns.currentTextChanged.connect(self.change_column)

    def dataset_export(self):
        output_dir = '.'
        fileName_choose, filetype = QFileDialog.getSaveFileName(self,
                                                                "文件保存",
                                                                output_dir + r"/role.csv",  # 起始路径
                                                                "All Files (*);;CSV Files (*.csv)")

        if fileName_choose == "":
            print("\n取消选择")
            return
        else:
            self.role_dataset.to_csv(fileName_choose, index=False)
            print("\n保存成功！")

    def change_column(self):
        """
        查找指定列的数据角色
        """
        col = self.comboBox_columns.currentText()
        if col.strip() == "全部":
            self.flush_preview(self.role_dataset)
        else:
            self.filter_dataset = self.role_dataset[self.role_dataset['名称'] == col]
            self.flush_preview(self.filter_dataset)

    def change_find(self):
        """
        查找指定列的数据角色
        """
        find_text = self.lineEdit_col_find.text()
        self.filter_dataset = self.role_dataset[self.role_dataset['名称'].map(str.lower).str.contains(find_text.lower())]
        self.flush_preview(self.filter_dataset)

    def dataset_role(self):
        data = self.current_dataset
        col_name = list()
        dtype = list()
        width = list()
        precision = list()
        label = list()
        total_cnt = list()
        missing = list()
        measure = list()
        role = []
        for col in data.columns:
            col_name.append(col)
            dtype.append(str(data[col].dtypes))
            width.append(max([len(str(x)) for x in data[col]]))  # 最大宽度

            if is_float_dtype(data[col]):  # 最大精度
                precision.append(max([len(str(x).split('.')[1]) for x in data[col].dropna()]))
            else:
                precision.append("")
            label.append('')
            total_cnt.append(len(data[col]))
            missing.append(data[col].isnull().sum())

            if is_numeric_dtype(data[col]):
                measure.append("标度")
            elif is_string_dtype(data[col]):
                measure.append("名义")
            else:
                measure.append("")

            if col.lower() == "id":
                role.append("ID")
            elif col.lower() == "id" or col.lower() == "target":
                role.append("目标")
            else:
                role.append("输入")
        self.role_dataset = pd.DataFrame({"名称": col_name, "类型": dtype, "宽度": width,
                                          "精度": precision, "标签": label, "数量": total_cnt,
                                          "缺失值": missing, "测量": measure, "角色": role})

        self.flush_preview(self.role_dataset)

    def flush_preview(self, dataset):
        if any(dataset):
            input_table_rows = dataset.head(100).shape[0]
            input_table_colunms = dataset.shape[1]
            input_table_header = dataset.columns.values.tolist()
            self.tableWidget_dataset.setColumnCount(input_table_colunms)
            self.tableWidget_dataset.setRowCount(input_table_rows)
            self.tableWidget_dataset.setHorizontalHeaderLabels(input_table_header)

            # 数据预览窗口
            for i in range(input_table_rows):
                input_table_rows_values = dataset.iloc[[i]]
                input_table_rows_values_array = np.array(input_table_rows_values)
                input_table_rows_values_list = input_table_rows_values_array.tolist()[0]
                for j in range(input_table_colunms):
                    input_table_items_list = input_table_rows_values_list[j]

                    input_table_items = str(input_table_items_list)
                    newItem = QTableWidgetItem(input_table_items)
                    newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.tableWidget_dataset.setItem(i, j, newItem)

