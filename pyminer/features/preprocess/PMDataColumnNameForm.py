#!/usr/bin/env python
# -*- coding:utf-8 -*-

import datetime
import numpy as np
import pandas as pd
import logging
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QInputDialog, QLineEdit, QAbstractItemView

from .PMDialog import PMDialog
from pyminer.ui.data.data_column_name import Ui_Form as DataColumnName_Ui_Form

class DataColumnNameForm(PMDialog, DataColumnName_Ui_Form):
    """
    打开"数据-列名处理"窗口
    """
    signal_data_change = pyqtSignal(str, dict, str, str, str, str, str)  # 自定义信号，用于修改数据
    signal_flush_console = pyqtSignal(str, str, str)  # 自定义信号，用于修改日志

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.current_dataset = pd.DataFrame()  # 当前数据集
        self.dataset_edit = pd.DataFrame()
        self.dataset_alter = pd.DataFrame()  # 处理后数据
        self.current_dataset_name = ""
        self.all_dataset = dict()

        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_ok.clicked.connect(self.dataset_update)
        self.pushButton_help.clicked.connect(self.get_help)
        self.pushButton_save.clicked.connect(self.dataset_save)
        self.pushButton_add.clicked.connect(self.var_selected_add)
        self.pushButton_selected_add.clicked.connect(self.var_selected_add)
        self.pushButton_selected_up.clicked.connect(self.var_selected_up)
        self.pushButton_selected_down.clicked.connect(self.var_selected_down)
        self.pushButton_selected_del.clicked.connect(self.var_selected_del)
        self.pushButton_delete.clicked.connect(self.var_selected_del)
        self.pushButton_preview.clicked.connect(self.dataset_columns_preview)



    def var_selected_del(self):
        # 移除选中的item
        current_row = self.listWidget_selected.currentRow()
        self.listWidget_selected.removeItemWidget(self.listWidget_selected.takeItem(current_row))
        # 修改当前数据集
        var_list = []
        count = self.listWidget_selected.count()
        for i in range(count):
            var_list.append(self.listWidget_selected.item(i).text())
        self.dataset_edit = self.current_dataset[var_list]

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
            # 修改当前数据集
            var_list = []
            for i in range(self.listWidget_selected.count()):
                var_list.append(self.listWidget_selected.item(i).text())
            self.dataset_edit = self.current_dataset[var_list]

    def dataset_init(self):
        self.filter_dataset = self.current_dataset.head(10)
        self.tableWidget_dataset.setColumnCount(len(self.filter_dataset.columns))
        self.tableWidget_dataset.setRowCount(len(self.filter_dataset.index))
        self.tableWidget_dataset.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget_dataset.setHorizontalHeaderLabels(self.filter_dataset.columns.values.tolist())

        for i in range(len(self.filter_dataset.index)):
            for j in range(len(self.filter_dataset.columns)):
                self.tableWidget_dataset.setItem(i, j, QTableWidgetItem(str(self.filter_dataset.iat[i, j])))

        for x in range(self.tableWidget_dataset.columnCount()):
            headItem = self.tableWidget_dataset.horizontalHeaderItem(x)  # 获得水平方向表头的Item对象

            headItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

    def dataset_columns_preview(self):
        data = self.dataset_edit.copy()
        col = self.comboBox_columns.currentText()
        replace = self.lineEdit_replace.text().strip()
        prefix_add = self.lineEdit_prefix_add.text().strip()
        prefix_del = self.lineEdit_prefix_del.text().strip()
        suffix_add = self.lineEdit_suffix_add.text().strip()
        suffix_del = self.lineEdit_suffix_del.text().strip()

        def check_prefix(x, y):
            if x[:len(y)] == y:
                return x[len(y):]
            else:
                return x

        def check_suffix(x, y):
            if x[-len(y):] == y:
                return x[:-len(y)]
            else:
                return x

        if len(replace) > 0:
            if col == "变量列表":
                QMessageBox.information(self, "注意", "请选择变量", QMessageBox.Yes)
                return
            else:
                data.rename(columns={col: replace}, inplace=True)

        if self.checkBox_prefix_add.isChecked() and len(prefix_add) > 0:
            data.columns = [prefix_add + col for col in data.columns]
        if self.checkBox_prefix_del.isChecked() and len(prefix_del) > 0:
            data.columns = [check_prefix(col, prefix_del) for col in data.columns]
        if self.checkBox_suffix_add.isChecked() and len(suffix_add) > 0:
            data.columns = [col + suffix_add for col in data.columns]
        if self.checkBox_suffix_del.isChecked() and len(suffix_del) > 0:
            data.columns = [check_suffix(col, suffix_del) for col in data.columns]
        self.flush_preview(data)  # 刷新预览

    def dataset_columns(self):
        col = self.comboBox_columns.currentText()
        replace = self.lineEdit_replace.text().strip()
        prefix_add = self.lineEdit_prefix_add.text().strip()
        prefix_del = self.lineEdit_prefix_del.text().strip()
        suffix_add = self.lineEdit_suffix_add.text().strip()
        suffix_del = self.lineEdit_suffix_del.text().strip()

        def check_prefix(x, y):
            if x[:len(y)] == y:
                return x[len(y):]
            else:
                return x

        def check_suffix(x, y):
            if x[-len(y):] == y:
                return x[:-len(y)]
            else:
                return x

        if len(replace) > 0:
            if col == "变量列表":
                QMessageBox.information(self, "注意", "请选择变量", QMessageBox.Yes)
                return
            else:
                self.current_dataset.rename(columns={col: replace}, inplace=True)

        if self.checkBox_prefix_add.isChecked() and len(prefix_add) > 0:
            self.dataset_edit.columns = [prefix_add + col for col in self.dataset_edit.columns]
        if self.checkBox_prefix_del.isChecked() and len(prefix_del) > 0:
            self.dataset_edit.columns = [check_prefix(col, prefix_del) for col in self.dataset_edit.columns]
        if self.checkBox_suffix_add.isChecked() and len(suffix_add) > 0:
            self.dataset_edit.columns = [col + suffix_add for col in self.dataset_edit.columns]
        if self.checkBox_suffix_del.isChecked() and len(suffix_del) > 0:
            self.dataset_edit.columns = [check_suffix(col, suffix_del) for col in self.dataset_edit.columns]
        self.dataset_alter = self.dataset_edit.copy()
        self.flush_preview(self.dataset_edit)  # 刷新预览

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

    def dataset_update(self):
        self.dataset_columns()
        reply = QMessageBox.information(self, "注意", "是否覆盖原数据", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            logging.info("发射导入数据信号")
            if len(self.dataset_alter) > 0:
                create_time = self.all_dataset.get(self.current_dataset_name + '.create_time')
                update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 数据更新时间
                path = self.all_dataset.get(self.current_dataset_name + '.path')
                file_size = self.all_dataset.get(self.current_dataset_name + '.file_size')
                remarks = ''
                self.signal_data_change.emit(self.current_dataset_name,
                                             self.dataset_alter.to_dict(),
                                             path,
                                             create_time,
                                             update_time,
                                             remarks,
                                             file_size)  # 发射信号
                self.close()
                self.signal_flush_console.emit('info', '数据处理', '列名处理完成')
            else:
                logging.info("导入数据信号发射失败")
                self.signal_flush_console.emit('error', '数据处理', '列名处理失败')
                self.close()

    def dataset_save(self):
        self.dataset_columns()
        default_name = self.current_dataset_name.split('.')[0] + '_col'
        dataset_name, ok = QInputDialog.getText(self, "数据集名称", "保存后的数据集名称:", QLineEdit.Normal, default_name)
        if ok and (len(dataset_name) != 0):
            logging.info("发射导入数据信号")
            if len(self.dataset_alter) > 0:
                create_time = self.all_dataset.get(self.current_dataset_name + '.create_time')
                update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 数据更新时间
                path = self.all_dataset.get(self.current_dataset_name + '.path')
                file_size = self.all_dataset.get(self.current_dataset_name + '.file_size')
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
