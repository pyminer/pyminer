#!/usr/bin/env python
# -*- coding:utf-8 -*-


import datetime
import numpy as np
import pandas as pd
import logging
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QInputDialog, QLineEdit

from .PMDialog import PMDialog
from pyminer.ui.data.data_missing_value import Ui_Form as DataMissingValue_Ui_Form

class DataMissingValueForm(PMDialog, DataMissingValue_Ui_Form):
    """
    打开"数据-缺失值"窗口
    """
    signal_data_change = pyqtSignal(str, dict, str, str, str, str, str)  # 自定义信号，用于修改数据

    def __init__(self):
        super().__init__()
        self.setupUi(self)


        self.current_dataset = pd.DataFrame()  # 当前数据集
        self.current_dataset_name = ""
        self.all_dataset = dict()
        self.missing_dataset = pd.DataFrame()  # 处理后的缺失值数据
        self.missing_stat_dataset = pd.DataFrame()  # 缺失值统计数据

        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_ok.clicked.connect(self.dataset_missing)
        self.pushButton_help.clicked.connect(self.get_help)
        self.pushButton_save.clicked.connect(self.dataset_save)

        self.pushButton_add.clicked.connect(self.var_selected_add)
        self.pushButton_selected_add.clicked.connect(self.var_selected_add)
        self.pushButton_selected_up.clicked.connect(self.var_selected_up)
        self.pushButton_selected_down.clicked.connect(self.var_selected_down)
        self.pushButton_selected_del.clicked.connect(self.var_selected_del)
        self.pushButton_delete.clicked.connect(self.var_selected_del)

        self.listWidget_selected.itemChanged.connect(self.dataset_filter_column)



    def var_selected_del(self):
        current_row = self.listWidget_selected.currentRow()
        self.listWidget_selected.removeItemWidget(self.listWidget_selected.takeItem(current_row))

    def var_selected_up(self):
        var_list = []
        # 获取listwidget中条目数
        count = self.listWidget_selected.count()
        for i in range(count):
            var_list.append(self.listWidget_selected.item(i).text())
        row = self.listWidget_selected.currentRow()
        print("row:", row)
        temp = var_list[row]
        var_list[row] = var_list[row - 1]
        var_list[row - 1] = temp
        # 清空当前listWidget
        self.listWidget_selected.clear()
        # 重新添加新项
        self.listWidget_selected.addItems(var_list)

    def var_selected_down(self):
        var_list = []
        # 获取listwidget中条目数
        count = self.listWidget_selected.count()
        for i in range(count):
            var_list.append(self.listWidget_selected.item(i).text())
        row = self.listWidget_selected.currentRow()
        print("row:", row)
        temp = var_list[row]
        var_list[row] = var_list[row + 1]
        var_list[row + 1] = temp
        # 清空当前listWidget
        self.listWidget_selected.clear()
        # 重新添加新项
        self.listWidget_selected.addItems(var_list)

    def var_selected_add(self):
        selected_item = self.listWidget_var.currentItem()
        if selected_item is None:
            QMessageBox.information(self, "注意", "请选择变量", QMessageBox.Yes)
        else:
            self.listWidget_selected.addItem(selected_item.text())

    def dataset_missing_stat(self):
        data = self.current_dataset.copy()
        col_name = list()
        dtype = list()
        total_cnt = list()
        missing = list()  # 缺失值数量
        missing_ratio = list()  # 缺失值占比
        unmissing = list()
        unmissing_ratio = list()  # 非缺失值占比
        for col in data.columns:
            col_name.append(col)
            dtype.append(str(data[col].dtypes))
            total_cnt.append(len(data))
            missing.append(data[col].isnull().sum())
            missing_ratio.append('{0:.2%}'.format(data[col].isnull().sum() / len(data)))
            unmissing.append(len(data) - data[col].isnull().sum())
            unmissing_ratio.append('{0:.2%}'.format((len(data) - data[col].isnull().sum()) / len(data)))

        self.missing_stat_dataset = pd.DataFrame({"名称": col_name, "类型": dtype, "总数": total_cnt,
                                                  "缺失值数量": missing,
                                                  "缺失值占比": missing_ratio,
                                                  "非缺失值数量": unmissing,
                                                  "非缺失值占比": unmissing_ratio})
        self.flush_preview(self.missing_stat_dataset)

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

    def dataset_missing(self):
        from pandas.api.types import is_numeric_dtype
        from pandas.api.types import is_float_dtype
        from pandas.api.types import is_string_dtype

        from sklearn.impute import SimpleImputer
        data = self.current_dataset.copy()
        columns = []
        for i in range(self.listWidget_selected.count()):
            columns.append(self.listWidget_selected.item(i).text())

        if self.radioButton_mean.isChecked():  # 均值填充缺失值
            for col in columns:
                if is_numeric_dtype(data[col]):
                    data.fillna(data[col].mean(), inplace=True)
                    print(data)
                else:
                    print("不能用平均值填充非数值列")
        elif self.radioButton_median.isChecked():  # 中位数填充缺失值
            for col in columns:
                if is_numeric_dtype(data[col]):
                    data.fillna(data[col].median(), inplace=True)
                    print(data)
                else:
                    print("不能用中位数值填充非数值列")
        elif self.radioButton_mode.isChecked():  # 众数填充缺失值
            for col in columns:
                data.fillna(list(data[col].mode())[0], inplace=True)
                print(data)
        elif self.radioButton_drop.isChecked():  # 删除有缺失值的行
            data.dropna(axis=0, subset=columns, inplace=True)
            print(data)
        elif self.radioButton_drop_col.isChecked():  # 删除全部为缺失值的列
            data.dropna(axis=1, how="all", inplace=True)
            print(data)
        elif self.radioButton_replace.isChecked():  # 替换缺失值
            data.fillna(self.lineEdit_missing_replace.text().strip(), inplace=True)
            print(data)
        elif self.radioButton_drop_ratio.isChecked():  # 替换缺失值
            ratio = self.doubleSpinBox_missing_ratio.value()
            missing_ratio = data.isnull().sum() / len(data) >= ratio
            missing_column = list(missing_ratio[missing_ratio.values == True].index)
            for col in missing_column:
                del data[col]
            print(data)
        self.missing_dataset = data  # 保存数据
        self.dataset_update()  # 更新数据

    def dataset_filter_column(self):
        var_list = []
        # 获取listwidget中条目数
        count = self.listWidget_selected.count()
        for i in range(count):
            var_list.append(self.listWidget_selected.item(i).text())
        self.current_dataset = self.current_dataset.loc[:, var_list]  # 筛选列

    def dataset_update(self):
        logging.info("发射导入数据信号")
        if len(self.missing_dataset) > 0:
            create_time = self.all_dataset.get(self.current_dataset_name + '.create_time')
            update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 数据更新时间
            path = self.all_dataset.get(self.current_dataset_name + '.path')
            file_size = self.all_dataset.get(self.current_dataset_name + '.file_size')
            remarks = ''
            self.signal_data_change.emit(self.current_dataset_name, self.missing_dataset.to_dict(), path,
                                         create_time, update_time, remarks, file_size)  # 发射信号
            self.close()
        else:
            logging.info("导入数据信号发射失败")
            self.close()

    def dataset_save(self):
        print(self.current_dataset_name)
        default_name = self.current_dataset_name.split('.')[0] + '_missing'
        print(default_name)
        dataset_name, ok = QInputDialog.getText(self, "数据集名称", "保存后的数据集名称:", QLineEdit.Normal, default_name)
        if ok and (len(dataset_name) != 0):
            logging.info("发射导入数据信号")
            if len(self.missing_dataset) > 0:
                create_time = self.all_dataset.get(self.current_dataset_name + '.create_time')
                update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 数据更新时间
                path = self.all_dataset.get(self.current_dataset_name + '.path')
                file_size = self.all_dataset.get(self.current_dataset_name + '.file_size')
                remarks = ''
                self.signal_data_change.emit(dataset_name, self.missing_dataset.to_dict(), path,
                                             create_time, update_time, remarks, file_size)  # 发射信号
                self.close()
            else:
                logging.info("导入数据信号发射失败")
                self.close()
