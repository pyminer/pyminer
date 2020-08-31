#!/usr/bin/env python
# -*- coding:utf-8 -*-


import datetime

import numpy as np
import pandas as pd
import logging
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QAbstractItemView, QMessageBox, QDialog, QInputDialog

from .PMDialog import PMDialog
from pyminer.ui.data.data_merge_horizontal import Ui_Form as DataMergeHorizontal_Ui_Form

class DataMergeHorizontalForm(PMDialog, DataMergeHorizontal_Ui_Form):
    """
    打开"数据-横向合并"窗口
    """
    signal_data_change = pyqtSignal(str, dict, str, str, str, str, str)  # 自定义信号，用于修改数据

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.center()

        self.current_dataset_name = ""
        self.all_dataset = {}  # 定义“全部数据集”为一个字典
        self.dataset_alter = pd.DataFrame()

        self.listWidget_dataset.setSelectionMode(QAbstractItemView.ExtendedSelection)  # 设置为按住ctrl可以多选
        self.listWidget_start.setAcceptDrops(True)
        self.listWidget_append.setAcceptDrops(True)
        self.listWidget_start.itemChanged.connect(self.slot_listWidget_start_change)

        self.pushButton_help.clicked.connect(self.get_help)
        self.pushButton_ok.clicked.connect(self.dataset_update)
        self.pushButton_save.clicked.connect(self.dataset_save)
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_start_add.clicked.connect(self.dataset_start_add)
        self.pushButton_start_up.clicked.connect(self.dataset_start_up)
        self.pushButton_start_down.clicked.connect(self.dataset_start_down)
        self.pushButton_start_del.clicked.connect(self.dataset_start_del)
        self.pushButton_append_add.clicked.connect(self.dataset_append_add)
        self.pushButton_append_up.clicked.connect(self.dataset_append_up)
        self.pushButton_append_down.clicked.connect(self.dataset_append_down)
        self.pushButton_append_del.clicked.connect(self.dataset_append_del)

    def slot_listWidget_start_change(self):
        self.current_dataset_name = self.listWidget_start.item(0).text()

    def dataset_start_del(self):
        current_row = self.listWidget_start.currentRow()
        self.listWidget_start.removeItemWidget(self.listWidget_start.takeItem(current_row))

    def dataset_append_add(self):
        selected_item = self.listWidget_dataset.currentItem()
        if selected_item is None:
            QMessageBox.information(self, "注意", "请选择合并数据集", QMessageBox.Yes)
        elif selected_item.text() != self.listWidget_start.item(0).text():
            current_item = self.listWidget_dataset.currentItem()
            self.listWidget_append.addItem(current_item.text())
        elif selected_item.text() == self.listWidget_start.item(0).text():
            QMessageBox.information(self, "注意", "合并数据集不能与起始数据集同名", QMessageBox.Yes)
        else:
            selected = self.listWidget_dataset.selectedItems()
            dataset_start_text = self.listWidget_dataset.currentItem().text()
            for item in selected:
                if item.text() != dataset_start_text:
                    self.listWidget_append.addItem(item.text())

    def dataset_append_del(self):
        current_row = self.listWidget_append.currentRow()
        self.listWidget_append.removeItemWidget(self.listWidget_append.takeItem(current_row))

    def dataset_append_up(self):
        var_list = []
        # 获取listwidget中条目数
        count = self.listWidget_append.count()
        for i in range(count):
            var_list.append(self.listWidget_append.item(i).text())
        row = self.listWidget_append.currentRow()
        print("row:", row)
        temp = var_list[row]
        var_list[row] = var_list[row - 1]
        var_list[row - 1] = temp
        # 清空当前listWidget
        self.listWidget_append.clear()
        # 重新添加新项
        self.listWidget_append.addItems(var_list)

    def dataset_append_down(self):
        var_list = []
        # 获取listwidget中条目数
        count = self.listWidget_append.count()
        for i in range(count):
            var_list.append(self.listWidget_append.item(i).text())
        row = self.listWidget_append.currentRow()
        print("row:", row)
        temp = var_list[row]
        var_list[row] = var_list[row + 1]
        var_list[row + 1] = temp
        # 清空当前listWidget
        self.listWidget_append.clear()
        # 重新添加新项
        self.listWidget_append.addItems(var_list)

    def dataset_start_add(self):
        selected_item = self.listWidget_dataset.currentItem()
        start_item = self.listWidget_start.item(0)
        if selected_item is None:
            QMessageBox.information(self, "注意", "请先选择起始数据集", QMessageBox.Yes)
        elif start_item is not None:
            if selected_item.text() == self.listWidget_start.item(0).text():
                QMessageBox.information(self, "注意", "起始数据集已存在", QMessageBox.Yes)
            else:
                self.listWidget_start.item(0).setText(selected_item.text())
        elif start_item is None:
            self.listWidget_start.addItem(selected_item.text())
        else:
            self.listWidget_start.removeItemWidget(self.listWidget_start.takeItem(0))
            self.listWidget_start.addItem(selected_item.text())

    def dataset_start_up(self):
        var_list = []
        # 获取listwidget中条目数
        count = self.listWidget_start.count()
        for i in range(count):
            var_list.append(self.listWidget_start.item(i).text())
        row = self.listWidget_start.currentRow()
        print("row:", row)
        temp = var_list[row]
        var_list[row] = var_list[row - 1]
        var_list[row - 1] = temp
        # 清空当前listWidget
        self.listWidget_start.clear()
        # 重新添加新项
        self.listWidget_start.addItems(var_list)

    def dataset_start_down(self):
        var_list = []
        # 获取listwidget中条目数
        count = self.listWidget_start.count()
        for i in range(count):
            var_list.append(self.listWidget_start.item(i).text())
        row = self.listWidget_start.currentRow()
        print("row:", row)
        temp = var_list[row]
        var_list[row] = var_list[row + 1]
        var_list[row + 1] = temp
        # 清空当前listWidget
        self.listWidget_start.clear()
        # 重新添加新项
        self.listWidget_start.addItems(var_list)

    def dataset_merge_horizontal(self):
        dataset_name = self.listWidget_start.item(0).text()  # dataset_name
        dataset_start = self.all_dataset.get(dataset_name)  # dataset_start
        dataset_merge_list_name = []  # 要合并的数据集名称
        dataset_merge_list = []  # 要合并的数据
        for i in range(self.listWidget_append.count()):  # 遍历列表n-1次
            if i < self.listWidget_append.count():
                dataset_name = self.listWidget_append.item(i).text()
                dataset_merge_list_name.append(dataset_name)
                dataset = self.all_dataset.get(self.listWidget_append.item(i).text()).copy()  # 避免修改原始数据
                dataset.columns = [x + "_" + dataset_name.split('.')[0] for x in dataset.columns]  # 为列名添加数据集后缀
                dataset_merge_list.append(dataset)

        if self.listWidget_start.count() < 1:
            QMessageBox.information(self, "注意", "请选择起始数据集", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        elif self.listWidget_append.count() < 1:
            QMessageBox.information(self, "注意", "请选择合并数据集", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        else:
            data_element = [dataset_start]
            for item in dataset_merge_list:
                data_element.append(item)
            self.dataset_alter = pd.concat(data_element, ignore_index=False, axis=1)  # 横向合并

    def dataset_update(self):
        self.dataset_merge_horizontal()
        reply = QMessageBox.information(self, "注意", "是否覆盖原数据", QMessageBox.Yes | QMessageBox.No)
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
            else:
                logging.info("导入数据信号发射失败")
                self.close()

    def dataset_save(self):
        self.dataset_merge_horizontal()
        default_name = self.current_dataset_name.split('.')[0] + '_h'
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
