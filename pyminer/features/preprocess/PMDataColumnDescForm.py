#!/usr/bin/env python
# -*- coding:utf-8 -*-


import datetime
import numpy as np
import pandas as pd
import logging

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMessageBox, QInputDialog, QTableWidgetItem

from pyminer.ui.data.data_column_desc import Ui_Form as Columns_desc_Ui_Form  # 数据列描述
from .PMDialog import PMDialog


class DataColumnDescForm(PMDialog, Columns_desc_Ui_Form):
    """
    打开"数据-列"窗口
    """
    signal_data_change = pyqtSignal(str, dict, str, str, str, str, str)  # 自定义信号，用于修改数据

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.current_dataset = pd.DataFrame()
        self.current_dataset_name = ''
        self.dataset_alter = pd.DataFrame()
        self.all_dataset = dict()

        self.listWidget_selected.itemChanged.connect(self.slot_var_change)

        self.pushButton_ok.clicked.connect(self.dataset_update)
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_help.clicked.connect(self.get_help)
        self.pushButton_save.clicked.connect(self.dataset_save)
        self.pushButton_selected_add_2.clicked.connect(self.var_selected_add)
        self.pushButton_selected_add.clicked.connect(self.var_selected_add)
        self.pushButton_selected_up.clicked.connect(self.var_selected_up)
        self.pushButton_selected_down.clicked.connect(self.var_selected_down)
        self.pushButton_selected_del.clicked.connect(self.var_selected_del)
        self.pushButton_group_add_2.clicked.connect(self.var_group_add)
        self.pushButton_group_add.clicked.connect(self.var_group_add)
        self.pushButton_group_up.clicked.connect(self.var_group_up)
        self.pushButton_group_down.clicked.connect(self.var_group_down)
        self.pushButton_group_del.clicked.connect(self.var_group_del)

    def slot_var_change(self):
        # 只允许查看一个变量的描述
        if self.listWidget_selected.count() > 0:
            QMessageBox.information(self, "注意", "只允许查看一个变量的描述", QMessageBox.Yes)

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
        current_item = self.listWidget_var.currentItem()
        selected_item = self.listWidget_selected.item(0)
        if current_item is None:
            QMessageBox.information(self, "注意", "请选择变量", QMessageBox.Yes)
        elif current_item is not None and selected_item is not None:
            if self.listWidget_var.currentItem().text() == self.listWidget_selected.item(0).text():
                QMessageBox.information(self, "注意", "变量已存在", QMessageBox.Yes)
            else:
                selected_item.setText(self.listWidget_var.currentItem().text())
        elif current_item is not None and selected_item is None:
            self.listWidget_selected.addItem(current_item.text())
        else:
            self.listWidget_selected.removeItemWidget(self.listWidget_selected.takeItem(0))
            self.listWidget_selected.addItem(current_item.text())

    def var_group_del(self):
        current_row = self.listWidget_group.currentRow()
        self.listWidget_group.removeItemWidget(self.listWidget_group.takeItem(current_row))

    def var_group_up(self):
        var_list = []
        # 获取listwidget中条目数
        count = self.listWidget_group.count()
        for i in range(count):
            var_list.append(self.listWidget_group.item(i).text())
        row = self.listWidget_group.currentRow()
        print("row:", row)
        temp = var_list[row]
        var_list[row] = var_list[row - 1]
        var_list[row - 1] = temp
        # 清空当前listWidget
        self.listWidget_group.clear()
        # 重新添加新项
        self.listWidget_group.addItems(var_list)

    def var_group_down(self):
        var_list = []
        # 获取listwidget中条目数
        count = self.listWidget_group.count()
        for i in range(count):
            var_list.append(self.listWidget_group.item(i).text())
        row = self.listWidget_group.currentRow()
        print("row:", row)
        temp = var_list[row]
        var_list[row] = var_list[row + 1]
        var_list[row + 1] = temp
        # 清空当前listWidget
        self.listWidget_group.clear()
        # 重新添加新项
        self.listWidget_group.addItems(var_list)

    def var_group_add(self):
        selected_item = self.listWidget_var.currentItem()
        if selected_item is None:
            QMessageBox.information(self, "注意", "请选择变量", QMessageBox.Yes)
        else:
            self.listWidget_group.addItem(selected_item.text())

    def dataset_column_desc(self):
        var = self.listWidget_selected.item(0).text()

        group_list = []  # 保存已选变量
        count = self.listWidget_group.count()  # 获取listwidget中条目数
        for i in range(count):
            group_list.append(self.listWidget_group.item(i).text())

        self.dataset_alter = self.current_dataset.copy().groupby(group_list)[var].describe().reset_index()
        if isinstance(self.dataset_alter, pd.DataFrame):
            self.flush_preview(self.dataset_alter)  # 预览列的基本描述
        else:
            self.dataset_alter = self.dataset_alter.to_frame()
            self.flush_preview(self.dataset_alter)

    def dataset_update(self):
        self.dataset_column_desc()
        self.tabWidget.setCurrentIndex(1)

    def dataset_save(self):
        self.dataset_column_desc()
        default_name = self.current_dataset_name.split('.')[0] + '_col'
        dataset_name, ok = QInputDialog.getText(self, "数据集名称", "保存后的数据集名称:", QLineEdit.Normal, default_name)
        if ok and (len(dataset_name) != 0):
            logging.info("发射导入数据信号")
            if len(self.dataset_alter) > 0:
                create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 数据更新时间
                path = ''
                file_size = ''
                remarks = ''
                self.signal_data_change.emit(dataset_name,
                                             self.dataset_alter.to_dict(),
                                             path,
                                             create_time,
                                             update_time,
                                             remarks,
                                             file_size)  # 发射信号
                logging.info("导入数据信号发射成功")
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

