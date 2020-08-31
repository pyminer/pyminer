#!/usr/bin/env python
# -*- coding:utf-8 -*-

import datetime
import numpy as np
import pandas as pd
import logging
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QMessageBox, QInputDialog, QLineEdit, QTableWidgetItem
from pandas.core.dtypes.common import is_string_dtype, is_numeric_dtype

from .PMDialog import PMDialog
from pyminer.ui.data.data_repace import Ui_Form as DataReplace_Ui_Form


class DataReplaceForm(PMDialog, DataReplace_Ui_Form):
    """
    打开"数据-内容替换"窗口
    """
    signal_data_change = pyqtSignal(str, dict, str, str, str, str, str)  # 自定义信号，用于修改数据
    signal_flush_console = pyqtSignal(str, str, str)  # 自定义信号，用于修改日志

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.current_dataset = pd.DataFrame()  # 当前数据集
        self.result_row = []
        self.result_col = []
        self.result_value = []
        self.current_dataset_name = ""
        self.data_manager = dict()
        self.result_dataset = pd.DataFrame()
        self.dataset_alter = pd.DataFrame()  # 修改后的数据集
        self.tableWidget_dataset.setVisible(False)

        self.pushButton_cancel.clicked.connect(self.close)
        self.tabWidget.currentChanged.connect(self.ui_init)
        self.pushButton_find.clicked.connect(self.data_find)
        self.pushButton_replace.clicked.connect(self.dataset_update)

    def ui_init(self):

        text = self.tabWidget.tabText(self.tabWidget.currentIndex())
        if text == "查找":
            self.pushButton_replace.setVisible(False)
        else:
            self.pushButton_replace.setVisible(True)

    def data_find(self):

        if self.tableWidget_dataset.isHidden():
            self.tableWidget_dataset.setVisible(True)

        if self.tabWidget.tabText(self.tabWidget.currentIndex()) == "查找":
            find_txt = self.lineEdit_find.text()
            if len(find_txt) == 0:
                QMessageBox.warning(self, '注意', '查找内容无效', QMessageBox.Yes)
                return

            self.result_dataset = ''
            self.result_col = []
            self.result_row = []
            self.result_value = []
            self.tableWidget_dataset.clearContents()

            data = self.current_dataset
            if self.comboBox_find_columns.currentText() == "全部列":
                for col in data.columns:
                    if is_string_dtype(data[col]):
                        if self.checkBox_find_cell.isChecked():
                            if self.checkBox_find_case.isChecked():  # 匹配单元格 且 匹配大小写
                                row = data[data[col].map(str) == find_txt].index.tolist()
                            else:  # 匹配单元格 且 不匹配大小写
                                row = data[data[col].map(str.lower) == find_txt.lower()].index.tolist()
                        else:
                            if self.checkBox_find_case.isChecked():  # 不匹配单元格 且 匹配大小写
                                row = data[data[col].map(str).str.contains(find_txt)].index.tolist()
                            else:  # 不匹配单元格 且 不匹配大小写
                                row = data[data[col].map(str.lower).str.contains(find_txt.lower())].index.tolist()

                    elif is_numeric_dtype(data[col]):
                        if self.checkBox_find_cell.isChecked():  # 匹配单元格
                            row = data[data[col].map(str) == find_txt].index.tolist()
                        else:  # 不匹配单元格
                            row = data[data[col].map(str).str.contains(find_txt)].index.tolist()

                    # 写入结果预览表
                    if len(row) > 0:
                        for i in row:
                            print("列{}，行{},值{}".format(col, i, data[col].iat[i]))
                            self.result_row.append(col)
                            self.result_col.append(i)
                            self.result_value.append(data[col].iat[i])
            else:
                col = self.comboBox_find_columns.currentText()
                if is_string_dtype(data[col]):
                    if self.checkBox_find_cell.isChecked():
                        if self.checkBox_find_case.isChecked():  # 匹配单元格 且 匹配大小写
                            row = data[data[col].map(str) == find_txt].index.tolist()
                        else:  # 匹配单元格 且 不匹配大小写
                            row = data[data[col].map(str.lower) == find_txt.lower()].index.tolist()
                    else:
                        if self.checkBox_find_case.isChecked():  # 不匹配单元格 且 匹配大小写
                            row = data[data[col].map(str).str.contains(find_txt)].index.tolist()
                        else:  # 不匹配单元格 且 不匹配大小写
                            row = data[data[col].map(str.lower).str.contains(find_txt.lower())].index.tolist()
                elif is_numeric_dtype(data[col]):
                    if self.checkBox_find_cell.isChecked():  # 匹配单元格
                        row = data[data[col].map(str) == find_txt].index.tolist()
                    else:  # 不匹配单元格
                        row = data[data[col].map(str).str.contains(find_txt)].index.tolist()

                if len(row) > 0:
                    for i in row:
                        print("列{}，行{},值{}".format(col, i, data[col].iat[i]))
                        self.result_row.append(col)
                        self.result_col.append(i)
                        self.result_value.append(data[col].iat[i])

            self.result_dataset = pd.DataFrame({'列': self.result_row, '行': self.result_col, '值': self.result_value})
            self.flush_preview(self.result_dataset)
        else:
            find_txt = self.lineEdit_replace_find.text()
            if len(find_txt) == 0:
                QMessageBox.warning(self, '注意', '查找内容无效', QMessageBox.Yes)
                return

            self.result_dataset = ''
            self.result_col = []
            self.result_row = []
            self.result_value = []
            self.tableWidget_dataset.clearContents()

            data = self.current_dataset
            if self.comboBox_replace_columns.currentText() == "全部列":
                for col in data.columns:
                    if is_string_dtype(data[col]):
                        if self.checkBox_replace_cell.isChecked():
                            if self.checkBox_replace_case.isChecked():  # 匹配单元格 且 匹配大小写
                                row = data[data[col].map(str) == find_txt].index.tolist()
                            else:  # 匹配单元格 且 不匹配大小写
                                row = data[data[col].map(str.lower) == find_txt.lower()].index.tolist()
                        else:
                            if self.checkBox_replace_case.isChecked():  # 不匹配单元格 且 匹配大小写
                                row = data[data[col].map(str).str.contains(find_txt)].index.tolist()
                            else:  # 不匹配单元格 且 不匹配大小写
                                row = data[data[col].map(str.lower).str.contains(find_txt.lower())].index.tolist()
                    elif is_numeric_dtype(data[col]):
                        if self.checkBox_replace_cell.isChecked():  # 匹配单元格
                            row = data[data[col].map(str) == find_txt].index.tolist()
                        else:  # 不匹配单元格
                            row = data[data[col].map(str).str.contains(find_txt)].index.tolist()

                    # 写入结果预览表
                    if len(row) > 0:
                        for i in row:
                            print("列{}，行{},值{}".format(col, i, data[col].iat[i]))
                            self.result_row.append(col)
                            self.result_col.append(i)
                            self.result_value.append(data[col].iat[i])
            else:
                col = self.comboBox_replace_columns.currentText()
                if is_string_dtype(data[col]):
                    if self.checkBox_replace_cell.isChecked():
                        if self.checkBox_replace_case.isChecked():  # 匹配单元格 且 匹配大小写
                            row = data[data[col].map(str) == find_txt].index.tolist()
                        else:  # 匹配单元格 且 不匹配大小写
                            row = data[data[col].map(str.lower) == find_txt.lower()].index.tolist()
                    else:
                        if self.checkBox_replace_case.isChecked():  # 不匹配单元格 且 匹配大小写
                            row = data[data[col].map(str).str.contains(find_txt)].index.tolist()
                        else:  # 不匹配单元格 且 不匹配大小写
                            row = data[data[col].map(str.lower).str.contains(find_txt.lower())].index.tolist()
                elif is_numeric_dtype(data[col]):
                    if self.checkBox_replace_cell.isChecked():  # 匹配单元格
                        row = data[data[col].map(str) == find_txt].index.tolist()
                    else:  # 不匹配单元格
                        row = data[data[col].map(str).str.contains(find_txt)].index.tolist()

                if len(row) > 0:
                    for i in row:
                        print("列{}，行{},值{}".format(col, i, data[col].iat[i]))
                        self.result_row.append(col)
                        self.result_col.append(i)
                        self.result_value.append(data[col].iat[i])

            self.result_dataset = pd.DataFrame({'列': self.result_row, '行': self.result_col, '值': self.result_value})
            self.flush_preview(self.result_dataset)

    def data_replace(self):
        if self.tableWidget_dataset.isHidden():
            self.tableWidget_dataset.setVisible(True)

        replace_txt = self.lineEdit_replace.text()
        self.dataset_alter = self.current_dataset.copy()
        if len(self.result_dataset) > 0:
            for col in self.result_dataset['列']:
                for row in self.result_dataset['行']:
                    content = self.dataset_alter[col].iat[row]
                    print('content:', content)
                    self.dataset_alter[col].iat[row] = replace_txt

        print('替换完成')

    def dataset_update(self):
        self.data_replace()
        reply = QMessageBox.information(self, "注意", "是否覆盖原数据", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            logging.info("发射导入数据信号")
            if len(self.dataset_alter) > 0:
                property_dic = self.data_manager.get_info(self.current_dataset_name)
                create_time = property_dic.get('create_time')
                update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 数据更新时间
                path = property_dic.get('path')
                file_size = property_dic.get('file_size')
                remarks = ''
                self.signal_data_change.emit(self.current_dataset_name,
                                             self.dataset_alter.to_dict(),
                                             path,
                                             create_time,
                                             update_time,
                                             remarks,
                                             file_size)  # 发射信号
                self.close()
            else:
                logging.info("导入数据信号发射失败")
                self.close()
        else:
            self.dataset_save()

    def dataset_save(self):
        default_name = self.current_dataset_name.split('.')[0] + '_replace'
        dataset_name, ok = QInputDialog.getText(self, "数据集名称", "保存后的数据集名称:", QLineEdit.Normal, default_name)
        if ok and (len(dataset_name) != 0):
            logging.info("发射导入数据信号")
            if len(self.dataset_alter) > 0:
                property_dic = self.data_manager.get_info(self.current_dataset_name)
                create_time = property_dic.get('create_time')
                update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 数据更新时间
                path = property_dic.get('path')
                file_size = property_dic.get('file_size')
                remarks = ''
                self.signal_data_change.emit(dataset_name,
                                             self.dataset_alter.to_dict(),
                                             path,
                                             create_time,
                                             update_time,
                                             remarks,
                                             file_size)  # 发射信号
                self.close()
            else:
                logging.info("导入数据信号发射失败")
                self.close()

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
